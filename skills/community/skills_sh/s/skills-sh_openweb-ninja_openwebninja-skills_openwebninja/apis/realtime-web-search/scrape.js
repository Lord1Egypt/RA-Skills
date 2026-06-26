#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search the web via Google and export results.

Required:
  --query         Search query (e.g. "best CRM software 2025")

Optional:
  --endpoint      Endpoint: /search (default), /search-light, /ai-mode, /ai-overviews
  --count         Max results to fetch (default: 30)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country/geo code, e.g. us, gb, de (default: us)
  --language      Language code, e.g. en, es, fr (default: en)
  --num           Results per page for /search (default: 10, max: 100)
  --tbs           Time-based search filter (e.g. qdr:d for past day, qdr:w for past week)
  --location      Location string for local results
  --device        desktop | mobile (default: desktop)
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
    const meta = loadMeta('realtime-web-search');
    const host = meta.rapidapi_host || 'real-time-web-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 30;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-web-search_${ts}.${format}`);

    // ── AI Mode (single call, no pagination) ─────────────────────────────────
    if (endpoint === '/ai-mode') {
        if (!args.query) { console.error('Error: --query required for /ai-mode'); process.exit(1); }
        const params = { prompt: args.query, gl: args.country || 'us', hl: args.language || 'en' };
        if (args.sessionToken) params.session_token = args.sessionToken;
        const data = await apiCall(host, '/ai-mode', params, apiKey, 'GET', null, 'realtime-web-search');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-web-search', endpoint: '/ai-mode', totalCalls: 1 });
        return;
    }

    // ── AI Overviews (single call, no pagination) ────────────────────────────
    if (endpoint === '/ai-overviews') {
        if (!args.query) { console.error('Error: --query required for /ai-overviews'); process.exit(1); }
        const params = { q: args.query, gl: args.country || 'us', hl: args.language || 'en' };
        const data = await apiCall(host, '/ai-overviews', params, apiKey, 'GET', null, 'realtime-web-search');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-web-search', endpoint: '/ai-overviews', query: args.query, totalCalls: 1 });
        return;
    }

    // ── Light Search (single call, no pagination) ────────────────────────────
    if (endpoint === '/search-light') {
        if (!args.query) { console.error('Error: --query required for /search-light'); process.exit(1); }
        const params = { q: args.query, limit: String(count) };
        const data = await apiCall(host, '/search-light', params, apiKey, 'GET', null, 'realtime-web-search');
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-web-search', endpoint: '/search-light', query: args.query, totalCalls: 1 });
        return;
    }

    // ── Full Search (offset-based pagination) ────────────────────────────────
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const numPerPage = parseInt(args.num, 10) || 10;
    const params = { q: args.query, num: numPerPage, gl: args.country || 'us', hl: args.language || 'en' };
    if (args.tbs) params.tbs = args.tbs;
    if (args.location) params.location = args.location;
    if (args.device) params.device = args.device;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'offset', offsetParam: 'start', pageSize: numPerPage,
        resultsPath: 'data', dryRun, delay: 300, maxCalls, apiId: 'realtime-web-search',
    });

    console.error(`${results.length} results in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-web-search', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
