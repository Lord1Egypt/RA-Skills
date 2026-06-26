#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search forums and discussions across the web (Google Forums tab).

Required:
  --query             Search query (e.g. "best ergonomic keyboard")

Optional:
  --count             Max results (default: 50)
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --country           Country code (default: us)
  --language          Language code (default: en)
  --time              Time filter: any | hour | day | week | month | year (default: any)
  --dry-run           Fetch first page only, print to console
  --max-calls         Safety cap on API calls (default: 20)
  --help              Show this help
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
    const meta = loadMeta('realtime-forums-search');
    const host = meta.rapidapi_host || 'real-time-forums-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 20;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `forums-search_${ts}.${format}`);

    const params = {
        query: args.query,
        country: args.country || 'us',
        language: args.language || 'en',
    };
    if (args.time && args.time !== 'any') params.time = args.time;

    // Offset-based pagination using 'start' param
    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'offset', offsetParam: 'start', pageSize: 10,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} forum results in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-forums-search', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
