#!/usr/bin/env node
import { Command } from 'commander';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import os from 'os';
import {
  loadConfig,
  saveConfig,
  configExists,
  DEFAULT_CONFIG,
  AGENTWATCH_DIR,
  PID_PATH,
  ClawDoctorConfig,
  loadLicense,
  saveLicense,
  validateKeyRemote,
  getActivePlan,
  getPlanFeatures,
  LicenseInfo,
} from './config.js';
import { Daemon } from './daemon.js';
import { getRecentEvents, pruneOldEvents } from './store.js';
import { nowIso, runShell } from './utils.js';
import { listSnapshots, executeRollback } from './snapshots.js';
import { getRecentAudit } from './audit.js';

// eslint-disable-next-line @typescript-eslint/no-require-imports
const pkg = require('../package.json') as { version: string };

const program = new Command();

program
  .name('clawdoctor')
  .description('Self-healing doctor for OpenClaw')
  .version(pkg.version);

// ── init ──────────────────────────────────────────────────────────────────────
program
  .command('init')
  .description('Interactive setup: detect OpenClaw, configure alerts')
  .option('--openclaw-path <path>', 'Path to OpenClaw data directory')
  .option('--telegram-chat <chatid>', 'Telegram chat ID')
  .option('--auto-fix', 'Enable gateway auto-restart')
  .option('--no-prompt', 'Skip all interactive prompts, use defaults')
  .action(async (opts: {
    openclawPath?: string;
    telegramChat?: string;
    autoFix?: boolean;
    noPrompt?: boolean;
  }) => {
    const nonInteractive = !!opts.noPrompt;

    if (!nonInteractive) {
      console.log('\n🔍 ClawDoctor Setup\n');
    }

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const ask = (question: string, defaultVal = ''): Promise<string> => {
      if (nonInteractive) return Promise.resolve(defaultVal);
      return new Promise(resolve => {
        const hint = defaultVal ? ` [${defaultVal}]` : '';
        rl.question(`${question}${hint}: `, answer => {
          resolve(answer.trim() || defaultVal);
        });
      });
    };

    // Detect OpenClaw
    const defaultOpenclawPath = opts.openclawPath ?? path.join(os.homedir(), '.openclaw');
    const openclawExists = fs.existsSync(defaultOpenclawPath);
    const openclawhWhich = runShell('which openclaw');

    if (!nonInteractive) {
      if (openclawExists) {
        console.log(`✅ Found OpenClaw at ${defaultOpenclawPath}`);
      } else {
        console.log(`⚠️  OpenClaw not found at ${defaultOpenclawPath}`);
      }

      if (openclawhWhich.ok) {
        console.log(`✅ openclaw binary found at ${openclawhWhich.stdout.trim()}`);
      } else {
        console.log(`⚠️  openclaw binary not found in PATH`);
      }

      console.log('');
    }

    const openclawPath = opts.openclawPath ?? await ask('OpenClaw data path', defaultOpenclawPath);

    // Telegram setup
    let botToken = '';
    let chatId = opts.telegramChat ?? '';
    if (!nonInteractive) {
      console.log('\n📱 Telegram Alerts (optional, press Enter to skip)\n');
      botToken = await ask('Telegram bot token (leave blank to skip)', botToken);
      if (botToken) {
        chatId = await ask('Telegram chat ID', chatId);
      }
    }

    // Watcher preferences (all enabled by default in non-interactive mode)
    let enableGateway = true;
    let enableCron = true;
    let enableSession = true;
    let enableAuth = true;
    let enableCost = true;

    if (!nonInteractive) {
      console.log('\n⚙️  Watcher Configuration\n');
      enableGateway = (await ask('Monitor gateway process?', 'yes')).toLowerCase() !== 'no';
      enableCron = (await ask('Monitor crons?', 'yes')).toLowerCase() !== 'no';
      enableSession = (await ask('Monitor sessions?', 'yes')).toLowerCase() !== 'no';
      enableAuth = (await ask('Monitor auth failures?', 'yes')).toLowerCase() !== 'no';
      enableCost = (await ask('Monitor cost anomalies?', 'yes')).toLowerCase() !== 'no';
    }

    // Healer preferences
    let enableProcessRestart = opts.autoFix ?? false;
    let dryRun = false;

    if (!nonInteractive) {
      console.log('\n🔧 Auto-Fix Configuration\n');
      enableProcessRestart = (await ask('Auto-restart gateway on failure?', 'yes')).toLowerCase() !== 'no';
      dryRun = (await ask('Enable dry-run mode (no actual healing)?', 'no')).toLowerCase() === 'yes';
    }

    rl.close();

    const config: ClawDoctorConfig = {
      ...DEFAULT_CONFIG,
      openclawPath,
      watchers: {
        gateway: { enabled: enableGateway, interval: 30 },
        cron: { enabled: enableCron, interval: 60 },
        session: { enabled: enableSession, interval: 60 },
        auth: { enabled: enableAuth, interval: 60 },
        cost: { enabled: enableCost, interval: 300 },
      },
      healers: {
        processRestart: { enabled: enableProcessRestart, dryRun: false },
        cronRetry: { enabled: true, dryRun: false },
        auth: { enabled: true, dryRun: true },
        session: { enabled: true, dryRun: true },
      },
      alerts: {
        telegram: {
          enabled: !!(botToken && chatId),
          botToken: botToken || '',
          chatId: chatId || '',
        },
      },
      dryRun,
      retentionDays: 7,
    };

    saveConfig(config);
    console.log(`\n✅ Config saved to ${AGENTWATCH_DIR}/config.json`);

    if (!nonInteractive) {
      console.log('\n💡 To start monitoring now, run: clawdoctor start');
      console.log('💡 To install as a systemd service, run: clawdoctor install-service');
      console.log('');
    }
  });

