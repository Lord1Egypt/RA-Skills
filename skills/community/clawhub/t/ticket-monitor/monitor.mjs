// monitor.mjs — 大麦余票实时监控主程序
// 轮询商品详情 → 与上次快照 diff → 变化时通过日志/Webhook/弹窗告警
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { fetchItemDetail, fetchRaw, extractItemId } from './damai.mjs';
import { dispatch, terminal, sendToast } from './notify.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function parseArgs(argv) {
  const a = {};
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === '--config') a.config = argv[++i];
    else if (k === '--item-id') a.itemId = argv[++i];
    else if (k === '--url') a.url = argv[++i];
    else if (k === '--interval') a.interval = argv[++i];
    else if (k === '--once') a.once = true;
    else if (k === '--raw') a.raw = true;
    else if (k === '--help' || k === '-h') a.help = true;
  }
  return a;
}

function loadConfig(cfgPath) {
  const p = cfgPath || path.join(__dirname, 'config.json');
  let cfg = {};
  try {
    cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    if (cfgPath) throw new Error(`无法读取配置 ${p}: ${e.message}`);
  }
  cfg.notify = cfg.notify || {};
  cfg.damai = cfg.damai || {};
  if (cfg.notify.logFile && !path.isAbsolute(cfg.notify.logFile)) {
    cfg.notify.logFile = path.resolve(__dirname, cfg.notify.logFile);
  }
  return cfg;
}

function fmt(v) {
  return v == null ? '—' : String(v);
}

function summarize(s) {
  const parts = [`[${s.itemName}] ${s.overallLabel}`];
  if (s.remainCount != null) parts.push(`余票 ${s.remainCount}`);
  for (const sess of s.sessions || []) {
    const skuInfo = (sess.skus || []).map((k) => `${k.name}:${k.salable ? '有' : '无'}`).join(',');
    parts.push(`${sess.name}[${sess.salable ? '有票' : '售罄'}]${skuInfo ? ` {${skuInfo}}` : ''}`);
  }
  return parts.join(' ');
}

function diff(prev, curr) {
  if (!prev) return [];
  const lines = [];
  if (prev.itemStatus !== curr.itemStatus) {
    lines.push(`演出状态: ${prev.itemStatusLabel} → ${curr.itemStatusLabel}`);
  }
  if (prev.overallLabel !== curr.overallLabel) {
    lines.push(`整体状态: ${prev.overallLabel} → ${curr.overallLabel}`);
  }
  if ((prev.remainCount ?? null) !== (curr.remainCount ?? null)) {
    lines.push(`余票数量: ${fmt(prev.remainCount)} → ${fmt(curr.remainCount)}`);
  }

  const prevS = new Map((prev.sessions || []).map((s) => [s.performId ?? s.name, s]));
  const currS = new Map((curr.sessions || []).map((s) => [s.performId ?? s.name, s]));
  for (const [key, c] of currS) {
    const p = prevS.get(key);
    if (!p) {
      lines.push(`新增场次: ${c.name}（${c.statusLabel}）`);
      continue;
    }
    if (p.salable !== c.salable) {
      lines.push(`场次「${c.name}」: ${p.salable ? '有票' : '售罄'} → ${c.salable ? '有票' : '售罄'}`);
    }
    if (p.status !== c.status) {
      lines.push(`场次「${c.name}」状态: ${p.statusLabel} → ${c.statusLabel}`);
    }
    if ((p.remainCount ?? null) !== (c.remainCount ?? null)) {
      lines.push(`场次「${c.name}」余票: ${fmt(p.remainCount)} → ${fmt(c.remainCount)}`);
    }
    const pSk = new Map((p.skus || []).map((k) => [k.name, k]));
    for (const ck of c.skus || []) {
      const pk = pSk.get(ck.name);
      if (pk && pk.salable !== ck.salable) {
        lines.push(`档位「${ck.name}」: ${pk.salable ? '有票' : '售罄'} → ${ck.salable ? '有票' : '售罄'}`);
      }
    }
  }
  for (const [key, p] of prevS) {
    if (!currS.has(key)) lines.push(`场次移除: ${p.name}`);
  }
  return lines;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log('用法: node monitor.mjs [--config <path>] [--item-id <id>|--url <url>] [--interval <秒>] [--once] [--raw]');
    return;
  }

  const cfg = loadConfig(args.config);
  const input = args.itemId || args.url || cfg.itemId || cfg.url;
  if (!input) {
    terminal('错误：请提供 itemId 或 url（config.json 或 --item-id/--url 参数）');
    return;
  }

  const itemId = extractItemId(input);
  const intervalMs = Number(args.interval || cfg.interval || 30) * 1000;
  const stateFile = path.resolve(__dirname, cfg.stateFile || 'state.json');

  let prev = null;
  try {
    prev = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  } catch {
    /* 首次运行无状态 */
  }

  if (args.raw) {
    const { raw } = await fetchRaw(input, cfg.damai);
    terminal(JSON.stringify(raw, null, 2));
    return;
  }

  if (args.once) {
    const snap = await fetchItemDetail(input, cfg.damai);
    terminal(JSON.stringify(snap, null, 2));
    return;
  }

  terminal(`开始监控 itemId=${itemId}，间隔 ${intervalMs / 1000}s（Ctrl+C 停止）`);
  terminal('注意：大麦公开接口通常只返回「有票/售罄」状态，精确余票张数一般不公开。');

  try {
    const snap = await fetchItemDetail(input, cfg.damai);
    terminal(`初始状态: ${summarize(snap)}`);
    prev = snap;
    fs.writeFileSync(stateFile, JSON.stringify(snap, null, 2), 'utf8');
    if (cfg.notify.toastOnStart) await dispatch('监控已启动', summarize(snap), cfg.notify);
  } catch (e) {
    terminal(`首次抓取失败: ${e.message}`);
  }

  while (true) {
    await sleep(intervalMs);
    try {
      const snap = await fetchItemDetail(input, cfg.damai);
      const lines = diff(prev, snap);
      if (lines.length) {
        await dispatch('余票变化', lines.join('\n'), cfg.notify);
      } else if (!cfg.quiet) {
        terminal(summarize(snap));
      }
      prev = snap;
      fs.writeFileSync(stateFile, JSON.stringify(snap, null, 2), 'utf8');
    } catch (e) {
      terminal(`抓取失败（下轮重试）: ${e.message}`);
      if (cfg.notify.toastOnError) sendToast('监控异常', e.message);
    }
  }
}

main().catch((e) => {
  terminal(`致命错误: ${e.stack || e.message}`);
  process.exit(1);
});
