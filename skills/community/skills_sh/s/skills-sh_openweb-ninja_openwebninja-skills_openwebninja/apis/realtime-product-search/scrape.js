#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search products across stores and export results.

Required:
  --query           Search query (e.g. "Nike shoes")
                    For /product-details-v2, /product-offers-v2, /product-reviews-v2: use --product-id instead
                    For /store-reviews: use --store-domain instead

Optional:
  --endpoint        Endpoint: /search-v2 (default), /search-light-v2, /deals-v2,
                    /product-details-v2, /product-offers-v2, /product-reviews-v2, /store-reviews
  --count           Max results (default: 100)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --product-id      Product ID (for /product-details-v2, /product-offers-v2, /product-reviews-v2)
  --store-domain    Store domain (for /store-reviews, e.g. "amazon.com")
  --min-price       Minimum price filter
  --max-price       Maximum price filter
  --condition       Product condition: ANY, NEW, USED, REFURBISHED (default: ANY)
  --sort-by         Sort: BEST_MATCH, TOP_RATED, LOWEST_PRICE, HIGHEST_PRICE
                    For reviews: MOST_RELEVANT, MOST_RECENT
                    For store reviews: MOST_HELPFUL, MOST_RECENT
  --country         Country code (default: us)
  --language        Language code (default: en)
  --stores          Filter by store (default: ANY)
  --free-shipping   Include only free shipping offers
  --free-returns    Include only free returns offers
  --on-sale         Include only on-sale items
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
        if (arg === '--free-shipping') { args.freeShipping = true; continue; }
        if (arg === '--free-returns') { args.freeReturns = true; continue; }
        if (arg === '--on-sale') { args.onSale = true; continue; }
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

    const endpoint = args.endpoint || '/search-v2';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-product-search');
    const host = meta.rapidapi_host || 'real-time-product-search.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 100;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const pageSize = 10;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-product-search_${ts}.${format}`);

    // ── Product Details (no pagination) ──
    if (endpoint === '/product-details-v2') {
        if (!args.productId) { console.error('Error: --product-id required for /product-details-v2'); process.exit(1); }
        const params = { product_id: args.productId, country: args.country || 'us', language: args.language || 'en' };
        const data = await apiCall(host, '/product-details-v2', params, apiKey);
        const records = data.data ? [data.data] : [data];
        writeOutput(records, outputPath, format, { api: 'realtime-product-search', endpoint, totalCalls: 1 });
        return;
    }

    // ── Product Offers (page-based, no limit param) ──
    if (endpoint === '/product-offers-v2') {
        if (!args.productId) { console.error('Error: --product-id required for /product-offers-v2'); process.exit(1); }
        const params = { product_id: args.productId, country: args.country || 'us', language: args.language || 'en' };
        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-offers-v2', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 10,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'realtime-product-search', endpoint, totalCalls: totalCallsMade });
        return;
    }

    // ── Product Reviews (cursor-based) ──
    if (endpoint === '/product-reviews-v2') {
        if (!args.productId) { console.error('Error: --product-id required for /product-reviews-v2'); process.exit(1); }
        const params = { product_id: args.productId, limit: Math.min(count, 10), country: args.country || 'us', language: args.language || 'en' };
        if (args.sortBy) params.sort_by = args.sortBy;
        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-reviews-v2', params, apiKey, count,
            pagination: 'cursor', cursorParam: 'cursor', cursorPath: 'cursor',
            pageSize: 10, resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'realtime-product-search', endpoint, totalCalls: totalCallsMade });
        return;
    }

    // ── Store Reviews (cursor-based) ──
    if (endpoint === '/store-reviews') {
        if (!args.storeDomain) { console.error('Error: --store-domain required for /store-reviews'); process.exit(1); }
        const params = { store_domain: args.storeDomain, limit: Math.min(count, 10), country: args.country || 'us', language: args.language || 'en' };
        if (args.sortBy) params.sort_by = args.sortBy;
        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/store-reviews', params, apiKey, count,
            pagination: 'cursor', cursorParam: 'cursor', cursorPath: 'cursor',
            pageSize: 10, resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'realtime-product-search', endpoint, totalCalls: totalCallsMade });
        return;
    }

    // ── Search / Deals endpoints (page-based) ──
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const params = {
        q: args.query, limit: pageSize,
        country: args.country || 'us', language: args.language || 'en',
    };
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.condition) params.product_condition = args.condition;
    if (args.stores) params.stores = args.stores;
    if (args.freeShipping) params.free_shipping = true;
    if (args.freeReturns) params.free_returns = true;
    if (args.onSale) params.on_sale = true;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint, params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize,
        resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} products in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-product-search', endpoint, query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
