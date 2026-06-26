#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> --location <loc> [options]

Scrape Yelp business data and reviews.

Required (varies by endpoint):
  --query         Search query (for /business-search)
  --location      Location (for /business-search, e.g. "San Francisco, CA, USA")
  --business-id   Yelp business ID or alias (for /business-details, /business-reviews)

Optional:
  --endpoint      Endpoint: /business-search (default), /business-details, /business-reviews
  --count         Max results (default: 100)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --sort-by       Search sort: RECOMMENDED, HIGHEST_RATED, REVIEW_COUNT (for /business-search)
  --sort          Review sort: BEST_MATCH, NEWEST, OLDEST, HIGHEST_RATED, LOWEST_RATED, ELITES
  --price-range   Price filter (for /business-search)
  --yelp-domain   Yelp domain (default: yelp.com)
  --language      Review language (default: en)
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

    const endpoint = args.endpoint || '/business-search';
    const apiKey = getApiKey();
    const meta = loadMeta('yelp-business-data');
    const host = meta.rapidapi_host || 'red-flower-business-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 100;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const yelpDomain = args.yelpDomain || 'yelp.com';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `yelp_${ts}.${format}`);

    // Business details (no pagination)
    if (endpoint === '/business-details') {
        if (!args.businessId) { console.error('Error: --business-id required for /business-details'); process.exit(1); }
        const params = { business_id: args.businessId, yelp_domain: yelpDomain };
        const data = await apiCall(host, '/business-details', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        writeOutput(records, outputPath, format, { api: 'yelp-business-data', endpoint: '/business-details', totalCalls: 1 });
        return;
    }

    // Business reviews (page-based, param: page, 10 per page)
    if (endpoint === '/business-reviews') {
        if (!args.businessId) { console.error('Error: --business-id required for /business-reviews'); process.exit(1); }
        const params = { business_id: args.businessId, yelp_domain: yelpDomain, page_size: 10, num_pages: 1 };
        if (args.sort) params.sort = args.sort;
        if (args.query) params.query = args.query;
        if (args.language) params.language = args.language;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/business-reviews', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 10,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'yelp-business-data', endpoint: '/business-reviews', businessId: args.businessId, totalCalls: totalCallsMade });
        return;
    }

    // Business search (offset-based, param: start)
    if (!args.query) { console.error('Error: --query required for /business-search. Use --help for usage.'); process.exit(1); }
    if (!args.location) { console.error('Error: --location required for /business-search. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query, location: args.location, yelp_domain: yelpDomain };
    if (args.sortBy) params.sort_by = args.sortBy;
    if (args.priceRange) params.price_range = args.priceRange;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/business-search', params, apiKey, count,
        pagination: 'offset', offsetParam: 'start', pageSize: 10,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} businesses in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'yelp-business-data', endpoint: '/business-search', query: args.query, location: args.location, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
