/**
 * Local Search - Search local files and project context
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import Fuse from 'fuse.js';

let fileIndex = [];
let fuse = null;

export async function indexProject(projectPath) {
  const patterns = [
    '**/*.js',
    '**/*.ts',
    '**/*.jsx',
    '**/*.tsx',
    '**/*.py',
    '**/*.rs',
    '**/*.go',
    '**/*.java',
    '**/*.md',
    '**/*.json'
  ];

  fileIndex = [];

  for (const pattern of patterns) {
    const files = await glob(pattern, { 
      cwd: projectPath,
      ignore: ['node_modules/**', '.git/**', 'dist/**', 'build/**', '__pycache__/**']
    });

    for (const file of files) {
      const fullPath = path.join(projectPath, file);
      try {
        const content = fs.readFileSync(fullPath, 'utf-8');
        const lines = content.split('\n');
        
        // Index in chunks for better search
        const chunkSize = 50;
        for (let i = 0; i < lines.length; i += chunkSize) {
          const chunk = lines.slice(i, i + chunkSize).join('\n');
          fileIndex.push({
            file,
            path: fullPath,
            chunk: i,
            content: chunk,
            preview: chunk.slice(0, 200)
          });
        }
      } catch (e) {
        // Skip binary or unreadable files
      }
    }
  }

  // Setup fuzzy search
  fuse = new Fuse(fileIndex, {
    keys: ['content', 'file'],
    threshold: 0.4,
    includeScore: true,
    minMatchCharLength: 3
  });

  console.log(`📂 Indexed ${fileIndex.length} chunks from ${projectPath}`);
}

export function searchLocal(parsed, projectPath) {
  if (!fuse && projectPath) {
    // Auto-index if not done
    indexProject(projectPath);
  }

  if (!fuse) return [];

  const query = [
    ...parsed.intents,
    ...parsed.languages,
    ...parsed.keywords
  ].join(' ');

  const results = fuse.search(query, { limit: 10 });

  return results.map(r => ({
    type: 'local',
    source: r.item.file,
    line: r.item.chunk * 50,
    content: r.item.content,
    score: 1 - r.item.score,
    relevance: r.item.score < 0.3 ? 'high' : r.item.score < 0.6 ? 'medium' : 'low'
  }));
}