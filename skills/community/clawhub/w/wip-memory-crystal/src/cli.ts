#!/usr/bin/env node
// memory-crystal/cli.ts — Universal CLI interface.
// crystal search "query" | crystal remember "fact" | crystal forget <id> | crystal status

import { Crystal, resolveConfig, createCrystal, type Chunk } from './core.js';
import { scaffoldLdm, ldmPaths, ensureLdm, getAgentId, deployCaptureScript, installCron, installBackupLaunchAgent, removeCron } from './ldm.js';
import { existsSync, copyFileSync, symlinkSync, lstatSync, unlinkSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
import { execSync } from 'node:child_process';
import { createInterface } from 'node:readline';

const USAGE = `
crystal — Sovereign memory system

Commands:
  crystal search <query> [-n limit] [--agent <id>] [--since <time>] [--until <date>] [--intent <context>] [--candidates <n>] [--explain] [--provider <openai|ollama|google>]
  crystal remember <text> [--category fact|preference|event|opinion|skill|user|feedback|project|reference]
  crystal forget <id>
  crystal status [--provider <openai|ollama|google>]

  crystal sources add <path> --name <name>    Add a directory for source indexing
  crystal sources sync <name> [--dry-run]     Sync (re-index changed files)
  crystal sources status                      Show all indexed collections
  crystal sources remove <name>               Remove a collection

  crystal role                                Show current role (Core/Node/Standalone)
  crystal promote                             Promote this device to Crystal Core
  crystal demote [--relay <url>]              Demote this device to Crystal Node
  crystal doctor [--fix]                      Full health check; --fix runs heal actions (e.g. restore missing capture shim)

  crystal cleanup [--dry-run]                  Clean orphaned vec/FTS entries
  crystal backup                              Run a backup now
  crystal backup setup                        Install daily backup (LaunchAgent, 03:00)
  crystal backup --keep <n>                   Keep last n backups (default: 7)

  crystal mlx setup [--yes]                    Install MLX local LLM (Apple Silicon only)
  crystal mlx status                          Show MLX server status
  crystal mlx stop                            Stop MLX server

  crystal bridge setup                        Install + register Bridge MCP server
  crystal bridge status                       Show Bridge install state

  crystal pair                                Show QR code with relay key (generate if none)
  crystal pair --code <string>                Accept a pairing code from another device

  crystal serve [--port 18790]                Crystal Core gateway (localhost HTTP server)
  crystal dream-weave [--agent <id>] [--mode full|incremental] [--dry-run] [--since <datetime>]
  crystal init [--agent <id>] [--core] [--node] [--pair <code>] [--import <path>] [--yes] [--skip-discover]
                                              Install or update Memory Crystal
  crystal update [--agent <id>] [--yes]       Update existing install (alias for init --update)
  crystal backfill [--agent <id>] [--dry-run] [--limit <n>]  Embed raw sessions into crystal
  crystal migrate-embeddings [--dry-run]      Migrate context-embeddings into crystal
  crystal migrate-db                          Move crystal.db to ~/.ldm/memory/

Environment:
  CRYSTAL_EMBEDDING_PROVIDER   openai | ollama | google (default: openai)
  CRYSTAL_OLLAMA_HOST          Ollama URL (default: http://localhost:11434)
  CRYSTAL_REMOTE_URL           Worker URL for cloud mirror mode
  CRYSTAL_REMOTE_TOKEN         Auth token for cloud mirror
  CRYSTAL_AGENT_ID             Agent identifier (default: cc-mini)
`.trim();

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    console.log(USAGE);
    process.exit(0);
  }

  if (args[0] === '--version' || args[0] === '-v') {
    try {
      const { readFileSync } = await import('node:fs');
      const { dirname, join } = await import('node:path');
      const { fileURLToPath } = await import('node:url');
      const thisDir = dirname(fileURLToPath(import.meta.url));
      const pkg = JSON.parse(readFileSync(join(thisDir, '..', 'package.json'), 'utf-8'));
      console.log(pkg.version);
    } catch {
      console.log('unknown');
    }
    process.exit(0);
  }

  const command = args[0];

  // Parse flags
  const flags: Record<string, string> = {};
  let positional: string[] = [];
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--dry-run' || args[i] === '--yes' || args[i] === '-y' || args[i] === '--skip-discover' || args[i] === '--include-secrets' || args[i] === '--deep' || args[i] === '--core' || args[i] === '--node' || args[i] === '--update' || args[i] === '--explain') {
      flags[args[i].replace(/^-+/, '')] = 'true';
    } else if (args[i].startsWith('--') || args[i] === '-n') {
      const key = args[i].replace(/^-+/, '');
      flags[key] = args[++i] || '';
    } else {
      positional.push(args[i]);
    }
  }

  // Commands that don't need Crystal: handle before init
  if (command === 'pair') {
    const { pairShow, pairReceive } = await import('./pair.js');
    if (flags.code) {
      pairReceive(flags.code);
    } else {
      await pairShow();
    }
    return;
  }

  // ── Role commands (no Crystal init needed) ──

  if (command === 'role') {
    const { detectRole } = await import('./role.js');
    const info = detectRole();
    console.log(`Crystal Role`);
    console.log(`  Role:        ${info.role} (${info.source})`);
    console.log(`  Agent ID:    ${info.agentId}`);
    console.log(`  Local DB:    ${info.hasLocalDb ? 'yes' : 'no'}`);
    console.log(`  Embeddings:  ${info.hasLocalEmbeddings ? 'yes (local)' : 'no (relay only)'}`);
    if (info.relayUrl) {
      console.log(`  Relay URL:   ${info.relayUrl}`);
      console.log(`  Relay token: ${info.relayToken ? 'set' : 'NOT SET'}`);
      console.log(`  Relay key:   ${info.relayKeyExists ? 'present' : 'NOT FOUND'}`);
    }
    return;
  }

  if (command === 'promote') {
    const { promoteToCore, detectRole } = await import('./role.js');
    promoteToCore();
    const info = detectRole();
    console.log('This device is now Crystal Core.');
    console.log('All embeddings will be generated locally.');
    console.log(`Database: ${info.hasLocalDb ? 'found' : 'will be created on next ingest'}`);
    return;
  }

  if (command === 'demote') {
    const { demoteToNode, detectRole } = await import('./role.js');
    const relayUrl = flags.relay || positional[0];
    demoteToNode(relayUrl);
    console.log('This device is now Crystal Node.');
    console.log('Conversations will be relayed to the Core for embedding.');
    if (relayUrl) {
      console.log(`Relay URL: ${relayUrl}`);
    } else {
      console.log('Set CRYSTAL_RELAY_URL in your shell profile to enable relay.');
    }
    return;
  }

  // ── Doctor (no Crystal init needed) ──

  if (command === 'doctor') {
    const { runDoctor } = await import('./doctor.js');
    const checks = await runDoctor();
    const icons: Record<string, string> = { ok: 'OK', warn: '!!', fail: 'XX' };
    console.log('Crystal Doctor\n');
    for (const check of checks) {
      console.log(`  [${icons[check.status]}] ${check.name}: ${check.detail}`);
      if (check.fix && check.status !== 'ok') {
        console.log(`       Fix: ${check.fix}`);
      }
    }
    if ('fix' in flags) {
      const healable = checks.filter(c => c.heal && c.status !== 'ok');
      if (healable.length === 0) {
        console.log('\nNothing to fix.');
      } else {
        console.log('\nApplying fixes...');
        for (const check of healable) {
          try {
            const result = check.heal!();
            console.log(`  [OK] ${check.name}: ${result}`);
            check.status = 'ok';
            check.detail = `healed: ${result}`;
          } catch (err: any) {
            console.log(`  [XX] ${check.name}: ${err.message}`);
          }
        }
      }
    }
    const fails = checks.filter(c => c.status === 'fail').length;
    const warns = checks.filter(c => c.status === 'warn').length;
    console.log(`\n${fails === 0 && warns === 0 ? 'All checks passed.' : `${fails} failures, ${warns} warnings.`}`);
    return;
  }

  // ── Backup (no Crystal init needed) ──

  if (command === 'backup') {
    const subCmd = positional[0];
    if (subCmd === 'setup') {
      try {
        if (!existsSync(join(ldmPaths().bin, 'ldm-backup.sh'))) throw new Error('ldm-backup.sh missing at ~/.ldm/bin/. Run "ldm install" first (LDM CLI owns this shim).');
        const plistPath = installBackupLaunchAgent();
        console.log('Backup LaunchAgent installed.');
        console.log(`  Runs daily at 03:00`);
        console.log(`  Plist: ${plistPath}`);
        console.log(`  Log: ~/.ldm/logs/ldm-backup.log`);
      } catch (err: any) {
        console.error(`Setup failed: ${err.message}`);
        process.exit(1);
      }
    } else {
      // Run backup now
      const paths = ldmPaths();
      const scriptPath = join(paths.bin, 'ldm-backup.sh');
      if (!existsSync(scriptPath)) {
        console.error(`Backup script not found at ${scriptPath}. Run "ldm install" first (LDM CLI owns this shim).`);
        process.exit(1);
      }
      const keepFlag = flags.keep ? `--keep ${flags.keep}` : '';
      const secretsFlag = 'include-secrets' in flags ? '--include-secrets' : '';
      try {
        execSync(`bash ${scriptPath} ${keepFlag} ${secretsFlag}`.trim(), { stdio: 'inherit' });
      } catch (err: any) {
        process.exit(1);
      }
    }
    return;
  }

  // ── Cleanup (no Crystal init needed, opens own DB connection for VACUUM) ──

  if (command === 'cleanup') {
    const dryRun = 'dry-run' in flags;
    const config = resolveConfig();
    const dbPath = join(config.dataDir, 'crystal.db');

    if (!existsSync(dbPath)) {
      console.error(`Database not found: ${dbPath}`);
      process.exit(1);
    }

    const DatabaseCtor = (await import('better-sqlite3')).default;
    const sqliteVecMod = await import('sqlite-vec');

    const db = new DatabaseCtor(dbPath);
    db.pragma('journal_mode = WAL');
    sqliteVecMod.load(db);

    const chunkCount = (db.prepare('SELECT COUNT(*) as cnt FROM chunks').get() as any).cnt;
    console.log('Crystal Cleanup');
    console.log(`  Database: ${dbPath}`);
    console.log(`  Chunks:   ${chunkCount.toLocaleString()}`);

    const orphanedVec = (db.prepare(
      'SELECT COUNT(*) as cnt FROM chunks_vec WHERE chunk_id NOT IN (SELECT id FROM chunks)'
    ).get() as any).cnt;
    const orphanedFts = (db.prepare(
      'SELECT COUNT(*) as cnt FROM chunks_fts WHERE rowid NOT IN (SELECT id FROM chunks)'
    ).get() as any).cnt;

    console.log(`\nOrphans found:`);
    console.log(`  Vec:   ${orphanedVec.toLocaleString()} orphaned vector entries`);
    console.log(`  FTS:   ${orphanedFts.toLocaleString()} orphaned full-text entries`);

    if (orphanedVec === 0 && orphanedFts === 0) {
      console.log(`\nNo orphans found. Database is clean.`);
      db.close();
      return;
    }

    if (dryRun) {
      console.log(`\n(dry run) Run "crystal cleanup" without --dry-run to remove them.`);
      db.close();
      return;
    }

    // Backup before cleanup
    const backupPath = dbPath + `.pre-cleanup-${Date.now()}`;
    console.log(`\nBacking up database...`);
    try {
      db.pragma('wal_checkpoint(TRUNCATE)');
      copyFileSync(dbPath, backupPath);
      const bSize = statSync(backupPath).size;
      console.log(`  Backup: ${backupPath} (${(bSize / 1024 / 1024 / 1024).toFixed(2)} GB)`);
    } catch (err: any) {
      console.error(`Backup failed: ${err.message}`);
      console.error('Aborting cleanup.');
      db.close();
      process.exit(1);
    }

    // Pause cron capture
    console.log(`\nPausing capture cron...`);
    removeCron();
    console.log(`  Cron paused.`);

    try {
      // Clean orphaned vec entries in batches
      if (orphanedVec > 0) {
        console.log(`\nCleaning orphaned vectors...`);
        const ids = db.prepare(
          'SELECT chunk_id FROM chunks_vec WHERE chunk_id NOT IN (SELECT id FROM chunks)'
        ).all() as Array<{ chunk_id: number }>;
        const delVec = db.prepare('DELETE FROM chunks_vec WHERE chunk_id = ?');
        const BATCH = 1000;
        let cleaned = 0;
        for (let i = 0; i < ids.length; i += BATCH) {
          const batch = ids.slice(i, i + BATCH);
          db.transaction(() => { for (const r of batch) { delVec.run(r.chunk_id); cleaned++; } })();
          if (cleaned % 10000 === 0 || i + BATCH >= ids.length) {
            process.stderr.write(`  ${cleaned.toLocaleString()} / ${ids.length.toLocaleString()} vectors cleaned\r`);
          }
        }
        console.log(`  ${cleaned.toLocaleString()} orphaned vectors removed.                  `);
      }

      // Rebuild FTS5 index from scratch
      if (orphanedFts > 0) {
        console.log(`\nRebuilding FTS index...`);
        const ftsStart = Date.now();
        db.exec('DELETE FROM chunks_fts');
        db.exec('INSERT INTO chunks_fts(rowid, text) SELECT id, text FROM chunks');
        const ftsElapsed = ((Date.now() - ftsStart) / 1000).toFixed(1);
        console.log(`  FTS rebuilt from ${chunkCount.toLocaleString()} chunks in ${ftsElapsed}s.`);
      }

      // VACUUM
      console.log(`\nVacuuming database...`);
      const preSize = statSync(dbPath).size;
      db.exec('VACUUM');
      const postSize = statSync(dbPath).size;
      const savedMB = ((preSize - postSize) / 1024 / 1024).toFixed(0);
      console.log(`  Before: ${(preSize / 1024 / 1024 / 1024).toFixed(2)} GB`);
      console.log(`  After:  ${(postSize / 1024 / 1024 / 1024).toFixed(2)} GB`);
      console.log(`  Saved:  ${savedMB} MB`);

      // Verify
      const postChunks = (db.prepare('SELECT COUNT(*) as cnt FROM chunks').get() as any).cnt;
      const postFts = (db.prepare('SELECT COUNT(*) as cnt FROM chunks_fts').get() as any).cnt;
      console.log(`\nVerification:`);
      console.log(`  Chunks:      ${postChunks.toLocaleString()}`);
      console.log(`  FTS entries: ${postFts.toLocaleString()}`);
      console.log(`  Match: ${postChunks === postFts ? 'YES' : 'NO (WARNING: mismatch!)'}`);

      console.log(`\nCleanup complete. Verify search: crystal search "test query"`);
    } finally {
      console.log(`\nResuming capture cron...`);
      installCron();
      console.log(`  Cron resumed.`);
      db.close();
    }
    return;
  }

  // ── Bridge (no Crystal init needed) ──

  // ── MLX (no Crystal init needed) ──

  if (command === 'mlx') {
    const subCmd = positional[0] || 'status';
    const { setupMlx, isServerRunning, stopServer, doctorCheck, MLX_CONFIG } = await import('./mlx-setup.js');

    if (subCmd === 'setup') {
      const yes = 'yes' in flags || 'y' in flags;
      const result = await setupMlx({ yes });
      for (const step of result.steps) {
        console.log(`  ${result.ok ? '[OK]' : '[!!]'} ${step}`);
      }
      if (!result.ok) process.exit(1);
    } else if (subCmd === 'status') {
      const check = doctorCheck();
      const icon = check.status === 'ok' ? '[OK]' : check.status === 'warn' ? '[!!]' : '[XX]';
      console.log(`MLX LLM: ${icon} ${check.detail}`);
      if (check.fix) console.log(`  Fix: ${check.fix}`);
      console.log(`  Port: ${MLX_CONFIG.port}`);
      console.log(`  Model: ${MLX_CONFIG.model}`);
      console.log(`  Log: ${MLX_CONFIG.logPath}`);
    } else if (subCmd === 'stop') {
      if (stopServer()) {
        console.log('MLX server stopped.');
      } else {
        console.log('MLX server was not running.');
      }
    } else {
      console.error(`Unknown mlx subcommand: ${subCmd}. Use: setup, status, stop`);
      process.exit(1);
    }
    return;
  }

  if (command === 'bridge') {
    const { isBridgeInstalled, isBridgeRegistered, registerBridgeMcp, registerBridgeDesktop, isBridgeDesktopRegistered } = await import('./bridge.js');
    const subCmd = positional[0] || 'status';

    if (subCmd === 'setup') {
      if (!isBridgeInstalled()) {
        console.log('Bridge (lesa-bridge) is not installed.');
        console.log('Install it first: npm install -g lesa-bridge');
        process.exit(1);
      }
      if (!isBridgeRegistered()) {
        try {
          registerBridgeMcp();
          console.log('Bridge registered with Claude Code CLI.');
        } catch (err: any) {
          console.error(`Claude Code registration failed: ${err.message}`);
        }
      } else {
        console.log('Bridge already registered with Claude Code CLI.');
      }
      if (!isBridgeDesktopRegistered()) {
        const ok = registerBridgeDesktop();
        if (ok) console.log('Bridge registered with Claude Desktop.');
      }
      console.log('Done. Restart Claude Code to activate.');
    } else {
      // status
      console.log('Bridge Status');
      console.log(`  Installed:    ${isBridgeInstalled() ? 'yes' : 'no'}`);
      console.log(`  Claude Code:  ${isBridgeRegistered() ? 'registered' : 'not registered'}`);
      console.log(`  Desktop:      ${isBridgeDesktopRegistered() ? 'registered' : 'not registered'}`);
    }
    return;
  }

  if (command === 'update') {
    // update is an alias for init --update
    flags['update'] = 'true';
    await handleLdmCommand('init', flags, positional);
    return;
  }

  if (command === 'init' || command === 'migrate-db') {
    await handleLdmCommand(command, flags, positional);
    return;
  }

  if (command === 'serve') {
    const { startServer } = await import('./crystal-serve.js');
    const port = flags.port ? parseInt(flags.port, 10) : 18790;
    startServer(port);
    return; // Server runs indefinitely
  }

  if (command === 'dream-weave') {
    await handleDreamWeave(flags);
    return;
  }

  if (command === 'backfill') {
    await handleBackfill(flags);
    return;
  }

  if (command === 'migrate-embeddings') {
    await handleMigrateEmbeddings(flags);
    return;
  }

  const overrides: any = {};
  if (flags.provider) overrides.embeddingProvider = flags.provider;

  const config = resolveConfig(overrides);
  const crystal = new Crystal(config);
  await crystal.init();

  try {
    switch (command) {
      case 'search': {
        const query = positional.join(' ');
        if (!query) { console.error('Usage: crystal search <query>'); process.exit(1); }
        const limit = parseInt(flags.n || '5', 10);
        const filter: any = {};
        if (flags.agent) filter.agent_id = flags.agent;
        if (flags.since) filter.since = flags.since;
        if (flags.until) filter.until = flags.until;
        const intent = flags.intent as string | undefined;
        const candidateLimit = flags.candidates ? parseInt(flags.candidates, 10) : undefined;
        const explainMode = 'explain' in flags;
        const results = await crystal.deepSearch(query, limit, filter, { intent, candidateLimit, explain: explainMode });
        if (results.length === 0) {
          console.log('No results found.');
        } else {
          const icon: Record<string, string> = { fresh: '🟢', recent: '🟡', aging: '🟠', stale: '🔴' };
          console.log('(Recency-weighted. 🟢 fresh <3d, 🟡 recent <7d, 🟠 aging <14d, 🔴 stale 14d+)\n');
          for (const [i, r] of results.entries()) {
            const score = (r.score * 100).toFixed(1);
            const date = r.created_at?.slice(0, 10) || 'unknown';
            const fresh = r.freshness ? `${icon[r.freshness]} ${r.freshness}, ` : '';
            console.log(`[${i + 1}] (${fresh}${score}% match, ${r.agent_id}, ${date}, ${r.role})`);
            console.log(r.text.slice(0, 300) + (r.text.length > 300 ? '...' : ''));
            if (explainMode && (r as any).explain) {
              const e = (r as any).explain;
              console.log(`  explain: fts=${e.fts_score?.toFixed(3) || 'n/a'} vec=${e.vec_score?.toFixed(3) || 'n/a'} rrf_rank=${e.rrf_rank} rerank=${e.rerank_score.toFixed(3)} recency=${e.recency_weight.toFixed(3)} final=${e.final_score.toFixed(4)}`);
            }
            console.log('---');
          }
        }
        break;
      }

      case 'remember': {
        const text = positional.join(' ');
        if (!text) { console.error('Usage: crystal remember <text>'); process.exit(1); }
        const category = (flags.category || 'fact') as any;
        const id = await crystal.remember(text, category);
        console.log(`Remembered (id: ${id}, category: ${category}): ${text}`);
        break;
      }

      case 'forget': {
        const id = parseInt(positional[0], 10);
        if (isNaN(id)) { console.error('Usage: crystal forget <id>'); process.exit(1); }
        const ok = crystal.forget(id);
        console.log(ok ? `Forgot memory ${id}` : `Memory ${id} not found or already deprecated`);
        break;
      }

      case 'status': {
        const status = await crystal.status();
        console.log(`Memory Crystal Status`);
        console.log(`  Data dir:   ${status.dataDir}`);
        console.log(`  Provider:   ${status.embeddingProvider}`);
        console.log(`  Chunks:     ${status.chunks.toLocaleString()}`);
        console.log(`  Memories:   ${status.memories}`);
        console.log(`  Sources:    ${status.sources}`);
        console.log(`  Agents:     ${status.agents.length > 0 ? status.agents.join(', ') : 'none yet'}`);
        break;
      }

      case 'sources': {
        const subCommand = positional[0];
        if (!subCommand) {
          console.error('Usage: crystal sources <add|sync|status|remove> ...');
          process.exit(1);
        }

        switch (subCommand) {
          case 'add': {
            const path = positional[1];
            const name = flags.name;
            if (!path || !name) {
              console.error('Usage: crystal sources add <path> --name <name>');
              process.exit(1);
            }
            const col = await crystal.sourcesAdd(path, name);
            console.log(`Added collection "${col.name}" at ${col.root_path}`);
            console.log(`Run "crystal sources sync ${name}" to index files.`);
            break;
          }

          case 'sync': {
            const name = positional[1];
            if (!name) {
              console.error('Usage: crystal sources sync <name> [--dry-run]');
              process.exit(1);
            }
            const dryRun = 'dry-run' in flags;
            if (dryRun) {
              console.log(`Dry run for "${name}"...`);
            } else {
              console.log(`Syncing "${name}"...`);
            }
            const result = await crystal.sourcesSync(name, { dryRun });
            console.log(`  Added:   ${result.added} files`);
            console.log(`  Updated: ${result.updated} files`);
            console.log(`  Removed: ${result.removed} files`);
            console.log(`  Chunks:  ${result.chunks_added} embedded`);
            console.log(`  Time:    ${(result.duration_ms / 1000).toFixed(1)}s`);
            break;
          }

          case 'status': {
            const status = crystal.sourcesStatus();
            if (status.collections.length === 0) {
              console.log('No source collections. Use "crystal sources add <path> --name <name>" to add one.');
            } else {
              console.log('Source Collections:');
              for (const col of status.collections) {
                const syncAgo = col.last_sync_at
                  ? `${Math.round((Date.now() - new Date(col.last_sync_at).getTime()) / 60000)}m ago`
                  : 'never';
                console.log(`  ${col.name}: ${col.file_count.toLocaleString()} files, ${col.chunk_count.toLocaleString()} chunks, last sync ${syncAgo}`);
              }
              console.log(`  Total: ${status.total_files.toLocaleString()} files, ${status.total_chunks.toLocaleString()} chunks`);
            }
            break;
          }

          case 'remove': {
            const name = positional[1];
            if (!name) {
              console.error('Usage: crystal sources remove <name>');
              process.exit(1);
            }
            const ok = crystal.sourcesRemove(name);
            console.log(ok ? `Removed collection "${name}"` : `Collection "${name}" not found`);
            break;
          }

          default:
            console.error(`Unknown sources subcommand: ${subCommand}`);
            process.exit(1);
        }
        break;
      }

      case 'migrate-db': {
        const paths = ensureLdm();
        const HOME = process.env.HOME || '';
        const legacyDir = join(HOME, '.openclaw', 'memory-crystal');
        const legacyDb = join(legacyDir, 'crystal.db');
        const destDb = paths.crystalDb;

        if (!existsSync(legacyDb)) {
          console.error(`Source not found: ${legacyDb}`);
          process.exit(1);
        }

        if (existsSync(destDb)) {
          try {
            const stat = lstatSync(destDb);
            if (!stat.isSymbolicLink()) {
              console.error(`Destination already exists (not a symlink): ${destDb}`);
              console.error('If this is from a previous migration, remove it first.');
              process.exit(1);
            }
          } catch {}
        }

        // Copy crystal.db (never move)
        console.log(`Copying ${legacyDb} -> ${destDb}`);
        copyFileSync(legacyDb, destDb);

        // Verify copy by opening with better-sqlite3
        const Database = (await import('better-sqlite3')).default;
        const db = new Database(destDb, { readonly: true });
        const row = db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any;
        db.close();
        console.log(`Verified: ${row.count.toLocaleString()} chunks in destination DB`);

        // Create symlink: legacy path -> new path
        if (existsSync(legacyDb)) {
          try {
            const stat = lstatSync(legacyDb);
            if (!stat.isSymbolicLink()) {
              unlinkSync(legacyDb);
              symlinkSync(destDb, legacyDb);
              console.log(`Symlinked ${legacyDb} -> ${destDb}`);
            }
          } catch (err: any) {
            console.error(`Symlink failed (non-fatal): ${err.message}`);
          }
        }

        // Handle lance/ directory if it exists
        const legacyLance = join(legacyDir, 'lance');
        if (existsSync(legacyLance)) {
          try {
            const stat = lstatSync(legacyLance);
            if (!stat.isSymbolicLink()) {
              // Copy lance dir handled by LanceDB on next write
              console.log(`Note: lance/ at ${legacyLance} left in place (LanceDB will use new path on next write)`);
            }
          } catch {}
        }

        console.log('Migration complete. Restart gateway to use new path.');
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        console.log(USAGE);
        process.exit(1);
    }
  } finally {
    crystal.close();
  }
}

