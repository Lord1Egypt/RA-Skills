#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search for books via Google Books and export results.

Required:
  --query           Search query (e.g. "good thriller")

Optional:
  --count           Max results to fetch (default: 30)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --document-type   any | books | newspapers | magazines (default: any)
  --view-type       any | preview_and_full_view | full_view (default: any)
  --year-from       Publication year from (e.g. 2020)
  --year-to         Publication year to (e.g. 2025)
  --country         Country code (default: us)
  --language        Language code (default: en)
  --dry-run         Fetch first page only, print to console
  --max-calls       Safety cap on API calls (default: 50)
  --help            Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg.startsWith('--') && i + 1 < argv.length) {
            const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
            args[key] = argv[++i];
        }
    }
    return args;
}

async function main() {
    const args = parseArgs(process.argv);
    if (args.help) { printHelp(); process.exit(0); }

    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const apiKey = getApiKey();
    const meta = loadMeta('realtime-books-data');
    const host = meta.rapidapi_host || 'real-time-books-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 30;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-books-data_${ts}.${format}`);

    const params = { query: args.query, country: args.country || 'us', language: args.language || 'en' };
    if (args.documentType) params.document_type = args.documentType;
    if (args.viewType) params.view_type = args.viewType;
    if (args.yearFrom) params.publication_year_from = args.yearFrom;
    if (args.yearTo) params.publication_year_to = args.yearTo;

    // Page-based pagination (param: page, starts at 1)
    const pageSize = 10;
    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} results in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-books-data', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
