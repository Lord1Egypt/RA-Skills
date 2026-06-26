#!/usr/bin/env node
/**
 * Capture a new note to the vault.
 */

const fs = require('fs');
const path = require('path');
const { VAULT_PATH, sanitizeFilename, buildFrontmatter, requireWriteApproval } = require('./lib/common');

const TYPE_FOLDERS = {
  idea: '02-Ideas',
  project: '03-Projects',
  person: '04-People',
  concept: '05-Concepts',
  reading: '06-Reading',
  daily: '01-Daily',
  moc: '07-MOCs',
  default: '00-Inbox'
};

function captureNote(data) {
  requireWriteApproval(data, 'allow_write');
  if (!data.title) return { error: 'Missing required field: title' };
  if (!fs.existsSync(VAULT_PATH)) return { error: `Vault not found: ${VAULT_PATH}` };

  const folderName = TYPE_FOLDERS[data.type] || TYPE_FOLDERS.default;
  const folderPath = path.join(VAULT_PATH, folderName);
  fs.mkdirSync(folderPath, { recursive: true });

  const frontmatter = buildFrontmatter(data);
  const body = data.content || '';
  const linksSection = data.links && data.links.length > 0
    ? '\n\n## Related\n\n' + data.links.map(l => `- [[${l}]]`).join('\n')
    : '';
  const fullContent = `${frontmatter}\n\n# ${data.title}\n\n${body}${linksSection}\n`;

  const datePrefix = new Date().toISOString().slice(0, 10);
  const filename = `${datePrefix}-${sanitizeFilename(data.title)}.md`;
  const filePath = path.join(folderPath, filename);

  if (fs.existsSync(filePath)) {
    return { error: `Note already exists: ${path.relative(VAULT_PATH, filePath)}` };
  }

  try {
    fs.writeFileSync(filePath, fullContent, 'utf-8');
    return {
      status: 'success',
      path: path.relative(VAULT_PATH, filePath),
      title: data.title,
      type: data.type || 'note'
    };
  } catch (e) {
    return { error: `Failed to write note: ${e.message}` };
  }
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: capture_note.js \'{...}\'', required: ['title', 'allow_write'], optional: ['content', 'type', 'tags', 'links'] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const result = captureNote(input);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
