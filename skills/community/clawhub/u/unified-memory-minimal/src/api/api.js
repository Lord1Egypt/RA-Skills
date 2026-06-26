/**
 * Memory API - REST API for memory operations
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAllMemories, saveMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const MEMORIES_FILE = join(MEMORY_DIR, 'memories.json');

function generateId() {
  return `mem_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
}

export function getMemories(filters) {
  let memories = getAllMemories();
  if (filters?.category) memories = memories.filter(m => m.category === filters.category);
  if (filters?.minImportance !== undefined) memories = memories.filter(m => m.importance >= filters.minImportance);
  memories.sort((a, b) => (b.importance || 0.5) - (a.importance || 0.5));
  if (filters?.limit) memories = memories.slice(0, filters.limit);
  return memories;
}

export function getMemory(id) {
  const memories = getAllMemories();
  return memories.find(m => m.id === id) || null;
}

export function createMemory(data) {
  const memories = getAllMemories();
  const now = new Date().toISOString();
  const memory = {
    id: generateId(),
    text: data.text,
    category: data.category || 'general',
    importance: data.importance ?? 0.5,
    confidence: data.confidence ?? 0.8,
    tags: data.tags || [],
    project: data.project || 'default',
    created_at: now,
    updated_at: now,
    accessed_at: now,
    access_count: 0,
  };
  memories.push(memory);
  saveMemories(memories);
  return memory;
}

export function updateMemory(id, data) {
  const memories = getAllMemories();
  const idx = memories.findIndex(m => m.id === id);
  if (idx === -1) return null;
  memories[idx] = { ...memories[idx], ...data, id, updated_at: new Date().toISOString() };
  saveMemories(memories);
  return memories[idx];
}

export function deleteMemory(id) {
  const memories = getAllMemories();
  const idx = memories.findIndex(m => m.id === id);
  if (idx === -1) return false;
  memories.splice(idx, 1);
  saveMemories(memories);
  return true;
}

export function searchMemories(query, limit = 10) {
  const memories = getAllMemories();
  const q = query.toLowerCase();
  const results = memories.filter(m => 
    m.text.toLowerCase().includes(q) || (m.tags && m.tags.some(t => t.toLowerCase().includes(q)))
  );
  return results.slice(0, limit);
}

export function recordAccess(id) {
  const memories = getAllMemories();
  const idx = memories.findIndex(m => m.id === id);
  if (idx !== -1) {
    memories[idx].access_count = (memories[idx].access_count || 0) + 1;
    memories[idx].accessed_at = new Date().toISOString();
    saveMemories(memories);
  }
}

export function printStats() {
  const memories = getAllMemories();
  const byCategory = {};
  const byTier = { hot: 0, warm: 0, cold: 0 };
  let totalImportance = 0;
  
  for (const m of memories) {
    byCategory[m.category] = (byCategory[m.category] || 0) + 1;
    totalImportance += m.importance || 0.5;
    const ac = m.access_count || 0;
    if (ac > 10) byTier.hot++;
    else if (ac > 2) byTier.warm++;
    else byTier.cold++;
  }
  
  console.log('\n📊 Memory Statistics\n');
  console.log(`  Total Memories: ${memories.length}`);
  console.log(`  Average Importance: ${memories.length > 0 ? (totalImportance / memories.length).toFixed(2) : 0}`);
  console.log('\n  By Category:');
  for (const [cat, count] of Object.entries(byCategory)) console.log(`    ${cat}: ${count}`);
  console.log('\n  By Tier:');
  console.log(`    Hot (access > 10): ${byTier.hot}`);
  console.log(`    Warm (access 3-10): ${byTier.warm}`);
  console.log(`    Cold (access < 3): ${byTier.cold}`);
  console.log('');
}

export function createApiServer(port = 37888) {
  const http = require('http');
  
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://localhost:${port}`);
    const path = url.pathname;
    const method = req.method;
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');
    
    if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }
    
    try {
      let body = '';
      if (['POST', 'PUT', 'PATCH'].includes(method)) {
        body = await new Promise((resolve, reject) => {
          let data = '';
          req.on('data', chunk => { data += chunk.toString(); });
          req.on('end', () => resolve(data));
          req.on('error', reject);
        });
      }
      
      let response;
      
      if (path === '/api/memories' && method === 'GET') {
        const limit = parseInt(url.searchParams.get('limit') || '50', 10);
        response = { success: true, data: getMemories({ limit }) };
      } else if (path.startsWith('/api/memories/') && method === 'GET') {
        const id = path.split('/')[3];
        const memory = getMemory(id);
        if (memory) { recordAccess(id); response = { success: true, data: memory }; }
        else response = { success: false, error: 'Not found' };
      } else if (path === '/api/memories' && method === 'POST') {
        const data = body ? JSON.parse(body) : {};
        response = { success: true, data: createMemory(data) };
      } else if (path === '/api/stats' && method === 'GET') {
        const memories = getAllMemories();
        response = { success: true, data: { total: memories.length, byCategory: {} } };
      } else if (path === '/api/health' && method === 'GET') {
        const memories = getAllMemories();
        response = { success: true, data: { score: memories.length > 0 ? 85 : 50, total: memories.length } };
      } else {
        response = { success: false, error: 'Not found' };
      }
      
      res.writeHead(response.success ? 200 : 404);
      res.end(JSON.stringify(response));
    } catch (e) {
      res.writeHead(500);
      res.end(JSON.stringify({ success: false, error: e.message }));
    }
  });
  
  server.listen(port, () => {
    console.log(`🧠 Memory API server running at http://localhost:${port}`);
  });
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const port = parseInt(args.find(a => a.startsWith('--port='))?.split('=')[1] || '37888', 10);
  createApiServer(port);
}
