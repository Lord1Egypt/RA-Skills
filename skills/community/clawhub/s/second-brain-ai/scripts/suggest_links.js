#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { VAULT_PATH, readVaultDir, parseFrontmatter, extractWikiLinks, extractTags, resolveInput } = require('./lib/common');

function suggestLinks(title, content = null, limit = 5) {
  if (!title) return { error: 'Title is required' };
  if (!fs.existsSync(VAULT_PATH)) {
    return { error: `Vault not found: ${VAULT_PATH}` };
  }

  const files = readVaultDir(VAULT_PATH);
  const titleLower = title.toLowerCase();
  let inputTags = [];
  let inputTerms = [];
  let existingLinks = [];

  if (content) {
    inputTags = extractTags(content);
    inputTerms = content.toLowerCase().split(/\s+/).filter(w => w.length > 3);
  } else {
    for (const filePath of files) {
      try {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const { frontmatter, body } = parseFrontmatter(fileContent);
        const fileTitle = frontmatter.title || path.basename(filePath, '.md');
        if (fileTitle.toLowerCase() === titleLower) {
          inputTags = [...(frontmatter.tags || []), ...extractTags(body)];
          inputTerms = body.toLowerCase().split(/\s+/).filter(w => w.length > 3);
          existingLinks = extractWikiLinks(fileContent);
          break;
        }
      } catch (_) {}
    }
  }

  const scored = [];
  for (const filePath of files) {
    try {
      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter, body } = parseFrontmatter(fileContent);
      const fileTitle = frontmatter.title || path.basename(filePath, '.md');
      if (fileTitle.toLowerCase() === titleLower) continue;
      if (existingLinks.some(l => l.toLowerCase() === fileTitle.toLowerCase())) continue;

      let score = 0;
      const reasons = [];
      const sharedTags = [];

      const noteTags = [...(frontmatter.tags || []), ...extractTags(body)];
      for (const tag of inputTags) {
        if (noteTags.includes(tag)) {
          score += 30;
          sharedTags.push(tag);
        }
      }
      if (sharedTags.length > 0) reasons.push('shared-tags');

      const bodyLower = body.toLowerCase();
      let termMatches = 0;
      for (const term of inputTerms) {
        if (bodyLower.includes(term)) termMatches++;
      }
      if (termMatches > 0) {
        score += Math.min(termMatches * 3, 30);
        reasons.push('content-match');
      }

      if (inputTerms.some(t => fileTitle.toLowerCase().includes(t))) {
        score += 20;
        reasons.push('title-match');
      }

      if (score > 0) {
        const confidence = Math.min(score / 50, 1);
        scored.push({
          note_title: fileTitle,
          note_path: path.relative(VAULT_PATH, filePath),
          reason: reasons.join(', '),
          confidence: parseFloat(confidence.toFixed(2)),
          shared_tags: sharedTags.slice(0, 5),
          score
        });
      }
    } catch (_) {}
  }

  scored.sort((a, b) => b.score - a.score);
  const suggestions = scored.slice(0, limit).map(({ score, ...rest }) => rest);

  return {
    title,
    suggestions,
    total: suggestions.length
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: suggest_links.js \'{...}\'', required: ['title'], optional: ['content', 'limit'] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const title = resolveInput(input, 'title', 'note_title');
  const result = suggestLinks(title, input.content, input.limit || 5);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
