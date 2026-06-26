#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search short-form videos across the web.

Required:
  --query         Search query (e.g. "funny cat")

Optional:
  --count         Max results to fetch (default: 50)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --time          Time filter: any (default), day, week, month, year
  --date-from     Posted date from (e.g. 1/19/2025)
  --date-to       Posted date to (e.g. 3/19/2025)
  --high-quality  Filter high quality only (true/false)
  --closed-captioned  Filter closed captioned only (true/false)
  --dry-run       Fetch first page only, print to console
  --max-calls     Safety cap on API calls (default: 50)
  --help          Show this help
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
    const meta = loadMeta('realtime-shorts-search');
    const host = meta.rapidapi_host || 'real-time-shorts-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-shorts-search_${ts}.${format}`);

    const params = { query: args.query };
    if (args.time) params.time = args.time;
    if (args.dateFrom) params.posted_date_from = args.dateFrom;
    if (args.dateTo) params.posted_date_to = args.dateTo;
    if (args.highQuality) params.high_quality = args.highQuality;
    if (args.closedCaptioned) params.closed_captioned = args.closedCaptioned;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize: 20,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} shorts in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-shorts-search', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
