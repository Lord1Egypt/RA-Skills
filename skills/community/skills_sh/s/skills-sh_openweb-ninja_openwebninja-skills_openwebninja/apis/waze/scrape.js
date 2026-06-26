#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --endpoint <endpoint> [options]

Query Waze for traffic alerts, jams, directions, venues, or autocomplete.

Endpoints:
  /alerts-and-jams   Traffic alerts and jams in a bounding box (default)
  /driving-directions Driving directions between two points
  /venues            Venues in a bounding box
  /autocomplete      Place autocomplete

Options for /alerts-and-jams:
  --bbox              Bounding box: "bottom_left_lat,bottom_left_lng|top_right_lat,top_right_lng"
                      Example: "40.666,-74.137|40.772,-73.768"
  --max-alerts        Max alerts to return (default: 20)
  --max-jams          Max jams to return (default: 20)
  --alert-types       Filter alert types (comma-separated)
  --alert-subtypes    Filter alert subtypes (comma-separated)

Options for /driving-directions:
  --source            Source coordinates: "lat,lng"
  --destination       Destination coordinates: "lat,lng"
  --return-coords     Return route coordinate pairs (flag)
  --arrival           Arrival unix timestamp

Options for /venues:
  --bbox              Bounding box (same format as above)
  --categories        Venue categories filter
  --zoom-level        Waze zoom level (1-14)

Options for /autocomplete:
  --query             Search query (e.g. "sunn")
  --coordinates       Bias coordinates: "lat,lng"
  --language          Language code

Common:
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --dry-run           Print response to console only
  --help              Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--return-coords') { args.returnCoords = true; continue; }
        if (arg.startsWith('--') && i + 1 < argv.length) {
            const key = arg.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
            args[key] = argv[++i];
        }
    }
    return args;
}

function parseBbox(bbox) {
    const parts = bbox.split('|');
    if (parts.length !== 2) { console.error('Error: --bbox format must be "bottom_left_lat,bottom_left_lng|top_right_lat,top_right_lng"'); process.exit(1); }
    return { bottom_left: parts[0].trim(), top_right: parts[1].trim() };
}

async function main() {
    const args = parseArgs(process.argv);
    if (args.help) { printHelp(); process.exit(0); }

    const endpoint = args.endpoint || '/alerts-and-jams';
    const apiKey = getApiKey();
    const meta = loadMeta('waze');
    const host = meta.rapidapi_host || 'waze.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `waze_${ts}.${format}`);

    // ── Alerts and Jams ──
    if (endpoint === '/alerts-and-jams') {
        if (!args.bbox) { console.error('Error: --bbox required for /alerts-and-jams. Use --help for usage.'); process.exit(1); }
        const { bottom_left, top_right } = parseBbox(args.bbox);
        const params = { bottom_left, top_right };
        if (args.maxAlerts) params.max_alerts = parseInt(args.maxAlerts, 10);
        if (args.maxJams) params.max_jams = parseInt(args.maxJams, 10);
        if (args.alertTypes) params.alert_types = args.alertTypes;
        if (args.alertSubtypes) params.alert_subtypes = args.alertSubtypes;

        console.error('Fetching alerts and jams...');
        const data = await apiCall(host, '/alerts-and-jams', params, apiKey);

        // Combine alerts + jams into a single array with a _type field
        const alerts = (data.data && data.data.alerts || data.alerts || []).map(a => ({ _type: 'alert', ...a }));
        const jams = (data.data && data.data.jams || data.jams || []).map(j => ({ _type: 'jam', ...j }));
        const allRecords = [...alerts, ...jams];

        console.error(`${alerts.length} alert(s), ${jams.length} jam(s) fetched.`);
        if (dryRun) { console.log(JSON.stringify(allRecords.slice(0, 5), null, 2)); return; }
        writeOutput(allRecords, outputPath, format, { api: 'waze', endpoint, alerts: alerts.length, jams: jams.length, totalCalls: 1 });
        return;
    }

    // ── Driving Directions ──
    if (endpoint === '/driving-directions') {
        if (!args.source || !args.destination) { console.error('Error: --source and --destination required for /driving-directions'); process.exit(1); }
        const params = { source_coordinates: args.source, destination_coordinates: args.destination };
        if (args.returnCoords) params.return_route_coordinates = true;
        if (args.arrival) params.arrival_timestamp = args.arrival;

        console.error('Fetching driving directions...');
        const data = await apiCall(host, '/driving-directions', params, apiKey);
        const records = data.data ? (Array.isArray(data.data) ? data.data : [data.data]) : [data];

        if (dryRun) { console.log(JSON.stringify(records.slice(0, 3), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'waze', endpoint, totalCalls: 1 });
        return;
    }

    // ── Venues ──
    if (endpoint === '/venues') {
        if (!args.bbox) { console.error('Error: --bbox required for /venues. Use --help for usage.'); process.exit(1); }
        const { bottom_left, top_right } = parseBbox(args.bbox);
        const params = { bottom_left, top_right };
        if (args.categories) params.categories = args.categories;
        if (args.zoomLevel) params.zoom_level = args.zoomLevel;

        console.error('Fetching venues...');
        const data = await apiCall(host, '/venues', params, apiKey);
        const records = data.data ? (Array.isArray(data.data) ? data.data : [data.data]) : [data];

        console.error(`${records.length} venue(s) fetched.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'waze', endpoint, totalCalls: 1 });
        return;
    }

    // ── Autocomplete ──
    if (endpoint === '/autocomplete') {
        if (!args.query) { console.error('Error: --query required for /autocomplete'); process.exit(1); }
        if (!args.coordinates) { console.error('Error: --coordinates required for /autocomplete (e.g. "37.376,-122.023")'); process.exit(1); }
        const params = { q: args.query, coordinates: args.coordinates };
        if (args.language) params.language = args.language;

        console.error('Fetching autocomplete suggestions...');
        const data = await apiCall(host, '/autocomplete', params, apiKey);
        const records = data.data ? (Array.isArray(data.data) ? data.data : [data.data]) : [data];

        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'waze', endpoint, totalCalls: 1 });
        return;
    }

    console.error(`Error: Unknown endpoint "${endpoint}". Use --help for available endpoints.`);
    process.exit(1);
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
