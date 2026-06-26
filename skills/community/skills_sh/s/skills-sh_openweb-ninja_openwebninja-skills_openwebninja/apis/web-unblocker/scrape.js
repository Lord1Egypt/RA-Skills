#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --url <target-url> [options]

Fetch a web page via the Web Unblocker API with smart retries, optional
JavaScript rendering, and proxy support.

Required:
  --url               URL to fetch / unblock

Rendering:
  --render-js         Enable JavaScript rendering (default: false)
  --wait-until        Page load condition: domloaded | load | networkidle (default: load)
  --wait-for-selector CSS selector to wait for before returning content
  --wait-for-timeout  Seconds to wait after page load
  --load-images       Allow image loading during JS render (default: false)
  --load-stylesheets  Allow stylesheet loading during JS render (default: false)
  --networkidle-timeout  Network idle timeout in seconds (default: 0.5)

Reliability:
  --extra-retries     Enable additional internal retries (costs 2 credits if triggered)
  --success-codes     Comma-separated HTTP codes considered successful (default: 200)
  --success-selectors CSS selectors indicating success if found
  --failure-selectors CSS selectors triggering failure/retry if found
  --min-response-len  Minimum response body size in bytes

Request:
  --method            HTTP method: GET | POST | PUT | PATCH | DELETE (default: GET)
  --body              Request payload for POST/PUT/PATCH
  --proxy             Proxy URL for the request

Output:
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --dry-run           Print response to console, don't save
  --help              Show this help
`);
}

function parseArgs(argv) {
    const args = {};
    for (let i = 2; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help') { args.help = true; continue; }
        if (arg === '--dry-run') { args.dryRun = true; continue; }
        if (arg === '--render-js') { args.renderJs = true; continue; }
        if (arg === '--load-images') { args.loadImages = true; continue; }
        if (arg === '--load-stylesheets') { args.loadStylesheets = true; continue; }
        if (arg === '--extra-retries') { args.extraRetries = true; continue; }
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

    if (!args.url) {
        console.error('Error: --url is required. Use --help for usage.');
        process.exit(1);
    }

    const apiKey = getApiKey();
    const meta = loadMeta('web-unblocker');
    const host = meta.rapidapi_host || 'web-unblocker1.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const outputPath = args.output || path.join('output', `web-unblocker_${ts}.${format}`);

    // ── Build request body ────────────────────────────────────────────────────
    const body = { url: args.url };

    if (args.renderJs)          body.render_js = true;
    if (args.waitUntil)         body.wait_until = args.waitUntil;
    if (args.waitForSelector)   body.wait_for_selector = args.waitForSelector;
    if (args.waitForTimeout)    body.wait_for_timeout = args.waitForTimeout;
    if (args.loadImages)        body.load_images = true;
    if (args.loadStylesheets)   body.load_stylesheets = true;
    if (args.networkidleTimeout) body.networkidle_timeout = parseFloat(args.networkidleTimeout);
    if (args.extraRetries)      body.extra_retries = true;
    if (args.minResponseLen)    body.min_response_length = parseInt(args.minResponseLen, 10);
    if (args.proxy)             body.proxy = args.proxy;
    if (args.body)              body.body = args.body;

    if (args.successCodes) {
        body.success_status_codes = args.successCodes.split(',').map(Number);
    }
    if (args.successSelectors) body.success_selectors = args.successSelectors;
    if (args.failureSelectors) body.failiure_selectors = args.failureSelectors;

    const httpMethod = (args.method || 'GET').toUpperCase();

    console.error(`Fetching: ${args.url}`);
    console.error(`  JS rendering: ${body.render_js ? 'on' : 'off'}, method: ${httpMethod}`);

    const data = await apiCall(host, '/request', {}, apiKey, 'POST', body);

    const records = [data];

    if (dryRun) {
        // For dry-run, show a summary: status, content length, snippet
        const htmlBody = (data.data && data.data.body) || data.body || data.html;
        const summary = {
            url: args.url,
            statusCode: (data.data && data.data.status) || data.status_code || data.statusCode,
            finalUrl: (data.data && data.data.final_url) || data.final_url,
            contentLength: htmlBody ? htmlBody.length : null,
            bodySnippet: (htmlBody || JSON.stringify(data)).slice(0, 500),
        };
        console.log(JSON.stringify(summary, null, 2));
        return;
    }

    writeOutput(records, outputPath, format, {
        api: 'web-unblocker',
        endpoint: '/request',
        url: args.url,
        renderJs: !!body.render_js,
        totalCalls: 1,
    });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
