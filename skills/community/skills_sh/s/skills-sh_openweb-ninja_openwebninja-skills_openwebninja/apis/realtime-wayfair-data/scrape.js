#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Wayfair products, get product details, and reviews.

Required (varies by endpoint):
  --query           Search query (for /search) — either --query or --manufacturer-id
  --manufacturer-id Wayfair brand/manufacturer ID (for /search browse) — either --query or --manufacturer-id
  --sku             Product SKU (for /product-details, /product-reviews)

Optional:
  --endpoint        Endpoint: /search (default), /product-details, /product-reviews
  --count           Max results to fetch (default: 96)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --domain          com | ca | co.uk | ie | de (default: com)
  --sort-by         Search sort: recommended, customer_rating, price_low_to_high, price_high_to_low
                    Reviews sort: relevance, helpful, date_ascending, date_descending, rating_ascending, rating_descending
  --category-id     Wayfair category ID (search)
  --min-price       Min price filter, USD (search)
  --max-price       Max price filter, USD (search)
  --color           Color filter, e.g. Black, White, Gray (search)
  --in-stock        Only in-stock products (search) — pass --in-stock
  --star            Review star filter 1-5 (for /product-reviews)
  --limit           Results per page for /search (24, 48, or 96; default 48)
  --dry-run         Fetch first page only, print to console
  --max-calls       Safety cap on API calls (default: 50)
  --help            Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--in-stock') { args.inStock = true; continue; }
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
    const meta = loadMeta('realtime-wayfair-data');
    const host = meta.rapidapi_host || 'real-time-wayfair-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 96;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const domain = args.domain || 'com';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-wayfair-data_${ts}.${format}`);

    // ── Product Details (single call, no pagination) ──────────────────────────
    if (endpoint === '/product-details') {
        if (!args.sku) { console.error('Error: --sku required for /product-details'); process.exit(1); }
        const params = { sku: args.sku, domain };
        const data = await apiCall(host, '/product-details', params, apiKey, 'GET', null, 'realtime-wayfair-data');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-wayfair-data', endpoint: '/product-details', totalCalls: 1 });
        return;
    }

    // ── Product Reviews (paginated, 10 per page) ──────────────────────────────
    if (endpoint === '/product-reviews') {
        if (!args.sku) { console.error('Error: --sku required for /product-reviews'); process.exit(1); }
        const pageSize = 10;
        const params = { sku: args.sku, domain };
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.star) params.star = args.star;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-reviews', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.reviews', dryRun, delay: 300, maxCalls,
            apiId: 'realtime-wayfair-data',
        });
        console.error(`${results.length} reviews in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-wayfair-data', endpoint: '/product-reviews', sku: args.sku, totalCalls: totalCallsMade });
        return;
    }

    // ── Search (default, paginated) ───────────────────────────────────────────
    if (!args.query && !args.manufacturerId) {
        console.error('Error: --query or --manufacturer-id required for /search. Use --help for usage.');
        process.exit(1);
    }

    const pageSize = parseInt(args.limit, 10) || 48;
    const params = { domain, items_per_page: pageSize };
    if (args.query) params.query = args.query;
    if (args.manufacturerId) params.manufacturer_id = args.manufacturerId;
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.categoryId) params.category_id = args.categoryId;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.color) params.color = args.color;
    if (args.inStock) params.in_stock = true;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
        apiId: 'realtime-wayfair-data',
    });

    console.error(`${results.length} products in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-wayfair-data', endpoint: '/search', query: args.query || args.manufacturerId, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
