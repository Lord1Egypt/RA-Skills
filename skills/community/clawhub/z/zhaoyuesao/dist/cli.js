#!/usr/bin/env node
'use strict';

/**
 * 月嫂下单客资 CLI
 *
 * Commands:
 *   send_code    --mobile <phone>
 *   verify_code  --mobile <phone> --code <code>
 *   submit_lead  --city-id <id> --telephone <phone> [--due-date <date>] [--period <period>] [--budget <budget>]
 *
 * Environment:
 *   (none — backend URL is hardcoded)
 *
 * Exit codes:
 *   0 = success (code === 0)
 *   1 = business error (code !== 0)
 *   2 = transport error (ECONNREFUSED, timeout, etc.)
 */

const http = require('http');
const https = require('https');
const url = require('url');

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------
const TIMEOUT_MS = 15000;
const BACKEND_URL = 'https://jzuser-recruit.daojia.com';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function log(...args) {
  process.stderr.write('[yuesao-cli] ' + args.join(' ') + '\n');
}

function output(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

function die(code, msg, exitCode) {
  output({ code: code, codeMsg: msg });
  process.exit(exitCode);
}

/**
 * Parse CLI arguments into {command, args}.
 * Manual parsing — no external dependencies.
 */
function parseArgs(argv) {
  const positional = [];
  const named = {};

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        named[key] = next;
        i++; // skip value
      } else {
        named[key] = true;
      }
    } else {
      positional.push(arg);
    }
  }

  return { command: positional[0], args: named };
}

/**
 * Convert --kebab-case keys to camelCase for body fields.
 */
function toCamelCase(str) {
  return str.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

/**
 * Make an HTTP(S) POST request. Returns a Promise<{statusCode, body}>.
 */

/**
 * Mask a phone number: keep first 3 and last 4 digits, replace middle with ****.
 */
function maskPhone(phone) {
  if (!phone || typeof phone !== 'string' || phone.length < 7) return '***';
  return phone.substring(0, 3) + '****' + phone.substring(phone.length - 4);
}

/**
 * Mask mobile/telephone fields in a JSON string for safe logging.
 */
function maskBodyForLog(bodyStr) {
  return bodyStr.replace(/"(mobile|telephone)"\s*:\s*"(\d{7,})"/g, (match, field, phone) => {
    return '"' + field + '":"' + maskPhone(phone) + '"';
  });
}

function postRequest(endpoint, bodyObj) {
  const fullUrl = BACKEND_URL + endpoint;
  const parsed = new url.URL(fullUrl);
  const transport = parsed.protocol === 'https:' ? https : http;

  const bodyStr = JSON.stringify(bodyObj);

  const options = {
    hostname: parsed.hostname,
    port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
    path: parsed.pathname + parsed.search,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(bodyStr),
    },
    timeout: TIMEOUT_MS,
  };

  log('POST', fullUrl, 'body:', maskBodyForLog(bodyStr));

  return new Promise((resolve, reject) => {
    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on('data', (chunk) => chunks.push(chunk));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        log('Response status:', res.statusCode, 'body:', body);
        resolve({ statusCode: res.statusCode, body: body });
      });
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('ETIMEDOUT'));
    });

    req.on('error', (err) => {
      reject(err);
    });

    req.write(bodyStr);
    req.end();
  });
}

/**
 * Execute a POST and handle transport vs business errors.
 */
async function execPost(endpoint, bodyObj) {
  let res;
  try {
    res = await postRequest(endpoint, bodyObj);
  } catch (err) {
    const reason = err.code || err.message || 'unknown';
    log('Transport error:', reason);
    die(-1, '网络请求失败: ' + reason, 2);
    return; // unreachable — die() calls process.exit
  }

  // Non-2xx HTTP → transport-level error
  if (res.statusCode < 200 || res.statusCode >= 300) {
    log('HTTP error status:', res.statusCode);
    die(-1, '网络请求失败: HTTP ' + res.statusCode, 2);
    return;
  }

  // Parse JSON response
  let json;
  try {
    json = JSON.parse(res.body);
  } catch (e) {
    log('JSON parse error:', e.message, 'raw:', res.body);
    die(-1, '网络请求失败: 响应解析失败', 2);
    return;
  }

  // Business-level: code === 0 is success, otherwise business error
  if (json.code === 0) {
    output(json);
    process.exit(0);
  } else {
    output(json);
    process.exit(1);
  }
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

function cmdSendCode(args) {
  const mobile = args.mobile;
  if (!mobile) {
    die(-1, '缺少参数: --mobile', 2);
    return;
  }
  execPost('/yuesao/sendCode', { mobile: mobile });
}

function cmdVerifyCode(args) {
  const mobile = args.mobile;
  const code = args.code;
  if (!mobile) {
    die(-1, '缺少参数: --mobile', 2);
    return;
  }
  if (!code) {
    die(-1, '缺少参数: --code', 2);
    return;
  }
  execPost('/yuesao/verifyCode', { mobile: mobile, code: code });
}

function cmdSubmitLead(args) {
  const cityId = args['city-id'];
  const telephone = args.telephone;
  if (!cityId) {
    die(-1, '缺少参数: --city-id', 2);
    return;
  }
  if (!telephone) {
    die(-1, '缺少参数: --telephone', 2);
    return;
  }

  const body = { cityId: parseInt(cityId, 10), telephone: telephone };

  // Optional fields (kebab-case → camelCase)
  if (args['due-date'] !== undefined) body.dueDate = args['due-date'];
  if (args.period !== undefined) body.period = args.period;
  if (args.budget !== undefined) body.budget = args.budget;

  execPost('/yuesao/submitLead', body);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const { command, args } = parseArgs(process.argv.slice(2));

switch (command) {
  case 'send_code':
    cmdSendCode(args);
    break;
  case 'verify_code':
    cmdVerifyCode(args);
    break;
  case 'submit_lead':
    cmdSubmitLead(args);
    break;
  default:
    log('Unknown command:', command);
    die(-1, '未知命令: ' + (command || '(none)') + '。可用命令: send_code, verify_code, submit_lead', 2);
}
