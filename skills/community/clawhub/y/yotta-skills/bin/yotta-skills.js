#!/usr/bin/env node
/**
 * yotta-skills（元阁）—— 全家技能一键安装 CLI（YottaSkills 合集）
 *
 * 用法:
 *   npx -y @yottameta/yotta-skills --list                 # 列出全家技能 + 版本 + 说明
 *   npx -y @yottameta/yotta-skills install --agent <name> # 装全家到智能体默认用户级目录（推荐）
 *   npx -y @yottameta/yotta-skills install --dir <path>   # 装全家到指定目录
 *   npx -y @yottameta/yotta-skills install <skill> --dir <path>  # 装单个技能
 *   npx -y @yottameta/yotta-skills update --agent <name>  # 增量更新已装技能（补齐缺失/版本不一致）
 *   npx -y @yottameta/yotta-skills update --check         # 只读检查更新（联网对 npm 最新，不改动；退出码 0/3/1）
 *   npx -y @yottameta/yotta-skills update --check --scheduled  # 后台周检（未到期不联网，到期单次检查并写缓存）
 *   npx -y @yottameta/yotta-skills update --auto          # 检查到家族更新后自动更新（仅 yotta-* 家族，含装前扫描）
 *   npx -y @yottameta/yotta-skills hook capabilities      # 查看宿主六事件能力矩阵
 *   npx -y @yottameta/yotta-skills hook evaluate --event before_send --manifest <file>  # 评估并留证
 *   npx -y @yottameta/yotta-skills --dry-run              # 预览将安装清单（不联网、不改动）
 *
 * 版本策略：默认 `--pin` 锁死清单精确版本（可复现，不静默跟随浮动版本）；`--range` 才跟随同 major 最新 patch。
 * 依赖：Node.js 18+（必需）；npm / 系统 tar 仅作回退通道（内置拉包 / 内置解包为主）；
 *       元信 scan 需要 Python 3.8+（可 --python / YOTTA_SKILLS_PYTHON 指向宿主自带 Python）。
 * 边界：只做「清单 + 下载 + 落位 + 汇总」；不内置任何技能本体；不 -g 污染。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');
const http = require('http');
const https = require('https');
const evidenceLib = require('../lib/install-evidence');
const gateLib = require('../lib/verify-gate');
const trustedVerifierLib = require('../lib/trusted-verifier');
const healthLib = require('../lib/install-health');
const lifecycleLib = require('../lib/install-lifecycle');
const snapshotLib = require('../lib/install-snapshot');
const updateCheckLib = require('../lib/update-check');
const hookAdapterLib = require('../lib/hook-adapter');
const scanPolicyLib = require('../lib/scan-policy');
const npmPackLib = require('../lib/npm-pack');
const usageJournalLib = require('../lib/usage-journal');
const m1FeaturesLib = require('../lib/m1-features');
const routeFeaturesLib = require('../lib/route-features');
const routeDynamicLib = require('../lib/route-dynamic');
const depsLib = require('../lib/deps');
const untarLib = require('../lib/untar');
const registryFetchLib = require('../lib/registry-fetch');
const agentDirsLib = require('../lib/agent-dirs');
const agentDiscoveryLib = require('../lib/agent-discovery');
const hubLib = require('../lib/hub');
const hubAdoptLib = require('../lib/hub-adopt');
const hubMigrateLib = require('../lib/hub-migrate');
const hubTargetsLib = require('../lib/hub-targets');
const selfInstallLib = require('../lib/self-install');
const skillsConfigLib = require('../lib/skills-config');
const hostsRegistryLib = require('../lib/hosts-registry');
const hostPurgeLib = require('../lib/host-purge');
const hubScanLib = require('../lib/hub-scan');
const hubViewServerLib = require('../lib/hub-view-server');
const { createInstaller, isSafeTarEntry } = require('../lib/install-pipeline');
const { COPY_SKIP, copyDir } = require('../lib/copy-tree');
const { versionRelation } = require('../lib/skills-scan');

const PKG_ROOT = path.join(__dirname, '..');
let VERSION = '0.30.14';
try { VERSION = require(path.join(PKG_ROOT, 'package.json')).version; } catch (_) { /* keep fallback */ }

