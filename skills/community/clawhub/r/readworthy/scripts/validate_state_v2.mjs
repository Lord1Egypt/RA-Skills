#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { isDeepStrictEqual } from 'node:util';
import { statePaths } from './state-path.mjs';

const paths = statePaths();
const allowedRecommendations = new Set(['A', 'B', 'C', 'D']);
const allowedEventKinds = new Set(['feedback', 'revision']);

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

for (const required of [paths.manifest, paths.profile, paths.index, paths.insights, paths.events, paths.articles]) {
  assert(fs.existsSync(required), `Missing state path: ${required}. Run init_state_v2.mjs first.`);
}

const manifest = readJson(paths.manifest);
const profile = readJson(paths.profile);
const index = readJson(paths.index);
const insights = readJson(paths.insights);
const articleFiles = fs.readdirSync(paths.articles).filter((name) => name.endsWith('.json')).sort();
const articles = articleFiles.map((name) => readJson(path.join(paths.articles, name)));
const eventLines = fs.readFileSync(paths.events, 'utf8').split('\n').filter(Boolean);
const events = eventLines.map((line, lineIndex) => {
  try {
    return JSON.parse(line);
  } catch (error) {
    throw new Error(`Invalid event JSON at line ${lineIndex + 1}: ${error.message}`);
  }
});

assert(manifest.schema_version === 2, 'Manifest must use schema_version 2');
assert(profile.schema_version === 2, 'Profile must use schema_version 2');
assert(index.schema_version === 2, 'Index must use schema_version 2');
assert(insights.schema_version === 2 && Array.isArray(insights.items), 'Insights must use schema_version 2 and items[]');
for (const key of ['topics', 'claims', 'preferences', 'decision_motive_library', 'narrative_exemplars']) {
  assert(Array.isArray(profile[key]), `Profile ${key} must be an array`);
}

const articleIds = articles.map((article) => article.id);
assert(new Set(articleIds).size === articleIds.length, 'Article ids must be unique');
for (const article of articles) {
  assert(article.schema_version === 2, `${article.id}: schema_version must be 2`);
  assert(article.metadata?.title && article.metadata?.url, `${article.id}: title and URL are required`);
  assert(/^[a-f0-9]{64}$/.test(article.content?.fingerprint_sha256 ?? ''), `${article.id}: invalid SHA-256 fingerprint`);
  assert(Array.isArray(article.analysis?.topics), `${article.id}: topics must be an array`);
  assert(Array.isArray(article.analysis?.claims), `${article.id}: claims must be an array`);
  assert(Array.isArray(article.analysis?.decision_tradeoffs), `${article.id}: decision_tradeoffs must be an array`);
  assert(allowedRecommendations.has(article.assessment?.current?.recommendation), `${article.id}: invalid recommendation`);
  assert(article.assessment.current.revision_id, `${article.id}: current revision id is required`);
  assert(Array.isArray(article.assessment?.history), `${article.id}: history must be an array`);
  assert(Array.isArray(article.feedback_ids), `${article.id}: feedback_ids must be an array`);
  for (const claim of article.analysis.claims) {
    assert(claim.knowledge, `${article.id}: every claim needs normalized knowledge`);
  }
}

const eventIds = events.map((event) => event.id);
assert(new Set(eventIds).size === eventIds.length, 'Event ids must be unique');
for (const event of events) {
  assert(event.schema_version === 2, `${event.id}: event schema_version must be 2`);
  assert(allowedEventKinds.has(event.event_kind), `${event.id}: invalid event kind`);
  assert(event.id && event.recorded_at, 'Every event needs id and recorded_at');
}

const expectedEntries = articles
  .map((article) => ({
    id: article.id,
    title: article.metadata.title,
    url: article.metadata.url,
    source_url: article.metadata.source_url ?? null,
    processed_at: article.metadata.processed_at,
    recommendation: article.assessment.current.recommendation,
    assessment_revision_id: article.assessment.current.revision_id,
    content_fingerprint_sha256: article.content.fingerprint_sha256,
  }))
  .sort((left, right) => `${left.processed_at}:${left.id}`.localeCompare(`${right.processed_at}:${right.id}`));

assert(index.article_count === articles.length, 'Index article_count is stale');
assert(isDeepStrictEqual(index.articles, expectedEntries), 'Index article entries are stale');
assert(isDeepStrictEqual(index.a_articles, expectedEntries.filter((entry) => entry.recommendation === 'A').map((entry) => entry.id)), 'A article index is stale');

console.log(JSON.stringify({
  ok: true,
  state_dir: paths.stateDir,
  articles: articles.length,
  events: events.length,
  feedback: events.filter((event) => event.event_kind === 'feedback').length,
  revisions: events.filter((event) => event.event_kind === 'revision').length,
  insights: insights.items.length,
}));
