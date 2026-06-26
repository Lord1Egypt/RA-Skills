#!/usr/bin/env node
/**
 * @zouroboros/memory CLI
 *
 * Usage:
 *   zouroboros-memory init
 *   zouroboros-memory store --entity <e> --value <v> [--key <k>] [--decay <d>] [--category <c>]
 *   zouroboros-memory search <query> [--entity <e>] [--limit <n>]
 *   zouroboros-memory hybrid <query> [--limit <n>]
 *   zouroboros-memory stats
 *   zouroboros-memory batch-store <json-file>
 */

import { parseArgs } from 'util';
import { readFileSync } from 'fs';
import {
  initDatabase,
  runMigrations,
  ensureProfileSchema,
  storeFact,
  searchFacts,
  searchFactsHybrid,
  getDbStats,
  cleanupExpiredFacts,
} from './index.js';
import type { MemoryConfig } from './types.js';

const DEFAULT_DB = `${process.env.HOME ?? '~'}/.zouroboros/memory.db`;

const DEFAULT_CONFIG: MemoryConfig = {
  enabled: true,
  dbPath: process.env.ZO_MEMORY_DB ?? DEFAULT_DB,
  vectorEnabled: !!(process.env.OLLAMA_URL),
  ollamaUrl: process.env.OLLAMA_URL ?? 'http://localhost:11434',
  ollamaModel: process.env.OLLAMA_MODEL ?? 'nomic-embed-text',
  autoCapture: false,
  captureIntervalMinutes: 30,
  graphBoost: true,
  hydeExpansion: false,
  decayConfig: { permanent: Infinity, long: 365, medium: 90, short: 30 },
};

function initMemory(dbPath?: string): MemoryConfig {
  const config = dbPath ? { ...DEFAULT_CONFIG, dbPath } : DEFAULT_CONFIG;
  initDatabase(config);
  runMigrations(config);
  ensureProfileSchema();
  return config;
}

function printJson(obj: unknown): void {
  console.log(JSON.stringify(obj, null, 2));
}

async function main(): Promise<void> {
  const { values, positionals } = parseArgs({
    args: process.argv.slice(2),
    options: {
      'db-path': { type: 'string' },
      entity: { type: 'string', short: 'e' },
      key: { type: 'string', short: 'k' },
      value: { type: 'string', short: 'v' },
      decay: { type: 'string', short: 'd' },
      category: { type: 'string', short: 'c' },
      persona: { type: 'string' },
      limit: { type: 'string', short: 'l' },
      importance: { type: 'string' },
      json: { type: 'boolean', default: true },
      help: { type: 'boolean', short: 'h' },
    },
    allowPositionals: true,
    strict: false,
  });

  const subcommand = positionals[0];

  if (!subcommand || values.help) {
    console.log(`
@zouroboros/memory CLI v1.0.0

USAGE
  zouroboros-memory <subcommand> [options]

SUBCOMMANDS
  init                    Initialize database at --db-path
  store                   Store a fact
  search <query>          Keyword search
  hybrid <query>          Hybrid RRF search (keyword + vector if enabled)
  stats                   Show database statistics
  prune                   Remove expired facts
  batch-store <file.json> Bulk-store facts from a JSON array file

OPTIONS
  --db-path <path>        Database path (default: ~/.zouroboros/memory.db)
                          Also reads ZO_MEMORY_DB env var
  --entity, -e <entity>   Entity name
  --key, -k <key>         Fact key
  --value, -v <value>     Fact value
  --decay, -d <class>     Decay class: permanent|long|medium|short (default: medium)
  --category, -c <cat>    Category: fact|preference|decision|convention|other|reference|project
  --persona <name>        Persona scope (default: shared)
  --limit, -l <n>         Result limit (default: 10)
  --importance <n>        Importance score 0-1 (default: 1.0)
  --help, -h              Show this help

EXAMPLES
  zouroboros-memory init
  zouroboros-memory store -e user -k name -v "Alice" --decay permanent
  zouroboros-memory search "project preferences" --limit 5
  zouroboros-memory hybrid "what does the user prefer?"
  zouroboros-memory stats
`);
    process.exit(0);
  }

  const dbPath = values['db-path'] as string | undefined;

  switch (subcommand) {
    case 'init': {
      const config = initMemory(dbPath);
      const stats = getDbStats(config);
      console.log(`Memory initialized at: ${config.dbPath}`);
      printJson(stats);
      break;
    }

    case 'store': {
      const entity = values.entity as string | undefined;
      const value = values.value as string | undefined;

      if (!entity || !value) {
        console.error('Error: --entity and --value are required for store');
        process.exit(1);
      }

      const config = initMemory(dbPath);
      const result = await storeFact({
        entity,
        key: values.key as string | undefined,
        value,
        decay: values.decay as any,
        category: values.category as any,
        persona: values.persona as string | undefined,
        importance: values.importance ? parseFloat(values.importance as string) : undefined,
      }, config);

      printJson(result);
      break;
    }

    case 'search': {
      const query = positionals[1];
      if (!query) {
        console.error('Error: query argument required for search');
        process.exit(1);
      }

      const config = initMemory(dbPath);
      const results = searchFacts(query, {
        entity: values.entity as string | undefined,
        persona: values.persona as string | undefined,
        limit: values.limit ? parseInt(values.limit as string, 10) : 10,
      });

      printJson(results);
      break;
    }

    case 'hybrid': {
      const query = positionals[1];
      if (!query) {
        console.error('Error: query argument required for hybrid');
        process.exit(1);
      }

      const config = initMemory(dbPath);
      const results = await searchFactsHybrid(query, config, {
        persona: values.persona as string | undefined,
        limit: values.limit ? parseInt(values.limit as string, 10) : 10,
      });

      printJson(results);
      break;
    }

    case 'stats': {
      const config = initMemory(dbPath);
      const stats = getDbStats(config);
      printJson(stats);
      break;
    }

    case 'prune': {
      const config = initMemory(dbPath);
      const count = cleanupExpiredFacts();
      printJson({ pruned: count });
      break;
    }

    case 'batch-store': {
      const file = positionals[1];
      if (!file) {
        console.error('Error: file path required for batch-store');
        process.exit(1);
      }

      let facts: Array<{
        entity: string;
        value: string;
        key?: string;
        decay?: string;
        category?: string;
        persona?: string;
        importance?: number;
      }>;

      try {
        facts = JSON.parse(readFileSync(file, 'utf-8'));
        if (!Array.isArray(facts)) throw new Error('Expected a JSON array');
      } catch (err) {
        console.error(`Error reading file: ${err instanceof Error ? err.message : err}`);
        process.exit(1);
      }

      const config = initMemory(dbPath);
      let stored = 0;
      let failed = 0;

      for (const fact of facts) {
        try {
          await storeFact({
            entity: fact.entity,
            value: fact.value,
            key: fact.key,
            decay: fact.decay as any,
            category: fact.category as any,
            persona: fact.persona,
            importance: fact.importance,
          }, config);
          stored++;
        } catch (err) {
          console.error(`Failed to store fact: ${err instanceof Error ? err.message : err}`);
          failed++;
        }
      }

      printJson({ stored, failed, total: facts.length });
      break;
    }

    default: {
      console.error(`Unknown subcommand: ${subcommand}`);
      console.error('Run with --help for usage information.');
      process.exit(1);
    }
  }
}

main().catch(err => {
  console.error('Fatal error:', err instanceof Error ? err.message : err);
  process.exit(1);
});
