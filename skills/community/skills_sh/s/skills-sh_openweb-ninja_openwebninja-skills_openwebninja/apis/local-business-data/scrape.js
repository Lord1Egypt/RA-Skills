#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Google Maps businesses and export results.

Required:
  --query         Search query (e.g. "Hotels in San Francisco, USA")

Optional:
  --endpoint      Endpoint: /search (default), /search-in-area, /search-nearby, /business-details, /business-reviews
  --count         Max results (default: 100, max per call: 500)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --contacts      Extract emails, phones, social profiles (extra credit)
  --subtypes      Filter by GMB category (e.g. "Coffee shop")
  --zips          Comma-separated zip codes — one search per zip, deduplicates
  --grid          Grid mode: tile a bounding box with /search-in-area, auto-subdivide dense cells
  --bbox          Bounding box for --grid: "swLat,swLng,neLat,neLng" (e.g. "32.5,-124.5,42.0,-114.0" for CA)
  --lat           Latitude
  --lng           Longitude
  --zoom          Starting zoom level (default: 13, for --grid default: 10)
  --region        Region code (default: us)
  --language      Language code (default: en)
  --business-id   Business ID (for /business-details or /business-reviews)
  --sort-by       Review sort: most_relevant, newest, highest_ranking, lowest_ranking
  --dry-run       Fetch first cell only (grid) or first call only, print to console
  --max-calls     Safety cap (default: 50, increase for --grid)
  --help          Show this help