async function handleLdmCommand(command: string, flags: Record<string, string>, positional: string[] = []): Promise<void> {
  if (command === 'init') {
    const { detectInstallState, runInstallOrUpdate, formatUpdateSummary } = await import('./installer.js');
    const agentId = flags.agent || getAgentId();

    // Detect current state
    const state = detectInstallState();
    const isFresh = !state.ldmExists || state.installedVersion === null;
    const isUpdate = !isFresh && state.needsUpdate;

    // If already up to date and not a fresh install
    if (!isFresh && !isUpdate && !('update' in flags) && !('dry-run' in flags)) {
      console.log(`Memory Crystal v${state.repoVersion} is already installed and up to date.`);
      console.log(`Run "crystal doctor" to check health.`);
      return;
    }

    // Dry-run: show full state and doctor output, then exit
    if ('dry-run' in flags) {
      const label = isFresh ? 'not installed' : isUpdate ? `v${state.installedVersion} -> v${state.repoVersion}` : `v${state.repoVersion} (up to date)`;
      console.log(`Memory Crystal ${label}\n`);
      const { runDoctor } = await import('./doctor.js');
      const checks = await runDoctor();
      for (const c of checks) {
        const icon = c.status === 'ok' ? '[OK]' : c.status === 'warn' ? '[!!]' : '[XX]';
        console.log(`  ${icon} ${c.name}: ${c.detail}`);
        if (c.fix) console.log(`       Fix: ${c.fix}`);
      }
      if (isFresh) console.log(`\nRun "crystal init" to install.`);
      else if (isUpdate) console.log(`\nRun "crystal init" to update.`);
      else console.log(`\nNo changes needed. Already at latest version.`);
      return;
    }

    // Show what we're about to do
    if (isUpdate && state.installedVersion) {
      console.log(formatUpdateSummary(state.installedVersion, state.repoVersion));
      console.log('');
    } else if (isFresh) {
      console.log(`Installing Memory Crystal v${state.repoVersion}...`);
      console.log('');
    }

    // Determine role from flags
    let role: 'core' | 'node' | undefined;
    if ('core' in flags) role = 'core';
    else if ('node' in flags) role = 'node';

    // Run install/update
    const result = await runInstallOrUpdate({
      agentId,
      role,
      pairCode: flags.pair,
      importDb: flags.import,
      yes: 'yes' in flags || 'y' in flags,
      skipDiscover: 'skip-discover' in flags,
    });

    // Print results
    if (result.action === 'up-to-date') {
      console.log(`Memory Crystal v${result.version} is already installed and up to date.`);
      console.log(`Run "crystal doctor" to check health.`);
      return;
    }

    console.log(`\n${result.action === 'installed' ? 'Install' : 'Update'} complete (v${result.version}):\n`);
    for (const step of result.steps) {
      const isError = step.includes('failed') || step.includes('FAILED');
      console.log(`  ${isError ? '[!!]' : '[OK]'} ${step}`);
    }

    // Check bridge status
    try {
      const { isBridgeInstalled, isBridgeRegistered } = await import('./bridge.js');
      if (isBridgeInstalled() && !isBridgeRegistered()) {
        console.log(`\n  Bridge found but not registered. Run "crystal bridge setup" to connect.`);
      } else if (!isBridgeInstalled()) {
        console.log(`\n  Bridge not installed. Run "npm install -g lesa-bridge && crystal bridge setup" for AI-to-AI communication.`);
      }
    } catch {}

    // Session discovery (fresh install only, unless --skip-discover)
    if (isFresh && !('skip-discover' in flags)) {
      try {
        const { discoverAll, formatBytes } = await import('./discover.js');
        const { bulkCopyToLdm } = await import('./bulk-copy.js');

        const discovery = discoverAll();
        if (discovery.totalFiles > 0) {
          console.log(`\nDiscovered sessions:`);
          for (const b of discovery.breakdown) {
            console.log(`  ${b.platform}: ${b.files} files (${formatBytes(b.sizeBytes)})`);
          }
          console.log(`  Total: ${discovery.totalFiles} files (${formatBytes(discovery.totalSizeBytes)})`);

          let shouldCopy = 'yes' in flags || 'y' in flags;
          if (!shouldCopy && process.stdin.isTTY) {
            shouldCopy = await askYesNo(`\nCopy to LDM? [Y/n] `);
          } else if (!shouldCopy) {
            shouldCopy = true;
          }

          if (shouldCopy) {
            for (const harness of discovery.harnesses) {
              const { discoverSessionFiles } = await import('./discover.js');
              const sessionPaths = discoverSessionFiles(harness);
              const copyResult = bulkCopyToLdm(sessionPaths, agentId, {
                workspace: harness.platform === 'openclaw',
                workspaceSrc: harness.workspaceDir,
              });
              console.log(`  ${harness.platform}: copied ${copyResult.filesCopied}, skipped ${copyResult.filesSkipped} (${formatBytes(copyResult.bytesWritten)} in ${copyResult.durationMs}ms)`);
            }
          }
        } else {
          console.log(`\nNo session files found on this machine.`);
        }
      } catch (err: any) {
        console.error(`\nSession discovery failed (non-fatal): ${err.message}`);
      }
    }

    // Next steps
    console.log(`\nNext: Run "crystal doctor" to verify everything is working.`);
    if (result.action === 'installed') {
      console.log(`Restart Claude Code to activate the new hooks and MCP server.`);
    }

    return;
  }

  if (command === 'migrate-db') {
    const paths = ensureLdm();
    const HOME = process.env.HOME || '';
    const legacyDir = join(HOME, '.openclaw', 'memory-crystal');
    const legacyDb = join(legacyDir, 'crystal.db');
    const destDb = paths.crystalDb;

    if (!existsSync(legacyDb)) {
      console.error(`Source not found: ${legacyDb}`);
      process.exit(1);
    }

    if (existsSync(destDb)) {
      try {
        const stat = lstatSync(destDb);
        if (!stat.isSymbolicLink()) {
          console.error(`Destination already exists (not a symlink): ${destDb}`);
          console.error('If this is from a previous migration, remove it first.');
          process.exit(1);
        }
      } catch {}
    }

    console.log(`Copying ${legacyDb} -> ${destDb}`);
    copyFileSync(legacyDb, destDb);

    // Verify copy
    const Database = (await import('better-sqlite3')).default;
    const db = new Database(destDb, { readonly: true });
    const row = db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any;
    db.close();
    console.log(`Verified: ${row.count.toLocaleString()} chunks in destination DB`);

    // Symlink legacy path to new location
    try {
      const stat = lstatSync(legacyDb);
      if (!stat.isSymbolicLink()) {
        unlinkSync(legacyDb);
        symlinkSync(destDb, legacyDb);
        console.log(`Symlinked ${legacyDb} -> ${destDb}`);
      }
    } catch (err: any) {
      console.error(`Symlink failed (non-fatal): ${err.message}`);
    }

    console.log('Migration complete. Restart gateway to use new path.');
    return;
  }
}

