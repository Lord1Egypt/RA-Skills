#!/usr/bin/env python3
"""
worktree-codex 实时监控展板 v1.1
- 任务生命周期绑定：idle 保持页面，/register 追加 agent，/reload 重置
- 规则式解析：tokens / elapsed / diff stat / turns / retries / session_id / shell cmds
- 甘特图时间线（所有 agent 横向对比）
- 串行等效耗时 vs 实际并行耗时
- 点击卡片展开完整 log
- token/line 效率比
- step-3.5-flash：代码质量简评 + 弯路检测 + 最差 prompt 指出 + 改进 prompt 片段
"""

import argparse, glob, json, os, re, threading, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# ──────────────────────────────────────────────
# 全局状态
# ──────────────────────────────────────────────

class State:
    def __init__(self, log_paths):
        self.log_paths    = list(log_paths)
        self.mode         = "active"
        self.ai_triggered = False
        self.ai_cache     = {}
        self.lock         = threading.Lock()

    def reload(self, new_paths):
        with self.lock:
            self.log_paths    = list(new_paths)
            self.mode         = "active"
            self.ai_triggered = False
            self.ai_cache.clear()

    def register(self, log_path):
        with self.lock:
            if log_path not in self.log_paths:
                self.log_paths.append(log_path)
            self.mode         = "active"
            self.ai_triggered = False
            self.ai_cache.clear()

    def set_idle(self):
        with self.lock:
            self.mode = "idle"

STATE: State = None

# ──────────────────────────────────────────────
# 规则式 Log 解析
# ──────────────────────────────────────────────

def parse_log(path: str) -> dict:
    empty = {"status": "waiting", "name": Path(path).stem,
             "tokens": None, "tokens_in": None, "tokens_out": None,
             "model": "unknown", "start_t": None, "end_t": None,
             "elapsed": None, "last_line": "", "log": "",
             "has_warning": False, "path": path,
             "files_changed": None, "insertions": None, "deletions": None,
             "turns": None, "retries": 0, "session_id": None,
             "shell_cmds": [], "tok_per_line": None}
    try:
        text = Path(path).read_text(errors="replace")
    except FileNotFoundError:
        return empty

    name_m    = re.search(r"\] (\S+) starting", text)
    name      = name_m.group(1) if name_m else Path(path).stem
    exit_m    = re.search(r"\] \S+ codex exited with code (\d+)", text)
    exit_code = int(exit_m.group(1)) if exit_m else None

    tokens_m   = re.search(r"tokens used\s*\n([\d,]+)", text)
    tokens     = int(tokens_m.group(1).replace(",", "")) if tokens_m else None
    tin_m      = re.search(r"input[:\s]+([\d,]+)\s*token", text, re.I)
    tout_m     = re.search(r"output[:\s]+([\d,]+)\s*token", text, re.I)
    tokens_in  = int(tin_m.group(1).replace(",", "")) if tin_m else None
    tokens_out = int(tout_m.group(1).replace(",", "")) if tout_m else None

    model_m    = re.search(r"model=(\S+)", text)
    model      = model_m.group(1) if model_m else "unknown"

    sid_m      = re.search(r"session id:\s*(\S+)", text)
    session_id = sid_m.group(1) if sid_m else None

    if "AGENT_DONE" in text:
        status = "done" if exit_code == 0 else "failed"
    elif exit_m and exit_code != 0:
        status = "failed"
    elif "starting in" in text:
        status = "running"
    else:
        status = "waiting"

    times   = re.findall(r"\[(\d{2}:\d{2}:\d{2})\]", text)
    start_t = times[0] if times else None
    end_t   = times[-1] if len(times) > 1 else None

    elapsed = None
    if start_t and end_t and start_t != end_t:
        def to_sec(t):
            h, m, s = map(int, t.split(":"))
            return h * 3600 + m * 60 + s
        elapsed = to_sec(end_t) - to_sec(start_t)

    lines_list = [l.strip() for l in text.splitlines() if l.strip()]
    last_line  = lines_list[-1] if lines_list else ""
    has_warning = bool(re.search(r"warning:.*metadata.*not found", text, re.I))

    diff_m        = re.search(r"(\d+) file[s]? changed", text)
    ins_m         = re.search(r"(\d+) insertion", text)
    del_m         = re.search(r"(\d+) deletion", text)
    files_changed = int(diff_m.group(1)) if diff_m else None
    insertions    = int(ins_m.group(1)) if ins_m else None
    deletions     = int(del_m.group(1)) if del_m else None

    # turn 数（codex 每次工具调用算一轮，用 "shell_call" 行估算）
    shell_cmds = re.findall(r'(?:Running|Executing|shell_call)[:\s]+`([^`\n]{1,80})`', text)
    turns      = len(shell_cmds) if shell_cmds else None

    # 重试/重连次数
    retries = len(re.findall(r"Reconnecting\.\.\.", text))

    # token/line 效率比
    total_lines = (insertions or 0) + (deletions or 0)
    tok_per_line = round(tokens / total_lines, 1) if tokens and total_lines > 0 else None

    return {"name": name, "status": status, "exit_code": exit_code,
            "tokens": tokens, "tokens_in": tokens_in, "tokens_out": tokens_out,
            "model": model, "start_t": start_t, "end_t": end_t, "elapsed": elapsed,
            "last_line": last_line, "log": text,          # 全文，前端截取
            "has_warning": has_warning, "path": path,
            "files_changed": files_changed, "insertions": insertions, "deletions": deletions,
            "turns": turns, "retries": retries, "session_id": session_id,
            "shell_cmds": shell_cmds[:20],                # 最多20条
            "tok_per_line": tok_per_line}

