/**
 * graph_migrate.js - 从旧 ontology 迁移数据到 unified-memory
 * 
 * 旧格式: graph.jsonl (WAL style)
 * 新格式: knowledge_graph.json (unified-memory graph_store)
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';
import { config } from '../config.js';
import { loadGraph, saveGraph } from './graph_store.js';

const OLD_ONTOLOGY = join(config.memoryDir, 'ontology/graph.jsonl');

function genId(name, type) {
  return `${type.slice(0,4).toLowerCase()}_${createHash('md5').update(`${name}::${type}`).digest('hex').slice(0, 8)}`;
}

export function migrateOldOntology() {
  if (!existsSync(OLD_ONTOLOGY)) {
    console.log('[Graph Migrate] No old ontology found, skipping');
    return { migrated: 0 };
  }

  const graph = loadGraph();
  const oldEntities = new Set(graph.entities.map(e => e.name));

  const lines = readFileSync(OLD_ONTOLOGY, 'utf8').split('\n').filter(Boolean);
  let migrated = 0;

  for (const line of lines) {
    try {
      const op = JSON.parse(line);
      
      if (op.op === 'create' && op.entity) {
        const e = op.entity;
        const typeMap = {
          'Person': 'person',
          'Organization': 'organization', 
          'Project': 'project',
          'Topic': 'topic',
          'Tool': 'tool',
        };
        const type = typeMap[e.type] || 'other';
        const name = e.properties?.name || e.properties?.title || e.id;

        if (!oldEntities.has(name)) {
          const now = new Date().toISOString();
          graph.entities.push({
            id: genId(name, type),
            name,
            type,
            description: e.properties?.description || null,
            properties: e.properties || {},
            memory_ids: [],
            count: 1,
            created_at: e.created || now,
            updated_at: e.updated || now,
          });
          oldEntities.add(name);
          migrated++;
        }
      }
    } catch {}
  }

  if (migrated > 0) {
    graph.version = (graph.version || 0) + 1;
    saveGraph(graph);
    console.log(`[Graph Migrate] Migrated ${migrated} entities`);
  }

  return { migrated };
}