// ── Dream Weave: narrative consolidation via Dream Weaver Protocol ──

async function handleDreamWeave(flags: Record<string, string>): Promise<void> {
  const agentId = flags.agent || getAgentId();
  const mode = (flags.mode || 'incremental') as 'full' | 'incremental';
  const dryRun = 'dry-run' in flags;
  const since = flags.since;
  const paths = ldmPaths(agentId);

  if (!existsSync(paths.transcripts)) {
    console.error(`No transcripts directory found at ${paths.transcripts}`);
    console.error(`Run "crystal init --agent ${agentId}" first.`);
    process.exit(1);
  }

  console.log(`Dream Weaver consolidation (${mode})`);
  console.log(`  Agent:       ${agentId}`);
  console.log(`  Transcripts: ${paths.transcripts}`);
  console.log(`  Output:      ${paths.agentRoot}`);
  if (since) console.log(`  Since:       ${since}`);
  if (dryRun) console.log(`  Mode:        dry run`);

  const { runDreamWeaver } = await import('./dream-weaver.js');

  try {
    const result = await runDreamWeaver({
      agentId,
      mode,
      transcriptsDir: paths.transcripts,
      outputDir: paths.agentRoot,
      sinceDatetime: since,
      dryRun,
    });

    console.log(`\nResults:`);
    console.log(`  Sessions processed: ${result.sessionsProcessed}`);
    console.log(`  Journals written:   ${result.journalsWritten.length}`);
    if (result.journalsWritten.length > 0) {
      for (const j of result.journalsWritten) {
        console.log(`    ${j}`);
      }
    }
    console.log(`  Identity created:   ${result.identityCreated}`);
    console.log(`  Context updated:    ${result.contextUpdated}`);
    console.log(`  Memories extracted: ${result.memoriesExtracted}`);
    console.log(`  Duration:           ${(result.durationMs / 1000).toFixed(1)}s`);
  } catch (err: any) {
    console.error(`Dream Weaver failed: ${err.message}`);
    process.exit(1);
  }
}

