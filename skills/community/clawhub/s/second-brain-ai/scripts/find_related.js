#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { VAULT_PATH, readVaultDir, parseFrontmatter, extractWikiLinks, extractTags, resolveInput } = require('./lib/common');

function findRelated(topic, limit = 5) {
  if (!topic || typeof topic !== 'string') {
    return { error: 'Missing required field: topic' };
  }
  if (!fs.existsSync(VAULT_PATH)) {
    return { error: `Vault not found: ${VAULT_PATH}` };
  }

  const files = readVaultDir(VAULT_PATH);
  const topicLower = topic.toLowerCase();
  const topicTerms = topicLower.split(/\s+/).filter(Boolean);
  const topicNotes = [];
  const related = [];

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter } = parseFrontmatter(content);
      const title = frontmatter.title || path.basename(filePath, '.md');
      if (topicTerms.some(t => title.toLowerCase().includes(t))) {
        topicNotes.push({
          path: path.relative(VAULT_PATH, filePath),
          title,
          relation: 'topic-match'
        });
      }
    } catch (_) {}
  }

  const topicTitles = new Set(topicNotes.map(n => n.title.toLowerCase()));

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter, body } = parseFrontmatter(content);
      const title = frontmatter.title || path.basename(filePath, '.md');
      if (topicTitles.has(title.toLowerCase())) continue;

      const links = extractWikiLinks(content);
      const tags = new Set([...(frontmatter.tags || []), ...extractTags(body)]);
      const lower = content.toLowerCase();
      let score = 0;
      const relations = [];

      for (const topicNote of topicNotes) {
        if (links.some(l => l.toLowerCase() === topicNote.title.toLowerCase())) {
          score += 40;
          relations.push('links-to');
          break;
        }
      }

      if (topicTerms.some(t => lower.includes(t))) {
        score += 20;
        relations.push('mentions');
      }

      for (const topicNote of topicNotes) {
        try {
          const noteContent = fs.readFileSync(path.join(VAULT_PATH, topicNote.path), 'utf-8');
          const { frontmatter: noteFm, body: noteBody } = parseFrontmatter(noteContent);
          const noteTags = new Set([...(noteFm.tags || []), ...extractTags(noteBody)]);
          const shared = [...tags].filter(tag => noteTags.has(tag));
          if (shared.length > 0) {
            score += shared.length * 15;
            relations.push('shared-tags');
            break;
          }
        } catch (_) {}
      }

      if (score > 0) {
        related.push({
          path: path.relative(VAULT_PATH, filePath),
          title,
          relation: [...new Set(relations)].join(', '),
          score
        });
      }
    } catch (_) {}
  }

  related.sort((a, b) => b.score - a.score);

  return {
    topic,
    topic_notes: topicNotes,
    related_notes: related.slice(0, limit),
    total: topicNotes.length + related.length
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: find_related.js \'{...}\'', required: ['topic'], optional: ['limit'] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const topic = resolveInput(input, 'topic', 'title', 'note_title', 'query', 'q');
  const result = findRelated(topic, input.limit || 5);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
