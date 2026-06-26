#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, toCSV, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search for images via Google Images and export results.

Required:
  --query         Search query (e.g. "sunset beach")

Optional:
  --count         Max results to fetch (default: 10, max: 100)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country code, e.g. us, gb, de (default: us)
  --region        Region code (default: us)
  --size          Image size filter: any, large, medium, icon, 400x300_and_more, etc.
  --color         Color filter: any, red, orange, yellow, green, teal, blue, purple, pink, etc.
  --type          Image type: any, face, photo, clipart, lineart, animated
  --time          Time filter: any, day, week, month, year
  --usage-rights  Usage rights: any, creative_commons, commercial
  --file-type     File type: any, jpg, jpeg, png, gif, svg, webp, ico, raw
  --aspect-ratio  Aspect ratio: any, tall, square, wide, panoramic
  --safe-search   Safe search: off, blur, on (default: blur)
  --fields        Comma-separated fields to return (e.g. title,url,thumbnail_url)
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

    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const apiKey = getApiKey();
    const meta = loadMeta('realtime-image-search');
    const host = meta.rapidapi_host || 'real-time-image-search.p.rapidapi.com';
    const count = Math.min(parseInt(args.count, 10) || 10, 100);
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-image-search_${ts}.${format}`);

    const params = { query: args.query, limit: String(count) };
    if (args.country) params.country = args.country;
    if (args.region) params.region = args.region;
    if (args.size) params.size = args.size;
    if (args.color) params.color = args.color;
    if (args.type) params.type = args.type;
    if (args.time) params.time = args.time;
    if (args.usageRights) params.usage_rights = args.usageRights;
    if (args.fileType) params.file_type = args.fileType;
    if (args.aspectRatio) params.aspect_ratio = args.aspectRatio;
    if (args.safeSearch) params.safe_search = args.safeSearch;
    if (args.fields) params.fields = args.fields;

    const data = await apiCall(host, '/search', params, apiKey);
    const raw = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
    const records = raw.filter(r => r && typeof r === 'object');
    if (records.length === 0) { console.error('Warning: API returned 0 valid image records. The upstream API may be unavailable or the subscription key may lack access.'); }

    console.error(`${records.length} image result(s) in 1 call.`);
    if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
    writeOutput(records, outputPath, format, { api: 'realtime-image-search', endpoint: '/search', query: args.query, totalCalls: 1 });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
