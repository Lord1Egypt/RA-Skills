#!/usr/bin/env node

/**
 * Exa API Helper Script
 * Provides a CLI wrapper around Exa endpoints for skill integration.
 *
 * Usage:
 *   node exa-api.js <search|contents|findsimilar|answer|research> [<json-string>]
 *   cat payload.json | node exa-api.js search
 *   node exa-api.js search --file ./payload.json
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_BASE = 'https://api.exa.ai';

function loadApiKey() {
  if (process.env.EXA_API_KEY) {
    return process.env.EXA_API_KEY;
  }

  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) {
    return null;
  }

  const envContent = fs.readFileSync(envPath, 'utf8');
  const match = envContent.match(/EXA_API_KEY\s*=\s*(.+)/);
  if (!match) {
    return null;
  }

  return match[1].trim().replace(/^[\"']|[\"']$/g, '');
}

function usage() {
  const cmd = path.basename(process.argv[1] || 'exa-api.js');
  console.error(
    [
      'Usage:',
      `  node ${cmd} <search|contents|findsimilar|answer|research> [<json-string>]`,
      `  cat payload.json | node ${cmd} search`,
      `  node ${cmd} search --file ./payload.json`,
      '',
      'Env:',
      '  EXA_API_KEY (env var) or .env file next to this script',
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

function postJson(endpointPath, apiKey, payload) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(payload);
    const url = new URL(endpointPath, API_BASE);

    const req = https.request(
      url,
      {
        method: 'POST',
        headers: {
          'x-api-key': apiKey,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body),
          'User-Agent': 'Exa-Skill/1.0',
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

    req.write(body);
    req.end();
  });
}

const ENDPOINT_BY_COMMAND = {
  search: '/search',
  contents: '/contents',
  findsimilar: '/findSimilar',
  answer: '/answer',
  research: '/research',
};

(async () => {
  const command = process.argv[2];
  if (!command || command === '--help' || command === '-h') {
    usage();
    process.exit(command ? 0 : 1);
  }

  const endpoint = ENDPOINT_BY_COMMAND[command];
  if (!endpoint) {
    usage();
    process.exit(1);
  }

  const apiKey = loadApiKey();
  if (!apiKey) {
    console.error('Missing Exa API key: set EXA_API_KEY or create .env next to exa-api.js');
    process.exit(1);
  }

  try {
    const payload = await readPayload(process.argv.slice(3));
    const result = await postJson(endpoint, apiKey, payload);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
})();
