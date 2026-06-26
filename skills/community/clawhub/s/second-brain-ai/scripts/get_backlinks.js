#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { VAULT_PATH, readVaultDir, parseFrontmatter, extractWikiLinks, resolveInput, findNoteByTitle } = require('./lib/common');

function getBacklinks(noteTitle) {
  if (!noteTitle || typeof noteTitle !== 'string') {
    return { error: 'Missing required field: note_title' };
  }
  if (!fs.existsSync(VAULT_PATH)) {
    return { error: `Vault not found: ${VAULT_PATH}` };
  }

  const targetNote = findNoteByTitle(noteTitle);
  const backlinks = [];

  if (!targetNote) {
    return {
      note_title: noteTitle,
      note_found: false,
      note_path: null,
      backlink_count: 0,
      backlinks: []
    };
  }

  const titleLower = noteTitle.toLowerCase();
  const files = readVaultDir(VAULT_PATH);

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter, body } = parseFrontmatter(content);
      const title = frontmatter.title || path.basename(filePath, '.md');
      if (title.toLowerCase() === titleLower) continue;

      const links = extractWikiLinks(content);
      const matchingLink = links.find(l => l.toLowerCase() === titleLower);

      if (matchingLink) {
        const lines = body.split('\n');
        let context = '';
        for (let i = 0; i < lines.length; i++) {
          if (lines[i].toLowerCase().includes(`[[${titleLower}`)) {
            const start = Math.max(0, i - 1);
            const end = Math.min(lines.length, i + 2);
            context = lines.slice(start, end).join(' ').trim();
            break;
          }
        }
        backlinks.push({
          path: path.relative(VAULT_PATH, filePath),
          title,
          context: context || body.slice(0, 100) + '...',
          modified: fs.statSync(filePath).mtime.toISOString().split('T')[0]
        });
      }
    } catch (_) {}
  }

  return {
    note_title: noteTitle,
    note_found: true,
    note_path: targetNote.path,
    backlink_count: backlinks.length,
    backlinks
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: get_backlinks.js \'{...}\'', required: ['note_title'], optional: [] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const noteTitle = resolveInput(input, 'note_title', 'title', 'noteTitle');
  const result = getBacklinks(noteTitle);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
