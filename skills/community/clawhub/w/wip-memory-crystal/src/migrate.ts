#!/usr/bin/env node
// memory-crystal/migrate.ts — Import chunks from context-embeddings.sqlite
// Re-embeds with configured provider (OpenAI/Ollama/Google).

import { Crystal, resolveConfig } from './core.js';
import Database from 'better-sqlite3';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const BATCH_SIZE = 50;

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const providerFlag = args.find((_, i) => args[i - 1] === '--provider');

  const openclawHome = process.env.OPENCLAW_HOME || join(process.env.HOME || '', '.openclaw');
  const sourcePath = join(openclawHome, 'memory', 'context-embeddings.sqlite');

  if (!existsSync(sourcePath)) {
    console.error(`Source not found: ${sourcePath}`);
    process.exit(1);
  }

  const sourceDb = new Database(sourcePath, { readonly: true });
  sourceDb.pragma('journal_mode = WAL');

  // Count existing chunks
  const total = (sourceDb.prepare('SELECT COUNT(*) as count FROM conversation_chunks').get() as any).count;
  console.log(`Found ${total} chunks in context-embeddings.sqlite`);

  if (dryRun) {
    // Show sample
    const samples = sourceDb.prepare('SELECT chunk_text, role, session_key, timestamp FROM conversation_chunks ORDER BY timestamp DESC LIMIT 5').all() as any[];
    console.log('\nSample (5 most recent):');
    for (const s of samples) {
      const date = s.timestamp ? new Date(s.timestamp).toISOString().slice(0, 10) : 'unknown';
      console.log(`  [${date}] [${s.role}] ${s.chunk_text.slice(0, 80)}...`);
    }
    console.log(`\nRun without --dry-run to import all ${total} chunks.`);
    sourceDb.close();
    return;
  }

  // Initialize crystal
  const overrides: any = {};
  if (providerFlag) overrides.embeddingProvider = providerFlag;
  const config = resolveConfig(overrides);
  const crystal = new Crystal(config);
  await crystal.init();

  console.log(`Embedding provider: ${config.embeddingProvider}`);
  console.log(`Target: ${config.dataDir}`);
  console.log(`Migrating ${total} chunks in batches of ${BATCH_SIZE}...`);

  // Fetch all chunks ordered by timestamp
  const rows = sourceDb.prepare(`
    SELECT chunk_text, role, agent_id, session_key, timestamp, compaction_number
    FROM conversation_chunks
    ORDER BY timestamp ASC
  `).all() as any[];

  let imported = 0;
  let failed = 0;

  for (let i = 0; i < rows.length; i += BATCH_SIZE) {
    const batch = rows.slice(i, i + BATCH_SIZE);
    const chunks = batch.map(row => ({
      text: row.chunk_text,
      role: (row.role || 'assistant') as 'user' | 'assistant' | 'system',
      source_type: 'conversation' as const,
      source_id: row.session_key || 'unknown',
      agent_id: row.agent_id || 'main',
      token_count: Math.ceil((row.chunk_text?.length || 0) / 4),
      created_at: row.timestamp ? new Date(row.timestamp).toISOString() : new Date().toISOString(),
    }));

    try {
      const count = await crystal.ingest(chunks);
      imported += count;
      const pct = Math.round((imported / total) * 100);
      process.stdout.write(`\r  ${imported}/${total} (${pct}%)`);
    } catch (err: any) {
      failed += batch.length;
      console.error(`\n  Batch error at ${i}: ${err.message}`);
    }
  }

  console.log(`\n\nMigration complete:`);
  console.log(`  Imported: ${imported}`);
  console.log(`  Failed:   ${failed}`);
  console.log(`  Provider: ${config.embeddingProvider}`);

  const status = await crystal.status();
  console.log(`  Total chunks in crystal: ${status.chunks}`);

  crystal.close();
  sourceDb.close();
}

main().catch(err => {
  console.error(`Migration failed: ${err.message}`);
  process.exit(1);
});
