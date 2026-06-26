#!/usr/bin/env bun
// SubsTracker CLI — thin routing layer
// Usage: bun scripts/main.ts <command> [subcommand] [--flags]

import { loadConfig, init, login, hasCookie } from "./client";
import * as subscriptions from "./subscriptions";
import * as payments from "./payments";
import * as config from "./config";
import * as dashboard from "./dashboard";
import * as notifications from "./notifications";

// ─── CLI Helpers ───

function parseFlags(args: string[]): Record<string, string | boolean> {
  const flags: Record<string, string | boolean> = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i]!;
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    }
  }
  return flags;
}

function positional(args: string[]): string[] {
  return args.filter((a) => !a.startsWith("--"));
}

function out(data: unknown): void {
  console.log(JSON.stringify(data, null, 2));
}

// ─── Help ───

function printHelp(): void {
  console.log(`SubsTracker CLI

Usage: bun scripts/main.ts <command> [subcommand] [--flags]

Commands:
  login
  subscriptions list | create | get <id> | update <id> | delete <id>
                toggle <id> | renew <id> | test-notify <id>
  payments      list <sub-id> | edit <sub-id> <pid> | delete <sub-id> <pid>
  dashboard
  config        get | update
  test-notification --type telegram|bark|...

Aliases: s=subscriptions  p=payments  d=dashboard  c=config  t=test-notification

Env: SUBSTRACKER_URL, SUBSTRACKER_USER, SUBSTRACKER_PASS
  Or .substracker-skills/.env (project) | ~/.substracker-skills/.env (user)`);
}

// ─── Router ───

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === "--help" || args[0] === "-h") {
    printHelp();
    return;
  }

  const cfg = loadConfig();
  init(cfg);

  const command = args[0]!;
  const sub = args[1] || "";
  const rest = args.slice(2);
  const flags = parseFlags(rest);
  const pos = positional(rest);

  // auto-login
  if (command !== "login" && !hasCookie()) {
    console.error("[substracker] No session, logging in...");
    if (!(await login())) { console.error("[substracker] Login failed"); process.exit(1); }
    console.error("[substracker] OK");
  }

  switch (command) {
    case "login":
      out({ success: await login() });
      break;

    // ── subscriptions ──
    case "subscriptions": case "sub": case "s":
      switch (sub) {
        case "list":        out(await subscriptions.list()); break;
        case "get":         out(await subscriptions.get(pos[0]!)); break;
        case "create":      out(await subscriptions.create(flags)); break;
        case "update":      out(await subscriptions.update(pos[0]!, flags)); break;
        case "delete":      out(await subscriptions.del(pos[0]!)); break;
        case "toggle":      out(await subscriptions.toggle(pos[0]!, flags)); break;
        case "renew":       out(await subscriptions.renew(pos[0]!, flags)); break;
        case "test-notify": out(await subscriptions.testNotify(pos[0]!)); break;
        default: throw new Error(`Unknown: subscriptions ${sub}`);
      }
      break;

    // ── payments ──
    case "payments": case "pay": case "p":
      switch (sub) {
        case "list":   out(await payments.list(pos[0]!)); break;
        case "edit":   out(await payments.edit(pos[0]!, pos[1]!, flags)); break;
        case "delete": out(await payments.del(pos[0]!, pos[1]!)); break;
        default: throw new Error(`Unknown: payments ${sub}`);
      }
      break;

    // ── dashboard ──
    case "dashboard": case "dash": case "d":
      out(await dashboard.stats());
      break;

    // ── config ──
    case "config": case "cfg": case "c":
      switch (sub) {
        case "get":    out(await config.get()); break;
        case "update": out(await config.update(parseFlags(args.slice(2)))); break;
        default: throw new Error(`Unknown: config ${sub}`);
      }
      break;

    // ── test notification ──
    case "test-notification": case "test": case "t":
      out(await notifications.test(parseFlags(args.slice(1))));
      break;

    default:
      console.error(`Unknown command: ${command}`);
      printHelp();
      process.exit(1);
  }
}

await main().catch((err) => {
  console.error(`Error: ${err instanceof Error ? err.message : String(err)}`);
  process.exit(1);
});
