#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --job-title <title> --location <location> [options]

Fetch job salary estimates by role and location, sourced from Glassdoor.

Required:
  --job-title         Job title to search (e.g. "software engineer")
  --location          Location to search in (e.g. "New York, NY" or "United States")

Optional:
  --endpoint          /job-salary (default) or /company-job-salary
  --company           Company name — required for /company-job-salary (e.g. "Google")
  --location-type     CITY | STATE | COUNTRY | ANY (default: ANY)
  --years-of-experience  Experience range: 0-1, 1-3, 3-5, 5-10, 10-15, 15+ (default: ALL)
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --dry-run           Fetch data and print to console without saving
  --max-calls         Safety cap on API calls (default: 10)
  --help              Show this help
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

    const endpoint = args.endpoint || '/job-salary';
    const apiKey = getApiKey();
    const meta = loadMeta('job-salary-data');
    const host = meta.rapidapi_host || 'job-salary-data.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `job-salary-data_${ts}.${format}`);

    if (!args.jobTitle) { console.error('Error: --job-title required. Use --help for usage.'); process.exit(1); }
    if (!args.location && endpoint === '/job-salary') { console.error('Error: --location required. Use --help for usage.'); process.exit(1); }
    if (endpoint === '/company-job-salary' && !args.company) { console.error('Error: --company required for /company-job-salary. Use --help for usage.'); process.exit(1); }

    const params = { job_title: args.jobTitle };

    if (endpoint === '/job-salary') {
        params.location = args.location;
        if (args.locationType) params.location_type = args.locationType;
        if (args.yearsOfExperience) params.years_of_experience = args.yearsOfExperience;
    } else {
        params.company_name = args.company;
        if (args.location) params.location = args.location;
        if (args.locationType) params.location_type = args.locationType;
        if (args.yearsOfExperience) params.years_of_experience = args.yearsOfExperience;
    }

    console.error(`Calling ${endpoint} for "${args.jobTitle}"...`);
    const data = await apiCall(host, endpoint, params, apiKey);
    const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);

    console.error(`${records.length} result(s) returned.`);
    if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
    writeOutput(records, outputPath, format, { api: 'job-salary-data', endpoint, jobTitle: args.jobTitle, totalCalls: 1 });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