// @generated view-html:start
const VIEW_HTML = "<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<meta name=\"robots\" content=\"noindex,nofollow\">\n<meta name=\"yotta-view-token\" content=\"__YOTTA_VIEW_TOKEN__\">\n<link rel=\"icon\" href=\"data:,\">\n<title>元阁 · 技能枢纽</title>\n<style>\n  :root{--bg:#0d1114;--bg2:#12171b;--panel:#171d22;--panel2:#1d242a;--line:rgba(148,190,170,.14);--line2:rgba(148,190,170,.28);\n    --text:#e9efe9;--muted:#9aa8a0;--faint:#6d7b74;--acc:#5fbf8f;--acc-ink:#0d1a13;--warn:#e0b263;--danger:#e07a7a;--info:#8fb4de;\n    --shadow:0 10px 28px rgba(0,0,0,.35)}\n  body.light{--bg:#f2f5f1;--bg2:#e9efea;--panel:#ffffff;--panel2:#f6f9f5;--line:rgba(24,58,44,.12);--line2:rgba(24,58,44,.24);\n    --text:#17211c;--muted:#5c6b63;--faint:#86958c;--acc:#2f7d59;--acc-ink:#ffffff;--warn:#9a6a14;--danger:#b23c3c;--info:#3c6ea5;\n    --shadow:0 8px 22px rgba(24,58,44,.08)}\n  *{box-sizing:border-box}[hidden]{display:none!important}\n  html,body{margin:0;padding:0}\n  body{background:var(--bg);color:var(--text);font:14px/1.6 \"Microsoft YaHei\",\"PingFang SC\",\"Noto Sans CJK SC\",system-ui,sans-serif;letter-spacing:0}\n  button{font:inherit;color:inherit;cursor:pointer}\n  input,textarea{font:inherit;color:var(--text);background:var(--panel2);border:1px solid var(--line2);border-radius:6px;padding:8px 11px;outline:0;width:100%}\n  input:focus,textarea:focus{border-color:var(--acc)}\n  textarea{min-height:76px;resize:vertical}\n  code,kbd{font-family:ui-monospace,Consolas,\"Courier New\",monospace;font-size:12px}\n  .sv{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;flex:none}\n\n  .shell{display:grid;grid-template-columns:232px minmax(0,1fr);min-height:100vh}\n  .sidebar{background:var(--bg2);border-right:1px solid var(--line);padding:20px 14px;display:flex;flex-direction:column;gap:20px;position:sticky;top:0;height:100vh;min-width:0}\n  .brand{display:flex;align-items:center;gap:10px;padding:0 6px}\n  .brand-mark{width:34px;height:34px;border-radius:8px;background:rgba(95,191,143,.14);border:1px solid var(--line2);display:grid;place-items:center;color:var(--acc)}\n  .brand-name{font-size:15px;font-weight:600}\n  .brand-sub{font-size:11px;color:var(--faint)}\n  .nav{display:flex;flex-direction:column;gap:3px;min-width:0}\n  .nav button{display:flex;align-items:center;gap:9px;padding:8px 10px;border-radius:6px;border:1px solid transparent;background:transparent;color:var(--muted);text-align:left}\n  .nav button:hover{background:var(--panel);color:var(--text)}\n  .nav button.active{background:var(--panel);color:var(--acc);border-color:var(--line)}\n  .side-foot{margin-top:auto;display:flex;flex-direction:column;gap:8px;min-width:0}\n  .privacy{display:flex;gap:8px;align-items:flex-start;padding:10px;border:1px solid var(--line);border-radius:8px;color:var(--muted);font-size:12px;background:var(--panel)}\n  .privacy .sv{color:var(--acc);margin-top:2px}\n  .ghost-btn{display:flex;align-items:center;justify-content:center;gap:8px;border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:6px;padding:8px}\n  .ghost-btn:hover{color:var(--text);border-color:var(--line2)}\n  .verline{padding:0 6px;color:var(--faint);font-size:11px}\n\n  .main{min-width:0;padding:24px 28px 70px}\n  .topbar{display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap}\n  .loadbar{display:flex;align-items:center;gap:9px;color:var(--muted);font-size:13px;padding:10px 13px;border:1px dashed var(--line2);border-radius:8px;margin:0 0 14px;background:var(--panel)}\n  .spinner{width:14px;height:14px;border-radius:50%;border:2px solid var(--line2);border-top-color:var(--acc);animation:spin .8s linear infinite;flex:none}\n  @keyframes spin{to{transform:rotate(360deg)}}\n  .page-title{font-size:19px;font-weight:600;margin:0}\n  .page-sub{color:var(--faint);font-size:12px;margin-top:2px}\n  .spacer{flex:1}\n  .chip{display:flex;align-items:center;gap:7px;padding:5px 10px;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:12px;white-space:nowrap}\n  .chips{display:flex;gap:6px;flex-wrap:wrap}\n  .chip{cursor:pointer;background:transparent}\n  .chip.active{color:var(--acc);border-color:rgba(95,191,143,.45);background:rgba(95,191,143,.10)}\n  .dot{width:7px;height:7px;border-radius:50%;background:var(--acc)}\n\n  .view{display:none}.view.active{display:block}\n  .grid{display:grid;gap:12px}.g4{grid-template-columns:repeat(4,minmax(0,1fr))}.g2{grid-template-columns:repeat(2,minmax(0,1fr))}\n  .panel{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:15px;min-width:0}\n  .panel h3{margin:0 0 4px;font-size:14px}\n  .section{margin-top:16px}\n  .shead{display:flex;align-items:baseline;gap:10px;margin-bottom:9px;flex-wrap:wrap}\n  .shead h2{font-size:14px;margin:0}\n  .label{color:var(--muted);font-size:12px}\n  .value{font-size:25px;font-weight:600;margin:7px 0 2px}\n  .delta{font-size:12px;color:var(--muted)}\n  .mono{font-family:ui-monospace,Consolas,monospace;font-size:12px;word-break:break-all}\n\n  .toolbar{display:flex;gap:9px;align-items:center;flex-wrap:wrap}\n  .search{display:flex;align-items:center;gap:8px;min-width:230px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:7px 11px;color:var(--muted)}\n  .search input{background:transparent;border:0;padding:0;width:100%}\n  .btn{display:inline-flex;align-items:center;gap:7px;padding:7px 13px;border-radius:6px;border:1px solid var(--line2);background:transparent;color:var(--text);white-space:nowrap}\n  .btn:hover{border-color:var(--acc)}\n  .btn.primary{background:var(--acc);border-color:var(--acc);color:var(--acc-ink);font-weight:600}\n  .btn.danger{border-color:rgba(224,122,122,.5);color:var(--danger)}\n  .btn.small{padding:4px 9px;font-size:12px}\n  .btn[disabled]{opacity:.45;cursor:not-allowed}\n  .ibtn{width:29px;height:29px;display:grid;place-items:center;border:1px solid var(--line);background:transparent;border-radius:6px;color:var(--muted)}\n  .ibtn:hover{color:var(--text);border-color:var(--line2)}\n\n  table{width:100%;border-collapse:collapse}\n  th,td{text-align:left;padding:10px 9px;border-bottom:1px solid var(--line);font-size:13px;vertical-align:top}\n  th{color:var(--faint);font-weight:500;font-size:12px}\n  tbody tr:hover{background:var(--panel2)}\n  .cell-main{font-weight:600}\n  .cell-sub{color:var(--faint);font-size:11px;word-break:break-all}\n\n  .list{display:flex;flex-direction:column;gap:7px;margin-top:12px}\n  .row{display:flex;align-items:center;gap:11px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--panel2);min-width:0}\n  .row-main{flex:1;min-width:0}\n  .row-title{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n  .row-meta{color:var(--faint);font-size:11px;margin-top:2px;word-break:break-all}\n  .row-actions{display:flex;gap:6px;flex-wrap:wrap}\n  .empty{color:var(--faint);text-align:center;padding:22px;border:1px dashed var(--line);border-radius:8px;margin-top:12px}\n\n  .badge{display:inline-block;font-size:11px;padding:1px 8px;border-radius:999px;border:1px solid var(--line2);color:var(--muted);background:transparent;white-space:nowrap}\n  .badge.ok{color:var(--acc);border-color:rgba(95,191,143,.45);background:rgba(95,191,143,.10)}\n  .badge.warn{color:var(--warn);border-color:rgba(224,178,99,.45);background:rgba(224,178,99,.10)}\n  .badge.danger{color:var(--danger);border-color:rgba(224,122,122,.45);background:rgba(224,122,122,.10)}\n  .badge.info{color:var(--info);border-color:rgba(143,180,222,.45);background:rgba(143,180,222,.10)}\n  .dot-mark{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:6px;background:var(--faint)}\n  .dot-mark.ok{background:var(--acc)}.dot-mark.warn{background:var(--warn)}.dot-mark.danger{background:var(--danger)}\n\n  .banner{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;border:1px solid var(--line2);border-radius:8px;background:var(--panel2)}\n  .banner.ok{border-color:rgba(95,191,143,.45)}\n  .banner.danger{border-color:rgba(224,122,122,.45)}\n  .banner .sv{margin-top:2px;color:var(--acc)}\n  .banner.danger .sv{color:var(--danger)}\n  .banner-title{font-weight:600}\n  .banner-body{color:var(--muted);font-size:12px;margin-top:2px}\n\n  .kv{display:grid;grid-template-columns:96px 1fr;gap:5px 10px;font-size:13px;margin:10px 0}\n  .kv dt{color:var(--faint)}.kv dd{margin:0;word-break:break-all}\n  .variants{border-top:1px dashed var(--line);margin-top:8px;padding-top:8px;display:flex;flex-direction:column;gap:5px}\n  .variant{display:flex;gap:9px;align-items:baseline;font-size:12px;color:var(--muted);flex-wrap:wrap}\n  .check{width:16px;height:16px;flex:none;accent-color:var(--acc)}\n  details summary{cursor:pointer;color:var(--muted);font-size:12px}\n\n  .actionbar{position:sticky;bottom:0;margin-top:14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:11px 13px;border:1px solid var(--line2);border-radius:8px;background:var(--bg2);box-shadow:var(--shadow)}\n  .result-list{display:flex;flex-direction:column;gap:6px;margin-top:10px}\n  .result{display:flex;gap:9px;align-items:baseline;flex-wrap:wrap;padding:8px 10px;border:1px solid var(--line);border-radius:6px;font-size:12px}\n\n  .mask{position:fixed;inset:0;background:rgba(0,0,0,.52);display:none;place-items:center;z-index:50;padding:18px}\n  .mask.open{display:grid}\n  .modal{width:min(600px,100%);max-height:86vh;overflow:auto;background:var(--panel);border:1px solid var(--line2);border-radius:8px;padding:18px;box-shadow:var(--shadow)}\n  .modal h3{margin:0 0 10px;font-size:16px}\n  .modal-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:14px}\n\n  .toasts{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);display:flex;flex-direction:column;gap:7px;align-items:center;z-index:60}\n  .toast{background:var(--panel2);border:1px solid var(--line2);border-radius:999px;padding:8px 15px;box-shadow:var(--shadow);font-size:13px}\n\n  .cmd-group{margin-top:14px}\n  .cmd{display:flex;gap:10px;align-items:center;padding:9px 11px;border:1px solid var(--line);border-radius:6px;background:var(--panel2);margin-top:6px}\n  .cmd code{flex:1;min-width:0;word-break:break-all;color:var(--text)}\n  .cmd .why{color:var(--faint);font-size:11px}\n  .note{color:var(--muted);font-size:12px;margin-top:8px}\n  .cmd-detail{border:1px solid var(--line);border-radius:6px;background:var(--panel2);margin-top:8px;padding:0 11px;min-width:0}\n  .cmd-detail summary{cursor:pointer;padding:9px 0;display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}\n  .cmd-detail .note{padding:0 0 8px}\n  .cmd-detail .cmd{margin:0 0 8px}\n\n  /* 0.30.0 UX-05：术语速查 */\n  .glossary{border:1px solid var(--line);border-radius:8px;background:var(--panel);padding:0 12px}\n  .glossary summary{padding:10px 0}\n  .glossary-body{display:grid;gap:6px;padding:0 0 12px;font-size:12px;color:var(--muted)}\n  .glossary-body b{color:var(--text)}\n\n  @media (max-width:980px){.g4{grid-template-columns:repeat(2,minmax(0,1fr))}}\n  @media (max-width:760px){\n    .shell{grid-template-columns:minmax(0,1fr)}\n    .sidebar{position:static;height:auto;padding:13px;gap:11px}\n    .nav{flex-direction:row;overflow-x:auto;width:100%;scrollbar-width:none;-webkit-overflow-scrolling:touch}\n    .nav::-webkit-scrollbar{display:none}\n    .nav button{white-space:nowrap;padding:7px 9px}\n    .side-foot{margin-top:0;flex-direction:row;align-items:center}\n    .privacy{display:none}\n    .ghost-btn{flex:1;white-space:nowrap}\n    .verline{white-space:nowrap;text-align:right}\n    .main{padding:16px 14px 56px}\n    .g4,.g2{grid-template-columns:minmax(0,1fr)}\n    .search{min-width:100%}\n    table{display:block;overflow-x:auto;white-space:nowrap}\n    .row{flex-wrap:wrap}\n  }\n</style>\n</head>\n<body>\n<div class=\"shell\">\n  <aside class=\"sidebar\">\n    <div class=\"brand\">\n      <div class=\"brand-mark\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 3 4 7v4c0 4.4 3.4 8.4 8 10 4.6-1.6 8-5.6 8-10V7z\"/><path d=\"M9 12l2 2 4-4\"/></svg></div>\n      <div><div class=\"brand-name\">元阁 · 技能枢纽</div><div class=\"brand-sub\">Hub 本地面板</div></div>\n    </div>\n    <nav class=\"nav\" id=\"nav\">\n      <button data-view=\"overview\" class=\"active\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M3 10.5 12 3l9 7.5\"/><path d=\"M5 9.5V21h14V9.5\"/></svg>概览</button>\n      <button data-view=\"hosts\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"7\" rx=\"2\"/><rect x=\"3\" y=\"13\" width=\"18\" height=\"7\" rx=\"2\"/><path d=\"M7 7.5h.01M7 16.5h.01\"/></svg>宿主矩阵</button>\n      <button data-view=\"adopt\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 3v12\"/><path d=\"m7 10 5 5 5-5\"/><path d=\"M4 21h16\"/></svg>收编向导</button>\n      <button data-view=\"links\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M10 13a5 5 0 0 0 7.1 0l2-2a5 5 0 0 0-7.1-7.1L11 4.9\"/><path d=\"M14 11a5 5 0 0 0-7.1 0l-2 2A5 5 0 0 0 12 20.1l1-1\"/></svg>链接与体检</button>\n      <button data-view=\"records\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M3 12a9 9 0 1 0 3-6.7\"/><path d=\"M3 4v5h5\"/><path d=\"M12 8v5l3 2\"/></svg>记录与回滚</button>\n      <button data-view=\"route\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"6\" cy=\"6\" r=\"2.5\"/><circle cx=\"18\" cy=\"18\" r=\"2.5\"/><path d=\"M8.5 6H15a3 3 0 0 1 0 6h-6a3 3 0 0 0 0 6h6.5\"/></svg>路由与编排</button>\n      <button data-view=\"cli\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"m4 7 5 5-5 5\"/><path d=\"M12 19h8\"/></svg>高级 CLI</button>\n    </nav>\n    <div class=\"side-foot\">\n      <div class=\"privacy\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z\"/><path d=\"m9 12 2 2 4-4\"/></svg><span>本机运行 · 零远程<br>写操作需页面令牌与确认</span></div>\n      <button class=\"ghost-btn\" id=\"themeBtn\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"12\" cy=\"12\" r=\"4\"/><path d=\"M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4\"/></svg>切换主题</button>\n      <div class=\"verline\" id=\"verLine\"></div>\n    </div>\n  </aside>\n\n  <main class=\"main\">\n    <div class=\"topbar\">\n      <div><h1 class=\"page-title\" id=\"pageTitle\">概览</h1><div class=\"page-sub\" id=\"pageSub\">Hub 里有什么、健康吗、最近做了什么</div></div>\n      <div class=\"spacer\"></div>\n      <button class=\"btn\" id=\"refreshBtn\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M3 12a9 9 0 1 0 3-6.7\"/><path d=\"M3 4v5h5\"/></svg>刷新</button>\n      <div class=\"chip\"><span class=\"dot\"></span>本机 · 127.0.0.1</div>\n    </div>\n    <div class=\"loadbar\" id=\"loadbar\" hidden><span class=\"spinner\"></span><span id=\"loadbarText\">正在加载…</span></div>\n\n    <section class=\"view active\" id=\"view-overview\">\n      <div class=\"grid g4\" id=\"ovCards\"></div>\n      <div class=\"section\" id=\"ovDoctor\"></div>\n      <div class=\"section grid g2\">\n        <div class=\"panel\"><h3>Hub 内容</h3><div class=\"faint\">技能真源在 Hub 目录，宿主目录通过链接分发。</div>\n          <label class=\"search section\" style=\"min-width:100%\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg><input id=\"ovSkillFilter\" placeholder=\"过滤技能（输入后显示全部匹配）\"></label>\n          <div class=\"list\" id=\"ovSkills\"></div>\n        </div>\n        <div class=\"panel\"><h3>最近动作</h3><div class=\"faint\">收编 / 链接 / 解除都写入 Hub 审计。</div><div class=\"list\" id=\"ovAudit\"></div></div>\n      </div>\n      <div class=\"section panel\">\n        <h3>Hub 位置</h3>\n        <div class=\"mono\" id=\"ovHubDir\">-</div>\n        <div class=\"faint\" id=\"ovHubMeta\"></div>\n        <div class=\"toolbar section\">\n          <button class=\"btn small\" data-goto=\"adopt\">去收编</button>\n          <button class=\"btn small\" data-goto=\"links\">去链接与体检</button>\n          <button class=\"btn small\" data-goto=\"records\">查看记录</button>\n          <button class=\"btn small\" id=\"copyHubDir\">复制路径</button>\n          <button class=\"btn small\" id=\"hubConfigBtn\">设置新位置</button>\n          <button class=\"btn small\" id=\"hubConfigClearBtn\" hidden title=\"清除持久 Hub 位置覆盖，回落默认解析；当前 Hub 有技能时会先展示影响面\">清除覆盖</button>\n        </div>\n      </div>\n      <div class=\"section\" id=\"ovSwitchBanner\" hidden></div>\n      <div class=\"section panel\" id=\"ovMigration\" hidden>\n        <h3>最近一次迁移</h3>\n        <div id=\"ovMigrationBody\"></div>\n        <div class=\"toolbar section\">\n          <button class=\"btn small danger\" id=\"migrationRollbackBtn\">回滚到原位置</button>\n          <button class=\"btn small\" id=\"copyMigrationTrash\">复制回收站路径</button>\n        </div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-hosts\">\n      <div class=\"toolbar\">\n        <label class=\"search\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg><input id=\"hostSearch\" placeholder=\"过滤宿主 / 目录\"></label>\n        <div class=\"chips\" id=\"hostStateChips\"></div>\n        <button class=\"btn small\" id=\"hostAddBtn\">添加自定义目录</button>\n      </div>\n      <details class=\"glossary section\">\n        <summary>术语速查</summary>\n        <div class=\"glossary-body\">\n          <div><b>可用</b>：宿主实体确认、技能目录存在（默认分发范围）。</div>\n          <div><b>残留</b>：宿主实体未确认（疑似已卸载）；可用「清理」把目录移入回收站。</div>\n          <div><b>仅标记</b>：检测到宿主已安装，但技能目录尚未创建。</div>\n          <div><b>隐藏标记</b>：只影响列表显示，不拦截任何行为（ignored）。</div>\n          <div><b>不接管</b>：发现 / 显示 / 链接三层全部跳过；已有链接不动（真正拦截行为的开关）。</div>\n          <div><b>清理</b>：解除指向 Hub 的链接 + 目录移入回收站（保留 7 天可恢复）。</div>\n          <div><b>桥接</b>：锁 / 数据目录（如 XDG state），永不作为链接目标。</div>\n        </div>\n      </details>\n      <div class=\"section panel\">\n        <div class=\"faint\" id=\"hostSummary\"></div>\n        <table><thead><tr><th>宿主</th><th>技能目录</th><th>范围</th><th>目录技能</th><th title=\"只统计指向当前生效 Hub 的链接（文件系统为真源）；指向其它位置的链接单独标注（配置错位预警）\">指向当前 Hub</th><th>异常</th><th>状态</th><th></th></tr></thead><tbody id=\"hostRows\"></tbody></table>\n        <div class=\"empty\" id=\"hostEmpty\" hidden>没有匹配的宿主目录。</div>\n      </div>\n      <div class=\"section panel\"><h3>已安装标记（无技能目录的宿主）</h3><div class=\"list\" id=\"hostMarks\"></div></div>\n      <div class=\"section panel\" id=\"hostExcludedWrap\" hidden>\n        <h3>不接管名单</h3>\n        <div class=\"faint\">这些宿主 / 目录在发现、显示、链接三层全部跳过（--include-discovered 也不纳入）。</div>\n        <div class=\"list\" id=\"hostExcluded\"></div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-adopt\">\n      <div class=\"grid g4\" id=\"adoptCards\"></div>\n      <div class=\"section toolbar\">\n        <label class=\"search\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg><input id=\"adoptSearch\" placeholder=\"过滤技能 slug / 来源宿主\"></label>\n        <button class=\"btn small\" id=\"adoptAll\">全选可收编</button>\n        <button class=\"btn small\" id=\"adoptNone\">清空</button>\n        <span class=\"spacer\"></span>\n        <span class=\"label\" id=\"adoptScanInfo\"></span>\n      </div>\n      <div class=\"list\" id=\"adoptList\"></div>\n      <div class=\"empty\" id=\"adoptEmpty\" hidden>没有可收编的候选。先在宿主里安装技能，或刷新宿主矩阵。</div>\n      <div class=\"actionbar\">\n        <span class=\"label\">已选 <b id=\"adoptCount\">0</b> 项</span>\n        <span class=\"spacer\"></span>\n        <span class=\"faint\">默认复制保真、原目录保留；冲突项默认跳过；执行时逐项运行元信扫描。</span>\n        <button class=\"btn primary\" id=\"adoptApply\">收编所选</button>\n      </div>\n      <div class=\"section panel\" id=\"adoptResultsWrap\" hidden><h3>收编结果</h3><div class=\"result-list\" id=\"adoptResults\"></div></div>\n    </section>\n\n    <section class=\"view\" id=\"view-links\">\n      <div id=\"linkDoctor\"></div>\n      <div class=\"section panel\">\n        <h3>分发目标</h3>\n        <div class=\"faint\">把 Hub 技能链接到宿主目录（Windows junction / POSIX symlink）；默认范围 = 已核实宿主，自动发现目录需在 CLI 用 --include-discovered 显式纳入，锁 / 数据桥接目录永不链接；元技能链接时收敛旧副本（移入回收站，保留 7 天可恢复）。</div>\n        <div class=\"list\" id=\"linkTargets\"></div>\n      </div>\n      <div class=\"section panel\">\n        <h3>当前链接</h3>\n        <table><thead><tr><th>技能</th><th>宿主</th><th>目标</th><th>状态</th><th></th></tr></thead><tbody id=\"linkRows\"></tbody></table>\n        <div class=\"empty\" id=\"linkEmpty\" hidden>还没有任何链接。</div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-records\">\n      <div class=\"toolbar\">\n        <button class=\"btn small\" data-tab=\"snapshots\">回滚快照</button>\n        <button class=\"btn small\" data-tab=\"evidence\">安装 / 回滚证据</button>\n        <button class=\"btn small\" data-tab=\"audit\">Hub 审计</button>\n        <span class=\"spacer\"></span>\n        <span class=\"label\" id=\"recordsInfo\"></span>\n      </div>\n      <div class=\"section panel\" id=\"recSnapshots\">\n        <table><thead><tr><th>技能</th><th>版本</th><th>时间</th><th>来源目录</th><th>状态</th><th></th></tr></thead><tbody id=\"snapshotRows\"></tbody></table>\n        <div class=\"empty\" id=\"snapshotEmpty\" hidden>没有安装快照。快照由 install / update 写入。</div>\n      </div>\n      <div class=\"section panel\" id=\"recEvidence\" hidden>\n        <div class=\"list\" id=\"evidenceRows\"></div>\n        <div class=\"empty\" id=\"evidenceEmpty\" hidden>没有证据记录。</div>\n      </div>\n      <div class=\"section panel\" id=\"recAudit\" hidden>\n        <div class=\"list\" id=\"auditRows\"></div>\n        <div class=\"empty\" id=\"auditEmpty\" hidden>没有 Hub 审计记录。</div>\n      </div>\n    </section>\n\n    <section class=\"view\" id=\"view-route\">\n      <div class=\"panel\">\n        <h3>一句话需求 → 技能组合</h3>\n        <div class=\"faint\">只读调用静态 playbook（7 组）+ 动态路由块；安装建议只给命令，不在网页执行。</div>\n        <div class=\"toolbar section\">\n          <label class=\"search\" style=\"flex:1\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><circle cx=\"11\" cy=\"11\" r=\"7\"/><path d=\"m20 20-3.5-3.5\"/></svg><input id=\"routeInput\" placeholder=\"例如：帮我做发布前质量检查\"></label>\n          <button class=\"btn primary\" id=\"routeBtn\">给出组合</button>\n        </div>\n      </div>\n      <div id=\"routeResult\" class=\"section\"></div>\n    </section>\n\n    <section class=\"view\" id=\"view-cli\">\n      <div class=\"banner\">\n        <svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"m4 7 5 5-5 5\"/><path d=\"M12 19h8\"/></svg>\n        <div><div class=\"banner-title\">高级 CLI（全量）</div><div class=\"banner-body\">全部命令 + 人话说明 + 可复制示例；网页只展示与复制，不代替终端执行安装、更新与删除。</div></div>\n      </div>\n      <div class=\"section panel\">\n        <div class=\"shead\"><h2>命令速查</h2><span class=\"faint\" id=\"cliMeta\">加载中…</span></div>\n        <div id=\"cliQuick\"></div>\n      </div>\n      <div class=\"section panel\">\n        <details id=\"cliFullWrap\">\n          <summary>完整命令与参数（点击展开）</summary>\n          <div id=\"cliFull\"></div>\n        </details>\n      </div>\n    </section>\n  </main>\n</div>\n\n<div class=\"mask\" id=\"mask\"><div class=\"modal\" id=\"modal\"></div></div>\n<div class=\"toasts\" id=\"toasts\"></div>\n\n<script>\n(function () {\n  var TOKEN = (document.querySelector('meta[name=\"yotta-view-token\"]') || {}).content || '';\n  var state = { view: 'overview', overview: null, hosts: null, adopt: null, selected: {}, records: null, tab: 'snapshots', hostFilter: '', hostStateFilter: '', adoptFilter: '', ovSkillFilter: '' };\n\n  function $(sel) { return document.querySelector(sel); }\n  function esc(value) {\n    return String(value === null || value === undefined ? '' : value)\n      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')\n      .replace(/\"/g, '&quot;').replace(/'/g, '&#39;');\n  }\n  function fmtTime(value) {\n    var ms = typeof value === 'number' ? value : Date.parse(value);\n    if (!ms || isNaN(ms)) return value ? String(value) : '-';\n    var d = new Date(ms);\n    function p(n) { return n < 10 ? '0' + n : '' + n; }\n    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());\n  }\n  function toast(text) {\n    var el = document.createElement('div');\n    el.className = 'toast';\n    el.textContent = text;\n    $('#toasts').appendChild(el);\n    setTimeout(function () { el.remove(); }, 3200);\n  }\n  function copyText(text) {\n    if (navigator.clipboard && navigator.clipboard.writeText) {\n      navigator.clipboard.writeText(text).then(function () { toast('已复制'); }, function () { fallbackCopy(text); });\n    } else fallbackCopy(text);\n  }\n  function fallbackCopy(text) {\n    var ta = document.createElement('textarea');\n    ta.value = text; document.body.appendChild(ta); ta.select();\n    try { document.execCommand('copy'); toast('已复制'); } catch (e) { toast('复制失败，请手动选择'); }\n    ta.remove();\n  }\n  async function api(path, opts) {\n    opts = opts || {};\n    var init = { method: opts.method || 'GET', headers: {} };\n    if (opts.body !== undefined) {\n      init.method = 'POST';\n      init.headers['Content-Type'] = 'application/json';\n      init.headers['X-Yotta-View-Token'] = TOKEN;\n      init.body = JSON.stringify(opts.body);\n    }\n    var res, data = null;\n    try { res = await fetch(path, init); } catch (e) { return { error: '无法连接本地服务：' + e.message }; }\n    try { data = await res.json(); } catch (e) { data = null; }\n    if (!res.ok) return data && data.error ? data : { error: '请求失败（HTTP ' + res.status + '）' };\n    if (!data) return { error: '响应不是合法 JSON' };\n    return data;\n  }\n\n  function openModal(title, bodyHtml, opts) {\n    opts = opts || {};\n    var html = '<h3>' + esc(title) + '</h3><div id=\"modalBody\">' + bodyHtml + '</div>' +\n      '<div class=\"modal-actions\"><button class=\"btn\" data-modal=\"cancel\">' + esc(opts.cancelText || '取消') + '</button>' +\n      (opts.okText === null ? '' : '<button class=\"btn ' + (opts.danger ? 'danger' : 'primary') + '\" data-modal=\"ok\">' + esc(opts.okText || '确认') + '</button>') +\n      '</div>';\n    $('#modal').innerHTML = html;\n    $('#mask').classList.add('open');\n    var ok = $('#modal').querySelector('[data-modal=\"ok\"]');\n    $('#modal').querySelector('[data-modal=\"cancel\"]').onclick = closeModal;\n    if (ok && opts.onOk) {\n      ok.onclick = async function () {\n        ok.disabled = true;\n        try { await opts.onOk(); } finally { ok.disabled = false; }\n      };\n    }\n  }\n  function closeModal() { $('#mask').classList.remove('open'); $('#modal').innerHTML = ''; }\n  function confirmModal(title, bodyHtml, okText, danger, onOk) {\n    openModal(title, bodyHtml, { okText: okText, danger: danger, onOk: onOk });\n  }\n  $('#mask').addEventListener('click', function (e) { if (e.target === $('#mask')) closeModal(); });\n  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });\n\n  var VIEWS = {\n    overview: { title: '概览', sub: 'Hub 里有什么、健康吗、最近做了什么', load: loadOverview },\n    hosts: { title: '宿主矩阵', sub: '装了哪些宿主、技能目录在哪、Hub 技能链到了谁', load: loadHosts },\n    adopt: { title: '收编向导', sub: '有哪些可收编、哪些是重复副本、收编后会发生什么', load: loadAdopt },\n    links: { title: '链接与体检', sub: '断链 / 漂移 / 目标缺失在哪、怎么修', load: loadLinks },\n    records: { title: '记录与回滚', sub: '安装、收编、链接都做了什么，怎么退回', load: loadRecords },\n    route: { title: '路由与编排', sub: '一句话需求该用哪些技能、缺什么（只读）', load: null },\n    cli: { title: '高级 CLI', sub: '全量命令速查与复制（与 CLI --help 同源）', load: null }\n  };\n  var loadSeq = 0;\n  function showLoad(text) {\n    loadSeq += 1;\n    $('#loadbarText').textContent = text;\n    $('#loadbar').hidden = false;\n    $('#refreshBtn').disabled = true;\n    return loadSeq;\n  }\n  function hideLoad(seq) {\n    if (seq !== undefined && seq !== loadSeq) return;\n    $('#loadbar').hidden = true;\n    $('#refreshBtn').disabled = false;\n  }\n  async function runLoad(name) {\n    var v = VIEWS[name];\n    if (!v) return;\n    if (!v.load) { loadSeq += 1; hideLoad(); return; }\n    var seq = showLoad('正在加载' + v.title + '…');\n    try { await v.load(); } finally { hideLoad(seq); }\n  }\n  function switchView(name) {\n    if (!VIEWS[name]) return;\n    state.view = name;\n    Array.prototype.forEach.call(document.querySelectorAll('#nav button'), function (b) { b.classList.toggle('active', b.dataset.view === name); });\n    Array.prototype.forEach.call(document.querySelectorAll('.view'), function (v) { v.classList.toggle('active', v.id === 'view-' + name); });\n    $('#pageTitle').textContent = VIEWS[name].title;\n    $('#pageSub').textContent = VIEWS[name].sub;\n    runLoad(name);\n  }\n  $('#nav').addEventListener('click', function (e) {\n    var b = e.target.closest('button[data-view]');\n    if (b) switchView(b.dataset.view);\n  });\n  document.addEventListener('click', function (e) {\n    var g = e.target.closest('[data-goto]');\n    if (g) switchView(g.dataset.goto);\n  });\n  $('#refreshBtn').onclick = function () { var v = VIEWS[state.view]; if (v && v.load) runLoad(state.view); else toast('已刷新'); };\n  $('#themeBtn').onclick = function () {\n    document.body.classList.toggle('light');\n    try { localStorage.setItem('yotta-hub-theme', document.body.classList.contains('light') ? 'light' : 'dark'); } catch (e) {}\n  };\n  try { if (localStorage.getItem('yotta-hub-theme') === 'light') document.body.classList.add('light'); } catch (e) {}\n\n  function statCard(label, value, delta, tone) {\n    return '<div class=\"panel\"><div class=\"label\">' + esc(label) + '</div><div class=\"value\">' + esc(value) + '</div><div class=\"delta ' + (tone ? 'badge ' + tone : '') + '\">' + esc(delta) + '</div></div>';\n  }\n  function doctorBanner(doctor) {\n    if (!doctor) return '';\n    if (doctor.ok) {\n      return '<div class=\"banner ok\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z\"/><path d=\"m9 12 2 2 4-4\"/></svg><div><div class=\"banner-title\">体检通过</div><div class=\"banner-body\">警告 ' + doctor.summary.warnings + ' / 信息 ' + doctor.summary.info + '；结构性错误 0。</div></div></div>';\n    }\n    var bad = (doctor.checks || []).filter(function (c) { return !c.ok; }).slice(0, 6).map(function (c) {\n      return '<div class=\"result\"><span class=\"badge ' + (c.severity === 'error' ? 'danger' : 'warn') + '\">' + esc(c.severity === 'error' ? '错误' : '警告') + '</span><span>' + esc(c.message) + '</span>' + (c.hint ? '<span class=\"faint\">修复：' + esc(c.hint) + '</span>' : '') + '</div>';\n    }).join('');\n    return '<div class=\"banner danger\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 9v4\"/><path d=\"M12 17h.01\"/><path d=\"M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z\"/></svg><div style=\"flex:1\"><div class=\"banner-title\">体检未通过（错误 ' + doctor.summary.errors + ' / 警告 ' + doctor.summary.warnings + '）</div><div class=\"result-list\">' + bad + '</div></div></div>';\n  }\n\n  async function loadOverview() {\n    var d = await api('/api/overview');\n    if (d.error) { toast(d.error); return; }\n    state.overview = d;\n    $('#ovCards').innerHTML =\n      statCard('Hub 技能', d.status.summary.skills, '外部来源 ' + d.status.summary.external, '') +\n      statCard('已链接', d.status.summary.links, '宿主目录投影', 'ok') +\n      statCard('异常链接', d.status.summary.brokenLinks, d.status.summary.brokenLinks ? '需要处理' : '全部正常', d.status.summary.brokenLinks ? 'danger' : 'ok') +\n      statCard('Doctor', d.doctor.ok ? '通过' : '未通过', '错误 ' + d.doctor.summary.errors + ' / 警告 ' + d.doctor.summary.warnings, d.doctor.ok ? 'ok' : 'danger');\n    $('#ovDoctor').innerHTML = doctorBanner(d.doctor);\n    renderOverviewSkills();\n    var audit = (d.audit && d.audit.recent) || [];\n    $('#ovAudit').innerHTML = audit.length ? audit.slice().reverse().map(function (a) {\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(a.event || '动作') + ' · ' + esc(a.slug || '') + '</div><div class=\"row-meta\">' + esc(fmtTime(a.at)) + (a.verdict ? ' · ' + esc(a.verdict) : '') + '</div></div></div>';\n    }).join('') : '<div class=\"empty\">还没有动作记录。</div>';\n    $('#ovHubDir').textContent = d.hubDir;\n    $('#copyHubDir').onclick = function () { copyText(d.hubDir); };\n    var hubInfo = d.hub || {};\n    var sourceNames = { flag: '--hub 参数', env: 'YOTTA_SKILLS_HUB 环境变量', config: 'config.json 配置', default: '默认位置' };\n    var metaParts = ['来源: ' + (sourceNames[hubInfo.source] || hubInfo.source || '默认位置')];\n    if (hubInfo.configured) metaParts.push('配置覆盖: ' + hubInfo.configured);\n    if (hubInfo.restartRequired) metaParts.push('配置已指向 ' + (hubInfo.effectiveNow || '') + '，重启 view 后生效');\n    $('#ovHubMeta').textContent = metaParts.join(' · ');\n    $('#hubConfigClearBtn').hidden = !hubInfo.configured;\n    renderMigrationBlock(d);\n  }\n\n  /* 0.29.5 S1/S2：迁移向导（迁移 / 仅切换）+ 最近迁移 + 一键回滚（与 CLI 同内核） */\n  function renderMigrationBlock(d) {\n    var mig = (d.migration && d.migration.last) || null;\n    var pending = (d.migration && d.migration.switchPending) || null;\n    var banner = $('#ovSwitchBanner');\n    if (pending) {\n      banner.hidden = false;\n      banner.innerHTML = '<div class=\"banner danger\"><svg class=\"sv\" viewBox=\"0 0 24 24\"><path d=\"M12 9v4\"/><path d=\"M12 17h.01\"/><path d=\"M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z\"/></svg>' +\n        '<div><div class=\"banner-title\">旧 Hub 还有 ' + esc(pending.skills) + ' 个技能未迁移</div>' +\n        '<div class=\"banner-body\">旧位置 <span class=\"mono\">' + esc(pending.from) + '</span> · 当前位置 <span class=\"mono\">' + esc(d.hubDir) + '</span></div>' +\n        '<div class=\"toolbar section\"><button class=\"btn small primary\" id=\"switchMigrateNow\">一键迁移到当前位置</button>' +\n        '<button class=\"btn small\" id=\"switchMigrateOpen\">迁移到其它位置…</button></div></div></div>';\n      $('#switchMigrateNow').onclick = function () {\n        confirmModal('迁移旧 Hub 到当前位置？',\n          '<p class=\"label\">将把 <span class=\"mono\">' + esc(pending.from) + '</span>（' + esc(pending.skills) + ' 个技能）复制到 <span class=\"mono\">' + esc(d.hubDir) + '</span>，逐技能校验后切换配置、重链全部宿主，旧 Hub 入回收站（7 天可回滚）。</p>',\n          '开始迁移', false, async function () {\n            await executeHubMigration({ hub: d.hubDir, mode: 'move' }, { from: pending.from });\n          });\n      };\n      $('#switchMigrateOpen').onclick = function () { openHubConfigWizard(); };\n    } else {\n      banner.hidden = true;\n      banner.innerHTML = '';\n    }\n    var box = $('#ovMigration');\n    if (!mig) {\n      box.hidden = true;\n      return;\n    }\n    box.hidden = false;\n    var kind = mig.kind === 'rollback' ? '回滚' : '迁移';\n    var lines = [\n      '最近一次' + kind + '：' + esc(mig.from) + ' → ' + esc(mig.to),\n      '时间 ' + esc(fmtTime(mig.at)) + ' · 技能 ' + esc(mig.verifiedSkills) + ' · 重链 ' + esc(mig.relinkDirs) + ' 个宿主目录',\n    ];\n    if (mig.trashedTo) lines.push('回收站 ' + esc(mig.trashedTo) + '（剩余 ' + esc(mig.daysLeft) + ' 天）');\n    if (mig.incomplete > 0) lines.push('⚠ 重链未全部完成（' + esc(mig.incomplete) + ' 项）；旧 Hub 保留在 ' + esc(mig.oldHubKept || mig.from));\n    if (mig.trashError) lines.push('⚠ 旧 Hub 移入回收站失败（已保留原位）：' + esc(mig.trashError));\n    $('#ovMigrationBody').innerHTML = '<div class=\"faint\">' + lines.join('<br>') + '</div>';\n    $('#copyMigrationTrash').hidden = !mig.trashedTo;\n    $('#copyMigrationTrash').onclick = function () { copyText(mig.trashedTo); };\n    $('#migrationRollbackBtn').onclick = rollbackFlow;\n  }\n\n  function rewireModalButtons(opts) {\n    var ok = $('#modal').querySelector('[data-modal=\"ok\"]');\n    var cancel = $('#modal').querySelector('[data-modal=\"cancel\"]');\n    if (ok && opts.okText) { ok.textContent = opts.okText; ok.disabled = false; ok.onclick = opts.onOk || closeModal; }\n    if (ok && opts.hideOk) ok.hidden = true;\n    if (cancel && opts.cancelText) { cancel.textContent = opts.cancelText; cancel.onclick = opts.onCancel || closeModal; }\n  }\n\n  function showMigrationResult(result) {\n    var move = result.move || {};\n    var done = !move.incomplete && !move.trashError;\n    $('#modalBody').innerHTML =\n      '<div class=\"result\"><span class=\"badge ' + (done ? 'ok' : 'danger') + '\">' + (done ? '迁移完成' : '部分完成') + '</span><span>' + esc(result.previous || '') + ' → ' + esc(result.hub || '') + '</span></div>' +\n      '<div class=\"result\"><span class=\"badge ok\">校验</span><span>' + esc(move.verifiedSkills || 0) + ' 个技能复制校验通过</span></div>' +\n      '<div class=\"result\"><span class=\"badge ok\">重链</span><span>' + esc(move.relinkDirs || 0) + ' 个宿主目录</span></div>' +\n      (move.trashedTo ? '<div class=\"result\"><span class=\"badge ok\">旧 Hub</span><span class=\"mono\">' + esc(move.trashedTo) + '</span><span>已入回收站（7 天可恢复）</span></div>' : '') +\n      (move.incomplete > 0 ? '<div class=\"result\"><span class=\"badge danger\">重链未全部完成</span><span>旧 Hub 保留在 <span class=\"mono\">' + esc(move.oldHubKept || move.from || '') + '</span>；重跑：yotta-skills hub link --all --force</span></div>' : '') +\n      (move.trashError ? '<div class=\"result\"><span class=\"badge warn\">回收站</span><span>旧 Hub 移入回收站失败（已保留原位）：' + esc(move.trashError) + '</span></div>' : '') +\n      '<div class=\"note\">新位置从下次面板加载开始生效（已在运行的 view 需重启）。</div>';\n    rewireModalButtons({\n      okText: '关闭',\n      onOk: closeModal,\n      cancelText: '刷新面板',\n      onCancel: function () { closeModal(); loadOverview(); },\n    });\n  }\n\n  function showSwitchResult(result) {\n    $('#modalBody').innerHTML =\n      '<div class=\"result\"><span class=\"badge ok\">已切换</span><span>' + esc(result.previous || '') + ' → ' + esc(result.hub || '') + '</span></div>' +\n      ((result.oldSkills || 0) > 0\n        ? '<div class=\"result\"><span class=\"badge warn\">未迁移</span><span>旧 Hub 还有 ' + esc(result.oldSkills) + ' 个技能未迁移；概览会持续提示，可一键迁移。</span></div>'\n        : '') +\n      '<div class=\"note\">只切换了指针，没有移动任何文件；新位置从下次面板加载开始生效。</div>';\n    rewireModalButtons({\n      okText: '关闭',\n      onOk: closeModal,\n      cancelText: '刷新面板',\n      onCancel: function () { closeModal(); loadOverview(); },\n    });\n  }\n\n  async function executeHubMigration(body, opts) {\n    opts = opts || {};\n    var seq = showLoad(body.mode === 'switch' ? '正在切换 Hub 位置…' : '正在迁移 Hub（复制 → 校验 → 重链 → 回收站）…');\n    var payload = Object.assign({ confirm: 'hub-config' }, body);\n    if (opts.from) payload = Object.assign(payload, { from: opts.from });\n    var r = await api('/api/hub/config', { body: payload });\n    hideLoad(seq);\n    if (r.error) {\n      if (r.code === 'target-residue') return wizardResiduePrompt(body, r.error, opts);\n      if (opts.inModal) {\n        $('#hubWizardResult').innerHTML = '<div class=\"result\"><span class=\"badge danger\">失败</span><span>' + esc(r.error) + '</span></div>';\n      } else {\n        toast(r.error);\n      }\n      return null;\n    }\n    if (opts.inModal) {\n      if (body.mode === 'switch') showSwitchResult(r);\n      else showMigrationResult(r);\n    }\n    else {\n      closeModal();\n      toast('迁移完成：校验 ' + ((r.move && r.move.verifiedSkills) || 0) + ' 个技能 · 重链 ' + ((r.move && r.move.relinkDirs) || 0) + ' 个目录' + (r.move && r.move.incomplete ? '（重链未全部完成，见概览提示）' : ''));\n      loadOverview();\n    }\n    return r;\n  }\n\n  function wizardResiduePrompt(body, error, opts) {\n    var host = opts && opts.inModal ? $('#hubWizardResult') : $('#modalBody');\n    if (!host) { toast(error); return; }\n    host.innerHTML = '<div class=\"result\"><span class=\"badge warn\">残留</span><span>' + esc(error) + '</span></div>' +\n      '<button class=\"btn small primary\" id=\"hubResidueClean\">清理残留并迁移</button>';\n    $('#hubResidueClean').onclick = async function () {\n      var seq = showLoad('正在清理残留并迁移…');\n      var payload = Object.assign({ confirm: 'hub-config', cleanResidue: true }, body);\n      if (opts && opts.from) payload.from = opts.from;\n      var r = await api('/api/hub/config', { body: payload });\n      hideLoad(seq);\n      if (r.error) { toast(r.error); return; }\n      if (opts && opts.inModal) showMigrationResult(r);\n      else { closeModal(); toast('迁移完成'); loadOverview(); }\n    };\n  }\n\n  function openHubConfigWizard() {\n    var d = state.overview || {};\n    var current = d.hubDir || '';\n    var skillCount = (d.status && d.status.summary && d.status.summary.skills) || 0;\n    var body = '<p class=\"label\">写入 config.json 持久覆盖（优先级低于 --hub 参数 / YOTTA_SKILLS_HUB）。</p>' +\n      '<label class=\"label\">新的 Hub 目录</label>' +\n      '<input id=\"hubNewPath\" placeholder=\"D:\\\\my-hub\" value=\"\">' +\n      '<div class=\"note mono\">当前: ' + esc(current) + '（' + esc(skillCount) + ' 个技能）</div>' +\n      '<div class=\"section\"><label class=\"label\"><input type=\"radio\" name=\"hubMode\" value=\"move\" checked style=\"width:auto\"> 迁移到新位置（推荐）</label>' +\n      '<div class=\"faint\">复制 → 逐技能校验 → 切换配置 → 全宿主重链 → 旧 Hub 入回收站（7 天可回滚）。</div>' +\n      '<label class=\"label section\"><input type=\"radio\" name=\"hubMode\" value=\"switch\" style=\"width:auto\"> 仅切换位置（保留旧内容）</label>' +\n      '<div class=\"faint\">只改指针，不移动任何文件；旧 Hub 内容保留，概览会提示未迁移。</div></div>' +\n      '<div id=\"hubWizardResult\" class=\"section\"></div>';\n    openModal('设置 Hub 位置', body, {\n      okText: '执行',\n      onOk: async function () {\n        var value = ($('#hubNewPath').value || '').trim();\n        if (!value) { toast('先填写新的 Hub 目录'); return; }\n        var mode = document.querySelector('input[name=\"hubMode\"]:checked').value;\n        if (mode === 'switch' && skillCount > 0) {\n          $('#hubWizardResult').innerHTML = '<div class=\"result\"><span class=\"badge warn\">确认</span><span>旧 Hub 还有 ' + esc(skillCount) + ' 个技能未迁移。仅切换位置不会移动它们。</span></div>' +\n            '<button class=\"btn small danger\" id=\"hubSwitchConfirm\">确认仅切换</button>';\n          $('#hubSwitchConfirm').onclick = function () { executeHubMigration({ hub: value, mode: 'switch' }, { inModal: true }); };\n          return;\n        }\n        await executeHubMigration({ hub: value, mode: mode }, { inModal: true });\n      },\n    });\n  }\n\n  function rollbackFlow() {\n    api('/api/hub/config').then(function (d) {\n      if (d.error) { toast(d.error); return; }\n      var rb = d.rollback || {};\n      if (!rb.lastMigration) { toast('没有可回滚的迁移记录'); return; }\n      if (!rb.ok) {\n        confirmModal('回滚被阻断', '<p class=\"label\">' + esc((rb.blocked || []).join('；') || rb.error || '') + '</p><div class=\"note\">回滚 fail-closed（不合并）；处理阻断项后重试。</div>', null, true, null);\n        return;\n      }\n      confirmModal('回滚 Hub 位置？',\n        '<p class=\"label\">将把当前 Hub 内容复制回原位置：<span class=\"mono\">' + esc(rb.current) + '</span> → <span class=\"mono\">' + esc(rb.target) + '</span>（复制校验 → 切换 → 重链 → 当前 Hub 入回收站 7 天）。</p>' +\n        '<div class=\"note\">位置回退（用当前内容），不是恢复旧快照。</div>',\n        '执行回滚', true, async function () {\n          var seq = showLoad('正在回滚 Hub 位置（复制 → 校验 → 重链 → 回收站）…');\n          var r = await api('/api/hub/config', { body: { rollback: true, confirm: 'hub-config' } });\n          hideLoad(seq);\n          if (r.error) {\n            if (r.code === 'target-residue') { wizardResiduePrompt({ rollback: true }, r.error, {}); return; }\n            toast(r.error); return;\n          }\n          closeModal();\n          toast('回滚完成：' + ((r.move && r.move.verifiedSkills) || 0) + ' 个技能已回到 ' + (r.hub || ''));\n          loadOverview();\n        });\n    });\n  }\n\n  $('#hubConfigBtn').onclick = openHubConfigWizard;\n  $('#hubConfigClearBtn').onclick = function () {\n    var d = state.overview || {};\n    var hubInfo = d.hub || {};\n    var skills = (d.status && d.status.summary && d.status.summary.skills) || 0;\n    var body = '<p class=\"label\">将删除 config.json 中的 Hub 覆盖，恢复 --hub &gt; 环境变量 &gt; 默认位置的解析。不会移动任何文件。</p>' +\n      '<div class=\"result\"><span class=\"badge warn\">影响面</span><b>' + esc(skills) + '</b><span>个技能与已建链接仍在 <span class=\"mono\">' + esc(hubInfo.configured || d.hubDir || '') + '</span>；清除后生效位置回落到默认 <span class=\"mono\">' + esc(hubInfo.defaultDir || '默认位置') + '</span>（可能是空目录），面板 / CLI 将按新位置工作。</span></div>' +\n      '<p class=\"faint\">替代路径：迁移到默认位置或其它位置，用「设置新位置」向导（等价 CLI hub config set --hub &lt;路径&gt; --move）。</p>';\n    if (skills > 0) {\n      body += '<div class=\"section\"><label class=\"label\">输入 clear 确认（当前 Hub 有技能）：</label><input id=\"hubClearConfirm\" placeholder=\"clear\"></div>';\n    }\n    confirmModal('清除 Hub 位置覆盖？', body, '清除覆盖', true, async function () {\n      if (skills > 0) {\n        var typed = ($('#hubClearConfirm') && $('#hubClearConfirm').value || '').trim();\n        if (typed !== 'clear') { toast('确认串不匹配（输入 clear）'); return; }\n      }\n      var r = await api('/api/hub/config', { body: { clear: true, confirm: 'hub-config' } });\n      if (r.error) { toast(r.error); return; }\n      closeModal();\n      toast('已清除覆盖；重启 view 后生效');\n      loadOverview();\n    });\n  };\n\n  function renderOverviewSkills() {\n    var d = state.overview;\n    if (!d) return;\n    var skills = (d.status && d.status.skills) || [];\n    var filter = state.ovSkillFilter.trim().toLowerCase();\n    var list = filter\n      ? skills.filter(function (s) { return String(s.slug || '').toLowerCase().indexOf(filter) >= 0; })\n      : skills.slice(0, 8);\n    $('#ovSkills').innerHTML = list.length ? list.map(function (s) {\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(s.slug) + '</div><div class=\"row-meta\">v' + esc(s.version || '-') + ' · ' + esc(s.origin === 'external' ? '外部来源' : '元阁家族') + ' · 链接 ' + (s.links || []).length + '</div></div>' +\n        '<span class=\"badge ' + (s.status === 'present' ? 'ok' : 'danger') + '\">' + esc(s.status === 'present' ? '已入库' : '缺失') + '</span>' +\n        '<div class=\"row-actions\"><button class=\"btn small danger\" data-remove-skill=\"' + esc(s.slug) + '\">删除</button></div></div>';\n    }).join('') : '<div class=\"empty\">' + (filter ? '没有匹配的技能。' : 'Hub 还是空的。先在「收编向导」把已装技能收编进来。') + '</div>';\n  }\n  $('#ovSkillFilter').addEventListener('input', function () {\n    state.ovSkillFilter = $('#ovSkillFilter').value || '';\n    renderOverviewSkills();\n  });\n  $('#ovSkills').addEventListener('click', async function (e) {\n    var b = e.target.closest('[data-remove-skill]');\n    if (!b) return;\n    var slug = b.dataset.removeSkill;\n    var plan = await api('/api/skills/remove-plan?slug=' + encodeURIComponent(slug));\n    if (!plan || plan.error) { toast((plan && plan.error) || '影响预览失败'); return; }\n    var targets = plan.targets || [];\n    var willUnlink = targets.filter(function (t) { return t.action === 'unlink'; });\n    var kept = targets.filter(function (t) { return t.action === 'keep'; });\n    var rows = targets.map(function (t) {\n      var tone = t.action === 'unlink' ? 'warn' : t.action === 'keep' ? 'info' : '';\n      return '<div class=\"result\"><span class=\"badge ' + tone + '\">' + esc(t.action === 'unlink' ? '将清理' : t.action === 'keep' ? '保留' : '无动作') + '</span><span class=\"mono\">' + esc(t.dir) + '</span><span class=\"faint\">' + esc(t.note || '') + '</span></div>';\n    }).join('');\n    var body = '<p class=\"label\">将清理 ' + willUnlink.length + ' 条宿主链接（含死链）' +\n      (plan.hubPresent ? '，并把 Hub 目录移入回收站（保留 7 天）' : '；Hub 目录已缺失，仅清理残留') +\n      '；保留 ' + kept.length + ' 项宿主真副本 / 外部链接。</p>' +\n      '<div class=\"result-list\">' + (rows || '<div class=\"faint\">没有需要处理的宿主目录。</div>') + '</div>' +\n      '<div class=\"section\"><label class=\"label\">输入完整技能名确认：' + esc(slug) + '</label><input id=\"removeConfirmSlug\" placeholder=\"' + esc(slug) + '\"></div>';\n    confirmModal('删除 Hub 技能 ' + slug + '？', body, '删除', true, async function () {\n      var typed = ($('#removeConfirmSlug') && $('#removeConfirmSlug').value || '').trim();\n      if (typed !== slug) { toast('技能名不匹配'); return; }\n      var r = await api('/api/skills/remove', { body: { slug: slug, confirm: 'remove', confirmSlug: typed } });\n      if (r.error) { toast(r.error); return; }\n      closeModal();\n      toast(r.verdict === 'cleanup-only' ? '已清理残留（Hub 目录原本缺失）' : '已删除 ' + slug + '（目录已入回收站）');\n      loadOverview();\n    });\n  });\n\n  async function loadHosts() {\n    var d = await api('/api/hosts');\n    if (d.error) { toast(d.error); return; }\n    state.hosts = d;\n    var s = d.summary.states || {};\n    $('#hostSummary').textContent = '可用 ' + (s.available || 0) + ' · 残留 ' + (s.orphan || 0) + ' · 未创建 ' + (s.missing || 0) + ' · 仅标记 ' + (s.markerOnly || 0) + (s.ignored ? ' · 隐藏标记 ' + s.ignored : '') + (d.summary.excluded ? ' · 不接管 ' + d.summary.excluded : '') + ' · 链接 ' + d.summary.links + '（异常 ' + d.summary.brokenLinks + '）' + (d.summary.otherHubLinks ? ' · 指向其它 Hub ' + d.summary.otherHubLinks : '');\n    renderHostStateChips();\n    renderHosts();\n    var marks = d.unpaired || [];\n    $('#hostMarks').innerHTML = marks.length ? marks.map(function (m) {\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(m.label) + '</div><div class=\"row-meta\">' + esc(m.source || '') + ' · 未发现技能目录</div></div><span class=\"badge info\">仅标记</span></div>';\n    }).join('') : '<div class=\"empty\">没有未配对的宿主标记。</div>';\n    renderHostExcluded(d.excluded || []);\n  }\n  function renderHostExcluded(list) {\n    $('#hostExcludedWrap').hidden = list.length === 0;\n    $('#hostExcluded').innerHTML = list.map(function (item) {\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(item.label || item.value) + '</div><div class=\"row-meta mono\">' + esc(item.value) + ' · ' + esc(item.kind === 'agent' ? '智能体' : '目录') + '</div></div><div class=\"row-actions\"><button class=\"btn small\" data-host-include=\"' + esc(item.value) + '\">恢复接管</button></div></div>';\n    }).join('');\n  }\n  function renderHostStateChips() {\n    var d = state.hosts; if (!d) return;\n    var s = d.summary.states || {};\n    var chips = [\n      ['', '全部'],\n      ['available', '可用 ' + (s.available || 0)],\n      ['orphan', '残留 ' + (s.orphan || 0)],\n      ['missing', '未创建 ' + (s.missing || 0)],\n      ['marker-only', '仅标记 ' + (s.markerOnly || 0)],\n      ['ignored', '隐藏标记 ' + (s.ignored || 0)],\n    ];\n    $('#hostStateChips').innerHTML = chips.map(function (c) {\n      return '<button class=\"chip' + (state.hostStateFilter === c[0] ? ' active' : '') + '\" data-host-state=\"' + esc(c[0]) + '\">' + esc(c[1]) + '</button>';\n    }).join('');\n  }\n  function hostStateBadge(h) {\n    if (h.bridgeOnly) return '<span class=\"badge info\">桥接</span>';\n    var map = { available: ['ok', '可用'], orphan: ['warn', '残留'], missing: ['', '未创建'], 'marker-only': ['info', '仅标记'], ignored: ['', '隐藏标记'] };\n    var item = map[h.state] || ['', h.state || '未知'];\n    return '<span class=\"badge ' + item[0] + '\">' + esc(item[1]) + (h.stateSource === 'manual' ? '·手动' : '') + '</span>' + (h.brokenLinks ? ' <span class=\"badge danger\">异常</span>' : '');\n  }\n  function renderHosts() {\n    var d = state.hosts; if (!d) return;\n    var q = state.hostFilter.toLowerCase();\n    var sf = state.hostStateFilter;\n    var rows = (d.hosts || []).filter(function (h) {\n      if (sf && h.state !== sf) return false;\n      if (!q) return true;\n      return String(h.label || '').toLowerCase().includes(q) || String(h.dir || '').toLowerCase().includes(q);\n    });\n    $('#hostEmpty').hidden = rows.length > 0;\n    var overrideIds = {};\n    ((d.overrides) || []).forEach(function (o) { overrideIds[String(o.agentId).toLowerCase()] = true; });\n    $('#hostRows').innerHTML = rows.map(function (h) {\n      var scopeBadge = h.bridgeOnly ? '<span class=\"badge info\">桥接·不链</span>'\n        : (h.detection === 'user-registry' ? '<span class=\"badge info\">用户注册</span>'\n        : (h.detection === 'override' ? '<span class=\"badge ok\">目录覆盖</span>'\n        : (h.verified ? '<span class=\"badge ok\">已核实</span>'\n        : ((h.detection === 'discovered' || h.detection === 'workspace') ? '<span class=\"badge warn\">自动发现</span>' : '<span class=\"badge warn\">映射·未核实</span>'))));\n      var action = '';\n      if (h.exists && h.state === 'orphan' && !h.bridgeOnly) action += '<button class=\"btn small danger\" data-host-purge=\"' + esc(h.dir) + '\" title=\"清理残留：解除指向 Hub 的链接 + 目录移入回收站（7 天可恢复）\">清理</button> ';\n      if (h.state === 'ignored') action += '<button class=\"btn small\" data-host-mark=\"' + esc(h.dir) + '\" data-mark-state=\"available\" title=\"恢复为可用状态（仅状态标记）\">标记可用</button> ';\n      else if (h.exists && !h.bridgeOnly) action += '<button class=\"btn small\" data-host-mark=\"' + esc(h.dir) + '\" data-mark-state=\"ignored\" title=\"只影响列表显示，不拦截行为（拦截用「不接管」）\">隐藏标记</button> ';\n      if (h.agentId && !h.bridgeOnly) {\n        if (overrideIds[String(h.agentId).toLowerCase()]) action += '<button class=\"btn small\" data-host-clear=\"' + esc(h.agentId) + '\" title=\"删除目录覆盖，恢复内置映射\">恢复默认</button> ';\n        else action += '<button class=\"btn small\" data-host-edit=\"' + esc(h.agentId) + '\" data-host-dir=\"' + esc(h.dir) + '\" data-host-label=\"' + esc(h.label) + '\" title=\"写入目录覆盖（hosts.json），不改宿主配置\">编辑目录</button> ';\n      }\n      if (!h.bridgeOnly) action += '<button class=\"btn small\" data-host-exclude=\"' + esc(h.agentId || h.dir) + '\" data-host-links=\"' + esc(h.hubLinks || 0) + '\" title=\"加入不接管名单：发现 / 显示 / 链接三层跳过；已有链接不动\">不接管</button> ';\n      if (h.detection === 'user-registry') action += '<button class=\"btn small\" data-host-rename=\"' + esc(h.dir) + '\" data-host-label=\"' + esc(h.label) + '\" title=\"只改显示名；目录与手动状态保持\">重命名</button> ';\n      if (h.detection === 'user-registry') action += '<button class=\"btn small\" data-host-unregister=\"' + esc(h.dir) + '\" data-host-links=\"' + esc(h.hubLinks || 0) + '\" title=\"只移除注册，不删目录；已有链接不清理（用 hub unlink --dir）\">移除注册</button>';\n      var linksCell = esc(h.hubLinks || 0);\n      if (h.hubLinksOther) {\n        var otherTitle = '指向其它位置的链接（配置错位预警）' + ((h.hubLinksOtherRoots || []).length ? '：' + h.hubLinksOtherRoots.join(' / ') : '');\n        linksCell += ' <span class=\"badge warn\" title=\"' + esc(otherTitle) + '\">其它 Hub ' + esc(h.hubLinksOther) + '</span>';\n      }\n      return '<tr><td><div class=\"cell-main\">' + esc(h.label) + '</div><div class=\"cell-sub\">' + esc(h.agentId || (h.known ? '已知宿主' : h.detection || '自动发现')) + '</div></td>' +\n        '<td><div class=\"mono\">' + esc(h.dir) + '</div><button class=\"btn small\" data-copy=\"' + esc(h.dir) + '\">复制</button></td>' +\n        '<td>' + scopeBadge + '</td>' +\n        '<td>' + esc(h.skillCount || 0) + '</td><td>' + linksCell + '</td><td>' + esc(h.brokenLinks || 0) + '</td><td>' + hostStateBadge(h) + '</td><td>' + action + '</td></tr>';\n    }).join('');\n  }\n  $('#hostSearch').addEventListener('input', function (e) { state.hostFilter = e.target.value; renderHosts(); });\n  $('#hostStateChips').addEventListener('click', function (e) {\n    var b = e.target.closest('[data-host-state]');\n    if (!b) return;\n    state.hostStateFilter = b.dataset.hostState;\n    renderHostStateChips();\n    renderHosts();\n  });\n  $('#hostAddBtn').addEventListener('click', function () {\n    var body = '<p class=\"label\">注册自定义宿主目录：纳入发现 / 分发 / 收编。不创建目录、不改宿主配置。</p>' +\n      '<div class=\"section\"><label class=\"label\">目录（必须已存在）</label><input id=\"hostAddDir\" placeholder=\"例如 D:\\\\my-agent\\\\skills\"></div>' +\n      '<div class=\"section\"><label class=\"label\">名称（可选，默认目录名）</label><input id=\"hostAddLabel\" placeholder=\"我的宿主\"></div>';\n    openModal('添加自定义目录', body, {\n      okText: '注册',\n      onOk: async function () {\n        var dir = ($('#hostAddDir') && $('#hostAddDir').value || '').trim();\n        var label = ($('#hostAddLabel') && $('#hostAddLabel').value || '').trim();\n        if (!dir) { toast('请填写目录'); return; }\n        var r = await api('/api/hosts/add', { body: { dir: dir, label: label } });\n        if (r.error) { toast(r.error); return; }\n        closeModal();\n        toast('已注册：' + ((r.entry && r.entry.label) || dir));\n        loadHosts();\n      },\n    });\n  });\n  async function openHostPurgeModal(dir) {\n    var plan = await api('/api/hosts/purge-plan?dir=' + encodeURIComponent(dir));\n    if (plan.error) { toast(plan.error); return; }\n    var body = '<p class=\"label\">只删除指向 Hub 的链接（含死链）；非 Hub 链接 / 非技能内容随目录保留在回收站（7 天可恢复）。</p>' +\n      '<div class=\"result\"><span class=\"badge warn\">将解除链接</span><b>' + esc(plan.unlinkCount) + '</b><span>条（保留 ' + esc(plan.keptLinks) + ' 非 Hub 链接 / ' + esc(plan.keptEntries) + ' 非链接内容）</span></div>' +\n      '<div class=\"mono\">' + esc(dir) + '</div>' +\n      '<div class=\"section\"><label class=\"label\">输入 purge 确认执行：</label><input id=\"hostPurgeConfirm\" placeholder=\"purge\"></div>';\n    confirmModal('清理残留目录？', body, '清理（移入回收站）', true, async function () {\n      var typed = ($('#hostPurgeConfirm') && $('#hostPurgeConfirm').value || '').trim();\n      if (typed !== 'purge') { toast('确认串不匹配（输入 purge）'); return; }\n      var r = await api('/api/hosts/purge', { body: { dir: dir, confirm: 'purge' } });\n      if (r.error) { toast(r.error); return; }\n      closeModal();\n      toast('已清理：解除 ' + r.unlinkCount + ' 条链接；回收站保留 7 天');\n      loadHosts();\n    });\n  }\n  function openHostEditModal(agentId, dir, label) {\n    var body = '<p class=\"label\">覆盖「' + esc(label) + '」的技能目录（写入 hosts.json，不改宿主配置）。被覆盖的旧目录不再进入默认发现 / 链接。</p>' +\n      '<div class=\"section\"><label class=\"label\">新目录（必须已存在）</label><input id=\"hostEditDir\" value=\"' + esc(dir) + '\"></div>';\n    openModal('编辑目录 · ' + esc(agentId), body, {\n      okText: '保存覆盖',\n      onOk: async function () {\n        var value = ($('#hostEditDir') && $('#hostEditDir').value || '').trim();\n        if (!value) { toast('请填写目录'); return; }\n        var r = await api('/api/hosts/set', { body: { agentId: agentId, dir: value } });\n        if (r.error) { toast(r.error); return; }\n        closeModal();\n        toast('已覆盖目录');\n        loadHosts();\n      },\n    });\n  }\n  $('#hostRows').addEventListener('click', async function (e) {\n    var copyBtn = e.target.closest('[data-copy]');\n    if (copyBtn) { copyText(copyBtn.dataset.copy); return; }\n    var purgeBtn = e.target.closest('[data-host-purge]');\n    if (purgeBtn) { openHostPurgeModal(purgeBtn.dataset.hostPurge); return; }\n    var editBtn = e.target.closest('[data-host-edit]');\n    if (editBtn) {\n      openHostEditModal(editBtn.dataset.hostEdit, editBtn.dataset.hostDir, editBtn.dataset.hostLabel);\n      return;\n    }\n    var clearBtn = e.target.closest('[data-host-clear]');\n    if (clearBtn) {\n      var clearAgent = clearBtn.dataset.hostClear;\n      confirmModal('恢复默认目录？', '<p class=\"label\">删除目录覆盖，恢复内置映射。</p><div class=\"mono\">' + esc(clearAgent) + '</div>', '恢复默认', false, async function () {\n        var r = await api('/api/hosts/set', { body: { agentId: clearAgent, clear: true } });\n        if (r.error) { toast(r.error); return; }\n        closeModal();\n        toast('已恢复内置映射');\n        loadHosts();\n      });\n      return;\n    }\n    var renameBtn = e.target.closest('[data-host-rename]');\n    if (renameBtn) {\n      var renameDir = renameBtn.dataset.hostRename;\n      var oldLabel = renameBtn.dataset.hostLabel;\n      openModal('重命名宿主 · ' + esc(oldLabel),\n        '<p class=\"label\">只改显示名；目录、手动状态与目录覆盖保持不动。</p>' +\n        '<div class=\"section\"><label class=\"label\">新名称</label><input id=\"hostRenameLabel\" value=\"' + esc(oldLabel) + '\"></div>', {\n        okText: '保存',\n        onOk: async function () {\n          var value = ($('#hostRenameLabel') && $('#hostRenameLabel').value || '').trim();\n          if (!value) { toast('请填写新名称'); return; }\n          var r = await api('/api/hosts/rename', { body: { dir: renameDir, label: value } });\n          if (r.error) { toast(r.error); return; }\n          closeModal();\n          toast('已重命名：' + (r.previous ? r.previous + ' → ' : '') + value);\n          loadHosts();\n        },\n      });\n      return;\n    }\n    var excludeBtn = e.target.closest('[data-host-exclude]');\n    if (excludeBtn) {\n      var excludeTarget = excludeBtn.dataset.hostExclude;\n      var excludeLinks = Number(excludeBtn.dataset.hostLinks || 0);\n      var excludeBody = '<p class=\"label\">该宿主 / 目录将从发现、显示、链接三层全部跳过（--include-discovered 也不纳入）；已有链接不受影响。</p>' +\n        (excludeLinks > 0\n          ? '<div class=\"result\"><span class=\"badge warn\">影响面</span><b>' + esc(excludeLinks) + '</b><span>条链接仍在该目录（用 hub unlink --dir 或「链接与体检」逐条解除）</span></div>'\n          : '<p class=\"faint\">该目录当前没有指向 Hub 的链接。</p>') +\n        '<div class=\"mono\">' + esc(excludeTarget) + '</div>';\n      confirmModal('加入「不接管」名单？', excludeBody, '不接管', false, async function () {\n        var r = await api('/api/hosts/exclude', { body: { target: excludeTarget } });\n        if (r.error) { toast(r.error); return; }\n        closeModal();\n        toast('已加入不接管名单');\n        loadHosts();\n      });\n      return;\n    }\n    var markBtn = e.target.closest('[data-host-mark]');\n    if (markBtn) {\n      var r = await api('/api/hosts/mark', { body: { dir: markBtn.dataset.hostMark, state: markBtn.dataset.markState } });\n      if (r.error) { toast(r.error); return; }\n      var markLabels = { available: '可用', orphan: '残留', ignored: '隐藏标记' };\n      toast('已标记：' + (markLabels[markBtn.dataset.markState] || markBtn.dataset.markState));\n      loadHosts();\n      return;\n    }\n    var unregBtn = e.target.closest('[data-host-unregister]');\n    if (unregBtn) {\n      var dir = unregBtn.dataset.hostUnregister;\n      var unregLinks = Number(unregBtn.dataset.hostLinks || 0);\n      var unregBody = '<p class=\"label\">只移除自定义宿主注册，不删除目录、不改宿主配置。</p>' +\n        (unregLinks > 0\n          ? '<div class=\"result\"><span class=\"badge warn\">影响面</span><b>' + esc(unregLinks) + '</b><span>条链接仍在该目录（移除注册不清理链接；用 hub unlink --dir 清理）</span></div>'\n          : '<p class=\"faint\">该目录当前没有指向 Hub 的链接。</p>') +\n        '<div class=\"mono\">' + esc(dir) + '</div>';\n      confirmModal('移除注册？', unregBody, '移除注册', false, async function () {\n        var r = await api('/api/hosts/remove', { body: { dir: dir } });\n        if (r.error) { toast(r.error); return; }\n        closeModal();\n        toast('已移除注册（目录保留）');\n        loadHosts();\n      });\n    }\n  });\n  $('#hostExcluded').addEventListener('click', async function (e) {\n    var includeBtn = e.target.closest('[data-host-include]');\n    if (!includeBtn) return;\n    var r = await api('/api/hosts/include', { body: { target: includeBtn.dataset.hostInclude } });\n    if (r.error) { toast(r.error); return; }\n    toast('已恢复接管');\n    loadHosts();\n  });\n\n  async function loadAdopt() {\n    var d = await api('/api/adopt/scan');\n    if (d.error) { toast(d.error); return; }\n    state.adopt = d;\n    state.selected = {};\n    $('#adoptCards').innerHTML =\n      statCard('候选技能', d.summary.candidates, '已装宿主里的技能', '') +\n      statCard('多副本冲突', d.summary.conflicts, '版本 / 哈希不一致', d.summary.conflicts ? 'warn' : 'ok') +\n      statCard('已在 Hub', d.summary.alreadyInHub, '默认跳过', 'info') +\n      statCard('扫描引擎', d.scan && d.scan.available ? '可用' : '未找到', d.scan && d.scan.available ? '收编时逐项扫描' : '可显式降级（CLI）', d.scan && d.scan.available ? 'ok' : 'warn');\n    $('#adoptScanInfo').textContent = '生成于 ' + fmtTime(d.generatedAt);\n    renderAdopt();\n  }\n  function renderAdopt() {\n    var d = state.adopt; if (!d) return;\n    var q = state.adoptFilter.toLowerCase();\n    var candidates = (d.candidates || []).filter(function (c) {\n      if (!q) return true;\n      return String(c.slug || '').toLowerCase().includes(q) || String(c.sourceHost || '').toLowerCase().includes(q);\n    });\n    $('#adoptEmpty').hidden = candidates.length > 0;\n    $('#adoptList').innerHTML = candidates.map(function (c) {\n      var variants = (c.variants || []).map(function (v) {\n        return '<div class=\"variant\"><span class=\"badge\">' + esc(v.host) + '</span><span class=\"mono\">' + esc(v.dir) + '</span><span>v' + esc(v.version || '-') + '</span></div>';\n      }).join('');\n      return '<div class=\"row\"><input class=\"check\" type=\"checkbox\" data-slug=\"' + esc(c.slug) + '\"' + (state.selected[c.slug] ? ' checked' : '') + (c.inHub ? ' disabled' : '') + '>' +\n        '<div class=\"row-main\"><div class=\"row-title\">' + esc(c.slug) + ' <span class=\"badge\">v' + esc(c.version || '-') + '</span>' +\n        (c.inHub ? ' <span class=\"badge info\">已在 Hub</span>' : '') +\n        (c.conflict ? ' <span class=\"badge warn\">多副本冲突</span>' : '') + '</div>' +\n        '<div class=\"row-meta\">来源：' + esc(c.sourceHost || '-') + ' · ' + esc(c.source || '') + '</div>' +\n        (c.variants && c.variants.length > 1 ? '<details><summary>' + c.variants.length + ' 个副本</summary><div class=\"variants\">' + variants + '</div></details>' : '') +\n        '</div></div>';\n    }).join('');\n    updateAdoptCount();\n  }\n  function updateAdoptCount() {\n    var n = Object.keys(state.selected).filter(function (k) { return state.selected[k]; }).length;\n    $('#adoptCount').textContent = String(n);\n    $('#adoptApply').disabled = n === 0;\n  }\n  $('#adoptSearch').addEventListener('input', function (e) { state.adoptFilter = e.target.value; renderAdopt(); });\n  $('#adoptList').addEventListener('change', function (e) {\n    var box = e.target.closest('input[data-slug]');\n    if (!box) return;\n    if (box.checked) state.selected[box.dataset.slug] = true; else delete state.selected[box.dataset.slug];\n    updateAdoptCount();\n  });\n  $('#adoptAll').onclick = function () {\n    ((state.adopt && state.adopt.candidates) || []).forEach(function (c) { if (!c.inHub) state.selected[c.slug] = true; });\n    renderAdopt();\n  };\n  $('#adoptNone').onclick = function () { state.selected = {}; renderAdopt(); };\n  $('#adoptApply').onclick = function () {\n    var slugs = Object.keys(state.selected).filter(function (k) { return state.selected[k]; });\n    if (!slugs.length) { toast('还没有选择技能'); return; }\n    var preview = slugs.slice(0, 24).join('、') + (slugs.length > 24 ? ' 等 ' + slugs.length + ' 项' : '');\n    confirmModal('收编 ' + slugs.length + ' 个技能到 Hub？', '<p class=\"label\">将复制到 Hub（原目录保留）；已在 Hub 或冲突项按默认策略处理；执行时逐项运行元信扫描，high / critical 会阻断。</p><div class=\"mono\">' + esc(preview) + '</div>', '开始收编', false, async function () {\n      var r = await api('/api/adopt/apply', { body: { include: slugs } });\n      if (r.error) { toast(r.error); return; }\n      closeModal();\n      var order = { imported: 0, blocked: 1, conflict: 2, skip: 3, error: 4 };\n      var results = (r.results || []).slice().sort(function (a, b) { return (order[a.status] || 9) - (order[b.status] || 9); });\n      $('#adoptResultsWrap').hidden = false;\n      $('#adoptResults').innerHTML = results.map(function (x) {\n        var tone = x.status === 'imported' ? 'ok' : x.status === 'error' || x.status === 'blocked' ? 'danger' : 'warn';\n        return '<div class=\"result\"><span class=\"badge ' + tone + '\">' + esc(x.status) + '</span><b>' + esc(x.slug) + '</b><span>' + esc(x.note || '') + '</span>' + (x.scanVerdict ? '<span class=\"faint\">verdict: ' + esc(x.scanVerdict) + '</span>' : '') + '</div>';\n      }).join('');\n      toast('收编完成：导入 ' + (r.summary ? r.summary.imported : 0) + ' / 阻断 ' + (r.summary ? r.summary.blocked : 0));\n      loadOverview();\n      loadAdopt();\n    });\n  };\n\n  async function loadLinks() {\n    var results = await Promise.all([api('/api/doctor'), api('/api/links'), api('/api/hosts')]);\n    var doctor = results[0], links = results[1], hosts = results[2];\n    if (doctor.error || links.error || hosts.error) { toast((doctor.error || links.error || hosts.error)); return; }\n    $('#linkDoctor').innerHTML = doctorBanner(doctor);\n    var existing = (hosts.hosts || []).filter(function (h) { return h.exists; });\n    $('#linkTargets').innerHTML = existing.length ? existing.map(function (h) {\n      var scopeBadge = h.bridgeOnly ? '<span class=\"badge info\">桥接·不链接</span>' : h.verified ? '<span class=\"badge ok\">已核实</span>' : '<span class=\"badge warn\">自动发现</span>';\n      var action = h.bridgeOnly ? '' : '<button class=\"btn small\" data-link-plan=\"' + esc(h.dir) + '\" data-label=\"' + esc(h.label) + '\">预览链接</button>';\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(h.label) + ' ' + scopeBadge + '</div><div class=\"row-meta mono\">' + esc(h.dir) + '</div><div class=\"row-meta\">目录技能 ' + esc(h.skillCount || 0) + ' · 指向当前 Hub ' + esc(h.hubLinks || 0) + (h.hubLinksOther ? ' · <span class=\"badge warn\">其它 Hub ' + esc(h.hubLinksOther) + '</span>' : '') + (h.brokenLinks ? ' · 异常 ' + h.brokenLinks : '') + '</div></div><div class=\"row-actions\">' + action + '</div></div>';\n    }).join('') : '<div class=\"empty\">尚未发现可用的宿主技能目录。</div>';\n    var rows = links.links || [];\n    $('#linkEmpty').hidden = rows.length > 0;\n    $('#linkRows').innerHTML = rows.map(function (l) {\n      var tone = l.status === 'ok' ? 'ok' : l.status === 'broken' ? 'danger' : 'warn';\n      return '<tr><td><div class=\"cell-main\">' + esc(l.slug) + '</div><div class=\"cell-sub\">' + esc(l.label || l.agent || '-') + '</div></td>' +\n        '<td class=\"mono\">' + esc(l.dir) + '</td><td class=\"mono\">' + esc(l.target) + '</td>' +\n        '<td><span class=\"badge ' + tone + '\">' + esc(l.status) + '</span></td>' +\n        '<td><button class=\"btn small danger\" data-unlink=\"' + esc(l.target) + '\" data-dir=\"' + esc(l.dir) + '\" data-slug=\"' + esc(l.slug) + '\">解除</button></td></tr>';\n    }).join('');\n  }\n  $('#linkTargets').addEventListener('click', async function (e) {\n    var b = e.target.closest('[data-link-plan]');\n    if (!b) return;\n    var dir = b.dataset.linkPlan;\n    var plan = await api('/api/links/plan?dir=' + encodeURIComponent(dir));\n    if (plan.error) { toast(plan.error); return; }\n    var would = plan.results.filter(function (r) { return r.status === 'would-link'; });\n    var converge = plan.results.filter(function (r) { return r.status === 'would-converge'; });\n    var skipped = plan.results.filter(function (r) { return r.status === 'skipped'; });\n    var conflicts = plan.results.filter(function (r) { return r.status === 'conflict'; });\n    var convergeMoves = converge.reduce(function (n, r) { return n + ((r.moves && r.moves.length) || 0); }, 0);\n    var linkable = would.length + converge.length;\n    var body = '<p class=\"label\">目标：' + esc(plan.label || '') + ' · <span class=\"mono\">' + esc(dir) + '</span></p>' +\n      '<div class=\"result\"><span class=\"badge ok\">将建立</span><b>' + linkable + '</b><span>个链接</span></div>' +\n      (converge.length ? '<div class=\"result\"><span class=\"badge warn\">将收敛</span><b>' + convergeMoves + '</b><span>份旧副本 → 回收站（保留 7 天，可恢复）：' + esc(converge.map(function (r) { return r.slug; }).join('、')) + '</span></div>' : '') +\n      (skipped.length ? '<div class=\"result\"><span class=\"badge warn\">跳过</span><b>' + skipped.length + '</b><span>项（Hub 版本旧于宿主 / 版本无法解析）：' + esc(skipped.map(function (r) { return r.slug; }).join('、')) + '</span></div>' : '') +\n      (conflicts.length ? '<div class=\"result\"><span class=\"badge warn\">跳过冲突</span><b>' + conflicts.length + '</b><span>个同名目录 / 链接（默认不覆盖）</span></div>' : '') +\n      (linkable ? '<details><summary>查看明细</summary><div class=\"variants\">' + would.concat(converge).map(function (r) { return '<div class=\"variant\"><span class=\"mono\">' + esc(r.slug) + '</span></div>'; }).join('') + '</div></details>' : '<p class=\"faint\">没有可建立的链接。</p>');\n    openModal('链接预览', body, {\n      okText: linkable ? '执行链接' : null,\n      onOk: async function () {\n        var r = await api('/api/links/apply', { body: { targetDir: dir } });\n        if (r.error) { toast(r.error); return; }\n        closeModal();\n        var done = (r.results || []).filter(function (x) { return x.status === 'linked'; }).length;\n        var moved = (r.results || []).reduce(function (n, x) { return n + ((x.moved && x.moved.length) || 0); }, 0);\n        toast('已建立 ' + done + ' 个链接' + (moved ? '；收敛 ' + moved + ' 份旧副本（回收站 7 天）' : ''));\n        loadLinks();\n      },\n    });\n  });\n  $('#linkRows').addEventListener('click', async function (e) {\n    var b = e.target.closest('[data-unlink]');\n    if (!b) return;\n    var target = b.dataset.unlink;\n    var dir = b.dataset.dir;\n    var slug = b.dataset.slug;\n    confirmModal('解除链接 ' + slug + '？', '<p class=\"label\">只删除宿主目录中的链接，Hub 真源保留。目标不是指向 Hub 的链接时会 fail-closed 拒绝。</p><div class=\"mono\">' + esc(target) + '</div>', '解除链接', true, async function () {\n      var r = await api('/api/links/remove', { body: { targetDir: dir, slugs: [slug], confirm: 'unlink' } });\n      if (r.error) { toast(r.error); return; }\n      closeModal();\n      toast('已解除 ' + slug);\n      loadLinks();\n    });\n  });\n\n  async function loadRecords() {\n    var d = await api('/api/records?limit=200');\n    if (d.error) { toast(d.error); return; }\n    state.records = d;\n    var valid = (d.snapshots || []).filter(function (s) { return s.valid; }).length;\n    $('#recordsInfo').textContent = '快照 ' + valid + ' / ' + (d.snapshots || []).length + ' · 证据 ' + (d.evidence.entries || []).length + ' · 审计 ' + (d.audit.entries || []).length;\n    renderSnapshots();\n    var ev = (d.evidence.entries || []).slice().reverse();\n    $('#evidenceEmpty').hidden = ev.length > 0;\n    $('#evidenceRows').innerHTML = ev.map(function (x) {\n      var tone = x.decision === 'ok' ? 'ok' : x.decision === 'fail' ? 'danger' : 'info';\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(x.event || 'event') + ' · ' + esc(x.skill || x.slug || '-') + '</div><div class=\"row-meta\">' + esc(fmtTime(x.ts || x.at)) + (x.version ? ' · v' + esc(x.version) : '') + (x.via ? ' · via ' + esc(x.via) : '') + '</div></div><span class=\"badge ' + tone + '\">' + esc(x.decision || '记录') + '</span></div>';\n    }).join('');\n    var aud = (d.audit.entries || []).slice().reverse();\n    $('#auditEmpty').hidden = aud.length > 0;\n    $('#auditRows').innerHTML = aud.map(function (x) {\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(x.event || 'audit') + ' · ' + esc(x.slug || '') + '</div><div class=\"row-meta\">' + esc(fmtTime(x.at)) + (x.verdict ? ' · ' + esc(x.verdict) : '') + (x.sourceHost ? ' · ' + esc(x.sourceHost) : '') + '</div></div></div>';\n    }).join('');\n  }\n  function renderSnapshots() {\n    var d = state.records; if (!d) return;\n    var rows = d.snapshots || [];\n    $('#snapshotEmpty').hidden = rows.length > 0;\n    $('#snapshotRows').innerHTML = rows.map(function (s) {\n      var canRollback = s.valid && s.source;\n      return '<tr><td><div class=\"cell-main\">' + esc(s.slug) + '</div><div class=\"cell-sub\">' + esc(s.name) + '</div></td>' +\n        '<td>v' + esc(s.version || '-') + '</td><td>' + esc(fmtTime(s.createdAt || s.mtime_ms)) + '</td><td class=\"mono\">' + esc(s.source || '-') + '</td>' +\n        '<td>' + (s.valid ? '<span class=\"badge ok\">可用</span>' : '<span class=\"badge danger\">不可用</span>') + (s.legacy ? ' <span class=\"badge warn\">旧格式</span>' : '') + (s.reason ? '<div class=\"cell-sub\">' + esc(s.reason) + '</div>' : '') + '</td>' +\n        '<td>' + (canRollback ? '<button class=\"btn small danger\" data-rollback=\"' + esc(s.path) + '\" data-slug=\"' + esc(s.slug) + '\" data-version=\"' + esc(s.version || '') + '\" data-source=\"' + esc(s.source || '') + '\">回滚</button>' : '<span class=\"faint\">CLI 处理</span>') + '</td></tr>';\n    }).join('');\n  }\n  document.querySelectorAll('#view-records [data-tab]').forEach(function (b) {\n    b.onclick = function () {\n      state.tab = b.dataset.tab;\n      Array.prototype.forEach.call(document.querySelectorAll('#view-records [data-tab]'), function (x) { x.classList.toggle('primary', x === b); });\n      $('#recSnapshots').hidden = state.tab !== 'snapshots';\n      $('#recEvidence').hidden = state.tab !== 'evidence';\n      $('#recAudit').hidden = state.tab !== 'audit';\n    };\n  });\n  document.querySelector('#view-records [data-tab=\"snapshots\"]').classList.add('primary');\n  $('#snapshotRows').addEventListener('click', function (e) {\n    var b = e.target.closest('[data-rollback]');\n    if (!b) return;\n    var slug = b.dataset.slug, snap = b.dataset.rollback, source = b.dataset.source;\n    confirmModal('回滚 ' + slug + ' 到 v' + b.dataset.version + '？', '<p class=\"label\">将用快照覆盖安装来源目录；恢复后自动体检并写入证据。</p><div class=\"mono\">' + esc(source) + '</div>', '执行回滚', true, async function () {\n      var r = await api('/api/rollback/apply', { body: { slug: slug, snapshot: snap, confirm: 'rollback' } });\n      if (r.error) { toast(r.error); return; }\n      closeModal();\n      toast(r.ok ? '回滚完成（doctor 通过）' : '回滚完成，但体检未通过');\n      loadRecords();\n      loadOverview();\n    });\n  });\n\n  $('#routeBtn').onclick = runRoute;\n  $('#routeInput').addEventListener('keydown', function (e) { if (e.key === 'Enter') runRoute(); });\n  async function runRoute() {\n    var request = $('#routeInput').value.trim();\n    if (!request) { toast('先输入一句需求'); return; }\n    var seq = showLoad('正在生成路由与编排…');\n    $('#routeBtn').disabled = true;\n    var d = await api('/api/route?request=' + encodeURIComponent(request));\n    hideLoad(seq);\n    $('#routeBtn').disabled = false;\n    if (d.error) { toast(d.error); return; }\n    var skills = (d.skills || []).map(function (s) {\n      return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + s.order + '. ' + esc(s.slug) + ' <span class=\"badge ' + (s.installed ? 'ok' : 'warn') + '\">' + esc(s.installed ? '已装' + (s.version ? ' v' + s.version : '') : '缺失') + '</span></div><div class=\"row-meta\">' + esc(s.role || '') + '</div></div></div>';\n    }).join('');\n    var missing = (d.missing_skills || []).length\n      ? '<div class=\"section panel\"><h3>缺失技能</h3><div class=\"toolbar\"><span class=\"mono\">' + esc((d.missing_skills || []).map(function (s) { return s.slug; }).join(', ')) + '</span><button class=\"btn small\" data-copy-cmd=\"' + esc(d.install_command || '') + '\">复制安装命令</button></div><div class=\"note\">安装与信任判断由你决定；元信装前扫描默认启用。</div></div>'\n      : '';\n    var others = (d.other_skill_candidates || []).length\n      ? '<div class=\"section panel\"><h3>其他已装技能候选</h3>' + d.other_skill_candidates.map(function (c) {\n        return '<div class=\"row\"><div class=\"row-main\"><div class=\"row-title\">' + esc(c.slug) + ' <span class=\"badge info\">v' + esc(c.version) + '</span></div><div class=\"row-meta\">' + esc((c.matched_terms || []).join('、')) + ' · ' + esc(c.description || '') + '</div></div></div>';\n      }).join('') + '<div class=\"note\">只读 frontmatter 机械匹配；使用前请自行确认。</div></div>'\n      : '';\n    $('#routeResult').innerHTML = '<div class=\"panel\"><div class=\"shead\"><h2>' + esc(d.playbook.name) + '</h2><span class=\"badge\">置信度 ' + esc(d.confidence) + '</span></div>' +\n      '<div class=\"label\">' + esc(d.playbook.intent) + '</div><div class=\"list\">' + skills + '</div>' +\n      '<div class=\"note\">动态路由：' + esc((d.dynamic && d.dynamic.status) || '未启用') + ' · 匹配词：' + esc((d.matched_keywords || []).join('、') || '无') + '</div></div>' + missing + others;\n  }\n  $('#routeResult').addEventListener('click', function (e) {\n    var b = e.target.closest('[data-copy-cmd]');\n    if (b) copyText(b.dataset.copyCmd);\n  });\n\n  /* 高级 CLI：/api/help 单一真源（与 CLI --help 同源；速查解析由服务端按最深前缀完成） */\n  function renderCliHelp(d) {\n    if (!d || d.error) { $('#cliMeta').textContent = '帮助加载失败'; return; }\n    var total = 0, optTotal = (d.options || []).length;\n    (d.groups || []).forEach(function (g) {\n      (g.commands || []).forEach(function (c) {\n        total += 1 + (c.subcommands || []).length;\n        optTotal += (c.options || []).length;\n        (c.subcommands || []).forEach(function (s) { optTotal += (s.options || []).length; });\n      });\n    });\n    $('#cliMeta').textContent = 'v' + (d.version || '-') + ' · 命令 ' + total + ' · 选项 ' + optTotal;\n    $('#cliQuick').innerHTML = (d.quick || []).map(function (g) {\n      return '<div class=\"cmd-group\"><h3>' + esc(g.group) + '</h3>' + (g.items || []).map(function (item) {\n        var meta = item.meta || {};\n        return '<div class=\"cmd\"><code>' + esc(item.example) + '</code><span class=\"why\">' + esc(meta.what || '') +\n          (item.note ? ' · ' + esc(item.note) : '') + '</span>' +\n          (item.danger ? '<span class=\"badge danger\">危险</span>' : '') +\n          '<button class=\"btn small\" data-copy-cmd=\"' + esc(item.example) + '\">复制</button></div>';\n      }).join('') + '</div>';\n    }).join('');\n    var full = (d.groups || []).map(function (g) {\n      return '<div class=\"cmd-group\"><h3>' + esc(g.group) + '</h3>' + (g.commands || []).map(function (c) {\n        var opts = (c.options || []).length\n          ? '<div class=\"note\">常用选项: ' + c.options.map(function (f) { return '<code>' + esc(f) + '</code>'; }).join(' ') + '</div>'\n          : '';\n        var subs = (c.subcommands || []).map(function (s) {\n          var sOpts = (s.options || []).length\n            ? '<div class=\"note\">选项: ' + s.options.map(function (f) { return '<code>' + esc(f) + '</code>'; }).join(' ') + '</div>'\n            : '';\n          return '<div class=\"cmd\"><code>' + esc('yotta-skills ' + s.usage) + '</code><span class=\"why\">' + esc(s.what || '') + '</span>' + sOpts +\n            (s.impact ? '<div class=\"note\">' + esc(s.impact) + '</div>' : '') +\n            (s.alternative ? '<div class=\"note\">' + esc(s.alternative) + '</div>' : '') +\n            '<button class=\"btn small\" data-copy-cmd=\"' + esc('yotta-skills ' + s.usage) + '\">复制</button></div>';\n        }).join('');\n        return '<details class=\"cmd-detail\"><summary><code>' + esc('yotta-skills ' + c.usage) + '</code> <span class=\"why\">' + esc(c.what || '') + '</span></summary>' +\n          (c.when ? '<div class=\"note\">' + esc(c.when) + '</div>' : '') +\n          (c.impact ? '<div class=\"note\">' + esc(c.impact) + '</div>' : '') +\n          (c.alternative ? '<div class=\"note\">' + esc(c.alternative) + '</div>' : '') + opts + subs + '</details>';\n      }).join('') + '</div>';\n    }).join('');\n    full += '<div class=\"cmd-group\"><h3>完整选项</h3>' + (d.options || []).map(function (o) {\n      return '<div class=\"cmd\"><code>' + esc(o.flag + (o.arg ? ' ' + o.arg : '')) + '</code><span class=\"why\">' + esc(o.what || '') +\n        (o.when ? ' · ' + esc(o.when) : '') + (o.caution ? ' · ⚠ ' + esc(o.caution) : '') + '</span></div>';\n    }).join('') + '</div>';\n    $('#cliFull').innerHTML = full;\n  }\n  api('/api/help').then(renderCliHelp);\n  document.addEventListener('click', function (e) {\n    var b = e.target.closest('#view-cli [data-copy-cmd]');\n    if (b) copyText(b.dataset.copyCmd);\n  });\n\n  (async function boot() {\n    var s = await api('/api/status');\n    if (s && !s.error) $('#verLine').textContent = 'v' + s.version + ' · ' + (s.standard || '');\n    else $('#verLine').textContent = '未连接本地服务';\n    runLoad('overview');\n  })();\n})();\n</script>\n</body>\n</html>\n";
// @generated view-html:end

