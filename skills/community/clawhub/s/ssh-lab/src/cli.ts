#!/usr/bin/env node
// ssh-lab CLI — zero-dependency argument parsing

import { hostsCommand } from './commands/hosts.js';
import { statusCommand } from './commands/status.js';
import { runCommand } from './commands/run.js';
import { tailCommand } from './commands/tail.js';
import { addCommand } from './commands/add.js';
import { lsCommand } from './commands/ls.js';
import { dfCommand } from './commands/df.js';
import { syncCommand } from './commands/sync.js';
import { watchCommand } from './commands/watch.js';
import { alertListCommand, alertAddCommand, alertRemoveCommand, alertCheckCommand } from './commands/alert.js';
import { doctorCommand } from './commands/doctor.js';
import { compareCommand } from './commands/compare.js';
import { render, exitCode } from './output/formatter.js';
import { TIMEOUT_TIERS } from './ssh/exec.js';
import type { OutputMode, AlertRuleKind } from './types/index.js';

// ── Argument parsing ────────────────────────────────────────

interface ParsedArgs {
  command: string;
  positional: string[];
  flags: Record<string, string | boolean>;
}

export function parseArgs(argv: string[]): ParsedArgs {
  const args = argv.slice(2); // skip node + script
  const positional: string[] = [];
  const flags: Record<string, string | boolean> = {};
  let command = '';

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const eqIdx = key.indexOf('=');
      if (eqIdx > 0) {
        flags[key.slice(0, eqIdx)] = key.slice(eqIdx + 1);
      } else if (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        flags[key] = args[++i];
      } else {
        flags[key] = true;
      }
    } else if (arg.startsWith('-') && arg.length === 2) {
      // Short flags: -n 50, -j (for --json), -q (for --quiet)
      const key = arg.slice(1);
      if (key === 'j') {
        flags['json'] = true;
      } else if (key === 'r') {
        flags['raw'] = true;
      } else if (key === 'q') {
        flags['quiet'] = true;
      } else if (i + 1 < args.length && !args[i + 1].startsWith('-')) {
        flags[key] = args[++i];
      } else {
        flags[key] = true;
      }
    } else if (!command) {
      command = arg;
    } else {
      positional.push(arg);
    }
  }

  return { command, positional, flags };
}

export function getOutputMode(flags: Record<string, string | boolean>): OutputMode {
  if (flags.json || flags.j) return 'json';
  if (flags.raw || flags.r) return 'raw';
  return (flags.output as OutputMode) || 'summary';
}

// ── Command dispatch ────────────────────────────────────────

const HELP = `ssh-lab — Remote server SSH workbench

USAGE:
  ssh-lab <command> [options]

COMMANDS:
  hosts                          List all configured servers
  add <name> <user@host>         Add/update a server
  status [host|all]              GPU + disk + process overview
  run <host|all> <cmd...>        Execute command on remote host(s)
  tail <host> <path> [-n lines]  Tail a remote log file
  ls <host> <path> [--sort time|size|name]  List remote directory
  df <host|all> [path]           Disk usage (+ optional du for path)
  sync <host> <src> <dst>        rsync file transfer
  watch <host> <path>            Snapshot file state (for polling)
  compare <h1> <h2> [--probes X] Side-by-side host comparison
  compare all [--probes gpu]     Compare all hosts
  doctor <host>                  Run connectivity & health diagnostics
  alert list                     Show configured alert rules
  alert add <kind> <host>        Add alert rule (gpu_idle|disk_full|process_died|...)
  alert remove <rule-id>         Remove an alert rule by id
  alert check [host|all]         Evaluate alerts against live status

OPTIONS:
  --json, -j                     Output as JSON
  --raw, -r                      Output raw text only
  --timeout <ms>                 SSH timeout (default: 15000)
  --quiet, -q                    Only output problems (for cron)
  --concurrency <n>              Max parallel SSH connections (default: 5, range: 1-50)
  --heartbeat                    Compact output for agent integration
  --probes <gpu,disk,process>    Select probes for compare
  --sort <time|size|name>        Sort order for ls (default: time)
  --direction <up|down>          Sync direction (default: down)
  --dry-run                      Sync dry run
  --help, -h                     Show this help

ALERT KINDS:
  gpu_idle, disk_full, process_died, ssh_unreachable, oom_detected, high_temp

EXAMPLES:
  ssh-lab hosts
  ssh-lab status all
  ssh-lab status GMI4 --json
  ssh-lab run GMI4 "nvidia-smi"
  ssh-lab run all "df -h" --json
  ssh-lab tail GMI4 /data/train.log -n 100
  ssh-lab ls GMI4 /data/checkpoints --sort size
  ssh-lab df all
  ssh-lab sync GMI4 /remote/ckpt ./local-ckpt
  ssh-lab doctor GMI4
  ssh-lab alert add disk_full all --threshold 90
  ssh-lab alert add process_died GMI4 --pattern "torchrun|deepspeed"
  ssh-lab alert check all
  ssh-lab add myserver user@192.168.1.100 --port 2222 --tags train,gpu
`;

