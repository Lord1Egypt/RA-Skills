#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --endpoint <endpoint> [options]

Scrape Google Play Store app data: search, reviews, details, charts, and categories.

Endpoints:
  /search              Search for apps (requires --query)
  /app-reviews         Get app reviews (requires --app-id)
  /app-details         Get full app details (requires --app-id, supports comma-separated batch)
  /categories          List all Play Store categories
  /top-grossing-apps   Top grossing apps chart
  /top-paid-apps       Top paid apps chart
  /top-free-apps       Top free apps chart
  /top-free-games      Top free games chart
  /top-grossing-games  Top grossing games chart
  /top-paid-games      Top paid games chart

Required (varies by endpoint):
  --query         Search query (for /search)
  --app-id        App ID, e.g. com.snapchat.android (for /app-reviews, /app-details)

Optional:
  --endpoint      Endpoint (default: /search)
  --count         Max results to fetch (default: 50)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --region        Region code (default: us)
  --language      Language code (default: en)
  --category      Play Store category for chart endpoints (e.g. SOCIAL)
  --sort-by       Sort reviews: MOST_RELEVANT, NEWEST, RATING (default: MOST_RELEVANT)
  --device        Device filter for reviews: PHONE, TABLET, CHROMEBOOK (default: PHONE)
  --rating        Rating filter for reviews: ANY, ONE_STAR, TWO_STARS, etc. (default: ANY)
  --dry-run       Print results to console only
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
    const meta = loadMeta('play-store-apps');
    const host = meta.rapidapi_host || 'store-apps.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const safeEndpoint = endpoint.replace(/\//g, '_');
    const outputPath = args.output || path.join('output', `play-store-apps${safeEndpoint}_${ts}.${format}`);

    const region = (args.region || 'us').toUpperCase();
    const language = (args.language || 'en').toUpperCase();

    // ── App Details (single call, supports batch) ─────────────────────────────
    if (endpoint === '/app-details') {
        if (!args.appId) { console.error('Error: --app-id required for /app-details'); process.exit(1); }
        const params = { app_id: args.appId, region, language };
        const data = await apiCall(host, '/app-details', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} app(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'play-store-apps', endpoint: '/app-details', totalCalls: 1 });
        return;
    }

    // ── Categories (single call) ──────────────────────────────────────────────
    if (endpoint === '/categories') {
        const data = await apiCall(host, '/categories', {}, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} category(ies) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 10), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'play-store-apps', endpoint: '/categories', totalCalls: 1 });
        return;
    }

    // ── Chart endpoints (single call, no pagination) ──────────────────────────
    const chartEndpoints = ['/top-grossing-apps', '/top-paid-apps', '/top-free-apps', '/top-free-games', '/top-grossing-games', '/top-paid-games'];
    if (chartEndpoints.includes(endpoint)) {
        const params = { limit: String(count), region, language };
        if (args.category) params.category = args.category;
        const data = await apiCall(host, endpoint, params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} app(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'play-store-apps', endpoint, totalCalls: 1 });
        return;
    }

    // ── App Reviews (cursor-based pagination) ─────────────────────────────────
    if (endpoint === '/app-reviews') {
        if (!args.appId) { console.error('Error: --app-id required for /app-reviews'); process.exit(1); }
        const pageSize = Math.min(count, 20);
        const params = { app_id: args.appId, limit: String(pageSize), region, language };
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.device) params.device = args.device;
        if (args.rating) params.rating = args.rating;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/app-reviews', params, apiKey, count,
            pagination: 'cursor', cursorParam: 'cursor', cursorPath: 'cursor',
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });

        console.error(`${results.length} review(s) in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'play-store-apps', endpoint: '/app-reviews', appId: args.appId, totalCalls: totalCallsMade });
        return;
    }

    // ── Search (cursor-based pagination) ──────────────────────────────────────
    if (endpoint === '/search') {
        if (!args.query) { console.error('Error: --query required for /search'); process.exit(1); }
        const params = { q: args.query, region: args.region || 'us', language: args.language || 'en' };

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/search', params, apiKey, count,
            pagination: 'cursor', cursorParam: 'cursor', cursorPath: 'data.cursor',
            resultsPath: 'data.apps', dryRun, delay: 300, maxCalls,
        });

        console.error(`${results.length} app(s) in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'play-store-apps', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
        return;
    }

    console.error(`Error: unknown endpoint "${endpoint}". Use --help for usage.`);
    process.exit(1);
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
