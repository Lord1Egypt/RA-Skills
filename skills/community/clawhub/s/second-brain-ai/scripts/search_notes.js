#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { VAULT_PATH, readVaultDir, parseFrontmatter, resolveInput } = require('./lib/common');

function searchWithFileScan(query, limit = 5) {
  const files = readVaultDir(VAULT_PATH);
  const results = [];
  const queryLower = query.toLowerCase();
  const terms = queryLower.split(/\s+/).filter(Boolean);

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter, body } = parseFrontmatter(content);
      const title = frontmatter.title || path.basename(filePath, '.md');
      const contentLower = content.toLowerCase();

      let score = 0;
      for (const term of terms) {
        if (title.toLowerCase().includes(term)) score += 10;
        const matches = contentLower.match(new RegExp(term, 'g'));
        if (matches) score += matches.length;
      }

      if (score > 0) {
        const firstTerm = terms.find(t => contentLower.includes(t));
        let snippet = body.slice(0, 100).replace(/\n/g, ' ') + '...';
        if (firstTerm) {
          const idx = contentLower.indexOf(firstTerm);
          const start = Math.max(0, idx - 50);
          const end = Math.min(content.length, idx + firstTerm.length + 100);
          snippet = '...' + body.slice(start, end).replace(/\n/g, ' ') + '...';
        }
        results.push({
          path: path.relative(VAULT_PATH, filePath),
          title,
          snippet,
          score,
          modified: fs.statSync(filePath).mtime.toISOString().split('T')[0],
          tags: frontmatter.tags || []
        });
      }
    } catch (_) {}
  }

  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit).map((r, idx) => ({ ...r, rank: idx + 1 }));
}

function searchNotes(query, limit = 5) {
  if (!query || typeof query !== 'string') {
    return { error: 'Missing required field: query (or topic/title)' };
  }
  if (!fs.existsSync(VAULT_PATH)) {
    return { error: `Vault not found: ${VAULT_PATH}` };
  }

  const results = searchWithFileScan(query, limit);
  return {
    status: 'success',
    query,
    total: results.length,
    results,
    used_index: false
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: search_notes.js \'{...}\'', required: ['query'], optional: ['limit'] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const query = resolveInput(input, 'query', 'topic', 'title', 'q');
  const result = searchNotes(query, input.limit || 5);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
