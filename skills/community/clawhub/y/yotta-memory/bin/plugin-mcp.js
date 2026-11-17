#!/usr/bin/env node
// yotta-memory（元忆）插件 MCP 启动器（v0.16.6）
// 宿主（Codex / Agent Plugins）只替换 ${PLUGIN_ROOT} 与注入 PLUGIN_ROOT / PLUGIN_DATA，
// 不替换 mcp.json 里的 ${AGENT_ID} / ${AGENT_KEY_FILE}。本启动器按优先级解析身份：
//   1) 宿主已替换的 --agent-id / --agent-key-file
//   2) YOTTA_MEMORY_AGENT_ID + YOTTA_MEMORY_AGENT_KEY_FILE 环境变量
//   3) PLUGIN_DATA/identity.json（agent_id / key_file；key_file 缺省 <PLUGIN_DATA>/.yotta-memory-agent-key）
//   4) 都没有 -> 以未授权模式启动，输出可执行的绑定指引（不出现字面量占位符）
// 绑定路径：用户在 yotta-memory view 授权后，AI 执行
//   yotta-memory key claim <agent_id> --to <PLUGIN_DATA>
// 或写入 <PLUGIN_DATA>/identity.json。
'use strict';
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const AGENT_KEY_FILENAME = '.yotta-memory-agent-key';
const PLACEHOLDER_RE = /^\$\{[A-Z_]+\}$/;

function cleanValue(value) {
  const v = String(value == null ? '' : value).trim();
  if (!v || PLACEHOLDER_RE.test(v)) return '';
  return v;
}

function readIdentityFile(pluginData) {
  if (!pluginData) return null;
  const file = path.join(pluginData, 'identity.json');
  if (!fs.existsSync(file)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    const id = cleanValue(data.agent_id || data.agentId || '');
    if (!id) return null;
    const keyFile = cleanValue(data.key_file || data.keyFile || '') ||
      path.join(pluginData, AGENT_KEY_FILENAME);
    return { id: id, keyFile: keyFile, source: 'plugin-data' };
  } catch (e) {
    return null;
  }
}

function resolvePluginIdentity(opts, env) {
  opts = opts || {};
  env = env || process.env;
  const hostId = cleanValue(opts.agentId);
  const hostKey = cleanValue(opts.keyFile);
  if (hostId && hostKey) {
    return { id: hostId, keyFile: hostKey, source: 'host-args' };
  }
  const envId = cleanValue(env.YOTTA_MEMORY_AGENT_ID);
  const envKey = cleanValue(env.YOTTA_MEMORY_AGENT_KEY_FILE);
  if (envId && envKey) {
    return { id: envId, keyFile: envKey, source: 'env' };
  }
  const fromData = readIdentityFile(cleanValue(env.PLUGIN_DATA));
  if (fromData) return fromData;
  return null;
}

function parseArgs(argv) {
  const rest = [];
  const opts = { agentId: '', keyFile: '' };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--agent-id') { opts.agentId = argv[++i]; continue; }
    if (a === '--agent-key-file') { opts.keyFile = argv[++i]; continue; }
    rest.push(a);
  }
  return { rest: rest, opts: opts };
}

function guidanceText(pluginData) {
  const dataDir = pluginData || '<PLUGIN_DATA>';
  return [
    '元忆插件 MCP 尚未装配智能体身份：宿主未替换 mcp.json 中的身份占位符，且未找到环境变量或 identity.json。',
    '当前以未授权模式启动：公共 FACT 可读，私密记忆（PREF / BOUND / COMMIT）fail-closed。',
    '绑定步骤（用户授权后由 AI 执行）：',
    '  1) 用户在 yotta-memory view 中授权本智能体；',
    '  2) AI 执行  yotta-memory key claim <agent_id> --to ' + dataDir,
    '     或写入 ' + path.join(dataDir, 'identity.json') + '：{"agent_id":"<agent_id>"}',
    '  3) 重启会话后插件即可读取私密记忆。',
  ].join('\n');
}

function main() {
  const parsed = parseArgs(process.argv.slice(2));
  const ident = resolvePluginIdentity(parsed.opts, process.env);
  const cli = path.join(__dirname, 'yotta-memory.js');
  const args = [cli].concat(parsed.rest);
  if (ident) {
    args.push('--agent-id', ident.id, '--agent-key-file', ident.keyFile);
  } else {
    process.stderr.write(guidanceText(process.env.PLUGIN_DATA) + '\n');
  }
  const child = spawn(process.execPath, args, { stdio: 'inherit' });
  child.on('exit', function (code, signal) {
    if (signal) process.kill(process.pid, signal);
    else process.exit(code == null ? 0 : code);
  });
  child.on('error', function (err) {
    process.stderr.write('元忆插件 MCP 启动失败: ' + (err && err.message ? err.message : String(err)) + '\n');
    process.exit(2);
  });
}

module.exports = {
  resolvePluginIdentity: resolvePluginIdentity,
  guidanceText: guidanceText,
};

if (require.main === module) main();
