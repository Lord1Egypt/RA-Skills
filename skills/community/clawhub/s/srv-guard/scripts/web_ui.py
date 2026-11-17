#!/usr/bin/env python3
"""Local-only web UI (HTTPS) for authorized server scans and explicitly confirmed fixes.

运行: python scripts/web_ui.py [--host 127.0.0.1] [--port 8765] [--cert crt --key key] [--no-tls]
默认使用 HTTPS + 自动生成的自签名证书（仅绑定回环地址）。不要暴露到网络。
"""
import argparse
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TOKEN = secrets.token_urlsafe(32)
SESSIONS = {}
PENDING = {}
SESSION_TTL = 1800
CONFIRM_TTL = 300
LOCK = threading.Lock()
MAX_BODY = 64 * 1024
WORK_SLOTS = threading.Semaphore(2)


class BusyError(Exception):
    """并发扫描/修复超出容量。"""


class SudoAuthError(Exception):
    """sudo 密码错误或无 sudo 权限。"""


SUDO_FAILS = {"count": 0, "until": 0.0}
SUDO_MAX_FAILS = 3
SUDO_LOCK_SECONDS = 300


def _sudo_failed():
    SUDO_FAILS["count"] += 1
    if SUDO_FAILS["count"] >= SUDO_MAX_FAILS:
        SUDO_FAILS["until"] = time.time() + SUDO_LOCK_SECONDS
        SUDO_FAILS["count"] = 0


def _sudo_ok():
    SUDO_FAILS["count"] = 0
    SUDO_FAILS["until"] = 0.0


def run_sudo_script(name, args, password, timeout=180, allow_rc=()):
    """用 sudo 执行脚本：密码只经 stdin 交给 sudo，不进 argv、不进日志、不落盘。"""
    if SUDO_FAILS["until"] > time.time():
        raise SudoAuthError("sudo 失败次数过多，已临时锁定，请 5 分钟后再试")
    sudo = shutil.which("sudo")
    if not sudo:
        raise RuntimeError("本机未安装 sudo，无法提权执行；请改用 root 终端的 CLI 或配置 NOPASSWD")
    argv = [sudo, "-S", "-p", "", "--", sys.executable, str(SCRIPT_DIR / name), *args]
    try:
        p = subprocess.run(argv, input=str(password) + "\n", capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout, cwd=str(SKILL_ROOT))
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"sudo 执行超时（{timeout}s）")
    if p.returncode != 0 and p.returncode not in allow_rc:
        msg = (p.stderr or "").strip() or (p.stdout or "").strip() or f"{name} 执行失败"
        low = msg.lower()
        if "incorrect password" in low or "sorry, try again" in low or "no password" in low:
            _sudo_failed()
            raise SudoAuthError("sudo 密码错误，或该用户没有 sudo 权限")
        raise RuntimeError(msg[-3000:])
    _sudo_ok()
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"{name} 输出非 JSON: {e}")


@contextmanager
def work_slot():
    if not WORK_SLOTS.acquire(blocking=False):
        raise BusyError("服务忙：正在执行其他扫描/修复，请稍后重试")
    try:
        yield
    finally:
        WORK_SLOTS.release()


