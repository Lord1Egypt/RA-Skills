#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Scrape Glassdoor company data, reviews, and salaries.

Required (varies by endpoint):
  --query         Search query (for /company-search)
  --company-id    Glassdoor company ID (for /company-overview, /company-reviews, /company-salaries-v2)

Optional:
  --endpoint      Endpoint: /company-search (default), /company-overview, /company-reviews, /company-salaries-v2
  --count         Max results for paginated endpoints (default: 100)
  --format        json | csv (default: json)
  --output        Output file path (auto-generated if omitted)
  --domain        Glassdoor domain (default: www.glassdoor.com)
  --sort          Sort order (varies by endpoint)
  --language      Language code: en, fr, nl, de, pt, es, it (for reviews)
  --job-title     Job title filter (for /company-salaries-v2)
  --location      Location filter (for /company-salaries-v2)
  --location-type Location type: ANY, CITY, STATE, COUNTRY
  --only-current  Only current employees: true/false (for reviews)
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

    const endpoint = args.endpoint || '/company-search';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-glassdoor-data');
    const host = meta.rapidapi_host || 'real-time-glassdoor-data.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 100;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 50;
    const glassdoorDomain = args.domain || 'www.glassdoor.com';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `glassdoor_${ts}.${format}`);

    // Company overview (no pagination)
    if (endpoint === '/company-overview') {
        if (!args.companyId) { console.error('Error: --company-id required for /company-overview'); process.exit(1); }
        const params = { company_id: args.companyId, domain: glassdoorDomain };
        const data = await apiCall(host, '/company-overview', params, apiKey);
        const records = data.data ? [data.data] : [data];
        writeOutput(records, outputPath, format, { api: 'realtime-glassdoor-data', endpoint: '/company-overview', totalCalls: 1 });
        return;
    }

    // Company reviews (page-based, param: page)
    if (endpoint === '/company-reviews') {
        if (!args.companyId) { console.error('Error: --company-id required for /company-reviews'); process.exit(1); }
        const params = { company_id: args.companyId, domain: glassdoorDomain };
        if (args.sort) params.sort = args.sort;
        if (args.language) params.language = args.language;
        if (args.query) params.query = args.query;
        if (args.onlyCurrent) params.only_current_employees = args.onlyCurrent;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/company-reviews', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 10,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'realtime-glassdoor-data', endpoint: '/company-reviews', companyId: args.companyId, totalCalls: totalCallsMade });
        return;
    }

    // Company salaries v2 (page-based, param: page)
    if (endpoint === '/company-salaries-v2') {
        if (!args.companyId) { console.error('Error: --company-id required for /company-salaries-v2'); process.exit(1); }
        const params = { company_id: args.companyId, domain: glassdoorDomain };
        if (args.jobTitle) params.job_title = args.jobTitle;
        if (args.location) params.location = args.location;
        if (args.locationType) params.location_type = args.locationType;
        if (args.sort) params.sort = args.sort;

        const { results, totalCallsMade } = await fetchAll({
            host, endpoint: '/company-salaries-v2', params, apiKey, count,
            pagination: 'page_number', pageParam: 'page', pageSize: 10,
            resultsPath: 'data', dryRun, delay: 300, maxCalls,
        });
        writeOutput(results, outputPath, format, { api: 'realtime-glassdoor-data', endpoint: '/company-salaries-v2', companyId: args.companyId, totalCalls: totalCallsMade });
        return;
    }

    // Company search (no pagination — uses limit param)
    if (endpoint === '/company-search') {
        if (!args.query) { console.error('Error: --query required for /company-search. Use --help for usage.'); process.exit(1); }
        const params = { query: args.query, limit: Math.min(count, 10), domain: glassdoorDomain };

        const data = await apiCall(host, '/company-search', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (Array.isArray(data) ? data : [data]);

        console.error(`${records.length} companies found.`);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 3), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-glassdoor-data', endpoint: '/company-search', query: args.query, totalCalls: 1 });
        return;
    }

    console.error(`Error: Unknown endpoint "${endpoint}". Use --help for usage.`);
    process.exit(1);
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
