#!/usr/bin/env node

/**
 * Firecrawl API Helper Script
 * Provides a CLI wrapper around Firecrawl endpoints for skill integration.
 *
 * Usage:
 *   node firecrawl-api.js <scrape|crawl|map|batch-scrape|crawl-status> [<json-string>]
 *   cat payload.json | node firecrawl-api.js scrape
 *   node firecrawl-api.js scrape --file ./payload.json
 *   node firecrawl-api.js crawl --wait < payload.json
 *   node firecrawl-api.js crawl-status <crawl-id> [--wait]
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_BASE = 'https://api.firecrawl.dev';

function loadApiKey() {
  if (process.env.FIRECRAWL_API_KEY) {
    return process.env.FIRECRAWL_API_KEY;
  }

  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) {
    return null;
  }

  const envContent = fs.readFileSync(envPath, 'utf8');
  const match = envContent.match(/FIRECRAWL_API_KEY\s*=\s*(.+)/);
  if (!match) {
    return null;
  }

  return match[1].trim().replace(/^[\"']|[\"']$/g, '');
}

function usage() {
  const cmd = path.basename(process.argv[1] || 'firecrawl-api.js');
  console.error(
    [
      'Usage:',
      `  node ${cmd} <scrape|crawl|map|batch-scrape|crawl-status> [<json-string>]`,
      `  cat payload.json | node ${cmd} scrape`,
      `  node ${cmd} scrape --file ./payload.json`,
      `  node ${cmd} crawl --wait < payload.json`,
      `  node ${cmd} crawl-status <crawl-id> [--wait]`,
      '',
      'Options:',
      '  --wait  Wait for crawl job completion (crawl / crawl-status only)',
      '  --id    Crawl job id (crawl-status only)',
      '',
      'Env:',
      '  FIRECRAWL_API_KEY (env var) or .env file next to this script',
    ].join('\n'),
  );
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => {
      data += chunk;
    });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

async function readPayload(args) {
  const fileFlagIndex = args.findIndex((arg) => arg === '--file');
  if (fileFlagIndex !== -1) {
    const filePath = args[fileFlagIndex + 1];
    if (!filePath) {
      throw new Error('Missing value for --file');
    }
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  }

  const dataFlagIndex = args.findIndex((arg) => arg === '--data');
  if (dataFlagIndex !== -1) {
    const json = args[dataFlagIndex + 1];
    if (!json) {
      throw new Error('Missing value for --data');
    }
    return JSON.parse(json);
  }

  if (args[0] && !args[0].startsWith('-')) {
    return JSON.parse(args[0]);
  }

  if (process.stdin.isTTY) {
    throw new Error('No payload provided (pass JSON arg, --data, --file, or pipe via stdin)');
  }

  const stdin = await readStdin();
  if (!stdin.trim()) {
    throw new Error('Empty stdin payload');
  }
  return JSON.parse(stdin);
}

function requestJson(method, endpointPath, apiKey, payload) {
  return new Promise((resolve, reject) => {
    const body = payload === undefined ? null : JSON.stringify(payload);
    const url = new URL(endpointPath, API_BASE);

    const req = https.request(
      url,
      {
        method,
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          ...(body === null
            ? {}
            : {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body),
              }),
          'User-Agent': 'Firecrawl-Skill/1.0',
        },
        timeout: 60_000,
      },
      (res) => {
        let data = '';
        res.setEncoding('utf8');
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          const ok = res.statusCode && res.statusCode >= 200 && res.statusCode < 300;
          if (!ok) {
            reject(new Error(`API Error ${res.statusCode}: ${data}`));
            return;
          }

          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(data);
          }
        });
      },
    );

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy(new Error('Request timed out'));
    });

    if (body !== null) {
      req.write(body);
    }
    req.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function takeFlag(args, flag) {
  const index = args.indexOf(flag);
  if (index === -1) {
    return false;
  }
  args.splice(index, 1);
  return true;
}

function takeFlagValue(args, flag) {
  const index = args.indexOf(flag);
  if (index === -1) {
    return null;
  }

  const value = args[index + 1];
  if (!value) {
    throw new Error(`Missing value for ${flag}`);
  }

  args.splice(index, 2);
  return value;
}

function extractCrawlJobId(result) {
  const candidates = [
    result?.id,
    result?.jobId,
    result?.data?.id,
    result?.data?.jobId,
    result?.crawlId,
    result?.data?.crawlId,
  ];

  return candidates.find((value) => typeof value === 'string' && value.trim().length > 0) || null;
}

function extractCrawlStatus(result) {
  const status = result?.status ?? result?.data?.status;
  if (typeof status !== 'string') {
    return null;
  }
  return status.trim().toLowerCase();
}

function isTerminalSuccessStatus(status) {
  return new Set(['completed', 'complete', 'done', 'success', 'succeeded', 'finished']).has(status);
}

function isTerminalFailureStatus(status) {
  return new Set(['failed', 'error', 'cancelled', 'canceled']).has(status);
}

async function getCrawlStatus(apiKey, crawlId) {
  const safeId = encodeURIComponent(crawlId);
  return requestJson('GET', `/v2/crawl/${safeId}`, apiKey);
}

async function waitForCrawlCompletion(apiKey, crawlId) {
  const pollIntervalMs = 3_000;

  // Poll forever by default; caller can abort with Ctrl+C.
  for (;;) {
    const statusResult = await getCrawlStatus(apiKey, crawlId);
    const status = extractCrawlStatus(statusResult);

    if (!status || isTerminalSuccessStatus(status)) {
      return statusResult;
    }

    if (isTerminalFailureStatus(status)) {
      throw new Error(`Crawl job ${crawlId} ended with status "${status}"`);
    }

    await sleep(pollIntervalMs);
  }
}

const ENDPOINT_BY_COMMAND = {
  scrape: '/v2/scrape',
  crawl: '/v2/crawl',
  map: '/v2/map',
  'batch-scrape': '/v2/batch-scrape',
};

(async () => {
  const command = process.argv[2];
  if (!command || command === '--help' || command === '-h') {
    usage();
    process.exit(command ? 0 : 1);
  }

  const args = process.argv.slice(3);
  if (args.includes('--help') || args.includes('-h')) {
    usage();
    process.exit(0);
  }

  const apiKey = loadApiKey();
  if (!apiKey) {
    console.error('Missing Firecrawl API key: set FIRECRAWL_API_KEY or create .env next to firecrawl-api.js');
    process.exit(1);
  }

  try {
    const wait = takeFlag(args, '--wait');

    if (command === 'crawl-status') {
      const explicitId = takeFlagValue(args, '--id');

      let crawlId = explicitId;
      if (!crawlId) {
        if (args[0] && !args[0].startsWith('-') && !args[0].trim().startsWith('{')) {
          crawlId = args[0];
        }

        const hasJsonPayload =
          args.includes('--file') ||
          args.includes('--data') ||
          (args[0] && args[0].trim().startsWith('{')) ||
          !process.stdin.isTTY;

        if (!crawlId && hasJsonPayload) {
          const payload = await readPayload(args);
          crawlId = extractCrawlJobId(payload);
        }
      }

      if (!crawlId) {
        throw new Error('Missing crawl id (pass <crawl-id>, --id <crawl-id>, or a JSON payload containing id/jobId)');
      }

      const result = wait
        ? await waitForCrawlCompletion(apiKey, crawlId)
        : await getCrawlStatus(apiKey, crawlId);
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    const endpoint = ENDPOINT_BY_COMMAND[command];
    if (!endpoint) {
      usage();
      process.exit(1);
    }

    if (wait && command !== 'crawl') {
      throw new Error('--wait is only supported for crawl or crawl-status');
    }

    const payload = await readPayload(args);
    const result = await requestJson('POST', endpoint, apiKey, payload);

    if (command === 'crawl' && wait) {
      const crawlId = extractCrawlJobId(result);
      if (!crawlId) {
        throw new Error('Missing crawl job id in response (expected id/jobId)');
      }

      const finalResult = await waitForCrawlCompletion(apiKey, crawlId);
      console.log(JSON.stringify(finalResult, null, 2));
      return;
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
})();