Grid mode example (all plumbers in California with emails):
  node scrape.js --query "plumbers" --grid --bbox "32.5,-124.5,42.0,-114.0" --contacts --max-calls 300 --format csv
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--contacts') { args.contacts = true; continue; }
        if (arg === '--grid') { args.grid = true; continue; }
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
    const meta = loadMeta('local-business-data');
    const host = meta.rapidapi_host || 'local-business-data.p.rapidapi.com';
    const count = Math.min(parseInt(args.count, 10) || 100, 500);
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `local-business-data_${ts}.${format}`);

    // Business details
    if (endpoint === '/business-details') {
        if (!args.businessId) { console.error('Error: --business-id required'); process.exit(1); }
        const params = { business_id: args.businessId, region: args.region || 'us', language: args.language || 'en' };
        if (args.contacts) params.extract_emails_and_contacts = true;
        const data = await apiCall(host, '/business-details', params, apiKey);
        const records = data.data ? [data.data] : [data];
        writeOutput(records, outputPath, format, { api: 'local-business-data', endpoint: '/business-details', totalCalls: 1 });
        return;
    }

    // Business reviews
    if (endpoint === '/business-reviews') {
        if (!args.businessId) { console.error('Error: --business-id required'); process.exit(1); }
        const params = { business_id: args.businessId, limit: Math.min(count, 20), region: args.region || 'us', language: args.language || 'en' };
        if (args.sortBy) params.sort_by = args.sortBy;
        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/business-reviews', params, apiKey, count,
            pagination: 'cursor', cursorParam: 'cursor', cursorPath: 'cursor',
            pageSize: 20, resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'local-business-data', endpoint: '/business-reviews', totalCalls: totalCallsMade });
        return;
    }

    // Search endpoints
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query, limit: count, language: args.language || 'en', region: args.region || 'us' };
    if (args.lat) params.lat = args.lat;
    if (args.lng) params.lng = args.lng;
    if (args.zoom) params.zoom = args.zoom;
    if (args.contacts) params.extract_emails_and_contacts = true;
    if (args.subtypes) params.subtypes = args.subtypes;

    let allResults = [];
    let totalCalls = 0;

    // ── Grid mode: tile a bounding box with adaptive subdivision ──────────
    if (args.grid) {
        if (!args.bbox) { console.error('Error: --bbox "swLat,swLng,neLat,neLng" required with --grid'); process.exit(1); }
        const [swLat, swLng, neLat, neLng] = args.bbox.split(',').map(Number);
        if ([swLat, swLng, neLat, neLng].some(isNaN)) { console.error('Error: --bbox must be 4 comma-separated numbers'); process.exit(1); }
        const startZoom = parseInt(args.zoom, 10) || 10;
        const maxZoom = startZoom + 4; // don't subdivide beyond this
        const seen = new Set();

        // Build initial grid cells
        function buildCells(sw_lat, sw_lng, ne_lat, ne_lng, zoom) {
            // Approximate degrees per cell at given zoom (rough heuristic)
            const degreesPerCell = 360 / Math.pow(2, zoom);
            const cells = [];
            for (let lat = sw_lat; lat < ne_lat; lat += degreesPerCell) {
                for (let lng = sw_lng; lng < ne_lng; lng += degreesPerCell) {
                    cells.push({
                        lat: lat + degreesPerCell / 2,
                        lng: lng + degreesPerCell / 2,
                        zoom,
                        size: degreesPerCell,
                    });
                }
            }
            return cells;
        }

        const queue = buildCells(swLat, swLng, neLat, neLng, startZoom);
        const limit = Math.min(parseInt(args.count, 10) || 500, 500);
        let subdivisions = 0;

        console.error(`Grid mode: ${queue.length} initial cells at zoom ${startZoom}, bbox [${swLat},${swLng},${neLat},${neLng}]`);

        while (queue.length > 0) {
            const cell = queue.shift();
            if (totalCalls >= maxCalls) { console.error(`Cost cap (${maxCalls} calls). Use --max-calls to raise.`); break; }
            totalCalls++;

            const cellParams = { ...params, lat: String(cell.lat), lng: String(cell.lng), zoom: String(cell.zoom), limit };
            try {
                const data = await apiCall(host, '/search-in-area', cellParams, apiKey);
                const records = data.data || [];
                let newCount = 0;
                for (const rec of records) {
                    if (rec.business_id && !seen.has(rec.business_id)) { seen.add(rec.business_id); allResults.push(rec); newCount++; }
                }
                console.error(`  Cell [${cell.lat.toFixed(2)},${cell.lng.toFixed(2)}] z${cell.zoom}: ${records.length} results (${newCount} new) | total: ${allResults.length} | calls: ${totalCalls}/${maxCalls}`);

                // If we hit the limit, subdivide into 4 smaller cells
                if (records.length >= limit && cell.zoom < maxZoom) {
                    subdivisions++;
                    const half = cell.size / 2;
                    const quarter = cell.size / 4;
                    const baseLat = cell.lat - half / 2;
                    const baseLng = cell.lng - half / 2;
                    for (let dLat = 0; dLat < 2; dLat++) {
                        for (let dLng = 0; dLng < 2; dLng++) {
                            queue.push({ lat: baseLat + dLat * half + quarter, lng: baseLng + dLng * half + quarter, zoom: cell.zoom + 1, size: half });
                        }
                    }
                    console.error(`    → Saturated (${records.length}/${limit}), subdivided into 4 cells at zoom ${cell.zoom + 1}`);
                }
            } catch (e) { console.error(`  Cell [${cell.lat.toFixed(2)},${cell.lng.toFixed(2)}] Error: ${e.message}`); }

            if (dryRun) break;
            if (totalCalls < maxCalls && queue.length > 0) await sleep(200);
        }
        console.error(`\nGrid complete: ${allResults.length} unique businesses, ${totalCalls} API calls, ${subdivisions} subdivisions`);
        if (dryRun) { console.log(JSON.stringify(allResults.slice(0, 5), null, 2)); return; }
        writeOutput(allResults, outputPath, format, { api: 'local-business-data', endpoint: '/search-in-area', query: args.query, mode: 'grid', bbox: args.bbox, totalCalls });
        return;
    }

    if (args.zips) {
        const zips = args.zips.split(',').map(z => z.trim()).filter(Boolean);
        const seen = new Set();
        console.error(`Multi-zip mode: ${zips.length} zip code(s)`);
        for (let i = 0; i < zips.length; i++) {
            if (i > 0) await sleep(200);
            totalCalls++;
            if (totalCalls > maxCalls) { console.error(`Cost cap (${maxCalls}). Use --max-calls to raise.`); break; }
            console.error(`  [${i + 1}/${zips.length}] ${zips[i]}`);
            try {
                const data = await apiCall(host, endpoint, { ...params, query: `${args.query} ${zips[i]}` }, apiKey);
                for (const rec of (data.data || [])) {
                    if (rec.business_id && !seen.has(rec.business_id)) { seen.add(rec.business_id); allResults.push(rec); }
                }
            } catch (e) { console.error(`    Error: ${e.message}`); }
            if (dryRun) break;
        }
    } else {
        const { results, totalCallsMade } = await fetchAll({
            host, endpoint, params, apiKey, count,
            pagination: 'none', pageSize: count, resultsPath: 'data',
            dryRun, delay: 200, maxCalls,
        });
        allResults = results;
        totalCalls = totalCallsMade;
    }

    console.error(`${allResults.length} businesses in ${totalCalls} call(s).`);
    if (dryRun) { console.log(JSON.stringify(allResults.slice(0, 3), null, 2)); return; }
    writeOutput(allResults, outputPath, format, { api: 'local-business-data', endpoint, query: args.query, totalCalls });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