function loadManifest() {
  const file = process.env.YOTTA_SKILLS_MANIFEST || path.join(PKG_ROOT, 'skills.json');
  let data;
  try {
    data = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    die('无法读取技能清单: ' + file + '（' + e.message + '）', 2, '检查 YOTTA_SKILLS_MANIFEST 或 skills.json 是否存在且为合法 JSON。');
  }
  const list = Array.isArray(data) ? data : data.skills;
  if (!Array.isArray(list) || list.length === 0) die('技能清单为空: ' + file);
  for (const s of list) {
    for (const f of ['slug', 'name', 'pkg', 'version']) {
      if (!s[f]) die('技能清单字段缺失 ' + f + '：' + JSON.stringify(s));
    }
  }
  return list;
}

const MANIFEST = loadManifest();

// 智能体 -> 用户级默认技能目录。单一真源在 lib/agent-dirs.js
// （兼容 Vercel Labs `skills` CLI / agentskills.io 的宿主表，MIT）。
const AGENT_DIRS = agentDirsLib.AGENT_DIRS;

function codexUserDir() {
  return agentDirsLib.resolveUserDir('.codex/skills', { homeDir: os.homedir(), env: process.env });
}
function opencodeUserDir() {
  return agentDirsLib.resolveUserDir('.config/opencode/skills', { homeDir: os.homedir(), env: process.env });
}
function resolveUserDir(rel) {
  return agentDirsLib.resolveUserDir(rel, { homeDir: os.homedir(), env: process.env });
}