// ── start ─────────────────────────────────────────────────────────────────────
program
  .command('start')
  .description('Start monitoring daemon (foreground)')
  .option('--dry-run', 'Run in dry-run mode (no healing actions)')
  .action((opts: { dryRun?: boolean }) => {
    let config: ClawDoctorConfig;
    try {
      config = loadConfig();
    } catch (err) {
      console.error(`Error: ${String(err)}`);
      process.exit(1);
    }

    if (opts.dryRun) config.dryRun = true;

    // Write PID file
    fs.mkdirSync(AGENTWATCH_DIR, { recursive: true });
    fs.writeFileSync(PID_PATH, String(process.pid), { encoding: 'utf-8', mode: 0o600 });

    const daemon = new Daemon(config);

    const shutdown = () => {
      daemon.stop();
      try { fs.unlinkSync(PID_PATH); } catch { /* ignore */ }
      process.exit(0);
    };

    process.on('SIGTERM', shutdown);
    process.on('SIGINT', shutdown);

    daemon.start();
  });

// ── stop ──────────────────────────────────────────────────────────────────────
program
  .command('stop')
  .description('Stop the running daemon')
  .action(() => {
    if (!fs.existsSync(PID_PATH)) {
      console.log('No daemon PID file found. Is clawdoctor running?');
      process.exit(1);
    }

    const pid = parseInt(fs.readFileSync(PID_PATH, 'utf-8').trim(), 10);
    if (isNaN(pid)) {
      console.error('Invalid PID file');
      process.exit(1);
    }

    try {
      process.kill(pid, 'SIGTERM');
      console.log(`Sent SIGTERM to PID ${pid}`);
    } catch (err) {
      console.error(`Failed to stop daemon (PID ${pid}):`, err);
      process.exit(1);
    }
  });

// ── status ────────────────────────────────────────────────────────────────────
program
  .command('status')
  .description('Show current health of all monitors')
  .action(async () => {
    let config: ClawDoctorConfig;
    try {
      config = loadConfig();
    } catch (err) {
      console.error(`Error: ${String(err)}`);
      process.exit(1);
    }

    const daemonRunning = isDaemonRunning();
    console.log(`\nClawDoctor Status`);
    console.log(`─────────────────`);
    console.log(`Daemon:     ${daemonRunning ? '✅ running' : '⚪ stopped'}`);
    console.log(`Config:     ${AGENTWATCH_DIR}/config.json`);
    console.log(`Dry Run:    ${config.dryRun ? 'yes' : 'no'}`);
    console.log(`Telegram:   ${config.alerts.telegram.enabled ? '✅ enabled' : '⚪ disabled'}`);
    console.log('');
    console.log('Watchers:');
    for (const [name, watcher] of Object.entries(config.watchers)) {
      console.log(`  ${watcher.enabled ? '✅' : '⚪'} ${name.padEnd(10)} (every ${watcher.interval}s)`);
    }
    console.log('');
    console.log('Healers:');
    for (const [name, healer] of Object.entries(config.healers)) {
      console.log(`  ${healer.enabled ? '✅' : '⚪'} ${name}`);
    }

    // Run a quick check
    console.log('\nRunning quick check...\n');
    const daemon = new Daemon(config);
    const results = await daemon.runOnce();

    for (const [watcherName, watchResults] of results) {
      for (const result of watchResults) {
        const icon = result.ok ? '✅' : (result.severity === 'critical' ? '🔴' : result.severity === 'error' ? '🟠' : '🟡');
        console.log(`${icon} [${watcherName}] ${result.message}`);
      }
    }
    console.log('');
  });

