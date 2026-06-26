#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, toCSV, writeOutput } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --query <name_or_topic> [options]

Search for social media profile links for a person or topic.

Required:
  --query             Search query (e.g. "John Smith" or "OpenAI")

Optional:
  --social-networks   Comma-separated list of networks to search
                      (default: facebook,tiktok,instagram,snapchat,twitter,youtube,linkedin,github)
  --format            json | csv (default: json)
  --output            Output file path (auto-generated if omitted)
  --dry-run           Print response to console only, do not write file
  --max-calls         Cost cap: max API calls (default: 1)
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
    if (!args.query) { console.error('Error: --query required. Use --help for usage.'); process.exit(1); }

    const apiKey = getApiKey();
    const meta = loadMeta('social-links-search');
    const host = meta.rapidapi_host || 'social-links-search.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const safeQuery = args.query.replace(/[^a-zA-Z0-9]/g, '_').slice(0, 40);
    const outputPath = args.output || path.join('output', `social-links_${safeQuery}_${ts}.${format}`);

    const params = { query: args.query };
    if (args.socialNetworks) params.social_networks = args.socialNetworks;

    console.error(`Searching social links for "${args.query}"...`);
    const data = await apiCall(host, '/search-social-links', params, apiKey);

    // Flatten social links into records
    const socialData = data.data || data.results || data;
    let records;
    if (Array.isArray(socialData)) {
        records = socialData;
    } else if (typeof socialData === 'object' && socialData !== null) {
        // Response is typically { facebook: [...], twitter: [...], ... }
        records = [];
        for (const [network, links] of Object.entries(socialData)) {
            if (Array.isArray(links)) {
                for (const link of links) {
                    if (typeof link === 'string') {
                        records.push({ network, url: link });
                    } else if (typeof link === 'object') {
                        records.push({ network, ...link });
                    }
                }
            } else if (typeof links === 'string') {
                records.push({ network, url: links });
            }
        }
        // If no flattening happened, wrap the whole object
        if (!records.length) records = [{ query: args.query, raw: socialData }];
    } else {
        records = [{ query: args.query, raw: data }];
    }

    if (dryRun) {
        console.log(JSON.stringify(records, null, 2));
        return;
    }

    writeOutput(records, outputPath, format, {
        api: 'social-links-search',
        endpoint: '/search-social-links',
        query: args.query,
        totalCalls: 1,
    });
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
