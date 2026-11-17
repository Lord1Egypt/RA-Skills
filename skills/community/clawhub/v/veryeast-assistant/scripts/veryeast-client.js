#!/usr/bin/env node
/* MCP client for veryeast-assistant FastMCP server (adapted from liepin-mcp.js).
   Usage: node veryeast-client.js '{"keyword":"保安","page":1}' */
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const MCP_ENDPOINT = process.env.VEAST_MCP_URL || 'https://www.veryeast.cn/mcp';
const API_KEY_ENV_VAR = 'VEAST_API_KEY';
const CLIENT_VERSION = '0.8.4';  // 与 SKILL.md frontmatter version 保持同步（UA system_version 打点用）
const AUTH_PAGE_URL = 'https://login.veryeast.cn/skill/auth';

// 宿主 agent 识别，纯自动零配置，三层：
//   1. VEAST_HOST_AGENT 显式覆盖（可选，不依赖）；
//   2. env 平台特征变量——平台运行时自动携带（Claude Code 设 CLAUDECODE 等），symlink 安装也躲不掉，最可靠；
//   3. skill 安装路径品牌词子串匹配——process.argv[1] 保留命令行字面路径（symlink alias 不丢），
//      __filename 是解析后的 realpath（copy 安装含平台目录）；mac/Win 反斜杠已统一，Windows AppData 路径兼容。
// 故意不放 process.cwd()——agent 工作目录含品牌词会误报。UA 带宿主名，server parse_ua 取首段落 ES
// fields.agent 供运营聚合各端调用。只用于打点，非鉴权。
function detectHostAgent() {
  if (process.env.VEAST_HOST_AGENT) return process.env.VEAST_HOST_AGENT.trim().toLowerCase();
  if (process.env.CLAUDECODE || process.env.CLAUDE_CODE_ENTRYPOINT || process.env.CLAUDE_CODE_EXECPATH) return 'claude-code';
  if (process.env.OPENCLAW_CLI) return 'openclaw';  // OpenClaw 运行时自带（OPENCLAW_CLI=1 / OPENCLAW_SHELL 等）
  if (process.env.CODEX_SESSION_ID || process.env.CODEX_THREAD_ID || process.env.CODEX_SHELL) return 'codex';  // Codex CLI 运行时自带
  // ↑ 其他平台 env 特征变量在此扩展（如某平台运行时自带自身标识变量）
  const PLATFORMS = [
    { name: 'claude-code', words: ['claude'] },
    { name: 'codex',       words: ['codex'] },
    { name: 'workbuddy',   words: ['workbuddy'] },
    { name: 'doubao',      words: ['doubao', 'doubaowork'] },
    { name: 'qwen',        words: ['qwen', 'tongyi'] },
    { name: 'qianfan',     words: ['qianfan', 'qianfan-desktop-app'] },  // 百度搭子（千帆桌面版）
    { name: 'openclaw',    words: ['openclaw'] },
    { name: 'hermes',      words: ['hermes'] },
    { name: 'marvis',      words: ['marvis'] },
  ];
  const blob = [
    process.env.VEAST_SKILL_DIR,
    process.argv[1],
    __filename,
  ].filter(Boolean).map(p => p.toLowerCase().replace(/\\/g, '/')).join(' ');
  for (const p of PLATFORMS) {
    if (p.words.some(w => blob.includes(w))) return p.name;
  }
  return 'unknown';
}
const HOST_AGENT = detectHostAgent();
const USER_AGENT = HOST_AGENT !== 'unknown'
  ? HOST_AGENT + '/veryeast-assistant/' + CLIENT_VERSION
  : 'veryeast-assistant/' + CLIENT_VERSION;

function findSkillDir() {
  if (process.env.VEAST_SKILL_DIR) return process.env.VEAST_SKILL_DIR;
  return path.dirname(path.dirname(__filename));
}

function loadApiKey() {
  if (process.env[API_KEY_ENV_VAR]) return process.env[API_KEY_ENV_VAR];
  const configPath = path.join(findSkillDir(), 'config.json');
  if (fs.existsSync(configPath)) {
    try { return JSON.parse(fs.readFileSync(configPath, 'utf8')).api_key || ''; } catch (e) {}
  }
  return '';
}

let apiKey = '';

