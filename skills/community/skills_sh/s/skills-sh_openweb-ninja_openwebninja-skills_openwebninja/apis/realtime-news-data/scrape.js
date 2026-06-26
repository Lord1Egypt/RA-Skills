#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search and fetch news articles, headlines, and topic coverage.

Required (varies by endpoint):
  --query         Search query (for /search, /local-headlines)
  --topic         Topic name (for /topic-headlines, /topic-news-by-section): WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SPORTS, SCIENCE, HEALTH

Optional:
  --endpoint      Endpoint: /search (default), /top-headlines, /topic-headlines, /topic-news-by-section, /local-headlines
  --count         Max results (default: 50)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country code, e.g. us, gb, de (default: us)
  --language      Language code, e.g. en, es, fr (default: en)
  --time          Time filter for /search: anytime, 1h, 24h, 7d, 30d, y (default: anytime)
  --source        Source domain filter for /search (e.g. cnn.com)
  --section       Section token for /topic-news-by-section
  --dry-run       Fetch once only, print to console
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
    const meta = loadMeta('realtime-news-data');
    const host = meta.rapidapi_host || 'real-time-news-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const country = args.country || 'us';
    const language = args.language || 'en';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-news-data_${ts}.${format}`);

    // ── Top Headlines (single call) ──────────────────────────────────────────
    if (endpoint === '/top-headlines') {
        const params = { limit: count, country, language };
        const data = await apiCall(host, '/top-headlines', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-news-data', endpoint: '/top-headlines', totalCalls: 1 });
        return;
    }

    // ── Topic Headlines (single call) ────────────────────────────────────────
    if (endpoint === '/topic-headlines') {
        if (!args.topic) { console.error('Error: --topic required for /topic-headlines'); process.exit(1); }
        const params = { topic: args.topic, limit: count, country, language };
        const data = await apiCall(host, '/topic-headlines', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-news-data', endpoint: '/topic-headlines', topic: args.topic, totalCalls: 1 });
        return;
    }

    // ── Topic News By Section (single call) ──────────────────────────────────
    if (endpoint === '/topic-news-by-section') {
        if (!args.topic) { console.error('Error: --topic required for /topic-news-by-section'); process.exit(1); }
        const params = { topic: args.topic, limit: count, country, language };
        if (args.section) params.section = args.section;
        const data = await apiCall(host, '/topic-news-by-section', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-news-data', endpoint: '/topic-news-by-section', topic: args.topic, totalCalls: 1 });
        return;
    }

    // ── Local Headlines (single call) ────────────────────────────────────────
    if (endpoint === '/local-headlines') {
        if (!args.query) { console.error('Error: --query required for /local-headlines'); process.exit(1); }
        const params = { query: args.query, limit: count, country, language };
        const data = await apiCall(host, '/local-headlines', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-news-data', endpoint: '/local-headlines', query: args.query, totalCalls: 1 });
        return;
    }

    // ── Search (default, single call with limit) ─────────────────────────────
    if (!args.query) { console.error('Error: --query required for /search. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query, limit: count, country, language };
    if (args.time) params.time_published = args.time;
    if (args.source) params.source = args.source;

    const data = await apiCall(host, '/search', params, apiKey);
    const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);

    console.error(`${records.length} articles in 1 call.`);
    if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
    writeOutput(records, outputPath, format, { api: 'realtime-news-data', endpoint: '/search', query: args.query, totalCalls: 1 });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
