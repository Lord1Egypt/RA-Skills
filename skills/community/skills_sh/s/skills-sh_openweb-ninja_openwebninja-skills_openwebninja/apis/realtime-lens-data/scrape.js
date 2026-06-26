#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, toCSV, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --url <image_url> [options]

Reverse image search, visual matches, exact matches, object detection, and OCR via Google Lens.

Required:
  --url           URL of an image to search / analyze

Optional:
  --endpoint      /search (default), /visual-matches, /exact-matches, /object-detection, /ocr
  --query         Additional text query to refine results (for /search, /visual-matches)
  --count         Limit for /exact-matches (default: 500, max: 500)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country code (default: us)
  --language      Language code (default: en)
  --safe-search   Safe search for /exact-matches: off, blur (default: blur)
  --dry-run       Print results to console only
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

    if (!args.url) { console.error('Error: --url required. Use --help for usage.'); process.exit(1); }

    const endpoint = args.endpoint || '/search';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-lens-data');
    const host = meta.rapidapi_host || 'real-time-lens-data.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const safeEndpoint = endpoint.replace(/\//g, '_');
    const outputPath = args.output || path.join('output', `realtime-lens-data${safeEndpoint}_${ts}.${format}`);

    // ── Image Search (/search) ────────────────────────────────────────────────
    if (endpoint === '/search') {
        const params = { url: args.url, language: args.language || 'en', country: args.country || 'us' };
        if (args.query) params.query = args.query;
        const data = await apiCall(host, '/search', params, apiKey);
        // data.data is an object with sub-arrays: organic_results, visual_matches, knowledge_graph, related_searches
        const d = data.data || data;
        const records = Array.isArray(d.organic_results) ? d.organic_results
            : Array.isArray(d.visual_matches) ? d.visual_matches
            : Array.isArray(d) ? d : [d];
        console.error(`${records.length} result(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-lens-data', endpoint: '/search', totalCalls: 1 });
        return;
    }

    // ── Visual Matches (/visual-matches) ──────────────────────────────────────
    if (endpoint === '/visual-matches') {
        const params = { url: args.url, language: args.language || 'en', country: args.country || 'us' };
        if (args.query) params.query = args.query;
        const data = await apiCall(host, '/visual-matches', params, apiKey);
        // data.data may be an array of matches directly, or an object with visual_matches key
        const d = data.data || data;
        const records = Array.isArray(d) ? d : (Array.isArray(d.visual_matches) ? d.visual_matches : [d]);
        console.error(`${records.length} visual match(es) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-lens-data', endpoint: '/visual-matches', totalCalls: 1 });
        return;
    }

    // ── Exact Matches (/exact-matches) ────────────────────────────────────────
    if (endpoint === '/exact-matches') {
        const count = Math.min(parseInt(args.count, 10) || 500, 500);
        const params = { url: args.url, limit: String(count) };
        if (args.safeSearch) params.safe_search = args.safeSearch;
        const data = await apiCall(host, '/exact-matches', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} exact match(es) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-lens-data', endpoint: '/exact-matches', totalCalls: 1 });
        return;
    }

    // ── Object Detection (/object-detection) ──────────────────────────────────
    if (endpoint === '/object-detection') {
        const params = { url: args.url };
        const data = await apiCall(host, '/object-detection', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} detection(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-lens-data', endpoint: '/object-detection', totalCalls: 1 });
        return;
    }

    // ── OCR (/ocr) ────────────────────────────────────────────────────────────
    if (endpoint === '/ocr') {
        const params = { url: args.url };
        if (args.language) params.language = args.language;
        const data = await apiCall(host, '/ocr', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} text block(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-lens-data', endpoint: '/ocr', totalCalls: 1 });
        return;
    }

    console.error(`Error: unknown endpoint "${endpoint}". Use --help for usage.`);
    process.exit(1);
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
