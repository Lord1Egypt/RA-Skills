#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <text> [options]

Get Google Search autocomplete / typeahead suggestions with Knowledge Graph info.

Required:
  --query         Partial search query (e.g. "how to")

Optional:
  --queries       Comma-separated queries for batch mode (e.g. "how to,what is,best")
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --language      Language code (default: en)
  --region        Region code (default: us)
  --user-agent    desktop | mobile (default: desktop)
  --cursor        Cursor pointer position in the query string
  --dry-run       Print results to console instead of saving
  --max-calls     Safety cap on API calls (default: 50)
  --help          Show this help

Notes:
  This API returns suggestions in a single call (no pagination).
  Use --queries for batch mode to fetch suggestions for multiple prefixes.
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
    const meta = loadMeta('web-search-autocomplete');
    const host = meta.rapidapi_host || 'web-search-autocomplete.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `web-search-autocomplete_${ts}.${format}`);

    // Build list of queries (single or batch)
    const queries = args.queries
        ? args.queries.split(',').map(q => q.trim()).filter(Boolean)
        : (args.query ? [args.query] : []);

    if (!queries.length) { console.error('Error: --query or --queries required. Use --help for usage.'); process.exit(1); }

    const allResults = [];
    let totalCalls = 0;

    for (let i = 0; i < queries.length; i++) {
        if (i > 0) await sleep(300);
        totalCalls++;
        if (totalCalls > maxCalls) { console.error(`Cost cap (${maxCalls}). Use --max-calls to raise.`); break; }

        console.error(`  [${i + 1}/${queries.length}] Query: "${queries[i]}"`);
        try {
            const params = { query: queries[i] };
            if (args.language) params.language = args.language;
            if (args.region) params.region = args.region;
            if (args.userAgent) params.user_agent = args.userAgent;
            if (args.cursor) params.cursor_pointer = args.cursor;

            const data = await apiCall(host, '/autocomplete', params, apiKey);
            const suggestions = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : []);

            // Flatten each suggestion with the source query
            for (const s of suggestions) {
                allResults.push({ source_query: queries[i], ...s });
            }
        } catch (e) { console.error(`    Error: ${e.message}`); }
        if (dryRun && i === 0) break;
    }

    console.error(`${allResults.length} suggestions in ${totalCalls} call(s).`);
    if (dryRun) { console.log(JSON.stringify(allResults.slice(0, 10), null, 2)); return; }
    writeOutput(allResults, outputPath, format, { api: 'web-search-autocomplete', endpoint: '/autocomplete', totalCalls });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
