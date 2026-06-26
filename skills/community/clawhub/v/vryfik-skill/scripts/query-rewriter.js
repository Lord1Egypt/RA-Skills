#!/usr/bin/env node
'use strict';

/**
 * Query Rewriter — Expands a single query into targeted sub-queries
 *
 * ClawHub Security: NO network access. NO file system writes.
 * Pure synchronous computation. Deterministic output.
 *
 * Input  JSON: { intent, query, entities, lang }
 * Output JSON: { subQueries: string[], strategy: string, estimatedLayers: string[] }
 */

// ---------------------------------------------------------------------------
// Expansion templates per intent
// ---------------------------------------------------------------------------
const TEMPLATES = {
  code_search: [
    q => q,
    q => `${q} example`,
    q => `${q} implementation`,
    q => `how to use ${q}`,
    q => `${q} best practice`
  ],
  file_search: [
    q => q,
    q => `"${q}"`,          // exact phrase for ripgrep
    q => q.replace(/\s+/g, '_'),   // snake_case variant
    q => q.replace(/\s+/g, '-')    // kebab-case variant
  ],
  doc_search: [
    q => `${q} documentation`,
    q => `${q} reference`,
    q => `${q} API`,
    q => `${q} guide`
  ],
  web_search: [
    q => q,
    q => `${q} site:stackoverflow.com`,
    q => `${q} site:github.com`
  ],
  api_search: [
    q => `${q} endpoint`,
    q => `${q} REST API`,
    q => `${q} OpenAPI spec`,
    q => `${q} request response example`
  ]
};

// ---------------------------------------------------------------------------
// Strategy matrix: maps intent → recommended layer order
// ---------------------------------------------------------------------------
const STRATEGY_MAP = {
  file_search:  { strategy: 'l1_only',        estimatedLayers: ['l1'] },
  code_search:  { strategy: 'l1_then_l2',     estimatedLayers: ['l1', 'l2'] },
  doc_search:   { strategy: 'l2_then_l3',     estimatedLayers: ['l2', 'l3'] },
  api_search:   { strategy: 'l2_then_l3',     estimatedLayers: ['l2', 'l3'] },
  web_search:   { strategy: 'l3_only',        estimatedLayers: ['l3'] }
};

// ---------------------------------------------------------------------------
// Chinese → English keyword bridging for mixed-language queries
// ---------------------------------------------------------------------------
const ZH_EN_BRIDGE = {
  '组件': 'component',
  '函数': 'function',
  '方法': 'method',
  '接口': 'interface',
  '用法': 'usage',
  '示例': 'example',
  '实现': 'implementation',
  '文档': 'documentation',
  '参数': 'parameter',
  '返回值': 'return value'
};

function bridgeZhTerms(query) {
  let result = query;
  for (const [zh, en] of Object.entries(ZH_EN_BRIDGE)) {
    result = result.replace(new RegExp(zh, 'g'), `${zh} ${en}`);
  }
  return result;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function rewrite(input) {
  const { intent = 'web_search', query = '', lang = 'en' } = input;

  if (!query.trim()) {
    return { error: 'Empty query' };
  }

  // Bridge Chinese terms when lang is zh
  const base = lang === 'zh' ? bridgeZhTerms(query) : query;

  const templates = TEMPLATES[intent] || TEMPLATES.web_search;

  // Generate sub-queries, deduplicate, cap at 5
  const seen = new Set();
  const subQueries = templates
    .map(fn => fn(base).trim())
    .filter(q => {
      if (seen.has(q)) return false;
      seen.add(q);
      return true;
    })
    .slice(0, 5);

  const strategyInfo = STRATEGY_MAP[intent] || STRATEGY_MAP.web_search;

  return {
    subQueries,
    ...strategyInfo,
    lang,
    originalQuery: query
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const arg = process.argv[2];

  if (arg) {
    try {
      console.log(JSON.stringify(rewrite(JSON.parse(arg))));
    } catch {
      console.log(JSON.stringify({ error: 'Invalid JSON input', received: arg }));
    }
    return;
  }

  if (!process.stdin.isTTY) {
    let buf = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', c => { buf += c; });
    process.stdin.on('end', () => {
      try {
        console.log(JSON.stringify(rewrite(JSON.parse(buf.trim()))));
      } catch {
        console.log(JSON.stringify({ error: 'Invalid JSON input' }));
      }
    });
    return;
  }

  console.error('Usage: node scripts/query-rewriter.js \'{"intent":"code_search","query":"Vue provide inject"}\'');
  process.exit(1);
}

main();