// ── 工具函数 ───────────────────────────────────────────────────────────────
function die(msg, code, hint) {
  process.stderr.write('错误：' + msg + '\n');
  if (hint) process.stderr.write('修复建议：' + hint + '\n');
  process.exit(code === undefined ? 2 : code);
}
function out(s) { process.stdout.write(s + '\n'); }

function tarBin() { return 'tar'; }

/** 供依赖提示复制的「原命令」回显（尽力还原参数，仅作提示用）。 */
function currentCommand() {
  const args = process.argv.slice(2).map((a) => (/\s/.test(a) ? '"' + a + '"' : a));
  return 'yotta-skills ' + args.join(' ');
}

// 解析 npm 调用方式（Windows 的 .cmd 不能直接 spawn：EINVAL；cmd /c 引号脆弱）。
// 最优：定位 npm.cmd -> 读内容 -> 提取 node_modules/npm/bin/npm-cli.js -> 用 node 直接执行。
// 兼容：--npm / YOTTA_SKILLS_NPM 可指向 .js（node 执行）、.cmd（同样解析）、或可执行文件。
// 标准 npm 安装器布局：npm-cli.js 恒在 npm.cmd 同目录 node_modules/npm/bin/ 下（不解析 cmd 脚本内容，
// 避免 %dp0% 等 cmd 变量干扰；找不到则返回 null 走 shell 回退）
function npmCliFromCmd(cmdFile) {
  try {
    const p = path.join(path.dirname(cmdFile), 'node_modules', 'npm', 'bin', 'npm-cli.js');
    return fs.existsSync(p) ? p : null;
  } catch (_) { return null; }
}
function resolveNpm(opts) {
  const custom = opts.npm || process.env.YOTTA_SKILLS_NPM;
  if (custom) {
    if (/\.js$/i.test(custom)) return { bin: process.execPath, prefix: [custom], shell: false };
    if (/\.(cmd|bat)$/i.test(custom)) {
      const cli = npmCliFromCmd(custom);
      if (cli) return { bin: process.execPath, prefix: [cli], shell: false };
      return { bin: custom, prefix: [], shell: true };
    }
    return { bin: custom, prefix: [], shell: false };
  }
  if (process.platform === 'win32') {
    try {
      const w = spawnSync('where.exe', ['npm.cmd'], { encoding: 'utf8', timeout: 15000 });
      const line = (w.stdout || '').split(/\r?\n/).map(s => s.trim()).find(Boolean);
      if (line) {
        const cli = npmCliFromCmd(line);
        if (cli) return { bin: process.execPath, prefix: [cli], shell: false };
      }
    } catch (_) { /* fallthrough */ }
    return { bin: 'npm.cmd', prefix: [], shell: true };
  }
  return { bin: 'npm', prefix: [], shell: false };
}


function parseArgs(argv) {
  const opts = {
    list: false, dryRun: false, pin: true, skipScan: false, force: false,
    help: false, version: false, agent: null, dir: null, npm: null,
    python: null, verify: null, command: null, skill: null, rest: [],
    inventory: false, reindex: false, noReindex: false, json: false, project: false, route: null,
    check: false, auto: false, scheduled: false, registry: null, slug: null,
    host: null, event: null, manifest: null, context: null,
    signal: null, yes: false, explain: false, promote: false,
    only: [], domain: null, installedOnly: false,
    hub: null, all: false, includeDiscovered: false, inPlace: false, allowUnverified: false,
    from: null, include: [], as: null, skillsCli: null,
    scan: false, apply: false,
    clear: false,
    move: false,
    port: null,
  };
  const positionals = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const take = (name) => { const v = argv[i + 1]; if (v === undefined || v.startsWith('--')) die(name + ' 缺少参数值', 2, '请为该选项提供一个非空值；可用 --help 查看用法。'); i++; return v; };
    if (a === '--list' || a === '-l') opts.list = true;
    else if (a === '--dry-run') opts.dryRun = true;
    else if (a === '--pin') opts.pin = true;
    else if (a === '--range') opts.pin = false;
    else if (a === '--skip-scan') opts.skipScan = true;
    else if (a === '--force') opts.force = true;
    else if (a === '--help' || a === '-h') opts.help = true;
    else if (a === '--version' || a === '-v') opts.version = true;
    else if (a === '--inventory' || a === '--inv') opts.inventory = true;
    else if (a === '--route') {
      const value = argv[i + 1];
      if (value === undefined || value.startsWith('--')) die('--route 缺少需求摘要', 2, '请提供一句需求描述，例如 --route "帮我做发布前质量检查"。');
      opts.route = value;
      i++;
    }
    else if (a === '--reindex' || a === '--rescan') opts.reindex = true;
    else if (a === '--no-reindex') opts.noReindex = true;
    else if (a === '--json') opts.json = true;
    else if (a === '--project') opts.project = true;
    else if (a === '--agent') opts.agent = take('--agent').toLowerCase();
    else if (a === '--dir') opts.dir = take('--dir');
    else if (a === '--npm') opts.npm = take('--npm');
    else if (a === '--python') opts.python = take('--python');
    else if (a === '--verify') opts.verify = take('--verify');
    else if (a === '--slug') {
      const value = take('--slug').toLowerCase();
      if (!/^[a-z0-9][a-z0-9-]*$/.test(value)) {
        die('--slug 格式非法', 2, '只允许小写字母、数字和连字符，例如 yotta-memory。');
      }
      opts.slug = value;
    }
    else if (a === '--check') opts.check = true;
    else if (a === '--auto') opts.auto = true;
    else if (a === '--scheduled') opts.scheduled = true;
    else if (a === '--registry') opts.registry = take('--registry');
    else if (a === '--only') {
      const value = take('--only');
      for (const item of value.split(',')) {
        const slug = item.trim().toLowerCase();
        if (slug) opts.only.push(slug);
      }
    }
    else if (a === '--domain') opts.domain = take('--domain').toLowerCase();
    else if (a === '--installed-only') opts.installedOnly = true;
    else if (a === '--hub') opts.hub = take('--hub');
    else if (a === '--state') opts.state = take('--state').toLowerCase();
    else if (a === '--label') opts.label = take('--label');
    else if (a === '--id') opts.id = take('--id').toLowerCase();
    else if (a === '--clear') opts.clear = true;
    else if (a === '--move') opts.move = true;
    else if (a === '--clean-residue') opts.cleanResidue = true;
    else if (a === '--purge') opts.purge = true;
    else if (a === '--all') opts.all = true;
    else if (a === '--include-discovered') opts.includeDiscovered = true;
    else if (a === '--in-place') opts.inPlace = true;
    else if (a === '--scan') opts.scan = true;
    else if (a === '--apply') opts.apply = true;
    else if (a === '--allow-unverified') opts.allowUnverified = true;
    else if (a === '--from') opts.from = take('--from');
    else if (a === '--include') {
      const value = take('--include');
      for (const item of value.split(',')) {
        const slug = item.trim().toLowerCase();
        if (slug) opts.include.push(slug);
      }
    }
    else if (a === '--as') opts.as = take('--as').toLowerCase();
    else if (a === '--skills-cli') opts.skillsCli = take('--skills-cli');
    else if (a === '--port') {
      const raw = take('--port');
      const value = Number(raw);
      if (!Number.isInteger(value) || value < 0 || value > 65535) {
        die('--port 端口非法: ' + raw, 2, '请提供 0-65535 之间的整数；例如 --port 8789。');
      }
      opts.port = value;
    }
    else if (a === '--host') opts.host = take('--host').toLowerCase();
    else if (a === '--event') opts.event = take('--event').toLowerCase();
    else if (a === '--manifest') opts.manifest = take('--manifest');
    else if (a === '--context') opts.context = take('--context');
    else if (a === '--skill') opts.skill = take('--skill').toLowerCase();
    else if (a === '--signal') opts.signal = take('--signal').toLowerCase();
    else if (a === '--yes') opts.yes = true;
    else if (a === '--explain') opts.explain = true;
    else if (a === '--promote') opts.promote = true;
    else if (a.startsWith('-')) die('未知参数: ' + a, 2, '可用 --help 查看支持的选项。');
    else positionals.push(a);
  }
  // 命令解析：install / update / doctor / rollback，其余位置参数 = 技能 slug（可多个）
  for (const p of positionals) {
    if (opts.command === 'hub') {
      opts.rest.push(p);
      continue;
    }
    if (p === 'install' || p === 'install-self' || p === 'update' || p === 'doctor' || p === 'rollback'
      || p === 'hook' || p === 'hub' || p === 'view' || p === 'where'
      || p === 'usage' || p === 'decide-memory') {
      if (opts.command && opts.command !== p) die('命令冲突：' + opts.command + ' 与 ' + p);
      opts.command = p;
    } else {
      opts.rest.push(p);
    }
  }
  // 直接给 slug 且无命令 → 视为 install 单个/多个
  if (!opts.command && opts.rest.length > 0) opts.command = 'install';
  // 原始位置参数副本：技能 slug 统一小写匹配，但目录路径（hub hosts add/remove 等）
  // 必须保留原始大小写（Windows 路径大小写不敏感但显示 / 台账需要原样）。
  opts.rawRest = opts.rest.slice();
  opts.skills = opts.rest.map(s => s.toLowerCase());
  if (opts.command === 'hub') {
    opts.hubAction = opts.skills[0] || 'status';
    opts.skills = opts.skills.slice(1);
  }
  if (opts.scheduled && (opts.command !== 'update' || !opts.check || opts.auto)) {
    die('--scheduled 只能与 update --check 一起使用', 2, '请使用 update --check --scheduled；自动更新不使用后台调度入口。');
  }
  if (opts.installedOnly && opts.command !== 'update') {
    die('--installed-only 只能与 update 一起使用', 2, '标准配方：yotta-skills update --installed-only --dir <技能目录>。');
  }
  if (opts.port !== null && opts.command !== 'view') {
    die('--port 只能与 view 一起使用', 2, '示例：yotta-skills view --port 8789。');
  }
  if (opts.state && !['available', 'orphan', 'missing', 'marker-only', 'ignored'].includes(opts.state)) {
    die('未知 --state: ' + opts.state, 2,
      '可用: available（可用）/ orphan（残留）/ missing（未创建）/ marker-only（仅标记）/ ignored（已忽略）。');
  }
  if (opts.state && !(opts.command === 'hub' && (opts.hubAction === 'hosts' || opts.hubAction === 'discover'))) {
    die('--state 只能与 hub hosts 一起使用', 2, '示例：yotta-skills hub hosts --state orphan。');
  }
  if ((opts.all || opts.includeDiscovered || opts.inPlace || opts.allowUnverified || opts.from || opts.include.length || opts.as || opts.scan || opts.apply)
    && opts.command !== 'hub') {
    die('--all / --include-discovered / --in-place / --allow-unverified / --from / --include / --as / --scan / --apply 只能与 hub 命令一起使用', 2,
      'Hub 用法：yotta-skills hub link --all --include-discovered 或 yotta-skills hub adopt --scan。');
  }
  if (opts.domain && !domainValues().includes(opts.domain)) {
    die('未知 domain: ' + opts.domain + '。可用: ' + domainValues().join(', '), 2, 'domain 对齐家族索引 9 类；用 yotta-skills --list 查看技能清单。');
  }
  // 0.29.2 U4：--hub 只在 hub / view / where 生效；其它命令静默忽略是误用坑，fail-closed。
  if (opts.hub && !(opts.command === 'hub' || opts.command === 'view' || opts.command === 'where')) {
    die('--hub 只能与 hub / view / where 一起使用', 2,
      '示例：yotta-skills hub status --hub "D:\\my-hub"。装到宿主目录请用 --dir <path>。');
  }
  if (opts.move && !(opts.command === 'hub' && opts.hubAction === 'config' && opts.skills[0] === 'set')) {
    die('--move 只能与 hub config set 一起使用', 2,
      '示例：yotta-skills hub config set --hub "D:\\my-hub" --move。');
  }
  if (opts.cleanResidue && !(opts.command === 'hub' && opts.hubAction === 'config' &&
      (opts.skills[0] === 'set' || opts.skills[0] === 'rollback'))) {
    die('--clean-residue 只能与 hub config set --move / hub config rollback 一起使用', 2,
      '示例：yotta-skills hub config set --hub "D:\\my-hub" --move --clean-residue。');
  }
  return opts;
}

function skillRange(s) {
  const major = String(s.version).split('.')[0];
  return major + '.x';
}
function specOf(s, pin) {
  return s.pkg + '@' + (pin ? s.version : skillRange(s));
}
function findSkill(slug) {
  return MANIFEST.find(s => s.slug === slug || s.pkg === slug || s.pkg.replace('@yottameta/', '') === slug);
}

const KNOWN_DOMAINS = ['security', 'quality', 'memory', 'writing', 'workflow', 'entry', 'compliance', 'education', 'distribution'];

function domainValues() {
  const values = new Set(KNOWN_DOMAINS);
  for (const s of MANIFEST) if (s.domain) values.add(s.domain);
  return [...values].sort();
}

function selectSkills(opts) {
  const picked = [];
  const seen = new Set();
  const push = (s) => {
    if (!seen.has(s.slug)) {
      seen.add(s.slug);
      picked.push(s);
    }
  };
  for (const slug of opts.skills) {
    const s = findSkill(slug);
    if (!s) die('未知技能: ' + slug + '（可用: yotta-skills --list）', 2, '请先运行 --list 查看技能名，或检查拼写。');
    push(s);
  }
  for (const slug of opts.only || []) {
    const s = findSkill(slug);
    if (!s) die('未知技能（--only）: ' + slug + '（可用: yotta-skills --list）', 2, '请先运行 --list 查看技能名，或检查拼写。');
    push(s);
  }
  let list = picked.length > 0 ? picked : MANIFEST.slice();
  if (opts.domain) {
    list = list.filter((s) => s.domain === opts.domain);
  }
  return list;
}

/** Hub 范围选择：全家清单 27 + 特殊家族 5（特殊家族版本跟随各自 npm latest）。 */
function findHubSkill(slug) {
  return findSkill(slug) || hubLib.HUB_FAMILY_EXTRAS.find((s) =>
    s.slug === slug || s.pkg === slug || s.pkg.replace('@yottameta/', '') === slug);
}

function selectHubSkills(opts) {
  const picked = [];
  const seen = new Set();
  const push = (s) => {
    if (!seen.has(s.slug)) {
      seen.add(s.slug);
      picked.push(s);
    }
  };
  for (const slug of opts.skills) {
    const s = findHubSkill(slug);
    if (!s) die('未知技能: ' + slug + '（可用: yotta-skills --list）', 2, '请先运行 --list 查看技能名，或检查拼写。');
    push(s);
  }
  for (const slug of opts.only || []) {
    const s = findHubSkill(slug);
    if (!s) die('未知技能（--only）: ' + slug + '（可用: yotta-skills --list）', 2, '请先运行 --list 查看技能名，或检查拼写。');
    push(s);
  }
  let list = picked.length > 0 ? picked : MANIFEST.slice().concat(hubLib.HUB_FAMILY_EXTRAS);
  if (opts.domain) {
    list = list.filter((s) => s.domain === opts.domain);
  }
  return list;
}

