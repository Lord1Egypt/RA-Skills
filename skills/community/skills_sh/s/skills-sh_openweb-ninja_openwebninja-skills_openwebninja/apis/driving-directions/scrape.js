#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --origin <place> --destination <place> [options]

Get driving directions between two locations and export the result.

Required:
  --origin          Origin address or place (e.g. "Church St & 29th St, San Francisco, CA, USA")
  --destination     Destination address or place (e.g. "Sunnyvale, CA, USA")

Optional:
  --departure-time  Departure time as Unix timestamp
  --arrival-time    Arrival time as Unix timestamp
  --distance-units  auto | km | mi (default: auto)
  --avoid           Routes to avoid, comma-separated (e.g. "tolls,ferries")
  --country         Country code (default: US)
  --language        Language code (default: EN)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --dry-run         Fetch and print to console without writing file
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

    if (!args.origin) { console.error('Error: --origin required. Use --help for usage.'); process.exit(1); }
    if (!args.destination) { console.error('Error: --destination required. Use --help for usage.'); process.exit(1); }

    const apiKey = getApiKey();
    const meta = loadMeta('driving-directions');
    const host = meta.rapidapi_host || 'driving-directions1.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `driving-directions_${ts}.${format}`);

    const params = {
        origin: args.origin,
        destination: args.destination,
        country: args.country || 'US',
        language: args.language || 'EN',
    };

    if (args.departureTime) params.departure_time = parseInt(args.departureTime, 10);
    if (args.arrivalTime) params.arrival_time = parseInt(args.arrivalTime, 10);
    if (args.distanceUnits) params.distance_units = args.distanceUnits;
    if (args.avoid) params.avoid_routes = args.avoid;

    console.error(`Getting directions: ${args.origin} → ${args.destination}`);

    const data = await apiCall(host, '/get-directions', params, apiKey);

    // Response has data array with route objects
    const routes = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);

    console.error(`${routes.length} route(s) returned.`);

    if (dryRun) {
        const preview = routes.map(r => ({
            summary: r.summary,
            distance: r.distance,
            duration: r.duration,
            duration_in_traffic: r.duration_in_traffic,
            steps_count: Array.isArray(r.steps) ? r.steps.length : undefined,
            steps_preview: Array.isArray(r.steps) ? r.steps.slice(0, 3).map(s => s.instruction || s.html_instructions || s) : undefined,
        }));
        console.log(JSON.stringify(preview, null, 2));
        return;
    }

    writeOutput(routes, outputPath, format, {
        api: 'driving-directions',
        endpoint: '/get-directions',
        origin: args.origin,
        destination: args.destination,
        totalCalls: 1,
    });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
