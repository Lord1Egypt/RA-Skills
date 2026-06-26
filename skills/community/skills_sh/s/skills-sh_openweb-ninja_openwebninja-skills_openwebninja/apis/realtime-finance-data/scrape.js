#!/usr/bin/env node
'use strict';

const { getApiKey, loadMeta, apiCall, fetchAll, toCSV, writeOutput, sleep } = require('../../lib/utils');
const path = require('path');

function printHelp() {
    console.log(`
Usage: node scrape.js --endpoint <endpoint> [options]

Fetch financial data (stocks, currencies, market trends) and export results.

Endpoints:
  /search                        Search for stocks/symbols (requires --query)
  /market-trends                 Market trends (requires --trend-type)
  /stock-quote                   Stock quote (requires --symbol)
  /stock-time-series             Stock time series (requires --symbol)
  /stock-news                    Stock news (requires --symbol)
  /stock-overview                Stock/company overview (requires --symbol)
  /company-income-statement      Income statement (requires --symbol)
  /company-balance-sheet         Balance sheet (requires --symbol)
  /company-cash-flow             Cash flow (requires --symbol)
  /currency-exchange-rate        Exchange rate (requires --from-symbol, --to-symbol)
  /currency-time-series          Currency time series (requires --from-symbol, --to-symbol)
  /currency-news                 Currency news (requires --from-symbol, --to-symbol)
  /stock-quote-yahoo-finance     Yahoo Finance quote (requires --symbol)
  /stock-time-series-yahoo-finance  Yahoo Finance time series (requires --symbol)

Required (varies by endpoint):
  --query           Search query (for /search)
  --symbol          Stock symbol, e.g. AAPL (for stock endpoints)
  --trend-type      Trend type, e.g. MARKET_INDEXES (for /market-trends)
  --from-symbol     Source currency, e.g. USD (for currency endpoints)
  --to-symbol       Target currency, e.g. EUR (for currency endpoints)

Optional:
  --endpoint        Endpoint (default: /search)
  --period          Time period, e.g. 1D, 5D, 1M, 6M, 1Y, 5Y (for time series)
  --language        Language code (default: en)
  --country         Country code (default: us, for /market-trends)
  --format          json | csv (default: json)
  --output          Output file path (auto-generated if omitted)
  --dry-run         Print to console, don't save
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

    const endpoint = args.endpoint || '/search';
    const apiKey = getApiKey();
    const meta = loadMeta('realtime-finance-data');
    const host = meta.rapidapi_host || 'real-time-finance-data.p.rapidapi.com';
    const format = args.format || 'json';
    const dryRun = !!args.dryRun;
    const language = args.language || 'en';

    const ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const safeName = endpoint.replace(/\//g, '_').slice(1);
    const outputPath = args.output || path.join('output', `realtime-finance-data_${safeName}_${ts}.${format}`);

    // ── /search ──────────────────────────────────────────────────────────────
    if (endpoint === '/search') {
        if (!args.query) { console.error('Error: --query required for /search'); process.exit(1); }
        const params = { query: args.query, language };
        const data = await apiCall(host, '/search', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-finance-data', endpoint: '/search', query: args.query, totalCalls: 1 });
        return;
    }

    // ── /market-trends ───────────────────────────────────────────────────────
    if (endpoint === '/market-trends') {
        if (!args.trendType) { console.error('Error: --trend-type required for /market-trends'); process.exit(1); }
        const params = { trend_type: args.trendType, country: args.country || 'us', language };
        const data = await apiCall(host, '/market-trends', params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-finance-data', endpoint: '/market-trends', trendType: args.trendType, totalCalls: 1 });
        return;
    }

    // ── Stock endpoints (require --symbol) ───────────────────────────────────
    const stockEndpoints = ['/stock-quote', '/stock-time-series', '/stock-news', '/stock-overview',
        '/company-income-statement', '/company-balance-sheet', '/company-cash-flow',
        '/stock-quote-yahoo-finance', '/stock-time-series-yahoo-finance'];
    if (stockEndpoints.includes(endpoint)) {
        if (!args.symbol) { console.error(`Error: --symbol required for ${endpoint}`); process.exit(1); }
        const params = { symbol: args.symbol, language };
        if (args.period) params.period = args.period;
        const data = await apiCall(host, endpoint, params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-finance-data', endpoint, symbol: args.symbol, totalCalls: 1 });
        return;
    }

    // ── Currency endpoints (require --from-symbol, --to-symbol) ──────────────
    const currencyEndpoints = ['/currency-exchange-rate', '/currency-time-series', '/currency-news'];
    if (currencyEndpoints.includes(endpoint)) {
        if (!args.fromSymbol || !args.toSymbol) { console.error(`Error: --from-symbol and --to-symbol required for ${endpoint}`); process.exit(1); }
        const params = { from_symbol: args.fromSymbol, to_symbol: args.toSymbol, language };
        if (args.period) params.period = args.period;
        const data = await apiCall(host, endpoint, params, apiKey);
        const records = Array.isArray(data.data) ? data.data : (data.data ? [data.data] : [data]);
        if (dryRun) { console.log(JSON.stringify(records.slice(0, 5), null, 2)); return; }
        writeOutput(records, outputPath, format, { api: 'realtime-finance-data', endpoint, fromSymbol: args.fromSymbol, toSymbol: args.toSymbol, totalCalls: 1 });
        return;
    }

    console.error(`Error: unknown endpoint "${endpoint}". Use --help for available endpoints.`);
    process.exit(1);
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