function readInstalledVersion(dir) {
  const f = path.join(dir, 'SKILL.md');
  try {
    const text = fs.readFileSync(f, 'utf8');
    const m = text.match(/^version:\s*([0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?)/m);
    return m ? m[1] : null;
  } catch (_) { return null; }
}


// ── 更新检查（只读）与自动更新 ─────────────────────────────────────────────
function registryUrl(pkg, registry) {
  var base = (registry || process.env.YOTTA_SKILLS_REGISTRY || 'https://registry.npmjs.org/').replace(/\/$/, '');
  return base + '/' + pkg.replace(/\//g, '%2f');
}

function fetchRegistryLatest(pkg, opts) {
  return new Promise(function (resolve) {
    var url = registryUrl(pkg, opts.registry);
    var client = url.startsWith('https:') ? https : http;
    var req = client.get(url, { timeout: 15000, headers: { 'accept': 'application/json', 'user-agent': 'yotta-skills-check' } }, function (res) {
      var data = '';
      res.setEncoding('utf8');
      res.on('data', function (c) { data += c; });
      res.on('end', function () {
        try {
          var j = JSON.parse(data);
          var latest = j && j['dist-tags'] && j['dist-tags'].latest;
          if (!latest) { resolve({ ok: false, error: '响应缺少 dist-tags.latest（' + pkg + '）' }); return; }
          resolve({ ok: true, version: latest });
        } catch (e) {
          resolve({ ok: false, error: '解析 registry 响应失败: ' + e.message });
        }
      });
    });
    req.on('error', function (e) { resolve({ ok: false, error: '网络错误: ' + (e && e.message ? e.message : e) }); });
    req.on('timeout', function () { req.destroy(); resolve({ ok: false, error: '网络超时（15s）' }); });
  });
}

function readInstalledMeta(dir) {
  var f = path.join(dir, 'SKILL.md');
  try {
    var text = fs.readFileSync(f, 'utf8');
    var name = (text.match(/^name:\s*(.+)$/m) || [])[1];
    var version = (text.match(/^version:\s*([0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?)/m) || [])[1];
    return { name: name ? name.trim() : null, version: version || null };
  } catch (e) { return { name: null, version: null }; }
}

function familySkillFor(slug) {
  var m = findSkill(slug);
  if (m) return m;
  if (/^yotta-/.test(slug)) {
    return { slug: slug, name: slug.replace(/^yotta-/, ''), pkg: '@yottameta/' + slug, version: null, desc: '推断的家族技能（不在 skills.json 清单）' };
  }
  return null;
}

function scanInstalledSlugs(dest) {
  var list = [];
  var entries;
  try { entries = fs.readdirSync(dest, { withFileTypes: true }); } catch (e) { return list; }
  for (var i = 0; i < entries.length; i++) {
    var e = entries[i];
    if (!e.isDirectory()) continue;
    var meta = readInstalledMeta(path.join(dest, e.name));
    if (meta.name) list.push({ slug: e.name, name: meta.name, version: meta.version });
  }
  return list;
}

async function runUpdateCheck(opts, dest) {
  var lines = [];
  var quiet = !!opts.json;
  function say(s) { if (!quiet) lines.push(s); }
  var scheduled = !!opts.scheduled;
  var cache = updateCheckLib.readCache();
  var target = cache.targets[updateCheckLib.targetKey(dest)] || null;
  var due = updateCheckLib.isDue(target, Date.now());
  if (!scheduled) {
    say('yotta-skills（元阁）v' + VERSION + ' —— 检查更新（只读，不改动） -> ' + dest);
    say('版本源: ' + (opts.registry || process.env.YOTTA_SKILLS_REGISTRY || 'https://registry.npmjs.org/'));
    say('');
  }
  if (scheduled && !due) {
    var cachedRows = (target && target.last_result && target.last_result.rows) || [];
    var cachedPayload = {
      dest: dest,
      scheduled: true,
      due: false,
      checked: false,
      updatable: cachedRows.filter(function (x) { return x.hasUpdate; }),
      updates: (target && target.last_result && target.last_result.updates) || 0,
      latest: (target && target.last_result && target.last_result.latest) || 0,
      localAhead: (target && target.last_result && target.last_result.localAhead) || 0,
      failed: 0,
      nonFamily: (target && target.last_result && target.last_result.nonFamily) || 0,
      cache: target,
      error: null,
    };
    if (opts.json) out(JSON.stringify(cachedPayload, null, 2));
    return {
      code: 0,
      scheduled: true,
      due: false,
      checked: false,
      rows: cachedRows,
      updates: cachedPayload.updates,
      latest: cachedPayload.latest,
      localAhead: cachedPayload.localAhead,
      failed: 0,
      nonFamily: cachedPayload.nonFamily,
    };
  }
  var installed = scanInstalledSlugs(dest);
  if (installed.length === 0) {
    var emptyResult = { updates: 0, latest: 0, localAhead: 0, failed: 0, nonFamily: 0, rows: [], errors: [] };
    var emptyCacheRecord = null;
    try {
      emptyCacheRecord = updateCheckLib.recordCheck(os.homedir(), dest, { result: emptyResult, error: null });
    } catch (_) { /* 缓存是后台优化的 best-effort，不阻断检查结果 */ }
    if (!scheduled) {
      say('（' + dest + ' 下未发现已装技能目录）');
      for (var emptyIndex = 0; emptyIndex < lines.length; emptyIndex++) out(lines[emptyIndex]);
    }
    return {
      code: 0,
      scheduled: scheduled,
      due: true,
      checked: true,
      rows: [],
      updates: 0,
      latest: 0,
      localAhead: 0,
      failed: 0,
      nonFamily: 0,
      cache: emptyCacheRecord,
    };
  }
  var rows = [];
  var failures = [];
  var updates = 0, latest = 0, localAhead = 0, failed = 0, nonFamily = 0;
  for (var i = 0; i < installed.length; i++) {
    var it = installed[i];
    var fam = familySkillFor(it.slug);
    if (!fam) {
      nonFamily++;
      say('  - ' + it.slug.padEnd(22) + '非元阁家族，跳过');
      continue;
    }
    var res = await fetchRegistryLatest(fam.pkg, opts);
    if (!res.ok) {
      failed++;
      failures.push({ slug: it.slug, error: res.error });
      say('  ✘ ' + it.slug.padEnd(22) + '检查失败: ' + res.error);
      continue;
    }
    var current = res.version;
    var cur = it.version || null;
    var relation = versionRelation(cur, current);
    if (relation === 'upgrade') {
      updates++;
      say('  ➤ ' + it.slug.padEnd(22) + '有更新：本地 v' + (cur || '未知') + ' -> 最新 v' + current);
      if (fam.version && fam.version !== current) {
        say('       ⚠ 清单 skills.json 记为 v' + fam.version + '，与 npm 最新 v' + current + ' 不一致（需同步清单）');
      }
    } else if (relation === 'equal') {
      latest++;
      say('  ✔ ' + it.slug.padEnd(22) + '已最新（本地 v' + cur + '）');
    } else if (relation === 'local-ahead') {
      localAhead++;
      say('  ⏸ ' + it.slug.padEnd(22) + '本地领先：本地 v' + cur + ' > 最新 v' + current + '（保留，不计入更新）');
    } else {
      say('  ？ ' + it.slug.padEnd(22) + '无法比较版本（本地 v' + (cur || '未知') + ' / 最新 v' + current + '），保留');
    }
    rows.push({
      slug: it.slug,
      installed: cur,
      latest: current,
      pkg: fam.pkg,
      hasUpdate: relation === 'upgrade',
      localAhead: relation === 'local-ahead',
      relation: relation,
      family: fam,
    });
  }
  var result = {
    updates: updates,
    latest: latest,
    localAhead: localAhead,
    failed: failed,
    nonFamily: nonFamily,
    rows: rows,
    errors: failures,
  };
  var lastError = failures.length > 0
    ? failures.map(function (x) { return x.slug + ': ' + x.error; }).join('; ')
    : null;
  var cacheRecord = null;
  try {
    cacheRecord = updateCheckLib.recordCheck(os.homedir(), dest, { result: result, error: lastError });
  } catch (_) { /* 缓存是后台优化的 best-effort，不阻断检查结果 */ }
  var code = (failed > 0) ? 1 : (updates > 0 ? 3 : 0);
  var updatable = rows.filter(function (x) { return x.hasUpdate; });
  if (scheduled) {
    if (updates > 0) {
      for (var j = 0; j < updatable.length; j++) {
        out('  ' + updatable[j].slug + '：本地 v' + (updatable[j].installed || '未知') + ' -> 最新 v' + updatable[j].latest);
      }
    }
    if (opts.json) {
      out(JSON.stringify({
        dest: dest,
        scheduled: true,
        due: true,
        checked: true,
        updatable: updatable,
        updates: updates,
        latest: latest,
        localAhead: localAhead,
        failed: failed,
        nonFamily: nonFamily,
        cache: cacheRecord,
        error: lastError,
      }, null, 2));
    }
    return { code: 0, scheduled: true, due: true, checked: true, rows: rows, updates: updates, latest: latest, localAhead: localAhead, failed: failed, nonFamily: nonFamily };
  }
  say('汇总: 有更新 ' + updates + ' / 本地领先 ' + localAhead + ' / 已最新 ' + latest + ' / 检查失败 ' + failed + ' / 非家族跳过 ' + nonFamily);
  for (var lineIndex = 0; lineIndex < lines.length; lineIndex++) out(lines[lineIndex]);
  if (opts.json) {
    out(JSON.stringify({
      dest: dest,
      updatable: updatable,
      updates: updates,
      latest: latest,
      localAhead: localAhead,
      failed: failed,
      nonFamily: nonFamily,
      cache: cacheRecord,
      error: lastError,
    }, null, 2));
  }
  return { code: code, scheduled: false, due: true, checked: true, rows: rows, updates: updates, latest: latest, localAhead: localAhead, failed: failed, nonFamily: nonFamily };
}

async function runUpdateAuto(opts, dest) {
  out('yotta-skills（元阁）v' + VERSION + ' —— 检查并自动更新（仅 yotta-* 家族） -> ' + dest);
  var r = await runUpdateCheck(Object.assign({}, opts, { json: false }), dest);
  if (r.failed > 0) {
    out('检查未完成（' + r.failed + ' 个失败），未自动更新；可先排查网络后重试。');
    return { code: 1 };
  }
  if (r.updates === 0) {
    if (r.localAhead > 0) {
      out('本地领先 ' + r.localAhead + ' 个（保留不降级）；其余已最新，无需更新。');
    } else {
      out('全部已最新，无需更新。');
    }
    return { code: 0 };
  }
  out('');
  out('检测到 ' + r.updates + ' 个家族技能可更新，开始自动更新（安装管线，含装前安全扫描）：');
  var ok = 0, failed2 = 0, autoExitCode = 0;
  for (var i = 0; i < r.rows.length; i++) {
    var row = r.rows[i];
    if (!row.hasUpdate) continue;
    var res = installOne(
      Object.assign({}, row.family, { version: row.latest }),
      dest,
      Object.assign({}, opts, { pin: true, skipScan: false }),
    );
    if (res.status === 'ok') ok++;
    else if (res.status === 'skip') ok++;
    else {
      failed2++;
      autoExitCode = Math.max(autoExitCode, res.exitCode || 1);
      out('  ✘ ' + row.slug + '  失败: ' + res.note);
    }
  }
  out('');
  out('自动更新汇总: 成功 ' + ok + ' / 失败 ' + failed2 + (r.localAhead > 0 ? ' / 本地领先保留 ' + r.localAhead : ''));
  if (failed2 === 0) maybeAutoReindex(opts, dest);
  return { code: failed2 > 0 ? autoExitCode : 0 };
}

// 复制原语（顶层跳过口径 / 缓存清理）统一在 lib/copy-tree.js，此处不再保留第二份实现。

function resolveTargetDir(opts) {
  if (opts.dir) return path.resolve(opts.dir);
  if (opts.agent) {
    const info = AGENT_DIRS[opts.agent];
    if (!info) die('未收录智能体: ' + opts.agent + '。可用: ' + Object.keys(AGENT_DIRS).join(', ') + '；或改用 --dir <路径>。');
    return resolveUserDir(info.dirs[0]);
  }
  return null; // 未指定目标（项目级检测由调用方处理）
}

function detectProjectDir() {
  const PROJECT_DIRS = [
    '.claude/skills', '.cursor/skills', '.codex/skills', '.config/goose/skills',
    '.config/agents/skills', '.opencode/skills', '.codeium/windsurf/skills',
    '.workbuddy/skills', '.kiro/skills', '.traecli/skills', '.gemini/skills',
    '.trae-cn/skills', '.qwen/skills', '.comate/skills', '.codebuddy/skills',
    '.kimi/skills', '.agents/skills',
  ];
  for (const d of PROJECT_DIRS) if (fs.existsSync(d)) return path.resolve(d);
  return null;
}

// ── 元信 scan 与安装门禁 ──────────────────────────────────────────────────
function findVerifyEngine(dest, opts) {
  // v0.19.13：不再用注册表（身份来自被扫描技能自己的 frontmatter）发现校验器，
  // 只认安装管线写入的受信记录（路径 + 摘要双绑定）。
  return hubScanLib.findVerifyEngine(dest, opts);
}

/** 安装 / 更新元信成功后写入受信记录（身份 + 摘要），后续门禁只认这份记录。 */
function recordTrustedVerifier(dest) {
  const engine = path.join(dest, 'yotta-verify', 'scripts', 'yotta_verify.py');
  const check = trustedVerifierLib.verifyEngine(engine, { requireRecord: false });
  if (!check.ok) return null;
  const record = {
    slug: check.info.slug,
    package: check.info.package,
    version: check.info.version,
    path: check.path,
    sha256: check.info.sha256,
    recordedAt: new Date().toISOString(),
  };
  trustedVerifierLib.saveRecord(record);
  return record;
}

/**
 * 元信自举运行时缓存（0.29.5 S4）：与受信记录同根，默认 ~/.yottaskills/runtime/verifier。
 * 自举产物不再写进目标目录（--dir 托管目录保持干净）；后续门禁通过受信记录
 * （路径 + SHA-256）使用缓存副本。
 */
function verifierRuntimeRoot() {
  return path.join(path.dirname(trustedVerifierLib.recordPath()), 'runtime', 'verifier');
}

function findPython(opts) {
  return hubScanLib.findPython(opts);
}

function runScan(engine, skillDir, opts) {
  return hubScanLib.runScan(engine, skillDir, opts);
}

function scanTarget(engine, skillDir, context) {
  const ctx = context || {};
  const scan = runScan(engine, skillDir, ctx.opts);
  if (!scan.ok) {
    out('  元信 scan: ' + scan.error);
    return scan;
  }
  const reviewed = scanPolicyLib.applyScanPolicy(scan, {
    slug: ctx.slug,
    version: ctx.version,
    pkgDir: skillDir,
    policy: scanPolicyLib.loadPolicy(path.join(PKG_ROOT, 'scan-policy.json')),
  });
  const counts = scan.counts || {};
  const line = 'critical ' + (counts.critical || 0) + ' / high ' + (counts.high || 0) +
    ' / medium ' + (counts.medium || 0) + ' / low ' + (counts.low || 0) +
    ' / info ' + (counts.info || 0);
  out('  元信 scan: ' + scan.verdict + '（' + line + '）');
  if (reviewed.policy && reviewed.policy.applied && reviewed.policy.excluded > 0) {
    out('  ↳ scanPolicy 复核：豁免 ' + reviewed.policy.excluded +
      ' 条已审查发现（检测规则 / 文档说明，treeHash 绑定）→ ' + reviewed.verdict);
  }
  if (reviewed.verdict === gateLib.BLOCK) out('  ⚠ 元信 verdict 为 DO NOT INSTALL，已阻断安装。');
  else if (reviewed.verdict === gateLib.CAUTION || reviewed.verdict === gateLib.REVIEW) {
    out('  ⚠ 元信 verdict 为 ' + reviewed.verdict + '，继续安装并保留风险证据。');
  }
  return reviewed;
}

/**
 * 0.30.0 OPT-05：refresh 被 scanPolicy 拦截时，输出与「上一已审版本」的
 * finding 差异摘要（同规则计数 + 新增 / 消失项），辅助人工判断是否 --allow-unverified。
 */
function scanFindingDiffLines(slug, scanInfo) {
  const lines = [];
  const info = scanInfo || {};
  const countRules = (findings) => {
    const map = new Map();
    for (const finding of findings || []) {
      const rule = String((finding && (finding.rule_id || finding.rule)) || 'unknown');
      map.set(rule, (map.get(rule) || 0) + 1);
    }
    return map;
  };
  const current = countRules(info.findings);
  const currentList = [...current.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([rule, count]) => rule + (count > 1 ? '×' + count : ''));
  lines.push('当前命中 ' + currentList.length + ' 类: ' + (currentList.join('、') || '无'));
  if (Array.isArray(info.excluded) && info.excluded.length > 0) {
    lines.push('scanPolicy 已豁免 ' + info.excluded.length + ' 条（treeHash 绑定）');
  }
  let entry = null;
  try {
    const policy = scanPolicyLib.loadPolicy(path.join(PKG_ROOT, 'scan-policy.json'));
    entry = policy && policy.skills ? policy.skills[slug] : null;
  } catch (_) {
    entry = null;
  }
  if (!entry) {
    lines.push('无上一已审版本记录（scan-policy.json 无该技能例外表）；人工复核全部命中后再决定是否 --allow-unverified。');
    return lines;
  }
  const prevRules = new Set((entry.exceptions || []).map((item) => String(item.rule)));
  const added = [...current.keys()].filter((rule) => !prevRules.has(rule));
  const gone = [...prevRules].filter((rule) => !current.has(rule));
  lines.push('与上一已审版本 v' + (entry.version || '?') + ' 对比: 新增 ' + (added.join('、') || '无') +
    ' / 消失 ' + (gone.join('、') || '无') + '（上一版豁免规则 ' + prevRules.size + ' 条）');
  return lines;
}

/** doctor 依赖自检（只告警不失败）：node / npm / python / tar 四项。 */
function probeDependencies(opts) {
  const npm = resolveNpm(opts);
  const npmProbe = spawnSync(npm.bin, [...npm.prefix, '--version'], {
    encoding: 'utf8',
    timeout: 15000,
    shell: npm.shell,
  });
  const python = findPython(opts);
  const pythonProbe = python
    ? spawnSync(python, ['--version'], { encoding: 'utf8', timeout: 15000 })
    : null;
  const tarProbe = spawnSync(tarBin(), ['--version'], { encoding: 'utf8', timeout: 15000 });
  return depsLib.dependencyReport({
    node: depsLib.nodeCheck(),
    npm: { found: !!(npmProbe && npmProbe.status === 0), version: depsLib.versionLine(npmProbe) },
    python: { found: !!python, version: depsLib.versionLine(pythonProbe), path: python || null },
    tar: { found: !!(tarProbe && tarProbe.status === 0), version: depsLib.versionLine(tarProbe) },
  });
}

// ── 安装 ───────────────────────────────────────────────────────────────────
const runNpmPackBase = npmPackLib.createPackRunner({ spawnSync, specOf, resolveNpm });

function fetchMode() {
  const raw = String(process.env.YOTTA_SKILLS_FETCH || 'auto').trim().toLowerCase();
  return raw === 'builtin' || raw === 'npm' ? raw : 'auto';
}

function extractMode() {
  const raw = String(process.env.YOTTA_SKILLS_EXTRACT || 'auto').trim().toLowerCase();
  return raw === 'builtin' || raw === 'tar' ? raw : 'auto';
}

/**
 * 拉包：默认内置通道（Node 内置 https，零 npm），失败回退 npm pack。
 * YOTTA_SKILLS_FETCH=builtin 禁用回退；=npm 直接走 npm（显式选择 / 离线测试）。
 */
function runNpmPack(skill, opts, packDir) {
  const mode = fetchMode();
  let builtin = null;
  if (mode !== 'npm') {
    builtin = registryFetchLib.fetchPackageSync(skill, opts, packDir);
    if (!builtin.error) return builtin;
  }
  if (mode === 'builtin') {
    return { error: '内置拉包失败（YOTTA_SKILLS_FETCH=builtin 已禁用 npm 回退）: ' + builtin.error };
  }
  const packed = runNpmPackBase(skill, opts, packDir);
  if (packed.error) {
    const detail = packed.detail || packed.error;
    let message = '拉包失败（内置 + npm 双通道）: 内置=' + (builtin ? builtin.error : '未启用') + '；npm=' + packed.error;
    if (depsLib.isNpmMissing(detail)) {
      message += '\n' + depsLib.describe('npm', { command: currentCommand(), missing: true });
    }
    return { error: message, detail };
  }
  packed.channel = 'npm';
  if (builtin) {
    packed.fallbackFrom = builtin.error;
    out('  ↳ 拉包通道：内置失败（' + builtin.error + '）→ npm 回退成功');
  }
  if (packed.registryFallback) {
    out('  ↳ npm 默认源 404，已用官方源重试成功（' + npmPackLib.OFFICIAL_REGISTRY + '）');
  }
  return packed;
}

function extractWithSystemTar(tarball, extractDir) {
  const packDir = path.dirname(tarball);
  const tarballName = path.basename(tarball);
  fs.mkdirSync(extractDir, { recursive: true });
  // 传相对文件名给 tar，避免 Windows 盘符被 MSYS tar 当成远端 host。
  const listed = spawnSync(tarBin(), ['-tzf', tarballName], { cwd: packDir, encoding: 'utf8', timeout: 120000, maxBuffer: 16 * 1024 * 1024 });
  if (listed.status !== 0) {
    return { error: (listed.stderr || listed.stdout || 'tar 列表读取失败').trim().split('\n').pop() };
  }
  const entries = String(listed.stdout || '').split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const unsafe = entries.find((entry) => !isSafeTarEntry(entry));
  if (unsafe) return { error: '压缩包包含不安全路径: ' + unsafe };
  const relativeTarball = path.relative(extractDir, tarball).replace(/\\/g, '/');
  const r = spawnSync(tarBin(), ['-xzf', relativeTarball], { cwd: extractDir, encoding: 'utf8', timeout: 120000 });
  if (r.status !== 0) return { error: (r.stderr || r.stdout || 'tar 解压失败').trim().split('\n').pop() };
  const pkgDir = path.join(extractDir, 'package');
  if (!fs.existsSync(path.join(pkgDir, 'SKILL.md'))) return { error: '解压产物缺少 SKILL.md（' + tarball + '）' };
  return { pkgDir };
}

/**
 * 解包：默认内置（zlib + tar 解析），失败回退系统 tar；
 * YOTTA_SKILLS_EXTRACT=builtin 禁用回退；=tar 直接走系统 tar。
 */
function extractTarball(tarball, extractDir) {
  const mode = extractMode();
  let builtin = null;
  if (mode !== 'tar') {
    builtin = untarLib.extractTarballBuiltin(tarball, extractDir);
    if (!builtin.error) return builtin;
  }
  if (mode === 'builtin') {
    return { error: '内置解包失败（YOTTA_SKILLS_EXTRACT=builtin 已禁用 tar 回退）: ' + builtin.error };
  }
  const fallback = extractWithSystemTar(tarball, extractDir);
  if (fallback.error) {
    const message = '解包失败（内置 + 系统 tar 双通道）: 内置=' + (builtin ? builtin.error : '未启用') + '；tar=' + fallback.error +
      '\n' + depsLib.describe('tar', { command: currentCommand(), missing: true });
    return { error: message };
  }
  if (builtin) {
    out('  ↳ 解包通道：内置失败（' + builtin.error + '）→ 系统 tar 回退成功');
    fallback.fallbackFrom = builtin.error;
  }
  fallback.channel = 'tar';
  return fallback;
}

function ensureGate(context) {
  const { skill, extracted, dest, opts } = context;
  const current = findVerifyEngine(dest, opts);
  if (current) {
    return {
      ok: true,
      engine: current,
      mode: opts.bootstrap ? 'trusted-bootstrap' : 'installed',
    };
  }
  if (skill.slug === 'yotta-verify') {
    const engine = path.join(extracted.pkgDir, 'scripts', 'yotta_verify.py');
    if (!fs.existsSync(engine)) return { ok: false, error: '元信包内缺少 scripts/yotta_verify.py' };
    return { ok: true, engine, mode: 'trusted-bootstrap' };
  }

  const verifier = findSkill('yotta-verify');
  if (!verifier) return { ok: false, error: 'skills.json 缺少 yotta-verify' };
  let tmp;
  try {
    tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'yotta-verify-bootstrap-'));
    const packDir = path.join(tmp, 'pack');
    fs.mkdirSync(packDir, { recursive: true });
    const packed = runNpmPack(verifier, opts, packDir);
    if (packed.error) return { ok: false, error: '元信自举下载失败: ' + packed.error };
    const extractDir = path.join(tmp, 'extract');
    fs.mkdirSync(extractDir, { recursive: true });
    const extractedVerifier = extractTarball(packed.tarball, extractDir);
    if (extractedVerifier.error) return { ok: false, error: '元信自举解包失败: ' + extractedVerifier.error };
    const engine = path.join(extractedVerifier.pkgDir, 'scripts', 'yotta_verify.py');
    if (!fs.existsSync(engine)) return { ok: false, error: '元信包内缺少 scripts/yotta_verify.py' };

    // 0.29.5 S4：自举落点改为运行时缓存（不污染目标目录；如 yottacode 的 skill-inventory）。
    // 安全边界不变：目标目录里未受信记录的元信副本一律不用（v0.19.13 反劫持模型），
    // 受信记录匹配（含记录指向目标目录副本）时才直接使用。
    const runtimeDir = verifierRuntimeRoot();
    out('  元信未安装，使用可信源包自举到运行时缓存（' + runtimeDir + '）并先自扫。');
    const result = installOne(verifier, runtimeDir, {
      ...opts,
      force: true,
      skipScan: false,
      bootstrap: true,
      verify: engine,
    });
    if (result.status !== 'ok') return { ok: false, error: '元信自举失败: ' + result.note };
    const installedEngine = path.join(runtimeDir, 'yotta-verify', 'scripts', 'yotta_verify.py');
    if (!fs.existsSync(installedEngine)) return { ok: false, error: '元信自举后未找到安装引擎' };
    if (!recordTrustedVerifier(runtimeDir)) {
      return { ok: false, error: '元信自举后身份 / 摘要校验未通过（fail-closed，不执行该引擎）' };
    }
    return { ok: true, engine: installedEngine, mode: 'trusted-bootstrap' };
  } finally {
    if (tmp) fs.rmSync(tmp, { recursive: true, force: true });
  }
}

const installOne = createInstaller({
  runNpmPack,
  extractTarball,
  copyDir: (src, dst, options) => {
    const skip = new Set(COPY_SKIP);
    for (const name of (options && options.keep) || []) skip.delete(name);
    copyDir(src, dst, skip, true);
  },
  readInstalledVersion,
  ensureGate,
  scanTarget,
  appendEvidence: evidenceLib.appendEvidence,
});

function summarizeInstallResults(results) {
  return {
    planned: results.filter(r => r.status === 'planned').length,
    install: results.filter(r => r.status === 'planned' && r.planned === 'install').length,
    update: results.filter(r => r.status === 'planned' && r.planned === 'update').length,
    ok: results.filter(r => r.status === 'ok').length,
    skip: results.filter(r => r.status === 'skip').length,
    failed: results.filter(r => r.status === 'fail').length,
  };
}

function runInstall(opts, dest) {
  const quiet = Boolean(opts.dryRun && opts.json);
  const skills = opts.hubScope ? selectHubSkills(opts) : selectSkills(opts);
  if (skills.length === 0) {
    if (!quiet) out('过滤后没有匹配的技能（--only / --domain），未执行任何操作。');
    process.exitCode = 2;
    return { failed: 1, exitCode: 2, results: [], summary: summarizeInstallResults([]) };
  }
  if (!quiet) {
    out('yotta-skills（元阁）v' + VERSION + ' —— 安装 ' + skills.length + ' 个技能 -> ' + dest);
    const sample = skills.find((s) => s.version !== 'latest') || null;
    out('版本策略: ' + (opts.pin
      ? 'pin（锁死清单精确版本，默认）' + (skills.some((s) => s.version === 'latest') ? '；特殊家族跟随各自 npm latest' : '')
      : 'range（' + (sample ? skillRange(sample) : 'latest') + '，跟随最新 patch）'));
  }
  const results = [];
  let failed = 0;
  let exitCode = 0;
  for (const s of skills) {
    const r = installOne(s, dest, opts);
    results.push(r);
    if (r.status === 'ok') {
      if (s.slug === 'yotta-verify') recordTrustedVerifier(dest);
      if (!quiet) {
        if (r.gate && r.gate.mode === 'explicit-unverified') {
          out('  ⚠ ' + s.slug.padEnd(22) + '未执行装前扫描（explicit-unverified）');
        }
        out('  ✔ ' + s.slug.padEnd(22) + s.name + '  -> ' + (r.version || '?'));
      }
    }
    else if (r.status === 'planned') {
      if (!quiet) {
        out('  [' + (r.planned === 'update' ? '将更新' : '将安装') + '] ' +
          s.slug.padEnd(22) + s.name + '  ' + (r.note || ''));
      }
    }
    else if (r.status === 'skip') {
      if (!quiet) out('  - ' + s.slug.padEnd(22) + s.name + '  （' + r.note + '，v' + r.version + '）');
    }
    else {
      failed++;
      exitCode = Math.max(exitCode, r.exitCode || 1);
      if (!quiet) out('  ✘ ' + s.slug.padEnd(22) + s.name + '  失败: ' + r.note);
    }
  }
  const summary = summarizeInstallResults(results);
  if (!quiet) {
    out('');
    if (opts.dryRun) {
      out('汇总: 将安装/更新 ' + summary.planned + ' / 已是最新 ' + summary.skip + ' / 失败 ' + failed + '（dry-run 预览）');
    } else {
      out('汇总: 成功 ' + summary.ok + ' / 跳过(已是最新) ' + summary.skip + ' / 失败 ' + failed + '（共 ' + results.length + '）');
    }
  }
  if (failed > 0) process.exitCode = exitCode || 1;
  return { failed, exitCode, results, summary };
}

function runUpdate(opts, dest) {
  const quiet = Boolean(opts.dryRun && opts.json);
  let skills = opts.hubScope ? selectHubSkills(opts) : selectSkills(opts);
  if (!quiet) out('yotta-skills（元阁）v' + VERSION + ' —— 增量更新 -> ' + dest);
  if (opts.installedOnly) {
    const candidates = skills.length;
    skills = skills.filter((s) => readInstalledVersion(path.join(dest, s.slug)) !== null);
    if (!quiet) out('范围: 仅已安装技能（--installed-only；候选 ' + candidates + ' / 已装 ' + skills.length + '）');
    if (skills.length === 0) {
      if (!quiet) out('目标目录未发现已安装的元阁家族技能，无动作（退出码 0）。');
      return { failed: 0, exitCode: 0, results: [], summary: summarizeInstallResults([]) };
    }
  } else if (skills.length === 0) {
    if (!quiet) out('过滤后没有匹配的技能（--only / --domain），未执行任何操作。');
    process.exitCode = 2;
    return { failed: 1, exitCode: 2, results: [], summary: summarizeInstallResults([]) };
  }
  const results = [];
  let failed = 0;
  let exitCode = 0;
  const pinExact = opts.pin !== false;
  for (const s of skills) {
    const existing = readInstalledVersion(path.join(dest, s.slug));
    const relation = versionRelation(existing, s.version);
    if (!opts.force && pinExact && relation === 'equal') {
      if (!quiet) out('  - ' + s.slug.padEnd(22) + s.name + '  （已是最新，v' + existing + '）');
      results.push({ skill: s, status: 'skip', version: existing, note: '已是最新' });
      continue;
    }
    if (!opts.force && pinExact && relation === 'local-ahead') {
      if (!quiet) {
        out('  - ' + s.slug.padEnd(22) + s.name + '  （本地领先 v' + existing + ' > 目标 v' + s.version +
          '，保留不降级；如需强制覆盖用 --force）');
      }
      results.push({ skill: s, status: 'skip', version: existing, note: '本地领先，保留不降级' });
      continue;
    }
    if (!opts.force && pinExact && relation === 'unknown') {
      if (!quiet) {
        out('  - ' + s.slug.padEnd(22) + s.name + '  （无法比较版本（本地 v' + existing + ' / 目标 v' + s.version +
          '），保留；如需强制覆盖用 --force）');
      }
      results.push({ skill: s, status: 'skip', version: existing, note: '无法比较版本，保留' });
      continue;
    }
    const r = installOne(s, dest, opts);
    results.push(r);
    if (r.status === 'ok') {
      if (s.slug === 'yotta-verify') recordTrustedVerifier(dest);
      if (!quiet) {
        if (r.gate && r.gate.mode === 'explicit-unverified') {
          out('  ⚠ ' + s.slug.padEnd(22) + '未执行装前扫描（explicit-unverified）');
        }
        out('  ✔ ' + s.slug.padEnd(22) + s.name + '  -> ' + (r.version || '?') + (existing ? '（原 v' + existing + '）' : '（新装）'));
      }
    }
    else if (r.status === 'planned') {
      if (!quiet) {
        out('  [' + (r.planned === 'update' ? '将更新' : '将安装') + '] ' +
          s.slug.padEnd(22) + s.name + '  ' + (r.note || ''));
      }
    }
    else if (r.status === 'skip') {
      if (!quiet) out('  - ' + s.slug.padEnd(22) + s.name + '  （' + r.note + '）');
    }
    else {
      failed++;
      exitCode = Math.max(exitCode, r.exitCode || 1);
      if (!quiet) out('  ✘ ' + s.slug.padEnd(22) + s.name + '  失败: ' + r.note);
    }
  }
  const summary = summarizeInstallResults(results);
  if (!quiet) {
    out('');
    if (opts.dryRun) {
      out('汇总: 将安装/更新 ' + summary.planned + ' / 已是最新 ' + summary.skip + ' / 失败 ' + failed + '（dry-run 预览）');
    } else {
      out('汇总: 更新 ' + summary.ok + ' / 已是最新 ' + summary.skip + ' / 失败 ' + failed);
    }
  }
  if (failed > 0) process.exitCode = exitCode || 1;
  return { failed, exitCode, results, summary };
}

// ── doctor / rollback ─────────────────────────────────────────────────────
function readInstalledManifest(target) {
  const file = path.join(target, 'skill-manifest.json');
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (_) {
    return null;
  }
}

function runCustomDoctor(skillDir, dest) {
  const manifest = readInstalledManifest(skillDir);
  if (!manifest || !manifest.install || !manifest.install.doctor) {
    return { ok: true, skipped: true, error: null, result: null };
  }
  if (manifest.trust !== 'yottameta') {
    return {
      ok: false,
      skipped: false,
      error: 'manifest trust 不是 yottameta，拒绝执行自定义 doctor',
      result: null,
    };
  }
  return lifecycleLib.runPhase(skillDir, manifest, 'doctor', {
    skillDir,
    packageDir: skillDir,
    dest,
  });
}

function withDoctorTarget(skill, target) {
  return Object.assign({}, skill, { target });
}

function selfDoctorTarget(dest) {
  const meta = readInstalledMeta(dest);
  const manifest = readInstalledManifest(dest);
  const candidates = [
    manifest && manifest.slug,
    meta.name,
    path.basename(dest),
  ]
    .filter(Boolean)
    .map((value) => String(value).trim().toLowerCase());

  for (const slug of candidates) {
    const skill = familySkillFor(slug);
    if (skill) return withDoctorTarget(skill, dest);
  }
  return null;
}

function doctorTargets(opts, dest) {
  const self = selfDoctorTarget(dest);
  if (opts.slug) {
    if (self && self.slug === opts.slug) return [self];
    const skill = familySkillFor(opts.slug);
    return skill ? [withDoctorTarget(skill, path.join(dest, skill.slug))] : [];
  }
  if (opts.skills.length) {
    const targets = [];
    for (const slug of opts.skills) {
      if (self && self.slug === slug) {
        targets.push(self);
        continue;
      }
      const skill = familySkillFor(slug);
      if (skill) targets.push(withDoctorTarget(skill, path.join(dest, skill.slug)));
    }
    return targets;
  }
  const found = [];
  let entries;
  try { entries = fs.readdirSync(dest, { withFileTypes: true }); } catch (_) { return self ? [self] : found; }
  for (const entry of entries) {
    if (!entry.isDirectory() || !/^yotta-/.test(entry.name)) continue;
    const skill = familySkillFor(entry.name);
    if (skill) found.push(withDoctorTarget(skill, path.join(dest, skill.slug)));
  }
  if (found.length === 0 && self) return [self];
  return found;
}

function doctorExitCode(payload) {
  if (payload.ok) return 0;
  if (payload.checked === 0) return 4;
  const manifestFailure = payload.results.some((result) =>
    (result.checks || []).some((check) =>
      (check.id === 'manifest' || check.id === 'manifest_trust') && !check.ok));
  return manifestFailure ? 6 : 1;
}

function runDoctor(opts, dest) {
  const scan = require('../lib/skills-scan');
  const registry = scan.readRegistry();
  const targets = doctorTargets(opts, dest);
  const results = [];
  const errors = [];
  const warnings = [];
  const fixes = [];

  if (targets.length === 0) {
    errors.push(opts.slug ? '未找到技能: ' + opts.slug : '目标目录下没有可检查的元阁家族技能');
  }

  for (const skill of targets) {
    const target = skill.target || path.join(dest, skill.slug);
    const result = healthLib.checkInstalledSkill({
      slug: skill.slug,
      target,
      expectedVersion: skill.version || null,
      expectedPackage: skill.pkg || null,
      registry,
    });
    const custom = runCustomDoctor(target, dest);
    result.custom_doctor = {
      ok: !!custom.ok,
      skipped: !!custom.skipped,
      error: custom.error || null,
      result: custom.result || null,
    };
    if (!custom.ok) {
      result.ok = false;
      result.errors.push('自定义 doctor 失败: ' + (custom.error || '未知错误'));
      result.checks.push({
        id: 'custom_doctor',
        ok: false,
        severity: 'error',
        message: '自定义 doctor 失败: ' + (custom.error || '未知错误'),
        hint: '修复技能包内的 doctor 脚本后重试',
      });
    } else if (!custom.skipped) {
      result.checks.push({
        id: 'custom_doctor',
        ok: true,
        severity: 'info',
        message: '自定义 doctor 通过',
        hint: null,
      });
    }
    results.push(result);
    errors.push.apply(errors, result.errors);
    warnings.push.apply(warnings, result.warnings);
    fixes.push.apply(fixes, result.fixes);
  }

  const dependencies = probeDependencies(opts);
  const payload = {
    ok: errors.length === 0,
    dir: dest,
    checked: results.length,
    results,
    errors,
    warnings,
    fixes: Array.from(new Set(fixes)),
    dependencies,
  };
  const code = doctorExitCode(payload);
  if (opts.json) {
    out(JSON.stringify(payload, null, 2));
  } else {
    out('yotta-skills（元阁）v' + VERSION + ' —— doctor');
    out('目标: ' + dest);
    for (const result of results) {
      out('');
      out((result.ok ? '✔ ' : '✘ ') + result.slug + ' v' + (result.version || '未知'));
      for (const check of result.checks) {
        out('  ' + (check.ok ? '✔' : '✘') + ' ' + check.message + (check.hint ? '（修复: ' + check.hint + '）' : ''));
      }
    }
    out('');
    out('依赖自检（只告警不失败）:');
    for (const dep of dependencies) {
      const mark = dep.ok ? '✔' : (dep.optional ? '△' : '✘');
      out('  ' + mark + ' ' + dep.name + (dep.version ? ' ' + dep.version : '') +
        '（需要 ' + dep.need + (dep.optional ? '；回退通道，可选' : '') + '）' +
        (dep.ok ? '' : ' —— 影响：' + dep.why));
      if (!dep.ok && dep.fix) out('      修复：' + dep.fix);
    }
    for (const item of warnings) out('[警告] ' + item);
    for (const item of fixes) out('[建议] ' + item);
    if (!payload.ok) out('doctor 未通过：请按上面的修复建议处理后重试。');
  }
  process.exitCode = code;
  return payload;
}

function latestRollbackTarget(home) {
  const file = path.join(home, '.yottaskills', 'install-log.jsonl');
  let lines;
  try { lines = fs.readFileSync(file, 'utf8').split(/\r?\n/).filter(Boolean); } catch (_) { return null; }
  for (let i = lines.length - 1; i >= 0; i--) {
    let entry;
    try { entry = JSON.parse(lines[i]); } catch (_) { continue; }
    if (!entry.skill || !entry.snapshot) continue;
    if (!fs.existsSync(entry.snapshot)) continue;
    if (!/^[a-z0-9][a-z0-9-]*$/.test(entry.skill)) continue;
    const expectedRoot = path.resolve(snapshotLib.snapshotRoot(home, entry.skill)) + path.sep;
    if (!path.resolve(entry.snapshot).startsWith(expectedRoot)) continue;
    const validation = snapshotLib.validateSnapshot(entry.snapshot);
    if (validation.ok) return { slug: entry.skill, snapshot: entry.snapshot };
  }
  return null;
}

function runRollback(opts, dest) {
  const home = os.homedir();
  const requestedSlug = opts.slug || (opts.skills.length ? opts.skills[0] : null);

  if (opts.list) {
    const rows = snapshotLib.listSnapshots(home, requestedSlug);
    const payload = {
      ok: true,
      dir: dest || null,
      slug: requestedSlug || null,
      count: rows.filter((row) => row.valid).length,
      snapshots: rows,
    };
    if (opts.json) out(JSON.stringify(payload, null, 2));
    else {
      out('yotta-skills（元阁）v' + VERSION + ' —— rollback 快照');
      for (const row of rows) {
        out('  ' + (row.valid ? '✔' : '✘') + ' ' + row.slug + ' v' + (row.version || '未知') + '  ' + row.path + (row.reason ? '（' + row.reason + '）' : ''));
      }
      out('可用快照: ' + payload.count + ' / ' + rows.length);
    }
    return payload;
  }

  let slug = requestedSlug;
  let selected = null;
  if (slug) {
    const rows = snapshotLib.listSnapshots(home, slug);
    selected = rows.find((row) => row.valid) || rows[0] || null;
  } else {
    const latest = latestRollbackTarget(home);
    if (latest) {
      slug = latest.slug;
      selected = snapshotLib.listSnapshots(home, slug).find((row) => row.path === latest.snapshot && row.valid) || null;
    }
  }

  if (!slug) {
    const payload = { ok: false, dir: dest, slug: null, errors: ['安装记录中没有可回滚的技能快照'] };
    if (opts.json) out(JSON.stringify(payload, null, 2));
    else out('回滚失败：安装记录中没有可回滚的技能快照。');
    process.exitCode = 1;
    return payload;
  }
  if (!selected || !selected.valid) {
    const payload = {
      ok: false,
      dir: dest,
      slug,
      errors: [selected && selected.reason ? '选中的快照不可用: ' + selected.reason : '没有可用快照'],
    };
    if (opts.json) out(JSON.stringify(payload, null, 2));
    else out('回滚失败：' + payload.errors[0]);
    process.exitCode = 1;
    return payload;
  }

  const target = path.join(dest, slug);
  const restored = snapshotLib.restoreSnapshot(selected.path, target);
  if (!restored.ok) {
    const payload = { ok: false, dir: dest, slug, snapshot: selected.path, errors: [restored.error] };
    if (opts.json) out(JSON.stringify(payload, null, 2));
    else out('回滚失败：' + restored.error);
    process.exitCode = 1;
    return payload;
  }

  const family = familySkillFor(slug);
  const scan = require('../lib/skills-scan');
  const doctor = healthLib.checkInstalledSkill({
    slug,
    target,
    expectedVersion: restored.version && restored.version !== 'unknown' ? restored.version : null,
    expectedPackage: family ? family.pkg : null,
    registry: scan.readRegistry(),
  });
  const custom = runCustomDoctor(target, dest);
  if (!custom.ok) {
    doctor.ok = false;
    doctor.errors.push('自定义 doctor 失败: ' + (custom.error || '未知错误'));
  }

  const payload = {
    ok: doctor.ok,
    dir: dest,
    slug,
    snapshot: selected.path,
    version: restored.version,
    doctor,
    errors: doctor.errors,
    warnings: doctor.warnings,
    fixes: doctor.fixes,
    reindexed: false,
  };
  try {
    evidenceLib.appendEvidence({
      event: 'rollback',
      skill: slug,
      package: family ? family.pkg : null,
      version: restored.version,
      decision: doctor.ok ? 'ok' : 'fail',
      snapshot: selected.path,
    }, { homeDir: home });
  } catch (error) {
    payload.ok = false;
    payload.errors.push('回滚证据写入失败: ' + error.message);
  }
  if (payload.ok && !opts.noReindex) {
    try {
      reindexRegistry({ ...opts, dir: dest });
      payload.reindexed = true;
    } catch (error) {
      payload.warnings.push('回滚完成，但注册表重扫失败: ' + error.message);
    }
  }

  if (opts.json) {
    out(JSON.stringify(payload, null, 2));
  } else {
    out('yotta-skills（元阁）v' + VERSION + ' —— rollback');
    out('技能: ' + slug);
    out('快照: ' + selected.path);
    out('结果: ' + (payload.ok ? '✔ 已恢复 v' + (restored.version || '未知') : '✘ 恢复后 doctor 未通过'));
    if (payload.errors.length) out('错误: ' + payload.errors.join('; '));
    if (payload.warnings.length) out('警告: ' + payload.warnings.join('; '));
    if (payload.reindexed) out('已重扫本地技能注册表。');
  }
  process.exitCode = payload.ok ? 0 : 1;
  return payload;
}

// ── 展示 ───────────────────────────────────────────────────────────────────
function printList(opts) {
  const skills = opts.skills.length ? selectSkills(opts) : MANIFEST;
  out('yotta-skills（元阁）v' + VERSION + ' —— 全家技能清单（' + skills.length + ' 个）');
  out('版本策略: ' + (opts.pin ? 'pin（精确锁定，默认）' : 'range（' + skillRange(skills[0]) + ' 起，跟随最新 patch）'));
  out('');
  for (const s of skills) {
    out('  ' + s.slug.padEnd(22) + s.name.padEnd(5) + ' ' + specOf(s, opts.pin).padEnd(52) + ' ' + s.version + '  ' + s.desc);
  }
  out('');
  out('安装: yotta-skills install --agent <name> 或 --dir <path>；预览: --dry-run；更新: update。');
}

function printHelp() {
  const help = require('../lib/cli-help');
  out('yotta-skills（元阁）v' + VERSION + ' —— npx 一次装齐全家技能');
  out('');
  out('用法:');
  for (const group of help.CLI_HELP_MODEL) {
    for (const cmd of group.commands) {
      out('  yotta-skills ' + cmd.usage + '  ' + cmd.what);
      for (const sub of cmd.subcommands || []) {
        out('  yotta-skills ' + sub.usage + '  ' + sub.what);
        if (sub.impact) out('      ' + sub.impact);
        if (sub.alternative) out('      ' + sub.alternative);
      }
    }
  }
  out('');
  out('选项:');
  for (const opt of help.CLI_GLOBAL_OPTIONS) {
    out('  ' + (opt.flag + (opt.arg ? ' ' + opt.arg : '')).padEnd(22) + opt.what);
  }
  out('');
  out('支持智能体: ' + Object.keys(AGENT_DIRS).length + ' 个已收录映射（本机实际发现用 yotta-skills hub hosts）');
  out('依赖: Node.js 18+（必需）；npm 与系统 tar 为回退通道（内置拉包 / 内置解包为主）；元信 scan 需要 Python 3.8+（--python / YOTTA_SKILLS_PYTHON 可指向宿主自带 Python）。');
  out('环境变量: YOTTA_SKILLS_FETCH（builtin|npm）/ YOTTA_SKILLS_EXTRACT（builtin|tar）/ YOTTA_SKILLS_NPM / YOTTA_SKILLS_PYTHON / YOTTA_SKILLS_VERIFY / YOTTA_SKILLS_NPM_FLAGS / YOTTA_SKILLS_REGISTRY / YOTTA_SKILLS_REGISTRY_FILE / YOTTA_SKILLS_MANIFEST 可覆盖。');
}



// ── 技能盘点 / re-index（自研零依赖扫描核心） ────────────────────────────────
/** 重扫所有技能根目录并增量合并进注册表；返回 { result, registry, changes }。 */
function reindexRegistry(opts) {
  const scan = require('../lib/skills-scan');
  const extraDirs = opts.dir ? [opts.dir] : [];
  const roots = scan.defaultRoots({ extraDirs: extraDirs, project: opts.project });
  const result = scan.scanRoots(roots);
  const prev = scan.readRegistry();
  const { registry, changes } = scan.mergeRegistry(result, prev);
  scan.saveRegistry(registry);
  return { result, registry, changes };
}

function runInventory(opts) {
  const scan = require('../lib/skills-scan');
  const { result, registry, changes } = reindexRegistry(opts);
  if (opts.json) {
    out(JSON.stringify({
      generated_at: registry.updated,
      note: registry.note,
      scanned: result.scanned,
      errors: result.errors,
      changes: changes,
      skills: Object.values(registry.skills).sort((a, b) => a.slug.localeCompare(b.slug)),
    }, null, 2));
    return;
  }
  out(scan.formatInventory(registry));
  out('');
  out('本次变化: 新增 ' + changes.added.length + ' / 更新 ' + changes.updated.length + ' / 消失 ' + changes.gone.length);
  if (result.errors.length) {
    out('跳过不存在目录 ' + result.errors.length + ' 个: ' + result.errors.map((e) => e.dir).join('; '));
  }
}

/** --reindex：重扫 + 增量合并，变化聚焦输出（手动触发 / 供钩子或脚本调用）。 */
function runReindex(opts) {
  const scan = require('../lib/skills-scan');
  const { result, registry, changes } = reindexRegistry(opts);
  if (opts.json) {
    out(JSON.stringify({
      reindexed_at: registry.updated,
      note: registry.note,
      count: Object.values(registry.skills).filter((s) => s.status !== 'gone').length,
      changes: changes,
      errors: result.errors,
      scanned: result.scanned,
    }, null, 2));
    return;
  }
  out('re-index 完成: 新增 ' + changes.added.length + ' / 更新 ' + changes.updated.length + ' / 消失 ' + changes.gone.length);
  for (const slug of changes.added) out('  + ' + slug);
  for (const slug of changes.updated) out('  ~ ' + slug);
  for (const slug of changes.gone) out('  - ' + slug);
  if (result.errors.length) {
    out('跳过不存在目录 ' + result.errors.length + ' 个');
  }
  out('注册表: ' + scan.registryPath());
}

/**
 * o1.route 动态扩展口：静态结果先算必算；provider 只允许在已装注册表白名单内增补 / 重排，
 * 任何失败都回静态结果（fail-open）。协议见 references/provider-protocol.md。
 */
function applyDynamicRoute(result, registry, opts) {
  const provider = require('../lib/provider');
  const { PLAYBOOKS } = require('../lib/route');
  const usage = usageJournalLib.readUsage();
  const payload = routeFeaturesLib.buildRouteFeatures({
    request: String(opts.route || ''),
    registry,
    staticResult: result,
    usage,
    playbooks: PLAYBOOKS,
  });
  let run;
  try {
    run = provider.runCapability('o1.route', payload);
  } catch (e) {
    return routeDynamicLib.dynamicBlock('error', '', '动态路由装载失败：' + e.message);
  }
  const block = routeDynamicLib.dynamicBlock(run.status, run.provider_id, run.note || run.message || '');
  if (run.status !== 'active' || !run.data || typeof run.data !== 'object') return block;
  return routeDynamicLib.applyDynamicData(result, run.data, registry, {
    providerId: run.provider_id,
  });
}

function dynamicRouteText(block) {
  if (!block) return '';
  if (block.status === 'active') {
    const who = block.provider_id ? '提供方 ' + block.provider_id : '提供方';
    const confidence = block.confidence ? '；置信度 ' + block.confidence : '';
    return '已应用（' + who + confidence + '；新增 ' + block.added.length + ' / 丢弃 ' + block.dropped.length + '）';
  }
  if (block.status === 'license_required') return '需授权（该能力需要授权后使用；静态路由不受影响）';
  if (block.status === 'timeout') return '未生效（提供方超时，已回落静态路由）';
  if (block.status === 'invalid_output') return '未生效（提供方输出无效，已回落静态路由）';
  if (block.status === 'error') return '未生效（提供方异常，已回落静态路由）';
  return block.status;
}

/** --route：静态编排路由，输出组合、顺序、角色、缺失技能建议与其他已装技能候选。 */
function runRoute(opts) {
  const { routeRequest, defaultYottaSlugs } = require('../lib/route');
  const { registry } = reindexRegistry(opts);
  const yottaSlugs = new Set([...defaultYottaSlugs(), ...MANIFEST.map((s) => s.slug)]);
  const result = routeRequest(opts.route, { registry, yottaSlugs });
  result.dynamic = applyDynamicRoute(result, registry, opts);
  try {
    usageJournalLib.recordRoute({
      playbook: result.playbook.id,
      confidence: result.confidence,
      skills: result.skills.map((skill) => skill.slug),
    });
  } catch (_) {
    // 使用记录失败不阻断路由
  }
  if (opts.json) {
    out(JSON.stringify(result, null, 2));
    return;
  }
  out('路由结果: ' + result.playbook.name + '（置信度: ' + result.confidence + '）');
  out('适配意图: ' + result.playbook.intent);
  out('依据: ' + (result.matched_keywords.length ? result.matched_keywords.join('、') : '无明确匹配，回退到入口澄清'));
  out('');
  out('调用顺序:');
  for (const skill of result.skills) {
    const status = skill.installed
      ? '已装' + (skill.version ? ' v' + skill.version : '')
      : '缺失';
    const conflictHint = skill.conflicts && skill.conflicts.length
      ? '（其他副本: ' + skill.conflicts
        .map((item) => (item.source || '其他') + ' v' + (item.version || '?'))
        .join('、') + '）'
      : '';
    out('  ' + skill.order + '. ' + skill.slug + ' [' + status + '] - ' + skill.role + conflictHint);
  }
  if (result.missing_skills.length) {
    out('');
    out('缺失技能: ' + result.missing_skills.map((skill) => skill.slug).join(', '));
    out('安装命令: ' + result.install_command);
    out('安全提示: 安装前请先执行装前安全扫描；本命令不会自动安装。');
  }
  if (result.other_skill_candidates.length) {
    out('');
    out('其他已装技能候选（非元阁家族，仅本地机械匹配 frontmatter description）:');
    for (const c of result.other_skill_candidates) {
      out('  - ' + c.slug + ' v' + c.version + ' [' + (c.sources || []).join(',') + ']');
      out('    匹配: ' + c.matched_terms.join('、') + '（得分 ' + c.score + '）· 扫描状态: ' + (c.scan_status === 'not_scanned' ? '未扫描' : c.scan_status));
      out('    ' + (c.description || ''));
    }
    out('安全提示: 其他已装技能只读 frontmatter description 做机械匹配，不读取全文指令、不自动调用；使用/安装前请先执行装前安全扫描，决定权在用户。');
  }
  if (result.dynamic.status !== 'not_installed') {
    out('');
    out('动态路由: ' + dynamicRouteText(result.dynamic));
    if (result.dynamic.status === 'active' && opts.explain) {
      if (result.dynamic.summary) out('动态摘要: ' + result.dynamic.summary);
      for (const reason of result.dynamic.reasons || []) out('  - ' + reason);
    }
  }
  out('');
  out('应用模式: 显式调用（可经用户确认后切换为按场景自动调用）');
  out('说明: ' + result.disclaimer);
}

function runUsage(opts) {
  const action = opts.rest[0] || 'status';
  if (action === 'status') {
    const state = usageJournalLib.readUsage();
    if (opts.json) {
      out(JSON.stringify(state, null, 2));
      return;
    }
    out('元阁本地使用记录：' + (state.enabled ? '已开启' : '已关闭'));
    out('文件: ' + usageJournalLib.usageFilePath());
    const skills = Object.keys(state.skills || {}).sort();
    if (!skills.length) {
      out('暂无记录。');
      return;
    }
    for (const slug of skills) {
      const item = state.skills[slug];
      out('  ' + slug + '  used=' + item.used + ' named=' + item.named
        + ' accepted=' + item.accepted + ' route_hits=' + item.route_hits
        + ' pairs=' + Object.keys(item.pairs || {}).length);
    }
    return;
  }
  if (action === 'enable' || action === 'disable') {
    const state = usageJournalLib.setEnabled(action === 'enable');
    if (opts.json) {
      out(JSON.stringify(state, null, 2));
      return;
    }
    out('元阁本地使用记录已' + (state.enabled ? '开启' : '关闭') + '。');
    out('文件: ' + usageJournalLib.usageFilePath());
    return;
  }
  if (action === 'mark') {
    if (!opts.skill) die('usage mark 缺少 --skill', 2, '例如 --skill yotta-memory。');
    if (!opts.signal) die('usage mark 缺少 --signal', 2, '可用 used / named / accepted。');
    let state;
    try {
      state = usageJournalLib.markUsage(opts.skill, opts.signal);
    } catch (error) {
      die(error.message, 2, '请检查 --skill 与 --signal。');
    }
    if (opts.json) {
      out(JSON.stringify(state, null, 2));
      return;
    }
    out('已记录：' + opts.skill + ' / ' + opts.signal);
    return;
  }
  if (action === 'reset') {
    if (!opts.yes) die('usage reset 需要 --yes 确认', 2, '该操作会清空本地使用记录。');
    const file = usageJournalLib.resetUsage();
    if (opts.json) {
      out(JSON.stringify({ reset: true, file }, null, 2));
      return;
    }
    out('已清空本地使用记录：' + file);
    return;
  }
  die('未知 usage 子命令: ' + action, 2, '支持 status / enable / disable / mark / reset。');
}

function m1StatusText(block) {
  if (!block) return '';
  if (block.status === 'active') {
    return '已应用（提供方 ' + (block.provider_id || '-') + '；建议 '
      + block.decisions.length + ' 条）';
  }
  if (block.status === 'license_required') return '需授权（该能力需要授权后使用）';
  if (block.status === 'timeout') return '未生效（提供方超时）';
  if (block.status === 'invalid_output') return '未生效（提供方输出无效）';
  if (block.status === 'error') return '未生效（提供方异常）';
  return block.status;
}

function runDecideMemory(opts) {
  if (opts.dryRun && opts.promote) {
    die('--dry-run 与 --promote 不能同时使用', 2, '默认就是只读；需要写建议文件时只加 --promote。');
  }
  const { registry } = reindexRegistry(opts);
  const usage = usageJournalLib.readUsage();
  const snapshot = m1FeaturesLib.buildFeatureSnapshot(registry, usage);
  const provider = require('../lib/provider');
  let run;
  try {
    run = provider.runCapability('m1.adjudicate', snapshot);
  } catch (error) {
    run = { status: 'error', provider_id: '', note: 'M1 装载失败：' + error.message };
  }
  const block = {
    status: run.status || 'error',
    provider_id: run.provider_id || '',
    applied: false,
    mode: opts.promote ? 'recommendation' : 'dry-run',
    decisions: [],
    summary: { promote: 0, hold: 0, demote: 0 },
    dropped: [],
    note: run.note || run.message || '',
  };
  if (run.status === 'active' && run.data && typeof run.data === 'object') {
    const allowed = new Set(Object.keys(registry.skills || {}));
    const verdicts = new Set(['promote', 'hold', 'demote']);
    const requested = Array.isArray(run.data.decisions) ? run.data.decisions : [];
    for (const raw of requested) {
      const slug = raw && typeof raw === 'object' ? String(raw.slug || '') : '';
      const score = raw && Number(raw.score);
      const verdict = raw && String(raw.verdict || '');
      if (!slug || !allowed.has(slug) || !verdicts.has(verdict) || !Number.isFinite(score) || score < 0 || score > 100) {
        if (slug) block.dropped.push(slug);
        continue;
      }
      const reasons = Array.isArray(raw.reasons)
        ? raw.reasons.filter((item) => typeof item === 'string').slice(0, 20)
        : [];
      block.decisions.push({
        slug,
        verdict,
        score: Math.round(score),
        reasons,
        signals: raw.signals && typeof raw.signals === 'object' && !Array.isArray(raw.signals)
          ? raw.signals
          : {},
      });
    }
    block.decisions.sort((left, right) => right.score - left.score || left.slug.localeCompare(right.slug));
    for (const decision of block.decisions) {
      if (block.summary[decision.verdict] !== undefined) block.summary[decision.verdict] += 1;
    }
    block.applied = block.decisions.length > 0;
  }

  let reportFile = null;
  if (opts.promote && block.status === 'active') {
    const report = {
      schema: 1,
      generated_at: snapshot.generated_at,
      provider_id: block.provider_id,
      mode: 'recommendation',
      decisions: block.decisions,
      memory_candidates: m1FeaturesLib.buildMemoryCandidates(block.decisions, registry),
      note: '只写本地建议文件；不写元忆、不删除任何内容。',
    };
    try {
      reportFile = m1FeaturesLib.writeAdjudication(report);
      block.report_file = reportFile;
    } catch (error) {
      die('M1 建议文件写入失败: ' + error.message, 1, '请检查 ~/.yottaskills 目录权限。');
    }
  }

  if (opts.json) {
    out(JSON.stringify({ schema: 1, generated_at: snapshot.generated_at, m1: block }, null, 2));
    return;
  }
  out('元阁记忆裁决（M1）');
  out('状态: ' + m1StatusText(block));
  if (block.status === 'active') {
    out('建议汇总: promote ' + block.summary.promote + ' / hold ' + block.summary.hold
      + ' / demote ' + block.summary.demote + '；丢弃 ' + block.dropped.length);
    for (const decision of block.decisions) {
      out('  [' + decision.verdict + '] ' + decision.slug + '  ' + decision.score
        + (decision.reasons.length ? '  - ' + decision.reasons.join('；') : ''));
      if (opts.explain) {
        const signals = decision.signals || {};
        out('    信号: used=' + (signals.used || 0) + ' named=' + (signals.named || 0)
          + ' accepted=' + (signals.accepted || 0) + ' route_hits=' + (signals.route_hits || 0)
          + ' distinct_pairs=' + (signals.distinct_pairs || 0)
          + ' description_quality=' + (signals.description_quality || 0)
          + ' recency=' + (signals.recency || 0));
      }
    }
    if (reportFile) out('建议文件: ' + reportFile);
  } else if (block.note) {
    out('说明: ' + block.note);
  }
  out('边界: 只建议不删除；不自动写元忆；数据不出本机。');
}

/** 装技能后自动 re-index（--no-reindex 关闭）：把本次落位结果反映进注册表。best-effort：失败不阻断安装。 */
function maybeAutoReindex(opts, dest) {
  if (opts.noReindex || opts.dryRun || !dest) return;
  const scan = require('../lib/skills-scan');
  try {
    const { changes } = reindexRegistry({ ...opts, dir: dest });
    out('');
    out('已自动 re-index 注册表（新增 ' + changes.added.length + ' / 更新 ' + changes.updated.length + ' / 消失 ' + changes.gone.length + '；注册表: ' + scan.registryPath() + '）');
  } catch (e) {
    out('');
    out('提示: 自动 re-index 跳过（' + e.message + '）；稍后可手动 --reindex 重扫');
  }
}

// ── 运行时 hook 适配层（P0-3） ───────────────────────────────────────────────
function readJsonFile(file, label) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    die(label + ' 读取失败: ' + error.message, 2, '请确认文件存在且为合法 JSON。');
  }
}

