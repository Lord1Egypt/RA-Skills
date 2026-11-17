#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { statePaths } from './state-path.mjs';

const paths = statePaths();
if (!fs.existsSync(paths.articles)) {
  throw new Error('Readworthy state is not initialized. Run node scripts/init_state_v2.mjs first.');
}

const articleFiles = fs.readdirSync(paths.articles).filter((name) => name.endsWith('.json')).sort();
const entries = articleFiles
  .map((name) => JSON.parse(fs.readFileSync(path.join(paths.articles, name), 'utf8')))
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

const index = {
  schema_version: 2,
  generated_at: new Date().toISOString(),
  article_count: entries.length,
  articles: entries,
  a_articles: entries.filter((entry) => entry.recommendation === 'A').map((entry) => entry.id),
  a_ranking: {
    status: 'not_materialized',
    article_ids: [],
    ordering_rule: 'Compute expected cognitive gain versus reading cost when requested',
  },
};

const temporaryPath = `${paths.index}.tmp`;
fs.writeFileSync(temporaryPath, `${JSON.stringify(index, null, 2)}\n`);
fs.renameSync(temporaryPath, paths.index);
console.log(JSON.stringify({ ok: true, state_dir: paths.stateDir, article_count: entries.length }));
