#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search eBay products, browse by category, get product details, and seller feedback.

Required (varies by endpoint):
  --query          Search query (for /search)
  --category-id    Category ID (for /products-by-category)
  --product-id     Product ID / eBay item ID (for /product-details)
  --seller-id      eBay seller username (for /seller-feedback)

Optional:
  --endpoint       Endpoint: /search (default), /products-by-category, /product-details, /seller-feedback
  --count          Max results to fetch (default: 120)
  --format         json | csv (default: json)
  --output         Output file path (auto-generated if omitted)
  --domain         eBay domain (default: com). e.g. com, co.uk, de, com.au, ca, fr, it, es
  --sort-by        Sort: BEST_MATCH, ENDING_SOONEST, NEWLY_LISTED, PRICE_LOWEST, PRICE_HIGHEST (search/category)
  --condition      Item condition, comma-separated: new, used, open_box, refurbished, for_parts (search/category)
  --buying-format  Buying format: buy_it_now, auction, accepts_offers (search/category)
  --show-only      Listing attributes, comma-separated: free_returns, deals_and_savings, returns_accepted, authorized_seller, sold_items, completed_items, free_shipping, local_pickup (search/category)
  --min-price      Min price filter (search/category)
  --max-price      Max price filter (search/category)
  --aspects        JSON-encoded array of {name,value} aspect filters, max 20 (search/category)
  --product-id     For /seller-feedback: filter a seller's feedback to a specific item
  --dry-run        Fetch first page only, print to console
  --max-calls      Safety cap on API calls (default: 50)
  --help           Show this help
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
    const meta = loadMeta('realtime-ebay-data');
    const host = meta.rapidapi_host || 'real-time-ebay-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 120;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const domain = args.domain || 'com';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-ebay-data_${ts}.${format}`);

    // ── Product Details (single call, no pagination) ──────────────────────────
    if (endpoint === '/product-details') {
        if (!args.productId) { console.error('Error: --product-id required for /product-details'); process.exit(1); }
        const params = { product_id: args.productId, domain };
        const data = await apiCall(host, '/product-details', params, apiKey, 'GET', null, 'realtime-ebay-data');
        const records = data.data ? [data.data] : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-ebay-data', endpoint: '/product-details', totalCalls: 1 });
        return;
    }

    // ── Seller Feedback (paginated, 25/page) ──────────────────────────────────
    if (endpoint === '/seller-feedback') {
        if (!args.sellerId) { console.error('Error: --seller-id required for /seller-feedback'); process.exit(1); }
        const pageSize = 25;
        const params = { seller_id: args.sellerId, domain };
        if (args.productId) params.product_id = args.productId;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/seller-feedback', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.reviews', dryRun, delay: 300, maxCalls, apiId: 'realtime-ebay-data',
        });
        console.error(`${results.length} reviews in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-ebay-data', endpoint: '/seller-feedback', sellerId: args.sellerId, totalCalls: totalCallsMade });
        return;
    }

    // ── Products by Category (paginated, 60/page) ─────────────────────────────
    if (endpoint === '/products-by-category') {
        if (!args.categoryId) { console.error('Error: --category-id required for /products-by-category'); process.exit(1); }
        const pageSize = 60;
        const params = { category_id: args.categoryId, domain };
        if (args.query) params.query = args.query;
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.condition) params.condition = args.condition;
        if (args.buyingFormat) params.buying_format = args.buyingFormat;
        if (args.showOnly) params.show_only = args.showOnly;
        if (args.minPrice) params.min_price = args.minPrice;
        if (args.maxPrice) params.max_price = args.maxPrice;
        if (args.aspects) params.aspects = args.aspects;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/products-by-category', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize,
            resultsPath: 'data.products', dryRun, delay: 300, maxCalls, apiId: 'realtime-ebay-data',
        });
        console.error(`${results.length} products in ${totalCallsMade} call(s).`);
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-ebay-data', endpoint: '/products-by-category', categoryId: args.categoryId, totalCalls: totalCallsMade });
        return;
    }

    // ── Search (default, paginated, 60/page) ──────────────────────────────────
    if (!args.query) { console.error('Error: --query required for /search. Use --help for usage.'); process.exit(1); }

    const pageSize = 60;
    const params = { query: args.query, domain };
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.condition) params.condition = args.condition;
    if (args.buyingFormat) params.buying_format = args.buyingFormat;
    if (args.showOnly) params.show_only = args.showOnly;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.aspects) params.aspects = args.aspects;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data.products', dryRun, delay: 300, maxCalls, apiId: 'realtime-ebay-data',
    });

    console.error(`${results.length} products in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 5), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-ebay-data', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
