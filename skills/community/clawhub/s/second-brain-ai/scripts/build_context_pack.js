#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { VAULT_PATH, readVaultDir, parseFrontmatter, extractWikiLinks, extractTags, resolveInput } = require('./lib/common');

function buildContextPack(topic, limit = 10) {
  if (!topic || typeof topic !== 'string') {
    return { error: 'Missing required field: topic' };
  }
  if (!fs.existsSync(VAULT_PATH)) {
    return { error: `Vault not found: ${VAULT_PATH}` };
  }

  const files = readVaultDir(VAULT_PATH);
  const topicLower = topic.toLowerCase();
  const topicTerms = topicLower.split(/\s+/).filter(Boolean);
  const scoredNotes = [];
  const allTags = new Map();

  for (const filePath of files) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      const { frontmatter, body } = parseFrontmatter(content);
      const title = frontmatter.title || path.basename(filePath, '.md');
      const contentLower = content.toLowerCase();
      let score = 0;

      for (const term of topicTerms) {
        if (title.toLowerCase().includes(term)) score += 25;
        const matches = contentLower.match(new RegExp(term, 'g'));
        if (matches) score += matches.length * 3;
      }

      const tags = [...(frontmatter.tags || []), ...extractTags(body)];
      for (const tag of tags) {
        allTags.set(tag, (allTags.get(tag) || 0) + 1);
        if (topicTerms.some(t => tag.toLowerCase().includes(t))) score += 15;
      }

      const stat = fs.statSync(filePath);
      const days = (Date.now() - stat.mtime.getTime()) / (1000 * 60 * 60 * 24);
      if (days < 30) score += 5;
      if (days < 7) score += 5;

      if (score > 0) {
        scoredNotes.push({
          path: path.relative(VAULT_PATH, filePath),
          title,
          type: frontmatter.type || 'note',
          score,
          tags: tags.slice(0, 10),
          links: extractWikiLinks(content),
          snippet: body.slice(0, 200).replace(/\n/g, ' ') + '...'
        });
      }
    } catch (_) {}
  }

  scoredNotes.sort((a, b) => b.score - a.score);
  const topNotes = scoredNotes.slice(0, limit);

  const conceptCounts = {};
  for (const note of topNotes) {
    for (const tag of note.tags) conceptCounts[tag] = (conceptCounts[tag] || 0) + 1;
    for (const link of note.links) conceptCounts[link] = (conceptCounts[link] || 0) + 1;
  }

  const keyConcepts = Object.entries(conceptCounts)
    .filter(([name]) => !topicLower.includes(name.toLowerCase()))
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name]) => name);

  const summary = topNotes.length > 0
    ? `Found ${scoredNotes.length} related notes. Top ${topNotes.length} cover: ${keyConcepts.slice(0, 5).join(', ') || 'various topics'}.`
    : `No notes found related to "${topic}".`;

  return {
    topic,
    summary,
    related_notes: topNotes.map(n => ({
      path: n.path,
      title: n.title,
      type: n.type,
      snippet: n.snippet,
      tags: n.tags.slice(0, 5),
      score: Math.round(n.score)
    })),
    key_concepts: keyConcepts,
    stats: {
      total_notes: files.length,
      related_found: scoredNotes.length,
      returned: topNotes.length
    }
  };
}

const args = process.argv.slice(2);
if (args.length === 0) {
  console.log(JSON.stringify({ error: 'Usage: build_context_pack.js \'{...}\'', required: ['topic'], optional: ['limit'] }, null, 2));
  process.exit(1);
}

try {
  const input = JSON.parse(args[0]);
  const topic = resolveInput(input, 'topic', 'query', 'title', 'q');
  const result = buildContextPack(topic, input.limit || 10);
  console.log(JSON.stringify(result, null, 2));
  if (result.error) process.exit(1);
} catch (e) {
  console.log(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
}