function runHook(opts) {
  const action = opts.rest[0] || 'capabilities';
  const host = opts.host || 'generic';
  const adapter = hookAdapterLib.createHookAdapter({ host });

  if (action === 'capabilities') {
    const payload = { host, capabilities: adapter.capabilities() };
    if (opts.json) out(JSON.stringify(payload, null, 2));
    else {
      out('yotta-skills（元阁）v' + VERSION + ' —— hook capabilities');
      out('宿主: ' + host);
      hookAdapterLib.EVENTS.forEach((event) => out('  ' + event.padEnd(18) + payload.capabilities[event]));
    }
    return;
  }

  if (action === 'evaluate') {
    if (!opts.event) die('hook evaluate 缺少 --event', 2, '请提供六个统一事件之一。');
    if (!opts.manifest) die('hook evaluate 缺少 --manifest', 2, '请提供 skill-manifest.json 路径。');
    const manifest = readJsonFile(opts.manifest, 'manifest');
    let context = {};
    if (opts.context) {
      try {
        context = JSON.parse(opts.context);
      } catch (error) {
        die('--context 不是合法 JSON: ' + error.message, 2, '请传入 JSON 对象。');
      }
    }
    if (!context || typeof context !== 'object' || Array.isArray(context)) {
      die('--context 必须是 JSON 对象', 2);
    }
    const result = adapter.evaluate(opts.event, manifest, context);
    const entries = result.results.length > 0
      ? result.results
      : [{ event: opts.event, skill: manifest.slug, action: null, decision: result.decision, evidence: {}, capability: adapter.capabilities()[opts.event] || 'unsupported', reason: result.user_message }];
    for (const entry of entries) {
      hookAdapterLib.appendHookEvidence({
        event: entry.event,
        skill: entry.skill,
        action: entry.action,
        result: entry.decision,
        capability: entry.capability,
        evidence: entry.evidence,
        reason: entry.reason,
      }, { homeDir: os.homedir() });
    }
    if (opts.json) out(JSON.stringify({ host, event: opts.event, ...result }, null, 2));
    else {
      out('yotta-skills（元阁）v' + VERSION + ' —— hook evaluate');
      out('宿主: ' + host + ' / 事件: ' + opts.event);
      out('决策: ' + result.decision + ' / verified: ' + result.verified);
      out(result.user_message);
      for (const entry of result.results) out('  ' + entry.action + ': ' + entry.decision + '（' + entry.capability + '）');
    }
    process.exitCode = result.decision === 'block' ? 3 : 0;
    return;
  }

  if (action === 'bind') {
    if (!opts.manifest) die('hook bind 缺少 --manifest', 2, '请提供 skill-manifest.json 路径。');
    const manifest = readJsonFile(opts.manifest, 'manifest');
    const bindings = adapter.bind(manifest, opts.event || null);
    if (opts.json) out(JSON.stringify({ host, bindings }, null, 2));
    else {
      out('yotta-skills（元阁）v' + VERSION + ' —— hook bind');
      out('宿主: ' + host + ' / 绑定 ' + bindings.length + ' 项');
      for (const binding of bindings) out('  ' + binding.id + '  ' + binding.event + '  ' + binding.action + '  ' + binding.capability);
    }
    return;
  }

  if (action === 'unbind') {
    const id = opts.rest[1];
    if (!id) die('hook unbind 缺少 binding id', 2, '先用 hook bind / list 获取 id。');
    const removed = adapter.unbind(id);
    if (opts.json) out(JSON.stringify({ host, id, removed }, null, 2));
    else out(removed ? '已解除绑定: ' + id : '未找到绑定: ' + id);
    process.exitCode = removed ? 0 : 1;
    return;
  }

  die('未知 hook 子命令: ' + action, 2, '支持 capabilities / evaluate / bind / unbind。');
}

// ── Hub（本机单点安装 + 链接分发） ─────────────────────────────────────────
function universalSkillDirs() {
  return hubTargetsLib.universalSkillDirs({ homeDir: os.homedir(), env: process.env });
}

function normalizeTargetKey(dir) {
  return hubTargetsLib.normalizeTargetKey(dir);
}

function hubScopeSummary(discovery) {
  const existing = (discovery.hosts || []).filter((host) => host.exists);
  return {
    verified: existing.filter((host) => host.verified && !host.bridgeOnly).length,
    discovered: existing.filter((host) => !host.verified && !host.bridgeOnly).length,
    bridge: existing.filter((host) => host.bridgeOnly).length,
  };
}

function hubScopeLine(opts, discovery) {
  const scope = hubScopeSummary(discovery);
  return '范围: 已核实 ' + scope.verified + ' 个目标' +
    (opts.includeDiscovered
      ? '（含自动发现 ' + scope.discovered + ' 个）'
      : '；跳过自动发现 ' + scope.discovered + ' 个（--include-discovered 纳入）') +
    '；跳过桥接 ' + scope.bridge + ' 个（锁 / 数据目录永不链接）';
}

function hubTargetDirs(opts, discovery) {
  const targets = [];
  const seen = new Set();
  // 0.29.1 U2：不接管名单 / 目录覆盖（与发现层同源 hosts.json）。
  const registry = hostsRegistryLib.readHostsRegistry({ homeDir: os.homedir(), env: process.env });
  const excludedEntry = (input) => hostsRegistryLib.excludedEntryFor(registry, input);
  const cleanupOnly = opts.hubAction === 'unlink' || opts.hubAction === 'remove';
  const add = (dir, agentId, label, meta) => {
    if (!dir) return;
    const resolved = path.resolve(dir);
    const key = normalizeTargetKey(resolved);
    if (seen.has(key)) return;
    seen.add(key);
    targets.push({
      dir: resolved,
      agentId: agentId || null,
      label: label || '指定目录',
      verified: Boolean(meta && meta.verified),
      bridgeOnly: Boolean(meta && meta.bridgeOnly),
      detection: (meta && meta.detection) || 'mapping',
      explicit: Boolean(meta && meta.explicit),
    });
  };

  if (opts.dir) {
    // Bridge dirs are never link targets, but `unlink --dir` stays available:
    // it is the explicit cleanup path for historical out-of-scope links.
    if (!cleanupOnly && agentDirsLib.isYottaCodeDir(opts.dir)) {
      die('YottaCode 自带三层技能管理（skill-inventory / skill / user-skills），不纳入元阁接管', 2,
        'YottaCode 目录由它自己管理，元阁不链接其目录。');
    }
    if (!cleanupOnly && excludedEntry({ dir: opts.dir })) {
      die('该目录在「不接管」名单：' + path.resolve(opts.dir), 2,
        '恢复接管：yotta-skills hub hosts include "' + path.resolve(opts.dir) + '"；再重新链接。');
    }
    if (!cleanupOnly &&
      agentDirsLib.isBridgeOnlyDir(opts.dir, { homeDir: os.homedir(), env: process.env })) {
      die('该目录是锁 / 数据桥接目录（XDG_STATE_HOME/skills 或 XDG_DATA_HOME/skills），永不作为链接目标', 2,
        '如需链接真实宿主目录，请改用 --agent <id> 或其它 --dir 路径。');
    }
    add(opts.dir, null, '指定目录', { explicit: true, verified: true });
    return targets;
  }
  if (opts.agent) {
    const info = AGENT_DIRS[opts.agent];
    if (!info) {
      die('未收录智能体: ' + opts.agent + '。可用: ' + Object.keys(AGENT_DIRS).join(', ') + '；或改用 --dir <路径>。',
        2, '先运行 yotta-skills hub hosts 查看本机实际技能目录。');
    }
    if (!cleanupOnly && (info.neverLink || agentDirsLib.isYottaCodeDir(resolveUserDir(info.dirs[0])))) {
      die('YottaCode 自带三层技能管理（skill-inventory / skill / user-skills），不纳入元阁接管', 2,
        'YottaCode 目录由它自己管理，元阁不链接其目录。');
    }
    if (!cleanupOnly && excludedEntry({ agentId: opts.agent })) {
      die('该智能体在「不接管」名单：' + opts.agent, 2,
        '恢复接管：yotta-skills hub hosts include ' + opts.agent + '；再重新链接。');
    }
    const override = (registry.overrides || [])
      .find((item) => String(item.agentId).toLowerCase() === opts.agent);
    const dir = override ? override.dir : resolveUserDir(info.dirs[0]);
    add(dir, opts.agent, override ? (override.label || info.label) : info.label,
      { explicit: true, verified: true });
    return targets;
  }
  if (!opts.all) {
    die('hub link / unlink 需要 --agent <id>、--dir <path> 或 --all', 2,
      '示例：yotta-skills hub link --all；或 yotta-skills hub link --agent codex。');
  }

  // 0.29.5：默认范围与面板迁移重链共用 lib/hub-targets.js 单一真源。
  for (const item of hubTargetsLib.computeHubTargets({
    discovery,
    registry,
    homeDir: os.homedir(),
    env: process.env,
    includeDiscovered: opts.includeDiscovered,
  })) {
    add(item.dir, item.agentId, item.label, item);
  }
  return targets;
}

/**
 * hub remove 的目标范围：
 * - --dir / --agent：单个显式目录（桥接目录允许作为显式清理路径）
 * - 默认：已核实宿主 ∪ 本技能链接台账中记录的目录（覆盖历史 / 死链）
 * - --include-discovered：在默认范围上纳入自动发现目录
 */
function hubRemoveTargets(opts, discovery, slug, hubDir) {
  if (opts.dir || opts.agent) return hubTargetDirs(opts, discovery);
  const targets = hubTargetDirs({ ...opts, all: true }, discovery);
  const seen = new Set(targets.map((target) => normalizeTargetKey(target.dir)));
  const recorded = hubLib.readLinkState(hubDir).links.filter((item) => item.slug === slug);
  for (const item of recorded) {
    if (!item.dir) continue;
    const resolved = path.resolve(item.dir);
    const key = normalizeTargetKey(resolved);
    if (seen.has(key)) continue;
    seen.add(key);
    targets.push({
      dir: resolved,
      agentId: item.agent || null,
      label: item.label || '台账记录目录',
      verified: false,
      bridgeOnly: false,
      detection: 'ledger',
      explicit: false,
    });
  }
  return targets;
}

const HOST_STATE_LABELS = {
  available: '可用',
  orphan: '残留·实体未确认',
  missing: '未创建',
  'marker-only': '仅标记',
  ignored: '已忽略',
};

function hostStateLabel(host) {
  const state = HOST_STATE_LABELS[host.state] || host.state || '未知';
  const manual = host.stateSource === 'manual' ? '·手动' : '';
  return state + manual;
}

function hostScopeLabel(host) {
  if (host.bridgeOnly) return '[桥接·不链接]';
  let scope = '';
  if (!host.verified) {
    // 0.29.1 U2：未核实映射 ≠ 自动发现；「自动发现」只用于文件系统扫描结果。
    scope = (host.detection === 'discovered' || host.detection === 'workspace')
      ? '·自动发现'
      : '·映射未核实';
  }
  return '[' + hostStateLabel(host) + scope + ']';
}

function hostStateCounts(hosts) {
  const counts = { available: 0, orphan: 0, 'marker-only': 0, missing: 0, ignored: 0 };
  for (const host of hosts || []) {
    counts[host.state] = (counts[host.state] || 0) + 1;
  }
  return counts;
}

function hubHostLines(discovery) {
  const lines = [];
  const existing = discovery.hosts.filter((host) => host.exists);
  const markerOnly = discovery.hosts.filter((host) => !host.exists && host.state === 'marker-only');
  const missing = discovery.hosts.filter((host) => !host.exists && host.state !== 'marker-only');
  const shown = new Set();
  for (const host of existing) {
    shown.add(String(host.label).toLowerCase());
    const marker = host.bridgeOnly ? '·' : host.state === 'available' ? '✔' : host.state === 'ignored' ? '·' : '△';
    lines.push('  ' + marker + ' ' +
      String(host.label).padEnd(28) + host.dir.padEnd(64) +
      String(host.skillCount).padStart(3) + ' 个技能  ' +
      hostScopeLabel(host));
  }
  for (const host of markerOnly) {
    shown.add(String(host.label).toLowerCase());
    lines.push('  △ ' + String(host.label).padEnd(28) + String(host.dir).padEnd(64) +
      '  0 个技能  ' + hostScopeLabel(host));
  }
  // 0.29.1 U2：CLI / 面板共用单一真源（未配对且无技能目录的标记）。
  const noSkillDir = agentDiscoveryLib.unpairedMarkers(discovery);
  for (const item of noSkillDir) {
    lines.push('  △ ' + String(item.label).padEnd(28) + '已安装，未发现技能目录  [不适用]');
  }
  return { lines, existing, missing, markerOnly, noSkillDir };
}

function printHubHosts(discovery, json) {
  if (json) {
    out(JSON.stringify(discovery, null, 2));
    return;
  }
  const view = hubHostLines(discovery);
  const counts = hostStateCounts(discovery.hosts);
  const bridgeCount = view.existing.filter((host) => host.bridgeOnly).length;
  out('yotta-skills（元阁）v' + VERSION + ' —— Hub 宿主发现（文件系统优先，不读元忆）');
  out('本机发现技能目录 ' + view.existing.length + ' 个（可用 ' + counts.available +
    ' / 残留 ' + counts.orphan + ' / 桥接 ' + bridgeCount + ' / 已忽略 ' + counts.ignored +
    '）/ 仅标记 ' + counts['marker-only'] + ' 个 / 未创建 ' + counts.missing + ' 个');
  out('默认链接范围 = 已核实目录（含残留，可清理）；--include-discovered 显式纳入自动发现目录；锁 / 数据桥接目录永不链接。');
  out('不接管名单（发现 / 显示 / 链接全部跳过）：yotta-skills hub hosts exclude <agentId|目录>；恢复用 include。');
  out('残留清理：yotta-skills hub hosts remove <目录> --purge（默认预览，--yes 执行）。');
  for (const line of view.lines) out(line);
  if (view.missing.length > 0) {
    out('');
    out('未创建技能目录 ' + view.missing.length + ' 个（已收录映射，安装后自动出现；yotta-skills hub hosts --state missing 查看）。');
  }
}

