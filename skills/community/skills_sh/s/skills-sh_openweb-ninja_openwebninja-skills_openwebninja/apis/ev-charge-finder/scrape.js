#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js [options]

Search for EV charging stations and export results.

At least one location method is required:
  --location        Free-form location query (e.g. "San Francisco, CA, USA")
  --lat / --lng     Latitude and longitude (both required together)

Optional:
  --endpoint        /search-by-location (default) or /search-by-coordinates-point
  --connector-type  Connector type filter (e.g. "CHAdeMO", "CCS", "Type 2")
  --available       Only show stations with available connectors (true/false)
  --min-kw          Minimum power in kilowatts
  --max-kw          Maximum power in kilowatts
  --query           Additional search query filter
  --count           Max results (default: 20)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --dry-run         Fetch first call only, print to console
  --help            Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--available') {
            // Check if next arg is a value or another flag
            if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) {
                args.available = argv[++i];
            } else {
                args.available = 'true';
            }
            continue;
        }
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
    const meta = loadMeta('ev-charge-finder');
    const host = meta.rapidapi_host || 'ev-charge-finder.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 20;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `ev-charge-finder_${ts}.${format}`);

    // Determine endpoint and build params
    let endpoint = args.endpoint;
    const params = { limit: count };

    if (args.lat && args.lng) {
        endpoint = endpoint || '/search-by-coordinates-point';
        params.lat = parseFloat(args.lat);
        params.lng = parseFloat(args.lng);
    } else if (args.location) {
        endpoint = endpoint || '/search-by-location';
        params.near = args.location;
    } else {
        console.error('Error: --location or --lat/--lng required. Use --help for usage.');
        process.exit(1);
    }

    if (args.connectorType) params.type = args.connectorType;
    if (args.available) params.available = args.available;
    if (args.minKw) params.min_kw = parseFloat(args.minKw);
    if (args.maxKw) params.max_kw = parseFloat(args.maxKw);
    if (args.query) params.query = args.query;

    console.error(`Searching EV stations via ${endpoint}...`);

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint, params, apiKey, count,
        pagination: 'none', pageSize: count, resultsPath: 'data',
        dryRun, delay: 200, maxCalls: 5,
    });

    console.error(`${results.length} station(s) in ${totalCallsMade} call(s).`);

    if (dryRun) {
        console.log(JSON.stringify(results.slice(0, 3), null, 2));
        return;
    }

    writeOutput(results, outputPath, format, {
        api: 'ev-charge-finder', endpoint, totalCalls: totalCallsMade,
    });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
