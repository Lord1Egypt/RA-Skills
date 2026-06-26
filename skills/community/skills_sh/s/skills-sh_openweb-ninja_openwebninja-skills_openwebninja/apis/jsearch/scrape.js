#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <search> [options]

Search jobs, get salary estimates, and export results.

Required:
  --query             Search query (e.g. "developer jobs in chicago")
                      For /estimated-salary this maps to --job-title

Optional:
  --endpoint          Endpoint: /search (default), /estimated-salary, /job-details
  --count             Max results (default: 50, page size fixed at 10)
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --location          Location for /estimated-salary (e.g. "new york")
  --remote            Filter remote jobs (work_from_home=true)
  --employment-type   FULLTIME | CONTRACTOR | PARTTIME | INTERN
  --date-posted       all | today | 3days | week | month (default: all)
  --country           Country code (default: us)
  --language          Language code (default: en)
  --radius            Search radius in km
  --job-id            Job ID for /job-details endpoint
  --experience        Experience filter: under_3_years_experience, more_than_3_years_experience, no_experience, no_degree
  --exclude-publishers  Comma-separated publishers to exclude (e.g. "BeeBe,Dice")
  --fields            Comma-separated fields to return
  --years-of-experience  For salary: ALL, LESS_THAN_ONE, ONE_TO_THREE, FOUR_TO_SIX, SEVEN_TO_NINE, TEN_TO_FOURTEEN, ABOVE_FIFTEEN
  --dry-run           Fetch first page only, print to console
  --max-calls         Safety cap on API calls (default: 20)
  --help              Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--remote') { args.remote = true; continue; }
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
    const meta = loadMeta('jsearch');
    const host = meta.rapidapi_host || 'jsearch.p.rapidapi.com';
    const count = parseInt(args.count, 10) || 50;
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const maxCalls = parseInt(args.maxCalls, 10) || 20;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `jsearch_${ts}.${format}`);

    // Job details
    if (endpoint === '/job-details') {
        if (!args.jobId) { console.error('Error: --job-id required for /job-details'); process.exit(1); }
        const params = { job_id: args.jobId };
        if (args.country) params.country = args.country;
        if (args.language) params.language = args.language;
        if (args.fields) params.fields = args.fields;
        const data = await apiCall(host, '/job-details', params, apiKey);
        const records = data.data ? (Array.isArray(data.data) ? data.data : [data.data]) : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'jsearch', endpoint: '/job-details', totalCalls: 1 });
        return;
    }

    // Estimated salary
    if (endpoint === '/estimated-salary') {
        const jobTitle = args.query || args.jobTitle;
        if (!jobTitle) { console.error('Error: --query (job title) required for /estimated-salary'); process.exit(1); }
        if (!args.location) { console.error('Error: --location required for /estimated-salary'); process.exit(1); }
        const params = { job_title: jobTitle, location: args.location };
        if (args.yearsOfExperience) params.years_of_experience = args.yearsOfExperience;
        if (args.fields) params.fields = args.fields;
        const data = await apiCall(host, '/estimated-salary', params, apiKey);
        const records = data.data ? (Array.isArray(data.data) ? data.data : [data.data]) : [data];
        if (dryRun) { console.log(JSON.stringify(records, null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'jsearch', endpoint: '/estimated-salary', query: jobTitle, totalCalls: 1 });
        return;
    }

    // Search
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const params = {
        query: args.query,
        num_pages: 1,
        country: args.country || 'us',
    };
    if (args.language) params.language = args.language;
    if (args.datePosted) params.date_posted = args.datePosted;
    if (args.remote) params.work_from_home = true;
    if (args.employmentType) params.employment_types = args.employmentType;
    if (args.experience) params.job_requirements = args.experience;
    if (args.radius) params.radius = args.radius;
    if (args.excludePublishers) params.exclude_job_publishers = args.excludePublishers;
    if (args.fields) params.fields = args.fields;

    // jsearch uses page-number pagination with fixed 10 results per page
    const { results: rawResults, totalCallsMade } = await fetchAll({
        host, endpoint: '/search', params, apiKey, count,
        pagination: 'page_number', pageParam: 'page', pageSize: 10,
        resultsPath: 'data', dryRun, delay: 300, maxCalls,
    });

    // jsearch nests jobs as data[].jobs[] — flatten page objects into individual job records
    const results = rawResults.flatMap(page => page.jobs || [page]);

    console.error(`${results.length} jobs in ${totalCallsMade} call(s).`);
    if (dryRun) { console.log(JSON.stringify(results.slice(0, 3), null, 2)); return; }
    writeOutput(results, outputPath, format, { api: 'jsearch', endpoint: '/search', query: args.query, totalCalls: totalCallsMade });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
