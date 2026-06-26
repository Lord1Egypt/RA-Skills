#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, toCSV, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --endpoint <endpoint> [options]

Track local business rankings on Google Maps with grid-based rank tracking.

Endpoints:
  /places                       Search for business locations (requires --query)
  /search                       Keyword search at a coordinate (requires --query, --lat, --lng)
  /ranking-at-coordinate        Rank at a coordinate (requires --place-id, --query, --lat, --lng)
  /calculate-grid-coordinates   Calculate grid points (requires --lat, --lng, --grid-size, --radius)
  /grid                         Full grid search (requires --place-id, --query, --lat, --lng, --grid-size, --radius)

Required (varies by endpoint):
  --query         Search query / keyword
  --lat           Latitude coordinate
  --lng           Longitude coordinate
  --place-id      Google Place ID of the business
  --grid-size     Grid size (e.g. 3 for 3x3, 5 for 5x5)
  --radius        Search radius

Optional:
  --endpoint      Endpoint (default: /places)
  --near          Location string for /places (e.g. "California, USA")
  --zoom          Map zoom level (default: 13)
  --shape         Grid shape: square, round (default: square)
  --radius-units  Radius units: km, mi (default: km)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
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

    const endpoint = args.endpoint || '/places';
    const apiKey = getApiKey();
    const meta = loadMeta('local-rank-tracker');
    const host = meta.rapidapi_host || 'local-rank-tracker.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const safeEndpoint = endpoint.replace(/\//g, '_');
    const outputPath = args.output || path.join('output', `local-rank-tracker${safeEndpoint}_${ts}.${format}`);

    // ── Search Business Locations (/places) ───────────────────────────────────
    if (endpoint === '/places') {
        if (!args.query) { console.error('Error: --query required for /places'); process.exit(1); }
        const params = { query: args.query };
        if (args.near) params.near = args.near;
        const data = await apiCall(host, '/places', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} location(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'local-rank-tracker', endpoint: '/places', query: args.query, totalCalls: 1 });
        return;
    }

    // ── Keyword Search at Coordinate (/search) ───────────────────────────────
    if (endpoint === '/search') {
        if (!args.query || !args.lat || !args.lng) {
            console.error('Error: --query, --lat, --lng required for /search'); process.exit(1);
        }
        const params = { query: args.query, lat: args.lat, lng: args.lng };
        if (args.zoom) params.zoom = args.zoom;
        const data = await apiCall(host, '/search', params, apiKey);
        const results = data.data && data.data.results ? data.data.results : (Array.isArray(data.data) ? data.data : [data]);
        console.error(`${results.length} result(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'local-rank-tracker', endpoint: '/search', query: args.query, totalCalls: 1 });
        return;
    }

    // ── Ranking at Coordinate (/ranking-at-coordinate) ────────────────────────
    if (endpoint === '/ranking-at-coordinate') {
        if (!args.placeId || !args.query || !args.lat || !args.lng) {
            console.error('Error: --place-id, --query, --lat, --lng required for /ranking-at-coordinate'); process.exit(1);
        }
        const params = { place_id: args.placeId, query: args.query, lat: args.lat, lng: args.lng };
        if (args.zoom) params.zoom = args.zoom;
        const data = await apiCall(host, '/ranking-at-coordinate', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`Ranking data in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'local-rank-tracker', endpoint: '/ranking-at-coordinate', totalCalls: 1 });
        return;
    }

    // ── Calculate Grid Coordinates (/calculate-grid-coordinates) ──────────────
    if (endpoint === '/calculate-grid-coordinates') {
        if (!args.lat || !args.lng || !args.gridSize || !args.radius) {
            console.error('Error: --lat, --lng, --grid-size, --radius required for /calculate-grid-coordinates'); process.exit(1);
        }
        const params = { lat: args.lat, lng: args.lng, grid_size: args.gridSize, radius: args.radius };
        if (args.radiusUnits) params.radius_units = args.radiusUnits;
        const data = await apiCall(host, '/calculate-grid-coordinates', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`${records.length} coordinate point(s) in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 10), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'local-rank-tracker', endpoint: '/calculate-grid-coordinates', totalCalls: 1 });
        return;
    }

    // ── Full Grid Search (/grid) ──────────────────────────────────────────────
    if (endpoint === '/grid') {
        if (!args.placeId || !args.query || !args.lat || !args.lng || !args.gridSize || !args.radius) {
            console.error('Error: --place-id, --query, --lat, --lng, --grid-size, --radius required for /grid'); process.exit(1);
        }
        const params = {
            place_id: args.placeId, query: args.query,
            lat: args.lat, lng: args.lng,
            grid_size: args.gridSize, radius: args.radius,
        };
        if (args.shape) params.shape = args.shape;
        if (args.radiusUnits) params.radius_units = args.radiusUnits;
        if (args.zoom) params.zoom = args.zoom;
        const data = await apiCall(host, '/grid', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        console.error(`Grid search complete in 1 call.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'local-rank-tracker', endpoint: '/grid', totalCalls: 1 });
        return;
    }

    console.error(`Error: unknown endpoint "${endpoint}". Use --help for usage.`);
    process.exit(1);
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