def plan_digest(scan_id, target, items, preview):
    """把「用户看过的 dry-run 计划」压成摘要，apply 时必须原样对应。"""
    payload = json.dumps({
        "scan_id": scan_id, "target": target, "items": sorted(items),
        "steps": [[r.get("item_id"), r.get("status"), r.get("commands"),
                   r.get("rollback_commands")] for r in preview.get("results", [])],
    }, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def purge_pending():
    now = time.time()
    with LOCK:
        for key in [k for k, v in PENDING.items() if v["expires"] < now]:
            del PENDING[key]

PAGE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Server Security Guard</title>
<style>
:root{color-scheme:dark;--bg:#10151c;--panel:#18212c;--line:#2a3949;--text:#e8eef5;--muted:#9aabbd;--accent:#55c2a3;--warn:#e8b45b;--bad:#ef7272}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,"Segoe UI",sans-serif}main{max-width:1050px;margin:32px auto;padding:0 18px}h1{font-size:25px;margin:0 0 4px}.sub{color:var(--muted);margin:0 0 22px}.bar,.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}.row{display:flex;gap:12px;align-items:end;flex-wrap:wrap}label{display:block;color:var(--muted);font-size:13px;margin-bottom:5px}input[type=text],input[type=number],input[type=password]{background:#0e141b;border:1px solid var(--line);border-radius:7px;color:var(--text);padding:10px 12px;font:inherit}#target{width:min(520px,80vw)}button{border:0;border-radius:7px;background:var(--accent);color:#08130f;font-weight:700;padding:10px 16px;cursor:pointer}button:disabled{opacity:.45;cursor:not-allowed}.secondary{background:#2b3c4e;color:var(--text)}.danger{background:var(--bad);color:#270b0b}.meta{color:var(--muted);font-size:13px}.finding{border-top:1px solid var(--line);padding:13px 2px;display:grid;grid-template-columns:24px 90px 1fr;gap:8px}.sev{font-size:12px;font-weight:700}.CRITICAL,.HIGH{color:var(--bad)}.MEDIUM{color:var(--warn)}.LOW,.INFO{color:var(--muted)}.evidence{font:12px ui-monospace,monospace;color:#b5c4d2;white-space:pre-wrap;overflow-wrap:anywhere;margin-top:4px}.actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:14px}.status{margin:14px 0;padding:11px;border-radius:8px;background:#111923;white-space:pre-wrap}.hidden{display:none}.notice{color:var(--warn);font-size:13px}.check{margin:0}.modal{position:fixed;inset:0;background:#000b;display:grid;place-items:center;padding:18px}.modalbox{max-width:500px;width:100%;background:var(--panel);border:1px solid var(--line);padding:20px;border-radius:12px}.modalbox input{width:100%;margin:10px 0}.right{margin-left:auto}@media(max-width:600px){.finding{grid-template-columns:24px 70px 1fr}}
</style></head><body><main><h1>服务器安全防护</h1><p class="sub">仅供已授权服务器使用 · 服务只监听本机 · 默认先预览，修复须再次明确确认</p>
<section class="bar"><div class="row"><div><label for="target">目标</label><input id="target" type="text" value="local" placeholder="local 或 ssh://user@host[:port]" autocomplete="off"></div><div><label for="scope">扫描范围</label><select id="scope" style="background:#0e141b;color:var(--text);padding:10px;border:1px solid var(--line);border-radius:7px"><option>all</option><option>config</option><option>service</option><option>port</option><option>patch</option><option>ssh</option></select></div><button id="scan">开始扫描</button></div><p class="sub" style="margin:10px 0 0">HTTPS · 自签名证书 · 仅监听本机（127.0.0.1）</p><p class="notice">修复会修改远端系统。先检查扫描证据与 dry-run 命令；仅对你有授权的主机执行。</p>
<div class="row" style="margin-top:12px"><div><label for="elevate"><input type="checkbox" id="elevate" style="vertical-align:-2px"> 以管理员权限修复（sudo）</label><div class="meta">仅 local 目标；密码只经本机回环传给 sudo，内存中一次性使用，不存储、不写日志</div></div><div id="sudoWrap" class="hidden"><label for="sudoPw">sudo 密码</label><input id="sudoPw" type="password" autocomplete="new-password" placeholder="仅本次使用"></div></div></section>
<div id="status" class="status hidden"></div><section id="results" class="card hidden"></section>
</main><div id="modal" class="modal hidden"><div class="modalbox"><h2>确认实际修复</h2><p id="confirmText">将对目标执行实际系统变更。确认已审核所选项及 dry-run 命令。</p><label for="phrase">输入 APPLY 才能继续</label><input id="phrase" type="text" autocomplete="off"><div class="actions"><button class="secondary right" id="cancel">取消</button><button class="danger" id="apply" disabled>执行修复</button></div></div></div>
<script>
(()=>{const token=location.hash.slice(1);history.replaceState(null,"",location.pathname);const $=s=>document.querySelector(s);let scanData=null,scanKey=null,confirmToken=null;
async function api(path,body){const r=await fetch(path,{method:body?"POST":"GET",headers:{"Authorization":"Bearer "+token,...(body?{"Content-Type":"application/json"}:{})},body:body?JSON.stringify(body):undefined});const d=await r.json();if(!r.ok)throw Error(d.error||`HTTP ${r.status}`);return d}
function show(msg){$('#status').textContent=msg;$('#status').classList.remove('hidden')}
$('#scan').onclick=async()=>{const target=$('#target').value.trim();if(!target)return show('请输入目标');$('#scan').disabled=true;$('#results').classList.add('hidden');show('扫描中…');try{scanData=await api('/api/scan',{target,scope:$('#scope').value});scanKey=scanData.scan_id;render(scanData)}catch(e){show('扫描失败：'+e.message)}finally{$('#scan').disabled=false}};
function render(d){const fs=d.findings||[];let html=`<h2>扫描结果</h2><p class="meta">目标：${esc(d.target)} · ${esc(d.timestamp)} · 共 ${fs.length} 项</p>`;if(!fs.length)html+='<p>未发现已实现规则命中的问题。未实现的检查项仍需人工核查。</p>';for(const f of fs){const safe=!!f.auto_fixable;html+=`<div class="finding"><input class="check" type="checkbox" data-id="${esc(f.id)}" ${safe?'':'disabled'} ${safe?'checked':''}><div class="sev ${esc(f.severity)}">${esc(f.severity)}<br>${esc(f.id)}</div><div><strong>${esc(f.title)}</strong>${safe?'':' <span class="meta">· 不支持自动修复</span>'}<div class="evidence">${esc(f.evidence||'')}</div></div></div>`}html+=`<div class="actions"><span class="meta">默认选中可自动修复项，可按需取消选择。</span><button id="preview">生成修复预览</button></div><div id="previewBox"></div>`;$('#results').innerHTML=html;$('#results').classList.remove('hidden');show('扫描完成。');$('#preview').onclick=preview}
$('#elevate').onchange=()=>{$('#sudoWrap').classList.toggle('hidden',!$('#elevate').checked);if(!$('#elevate').checked)$('#sudoPw').value=''};
function elev(){return $('#elevate').checked?{use_sudo:true,sudo_password:$('#sudoPw').value}:{use_sudo:false}};
async function preview(){const ids=[...document.querySelectorAll('.check:checked')].map(e=>e.dataset.id);if(!ids.length)return show('没有选择可自动修复项。');if($('#elevate').checked&&!$('#sudoPw').value)return show('已勾选管理员权限，请输入 sudo 密码。');show('生成 dry-run 预览…');try{const d=await api('/api/preview',{scan_id:scanKey,items:ids,...elev()});let h='<h3>Dry-run 预览（尚未改动系统）</h3>';for(const r of d.results||[]){h+=`<div class="finding"><span></span><div class="sev">${esc(r.status)}</div><div><strong>${esc(r.item_id)}</strong><div class="evidence">${esc((r.commands||[]).join('\n'))}</div><div class="meta">${esc(r.message||'')}</div></div></div>`}h+='<div class="actions"><span class="notice">确认前请核对目标、项目、命令与回滚方式。</span><button class="danger" id="openConfirm">确认并修复所选项</button></div>';$('#previewBox').innerHTML=h;confirmToken=d.confirm_token||null;show('Dry-run 完成，系统尚未改动。');$('#openConfirm').onclick=()=>{$('#phrase').value='';$('#apply').disabled=true;$('#modal').classList.remove('hidden')}}catch(e){show('预览失败：'+e.message)}}
$('#phrase').oninput=()=>$('#apply').disabled=$('#phrase').value.trim()!=='APPLY';$('#cancel').onclick=()=>$('#modal').classList.add('hidden');
$('#apply').onclick=async()=>{const ids=[...document.querySelectorAll('.check:checked')].map(e=>e.dataset.id);$('#apply').disabled=true;show('正在执行实际修复…');try{const d=await api('/api/apply',{scan_id:scanKey,items:ids,confirm_token:confirmToken,...elev(),confirmation:$('#phrase').value.trim()});confirmToken=null;$('#sudoPw').value='';$('#modal').classList.add('hidden');const box=$('#previewBox');let h='<h3>执行结果'+(d.elevated?'（以管理员权限）':'')+'</h3>';for(const r of d.results||[]){h+=`<div class="finding"><span></span><div class="sev">${esc(r.status)}</div><div><strong>${esc(r.item_id)}</strong><div class="evidence">${esc((r.commands||[]).join('\n'))}</div><div class="meta">${esc(r.message||'')}</div><div class="evidence">回滚：${esc((r.rollback_commands||[]).join('\n')||'无')}</div></div></div>`}box.innerHTML=h;show('执行完成；请检查各项状态与回滚信息。')}catch(e){confirmToken=null;show('执行失败：'+e.message+'（请重新扫描并预览后再试）')}finally{$('#apply').disabled=$('#phrase').value.trim()!=='APPLY'}};
function esc(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
})();
</script></body></html>'''


def valid_target(target):
    import sys
    sys.path.insert(0, str(SCRIPT_DIR))
    import _common
    _common.parse_target(target)
    return target


def run_script(name, args, timeout=180, allow_rc=()):
    path = SCRIPT_DIR / name
    p = subprocess.run([sys.executable, str(path), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=timeout,
                       cwd=str(SKILL_ROOT))
    if p.returncode != 0 and p.returncode not in allow_rc:
        raise RuntimeError((p.stderr.strip() or p.stdout.strip() or f"{name} failed")[-3000:])
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"{name} 输出非 JSON: {e}; {p.stderr[-1000:]}")


def purge_sessions():
    now = time.time()
    with LOCK:
        for key in list(SESSIONS):
            if now - SESSIONS[key]["created"] > SESSION_TTL:
                del SESSIONS[key]


class Handler(BaseHTTPRequestHandler):
    server_version = "ServerSecurityGuardUI/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("[web-ui] " + (fmt % args) + "\n")

    def _json(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(data)

    def _authorized(self):
        # 用 urlparse 解析 authority，正确处理 [::1]:8765 这类 IPv6 形式
        host_header = self.headers.get("Host", "")
        try:
            host = (urlparse("//" + host_header).hostname or "").lower()
        except ValueError:
            return False
        if host not in ("127.0.0.1", "localhost", "::1"):
            return False
        origin = self.headers.get("Origin")
        if origin:
            parsed = urlparse(origin)
            if (parsed.hostname or "").lower() not in ("127.0.0.1", "localhost", "::1"):
                return False
        supplied = self.headers.get("Authorization", "")
        return supplied.startswith("Bearer ") and hmac.compare_digest(supplied[7:], TOKEN)

    def _body(self):
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise ValueError("invalid Content-Length")
        if size <= 0 or size > MAX_BODY:
            raise ValueError("request body size out of range")
        data = json.loads(self.rfile.read(size).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("JSON object required")
        return data

    def do_GET(self):
        if self.path != "/":
            return self._json(404, {"error": "not found"})
        body = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self._authorized():
            return self._json(403, {"error": "forbidden: local access token required"})
        try:
            body = self._body()
            route = urlparse(self.path).path
            purge_sessions()
            purge_pending()
            if route == "/api/scan":
                target = valid_target(str(body.get("target", "")))
                scope = str(body.get("scope", "all"))
                if scope not in ("all", "config", "service", "port", "patch", "ssh"):
                    raise ValueError("invalid scan scope")
                with work_slot():
                    result = run_script("vuln_scan.py", ["--target", target, "--scope", scope])
                scan_id = secrets.token_urlsafe(24)
                with LOCK:
                    SESSIONS[scan_id] = {"created": time.time(), "target": target, "scan": result}
                return self._json(200, {"scan_id": scan_id, "target": target,
                                        "timestamp": result.get("timestamp"),
                                        "findings": result.get("findings", []),
                                        "summary": result.get("summary", {}),
                                        "total": result.get("total", 0),
                                        "errors": result.get("errors", [])})
            if route in ("/api/preview", "/api/apply"):
                scan_id = str(body.get("scan_id", ""))
                with LOCK:
                    session = SESSIONS.get(scan_id)
                if not session or time.time() - session["created"] > SESSION_TTL:
                    raise ValueError("scan session missing or expired; rescan first")
                available = {f["id"] for f in session["scan"].get("findings", [])
                             if f.get("auto_fixable", True)}
                items = body.get("items")
                if not isinstance(items, list) or not items or len(items) > 80:
                    raise ValueError("select one or more repair item IDs")
                items = list(dict.fromkeys(str(x) for x in items))
                if any(x not in available for x in items):
                    raise ValueError("selected item was not marked auto-fixable in this scan")
                with __import__("tempfile").TemporaryDirectory(prefix="ssg-web-") as td:
                    inp = Path(td) / "scan.json"
                    inp.write_text(json.dumps(session["scan"], ensure_ascii=False), encoding="utf-8")
                    args = ["--target", session["target"], "--input", str(inp), "--items", ",".join(items)]
                    # ---- 管理员权限（可选）：密码仅本请求内使用，不存储不回传 ----
                    use_sudo = bool(body.get("use_sudo"))
                    sudo_pw = body.get("sudo_password") or ""
                    if use_sudo:
                        if session["target"] != "local":
                            raise ValueError("管理员提权仅支持 local 目标：远程主机请用 root 登录"
                                             "或已配置 NOPASSWD 的 sudo 账号")
                        if not isinstance(sudo_pw, str) or not sudo_pw.strip():
                            raise ValueError("已勾选管理员权限，但未提供密码")
                        if len(sudo_pw) > 512:
                            raise ValueError("密码长度异常")

                    def _run_fix(extra=(), **kw):
                        if use_sudo:
                            return run_sudo_script("vuln_fix.py", args + list(extra), sudo_pw, **kw)
                        return run_script("vuln_fix.py", args + list(extra), **kw)

                    if route == "/api/preview":
                        with work_slot():
                            result = _run_fix()
                        token = secrets.token_urlsafe(32)
                        with LOCK:
                            PENDING[token] = {
                                "scan_id": scan_id, "items": items, "target": session["target"],
                                "digest": plan_digest(scan_id, session["target"], items, result),
                                "expires": time.time() + CONFIRM_TTL,
                            }
                        return self._json(200, dict(result, confirm_token=token,
                                                    confirm_expires_in=CONFIRM_TTL))
                    # ---- apply：必须持有本次预览签发的确认令牌，且一次性 ----
                    if body.get("confirmation") != "APPLY":
                        raise ValueError("explicit APPLY confirmation required")
                    token = str(body.get("confirm_token", ""))
                    with LOCK:
                        pending = PENDING.get(token)
                    if not pending:
                        raise ValueError("缺少或已失效的预览确认：请重新预览后再执行")
                    if pending["expires"] < time.time():
                        raise ValueError("预览确认已过期：请重新预览后再执行")
                    if pending["scan_id"] != scan_id or sorted(pending["items"]) != sorted(items):
                        raise ValueError("确认令牌与当前所选项目不匹配：请重新预览")
                    with work_slot():
                        preview = _run_fix()
                        if plan_digest(scan_id, session["target"], items, preview) != pending["digest"]:
                            raise ValueError("修复计划或目标状态已变化：请重新预览并确认")
                        with LOCK:
                            PENDING.pop(token, None)  # 单次使用
                        applied = _run_fix(["--apply"], allow_rc=(3,))
                    if applied.get("status") == "requires_privilege":
                        return self._json(409, dict(applied, error=applied.get("error") or
                                                    "修复需要 root/sudo 权限，未做任何变更"))
                    applied["elevated"] = use_sudo
                    return self._json(200, applied)
            return self._json(404, {"error": "not found"})
        except BusyError as e:
            return self._json(429, {"error": str(e)})
        except SudoAuthError as e:
            return self._json(401, {"error": str(e)})
        except (ValueError, RuntimeError, subprocess.TimeoutExpired) as e:
            return self._json(400, {"error": str(e)})
        except Exception as e:
            self.log_error("request failed: %s", e)
            return self._json(500, {"error": "internal error"})

    def log_error(self, fmt, *args):
        sys.stderr.write("[web-ui] ERROR " + (fmt % args) + "\n")


def _state_dir():
    """证书/状态目录（用户级，权限 0700）。"""
    d = Path(os.environ.get("SSG_STATE_DIR") or (Path.home() / ".server-security-guard"))
    d.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(d, 0o700)
    except OSError:
        pass
    return d


def _cert_still_good(cert, min_days=7):
    """证书存在且剩余有效期充足。"""
    try:
        info = ssl._ssl._test_decode_cert(str(cert))  # noqa: SLF001 - stdlib 无公开替代
        not_after = info.get("notAfter")
        if not not_after:
            return False
        return ssl.cert_time_to_seconds(not_after) - time.time() > min_days * 86400
    except Exception:
        return False


def _gen_cert_openssl(cert, key):
    """用 openssl 生成自签名证书（含 127.0.0.1/::1/localhost 的 SAN）。"""
    openssl = shutil.which("openssl")
    if not openssl:
        raise RuntimeError("openssl 不存在")
    base = [openssl, "req", "-x509", "-newkey", "rsa:2048", "-nodes",
            "-keyout", str(key), "-out", str(cert), "-days", "365",
            "-subj", "/CN=127.0.0.1"]
    san = "subjectAltName=IP:127.0.0.1,IP:::1,DNS:localhost"
    attempts = [base + ["-addext", san]]
    cnf = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False, encoding="utf-8") as fh:
            fh.write("[req]\ndistinguished_name=dn\nx509_extensions=v3\n[dn]\nCN=127.0.0.1\n"
                     f"[v3]\n{san}\n")
            cnf = fh.name
        # 兼容不支持 -addext 的旧 openssl
        attempts.append(base + ["-config", cnf, "-extensions", "v3"])
        last = ""
        for cmd in attempts:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if p.returncode == 0 and cert.exists() and key.exists():
                return
            last = (p.stderr or p.stdout or "").strip()[-500:]
        raise RuntimeError(f"openssl 生成证书失败: {last}")
    finally:
        if cnf:
            try:
                os.unlink(cnf)
            except OSError:
                pass


def _gen_cert_cryptography(cert, key):
    """openssl 不可用时的纯 Python 回退。"""
    from datetime import datetime, timedelta, timezone

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1")])
    now = datetime.now(timezone.utc)
    crt = (x509.CertificateBuilder()
           .subject_name(name).issuer_name(name)
           .public_key(k.public_key())
           .serial_number(x509.random_serial_number())
           .not_valid_before(now - timedelta(minutes=5))
           .not_valid_after(now + timedelta(days=365))
           .add_extension(x509.SubjectAlternativeName([
               x509.IPAddress(__import__("ipaddress").ip_address("127.0.0.1")),
               x509.IPAddress(__import__("ipaddress").ip_address("::1")),
               x509.DNSName("localhost")]), critical=False)
           .sign(k, hashes.SHA256()))
    key.write_bytes(k.private_bytes(serialization.Encoding.PEM,
                                    serialization.PrivateFormat.TraditionalOpenSSL,
                                    serialization.NoEncryption()))
    cert.write_bytes(crt.public_bytes(serialization.Encoding.PEM))


def ensure_cert(cert_path=None, key_path=None):
    """返回 (cert, key, 说明)。自签名证书生成一次后复用，私钥权限 0600。"""
    if cert_path and key_path:
        c, k = Path(cert_path), Path(key_path)
        if not (c.exists() and k.exists()):
            raise RuntimeError(f"证书或私钥不存在: {c} / {k}")
        return c, k, "用户提供"
    d = _state_dir()
    cert, key = d / "tls.crt", d / "tls.key"
    if cert.exists() and key.exists() and _cert_still_good(cert):
        return cert, key, "复用已有证书"
    errors = []
    for gen in (_gen_cert_openssl, _gen_cert_cryptography):
        try:
            gen(cert, key)
            try:
                os.chmod(key, 0o600)
            except OSError:
                pass
            return cert, key, f"新生成（{gen.__name__.replace('_gen_cert_', '')}）"
        except Exception as e:
            errors.append(f"{gen.__name__}: {e}")
    raise RuntimeError("无法生成自签名证书；请安装 openssl 或 python cryptography，"
                       "或用 --cert/--key 指定证书。详情: " + " | ".join(errors))


class GuardServer(ThreadingHTTPServer):
    """TLS 握手失败/浏览器探测不发堆栈，保持日志干净。"""

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ssl.SSLError, ConnectionError, TimeoutError, OSError)):
            return
        super().handle_error(request, client_address)


def build_server(host, port, cert=None, key=None, no_tls=False):
    """按配置构建服务（默认 HTTPS）。返回 (server, scheme, cert_info)。"""
    server = GuardServer((host, port), Handler)
    server.daemon_threads = True
    if no_tls:
        return server, "http", None
    try:
        c, k, how = ensure_cert(cert, key)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(str(c), str(k))
        server.socket = context.wrap_socket(server.socket, server_side=True)
        return server, "https", (c, k, how)
    except Exception:
        server.server_close()
        raise


def main():
    parser = argparse.ArgumentParser(description="Loopback-only HTTPS UI for server-security-guard")
    parser.add_argument("--host", default="127.0.0.1", help="loopback address only (default 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--cert", help="TLS 证书路径（不填则自动生成自签名证书并复用）")
    parser.add_argument("--key", help="TLS 私钥路径（与 --cert 同时使用）")
    parser.add_argument("--no-tls", action="store_true",
                        help="禁用 HTTPS（不推荐：提权密码会以明文经过回环）")
    args = parser.parse_args()
    if args.host not in ("127.0.0.1", "localhost", "::1"):
        parser.error("security policy: bind to loopback only; do not expose this UI to a network")
    if bool(args.cert) != bool(args.key):
        parser.error("--cert 与 --key 必须同时提供")

    if args.no_tls:
        print("[WARN] 已禁用 HTTPS：令牌与 sudo 密码将以明文经过回环，仅限本机调试。",
              file=sys.stderr, flush=True)
    try:
        server, scheme, info = build_server(args.host, args.port, args.cert, args.key, args.no_tls)
    except Exception as e:
        print(f"[ERROR] 无法启用 HTTPS: {e}", file=sys.stderr, flush=True)
        print("可提供 --cert/--key，或（不推荐）用 --no-tls 退回 HTTP。", file=sys.stderr, flush=True)
        sys.exit(2)
    if info:
        print(f"TLS: 证书 {info[0]}（{info[2]}）", flush=True)
        print("浏览器会提示自签名证书不受信任——确认证书指纹后继续访问即可。", flush=True)

    print(f"Local-only UI: {scheme}://{args.host}:{server.server_address[1]}/#{TOKEN}", flush=True)
    print("Keep this service on loopback; stop with Ctrl+C. Apply requires typing APPLY after reviewing dry-run.",
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
