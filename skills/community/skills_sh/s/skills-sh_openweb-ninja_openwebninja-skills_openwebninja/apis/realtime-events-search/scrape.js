#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search for local public events or fetch event details.

Endpoints:
  /search-events    Search events (default, requires --query)
  /event-details    Get event details (requires --event-id)

Required (varies by endpoint):
  --query           Search query (e.g. "Concerts in San Francisco")
  --event-id        Event ID for /event-details

Optional:
  --endpoint        Endpoint (default: /search-events)
  --count           Max results to fetch (default: 30)
  --date            Date filter: any, today, tomorrow, week, weekend, next_week, month, next_month
  --is-virtual      true | false — filter for virtual events (default: false)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
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

    const endpoint = args.endpoint || '/search-events';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-events-search');
    const host = meta.rapidapi_host || 'real-time-events-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 30;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-events-search_${ts}.${format}`);

    // ── /event-details (single call, no pagination) ──────────────────────────
    if (endpoint === '/event-details') {
        if (!args.eventId) { console.error('Error: --event-id required for /event-details'); process.exit(1); }
        const params = { event_id: args.eventId };
        const data = await apiCall(host, '/event-details', params, apiKey);
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-events-search', endpoint: '/event-details', totalCalls: 1 });
        return;
    }

    // ── /search-events (offset-based pagination via 'start') ─────────────────
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query };
    if (args.date) params.date = args.date;
    if (args.isVirtual) params.is_virtual = args.isVirtual;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search-events', params, apiKey, count,
        pagination: 'offset', offsetParam: 'start', pageSize: 10,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} results in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-events-search', endpoint: '/search-events', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