// ── Backfill: embed raw session files from LDM transcripts ──

async function handleBackfill(flags: Record<string, string>): Promise<void> {
  const agentId = flags.agent || getAgentId();
  const dryRun = 'dry-run' in flags;
  const limit = flags.limit ? parseInt(flags.limit, 10) : 0;
  const paths = ldmPaths(agentId);

  if (!existsSync(paths.transcripts)) {
    console.error(`No transcripts directory found at ${paths.transcripts}`);
    console.error(`Run "crystal init --agent ${agentId}" first.`);
    process.exit(1);
  }

  // Discover all JSONL files in transcripts
  const jsonlFiles: string[] = [];
  try {
    for (const file of readdirSync(paths.transcripts)) {
      if (file.endsWith('.jsonl') && !file.startsWith('.')) {
        jsonlFiles.push(join(paths.transcripts, file));
      }
    }
  } catch {}

  if (jsonlFiles.length === 0) {
    console.log(`No JSONL files found in ${paths.transcripts}`);
    console.log(`Run "crystal init" to discover and copy session files.`);
    return;
  }

  const filesToProcess = limit > 0 ? jsonlFiles.slice(0, limit) : jsonlFiles;

  // Detect format and estimate tokens
  const { isOpenClawJsonl, extractOpenClawMessages } = await import('./oc-backfill.js');

  let totalTokens = 0;
  let totalMessages = 0;
  let ocFiles = 0;
  let ccFiles = 0;

  console.log(`Scanning ${filesToProcess.length} JSONL files in ${paths.transcripts}...`);

  // First pass: scan for message count and token estimate
  for (const filePath of filesToProcess) {
    const isOC = isOpenClawJsonl(filePath);
    if (isOC) {
      ocFiles++;
      const { messages } = extractOpenClawMessages(filePath, 0);
      totalMessages += messages.length;
      totalTokens += messages.reduce((sum, m) => sum + Math.ceil(m.text.length / 4), 0);
    } else {
      ccFiles++;
      // Use cc-poller's extractMessages pattern (inline to avoid circular imports)
      const fileSize = statSync(filePath).size;
      const content = readFileSync(filePath, 'utf-8');
      const lines = content.split('\n').filter(Boolean);
      for (const line of lines) {
        try {
          const obj = JSON.parse(line);
          if (obj.type !== 'user' && obj.type !== 'assistant') continue;
          const msg = obj.message;
          if (!msg) continue;
          let text = '';
          if (typeof msg.content === 'string') text = msg.content;
          else if (Array.isArray(msg.content)) {
            text = msg.content
              .map((b: any) => b.type === 'text' ? b.text : b.type === 'thinking' ? `[thinking] ${b.thinking}` : '')
              .filter(Boolean).join('\n\n');
          }
          if (text.length >= 20) {
            totalMessages++;
            totalTokens += Math.ceil(text.length / 4);
          }
        } catch {}
      }
    }
  }

  const estimatedCost = (totalTokens / 1_000_000) * 0.02;

  console.log(`\nBackfill summary:`);
  console.log(`  Files:         ${filesToProcess.length} (${ccFiles} Claude Code, ${ocFiles} OpenClaw)`);
  console.log(`  Messages:      ${totalMessages.toLocaleString()}`);
  console.log(`  Est. tokens:   ${totalTokens.toLocaleString()}`);
  console.log(`  Est. cost:     $${estimatedCost.toFixed(2)} (text-embedding-3-small)`);
  if (limit > 0) console.log(`  Limit:         ${limit} files`);

  if (dryRun) {
    console.log(`\n(dry run, no embeddings created)`);
    return;
  }

  // Check role for relay vs local
  let role = 'core';
  try {
    const { detectRole } = await import('./role.js');
    role = detectRole().role;
  } catch {}

  if (role === 'node') {
    console.log(`\nNode mode: would relay to Core for embedding.`);
    console.log(`(Node backfill relay not yet implemented. Run on Core instead.)`);
    return;
  }

  // Local embed (Core / Standalone)
  console.log(`\nEmbedding locally...`);
  const config = resolveConfig();
  const crystal = createCrystal(config);
  await crystal.init();

  let totalChunks = 0;
  let filesProcessed = 0;
  const BATCH_SIZE = 200;

  for (const filePath of filesToProcess) {
    const isOC = isOpenClawJsonl(filePath);
    let messages: Array<{ role: string; text: string; timestamp: string; sessionId: string }>;

    if (isOC) {
      messages = extractOpenClawMessages(filePath, 0).messages;
    } else {
      messages = extractCCMessages(filePath);
    }

    if (messages.length === 0) continue;

    const maxSingleChunkChars = 2000 * 4;
    const chunks: Chunk[] = [];

    for (const msg of messages) {
      if (msg.text.length <= maxSingleChunkChars) {
        chunks.push({
          text: msg.text,
          role: msg.role as 'user' | 'assistant',
          source_type: 'conversation',
          source_id: isOC ? `oc:${msg.sessionId}` : `cc:${msg.sessionId}`,
          agent_id: agentId,
          token_count: Math.ceil(msg.text.length / 4),
          created_at: msg.timestamp,
        });
      } else {
        for (const ct of crystal.chunkText(msg.text)) {
          chunks.push({
            text: ct,
            role: msg.role as 'user' | 'assistant',
            source_type: 'conversation',
            source_id: isOC ? `oc:${msg.sessionId}` : `cc:${msg.sessionId}`,
            agent_id: agentId,
            token_count: Math.ceil(ct.length / 4),
            created_at: msg.timestamp,
          });
        }
      }
    }

    // Ingest in batches
    let fileChunks = 0;
    for (let i = 0; i < chunks.length; i += BATCH_SIZE) {
      const batch = chunks.slice(i, i + BATCH_SIZE);
      try {
        fileChunks += await crystal.ingest(batch);
      } catch (err: any) {
        process.stderr.write(`  Error on ${basename(filePath)}: ${err.message}\n`);
        break;
      }
    }

    totalChunks += fileChunks;
    filesProcessed++;
    if (filesProcessed % 50 === 0) {
      process.stderr.write(`  [${filesProcessed}/${filesToProcess.length}] ${totalChunks} chunks embedded...\n`);
    }
  }

  if ('close' in crystal) (crystal as any).close();
  console.log(`\nBackfill complete: ${totalChunks} chunks embedded from ${filesProcessed} files.`);
}

