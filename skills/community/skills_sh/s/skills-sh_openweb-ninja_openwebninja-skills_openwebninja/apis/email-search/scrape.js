#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, toCSV, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search_query> --domain <email_domain> [options]

Search the web for email addresses matching a query and domain.

Required:
  --query           Search query (e.g. "Car Dealer California USA")
  --domain          Email domain to search (e.g. "gmail.com" or "company.com")

Optional:
  --limit           Max emails to return (default: 5000, API max: 5000)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --dry-run         Print response to console only, do not write file
  --max-calls       Cost cap: max API calls (default: 1)
  --help            Show this help
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
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }
    if (!args.domain) { console.error('Error: --domain required. Use --help for usage.'); process.exit(1); }

    const apiKey = getApiKey();
    const meta = loadMeta('email-search');
    const host = meta.rapidapi_host || 'email-search16.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const limit = parseInt(args.limit, 10) || 5000;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const safeQuery = args.query.replace(/[^a-zA-Z0-9]/g, '_').slice(0, 40);
    const outputPath = args.output || path.join('output', `email-search_${safeQuery}_${ts}.${format}`);

    const params = {
        query: args.query,
        email_domain: args.domain,
        limit: limit,
    };

    console.error(`Searching emails for "${args.query}" @ ${args.domain} (limit: ${limit})...`);
    const data = await apiCall(host, '/search-emails', params, apiKey);

    // Extract email list from response
    const emails = Array.isArray(data) ? data
        : Array.isArray(data.emails) ? data.emails
        : Array.isArray(data.results) ? data.results
        : Array.isArray(data.data) ? data.data
        : [data];

    const records = emails.map(e => typeof e === 'string' ? { email: e } : e);

    if (dryRun) {
        console.log(JSON.stringify(records.slice(0, 20), null, 2));
        console.error(`\n(showing first 20 of ${records.length} results — dry-run mode)`);
        return;
    }

    writeOutput(records, outputPath, format, {
        api: 'email-search',
        endpoint: '/search-emails',
        query: args.query,
        domain: args.domain,
        totalCalls: 1,
    });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
