#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { VAULT_PATH, readVaultDir, parseFrontmatter, requireWriteApproval } = require('./lib/common');

function findNoteFile(title) {
  if (!fs.existsSync(VAULT_PATH)) return null;
  const files = readVaultDir(VAULT_PATH);
  const titleLower = title.toLowerCase();
  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter } = parseFrontmatter(content);
      const fileTitle = frontmatter.title || path.basename(filePath, '.md');
      if (fileTitle.toLowerCase() === titleLower) return filePath;
    } catch (_) {}
  }
  return null;
}

function updateFrontmatterUpdated(content, updated) {
  if (/^---\n[\s\S]*?\n---/m.test(content)) {
    if (/^(---\n[\s\S]*?)^updated: [^\n]+/m.test(content)) {
      return content.replace(/^(---\n[\s\S]*?)^updated: [^\n]+/m, `$1updated: ${updated}`);
    }
    return content.replace(/^---\n/, `---\nupdated: ${updated}\n`);
  }
  return content;
}

function buildAppendBlock(data) {
  const nowIso = new Date().toISOString();
  const appendedBy = data.appended_by || data.by || data.author || data.actor;
  if (!appendedBy || typeof appendedBy !== 'string' || !appendedBy.trim()) {
    return { error: 'Missing required field: appended_by' };
  }
  const marker = [
    '> Append Record',
    `> Added by: ${appendedBy.trim()}`,
    ...(data.timestamp !== false ? [`> Added at: ${nowIso}`] : []),
    '',
    data.content.trim(),
    ''
  ].join('\n');
  const block = data.section
    ? `\n\n## ${data.section}\n\n${marker}\n`
    : `\n\n---\n\n${marker}\n`;
  return { block, appendedBy: appendedBy.trim(), addedAt: nowIso };
}

function appendNote(data) {
  requireWriteApproval(data, 'allow_write');
  if (!data.title) return { error: 'Missing required field: title' };
  if (!data.content) return { error: 'Missing required field: content' };
  if (!fs.existsSync(VAULT_PATH)) return { error: `Vault not found: ${VAULT_PATH}` };

  const filePath = findNoteFile(data.title);
  if (!filePath) return { error: `Note not found: ${data.title}` };

  const append = buildAppendBlock(data);
  if (append.error) return { error: append.error };

  let content = fs.readFileSync(filePath, 'utf-8').replace(/\s*$/, '');
  content += append.block;
  content = updateFrontmatterUpdated(content, new Date().toISOString().split('T')[0]);
  fs.writeFileSync(filePath, content, 'utf-8');

  return {
    status: 'success',
    path: path.relative(VAULT_PATH, filePath),
    title: data.title,
    action: 'appended',
    section_added: data.section || null,
    appended_by: append.appendedBy,
    added_at: append.addedAt,
    attribution_required: true
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: append_note.js \'{...}\'', required: ['title', 'content', 'allow_write', 'appended_by'], optional: ['section', 'timestamp'] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const result = appendNote(input);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
