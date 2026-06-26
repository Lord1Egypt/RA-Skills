#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Google Videos for real-time video results from across the web.

Required:
  --query         Search query (e.g. "react tutorial")

Optional:
  --count         Max results to fetch (default: 50)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country code, ISO 3166-1 alpha-2 (default: us)
  --language      Language code, ISO 639-1 (default: en)
  --time-period   any (default), last_hour, last_day, last_week, last_month, last_year
  --date-from     Custom range start, MM/DD/YYYY (use with --date-to)
  --date-to       Custom range end, MM/DD/YYYY (use with --date-from)
  --sort-by       relevance (default), date
  --duration      any (default), short (<4m), medium (4-20m), long (>20m)
  --safe          off (default), active
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
    const meta = loadMeta('realtime-video-search');
    const host = meta.rapidapi_host || 'real-time-video-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-video-search_${ts}.${format}`);

    const params = { query: args.query };
    if (args.country) params.country = args.country;
    if (args.language) params.language = args.language;
    if (args.timePeriod) params.time_period = args.timePeriod;
    if (args.dateFrom) params.date_from = args.dateFrom;
    if (args.dateTo) params.date_to = args.dateTo;
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.duration) params.duration = args.duration;
    if (args.safe) params.safe = args.safe;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize: 10,
        resultsPath: 'data.videos', dryRun, delay: 300, maxCalls,
        apiId: 'realtime-video-search',
    });

    console.error(`${results.length} videos in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-video-search', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