function rpc(id, method, params) {
  // id 传 null = JSON-RPC 通知（无 id，不期待响应；如 notifications/initialized）。
  // 通知带 id 会被 server 当请求解析，报 31 个校验错误刷日志。
  const isNotify = id === null;
  return new Promise((resolve, reject) => {
    const payload = { jsonrpc: '2.0', method, params: params || {} };
    if (!isNotify) payload.id = id;
    const body = JSON.stringify(payload);
    const url = new URL(MCP_ENDPOINT);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'Accept': 'application/json, text/event-stream',
        'User-Agent': USER_AGENT,  // 含宿主 agent 名（如 workbuddy/veryeast-assistant/0.7.6），server 落 ES fields.agent
      },
      timeout: 30000,
    };
    if (apiKey) options.headers['Authorization'] = 'Bearer ' + apiKey;

    const mod = url.protocol === 'https:' ? https : http;
    const req = mod.request(options, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const raw = chunks.join('').trim();
        // 401 = MCP 端点鉴权拒（api_key 无效/过期）。原始报错含内部术语，直接透传
        // 会漏技术词——统一转人话 + 授权指引（与无 key 门控同风格）
        if (res.statusCode === 401) {
          return reject(new Error('登录态无效或已过期（api_key 不正确或已过期）。请前往 ' + AUTH_PAGE_URL
            + ' 重新获取 api_key，用 node scripts/authorize.js \'<key>\' 写入后重试'));
        }
        // 其余非 2xx：打状态码 + 原始 body，杜绝把失败误读成 "结果为空"
        if (res.statusCode && res.statusCode >= 400) {
          return reject(new Error('HTTP ' + res.statusCode + ': ' + (raw || res.statusMessage || 'empty body')));
        }
        // 通知无响应体（server 回 202/空 body），不解析
        if (isNotify) return resolve({ ok: true });
        if (!raw) return resolve({ result: null });
        const lines = raw.split('\n');
        for (const l of lines) {
          const t = l.trim();
          if (t.startsWith('data:')) {
            try {
              const obj = JSON.parse(t.slice(5).trim());
              if (obj.result !== undefined || obj.error) return resolve(obj);
            } catch (e) {}
          }
        }
        try { return resolve(JSON.parse(raw)); } catch (e) {}
        reject(new Error('Failed to parse response: ' + raw.slice(0, 200)));
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.write(body);
    req.end();
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage:');
    console.error('  node scripts/veryeast-client.js \'{"keyword":"保安"}\' [toolName]');
    console.error('  node scripts/veryeast-client.js --file args.json [toolName]   # Windows PowerShell 引号问题绕行');
    console.error('  node scripts/veryeast-client.js --stdin [toolName]            # 管道/重定向读 JSON');
    console.error('  工具：search_job(默认)/resolve_area/resolve_option/resolve_job/get_resume/');
    console.error('        update_base/update_job_status/update_description/add_intention/update_intention/');
    console.error('        add_work/update_work/add_edu/update_edu/apply_job');
    process.exit(1);
  }
  // --file <path> / --stdin：从文件/管道读 JSON，绕开 Windows PowerShell 5.1 剥双引号导致解析失败
  let raw = null;
  let toolName = 'search_job';
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file') {
      const p = args[++i];
      if (!p) { console.error('--file 需要文件路径'); process.exit(1); }
      raw = fs.readFileSync(p, 'utf8');
    } else if (args[i] === '--stdin') {
      raw = fs.readFileSync(0, 'utf8');
    } else if (raw === null) {
      raw = args[i];
    } else {
      toolName = args[i];
    }
  }
  // 文件/管道可能带 BOM（Windows Out-File utf8 默认带），剥掉再解析
  if (raw) raw = raw.replace(/^﻿/, '');
  let toolArgs;
  try { toolArgs = JSON.parse(raw); } catch (e) {
    console.error('Invalid params JSON: ' + raw);
    console.error('提示：Windows PowerShell 会剥离双引号导致解析失败，可用 --file args.json 传 JSON 文件绕过');
    process.exit(1);
  }
  if (toolName === 'search_job' && !toolArgs.keyword) { console.error('keyword required'); process.exit(1); }

  apiKey = loadApiKey();

  // 投递是最高风险写操作：最后一道哨兵提醒（真正投递动作，须为用户已明确同意的职位）
  if (toolName === 'apply_job' && toolArgs.confirm === true) {
    console.error('⚠️ apply_job confirm=true：将真实投递 job_id=' + toolArgs.job_id
      + '（须为用户已明确同意的职位，否则请先展示信息并确认）');
  }

  // 所有 veryeast 接口都需要登录态：未配置 api_key 直接拦下引导，不发起任何调用。
  if (!apiKey) {
    console.error('未配置 api_key：veryeast 所有接口都需要登录态。请前往 ' + AUTH_PAGE_URL + ' 获取 api_key，');
    console.error('再用 node scripts/authorize.js \'<key>\' 写入 config.json，或设置环境变量 VEAST_API_KEY 后重试。');
    process.exit(1);
  }

  try {
    await rpc(1, 'initialize', {
      protocolVersion: '2025-03-26',
      capabilities: {},
      clientInfo: { name: 'veryeast-assistant', version: CLIENT_VERSION },
    });
    await rpc(null, 'notifications/initialized', {});  // null id = 通知，不带 id

    const result = await rpc(3, 'tools/call', { name: toolName, arguments: toolArgs });
    if (result.error) {
      console.error('MCP Error: ' + (result.error.message || JSON.stringify(result.error)));
      process.exit(1);
    }
    // FastMCP 工具错误以 isError:true 结果返回（非信封错误），需置非 0 退出码供调用方区分成败
    if (result.result && result.result.isError) {
      console.error('Tool Error: ' + JSON.stringify(result.result));
      process.exit(1);
    }
    if (result.result && result.result.content) {
      const text = result.result.content[0].text;
      try { console.log(JSON.stringify(JSON.parse(text), null, 2)); }
      catch (e) { console.log(text); }
    } else {
      console.log(JSON.stringify(result, null, 2));
    }
  } catch (err) {
    console.error('Request failed: ' + err.message);
    process.exit(1);
  }
}

main();