async function main(): Promise<void> {
  const { command, positional, flags } = parseArgs(process.argv);
  const mode = getOutputMode(flags);
  const userTimeout = flags.timeout ? parseInt(flags.timeout as string, 10) : undefined;
  const heartbeat = !!flags.heartbeat;
  const quiet = !!(flags.quiet || flags.q);
  const concurrency = flags.concurrency
    ? Math.max(1, Math.min(50, parseInt(flags.concurrency as string, 10) || 5))
    : undefined;

  // Per-command timeout tiers (user --timeout always wins)
  const timeoutFor = (tier: keyof typeof TIMEOUT_TIERS) =>
    userTimeout ?? TIMEOUT_TIERS[tier];

  if (!command || flags.help || flags.h) {
    process.stdout.write(HELP);
    process.exit(0);
  }

  switch (command) {
    case 'hosts': {
      const result = hostsCommand();
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'add': {
      if (positional.length < 2) {
        process.stderr.write('Usage: ssh-lab add <name> <user@host> [--port N] [--tags a,b]\n');
        process.exit(1);
      }
      const tags = flags.tags ? (flags.tags as string).split(',') : undefined;
      const port = flags.port ? parseInt(flags.port as string, 10) : undefined;
      const result = addCommand(positional[0], positional[1], {
        port,
        tags,
        notes: flags.notes as string,
        defaultPath: flags.path as string,
      });
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'status': {
      const target = positional[0] || 'all';
      const result = await statusCommand(target, timeoutFor('standard'), { heartbeat, quiet, concurrency });

      if (heartbeat && quiet && result.ok) {
        // Quiet heartbeat: suppress output when all clear
        const data = result.data as any[];
        if (data && Array.isArray(data)) {
          const problems = data.flatMap((h: any) =>
            (h.alerts || []).filter((a: any) => a.level === 'warn' || a.level === 'error')
          );
          if (problems.length === 0) {
            process.exit(0);
          }
        }
      }

      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'run': {
      if (positional.length < 2) {
        process.stderr.write('Usage: ssh-lab run <host|all> <command...>\n');
        process.exit(1);
      }
      const host = positional[0];
      const cmd = positional.slice(1).join(' ');
      const result = await runCommand(host, cmd, timeoutFor('standard'), { concurrency });
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'tail': {
      if (positional.length < 2) {
        process.stderr.write('Usage: ssh-lab tail <host> <path> [-n lines]\n');
        process.exit(1);
      }
      const lines = flags.n ? parseInt(flags.n as string, 10) : 50;
      const result = await tailCommand(positional[0], positional[1], lines, timeoutFor('stream'));
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'ls': {
      if (positional.length < 2) {
        process.stderr.write('Usage: ssh-lab ls <host> <path> [--sort time|size|name]\n');
        process.exit(1);
      }
      const sort = (flags.sort as string) || 'time';
      const validSorts = ['time', 'size', 'name'] as const;
      const sortMode = validSorts.includes(sort as typeof validSorts[number])
        ? sort as 'time' | 'size' | 'name' : 'time';
      const result = await lsCommand(positional[0], positional[1], sortMode, timeoutFor('standard'));
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'df': {
      const target = positional[0] || 'all';
      const path = positional[1];
      const result = await dfCommand(target, path, timeoutFor('standard'));
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'sync': {
      if (positional.length < 3) {
        process.stderr.write('Usage: ssh-lab sync <host> <src> <dst> [--direction up|down] [--dry-run]\n');
        process.exit(1);
      }
      const direction = (flags.direction as string) === 'up' ? 'up' as const : 'down' as const;
      const exclude = flags.exclude ? (flags.exclude as string).split(',') : undefined;
      const result = await syncCommand(positional[0], positional[1], positional[2], {
        direction,
        dryRun: !!flags['dry-run'],
        exclude,
        timeoutMs: timeoutFor('transfer'),
      });
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'watch': {
      if (positional.length < 2) {
        process.stderr.write('Usage: ssh-lab watch <host> <path> [-n lines] [--prev-hash hash]\n');
        process.exit(1);
      }
      const watchLines = flags.n ? parseInt(flags.n as string, 10) : 30;
      const prevHash = flags['prev-hash'] as string | undefined;
      const result = await watchCommand(positional[0], positional[1], {
        lines: watchLines,
        prevHash,
        timeoutMs: timeoutFor('stream'),
      });
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'alert': {
      const sub = positional[0];
      switch (sub) {
        case 'list': {
          const result = alertListCommand();
          render(result, mode);
          process.exit(exitCode(result));
          break;
        }
        case 'add': {
          if (positional.length < 3) {
            process.stderr.write('Usage: ssh-lab alert add <kind> <host> [--threshold N] [--process-pattern regex]\n');
            process.stderr.write('Kinds: gpu_idle, disk_full, process_died, ssh_unreachable, oom_detected, high_temp\n');
            process.exit(1);
          }
          const kind = positional[1] as AlertRuleKind;
          const alertHost = positional[2];
          const threshold = flags.threshold ? parseInt(flags.threshold as string, 10) : undefined;
          const processPattern = flags['process-pattern'] as string | undefined;
          const result = alertAddCommand(kind, alertHost, { threshold, processPattern });
          render(result, mode);
          process.exit(exitCode(result));
          break;
        }
        case 'remove': {
          if (!positional[1]) {
            process.stderr.write('Usage: ssh-lab alert remove <rule-id>\n');
            process.exit(1);
          }
          const result = alertRemoveCommand(positional[1]);
          render(result, mode);
          process.exit(exitCode(result));
          break;
        }
        case 'check': {
          const alertTarget = positional[1] || 'all';
          const result = await alertCheckCommand(alertTarget, timeoutFor('standard'));

          // Quiet mode: no output when all clear
          if (quiet && result.ok && result.data) {
            const firings = (result.data as any[]).flatMap((r: any) => r.firings || []);
            if (firings.length === 0) {
              process.exit(0);
            }
          }

          render(result, mode);

          // Semantic exit codes: 0=ok, 1=warning, 2=critical
          const data = result.data as any[] | undefined;
          if (data) {
            const hasCritical = data.some((r: any) =>
              (r.firings || []).some((f: any) => f.level === 'critical')
            );
            const hasWarning = data.some((r: any) =>
              (r.firings || []).some((f: any) => f.level === 'warning')
            );
            process.exit(hasCritical ? 2 : hasWarning ? 1 : 0);
          }
          process.exit(exitCode(result));
          break;
        }
        default:
          process.stderr.write(`Unknown alert subcommand: ${sub || '(none)'}\n`);
          process.stderr.write('Usage: ssh-lab alert <list|add|remove|check>\n');
          process.exit(1);
      }
      break;
    }

    case 'doctor': {
      if (!positional[0]) {
        process.stderr.write('Usage: ssh-lab doctor <host>\n');
        process.exit(1);
      }
      const result = await doctorCommand(positional[0], timeoutFor('quick'));
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    case 'compare': {
      if (positional.length < 1 || flags.help || flags.h) {
        process.stderr.write(`Usage: ssh-lab compare <host1> <host2> [--probes gpu,disk,process]
       ssh-lab compare all [--probes gpu]

Compare GPU, disk, and process status across multiple hosts side-by-side.

Options:
  --probes <list>   Comma-separated probe names (default: gpu,disk,process)
  --timeout <ms>    SSH timeout per host (default: 15000)
  --json, -j        Output as JSON

Examples:
  ssh-lab compare GMI4 GMI5
  ssh-lab compare all --probes gpu
  ssh-lab compare GMI4 GMI5 GMI6 --probes gpu,disk
`);
        process.exit(positional.length < 1 ? 1 : 0);
      }
      const result = await compareCommand(positional, {
        probes: flags.probes as string | undefined,
        timeoutMs: timeoutFor('standard'),
        maxConcurrency: concurrency,
      });
      render(result, mode);
      process.exit(exitCode(result));
      break;
    }

    default:
      process.stderr.write(`Unknown command: ${command}\n\n`);
      process.stdout.write(HELP);
      process.exit(1);
  }
}

// Only run when invoked directly (not when imported as library)
const isDirectRun = process.argv[1]?.endsWith('/cli.js') || process.argv[1]?.endsWith('/cli.ts');
if (isDirectRun) {
  main().catch((err) => {
    process.stderr.write(`Fatal: ${err}\n`);
    process.exit(1);
  });
}
