#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Home Depot products, browse categories, look up items, get details and reviews.

Required (varies by endpoint):
  --query         Search query (for /search)
  --item-id       Item id / internet number (for /product-details, /product-reviews)
  --url           Product page URL (alternative to --item-id for /product-details)
  --category-id   Category id (for /products-by-category)
  --search        Model number or internet number (for /item-lookup)

Optional:
  --endpoint      Endpoint: /search (default), /products-by-category, /product-details, /item-lookup, /product-reviews
  --count         Max results to fetch (default: 72)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --sort-by       Sort. Products: best_match, top_sellers, top_rated, price_low_to_high, price_high_to_low, newest.
                  Reviews: helpful, newest, oldest, photos_first, highest_rating, lowest_rating, relevance
  --min-price     Min price filter (search/category)
  --max-price     Max price filter (search/category)
  --brand         Brand filter, e.g. DEWALT (search/category)
  --in-stock      Only in-stock/fulfillable products (search/category)
  --store-id      Home Depot store number for localized pricing/inventory
  --zipcode       5-digit US zip code for localized delivery/pricing
  --rating        Review star filter 1-5 (for /product-reviews)
  --verified-only Only verified-purchaser reviews (for /product-reviews)
  --search-text   Keyword filter for review text (for /product-reviews)
  --items-per-page  Results per page (default: 24 for products, 20 for reviews)
  --dry-run       Fetch first page only, print to console
  --max-calls     Safety cap on API calls (default: 50)
  --help          Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--in-stock') { args.inStock = true; continue; }
        if (arg === '--verified-only') { args.verifiedOnly = true; continue; }
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
    const meta = loadMeta('realtime-homedepot-data');
    const host = meta.rapidapi_host || 'realtime-homedepot-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 72;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-homedepot-data_${ts}.${format}`);

    // ── Product Details (single call, no pagination) ──────────────────────────
    if (endpoint === '/product-details') {
        if (!args.itemId && !args.url) { console.error('Error: --item-id or --url required for /product-details'); process.exit(1); }
        const params = {};
        if (args.itemId) params.item_id = args.itemId;
        if (args.url) params.url = args.url;
        if (args.storeId) params.store_id = args.storeId;
        if (args.zipcode) params.zipcode = args.zipcode;
        const data = await apiCall(host, '/product-details', params, apiKey, 'GET', null, 'realtime-homedepot-data');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-homedepot-data', endpoint: '/product-details', totalCalls: 1 });
        return;
    }

    // ── Product Reviews (paginated) ───────────────────────────────────────────
    if (endpoint === '/product-reviews') {
        if (!args.itemId) { console.error('Error: --item-id required for /product-reviews'); process.exit(1); }
        const pageSize = parseInt(args.itemsPerPage, 10) || 20;
        const params = { item_id: args.itemId, items_per_page: pageSize };
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.rating) params.rating = args.rating;
        if (args.verifiedOnly) params.verified_only = true;
        if (args.searchText) params.search_text = args.searchText;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-reviews', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.reviews', dryRun, delay: 300, maxCalls,
            apiId: 'realtime-homedepot-data',
        });
        console.error(`${results.length} reviews in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-homedepot-data', endpoint: '/product-reviews', itemId: args.itemId, totalCalls: totalCallsMade });
        return;
    }

    // ── Products by Category (paginated) ──────────────────────────────────────
    if (endpoint === '/products-by-category') {
        if (!args.categoryId) { console.error('Error: --category-id required for /products-by-category'); process.exit(1); }
        const pageSize = parseInt(args.itemsPerPage, 10) || 24;
        const params = { category_id: args.categoryId, items_per_page: pageSize };
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.minPrice) params.min_price = args.minPrice;
        if (args.maxPrice) params.max_price = args.maxPrice;
        if (args.brand) params.brand = args.brand;
        if (args.inStock) params.in_stock = true;
        if (args.storeId) params.store_id = args.storeId;
        if (args.zipcode) params.zipcode = args.zipcode;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/products-by-category', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
            apiId: 'realtime-homedepot-data',
        });
        console.error(`${results.length} products in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-homedepot-data', endpoint: '/products-by-category', categoryId: args.categoryId, totalCalls: totalCallsMade });
        return;
    }

    // ── Item Lookup (paginated) ───────────────────────────────────────────────
    if (endpoint === '/item-lookup') {
        if (!args.search) { console.error('Error: --search required for /item-lookup'); process.exit(1); }
        const pageSize = parseInt(args.itemsPerPage, 10) || 24;
        const params = { search: args.search, items_per_page: pageSize };
        if (args.storeId) params.store_id = args.storeId;
        if (args.zipcode) params.zipcode = args.zipcode;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/item-lookup', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
            apiId: 'realtime-homedepot-data',
        });
        console.error(`${results.length} products in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-homedepot-data', endpoint: '/item-lookup', search: args.search, totalCalls: totalCallsMade });
        return;
    }

    // ── Search (default, paginated) ───────────────────────────────────────────
    if (!args.query) { console.error('Error: --query required for /search. Use --help for usage.'); process.exit(1); }

    const pageSize = parseInt(args.itemsPerPage, 10) || 24;
    const params = { query: args.query, items_per_page: pageSize };
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.brand) params.brand = args.brand;
    if (args.inStock) params.in_stock = true;
    if (args.storeId) params.store_id = args.storeId;
    if (args.zipcode) params.zipcode = args.zipcode;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
        apiId: 'realtime-homedepot-data',
    });

    console.error(`${results.length} products in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-homedepot-data', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
