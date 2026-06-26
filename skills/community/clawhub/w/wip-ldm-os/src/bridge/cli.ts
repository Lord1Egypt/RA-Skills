#!/usr/bin/env node
// wip-bridge/cli.ts: CLI interface.
// lesa send "message", lesa inbox, lesa search "query", lesa read <file>

import { existsSync, statSync } from "node:fs";
import {
  resolveConfig,
  resolveGatewayConfig,
  resolveApiKey,
  sendMessage,
  searchConversations,
  searchWorkspace,
  readWorkspaceFile,
  discoverSkills,
} from "./core.js";

const config = resolveConfig();

function usage(): void {
  console.log(`wip-bridge: Claude Code CLI ↔ OpenClaw TUI agent bridge

Usage:
  lesa send <message>         Send a message to the OpenClaw agent
  lesa search <query>         Semantic search over conversation history
  lesa memory <query>         Keyword search across workspace files
  lesa read <path>            Read a workspace file (relative to workspace/)
  lesa status                 Show bridge configuration
  lesa diagnose               Check gateway, inbox, DB, skills health
  lesa help                   Show this help

Examples:
  lesa send "What are you working on?"
  lesa search "API key resolution"
  lesa memory "compaction"
  lesa read MEMORY.md
  lesa read memory/2026-02-10.md`);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === "help" || command === "--help" || command === "-h") {
    usage();
    process.exit(0);
  }

  const arg = args.slice(1).join(" ");

  switch (command) {
    case "send": {
      if (!arg) {
        console.error("Error: message required. Usage: lesa send <message>");
        process.exit(1);
      }
      try {
        const reply = await sendMessage(config.openclawDir, arg);
        console.log(reply);
      } catch (err: any) {
        console.error(`Error: ${err.message}`);
        process.exit(1);
      }
      break;
    }

    case "search": {
      if (!arg) {
        console.error("Error: query required. Usage: lesa search <query>");
        process.exit(1);
      }
      try {
        const results = await searchConversations(config, arg);
        if (results.length === 0) {
          console.log("No results found.");
        } else {
          const icon: Record<string, string> = { fresh: "🟢", recent: "🟡", aging: "🟠", stale: "🔴" };
          for (const [i, r] of results.entries()) {
            const sim = r.similarity !== undefined ? ` (${(r.similarity * 100).toFixed(1)}%)` : "";
            const fresh = r.freshness ? ` ${icon[r.freshness]} ${r.freshness}` : "";
            console.log(`[${i + 1}]${sim}${fresh} ${r.sessionKey} ${r.date}`);
            console.log(r.text);
            if (i < results.length - 1) console.log("\n---\n");
          }
        }
      } catch (err: any) {
        console.error(`Error: ${err.message}`);
        process.exit(1);
      }
      break;
    }

    case "memory": {
      if (!arg) {
        console.error("Error: query required. Usage: lesa memory <query>");
        process.exit(1);
      }
      try {
        const results = searchWorkspace(config.workspaceDir, arg);
        if (results.length === 0) {
          console.log(`No workspace files matched "${arg}".`);
        } else {
          for (const r of results) {
            console.log(`### ${r.path}`);
            for (const excerpt of r.excerpts) {
              console.log(`  ${excerpt.replace(/\n/g, "\n  ")}`);
            }
            console.log();
          }
        }
      } catch (err: any) {
        console.error(`Error: ${err.message}`);
        process.exit(1);
      }
      break;
    }

    case "read": {
      if (!arg) {
        console.error("Error: path required. Usage: lesa read <path>");
        process.exit(1);
      }
      try {
        const result = readWorkspaceFile(config.workspaceDir, arg);
        console.log(result.content);
      } catch (err: any) {
        console.error(err.message);
        process.exit(1);
      }
      break;
    }

    case "status": {
      console.log(`wip-bridge status`);
      console.log(`  OpenClaw dir:  ${config.openclawDir}`);
      console.log(`  Workspace:     ${config.workspaceDir}`);
      console.log(`  Database:      ${config.dbPath}`);
      console.log(`  Inbox port:    ${config.inboxPort}`);
      console.log(`  Embedding:     ${config.embeddingModel} (${config.embeddingDimensions}d)`);
      break;
    }

    case "diagnose": {
      console.log("wip-bridge diagnose\n");
      let issues = 0;

      // 1. OpenClaw dir
      if (existsSync(config.openclawDir)) {
        console.log(`  ✓ OpenClaw dir exists: ${config.openclawDir}`);
      } else {
        console.log(`  ✗ OpenClaw dir missing: ${config.openclawDir}`);
        issues++;
      }

      // 2. Gateway config + connectivity
      try {
        const gw = resolveGatewayConfig(config.openclawDir);
        console.log(`  ✓ Gateway config found (port ${gw.port}, token present)`);

        try {
          const resp = await fetch(`http://127.0.0.1:${gw.port}/health`, { signal: AbortSignal.timeout(3000) });
          if (resp.ok) {
            console.log(`  ✓ Gateway responding on port ${gw.port}`);
          } else {
            console.log(`  ✗ Gateway returned ${resp.status}`);
            issues++;
          }
        } catch {
          console.log(`  ✗ Gateway not reachable on port ${gw.port}`);
          issues++;
        }
      } catch (err: any) {
        console.log(`  ✗ Gateway config: ${err.message}`);
        issues++;
      }

      // 3. Inbox endpoint
      try {
        const resp = await fetch(`http://127.0.0.1:${config.inboxPort}/status`, { signal: AbortSignal.timeout(3000) });
        const data = await resp.json() as { ok: boolean; pending: number };
        if (data.ok) {
          console.log(`  ✓ Inbox endpoint responding (${data.pending} pending)`);
        } else {
          console.log(`  ✗ Inbox endpoint returned unexpected response`);
          issues++;
        }
      } catch {
        console.log(`  - Inbox not running (normal if MCP server isn't started)`);
      }

      // 4. Embeddings DB
      if (existsSync(config.dbPath)) {
        const stats = statSync(config.dbPath);
        const sizeMB = (stats.size / 1024 / 1024).toFixed(1);
        console.log(`  ✓ Embeddings DB exists (${sizeMB} MB)`);
      } else {
        console.log(`  ✗ Embeddings DB missing: ${config.dbPath}`);
        issues++;
      }

      // 5. API key
      const apiKey = resolveApiKey(config.openclawDir);
      if (apiKey) {
        console.log(`  ✓ OpenAI API key found (semantic search enabled)`);
      } else {
        console.log(`  - No OpenAI API key (text search fallback)`);
      }

      // 6. Skills
      try {
        const skills = discoverSkills(config.openclawDir);
        const executable = skills.filter(s => s.hasScripts).length;
        console.log(`  ✓ Skills discovered: ${skills.length} total, ${executable} executable`);
      } catch (err: any) {
        console.log(`  ✗ Skill discovery failed: ${err.message}`);
        issues++;
      }

      // 7. Workspace
      if (existsSync(config.workspaceDir)) {
        console.log(`  ✓ Workspace dir exists`);
      } else {
        console.log(`  ✗ Workspace dir missing: ${config.workspaceDir}`);
        issues++;
      }

      console.log();
      if (issues === 0) {
        console.log("  All checks passed.");
      } else {
        console.log(`  ${issues} issue(s) found.`);
      }
      break;
    }

    default:
      console.error(`Unknown command: ${command}`);
      usage();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error(`Fatal: ${err.message}`);
  process.exit(1);
});