def collect_stats(agents):
    total_tokens   = sum(a["tokens"] or 0 for a in agents)
    done    = sum(1 for a in agents if a["status"] == "done")
    fail    = sum(1 for a in agents if a["status"] == "failed")
    run     = sum(1 for a in agents if a["status"] == "running")
    wait    = sum(1 for a in agents if a["status"] == "waiting")
    elapsed_list   = [a["elapsed"] for a in agents if a.get("elapsed")]
    serial_equiv   = sum(elapsed_list) if elapsed_list else None
    actual_parallel = max(elapsed_list) if elapsed_list else None
    saved = round(serial_equiv - actual_parallel, 1) if serial_equiv and actual_parallel else None
    return {"total": len(agents), "done": done, "failed": fail,
            "running": run, "waiting": wait, "total_tokens": total_tokens,
            "all_done": (done + fail) == len(agents) and len(agents) > 0,
            "serial_equiv": serial_equiv, "actual_parallel": actual_parallel,
            "time_saved": saved}

# ──────────────────────────────────────────────
# step-3.5-flash 智能分析（后台线程，失败静默）
# ──────────────────────────────────────────────

def ai_analyze_async(agents):
    def _run():
        try:
            import httpx
            cfg = json.load(open(os.path.expanduser("~/.openclaw/openclaw.json")))
            key = cfg["env"]["OPENROUTER_API_KEY"]

            # 给每个 agent 提供：数据摘要 + log 尾部500字（让 step 看实际输出）
            agent_blocks = []
            for a in agents:
                elapsed_str  = f"{a['elapsed']}s" if a.get("elapsed") else "?"
                tpl_str      = f"{a['tok_per_line']} tok/line" if a.get("tok_per_line") else "?"
                diff_str     = f"+{a.get('insertions',0)}-{a.get('deletions',0)} lines" if a.get("files_changed") else "no diff"
                turns_str    = f"{a['turns']} shell calls" if a.get("turns") else "?"
                retries_str  = f"{a['retries']} retries" if a.get("retries") else "0 retries"
                log_tail     = a["log"][-150:].strip() if a.get("log") else "(no log)"
                agent_blocks.append(
                    f"=== {a['name']} ===\n"
                    f"status={a['status']} model={a['model']} tokens={a['tokens']} "
                    f"elapsed={elapsed_str} efficiency={tpl_str}\n"
                    f"diff={diff_str} turns={turns_str} {retries_str}"
                    + (" ⚠no-model-metadata" if a.get("has_warning") else "") + "\n"
                    f"log tail:\n{log_tail}"
                )

            prompt = "\n\n".join(agent_blocks)

            user_msg = (
                f"并行编码任务数据和log尾部：\n\n{prompt}\n\n"
                "直接输出bullet（不超过6条，每条含具体数字）：\n"
                "• token效率：最费/最省各谁，tok/line是否合理\n"
                "• 有无弯路（重试/反复修改）\n"
                "• 代码质量简评（从log tail判断）\n"
                "• 最差prompt是哪个agent，问题在哪\n"
                "• 1条改进prompt片段（代码块）"
            )
            print(f"[dashboard] AI prompt length: {len(user_msg)} chars")
            resp = httpx.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}",
                         "HTTP-Referer": "https://github.com/InuyashaYang"},
                json={"model": "stepfun/step-3.5-flash:free",
                      "messages": [
                          {"role": "system", "content":
                           "你是代码Agent效率审查员。只输出bullet list，不超过6条，每条含具体数字，无开场白。"},
                          {"role": "user", "content": user_msg}
                      ],
                      "max_tokens": 600},
                timeout=30,
            )
            resp_json = resp.json()
            content = (resp_json.get("choices", [{}])[0]
                       .get("message", {}).get("content") or "")
            result = content.strip() if content else "（step 返回空内容）"
            STATE.ai_cache["last"] = result
        except Exception as e:
            # 把 resp 原始内容也记下来，方便诊断
            try:
                raw = resp.text[:300]
            except Exception:
                raw = "(no response)"
            STATE.ai_cache["last"] = f"（AI 分析不可用：{e} | raw: {raw}）"

    threading.Thread(target=_run, daemon=True).start()

