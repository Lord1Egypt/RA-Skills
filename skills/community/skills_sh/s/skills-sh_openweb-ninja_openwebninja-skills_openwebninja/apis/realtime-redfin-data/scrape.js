#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --location <zip|redfin_url> [options]

Search Redfin (US & Canada) property listings, get property details, and market trends.

Required (varies by endpoint):
  --location          Location: 5-digit US zip, Canadian postal-code area, or Redfin region URL
                      (for /search and /market-trends, e.g. "90210")
  --property-id       Redfin property ID (for /property-details; or use --url)
  --ne-lat/--ne-lng   Northeast corner of bounding box (for /search-coordinates)
  --sw-lat/--sw-lng   Southwest corner of bounding box (for /search-coordinates)
  --polygon           Polygon as "lng1 lat1,lng2 lat2,lng3 lat3,..." (for /search-polygon)

Optional:
  --endpoint          Endpoint: /search (default), /search-coordinates, /search-polygon, /property-details, /market-trends
  --count             Max results to fetch (default: 80)
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --status            for_sale (default), sold, for_rent, coming_soon
  --property-types    Comma-separated: HOUSE,CONDO,TOWNHOUSE,MULTI_FAMILY,LAND,OTHER,MANUFACTURED,CO_OP
  --sort              redfin_recommended (default), newest, oldest, price_low_high, price_high_low, beds, baths, sqft, lot_size
  --num-homes         Results per page (default: 40, up to 350)
  --country-code      US (default) or CA
  --min-price         Min price filter
  --max-price         Max price filter
  --min-beds          Min bedrooms
  --max-beds          Max bedrooms
  --min-baths         Min bathrooms (supports half-baths, e.g. 2.5)
  --min-sqft          Min interior square footage
  --max-sqft          Max interior square footage
  --min-lot-size      Min lot size (sqft)
  --max-lot-size      Max lot size (sqft)
  --min-year-built    Min year built
  --max-year-built    Max year built
  --max-hoa           Max monthly HOA dues
  --has-pool          Only properties with a pool (true)
  --has-garage        Only properties with a garage (true)
  --is-waterfront     Only waterfront properties (true)
  --time-on-market-days   Only properties on market within the last N days
  --sold-within-days  For --status sold, only properties sold within the last N days (1-1095)
  --url               Redfin listing URL (for /property-details)
  --dry-run           Fetch first page only, print to console
  --max-calls         Safety cap on API calls (default: 50)
  --help              Show this help
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

function addSearchFilters(params, args) {
    if (args.status) params.status = args.status;
    if (args.propertyTypes) params.property_types = args.propertyTypes;
    if (args.sort) params.sort = args.sort;
    if (args.countryCode) params.country_code = args.countryCode;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.minBeds) params.min_beds = args.minBeds;
    if (args.maxBeds) params.max_beds = args.maxBeds;
    if (args.minBaths) params.min_baths = args.minBaths;
    if (args.minSqft) params.min_sqft = args.minSqft;
    if (args.maxSqft) params.max_sqft = args.maxSqft;
    if (args.minLotSize) params.min_lot_size = args.minLotSize;
    if (args.maxLotSize) params.max_lot_size = args.maxLotSize;
    if (args.minYearBuilt) params.min_year_built = args.minYearBuilt;
    if (args.maxYearBuilt) params.max_year_built = args.maxYearBuilt;
    if (args.maxHoa) params.max_hoa = args.maxHoa;
    if (args.hasPool) params.has_pool = args.hasPool;
    if (args.hasGarage) params.has_garage = args.hasGarage;
    if (args.isWaterfront) params.is_waterfront = args.isWaterfront;
    if (args.timeOnMarketDays) params.time_on_market_days = args.timeOnMarketDays;
    if (args.soldWithinDays) params.sold_within_days = args.soldWithinDays;
}

async function main() {
    const args = parseArgs(process.argv);
    if (args.help) { printHelp(); process.exit(0); }

    const endpoint = args.endpoint || '/search';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-redfin-data');
    const host = meta.rapidapi_host || 'real-time-redfin-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 80;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const pageSize = parseInt(args.numHomes, 10) || 40; // num_homes per page (default 40, up to 350)

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-redfin-data_${ts}.${format}`);

    // ── Property Details (single call) ────────────────────────────────────────
    if (endpoint === '/property-details') {
        if (!args.propertyId && !args.url) { console.error('Error: --property-id or --url required for /property-details'); process.exit(1); }
        const params = {};
        if (args.propertyId) params.property_id = args.propertyId;
        if (args.url) params.url = args.url;
        if (args.countryCode) params.country_code = args.countryCode;
        const data = await apiCall(host, '/property-details', params, apiKey, 'GET', null, 'realtime-redfin-data');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-redfin-data', endpoint: '/property-details', totalCalls: 1 });
        return;
    }

    // ── Market Trends (single call) ───────────────────────────────────────────
    if (endpoint === '/market-trends') {
        if (!args.location) { console.error('Error: --location required for /market-trends'); process.exit(1); }
        const params = { location: args.location };
        if (args.countryCode) params.country_code = args.countryCode;
        const data = await apiCall(host, '/market-trends', params, apiKey, 'GET', null, 'realtime-redfin-data');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-redfin-data', endpoint: '/market-trends', location: args.location, totalCalls: 1 });
        return;
    }

    // ── Search by Coordinates / bounding box (paginated) ──────────────────────
    if (endpoint === '/search-coordinates') {
        if (!args.neLat || !args.neLng || !args.swLat || !args.swLng) {
            console.error('Error: --ne-lat, --ne-lng, --sw-lat and --sw-lng required for /search-coordinates'); process.exit(1);
        }
        const params = { ne_lat: args.neLat, ne_lng: args.neLng, sw_lat: args.swLat, sw_lng: args.swLng };
        addSearchFilters(params, args);

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/search-coordinates', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.results', dryRun, delay: 300, maxCalls, apiId: 'realtime-redfin-data',
        });
        console.error(`${results.length} properties in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-redfin-data', endpoint: '/search-coordinates', totalCalls: totalCallsMade });
        return;
    }

    // ── Search by Polygon (paginated) ─────────────────────────────────────────
    if (endpoint === '/search-polygon') {
        if (!args.polygon) { console.error('Error: --polygon required for /search-polygon'); process.exit(1); }
        const params = { polygon: args.polygon };
        addSearchFilters(params, args);

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/search-polygon', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.results', dryRun, delay: 300, maxCalls, apiId: 'realtime-redfin-data',
        });
        console.error(`${results.length} properties in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-redfin-data', endpoint: '/search-polygon', totalCalls: totalCallsMade });
        return;
    }

    // ── Search by Location (default, paginated) ───────────────────────────────
    if (!args.location) { console.error('Error: --location required for /search (5-digit US zip, Canadian postal-code area, or Redfin URL). Use --help for usage.'); process.exit(1); }

    const params = { location: args.location };
    addSearchFilters(params, args);

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data.results', dryRun, delay: 300, maxCalls, apiId: 'realtime-redfin-data',
    });

    console.error(`${results.length} properties in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-redfin-data', endpoint: '/search', location: args.location, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
