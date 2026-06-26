#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Scrape Trustpilot company data and reviews.

Required (varies by endpoint):
  --query         Search query (for /company-search)
  --domain        Company domain (for /company-details, /company-reviews)

Optional:
  --endpoint      Endpoint: /company-search (default), /company-details, /company-reviews
  --count         Max results for paginated endpoints (default: 100)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --locale        Locale (default: en-US)
  --sort          Review sort: most_relevant, recency (for /company-reviews)
  --rating        Filter reviews by rating: 1, 2, 3, 4, 5
  --date-posted   Filter by date: any, last_12_months, last_6_months, last_3_months, last_30_days
  --verified      Only verified reviews (for /company-reviews)
  --min-rating    Min company rating: any, 3, 4, 4.5 (for /company-search)
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
        if (arg === '--verified') { args.verified = true; continue; }
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

    const endpoint = args.endpoint || '/company-search';
    const apiKey = getApiKey();
    const meta = loadMeta('trustpilot-company-and-reviews');
    const host = meta.rapidapi_host || 'trustpilot-company-and-reviews-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 100;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const locale = args.locale || 'en-US';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `trustpilot_${ts}.${format}`);

    // Company details (no pagination)
    if (endpoint === '/company-details') {
        if (!args.domain) { console.error('Error: --domain required for /company-details'); process.exit(1); }
        const params = { company_domain: args.domain, locale };
        const data = await apiCall(host, '/company-details', params, apiKey);
        const records = data.data ? [data.data] : [data];
        writeOutput(records, outputPath, format, { api: 'trustpilot-company-and-reviews', endpoint: '/company-details', totalCalls: 1 });
        return;
    }

    // Company reviews (page-based, 20 per page, capped ~200)
    if (endpoint === '/company-reviews') {
        if (!args.domain) { console.error('Error: --domain required for /company-reviews'); process.exit(1); }
        const reviewCount = Math.min(count, 200); // Reviews capped at ~200 without auth cookie
        const params = { company_domain: args.domain, locale };
        if (args.sort) params.sort = args.sort;
        if (args.rating) params.rating = args.rating;
        if (args.datePosted) params.date_posted = args.datePosted;
        if (args.verified) params.verified = true;
        if (args.query) params.query = args.query;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/company-reviews', params, apiKey, count: reviewCount,
            pagination: 'page_number', pageParam: 'page', pageSize: 20,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'trustpilot-company-and-reviews', endpoint: '/company-reviews', domain: args.domain, totalCalls: totalCallsMade });
        return;
    }

    // Company search (page-based)
    if (!args.query) { console.error('Error: --query required for /company-search. Use --help for usage.'); process.exit(1); }

    const params = { query: args.query, locale };
    if (args.minRating) params.min_rating = args.minRating;
    if (args.minReviewCount) params.min_review_count = args.minReviewCount;

    const { results, totalCallsMade } = await fetchAll({
        host, endpoint: '/company-search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize: 20,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    console.error(`${results.length} companies in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'trustpilot-company-and-reviews', endpoint: '/company-search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