/** Extract messages from a Claude Code JSONL (inline to avoid cc-poller import). */
function extractCCMessages(filePath: string): Array<{ role: string; text: string; timestamp: string; sessionId: string }> {
  const messages: Array<{ role: string; text: string; timestamp: string; sessionId: string }> = [];
  try {
    const content = readFileSync(filePath, 'utf-8');
    for (const line of content.split('\n')) {
      if (!line) continue;
      try {
        const obj = JSON.parse(line);
        if (obj.type !== 'user' && obj.type !== 'assistant') continue;
        const msg = obj.message;
        if (!msg) continue;
        let text = '';
        if (typeof msg.content === 'string') text = msg.content;
        else if (Array.isArray(msg.content)) {
          const parts: string[] = [];
          for (const block of msg.content) {
            if (block.type === 'text' && block.text) parts.push(block.text);
            if (block.type === 'thinking' && block.thinking) parts.push(`[thinking] ${block.thinking}`);
          }
          text = parts.join('\n\n');
        }
        if (text.length < 20) continue;
        messages.push({
          role: msg.role || obj.type,
          text,
          timestamp: obj.timestamp || new Date().toISOString(),
          sessionId: obj.sessionId || 'unknown',
        });
      } catch {}
    }
  } catch {}
  return messages;
}

