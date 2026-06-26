#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';

function usage() {
  return `openclaw-wtt-bootstrap

Usage:
  openclaw-wtt-bootstrap --agent-id <agent_id> --token <agent_token> [options]

Options:
  --cloud-url <url>        WTT API base (default: https://www.waxbyte.com)
  --account-id <id>        WTT account id under channels.wtt.accounts (default: default)
  --allow-from <csv|*>     commands.allowFrom.wtt value (default: *)
  --config <path>          openclaw.json path (default: ~/.openclaw/openclaw.json)
  --no-restart             Do not run 'openclaw gateway restart'
  --help                   Show help

Examples:
  openclaw-wtt-bootstrap --agent-id agent-abc --token agt_xxx
  openclaw-wtt-bootstrap --agent-id agent-abc --token agt_xxx --cloud-url https://www.waxbyte.com

Notes:
  - Get <agent_id> and <agent_token> from WTT Web (https://www.wtt.sh) claim/bind flow first.
`;
}

function parseArgs(argv) {
  const args = {
    agentId: '',
    token: '',
    cloudUrl: 'https://www.waxbyte.com',
    accountId: 'default',
    allowFrom: '*',
    configPath: process.env.OPENCLAW_CONFIG_PATH || path.join(os.homedir(), '.openclaw', 'openclaw.json'),
    restart: true,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--help' || a === '-h') return { help: true };
    if (a === '--no-restart') { args.restart = false; continue; }
    const next = argv[i + 1];
    const needValue = ['--agent-id', '--token', '--cloud-url', '--account-id', '--allow-from', '--config'];
    if (needValue.includes(a)) {
      if (!next || next.startsWith('--')) throw new Error(`Missing value for ${a}`);
      i += 1;
      if (a === '--agent-id') args.agentId = next.trim();
      if (a === '--token') args.token = next.trim();
      if (a === '--cloud-url') args.cloudUrl = next.trim();
      if (a === '--account-id') args.accountId = next.trim();
      if (a === '--allow-from') args.allowFrom = next.trim();
      if (a === '--config') args.configPath = next.trim();
      continue;
    }
    throw new Error(`Unknown arg: ${a}`);
  }

  if (!args.agentId) throw new Error('Missing --agent-id');
  if (!args.token) throw new Error('Missing --token');
  return args;
}

function asObj(v) {
  return v && typeof v === 'object' && !Array.isArray(v) ? v : {};
}

function parseAllowFrom(value) {
  if (!value) return ['*'];
  if (value === '*') return ['*'];
  return value.split(',').map((s) => s.trim()).filter(Boolean);
}

function mergeConfig(raw, params) {
  const cfg = asObj(raw);

  const plugins = asObj(cfg.plugins);
  const entries = asObj(plugins.entries);
  entries.wtt = { ...asObj(entries.wtt), enabled: true };

  const allowRaw = Array.isArray(plugins.allow) ? plugins.allow : [];
  const allow = allowRaw
    .filter((v) => typeof v === 'string')
    .map((v) => v.trim())
    .filter(Boolean);
  if (!allow.includes('wtt')) allow.push('wtt');

  plugins.entries = entries;
  plugins.allow = allow;
  cfg.plugins = plugins;

  const commands = asObj(cfg.commands);
  const allowFrom = asObj(commands.allowFrom);
  allowFrom.wtt = parseAllowFrom(params.allowFrom);
  commands.allowFrom = allowFrom;
  cfg.commands = commands;

  const channels = asObj(cfg.channels);
  const wtt = asObj(channels.wtt);
  const accounts = asObj(wtt.accounts);
  const current = asObj(accounts[params.accountId]);

  accounts[params.accountId] = {
    ...current,
    enabled: true,
    cloudUrl: params.cloudUrl,
    agentId: params.agentId,
    token: params.token,
    slashCompat: true,
    slashCompatWttPrefixOnly: true,
    slashBypassMentionGate: true,
    taskExecutorScope: 'pipeline_only',
  };

  wtt.accounts = accounts;
  channels.wtt = wtt;
  cfg.channels = channels;

  return cfg;
}

function readJsonSafe(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    if (e && e.code === 'ENOENT') return {};
    throw e;
  }
}

function writeJsonAtomic(file, obj) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  if (fs.existsSync(file)) {
    fs.copyFileSync(file, `${file}.bak`);
  }
  const tmp = `${file}.tmp-${Date.now()}`;
  fs.writeFileSync(tmp, `${JSON.stringify(obj, null, 2)}\n`, 'utf8');
  fs.renameSync(tmp, file);
}

function maskToken(token) {
  if (!token || token.length < 8) return '***';
  return `${token.slice(0, 4)}***${token.slice(-4)}`;
}

function restartGateway() {
  // Use login shell to pick up user-managed PATH (pnpm/nvm/homebrew installs).
  const r = spawnSync('bash', ['-lc', 'openclaw gateway restart'], { stdio: 'inherit' });
  if (r.status !== 0) {
    throw new Error('openclaw gateway restart failed');
  }
}

(function main() {
  try {
    const parsed = parseArgs(process.argv);
    if (parsed.help) {
      process.stdout.write(usage());
      process.exit(0);
    }

    const current = readJsonSafe(parsed.configPath);
    const next = mergeConfig(current, parsed);
    writeJsonAtomic(parsed.configPath, next);

    process.stdout.write(`✅ WTT config written: ${parsed.configPath}\n`);
    process.stdout.write(`   account: ${parsed.accountId}\n`);
    process.stdout.write(`   agentId: ${parsed.agentId}\n`);
    process.stdout.write(`   token: ${maskToken(parsed.token)}\n`);
    process.stdout.write(`   cloudUrl: ${parsed.cloudUrl}\n`);

    if (parsed.restart) {
      restartGateway();
      process.stdout.write('✅ openclaw gateway restarted\n');
    } else {
      process.stdout.write('ℹ️ restart skipped (--no-restart)\n');
    }

    process.stdout.write('\n✅ Bootstrap finished. Ensure these credentials were obtained from https://www.wtt.sh claim/bind flow.\n');
  } catch (err) {
    process.stderr.write(`❌ ${err instanceof Error ? err.message : String(err)}\n\n${usage()}`);
    process.exit(1);
  }
})();
