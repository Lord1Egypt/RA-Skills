#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search Amazon products, get details, and fetch reviews.

Required (varies by endpoint):
  --query         Search query (for /search)
  --asin          Single ASIN (for /product-details, /product-reviews, /top-product-reviews, /product-offers)
  --asins         Comma-separated ASINs for batch /product-details

Optional:
  --endpoint      Endpoint: /search (default), /product-details, /product-reviews, /top-product-reviews, /product-offers, /best-sellers, /deals-v2
  --count         Max results to fetch (default: 50)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --country       Country code (default: US)
  --language      Language code (e.g. en_US)
  --sort-by       Sort: RELEVANCE, LOWEST_PRICE, HIGHEST_PRICE, REVIEWS, NEWEST, BEST_SELLERS (search); TOP_REVIEWS, newest, etc (reviews)
  --category      Category ID (for /best-sellers or /search filter)
  --min-price     Min price filter (search)
  --max-price     Max price filter (search)
  --brand         Brand filter (search)
  --star-rating   Review star filter: ALL, 5_STARS, 4_STARS, 3_STARS, 2_STARS, 1_STARS, POSITIVE, CRITICAL
  --is-prime      Filter Prime-only (TRUE/FALSE)
  --cookie        Logged-in Amazon cookie (required for /product-reviews)
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
    const meta = loadMeta('realtime-amazon-data');
    const host = meta.rapidapi_host || 'real-time-amazon-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const country = args.country || 'US';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `realtime-amazon-data_${ts}.${format}`);

    // ── Product Details (single or batch) ────────────────────────────────────
    if (endpoint === '/product-details') {
        const asins = args.asins ? args.asins.split(',').map(a => a.trim()).filter(Boolean) : (args.asin ? [args.asin] : []);
        if (!asins.length) { console.error('Error: --asin or --asins required for /product-details'); process.exit(1); }

        const allResults = [];
        let totalCalls = 0;
        for (let i = 0; i < asins.length; i++) {
            if (i > 0) await sleep(300);
            totalCalls++;
            if (totalCalls > maxCalls) { console.error(`Cost cap (${maxCalls}). Use --max-calls to raise.`); break; }
            console.error(`  [${i + 1}/${asins.length}] ASIN: ${asins[i]}`);
            try {
                const params = { asin: asins[i], country };
                if (args.language) params.language = args.language;
                const data = await apiCall(host, '/product-details', params, apiKey);
                const record = data.data || data;
                allResults.push(record);
            } catch (e) { console.error(`    Error: ${e.message}`); }
            if (dryRun) break;
        }
        if (dryRun) { console.log(JSON.stringify(allResults.slice(0, 3), null, 2)); return; }
        writeOutput(allResults, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/product-details', totalCalls });
        return;
    }

    // ── Top Product Reviews (no pagination, no cookie) ───────────────────────
    if (endpoint === '/top-product-reviews') {
        if (!args.asin) { console.error('Error: --asin required for /top-product-reviews'); process.exit(1); }
        const params = { asin: args.asin, country };
        if (args.language) params.language = args.language;
        const data = await apiCall(host, '/top-product-reviews', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 3), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/top-product-reviews', totalCalls: 1 });
        return;
    }

    // ── Product Reviews (paginated, requires cookie) ─────────────────────────
    if (endpoint === '/product-reviews') {
        if (!args.asin) { console.error('Error: --asin required for /product-reviews'); process.exit(1); }
        if (!args.cookie) { console.error('Error: --cookie required for /product-reviews (logged-in Amazon cookie)'); process.exit(1); }
        const params = { asin: args.asin, country, cookie: args.cookie };
        if (args.language) params.language = args.language;
        if (args.sortBy) params.sort_by = args.sortBy;
        if (args.starRating) params.star_rating = args.starRating;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-reviews', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 10,
            resultsPath: 'data.reviews', dryRun, delay: 300, maxCalls,
        });
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/product-reviews', asin: args.asin, totalCalls: totalCallsMade });
        return;
    }

    // ── Product Offers (paginated) ───────────────────────────────────────────
    if (endpoint === '/product-offers') {
        if (!args.asin) { console.error('Error: --asin required for /product-offers'); process.exit(1); }
        const params = { asin: args.asin, country, limit: 100 };
        if (args.language) params.language = args.language;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/product-offers', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 100,
            resultsPath: 'data.product_offers', dryRun, delay: 300, maxCalls,
        });
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/product-offers', asin: args.asin, totalCalls: totalCallsMade });
        return;
    }

    // ── Best Sellers (paginated) ─────────────────────────────────────────────
    if (endpoint === '/best-sellers') {
        if (!args.category) { console.error('Error: --category required for /best-sellers'); process.exit(1); }
        const params = { category: args.category, country };
        if (args.language) params.language = args.language;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/best-sellers', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 30,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/best-sellers', category: args.category, totalCalls: totalCallsMade });
        return;
    }

    // ── Deals ────────────────────────────────────────────────────────────────
    if (endpoint === '/deals-v2') {
        const params = { country };
        if (args.language) params.language = args.language;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/deals-v2', params, apiKey, count,
            pagination: 'offset', offsetParam: 'offset', pageSize: 30,
            resultsPath: 'data.deals', dryRun, delay: 300, maxCalls,
        });
        if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
        writeOutput(results, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/deals-v2', totalCalls: totalCallsMade });
        return;
    }

    // ── Search (default, paginated) ──────────────────────────────────────────
    if (!args.query) { console.error('Error: --query required for /search. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query, country };
    if (args.language) params.language = args.language;
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.category) params.category_id = args.category;
    if (args.minPrice) params.min_price = args.minPrice;
    if (args.maxPrice) params.max_price = args.maxPrice;
    if (args.brand) params.brand = args.brand;
    if (args.isPrime) params.is_prime = args.isPrime;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize: 60,
        resultsPath: 'data.products', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} products in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'realtime-amazon-data', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