// ── log ───────────────────────────────────────────────────────────────────────
program
  .command('log')
  .description('Show recent events from local SQLite')
  .option('-n, --lines <number>', 'Number of events to show', '50')
  .option('-w, --watcher <name>', 'Filter by watcher name')
  .option('-s, --severity <level>', 'Filter by severity (info|warning|error|critical)')
  .action((opts: { lines: string; watcher?: string; severity?: string }) => {
    const limit = parseInt(opts.lines, 10);
    let config: ClawDoctorConfig;
    try {
      config = loadConfig();
    } catch (err) {
      console.error(`Error: ${String(err)}`);
      process.exit(1);
    }

    // Prune first
    pruneOldEvents(config.retentionDays);

    const events = getRecentEvents(
      limit,
      opts.watcher,
      opts.severity as import('./store.js').Severity | undefined
    );

    if (events.length === 0) {
      console.log('No events found.');
      return;
    }

    console.log(`\nRecent Events (${events.length})\n`);
    for (const event of events.reverse()) {
      const severityIcon = { info: '⚪', warning: '🟡', error: '🟠', critical: '🔴' }[event.severity] ?? '⚪';
      const ts = event.timestamp.slice(0, 19).replace('T', ' ');
      console.log(`${severityIcon} ${ts}  [${event.watcher}]  ${event.message}`);
      if (event.action_taken) {
        console.log(`   → ${event.action_taken}: ${event.action_result ?? ''}`);
      }
    }
    console.log('');
  });

// ── install-service ───────────────────────────────────────────────────────────
program
  .command('install-service')
  .description('Install clawdoctor as a systemd user service')
  .action(() => {
    const agentWatchBin = runShell('which clawdoctor').stdout.trim() || process.argv[1];
    const serviceContent = `[Unit]
Description=ClawDoctor - OpenClaw monitor
After=network.target

[Service]
Type=simple
ExecStart=${agentWatchBin} start
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/home/%u/.clawdoctor

[Install]
WantedBy=default.target
`;

    const systemdUserDir = path.join(os.homedir(), '.config', 'systemd', 'user');
    fs.mkdirSync(systemdUserDir, { recursive: true });
    const serviceFile = path.join(systemdUserDir, 'clawdoctor.service');
    fs.writeFileSync(serviceFile, serviceContent, 'utf-8');

    console.log(`✅ Service file written to ${serviceFile}`);
    console.log('\nTo enable and start:');
    console.log('  systemctl --user daemon-reload');
    console.log('  systemctl --user enable clawdoctor');
    console.log('  systemctl --user start clawdoctor');
    console.log('');
  });

// ── activate ──────────────────────────────────────────────────────────────────
program
  .command('activate [key]')
  .description('Activate a license key')
  .option('--key <key>', 'License key (alternative to positional argument)')
  .action(async (positionalKey?: string, opts?: { key?: string }) => {
    const key = positionalKey ?? opts?.key ?? process.env.CLAWDOCTOR_KEY;

    if (!key) {
      console.error('Usage: clawdoctor activate <key>');
      console.error('       clawdoctor activate --key <key>');
      console.error('       CLAWDOCTOR_KEY=<key> clawdoctor activate');
      process.exit(1);
    }

    console.log('Validating license key...');
    const result = await validateKeyRemote(key);

    if (!result.valid) {
      console.error('License key is invalid or expired.');
      process.exit(1);
    }

    const info: LicenseInfo = {
      key,
      plan: result.plan ?? 'diagnose',
      features: result.features ?? [],
      email: result.email,
      createdAt: result.createdAt,
      validatedAt: new Date().toISOString(),
    };

    saveLicense(info);

    console.log(`\n✅ License activated: ${info.plan.toUpperCase()} plan`);
    if (info.email) console.log(`   Account: ${info.email}`);
    console.log('\nUnlocked features:');
    for (const f of info.features) {
      console.log(`  - ${f}`);
    }
    console.log('');
  });

// ── plan ──────────────────────────────────────────────────────────────────────
program
  .command('plan')
  .description('Show current plan, features, and license status')
  .action(() => {
    const license = loadLicense();
    const plan = license?.plan ?? 'free';
    const features = license ? license.features : getPlanFeatures('free');

    console.log('\nClawDoctor Plan\n───────────────');
    console.log(`Plan:       ${plan.toUpperCase()}`);

    if (license) {
      console.log(`Key:        ${license.key.slice(0, 8)}...${license.key.slice(-4)}`);
      if (license.email) console.log(`Account:    ${license.email}`);
      console.log(`Validated:  ${license.validatedAt.slice(0, 10)}`);
      console.log(`Status:     active`);
    } else {
      const envKey = process.env.CLAWDOCTOR_KEY;
      if (envKey) {
        console.log(`Key:        via CLAWDOCTOR_KEY env var`);
        console.log(`Status:     not locally validated`);
      } else {
        console.log(`Key:        none`);
        console.log(`Status:     free tier`);
      }
    }

    console.log('\nFeatures:');
    for (const f of features) {
      console.log(`  - ${f}`);
    }

    if (plan === 'free') {
      console.log('\n💡 Upgrade at https://clawdoctor.dev/#pricing');
    }
    console.log('');
  });