function printHubStatus(payload, discovery, json) {
  if (json) {
    out(JSON.stringify({ ...payload, discovery }, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— Hub 状态');
  out('标准: ' + payload.standard);
  out('Hub: ' + payload.hubDir);
  out('技能: ' + payload.summary.skills + ' / 非元阁技能: ' + payload.summary.external +
    ' / 链接: ' + payload.summary.links + ' / 异常链接: ' + payload.summary.brokenLinks);
  out('');
  for (const skill of payload.skills) {
    const origin = skill.origin === 'yotta' ? '元技能' : '非元阁技能（无更新源）';
    const links = skill.links.length > 0 ? skill.links.map((link) => link.label || link.agent || '链接').join(', ') : '-';
    out('  ' + skill.slug.padEnd(26) + 'v' + String(skill.version || '-').padEnd(10) +
      origin.padEnd(22) + '链接: ' + links +
      (skill.status === 'missing' ? '  [目标缺失]' : ''));
  }
  if (payload.skills.length === 0) out('  （Hub 为空；先运行 yotta-skills hub install）');
  const broken = payload.links.filter((link) => link.status !== 'ok');
  if (broken.length > 0) {
    out('');
    out('异常链接:');
    for (const link of broken) out('  ✘ ' + link.slug + '  ' + link.target + '（' + link.status + '）');
  }
  out('');
  printHubHosts(discovery, false);
}

function printHubRemove(payload, json) {
  if (json) {
    out(JSON.stringify(payload, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— Hub 删除技能');
  out('Hub: ' + payload.hubDir);
  out('技能: ' + payload.slug +
    (payload.hubPresent ? '（Hub 内存在）' : '（Hub 内不存在，执行清理）') +
    (payload.hubVersion ? ' v' + payload.hubVersion : ''));
  if (payload.dryRun) out('模式: dry-run（只读预演，不写入）');
  out('');
  for (const item of payload.targets || []) {
    const mark = item.action === 'unlink' ? '✔' : item.action === 'keep' ? '△' : '·';
    out('  ' + mark + ' ' + item.dir + '（' + item.label + '）');
    out('      ' + item.note);
  }
  if (!(payload.targets || []).length) out('  （没有需要处理的宿主目录）');
  out('');
  if (payload.dryRun) {
    out('预演汇总: 将清理链接 ' + payload.unlinkable + ' 条 / 保留 ' + payload.kept.length +
      ' 项' + (payload.hubPresent ? ' / Hub 目录将移入回收站（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）' : ''));
    return;
  }
  if (payload.verdict === 'failed') {
    for (const item of payload.failed || []) out('  ✘ ' + item.dir + '  ' + item.note);
    out('删除中止：链接或目录处理失败，Hub 真源未删除（已清理的部分可重跑收尾）。');
    return;
  }
  if (payload.verdict === 'not-found') {
    out('未找到该技能：Hub / 台账 / 链接均无痕迹（未做任何写入）。');
    return;
  }
  out('汇总: 清理链接 ' + (payload.unlinked || []).length + ' 条 / 保留 ' + payload.kept.length +
    ' 项' + (payload.trashedTo
      ? ' / Hub 目录已移入回收站（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）: ' + payload.trashedTo
      : ' / Hub 目录不存在（仅清理残留）'));
  out('审计已写入: ' + hubLib.AUDIT_FILE);
}

function hubScanEngine(hubDir, discovery, opts) {
  return hubScanLib.scanEngineForHub(hubDir, discovery, opts);
}

function hubScanSkill(hubDir, discovery, opts, skillDir) {
  return hubScanLib.hubScanSkill(hubDir, discovery, opts, skillDir);
}

function printAdoptScan(payload, json) {
  if (json) {
    out(JSON.stringify(payload, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— Hub 收编预演（只读）');
  out('Hub: ' + payload.hubDir);
  out('候选 ' + payload.summary.candidates + ' / 冲突 ' + payload.summary.conflicts +
    ' / 已在 Hub ' + payload.summary.alreadyInHub +
    (payload.summary.skipped ? ' / 跳过 ' + payload.summary.skipped : ''));
  out('');
  for (const item of payload.candidates) {
    const mark = item.conflict ? '△' : item.inHub ? '·' : '✔';
    out('  ' + mark + ' ' + item.slug.padEnd(26) + 'v' + String(item.version || '-').padEnd(10) +
      (item.sourceHost || '-') + '  ' + (item.source || ''));
    if (item.conflict) {
      out('      冲突副本: ' + item.variants.map((variant) =>
        (variant.host || '?') + ' v' + (variant.version || '?')).join(', '));
    }
    if (item.standardWarnings && item.standardWarnings.length) {
      out('      标准告警（不影响使用则不处理）: ' + item.standardWarnings.join('；'));
    }
  }
  if (payload.candidates.length === 0) out('  （没有发现可收编技能）');
  if ((payload.skipped || []).length) {
    out('');
    out('跳过 ' + payload.skipped.length + ' 个不可读候选（坏链 / 竞态删除；只读扫描不中断）:');
    for (const item of payload.skipped) {
      out('  ✘ ' + item.slug + '  ' + item.dir + '（' + item.reason + '）');
    }
  }
}

function printAdoptApply(payload, json) {
  if (json) {
    out(JSON.stringify(payload, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— Hub 收编');
  out('目标 Hub: ' + payload.hubDir);
  if (payload.scope) out('范围: ' + payload.scope);
  if (payload.skipScan) out('⚠ --skip-scan：已跳过元信装前扫描复核，请确认来源可信。');
  for (const item of payload.results) {
    const mark = item.status === 'imported' ? '✔' : item.status === 'skip' ? '·' : item.status === 'conflict' ? '△' : '✘';
    out('  ' + mark + ' ' + item.slug.padEnd(26) + item.note);
  }
  out('汇总: 收编 ' + payload.results.filter((item) => item.status === 'imported').length +
    ' / 跳过 ' + payload.results.filter((item) => item.status === 'skip').length +
    ' / 冲突 ' + payload.results.filter((item) => item.status === 'conflict').length +
    ' / 失败 ' + payload.results.filter((item) => !['imported', 'skip', 'conflict'].includes(item.status)).length);
}

function printHubDoctor(payload, json) {
  if (json) {
    out(JSON.stringify(payload, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— Hub doctor');
  out('Hub: ' + payload.hubDir);
  for (const check of payload.checks) {
    if (check.ok && check.severity !== 'info') continue;
    const mark = check.ok ? '✔' : check.severity === 'warning' ? '△' : '✘';
    out('  ' + mark + ' ' + check.message + (check.hint ? '（修复: ' + check.hint + '）' : ''));
  }
  out('汇总: 错误 ' + payload.summary.errors + ' / 警告 ' + payload.summary.warnings);
  if (!payload.ok) out('Hub doctor 未通过：请按上面的修复建议处理后重试。');
}

/** 0.29.1 U3：hub install / update 成功、失败各写一条 Hub 审计（skip / dry-run 不写；best-effort）。 */
function appendHubInstallAudit(hubDir, action, results) {
  for (const r of results || []) {
    if (!r || r.status === 'skip' || r.status === 'planned') continue;
    const entry = {
      event: action === 'install' ? 'install' : 'update',
      slug: r.skill && r.skill.slug ? r.skill.slug : null,
      version: r.version || null,
      source: 'npm',
      via: 'hub',
      ok: r.status === 'ok',
    };
    if (r.snapshot) entry.snapshot = r.snapshot;
    if (r.gate && r.gate.verdict) entry.verdict = r.gate.verdict;
    if (r.status !== 'ok') entry.error = r.note || 'unknown';
    try {
      hubLib.appendAudit(hubDir, entry);
    } catch (_) { /* best-effort：审计失败不阻断安装 / 更新主流程 */ }
  }
}

function runHub(opts) {
  const hubDir = hubLib.resolveHubDir(opts);
  const action = opts.hubAction || 'status';
  // 0.29.2 U4：config 不依赖宿主发现，提前派发（get/set/clear 无需扫描宿主目录）。
  if (action === 'config') {
    runHubConfig(opts);
    return;
  }
  const discovery = agentDiscoveryLib.discoverHosts({ homeDir: os.homedir(), env: process.env });

  if (action === 'hosts' || action === 'discover') {
    const sub = opts.skills[0] || null;
    if (sub === 'add') { runHostsAdd(opts); return; }
    if (sub === 'remove') { runHostsRemove(opts); return; }
    if (sub === 'list') { runHostsList(opts); return; }
    if (sub === 'rename') { runHostsRename(opts); return; }
    if (sub === 'mark') { runHostsMark(opts); return; }
    if (sub === 'exclude') { runHostsExclude(opts); return; }
    if (sub === 'include') { runHostsInclude(opts); return; }
    if (sub === 'set') { runHostsSet(opts); return; }
    if (sub) {
      die('未知 hub hosts 子命令: ' + sub, 2,
        '支持 add / remove / rename / list / mark / exclude / include / set；无子命令 = 只读发现。');
    }
    const view = opts.state
      ? { ...discovery, hosts: discovery.hosts.filter((host) => host.state === opts.state) }
      : discovery;
    printHubHosts(view, opts.json);
    return;
  }

  if (action === 'install' || action === 'update') {
    const quiet = Boolean(opts.dryRun && opts.json);
    if (!quiet) {
      out('Hub: ' + hubDir);
      out('范围: 全家清单 ' + MANIFEST.length + ' + 特殊家族 ' + hubLib.HUB_FAMILY_EXTRAS.length +
        '（特殊家族跟随各自 npm latest；非元技能不参与更新）');
      if (opts.dryRun) out('模式: dry-run（只读预演；无网络、无写入）');
    }
    const hubOpts = { ...opts, hubScope: true };
    const result = action === 'install' ? runInstall(hubOpts, hubDir) : runUpdate(hubOpts, hubDir);
    if (opts.dryRun) {
      // 0.29.0 D1：预览不更新 Hub 台账（无写入）。
      if (quiet) {
        out(JSON.stringify({
          action,
          hubDir,
          dryRun: true,
          scope: { manifest: MANIFEST.length, extras: hubLib.HUB_FAMILY_EXTRAS.length },
          skills: (result.results || []).map(function (r) {
            const isPlanned = r.status === 'planned';
            const isSkip = r.status === 'skip';
            return {
              slug: r.skill.slug,
              name: r.skill.name,
              pkg: r.skill.pkg,
              planned: isPlanned ? r.planned : (isSkip ? 'skip' : 'fail'),
              version: isPlanned ? r.version : (r.version || null),
              installedVersion: isPlanned ? (r.installedVersion || null) : (isSkip ? r.version : null),
              latestUnresolved: Boolean(r.latestUnresolved),
              spec: specOf(r.skill, opts.pin),
              note: r.note || null,
            };
          }),
          summary: result.summary || { planned: 0, skip: 0, failed: 0 },
        }, null, 2));
      } else {
        out('');
        out('（dry-run 未执行任何下载 / 写入；Hub 台账未更新）');
      }
      if (result.failed > 0) process.exitCode = result.exitCode || 1;
      return;
    }
    const synced = hubLib.syncHubState(hubDir, { manifest: MANIFEST });
    const count = Object.values(synced.state.skills).filter((item) => item.status === 'present').length;
    const external = Object.values(synced.state.skills)
      .filter((item) => item.origin === 'external' && item.status === 'present').length;
    out('');
    if (action === 'update' && external > 0) {
      out('非元技能 ' + external + ' 个不参与更新（来源无统一安装源，用户自行处理）。');
    }
    out('Hub 台账已更新: ' + count + ' 个技能；标准 ' + hubLib.STANDARD_ID);
    appendHubInstallAudit(hubDir, action, result.results);
    if (result.failed > 0) process.exitCode = result.exitCode || 1;
    return;
  }

  if (action === 'adopt') {
    if (opts.as) {
      die('hub adopt --as 暂未启用', 2, '先收编原 slug；改名 / 冲突改写放到后续里程碑，避免静默改技能身份。');
    }
    const scan = hubAdoptLib.scanCandidates({ hubDir, discovery, manifest: MANIFEST });
    if (!opts.apply) {
      printAdoptScan(scan, opts.json);
      return;
    }
    const payload = hubAdoptLib.applyCandidates({
      hubDir,
      candidates: scan.candidates,
      include: opts.include,
      force: opts.force,
      inPlace: opts.inPlace,
      skipScan: opts.skipScan,
      allowUnverified: opts.allowUnverified,
      manifest: MANIFEST,
      homeDir: os.homedir(),
      env: process.env,
      scan: (skillDir) => hubScanSkill(hubDir, discovery, opts, skillDir),
    });
    payload.scope = opts.include && opts.include.length
      ? '指定 ' + opts.include.length + ' 个技能（--include）'
      : '全部候选（本机已发现宿主）';
    payload.skipScan = Boolean(opts.skipScan);
    printAdoptApply(payload, opts.json);
    if (payload.results.some((item) => !['imported', 'skip', 'conflict'].includes(item.status))) process.exitCode = 1;
    return;
  }

  if (action === 'refresh') {
    if (!opts.from) die('hub refresh 缺少 --from <path>', 2, '示例：yotta-skills hub refresh my-skill --from <技能目录>。');
    if (opts.skills.length !== 1) die('hub refresh 需要一个且仅一个技能 slug', 2, '示例：yotta-skills hub refresh my-skill --from <技能目录>。');
    const result = hubAdoptLib.refreshFrom({
      hubDir,
      slug: opts.skills[0],
      from: opts.from,
      skipScan: opts.skipScan,
      allowUnverified: opts.allowUnverified,
      manifest: MANIFEST,
      homeDir: os.homedir(),
      env: process.env,
      scan: (skillDir) => hubScanSkill(hubDir, discovery, opts, skillDir, { slug: opts.skills[0] }),
    });
    if (opts.json) out(JSON.stringify(result, null, 2));
    else if (result.ok) {
      out('已刷新: ' + result.slug + '（来源 ' + result.source + '）');
      if (result.scanPolicy && result.scanPolicy.applied && result.scanPolicy.excluded > 0) {
        out('  ↳ scanPolicy 复核：豁免 ' + result.scanPolicy.excluded + ' 条已审查发现 → ' + result.verdict);
      }
    }
    else {
      out('刷新失败: ' + result.error);
      if (result.blocked) {
        for (const line of scanFindingDiffLines(opts.skills[0], result.scan)) out('  ' + line);
        out('  复核确认后可显式放行：yotta-skills hub refresh ' + opts.skills[0] +
          ' --from "' + opts.from + '" --allow-unverified');
      }
    }
    if (!result.ok) process.exitCode = 1;
    return;
  }

  if (action === 'cleanup-backups') {
    // 0.29.5 S3：历史备份 / 暂存残留清理（默认预览；--yes 执行；入回收站 7 天）。
    let dirs;
    if (opts.dir || opts.agent) {
      dirs = hubTargetDirs(opts, discovery).map((item) => ({ dir: item.dir, label: item.label }));
    } else {
      dirs = [{ dir: hubDir, label: 'Hub' }].concat(
        hubTargetDirs({ all: true, hubAction: 'cleanup-backups', includeDiscovered: opts.includeDiscovered }, discovery)
          .filter((item) => fs.existsSync(item.dir))
          .map((item) => ({ dir: item.dir, label: item.label })),
      );
    }
    const seenDirs = new Set();
    dirs = dirs.filter((item) => {
      const key = normalizeTargetKey(item.dir);
      if (seenDirs.has(key)) return false;
      seenDirs.add(key);
      return true;
    });
    const residues = hubLib.findBackupResidues({ dirs });
    if (!opts.yes) {
      if (opts.json) {
        out(JSON.stringify({
          action: 'cleanup-backups',
          preview: true,
          dirs: dirs.map((item) => item.dir),
          count: residues.length,
          residues,
        }, null, 2));
        return;
      }
      out('yotta-skills（元阁）v' + VERSION + ' —— 历史备份 / 暂存残留清理（预览）');
      out('范围: ' + dirs.length + ' 个目录（Hub + 已核实宿主）');
      if (residues.length === 0) {
        out('未发现 .yottaskills-backup-* / .yottaskills-import-* / .yottaskills-rollback-* / .yottaskills-staging 残留。');
      } else {
        for (const item of residues) out('  △ ' + item.path);
        out('共 ' + residues.length + ' 项；确认后加 --yes 执行（移入回收站，保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）。');
      }
      out('（预览未执行任何变更）');
      return;
    }
    const result = hubLib.cleanupBackupResidues({ dirs, hubDir, env: process.env, residues });
    if (opts.json) {
      out(JSON.stringify({ action: 'cleanup-backups', preview: false, ...result }, null, 2));
    } else {
      out('yotta-skills（元阁）v' + VERSION + ' —— 历史备份 / 暂存残留清理');
      out('✔ 已清理 ' + result.moved.length + ' / ' + result.found + ' 项 → 回收站: ' + result.trashRoot +
        '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
      for (const item of result.failed) out('  ✘ ' + item.path + '：' + item.error);
    }
    if (!result.ok) process.exitCode = 1;
    return;
  }

  if (action === 'link') {
    const targets = hubTargetDirs(opts, discovery);
    if (opts.all && !opts.json) out(hubScopeLine(opts, discovery));
    let failed = 0;
    const targetPayloads = [];
    for (const target of targets) {
      if (path.resolve(target.dir) === path.resolve(hubDir)) {
        targetPayloads.push({ dir: target.dir, label: target.label, skipped: true, results: [] });
        if (!opts.json) out('跳过 Hub 自身: ' + target.dir);
        continue;
      }
      const result = hubLib.linkSkills({
        hubDir,
        targetDir: target.dir,
        agentId: target.agentId,
        label: target.label,
        slugs: opts.skills,
        force: opts.force,
        dryRun: opts.dryRun,
        manifest: MANIFEST,
      });
      targetPayloads.push({ dir: target.dir, label: target.label, results: result.results });
      if (!opts.json) {
        out('');
        out('目标: ' + target.dir + '（' + target.label + '）');
        for (const item of result.results) {
          const mark = item.status === 'linked' ? '✔'
            : item.status === 'error' ? '✘'
              : item.status === 'missing' ? '·' : '△';
          out('  ' + mark + ' ' + item.slug.padEnd(26) + item.note);
          if (item.status === 'error') failed++;
        }
        const movedCount = result.results.reduce((n, item) => n + ((item.moved && item.moved.length) || 0), 0);
        if (movedCount > 0) {
          out('  收敛: 移动 ' + movedCount + ' 份旧副本 -> ' + (result.trashRoot || '') +
            '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
        }
        const replacedCount = result.results.filter((item) => item.backup).length;
        if (replacedCount > 0) {
          out('  替换: ' + replacedCount + ' 份真目录旧副本已移入回收站 -> ' + (result.trashRoot || '') +
            '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
        }
      } else {
        failed += result.results.filter((item) => item.status === 'error').length;
      }
    }
    if (opts.json) out(JSON.stringify({ hubDir, targets: targetPayloads, failed }, null, 2));
    if (failed > 0) process.exitCode = 1;
    return;
  }

  if (action === 'unlink') {
    const targets = hubTargetDirs(opts, discovery);
    if (opts.all && !opts.json) out(hubScopeLine(opts, discovery));
    const explicitTarget = Boolean(opts.dir || opts.agent);
    let failed = 0;
    const targetPayloads = [];
    for (const target of targets) {
      const result = hubLib.unlinkSkills({
        hubDir,
        targetDir: target.dir,
        slugs: opts.skills,
        dryRun: opts.dryRun,
      });
      targetPayloads.push({ dir: target.dir, label: target.label, results: result.results,
        discovery: result.discovery || null });
      if (!opts.json) {
        out('');
        out('目标: ' + target.dir + '（' + target.label + '）');
        for (const item of result.results) {
          const mark = item.status === 'unlinked' ? '✔' : item.status === 'refused' ? '△' : item.status === 'error' ? '✘' : '·';
          out('  ' + mark + ' ' + item.slug.padEnd(26) + item.note);
          if (item.status === 'error') failed++;
        }
        // 0.30.0 OPT-02：预演 / 执行汇总（对齐 hub remove）。
        const would = result.results.filter((item) => item.status === 'would-unlink').length;
        const unlinked = result.results.filter((item) => item.status === 'unlinked').length;
        const kept = result.results.filter((item) => item.status === 'refused' || item.status === 'missing').length;
        const errors = result.results.filter((item) => item.status === 'error').length;
        if (result.results.length > 0 || explicitTarget) {
          if (opts.dryRun) {
            out('  预演汇总: 将清理链接 ' + would + ' 条 / 保留 ' + kept + ' 项' +
              (errors ? ' / 失败 ' + errors : ''));
          } else {
            out('  汇总: 清理链接 ' + unlinked + ' 条 / 保留 ' + kept + ' 项' +
              (errors ? ' / 失败 ' + errors : ''));
          }
        }
        // 0.30.0 UX-02 / OPT-01：空结果必须解释，不再静默。
        const disc = result.discovery;
        if (result.results.length === 0 && explicitTarget) {
          if (disc && disc.dirReadable === false) {
            out('  目录不存在或不可读：' + target.dir);
          } else {
            out('  未发现指向当前 Hub 的链接（已扫描目录与链接台账）；无需清理。');
          }
          out('  当前 Hub: ' + hubDir + '（如与预期不符，用 yotta-skills hub config get 自查位置来源）');
        }
        if (disc && disc.otherLinks > 0) {
          out('  ⚠ 该目录另有 ' + disc.otherLinks + ' 条指向其它位置的链接（未动，fail-closed）：');
          for (const other of disc.otherTargets) out('    → ' + other);
          if (disc.otherTargets.length < disc.otherLinks) out('    （仅列前 5 个目标）');
          out('    若这些应指向当前 Hub：先 yotta-skills hub config get 核对位置，再 yotta-skills hub link --dir "' +
            target.dir + '" --force 重建。');
        }
      } else {
        failed += result.results.filter((item) => item.status === 'error').length;
      }
    }
    if (opts.json) out(JSON.stringify({ hubDir, targets: targetPayloads, failed }, null, 2));
    if (failed > 0) process.exitCode = 1;
    return;
  }

  if (action === 'remove') {
    if (opts.skills.length !== 1) {
      die('hub remove 需要一个且仅一个技能 slug', 2,
        '示例：yotta-skills hub remove my-skill；只读预演加 --dry-run。');
    }
    const slug = opts.skills[0];
    if (!/^[a-z0-9][a-z0-9-]*$/.test(slug)) {
      die('hub remove slug 格式非法: ' + slug, 2, '只允许小写字母、数字和连字符，例如 my-skill。');
    }
    if (opts.dir || opts.agent) {
      let hubEntryPresent = false;
      try {
        const stat = fs.lstatSync(path.join(hubDir, slug));
        hubEntryPresent = stat.isDirectory() || stat.isSymbolicLink();
      } catch (_) { hubEntryPresent = false; }
      if (hubEntryPresent) {
        die('hub remove 的 --agent / --dir 只用于清理 Hub 目标已缺失的死链', 2,
          '删除整个 Hub 技能请用全范围（不加 --agent/--dir）；只解除指定宿主的链接请用 hub unlink <slug> --agent <id> 或 --dir <目录>。');
      }
    }
    const targets = hubRemoveTargets(opts, discovery, slug, hubDir);
    if (!opts.json) {
      out('范围: ' + targets.length + ' 个宿主目录' +
        (opts.dir || opts.agent ? '（显式指定）' : '（已核实宿主 ∪ 本技能链接台账）'));
    }
    const payload = hubLib.removeSkills({
      hubDir,
      slug,
      targets,
      dryRun: opts.dryRun,
      manifest: MANIFEST,
    });
    printHubRemove(payload, opts.json);
    if (payload.exitCode) process.exitCode = payload.exitCode;
    return;
  }

  if (action === 'status') {
    const payload = hubLib.status({ hubDir, manifest: MANIFEST });
    printHubStatus(payload, discovery, opts.json);
    return;
  }

  if (action === 'doctor') {
    const payload = hubLib.doctor({
      hubDir,
      manifest: MANIFEST,
      homeDir: os.homedir(),
      env: process.env,
      discovery,
      linkScopeDirs: hubTargetDirs({ all: true }, discovery).map((target) => target.dir),
    });
    printHubDoctor(payload, opts.json);
    if (!payload.ok) process.exitCode = 1;
    return;
  }

  die('未知 hub 子命令: ' + action, 2,
    '支持 install / update / adopt / refresh / link / unlink / remove / status / hosts / config / doctor / cleanup-backups。');
}

// ── hub hosts add / remove / list / mark（0.29.0 F2/F3 注册表与手动标记） ─────
function hostRegistryOptions(opts) {
  return { homeDir: os.homedir(), env: process.env, hub: opts.hub };
}

function auditHostEvent(opts, entry) {
  const hubDir = hubLib.resolveHubDir(opts);
  if (!fs.existsSync(hubDir)) return;
  try {
    hubLib.appendAudit(hubDir, entry);
  } catch (_) { /* 审计失败不阻断注册 / 清理主流程 */ }
}

function auditHubConfigEvent(hubDir, entry) {
  if (!hubDir || !fs.existsSync(hubDir)) return;
  try {
    hubLib.appendAudit(hubDir, entry);
  } catch (_) { /* 审计失败不阻断配置主流程 */ }
}

/** 旧 Hub / 目标目录的技能计数（只读；用于「未迁移」提示与切换记录）。 */
function countHubSkills(dir) {
  try {
    return hubLib.scanHubSkills(dir).length;
  } catch (_) {
    return 0;
  }
}

/** 迁移 / 回滚的重链范围（与 hub link --all 同一口径，只取存在的目录）。 */
function hubMigrationTargets() {
  const discovery = agentDiscoveryLib.discoverHosts({ homeDir: os.homedir(), env: process.env });
  return hubTargetDirs({ all: true, hubAction: 'config' }, discovery)
    .filter((item) => fs.existsSync(item.dir));
}

/** 「最近一次迁移」文本块（CLI 与输出口径；面板走 JSON 同源字段）。 */
function migrationLines(migration) {
  const kindLabel = migration.kind === 'rollback' ? '回滚' : '迁移';
  const lines = [];
  lines.push('最近一次' + kindLabel + ':');
  if (migration.at) lines.push('  时间: ' + migration.at);
  lines.push('  ' + migration.from + ' → ' + migration.to);
  lines.push('  技能: ' + migration.verifiedSkills + ' 个（复制校验通过）；重链: ' +
    migration.relinkDirs + ' 个宿主目录');
  if (migration.trashedTo) {
    lines.push('  回收站: ' + migration.trashedTo + '（保留 ' + hubLib.TRASH_RETENTION_DAYS +
      ' 天，剩余 ' + hubMigrateLib.trashDaysLeft(migration.at) + ' 天）');
  }
  if (migration.incomplete > 0) {
    lines.push('  ⚠ 重链未全部完成（' + migration.incomplete + ' 项）；旧 Hub 保留在 ' +
      (migration.oldHubKept || migration.from) + '，可重跑：yotta-skills hub link --all --force');
  }
  if (migration.trashError) lines.push('  ⚠ 旧 Hub 移入回收站失败（已保留原位）: ' + migration.trashError);
  lines.push('  回滚: yotta-skills hub config rollback（预览）/ --yes 执行（位置回退，用当前内容）');
  return lines;
}

/** 0.30.0 OPT-04：view 面板运行标记（<skillsRoot>/view-server.json；进程不在 = 残留忽略）。 */
function viewServerMarkerPath(configOpts) {
  return path.join(skillsConfigLib.resolveSkillsRoot(configOpts), 'view-server.json');
}

function readRunningViewServer(configOpts) {
  try {
    const data = JSON.parse(fs.readFileSync(viewServerMarkerPath(configOpts), 'utf8'));
    if (!data || !data.pid) return null;
    let alive = true;
    try {
      process.kill(data.pid, 0);
    } catch (error) {
      alive = !(error && error.code === 'ESRCH');
    }
    return alive ? data : null;
  } catch (_) {
    return null;
  }
}

/** 0.29.2 U4：hub config get / set / clear；0.29.5 增 rollback（面板同源内核）。 */
function runHubConfig(opts) {
  const sub = opts.skills[0] || 'get';
  const configOpts = { homeDir: os.homedir(), env: process.env };

  if (sub === 'get') {
    const resolved = hubLib.resolveHub({ ...configOpts, hub: opts.hub });
    const config = skillsConfigLib.readConfig(configOpts);
    const payload = {
      action: 'config.get',
      hub: resolved.dir,
      source: resolved.source,
      configured: resolved.configured,
      configFile: resolved.configFile,
      defaultDir: resolved.defaultDir,
      lastMigration: config.lastMigration,
      lastSwitch: config.lastSwitch,
    };
    if (config.lastMigration) payload.migrationDaysLeft = hubMigrateLib.trashDaysLeft(config.lastMigration.at);
    // 0.30.0 OPT-04：运行中 view 面板的生效位置与当前解析不一致 → 提示重启。
    const runningView = readRunningViewServer(configOpts);
    const viewRestartRequired = Boolean(runningView && runningView.hubDir &&
      normalizeTargetKey(runningView.hubDir) !== normalizeTargetKey(resolved.dir));
    payload.viewServer = runningView
      ? { pid: runningView.pid, port: runningView.port, hubDir: runningView.hubDir,
          startedAt: runningView.startedAt || null }
      : null;
    payload.restartRequired = viewRestartRequired;
    if (opts.json) { out(JSON.stringify(payload, null, 2)); return; }
    out('yotta-skills（元阁）v' + VERSION + ' —— Hub 配置');
    out('生效 Hub: ' + payload.hub + '（来源: ' + skillsConfigLib.sourceLabel(payload.source) + '）');
    out('配置覆盖: ' + (payload.configured || '无'));
    out('配置文件: ' + payload.configFile);
    out('默认位置: ' + payload.defaultDir);
    if (config.lastMigration) {
      out('');
      for (const line of migrationLines(config.lastMigration)) out(line);
    } else {
      out('最近一次迁移: 无（hub config set --hub <path> --move 迁移后记录，可一键回滚）');
    }
    if (config.lastSwitch) {
      const oldCount = countHubSkills(config.lastSwitch.from);
      if (oldCount > 0) {
        out('');
        out('未迁移提示: 旧 Hub ' + config.lastSwitch.from + ' 还有 ' + oldCount +
          ' 个技能未迁移（当前位置 ' + resolved.dir + '）');
        out('  一键迁移: yotta-skills hub config set --hub "' + resolved.dir + '" --move');
      }
    }
    if (viewRestartRequired) {
      out('');
      out('⚠ 运行中的 view 面板（PID ' + runningView.pid + '，端口 ' + runningView.port +
        '）生效位置仍是: ' + runningView.hubDir);
      out('  重启面板后才会切到: ' + resolved.dir + '（面板: http://127.0.0.1:' + runningView.port + '/）');
    }
    return;
  }

  if (sub === 'set') {
    if (!opts.hub) {
      die('hub config set 需要 --hub <path>', 2,
        '示例：yotta-skills hub config set --hub "D:\\my-hub"。');
    }
    const current = hubLib.resolveHub(configOpts);
    const guard = skillsConfigLib.validateHubPath(opts.hub, configOpts);
    if (!guard.ok) die(guard.error, 2, '校验路径后重试；迁移（--move）仅在旧 Hub 有内容时需要。');
    const target = guard.dir;
    if (opts.move && path.resolve(target) === path.resolve(current.dir)) {
      die('新旧 Hub 路径相同，无需 --move', 2, '直接设置其它位置：hub config set --hub <path>。');
    }

    let moveReport = null;
    let migrationResult = null;
    if (opts.move) {
      migrationResult = hubMigrateLib.runHubMigration({
        from: current.dir,
        to: target,
        targets: hubMigrationTargets(),
        manifest: MANIFEST,
        homeDir: os.homedir(),
        env: process.env,
        configOpts,
        via: 'cli',
        cleanResidue: Boolean(opts.cleanResidue),
      });
      if (!migrationResult.ok && migrationResult.phase !== 'relink') {
        const hint = migrationResult.code === 'target-residue'
          ? '目标目录只含空 Hub 台账残留；确认后可加 --clean-residue 清理后迁移。'
          : '迁移 fail-closed：配置未切换、旧 Hub 未动；可改用不带 --move 的 set。';
        die(migrationResult.error, migrationResult.phase === 'config' ? 1 : 2, hint);
      }
      moveReport = migrationResult.report;
    } else {
      const setResult = skillsConfigLib.setHub(configOpts, { hub: target });
      if (!setResult.ok) die(setResult.error, 2, '检查路径后重试。');
      const oldSkills = countHubSkills(current.dir);
      if (oldSkills > 0) {
        skillsConfigLib.recordLastSwitch(configOpts, {
          from: current.dir,
          to: target,
          at: new Date().toISOString(),
          skills: oldSkills,
          via: 'cli',
        });
      }
      moveReport = {
        moved: false,
        reason: '未指定 --move：仅切换指针（旧 Hub 内容保留）。填充新 Hub：hub install；重链：hub link --all --force',
        trashedTo: null,
        relink: [],
        oldSkills,
      };
    }

    const resolved = hubLib.resolveHub(configOpts);
    const payload = {
      action: 'config.set',
      hub: resolved.dir,
      source: resolved.source,
      previous: current.dir,
      previousSource: current.source,
      configFile: resolved.configFile,
      move: moveReport,
    };
    auditHubConfigEvent(fs.existsSync(target) ? target : current.dir, {
      event: 'config.set',
      hub: target,
      previousHub: current.dir,
      source: resolved.source,
      moved: Boolean(moveReport && moveReport.moved),
      via: 'cli',
    });
    if (opts.json) {
      out(JSON.stringify(payload, null, 2));
    } else {
      out('yotta-skills（元阁）v' + VERSION + ' —— Hub 配置');
      out('✔ 已设置 Hub: ' + payload.hub + '（来源: ' + skillsConfigLib.sourceLabel(payload.source) + '）');
      out('  配置文件: ' + payload.configFile);
      if (moveReport && moveReport.moved) {
        out('  迁移: 复制校验 ' + moveReport.verifiedSkills + ' 个技能；重链 ' +
          moveReport.relinkDirs + ' 个宿主目录');
        if (moveReport.incomplete > 0) {
          out('  ⚠ 重链未全部完成（' + moveReport.incomplete + ' 项）；旧 Hub 保留在 ' + moveReport.oldHubKept +
            '，可重跑：yotta-skills hub link --all --force');
        } else if (moveReport.trashedTo) {
          out('  旧 Hub 已移入回收站: ' + moveReport.trashedTo + '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
        } else if (moveReport.trashError) {
          out('  ⚠ 旧 Hub 移入回收站失败（已保留原位）: ' + moveReport.trashError);
        }
      } else if (moveReport) {
        out('  ' + moveReport.reason);
        if (moveReport.oldSkills > 0) {
          out('  ⚠ 旧 Hub 还有 ' + moveReport.oldSkills + ' 个技能未迁移；迁移用：yotta-skills hub config set --hub "' +
            resolved.dir + '" --move');
        }
      }
      out('  提示: 已在运行的 view 面板需重启后生效。');
    }
    if (migrationResult && !migrationResult.ok) process.exitCode = 1;
    return;
  }

  if (sub === 'rollback') {
    const preview = hubMigrateLib.previewRollback({ configOpts, env: process.env });
    if (!preview.ok && preview.code === 'no-migration') {
      die(preview.error, 2, '先完成一次迁移：yotta-skills hub config set --hub <path> --move。');
    }
    if (!opts.yes) {
      const payload = { action: 'config.rollback', preview: true, ...preview };
      if (opts.json) out(JSON.stringify(payload, null, 2));
      else {
        out('yotta-skills（元阁）v' + VERSION + ' —— Hub 迁移回滚（预览）');
        out('当前 Hub: ' + preview.current);
        out('回滚目标: ' + preview.target + (preview.targetState.exists ? '（' + (preview.targetState.empty ? '空目录' : preview.targetState.residueOnly ? '仅空台账残留' : '非空') + '）' : '（不存在，将新建）'));
        out('语义: 位置回退（用当前内容复制回原位置；不恢复旧快照）');
        if (preview.lastMigration.trashedTo) {
          out('上次迁移回收站: ' + preview.lastMigration.trashedTo + '（剩余 ' + preview.daysLeft + ' 天）');
        }
        if (!preview.ok) {
          for (const reason of preview.blocked) out('⚠ ' + reason);
          out('（预览未执行任何变更；处理阻断项后重试）');
          process.exitCode = 2;
        } else {
          out('执行: yotta-skills hub config rollback --yes');
        }
      }
      return;
    }
    if (!preview.ok) {
      die('回滚被阻断：' + preview.blocked.join('；'), 2,
        '回滚 fail-closed（不合并）；目标非空时先清理目标，或继续使用当前位置。');
    }
    const migration = hubMigrateLib.runHubMigration({
      from: preview.current,
      to: preview.target,
      kind: 'rollback',
      targets: hubMigrationTargets(),
      manifest: MANIFEST,
      homeDir: os.homedir(),
      env: process.env,
      configOpts,
      via: 'cli',
      cleanResidue: Boolean(opts.cleanResidue),
    });
    if (!migration.ok && migration.phase !== 'relink') {
      const hint = migration.code === 'target-residue'
        ? '目标目录只含空 Hub 台账残留；确认后可加 --clean-residue 清理后回滚。'
        : '回滚 fail-closed：配置未切换、当前 Hub 未动。';
      die(migration.error, migration.phase === 'config' ? 1 : 2, hint);
    }
    const report = migration.report;
    const payload = { action: 'config.rollback', preview: false, ...report };
    if (opts.json) out(JSON.stringify(payload, null, 2));
    else {
      out('yotta-skills（元阁）v' + VERSION + ' —— Hub 迁移回滚');
      out('✔ 已回滚位置: ' + report.from + ' → ' + report.to);
      out('  技能: 复制校验 ' + report.verifiedSkills + ' 个；重链 ' + report.relinkDirs + ' 个宿主目录');
      if (report.incomplete > 0) {
        out('  ⚠ 重链未全部完成（' + report.incomplete + ' 项）；原 Hub 保留在 ' + report.oldHubKept +
          '，可重跑：yotta-skills hub link --all --force');
      } else if (report.trashedTo) {
        out('  原 Hub 已移入回收站: ' + report.trashedTo + '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
      }
      out('  提示: 已在运行的 view 面板需重启后生效。');
    }
    if (!migration.ok) process.exitCode = 1;
    return;
  }

  if (sub === 'clear') {
    const current = hubLib.resolveHub(configOpts);
    // 0.30.0 UX-04：清除覆盖前做影响面强提示 —— 当前配置 Hub 有技能时
    // 默认阻断（fail-closed），确认已知影响后加 --yes 才执行。
    const currentSkills = current.source === 'config' ? countHubSkills(current.dir) : 0;
    if (currentSkills > 0 && !opts.yes) {
      die('hub config clear 被阻断：当前配置 Hub 还有 ' + currentSkills + ' 个技能', 2,
        '影响面：清除后生效位置回落到默认 ' + skillsConfigLib.defaultHubDir(configOpts) +
        '（默认位置可能是空目录）；Hub 真源与宿主链接不会移动，但元阁命令将按新位置工作（表现为台账 / 链接全部空转）。\n' +
        '替代路径：迁到默认位置 = yotta-skills hub config set --hub "' +
        skillsConfigLib.defaultHubDir(configOpts) + '" --move；迁到其它位置 = yotta-skills hub config set --hub "<新路径>" --move。\n' +
        '确认已知影响后执行：yotta-skills hub config clear --yes');
    }
    const result = skillsConfigLib.clearHub(configOpts);
    if (!result.ok) {
      die(result.error + '（当前来源: ' + skillsConfigLib.sourceLabel(current.source) + '）', 2,
        '当前生效位置: ' + current.dir + '；如需改位置用 hub config set --hub <path>。');
    }
    const resolved = hubLib.resolveHub(configOpts);
    auditHubConfigEvent(fs.existsSync(current.dir) ? current.dir : resolved.dir, {
      event: 'config.clear',
      removed: result.removed,
      hub: resolved.dir,
      via: 'cli',
    });
    const payload = {
      action: 'config.clear',
      removed: result.removed,
      hub: resolved.dir,
      source: resolved.source,
      configFile: result.configFile,
      previousHub: current.dir,
      previousSkills: currentSkills,
      defaultDir: skillsConfigLib.defaultHubDir(configOpts),
    };
    if (opts.json) { out(JSON.stringify(payload, null, 2)); return; }
    out('yotta-skills（元阁）v' + VERSION + ' —— Hub 配置');
    out('✔ 已清除配置覆盖: ' + payload.removed);
    out('  生效 Hub: ' + payload.hub + '（来源: ' + skillsConfigLib.sourceLabel(payload.source) + '）');
    out('  默认位置: ' + payload.defaultDir + '（回落目标）');
    if (payload.previousSkills > 0) {
      out('  ⚠ 原 Hub 仍有 ' + payload.previousSkills + ' 个技能未迁移：' + payload.previousHub);
    }
    out('  提示: 已在运行的 view 面板需重启后生效。');
    return;
  }

  die('未知 hub config 子命令: ' + sub, 2,
    '支持 get / set / clear / rollback；示例：yotta-skills hub config set --hub "D:\\my-hub" --move。');
}

/** hub hosts 子命令的原始位置参数（保留路径大小写；slug 版本已小写化）。 */
function hostsSubcommandArg(opts, index) {
  if (opts.rawRest && opts.rawRest.length > index) return opts.rawRest[index];
  return opts.skills[index] || null;
}

/** 0.30.0 UX-09：移除注册 / 不接管时提示目录里剩余的 Hub 链接。 */
function printRemainingHubLinks(dir, opts) {
  if (!dir) return;
  let stat = null;
  try { stat = fs.statSync(dir); } catch (_) { return; }
  if (!stat.isDirectory()) return;
  const hubDir = hubLib.resolveHubDir({ hub: opts && opts.hub, homeDir: os.homedir(), env: process.env });
  const scan = hubLib.scanDirForHubLinks(dir, hubDir);
  if (scan.hubSlugs.length > 0) {
    out('  ⚠ 该目录还有 ' + scan.hubSlugs.length + ' 条指向 Hub 的链接（可用: yotta-skills hub unlink --dir "' +
      dir + '" 清理）');
  }
  if (scan.otherLinks.length > 0) {
    out('  ⚠ 另有 ' + scan.otherLinks.length + ' 条指向其它位置的链接（fail-closed 不动；如与预期不符用 hub config get 自查）');
  }
}

function runHostsAdd(opts) {
  const dir = hostsSubcommandArg(opts, 2);
  if (!dir) {
    die('hub hosts add 需要目录', 2,
      '示例：yotta-skills hub hosts add "<技能目录>" --label "我的宿主"。');
  }
  const registryOpts = hostRegistryOptions(opts);
  const result = hostsRegistryLib.addHost(registryOpts, { dir, label: opts.label, agentId: opts.id });
  if (!result.ok) {
    die(result.error, 2, '确认目录存在且不是 Hub / 锁桥接目录后重试。');
  }
  auditHostEvent(opts, {
    event: 'hosts.add',
    dir: result.entry.dir,
    label: result.entry.label,
    agentId: result.entry.agentId,
  });
  if (opts.json) {
    out(JSON.stringify({
      action: 'hosts.add',
      entry: result.entry,
      registryPath: hostsRegistryLib.hostsRegistryPath(registryOpts),
    }, null, 2));
    return;
  }
  out('✔ 已注册自定义宿主: ' + result.entry.label);
  out('  目录: ' + result.entry.dir);
  out('  注册表: ' + hostsRegistryLib.hostsRegistryPath(registryOpts));
  out('  已纳入: hub link --all / hub adopt --scan / 面板宿主矩阵（不创建目录、不改宿主配置）。');
}

function runHostsList(opts) {
  const registryOpts = hostRegistryOptions(opts);
  const registry = hostsRegistryLib.readHostsRegistry(registryOpts);
  if (opts.json) {
    out(JSON.stringify({
      action: 'hosts.list',
      registryPath: hostsRegistryLib.hostsRegistryPath(registryOpts),
      hosts: registry.hosts,
      excluded: registry.excluded,
      overrides: registry.overrides,
    }, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— 自定义宿主注册表（仅手动 add 的目录）');
  out('注册表: ' + hostsRegistryLib.hostsRegistryPath(registryOpts));
  out('（本表只列手动注册的目录；全部宿主 / 技能目录请用: yotta-skills hub hosts）');
  if (registry.hosts.length === 0 && (registry.excluded || []).length === 0 && (registry.overrides || []).length === 0) {
    out('（空；用 yotta-skills hub hosts add <目录> 注册）');
    return;
  }
  for (const item of registry.hosts) {
    out('  ' + String(item.label).padEnd(28) + item.dir +
      (item.manualState ? '  [手动: ' + item.manualState + ']' : ''));
  }
  if ((registry.excluded || []).length > 0) {
    out('');
    out('不接管名单 ' + registry.excluded.length + ' 个（发现 / 显示 / 链接全部跳过）：');
    for (const item of registry.excluded) {
      out('  ⊘ ' + String(item.label || item.value).padEnd(28) + item.value);
    }
  }
  if ((registry.overrides || []).length > 0) {
    out('');
    out('目录覆盖 ' + registry.overrides.length + ' 个：');
    for (const item of registry.overrides) {
      out('  ↳ ' + String(item.label || item.agentId).padEnd(28) + item.dir +
        '（原: ' + (item.previousDirs || []).join(' / ') + '）');
    }
  }
}

/** 0.30.0 UX-08：一步改名（只改显示名，不动目录 / 手动状态 / 覆盖）。 */
function runHostsRename(opts) {
  const target = hostsSubcommandArg(opts, 2);
  if (!target && !opts.id) {
    die('hub hosts rename 需要 <目录> 或 --id <agentId>', 2,
      '示例：yotta-skills hub hosts rename "<技能目录>" --label "新名称"（只改显示名，不动目录与状态）。');
  }
  if (!opts.label) {
    die('hub hosts rename 需要 --label <新名称>', 2,
      '示例：yotta-skills hub hosts rename "<技能目录>" --label "新名称"。');
  }
  const registryOpts = hostRegistryOptions(opts);
  const result = hostsRegistryLib.renameHost(registryOpts, { dir: target, id: opts.id, label: opts.label });
  if (!result.ok) {
    die(result.error, 2, result.hint || '用 yotta-skills hub hosts list 查看已注册项。');
  }
  auditHostEvent(opts, {
    event: 'hosts.rename',
    dir: result.entry.dir,
    from: result.previous,
    to: result.entry.label,
  });
  if (opts.json) {
    out(JSON.stringify({ action: 'hosts.rename', entry: result.entry, previous: result.previous }, null, 2));
    return;
  }
  out('✔ 已改名: ' + result.previous + ' -> ' + result.entry.label);
  out('  目录: ' + result.entry.dir + '（未动；手动状态 / 覆盖保持）');
}

function runHostsRemove(opts) {
  const dir = hostsSubcommandArg(opts, 2);
  if (opts.purge) {
    runHostsPurge(opts, dir);
    return;
  }
  if (!dir && !opts.id) {
    die('hub hosts remove 需要 <目录> 或 --id <agentId>', 2,
      '示例：yotta-skills hub hosts remove "<技能目录>"；残留清理加 --purge（默认预览）。');
  }
  const registryOpts = hostRegistryOptions(opts);
  const result = hostsRegistryLib.removeHost(registryOpts, { dir, id: opts.id });
  if (!result.ok) {
    die(result.error, 2, '示例：yotta-skills hub hosts list 查看已注册项。');
  }
  auditHostEvent(opts, {
    event: 'hosts.remove',
    dir: result.removed.dir,
    label: result.removed.label,
    agentId: result.removed.agentId,
  });
  if (opts.json) {
    out(JSON.stringify({ action: 'hosts.remove', removed: result.removed }, null, 2));
    return;
  }
  out('✔ 已移除注册（目录未删除）: ' + result.removed.dir);
  printRemainingHubLinks(result.removed.dir, opts);
}

function runHostsMark(opts) {
  const dir = hostsSubcommandArg(opts, 2);
  if (!dir) {
    die('hub hosts mark 需要目录', 2,
      '示例：yotta-skills hub hosts mark "<技能目录>" --state orphan。');
  }
  const state = opts.state;
  if (!state) {
    die('hub hosts mark 需要 --state <available|orphan|ignored>', 2,
      '可用（available）/ 残留（orphan）/ 隐藏标记（ignored，只影响显示、不拦截行为）。');
  }
  const registryOpts = hostRegistryOptions(opts);
  const result = hostsRegistryLib.markHost(registryOpts, { dir, state });
  if (!result.ok) {
    die(result.error, 2, '手动标记与注册表共用存储（hosts.json）。');
  }
  auditHostEvent(opts, { event: 'hosts.mark', dir: result.entry.dir, state });
  if (opts.json) {
    out(JSON.stringify({ action: 'hosts.mark', entry: result.entry }, null, 2));
    return;
  }
  out('✔ 已手动标记: ' + result.entry.dir + '  ->  ' + state);
}

/** 0.29.1 U2：不接管开关（发现 / 显示 / 链接三层全部跳过，--include-discovered 也不纳入）。 */
function runHostsExclude(opts) {
  const target = hostsSubcommandArg(opts, 2);
  if (!target) {
    die('hub hosts exclude 需要 <agentId|目录>', 2,
      '示例：yotta-skills hub hosts exclude box；或 hub hosts exclude "D:\\my-agent\\skills"。');
  }
  const registryOpts = hostRegistryOptions(opts);
  const result = hostsRegistryLib.excludeHost(registryOpts, { target });
  if (!result.ok) {
    die(result.error, 2, '目标可以是已收录 agentId，或技能目录（非 Hub / 非锁桥接 / 非 YottaCode）。');
  }
  auditHostEvent(opts, {
    event: 'hosts.exclude',
    kind: result.entry.kind,
    value: result.entry.value,
    label: result.entry.label,
  });
  if (opts.json) {
    out(JSON.stringify({ action: 'hosts.exclude', entry: result.entry, already: Boolean(result.already) }, null, 2));
    return;
  }
  out((result.already ? '· 已在' : '✔ 已加入') + '「不接管」名单: ' + result.entry.label + '（' + result.entry.value + '）');
  out('  发现 / 显示 / 链接三层全部跳过（--include-discovered 也不纳入）。');
  if (result.entry.kind === 'dir') printRemainingHubLinks(result.entry.value, opts);
  out('  恢复接管：yotta-skills hub hosts include ' +
    (result.entry.kind === 'dir' ? '"' + result.entry.value + '"' : result.entry.value));
}

/** 0.29.1 U2：恢复接管（移出「不接管」名单）。 */
function runHostsInclude(opts) {
  const target = hostsSubcommandArg(opts, 2);
  if (!target) {
    die('hub hosts include 需要 <agentId|目录>', 2,
      '示例：yotta-skills hub hosts include box；或 hub hosts include "D:\\my-agent\\skills"。');
  }
  const registryOpts = hostRegistryOptions(opts);
  const result = hostsRegistryLib.includeHost(registryOpts, { target });
  if (!result.ok) {
    die(result.error, 2, '用 yotta-skills hub hosts list 或面板「不接管」名单查看当前条目。');
  }
  auditHostEvent(opts, {
    event: 'hosts.include',
    kind: result.removed.kind,
    value: result.removed.value,
    label: result.removed.label,
  });
  if (opts.json) {
    out(JSON.stringify({ action: 'hosts.include', removed: result.removed }, null, 2));
    return;
  }
  out('✔ 已恢复接管: ' + result.removed.label + '（下次发现 / 链接生效）');
}

/** 0.29.1 U2：目录覆盖（hub hosts set <agentId> --dir <目录>；--clear 恢复默认）。 */
function runHostsSet(opts) {
  const agentId = hostsSubcommandArg(opts, 2);
  if (!agentId) {
    die('hub hosts set 需要 <agentId>', 2,
      '示例：yotta-skills hub hosts set box --dir "D:\\box-agent\\skills"；恢复默认加 --clear。');
  }
  const registryOpts = hostRegistryOptions(opts);
  if (opts.clear) {
    const result = hostsRegistryLib.clearHostOverride(registryOpts, { agentId });
    if (!result.ok) {
      die(result.error, 2, '示例：yotta-skills hub hosts set <agentId> --dir <目录>。');
    }
    auditHostEvent(opts, { event: 'hosts.set', agentId, cleared: true, dir: result.removed.dir });
    if (opts.json) {
      out(JSON.stringify({ action: 'hosts.set', cleared: true, removed: result.removed }, null, 2));
      return;
    }
    out('✔ 已恢复内置映射: ' + agentId);
    return;
  }
  const result = hostsRegistryLib.setHostOverride(registryOpts, { agentId, dir: opts.dir, label: opts.label });
  if (!result.ok) {
    die(result.error, 2, '目录需已存在，且不是 Hub / 锁桥接 / YottaCode 目录。');
  }
  auditHostEvent(opts, { event: 'hosts.set', agentId, dir: result.entry.dir, label: result.entry.label });
  if (opts.json) {
    out(JSON.stringify({ action: 'hosts.set', entry: result.entry }, null, 2));
    return;
  }
  out('✔ 已覆盖目录: ' + result.entry.label + ' -> ' + result.entry.dir);
  out('  被覆盖的旧目录不再进入默认发现 / 链接；恢复默认：yotta-skills hub hosts set ' + agentId + ' --clear。');
}

/**
 * 残留目录清理（F3）：默认预览；--yes 执行。核心逻辑在 lib/host-purge.js
 * （CLI 与面板共用，fail-closed）。
 */
function runHostsPurge(opts, dir) {
  if (!dir) {
    die('hub hosts remove --purge 需要显式目录', 2,
      '示例：yotta-skills hub hosts remove "<技能目录>" --purge（默认预览；确认后加 --yes 执行）。');
  }
  const purgeOptions = {
    hubDir: hubLib.resolveHubDir(opts),
    dir,
    homeDir: os.homedir(),
    env: process.env,
    hub: opts.hub,
  };
  const plan = hostPurgeLib.planHostPurge(purgeOptions);
  if (!plan.ok) {
    die(plan.error, 2, '只允许清理残留目录；如确认要清理，先运行 yotta-skills hub hosts mark "<目录>" --state orphan。');
  }
  if (!opts.yes) {
    const payload = {
      action: 'hosts.purge',
      dryRun: true,
      dir: plan.target,
      state: plan.state,
      hubDir: plan.hubDir,
      unlinkCount: plan.linkSlugs.length,
      keptLinks: plan.keptLinks,
      keptEntries: plan.keptEntries,
      trashedTo: plan.trashPath,
      note: '预览未执行任何变更；确认后加 --yes 执行。',
    };
    if (opts.json) { out(JSON.stringify(payload, null, 2)); return; }
    out('yotta-skills（元阁）v' + VERSION + ' —— 残留清理（预览）');
    out('目录: ' + plan.target);
    out('状态: 残留（实体未确认）');
    out('将解除 Hub 链接: ' + plan.linkSlugs.length + ' 条（非 Hub 链接 ' + plan.keptLinks + ' / 非链接内容 ' + plan.keptEntries + ' 保留）');
    out('将移入回收站: ' + plan.trashPath + '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
    out('（预览未执行任何变更；确认后加 --yes 执行）');
    return;
  }
  const result = hostPurgeLib.applyHostPurge(purgeOptions);
  if (!result.ok) {
    die(result.error, 2, '残留清理失败；请检查目录状态后重试。');
  }
  const payload = {
    action: 'hosts.purge',
    dryRun: false,
    dir: result.dir,
    state: result.state,
    hubDir: plan.hubDir,
    unlinkCount: result.unlinkCount,
    keptLinks: result.keptLinks,
    keptEntries: result.keptEntries,
    trashedTo: result.trashedTo,
    restore: '把目录移回原位置即可恢复；回收站保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天。',
  };
  if (opts.json) { out(JSON.stringify(payload, null, 2)); return; }
  out('✔ 已清理残留目录: ' + result.dir);
  out('  解除 Hub 链接: ' + result.unlinkCount + ' 条（非 Hub 链接 ' + result.keptLinks + ' / 非链接内容 ' + result.keptEntries + ' 随目录保留在回收站）');
  out('  回收站: ' + result.trashedTo + '（保留 ' + hubLib.TRASH_RETENTION_DAYS + ' 天）');
  out('  恢复: 把目录移回原位置即可。');
}

// ── install-self / where：元阁独立安装与位置查看（0.29.0 F1） ───────────────
function runSelfInstall(opts) {
  const result = selfInstallLib.installSelf({
    dir: opts.dir,
    dryRun: opts.dryRun,
    force: opts.force,
    hub: opts.hub,
    homeDir: os.homedir(),
    env: process.env,
  });
  if (!result.ok) {
    die(result.error, result.exitCode || 2,
      result.hint || '独立安装默认位置 ~/.yottaskills/yotta-skills；用 --dir 指定位置。');
  }
  if (opts.json) {
    out(JSON.stringify(result, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— 独立安装');
  out('目标: ' + result.dir);
  if (result.dryRun) {
    out('将写入: ' + result.files.join(' / '));
    out('登记: ' + result.registry);
    out('（dry-run 未执行任何写入）');
    return;
  }
  out('✔ 已安装运行件: ' + result.files.join(' / '));
  out('登记: ' + result.registry);
  out('提示: 直接用 node ' + path.join(result.dir, 'bin', 'yotta-skills.js') + ' 运行；不写宿主配置、不建全局 shim。');
}

function runWhere(opts) {
  const info = selfInstallLib.whereInfo({
    hub: opts.hub,
    homeDir: os.homedir(),
    env: process.env,
  });
  if (opts.json) {
    out(JSON.stringify(info, null, 2));
    return;
  }
  out('yotta-skills（元阁）v' + VERSION + ' —— 位置');
  out('运行中 CLI: ' + (info.running || '未知'));
  if (info.installs.length === 0) {
    out('独立安装: 未独立安装（经 npx / 宿主副本运行）');
  } else {
    for (const item of info.installs) {
      out('独立安装: ' + item.dir + '（v' + (item.version || '?') + (item.current ? '，当前运行项' : '') + '）');
    }
  }
  out('默认安装位置: ' + info.defaultDir);
  out('Hub 真源: ' + info.hubDir + '（来源: ' + skillsConfigLib.sourceLabel(info.hubSource) + '）');
  if (info.hubConfigured && info.hubSource !== 'config') {
    out('配置覆盖: ' + info.hubConfigured + '（当前被更高优先级来源覆盖）');
  }
}

// ── view：本机技能枢纽面板（127.0.0.1，只读 API + 预览确认动作） ───────────
function runView(opts) {
  const home = os.homedir();
  const hubResolved = hubLib.resolveHub({ hub: opts.hub, homeDir: home, env: process.env });
  const hubDir = hubResolved.dir;
  const port = opts.port === null || opts.port === undefined ? hubViewServerLib.DEFAULT_PORT : opts.port;
  const view = hubViewServerLib.createHubViewServer({
    hubDir,
    hubSource: hubResolved.source,
    hubFlag: Boolean(opts.hub),
    homeDir: home,
    env: process.env,
    manifest: MANIFEST,
    version: VERSION,
    port,
    html: VIEW_HTML,
    python: opts.python,
    verify: opts.verify,
    scanSkill: (skillDir, found, scanOpts) => hubScanSkill(hubDir, found, {
      python: opts.python,
      verify: opts.verify,
      skipScan: Boolean(scanOpts && scanOpts.skipScan),
    }, skillDir),
    onError: (error) => {
      if (error && error.code === 'EADDRINUSE') {
        die('端口 ' + port + ' 已被占用（yotta-skills view 未启动）', 2,
          '换一个端口：yotta-skills view --port ' + (port + 1 < 65535 ? port + 1 : 8789) + '；或先关闭占用该端口的进程。');
      }
      die('yotta-skills view 启动失败: ' + (error && error.message ? error.message : String(error)), 2,
        '检查端口占用与目录权限后重试。');
    },
  });
  view.listen(port, '127.0.0.1', () => {
    const address = view.server.address();
    const actual = address && typeof address === 'object' ? address.port : port;
    out('yotta-skills（元阁）v' + VERSION + ' —— 技能枢纽面板已启动');
    out('URL: http://127.0.0.1:' + actual + '（仅本机；按 Ctrl+C 停止）');
    out('Hub: ' + hubDir + (fs.existsSync(hubDir) ? '' : '（尚未初始化：面板会给出引导）'));
    out('边界: 零遥测 / 零远程资源；写操作需页面会话令牌，破坏性动作需二次确认。');
    // 0.30.0 OPT-04：运行标记（供 hub config get 判断「面板需重启」；best-effort）。
    const markerFile = viewServerMarkerPath({ homeDir: home, env: process.env });
    try {
      fs.mkdirSync(path.dirname(markerFile), { recursive: true });
      fs.writeFileSync(markerFile, JSON.stringify({
        pid: process.pid,
        port: actual,
        hubDir,
        startedAt: new Date().toISOString(),
      }, null, 2) + '\n');
    } catch (_) { /* 标记失败不影响面板 */ }
    process.on('exit', () => {
      try { fs.unlinkSync(markerFile); } catch (_) { /* 残留由 PID 存活检查兜底 */ }
    });
  });
}

// ── main ───────────────────────────────────────────────────────────────────
function main() {
  const node = depsLib.nodeCheck();
  if (!node.ok) {
    die('需要 Node 18+（用途：运行元阁 CLI 本体；当前 v' + node.version + '）', 4,
      depsLib.fixFor('node') + '；装好后重跑：' + currentCommand());
  }
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) { printHelp(); return; }
  if (opts.version) { out('yotta-skills v' + VERSION); return; }
  if (opts.list && !opts.command) { printList(opts); return; }
  if (opts.inventory && !opts.command) { runInventory(opts); return; }
  if (opts.reindex && !opts.command) { runReindex(opts); return; }
  if (opts.route && !opts.command) { runRoute(opts); return; }

  const command = opts.command || 'install';
  if (command === 'usage') {
    runUsage(opts);
    return;
  }
  if (command === 'decide-memory') {
    runDecideMemory(opts);
    return;
  }
  if (command === 'hook') {
    runHook(opts);
    return;
  }
  if (command === 'view') {
    runView(opts);
    return;
  }
  if (command === 'hub') {
    runHub(opts);
    return;
  }
  if (command === 'install-self') {
    runSelfInstall(opts);
    return;
  }
  if (command === 'where') {
    runWhere(opts);
    return;
  }
  if (command === 'rollback' && opts.list) {
    runRollback(opts, null);
    return;
  }
  let dest = resolveTargetDir(opts);
  if (!dest && !opts.dryRun) dest = detectProjectDir();
  if (!dest && (command === 'install' || command === 'doctor' || command === 'rollback') && !opts.dryRun) {
    die('未指定目标：请用 --agent <name> 或 --dir <path>（当前目录未检测到项目级技能目录）。', 4,
      '装到本机 Hub 用 hub install；直装到某智能体用 --agent / --dir；独立安装元阁用 install-self。');
  }

  if (opts.dryRun) {
    let skills = selectSkills(opts);
    if (command === 'update' && opts.installedOnly && dest) {
      skills = skills.filter((s) => readInstalledVersion(path.join(dest, s.slug)) !== null);
    }
    if (skills.length === 0) {
      out(opts.installedOnly
        ? 'dry-run：目标目录没有可维护的已安装家族技能（无动作）。'
        : 'dry-run：过滤后没有匹配的技能（--only / --domain）。');
      process.exitCode = opts.installedOnly ? 0 : 2;
      return;
    }
    out('yotta-skills（元阁）v' + VERSION + ' —— dry-run（' + command + '，' + skills.length + ' 个技能）');
    out('目标: ' + (dest || '未指定（将检测项目级目录）'));
    out('版本策略: ' + (opts.pin ? 'pin（锁死）' : 'range（' + skillRange(skills[0]) + '）'));
    out('');
    for (const s of skills) {
      let tag = command === 'update' ? '将检查/更新' : '将安装';
      let suffix = '';
      if (command === 'update' && dest && !opts.force && opts.pin !== false) {
        const existing = readInstalledVersion(path.join(dest, s.slug));
        const relation = versionRelation(existing, s.version);
        if (relation === 'equal') {
          tag = '已最新';
          suffix = '（跳过，v' + existing + '）';
        } else if (relation === 'local-ahead') {
          tag = '本地领先';
          suffix = '（保留不降级：v' + existing + ' > v' + s.version + '）';
        } else if (relation === 'unknown') {
          tag = '无法比较';
          suffix = '（保留：本地 v' + (existing || '未知') + '）';
        } else if (relation === 'upgrade') {
          tag = '将更新';
          suffix = '（v' + existing + ' -> v' + s.version + '）';
        } else if (relation === 'install') {
          tag = '将安装';
        }
      }
      out('  [' + tag + '] ' + s.slug.padEnd(22) + s.name.padEnd(5) + ' ' + specOf(s, opts.pin).padEnd(52) + ' ' + s.version + '  ' + s.desc + suffix);
    }
    out('');
    out('（dry-run 未执行任何下载/写入）');
    return;
  }

  if (command === 'doctor') {
    runDoctor(opts, dest);
  } else if (command === 'rollback') {
    runRollback(opts, dest);
  } else if (command === 'update') {
    if (opts.check || opts.auto) {
      var runFn = opts.auto ? runUpdateAuto : runUpdateCheck;
      runFn(opts, dest).then(function (r) {
        process.exitCode = r.code;
      });
    } else {
      const result = runUpdate(opts, dest);
      if (!result.failed) maybeAutoReindex(opts, dest);
    }
  } else {
    const result = runInstall(opts, dest);
    if (!result.failed) maybeAutoReindex(opts, dest);
  }
}

try {
  main();
} catch (err) {
  process.stderr.write('错误：' + (err && err.message ? err.message : String(err)) + '\n');
  process.stderr.write('修复建议：检查目标目录权限、npm 可用性与网络；可用 --help 查看用法。\n');
  process.exitCode = 1;
}