// ── Migrate embeddings from context-embeddings into crystal ──

async function handleMigrateEmbeddings(flags: Record<string, string>): Promise<void> {
  const dryRun = 'dry-run' in flags;
  const HOME = process.env.HOME || '';
  const cePath = join(HOME, '.openclaw', 'memory', 'context-embeddings.sqlite');

  if (!existsSync(cePath)) {
    console.error(`Context-embeddings database not found at ${cePath}`);
    process.exit(1);
  }

  const Database = (await import('better-sqlite3')).default;

  // Open CE read-only
  const ceDb = new Database(cePath, { readonly: true });
  const ceCount = (ceDb.prepare('SELECT COUNT(*) as cnt FROM conversation_chunks').get() as any).cnt;
  console.log(`Context-embeddings: ${ceCount.toLocaleString()} chunks`);

  // Open crystal
  const config = resolveConfig();
  const crystalDbPath = join(config.dataDir, 'crystal.db');
  if (!existsSync(crystalDbPath)) {
    console.error(`Crystal database not found at ${crystalDbPath}`);
    ceDb.close();
    process.exit(1);
  }

  const crystalDb = new Database(crystalDbPath);

  // Load sqlite-vec extension for chunks_vec access
  try {
    const sqliteVec = await import('sqlite-vec');
    sqliteVec.load(crystalDb);
  } catch (err: any) {
    console.error(`Failed to load sqlite-vec: ${err.message}`);
    ceDb.close();
    crystalDb.close();
    process.exit(1);
  }

  // Check for chunks_vec table
  const hasVec = crystalDb.prepare(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='chunks_vec'"
  ).get();

  if (!hasVec) {
    console.error('Crystal database missing chunks_vec table. Run crystal ingest first.');
    ceDb.close();
    crystalDb.close();
    process.exit(1);
  }

  // Count existing crystal chunks for comparison
  const crystalCount = (crystalDb.prepare('SELECT COUNT(*) as cnt FROM chunks').get() as any).cnt;
  console.log(`Crystal: ${crystalCount.toLocaleString()} chunks`);

  // Scan CE chunks, check which are unique
  const ceRows = ceDb.prepare(
    'SELECT id, agent_id, session_key, chunk_text, role, timestamp, embedding FROM conversation_chunks'
  ).all() as any[];

  const { createHash } = await import('node:crypto');
  let migrated = 0;
  let skipped = 0;
  let failed = 0;

  // Prepare crystal statements
  const checkHash = crystalDb.prepare('SELECT id FROM chunks WHERE text_hash = ?');
  const insertChunk = crystalDb.prepare(
    `INSERT INTO chunks (text, text_hash, role, source_type, source_id, agent_id, token_count, created_at)
     VALUES (?, ?, ?, 'conversation', ?, ?, ?, ?)`
  );
  const insertVec = crystalDb.prepare(
    'INSERT INTO chunks_vec (chunk_id, embedding) VALUES (?, ?)'
  );

  if (dryRun) {
    // Just count unique chunks
    for (const row of ceRows) {
      const hash = createHash('sha256').update(row.chunk_text).digest('hex');
      const existing = checkHash.get(hash);
      if (existing) {
        skipped++;
      } else {
        migrated++;
      }
    }
    console.log(`\nDry run results:`);
    console.log(`  Would migrate: ${migrated.toLocaleString()} unique chunks`);
    console.log(`  Would skip:    ${skipped.toLocaleString()} duplicates`);
    console.log(`  Cost:          $0.00 (embeddings copied directly, no API calls)`);
    ceDb.close();
    crystalDb.close();
    return;
  }

  // Backup crystal.db before migration
  console.log(`\nBacking up crystal.db...`);
  const backupPath = crystalDbPath + `.pre-migration-${Date.now()}`;
  try {
    crystalDb.backup(backupPath);
    console.log(`  Backup: ${backupPath}`);
  } catch (err: any) {
    console.error(`Backup failed: ${err.message}`);
    console.error('Aborting migration. Fix backup and retry.');
    ceDb.close();
    crystalDb.close();
    process.exit(1);
  }

  // Migrate in a transaction
  console.log(`Migrating...`);
  const migrate = crystalDb.transaction(() => {
    for (const row of ceRows) {
      const hash = createHash('sha256').update(row.chunk_text).digest('hex');
      const existing = checkHash.get(hash);
      if (existing) {
        skipped++;
        continue;
      }

      if (!row.embedding || row.embedding.length !== 6144) {
        failed++;
        continue;
      }

      try {
        // Map CE fields to crystal fields
        const agentId = row.agent_id === 'main' ? 'oc-lesa-mini' : row.agent_id;
        const sourceId = `ce:${row.session_key}`;
        const tokenCount = Math.ceil(row.chunk_text.length / 4);
        // CE uses Unix timestamp in ms; crystal uses ISO string
        const createdAt = new Date(row.timestamp).toISOString();

        const result = insertChunk.run(
          row.chunk_text, hash, row.role, sourceId, agentId, tokenCount, createdAt
        );
        const chunkId = result.lastInsertRowid;

        // Copy embedding blob directly (same model: text-embedding-3-small, float32[1536])
        insertVec.run(chunkId, row.embedding);
        migrated++;
      } catch (err: any) {
        failed++;
      }
    }
  });

  try {
    migrate();
  } catch (err: any) {
    console.error(`Migration failed: ${err.message}`);
    console.error(`Restore from backup: cp "${backupPath}" "${crystalDbPath}"`);
    ceDb.close();
    crystalDb.close();
    process.exit(1);
  }

  ceDb.close();
  crystalDb.close();

  console.log(`\nMigration complete:`);
  console.log(`  Migrated: ${migrated.toLocaleString()} unique chunks`);
  console.log(`  Skipped:  ${skipped.toLocaleString()} duplicates`);
  console.log(`  Failed:   ${failed.toLocaleString()}`);
  console.log(`  Cost:     $0.00 (embeddings copied directly)`);
  console.log(`  Backup:   ${backupPath}`);
  console.log(`\nNext: Verify with "crystal doctor" and "crystal search <test query>"`);
  console.log(`Then: Remove context-embeddings from openclaw.json plugins to stop dual-write.`);
}

// ── Helpers ──

function askYesNo(prompt: string): Promise<boolean> {
  return new Promise((resolve) => {
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    rl.question(prompt, (answer) => {
      rl.close();
      const a = answer.trim().toLowerCase();
      resolve(a === '' || a === 'y' || a === 'yes');
    });
  });
}

main().catch(err => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