// ── snapshots ─────────────────────────────────────────────────────────────────
program
  .command('snapshots')
  .description('List recent config snapshots taken before auto-fix actions')
  .option('-n, --lines <number>', 'Number of snapshots to show', '20')
  .action((opts: { lines: string }) => {
    const limit = parseInt(opts.lines, 10);
    const snapshots = listSnapshots().slice(0, limit);

    if (snapshots.length === 0) {
      console.log('No snapshots found. Snapshots are created before auto-fix actions.');
      return;
    }

    console.log(`\nConfig Snapshots (${snapshots.length})\n`);
    console.log(`${'ID'.padEnd(40)}  ${'Action'.padEnd(20)}  ${'Target'.padEnd(30)}  Timestamp`);
    console.log('─'.repeat(110));
    for (const { id, snapshot } of snapshots) {
      const ts = snapshot.timestamp.slice(0, 19).replace('T', ' ');
      console.log(
        `${id.padEnd(40)}  ${snapshot.action.padEnd(20)}  ${snapshot.target.padEnd(30)}  ${ts}`
      );
    }
    console.log(`\nRun 'clawdoctor rollback <id>' to execute a rollback.\n`);
  });

// ── rollback ──────────────────────────────────────────────────────────────────
program
  .command('rollback <snapshot-id>')
  .description('Rollback to a previous state using a snapshot')
  .option('--dry-run', 'Show what would be executed without running it')
  .action((snapshotId: string, opts: { dryRun?: boolean }) => {
    const snapshots = listSnapshots();
    const found = snapshots.find(s => s.id === snapshotId);

    if (!found) {
      console.error(`Snapshot '${snapshotId}' not found.`);
      console.error(`Run 'clawdoctor snapshots' to list available snapshots.`);
      process.exit(1);
    }

    const { snapshot } = found;
    console.log(`\nSnapshot: ${snapshotId}`);
    console.log(`Action:   ${snapshot.action}`);
    console.log(`Target:   ${snapshot.target}`);
    console.log(`Taken:    ${snapshot.timestamp.slice(0, 19).replace('T', ' ')}`);
    console.log(`Rollback: ${snapshot.rollbackCommand}`);

    if (opts.dryRun) {
      console.log('\n[DRY RUN] Would execute rollback command above.');
      return;
    }

    console.log('\nExecuting rollback...');
    const result = executeRollback(snapshotId);

    if (result.success) {
      console.log(`✅ ${result.message}`);
    } else {
      console.error(`❌ ${result.message}`);
      process.exit(1);
    }
  });

// ── audit ─────────────────────────────────────────────────────────────────────
program
  .command('audit')
  .description('Show recent healer actions from the audit trail')
  .option('-n, --lines <number>', 'Number of entries to show', '50')
  .action((opts: { lines: string }) => {
    const limit = parseInt(opts.lines, 10);
    const entries = getRecentAudit(limit);

    if (entries.length === 0) {
      console.log('No audit entries found. Entries are recorded when healers take action.');
      return;
    }

    console.log(`\nHealer Audit Trail (${entries.length} entries)\n`);
    console.log(
      `${'Timestamp'.padEnd(20)}  ${'Healer'.padEnd(16)}  ${'Tier'.padEnd(7)}  ${'Action'.padEnd(22)}  ${'Target'.padEnd(30)}  Result`
    );
    console.log('─'.repeat(120));
    for (const entry of entries) {
      const ts = entry.timestamp.slice(0, 19).replace('T', ' ');
      const tierIcon = entry.tier === 'green' ? '🟢' : '🟡';
      const resultIcon = entry.result === 'success' ? '✅' :
        entry.result === 'failed' ? '❌' :
        entry.result === 'dry-run' ? '🔵' : '⏳';
      console.log(
        `${ts.padEnd(20)}  ${entry.healer.padEnd(16)}  ${(tierIcon + ' ' + entry.tier).padEnd(9)}  ${entry.action.padEnd(22)}  ${entry.target.padEnd(30)}  ${resultIcon} ${entry.result}`
      );
      if (entry.snapshotId) {
        console.log(`${''.padEnd(20)}  Snapshot: ${entry.snapshotId}`);
      }
    }
    console.log('');
  });

function isDaemonRunning(): boolean {
  if (!fs.existsSync(PID_PATH)) return false;
  try {
    const pid = parseInt(fs.readFileSync(PID_PATH, 'utf-8').trim(), 10);
    if (isNaN(pid)) return false;
    process.kill(pid, 0); // Check if process exists
    return true;
  } catch {
    return false;
  }
}

program.parse(process.argv);
