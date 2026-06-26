#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --url <image-url> [options]

Find web pages containing a given image via reverse image search.

Required:
  --url           Publicly accessible URL of the image to search

Optional:
  --limit         Number of results to return (1–500, default: 500)
  --safe-search   Content filtering: off | blur (default: off)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --dry-run       Fetch data and print to console without saving
  --max-calls     Safety cap on API calls (default: 10)
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

    const apiKey = getApiKey();
    const meta = loadMeta('reverse-image-search');
    const host = meta.rapidapi_host || 'reverse-image-search3.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const limit = parseInt(args.limit, 10) || 500;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `reverse-image-search_${ts}.${format}`);

    if (!args.url) { console.error('Error: --url required. Use --help for usage.'); process.exit(1); }

    const params = { url: args.url, limit };
    if (args.safeSearch) params.safe_search = args.safeSearch;

    console.error(`Searching for pages containing image: ${args.url}`);
    const data = await apiCall(host, '/reverse-image-search', params, apiKey);
    const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);

    console.error(`${records.length} result(s) returned.`);
    if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
    writeOutput(records, outputPath, format, { api: 'reverse-image-search', endpoint: '/reverse-image-search', imageUrl: args.url, totalCalls: 1 });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