# ──────────────────────────────────────────────
# HTML
# ──────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>worktree-codex dashboard</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0d1117; color: #c9d1d9; font-family: 'Cascadia Code','Fira Code',monospace; font-size: 13px; }
header { background: #161b22; border-bottom: 1px solid #30363d; padding: 12px 20px; display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
header h1 { font-size: 15px; color: #58a6ff; white-space: nowrap; }
#overall { display: flex; gap: 10px; font-size: 12px; color: #8b949e; flex-wrap: wrap; align-items: center; }
#time-saved { font-size: 12px; color: #3fb950; font-weight: bold; }
#idle-banner { display: none; background: #21262d; color: #8b949e; font-size: 12px; padding: 6px 20px; border-bottom: 1px solid #30363d; }
.badge { padding: 2px 8px; border-radius: 10px; font-weight: bold; font-size: 11px; }
.badge.done    { background: #238636; color: #fff; }
.badge.running { background: #1f6feb; color: #fff; }
.badge.failed  { background: #da3633; color: #fff; }
.badge.waiting { background: #30363d; color: #8b949e; }
.badge.idle    { background: #30363d; color: #f0883e; }

/* 甘特图 */
#gantt { margin: 12px 16px 0; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; display: none; }
#gantt h3 { font-size: 12px; color: #58a6ff; margin-bottom: 10px; }
.gantt-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 11px; }
.gantt-label { width: 80px; text-align: right; color: #8b949e; flex-shrink: 0; }
.gantt-track { flex: 1; height: 16px; background: #21262d; border-radius: 3px; position: relative; }
.gantt-bar { position: absolute; height: 100%; border-radius: 3px; }
.gantt-bar.done    { background: #238636; }
.gantt-bar.running { background: #1f6feb; animation: pulse 1.5s infinite; }
.gantt-bar.failed  { background: #da3633; }
.gantt-time { width: 40px; font-size: 10px; color: #8b949e; }

/* 卡片 */
#agents { display: flex; flex-wrap: wrap; gap: 12px; padding: 16px; }
.card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; width: 340px; padding: 14px; transition: border-color .3s; cursor: pointer; }
.card:hover { border-color: #58a6ff44; }
.card.running { border-color: #1f6feb; }
.card.done    { border-color: #238636; }
.card.failed  { border-color: #da3633; }
.card-header  { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.card-name    { font-size: 14px; font-weight: bold; color: #e6edf3; }
.card-meta    { font-size: 11px; color: #8b949e; margin-bottom: 6px; }
.progress-bar { height: 3px; background: #30363d; border-radius: 2px; overflow: hidden; margin-bottom: 8px; }
.progress-fill { height: 100%; border-radius: 2px; transition: width .5s; }
.fill-running { background: #1f6feb; animation: pulse 1.5s infinite; }
.fill-done    { background: #238636; }
.fill-failed  { background: #da3633; }
.fill-waiting { background: #30363d; width: 0%; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.log-box { background: #0d1117; border: 1px solid #21262d; border-radius: 4px; padding: 8px; height: 60px; overflow-y: auto; font-size: 11px; color: #8b949e; white-space: pre-wrap; word-break: break-all; }
.stat-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.stat-chip { font-size: 11px; padding: 2px 7px; border-radius: 8px; background: #21262d; }
.chip-token  { color: #f0883e; }
.chip-diff   { color: #3fb950; }
.chip-time   { color: #8b949e; }
.chip-warn   { color: #d29922; }
.chip-turns  { color: #a371f7; }
.chip-eff    { color: #58a6ff; }

/* 展开 log 弹窗 */
#log-modal { display: none; position: fixed; inset: 0; background: #000a; z-index: 100; align-items: center; justify-content: center; }
#log-modal.open { display: flex; }
#log-modal-inner { background: #161b22; border: 1px solid #30363d; border-radius: 10px; width: 80vw; max-height: 80vh; display: flex; flex-direction: column; }
#log-modal-header { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid #30363d; }
#log-modal-title { font-size: 13px; font-weight: bold; color: #e6edf3; }
#log-modal-close { cursor: pointer; color: #8b949e; font-size: 18px; line-height: 1; }
#log-modal-body { flex: 1; overflow-y: auto; padding: 12px 16px; font-size: 11px; color: #8b949e; white-space: pre-wrap; word-break: break-all; }

/* AI 分析 */
#ai-box { margin: 0 16px 16px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px; display: none; }
#ai-box h3 { font-size: 12px; color: #58a6ff; margin-bottom: 8px; }
#ai-content { font-size: 12px; color: #c9d1d9; white-space: pre-wrap; line-height: 1.7; }
#ai-loading { color: #8b949e; font-size: 11px; }
footer { text-align: center; padding: 8px; color: #30363d; font-size: 11px; }
</style>
</head>
<body>
<header>
  <h1>⚡ worktree-codex</h1>
  <div id="overall"></div>
  <div id="time-saved"></div>
</header>
<div id="idle-banner">⏸ 任务已完成，等待下次任务… 页面不失效</div>
<div id="gantt"><h3>📊 时间线</h3><div id="gantt-rows"></div></div>
<div id="agents"></div>
<div id="ai-box">
  <h3>🤖 step-3.5-flash 分析</h3>
  <div id="ai-loading">正在分析…</div>
  <div id="ai-content" style="display:none"></div>
</div>
<footer>worktree-codex v1.1 · <span id="conn-status">connecting…</span></footer>

<!-- log 展开弹窗 -->
<div id="log-modal">
  <div id="log-modal-inner">
    <div id="log-modal-header">
      <span id="log-modal-title"></span>
      <span id="log-modal-close">✕</span>
    </div>
    <div id="log-modal-body"></div>
  </div>
</div>

<script>
const statusLabel = {done:'✅ done', running:'⚡ running', failed:'❌ failed', waiting:'⏳ waiting'};
const progressPct = {done:100, running:60, failed:100, waiting:0};
let allAgents = [];

function esc(t) {
  return String(t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── 甘特图 ──
function renderGantt(agents) {
  const finished = agents.filter(a => a.elapsed);
  if (!finished.length) { document.getElementById('gantt').style.display='none'; return; }
  document.getElementById('gantt').style.display='block';
  const maxE = Math.max(...finished.map(a => a.elapsed));
  document.getElementById('gantt-rows').innerHTML = agents.map(a => {
    if (!a.elapsed) return '';
    const pct = (a.elapsed / maxE * 100).toFixed(1);
    return `<div class="gantt-row">
      <span class="gantt-label">${esc(a.name)}</span>
      <div class="gantt-track">
        <div class="gantt-bar ${a.status}" style="width:${pct}%"></div>
      </div>
      <span class="gantt-time">${a.elapsed}s</span>
    </div>`;
  }).join('');
}

// ── 卡片 ──
function renderCard(a) {
  const pct   = progressPct[a.status] || 0;
  const time  = (a.start_t && a.end_t && a.start_t !== a.end_t)
    ? `${a.start_t} → ${a.end_t}` : (a.start_t || '–');
  const chips = [];
  if (a.tokens)         chips.push(`<span class="stat-chip chip-token">🔥 ${a.tokens.toLocaleString()} tok</span>`);
  if (a.elapsed!=null)  chips.push(`<span class="stat-chip chip-time">⏱ ${a.elapsed}s</span>`);
  if (a.files_changed!=null) chips.push(`<span class="stat-chip chip-diff">📝 ${a.files_changed}f +${a.insertions??0} -${a.deletions??0}</span>`);
  if (a.tok_per_line!=null)  chips.push(`<span class="stat-chip chip-eff">⚡ ${a.tok_per_line} tok/ln</span>`);
  if (a.turns!=null)    chips.push(`<span class="stat-chip chip-turns">🔄 ${a.turns} calls</span>`);
  if (a.retries>0)      chips.push(`<span class="stat-chip chip-warn">↩ ${a.retries} retry</span>`);
  if (a.has_warning)    chips.push(`<span class="stat-chip chip-warn">⚠ no metadata</span>`);
  return `<div class="card ${a.status}" id="card-${a.name}" onclick="openLog('${a.name}')">
    <div class="card-header">
      <span class="card-name">${esc(a.name)}</span>
      <span class="badge ${a.status}">${statusLabel[a.status]||a.status}</span>
    </div>
    <div class="card-meta">${esc(a.model)} · ${esc(time)}</div>
    <div class="progress-bar"><div class="progress-fill fill-${a.status}" style="width:${pct}%"></div></div>
    <div class="log-box">${esc(a.last_line)}</div>
    <div class="stat-row">${chips.join('')}</div>
  </div>`;
}

// ── 顶栏 ──
function renderOverall(s, mode) {
  const idle = mode === 'idle' ? '<span class="badge idle">⏸ idle</span>' : '';
  return `<span>agents: <b>${s.total}</b></span>
    <span class="badge done">${s.done} done</span>
    <span class="badge running">${s.running} run</span>
    <span class="badge failed">${s.failed} fail</span>
    <span>🔥 ${s.total_tokens.toLocaleString()} tok</span>${idle}`;
}
function renderTimeSaved(s) {
  if (!s.time_saved || s.time_saved <= 0) return '';
  return `⚡ 并行节省 ${s.time_saved}s（串行需 ${s.serial_equiv}s，实际 ${s.actual_parallel}s）`;
}

// ── log 弹窗 ──
function openLog(name) {
  const a = allAgents.find(x => x.name === name);
  if (!a) return;
  document.getElementById('log-modal-title').textContent = `${name} — 完整 log`;
  document.getElementById('log-modal-body').textContent  = a.log || '(empty)';
  document.getElementById('log-modal').classList.add('open');
}
document.getElementById('log-modal-close').onclick = () =>
  document.getElementById('log-modal').classList.remove('open');
document.getElementById('log-modal').onclick = e => {
  if (e.target === document.getElementById('log-modal'))
    document.getElementById('log-modal').classList.remove('open');
};

// ── SSE ──
let es = null;
let lastMsgAt = Date.now();
const DEAD_TIMEOUT = 35000; // 35s 没收到任何消息则判定假死

// 定时检查假死
setInterval(() => {
  if (es && Date.now() - lastMsgAt > DEAD_TIMEOUT) {
    document.getElementById('conn-status').textContent = '⚠ heartbeat timeout, reconnecting…';
    connect();
  }
}, 5000);

function connect() {
  if (es) es.close();
  es = new EventSource('/events');
  lastMsgAt = Date.now();
  document.getElementById('conn-status').textContent = 'connected';

  es.onmessage = e => {
    lastMsgAt = Date.now();
    const data = JSON.parse(e.data);
    if (data.type === 'ping') {
      // 纯心跳，只更新时间戳，不渲染
      document.getElementById('conn-status').textContent = `✅ alive · ${new Date().toLocaleTimeString()}`;
      return;
    }
    if (data.type === 'agents') {
      allAgents = data.agents;
      document.getElementById('overall').innerHTML     = renderOverall(data.stats, data.mode);
      document.getElementById('time-saved').textContent = renderTimeSaved(data.stats);
      document.getElementById('idle-banner').style.display = data.mode==='idle' ? 'block' : 'none';
      renderGantt(data.agents);
      const c = document.getElementById('agents');
      data.agents.forEach(a => {
        const ex = document.getElementById('card-' + a.name);
        const html = renderCard(a);
        if (ex) ex.outerHTML = html; else c.insertAdjacentHTML('beforeend', html);
      });
    } else if (data.type === 'ai_waiting') {
      document.getElementById('ai-box').style.display = 'block';
      document.getElementById('ai-loading').style.display = 'block';
      document.getElementById('ai-content').style.display = 'none';
    } else if (data.type === 'ai_analysis') {
      document.getElementById('ai-box').style.display = 'block';
      document.getElementById('ai-loading').style.display = 'none';
      const ct = document.getElementById('ai-content');
      ct.style.display = 'block';
      ct.textContent = data.text;
    } else if (data.type === 'reload') {
      allAgents = [];
      document.getElementById('agents').innerHTML = '';
      document.getElementById('gantt-rows').innerHTML = '';
      document.getElementById('gantt').style.display = 'none';
      document.getElementById('ai-box').style.display = 'none';
      document.getElementById('idle-banner').style.display = 'none';
      document.getElementById('time-saved').textContent = '';
    }
  };
  es.onerror = () => {
    document.getElementById('conn-status').textContent = 'reconnecting…';
    setTimeout(connect, 3000);
  };
}
connect();
</script>
</body>
</html>"""

# ──────────────────────────────────────────────
# HTTP Handler
# ──────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        if self.path == "/":
            self._send(200, "text/html", HTML.encode())
        elif self.path == "/events":
            self._sse()
        elif self.path == "/state":
            with STATE.lock:
                agents = [parse_log(p) for p in STATE.log_paths]
                stats  = collect_stats(agents)
            body = json.dumps({"agents": agents, "stats": stats, "mode": STATE.mode}).encode()
            self._send(200, "application/json", body)
        else:
            self._send(404, "text/plain", b"not found")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
        except Exception as e:
            self._send(400, "application/json", json.dumps({"ok": False, "error": str(e)}).encode())
            return

        if self.path == "/reload":
            paths = []
            for p in data.get("logs", []):
                expanded = glob.glob(p)
                paths.extend(expanded if expanded else [p])
            STATE.reload(paths)
            print(f"[dashboard] reload: {len(paths)} log(s)")
            self._send(200, "application/json", json.dumps({"ok": True, "logs": paths}).encode())

        elif self.path == "/register":
            log_path = data.get("log", "")
            if not log_path:
                self._send(400, "application/json", json.dumps({"ok": False, "error": "missing log"}).encode())
                return
            STATE.register(log_path)
            print(f"[dashboard] register: {log_path} (total={len(STATE.log_paths)})")
            self._send(200, "application/json",
                       json.dumps({"ok": True, "log": log_path, "total": len(STATE.log_paths)}).encode())
        else:
            self._send(404, "text/plain", b"not found")

    def _send(self, code, ct, body):
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        def push(data: dict):
            msg = f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            self.wfile.write(msg.encode())
            self.wfile.flush()

        last_mode  = None
        last_ping  = time.time()
        PING_INTERVAL = 15  # 秒，前端超过 35s 没收到任何消息则重连

        try:
            while True:
                with STATE.lock:
                    mode     = STATE.mode
                    paths    = list(STATE.log_paths)
                    ai_cache = dict(STATE.ai_cache)

                if last_mode == "idle" and mode == "active":
                    push({"type": "reload"})
                last_mode = mode

                agents = [parse_log(p) for p in paths]
                stats  = collect_stats(agents)
                push({"type": "agents", "agents": agents, "stats": stats, "mode": mode})

                if mode == "active" and stats["all_done"] and not STATE.ai_triggered:
                    with STATE.lock:
                        STATE.ai_triggered = True
                    push({"type": "ai_waiting"})
                    ai_analyze_async(agents)
                    STATE.set_idle()

                if "last" in ai_cache:
                    push({"type": "ai_analysis", "text": ai_cache["last"]})
                    with STATE.lock:
                        STATE.ai_cache.clear()

                # 心跳：每 PING_INTERVAL 秒推一次 ping，防止连接假死
                now = time.time()
                if now - last_ping >= PING_INTERVAL:
                    push({"type": "ping", "ts": int(now)})
                    last_ping = now

                time.sleep(2 if mode == "idle" else 1)

        except (BrokenPipeError, ConnectionResetError):
            pass

# ──────────────────────────────────────────────
# 入口
# ──────────────────────────────────────────────

def main():
    global STATE
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", nargs="*", default=[],
                        help="log 文件路径（可选；agent 启动时自动 POST /register 追加）")
    parser.add_argument("--port", type=int, default=7789)
    args = parser.parse_args()

    paths = []
    for p in (args.logs or []):
        expanded = glob.glob(p)
        paths.extend(expanded if expanded else [p])

    STATE = State(paths)
    print(f"[dashboard] 展板地址: http://localhost:{args.port}")
    print(f"[dashboard] 初始 log: {len(paths)} 个")

    server = HTTPServer(("", args.port), Handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
