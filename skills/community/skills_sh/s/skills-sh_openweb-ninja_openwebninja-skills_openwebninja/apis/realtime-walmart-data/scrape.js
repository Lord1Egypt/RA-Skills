#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Walmart products, get details, offers, and reviews.

Required (varies by endpoint):
  --query         Search query (for /search)
  --product-id    Product ID (for /product-details, /product-offers, /product-reviews)
  --category-id   Category ID (for /products-by-category)

Optional:
  --endpoint      Endpoint: /search (default), /products-by-category, /product-details, /product-offers, /product-reviews
  --count         Max results to fetch (default: 80)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --domain        us | ca (default: us)
  --sort-by       Sort: best_match, price_low, price_high, best_seller, top_rated (search/category)
  --min-price     Min price filter (search/category)
  --max-price     Max price filter (search/category)
  --store-id      Walmart store ID
  --state         US state code, e.g. CA
  --zip           ZIP code, e.g. 90210
  --facet         Facet filter string
  --rating        Review star filter 1-5 (for /product-reviews)
  --sort          Review sort: relevancy, recent, rating_high_low, rating_low_high
  --limit         Results per page (default: 40 for search, 10 for reviews)
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
    const meta = loadMeta('realtime-walmart-data');
    const host = meta.rapidapi_host || 'real-time-walmart-data1.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 80;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const domain = args.domain || 'us';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-walmart-data_${ts}.${format}`);

    // ── Product Details (single call, no pagination) ──────────────────────────
    if (endpoint === '/product-details') {
        if (!args.productId) { console.error('Error: --product-id required for /product-details'); process.exit(1); }
        const params = { product_id: args.productId, domain };
        const data = await apiCall(host, '/product-details', params, apiKey);
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-walmart-data', endpoint: '/product-details', totalCalls: 1 });
        return;
    }

    // ── Product Offers (single call, no pagination) ───────────────────────────
    if (endpoint === '/product-offers') {
        if (!args.productId) { console.error('Error: --product-id required for /product-offers'); process.exit(1); }
        const params = { product_id: args.productId, domain };
        const data = await apiCall(host, '/product-offers', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-walmart-data', endpoint: '/product-offers', totalCalls: 1 });
        return;
    }

    // ── Product Reviews (paginated) ───────────────────────────────────────────
    if (endpoint === '/product-reviews') {
        if (!args.productId) { console.error('Error: --product-id required for /product-reviews'); process.exit(1); }
        const pageSize = parseInt(args.limit, 10) || 10;
        const params = { product_id: args.productId, domain, limit: pageSize };
        if (args.rating) params.rating = args.rating;
        if (args.sort) params.sort = args.sort;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-reviews', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        console.error(`${results.length} reviews in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-walmart-data', endpoint: '/product-reviews', productId: args.productId, totalCalls: totalCallsMade });
        return;
    }

    // ── Products by Category (paginated) ──────────────────────────────────────
    if (endpoint === '/products-by-category') {
        if (!args.categoryId) { console.error('Error: --category-id required for /products-by-category'); process.exit(1); }
        const pageSize = parseInt(args.limit, 10) || 40;
        const params = { category_id: args.categoryId, domain, limit: pageSize };
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.minPrice) params.min_price = args.minPrice;
        if (args.maxPrice) params.max_price = args.maxPrice;
        if (args.storeId) params.store_id = args.storeId;
        if (args.facet) params.facet = args.facet;
        if (args.state) params.state = args.state;
        if (args.zip) params.zip = args.zip;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/products-by-category', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        console.error(`${results.length} products in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-walmart-data', endpoint: '/products-by-category', categoryId: args.categoryId, totalCalls: totalCallsMade });
        return;
    }

    // ── Search (default, paginated) ───────────────────────────────────────────
    if (!args.query) { console.error('Error: --query required for /search. Use --help for usage.'); process.exit(1); }

    const pageSize = parseInt(args.limit, 10) || 40;
    const params = { query: args.query, domain, limit: pageSize };
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.storeId) params.store_id = args.storeId;
    if (args.facet) params.facet = args.facet;
    if (args.state) params.state = args.state;
    if (args.zip) params.zip = args.zip;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} products in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-walmart-data', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
