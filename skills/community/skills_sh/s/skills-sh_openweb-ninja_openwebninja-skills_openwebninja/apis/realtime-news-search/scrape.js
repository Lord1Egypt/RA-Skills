#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Google News for any query and export real-time news results.

Required:
  --query         News search query (e.g. "artificial intelligence startups")

Optional:
  --endpoint      Endpoint: /search (default)
  --count         Max results to fetch (default: 50)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country code, e.g. us, gb, de (default: us)
  --language      Language code, e.g. en, es, fr (default: en)
  --time-period   Time filter: any, last_hour, last_day, last_week, last_month, last_year (default: any)
  --date-from     Custom range start MM/DD/YYYY (use with --date-to; not with --time-period)
  --date-to       Custom range end MM/DD/YYYY (use with --date-from)
  --sort-by       Sort order: relevance (default), date
  --safe          Safe search: off (default), active
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

    const endpoint = args.endpoint || '/search';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-news-search');
    const host = meta.rapidapi_host || 'real-time-news-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const country = args.country || 'us';
    const language = args.language || 'en';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-news-search_${ts}.${format}`);

    // ── Search (page-number pagination, 10 results/page) ─────────────────────
    if (!args.query) { console.error('Error: --query required for /search. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query, country, language };
    if (args.timePeriod) params.time_period = args.timePeriod;
    if (args.dateFrom) params.date_from = args.dateFrom;
    if (args.dateTo) params.date_to = args.dateTo;
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.safe) params.safe = args.safe;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint, params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize: 10,
        resultsPath: 'data.news', dryRun, delay: 300, maxCalls, apiId: 'realtime-news-search',
    });

    console.error(`${results.length} articles in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-news-search', endpoint, query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
