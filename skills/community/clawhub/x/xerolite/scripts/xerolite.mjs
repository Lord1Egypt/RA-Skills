#!/usr/bin/env node

/**
 * Xerolite API CLI
 *
 * Env (optional):
 *   XEROLITE_API_URL  Base URL for Xerolite API. If not set, defaults to http://localhost.
 *   XEROLITE_AGENTIC_API_KEY  API key for agentic endpoints.
 *   XEROLITE_VERBOSE=1  Log request URL, headers (API key shown partially), body on stderr.
 *
 * This version requires API key authorization for agentic endpoints.
 *
 * Commands:
 *   node xerolite.mjs order place --symbol AAPL --currency USD --asset-class STOCK --exch SMART --action BUY --qty 10 [--api-key YOUR_KEY]
 *   node xerolite.mjs contract search --symbol AAPL --currency USD --asset-class STOCK --exch SMART [--api-key YOUR_KEY]
 *   node xerolite.mjs portfolio get [--api-key YOUR_KEY]
 *
 * Logging:
 *   By default, only the HTTP response is printed. Verbose: URL + headers (partial API key for local/debug) + body on stderr.
 */

const [, , cmd, subcmd, ...args] = process.argv;

const VERBOSE =
  process.env.XEROLITE_VERBOSE === '1' ||
  process.env.XEROLITE_VERBOSE === 'true' ||
  args.includes('--verbose') ||
  args.includes('-v');

/** Strip --verbose / -v from args so they are not treated as command flags. */
const argvForFlags = args.filter((a) => a !== '--verbose' && a !== '-v');

/** Verbose-only: show first/last few chars so you can tell keys apart; not for shared logs. */
function maskApiKeyForVerboseLog(value) {
  const v = String(value);
  if (v.length <= 10) return '****';
  return `${v.slice(0, 4)}…${v.slice(-4)} (len ${v.length})`;
}

function headersForVerboseLog(headers) {
  const h = { ...headers };
  if (h['X-Agentic-Api-Key'] != null) {
    h['X-Agentic-Api-Key'] = maskApiKeyForVerboseLog(h['X-Agentic-Api-Key']);
  }
  return h;
}

if (!cmd || !subcmd) {
  console.error('Usage:');
  console.error('  node xerolite.mjs order place --symbol AAPL --currency USD --asset-class STOCK --exch SMART --action BUY --qty 10');
  console.error('  node xerolite.mjs contract search --symbol AAPL --currency USD --asset-class STOCK --exch SMART');
  console.error('  node xerolite.mjs portfolio get');
  process.exit(1);
}

const baseUrl = (process.env.XEROLITE_API_URL && process.env.XEROLITE_API_URL.trim() !== '')
  ? process.env.XEROLITE_API_URL.trim()
  : 'http://localhost';

/** Default flag values when not provided (reduces required flags). */
const FLAG_DEFAULTS = {
  'currency': 'USD',
  'asset-class': 'STOCK',
  exch: 'SMART',
};

function parseFlags(rest) {
  const result = {};
  for (let i = 0; i < rest.length; i++) {
    const token = rest[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const value = rest[i + 1];
      if (!value || value.startsWith('--')) {
        console.error(`Missing value for flag --${key}`);
        process.exit(1);
      }
      result[key] = value;
      i++;
    }
  }
  return result;
}

/** Apply default values for flags that were not provided. */
function applyDefaults(flags) {
  return { ...FLAG_DEFAULTS, ...flags };
}

function buildBody(command, subcommand, flags) {
  if (command === 'contract' && subcommand === 'search') {
    const flagsWithDefaults = applyDefaults(flags);
    const { symbol, currency, 'asset-class': assetClass } = flagsWithDefaults;
    if (!symbol) {
      console.error('contract search requires --symbol (optional: --currency, --asset-class, --exch; default: USD, STOCK, SMART)');
      process.exit(1);
    }
    return {
      brokerName: 'IBKR',
      symbol,
      currency,
      xeroAssetClass: assetClass
    };
  }

  if (command === 'order' && subcommand === 'place') {
    const flagsWithDefaults = applyDefaults(flags);
    const { action, qty, symbol, currency, 'asset-class': assetClass, exch } = flagsWithDefaults;
    if (!action || !qty || !symbol) {
      console.error('order place requires --action --qty --symbol (optional: --currency, --asset-class, --exch; default: USD, STOCK, SMART)');
      process.exit(1);
    }
    return {
      name: 'Agent',
      action,
      qty: String(qty),
      symbol,
      currency,
      asset_class: assetClass,
      exch,
    };
  }

  if (command === 'portfolio' && subcommand === 'get') {
    return {};
  }

  console.error(`Unknown command: ${command} ${subcommand}`);
  process.exit(1);
}

function resolvePath(command, subcommand) {
  if (command === 'contract' && subcommand === 'search') {
    return '/api/agentic/contract/search';
  }
  if (command === 'order' && subcommand === 'place') {
    return '/api/agentic/order/place-order';
  }
  if (command === 'portfolio' && subcommand === 'get') {
    return '/api/agentic/portfolio';
  }
  console.error(`No path configured for command: ${command} ${subcommand}`);
  process.exit(1);
}

async function main() {
  const flags = parseFlags(argvForFlags);
  const apiKey = flags['api-key'] || process.env.XEROLITE_AGENTIC_API_KEY;
  delete flags['api-key'];

  if (!apiKey || String(apiKey).trim() === '') {
    console.error('Missing API key. Provide --api-key or set XEROLITE_AGENTIC_API_KEY.');
    process.exit(1);
  }

  const body = buildBody(cmd, subcmd, flags);
  const path = resolvePath(cmd, subcmd);

  const url = new URL(path, baseUrl).toString();

  const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Agentic-Api-Key': apiKey,
  };

  if (VERBOSE) {
    console.error('[xerolite] POST', url);
    console.error('[xerolite] headers', headersForVerboseLog(headers));
    console.error('[xerolite] body', JSON.stringify(body, null, 2));
  }

  const res = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  const text = await res.text();

  if (!res.ok) {
    console.error(`Status: ${res.status} ${res.statusText}`);
  } else {
    console.log(`Status: ${res.status} ${res.statusText}`);
  }
  if (text) {
    try {
      const json = JSON.parse(text);
      console.log(JSON.stringify(json, null, 2));
    } catch {
      console.log(text);
    }
  }

  if (!res.ok) {
    process.exit(1);
  }
}

main().catch(err => {
  console.error('Request failed:', err.message || err);
  process.exit(1);
});
