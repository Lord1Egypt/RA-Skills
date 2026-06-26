#!/usr/bin/env node
/**
 * Sure API CLI (we-promise/sure)
 *
 * Read-only + write operations for official API endpoints.
 *
 * Secrets:
 * - Reads SURE_BASE_URL and SURE_API_KEY from /root/.openclaw/workspace/secure/api-fillin.env
 * - Never prints the API key.
 *
 * Examples:
 *   node skills/sure-api/scripts/sure_api_cli.js accounts:list
 *   node skills/sure-api/scripts/sure_api_cli.js categories:list --classification expense
 *   node skills/sure-api/scripts/sure_api_cli.js transactions:list --start_date 2026-03-01 --end_date 2026-03-31 --type expense
 *   node skills/sure-api/scripts/sure_api_cli.js transactions:create \
 *     --account_id <uuid> --date 2026-03-01 --amount 12.34 --name "午饭" --nature expense
 */

const fs = require('fs');

function loadEnvFile(path) {
  if (!fs.existsSync(path)) return {};
  const lines = fs.readFileSync(path, 'utf8').split(/\r?\n/);
  const env = {};
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!m) continue;
    env[m[1]] = m[2];
  }
  return env;
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--') {
      args._.push(...argv.slice(i + 1));
      break;
    }
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next == null || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

function qsFromArgs(obj, allowedKeys) {
  const params = new URLSearchParams();
  for (const k of allowedKeys) {
    if (obj[k] == null) continue;
    const v = obj[k];
    // allow comma-separated lists for *_ids
    if (k.endsWith('_ids') && typeof v === 'string' && v.includes(',')) {
      for (const part of v.split(',').map(x => x.trim()).filter(Boolean)) {
        params.append(k + '[]', part);
      }
    } else {
      params.set(k, String(v));
    }
  }
  const s = params.toString();
  return s ? `?${s}` : '';
}

async function request({ baseUrl, apiKey, method, path, body }) {
  const url = baseUrl.replace(/\/$/, '') + path;
  const headers = {
    'X-Api-Key': apiKey,
    'Accept': 'application/json',
  };
  const init = { method, headers };
  if (body != null) {
    headers['Content-Type'] = 'application/json';
    init.body = JSON.stringify(body);
  }

  const res = await fetch(url, init);
  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { _raw: text };
  }

  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} ${res.statusText}`);
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

function print(obj) {
  process.stdout.write(JSON.stringify(obj, null, 2) + '\n');
}

function usage() {
  console.error(`Usage:
  sure_api_cli.js <command> [options]

Commands:
  accounts:list
  categories:list
  tags:list | tags:create | tags:update | tags:delete
  merchants:list
  transactions:list | transactions:get | transactions:create | transactions:update | transactions:delete
  imports:list
  holdings:list
  trades:list
  valuations:get | valuations:update

Notes:
  - Writes require --yes (safety gate).
  - For create/update, use --dry-run to print payload without sending.
`);
  process.exit(2);
}

(async () => {
  const argv = process.argv.slice(2);
  if (argv.length === 0) usage();

  const cmd = argv[0];
  const args = parseArgs(argv.slice(1));

  const env = {
    ...process.env,
    ...loadEnvFile('/root/.openclaw/workspace/secure/api-fillin.env'),
  };

  const baseUrl = args.base_url || env.SURE_BASE_URL;
  const apiKey = args.api_key || env.SURE_API_KEY;

  if (!baseUrl) throw new Error('Missing SURE_BASE_URL (or --base_url)');
  if (!apiKey) throw new Error('Missing SURE_API_KEY (or --api_key)');

  const yes = !!args.yes;
  const dryRun = !!args['dry-run'] || !!args.dry_run;

  // ----------------------
  // READ-ONLY
  // ----------------------

  if (cmd === 'accounts:list') {
    return print(await request({ baseUrl, apiKey, method: 'GET', path: '/api/v1/accounts' }));
  }

  if (cmd === 'categories:list') {
    const q = qsFromArgs(args, ['page', 'per_page', 'classification', 'roots_only', 'parent_id']);
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/categories${q}` }));
  }

  if (cmd === 'tags:list') {
    const q = qsFromArgs(args, ['page', 'per_page']);
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/tags${q}` }));
  }

  if (cmd === 'merchants:list') {
    const q = qsFromArgs(args, ['page', 'per_page']);
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/merchants${q}` }));
  }

  if (cmd === 'transactions:list') {
    const q = qsFromArgs(args, [
      'page','per_page','account_id','category_id','merchant_id','start_date','end_date',
      'min_amount','max_amount','type','search','account_ids','category_ids','merchant_ids','tag_ids'
    ]);
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/transactions${q}` }));
  }

  if (cmd === 'transactions:get') {
    const id = args.id || args._[0];
    if (!id) throw new Error('transactions:get requires --id <uuid>');
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/transactions/${id}` }));
  }

  if (cmd === 'imports:list') {
    const q = qsFromArgs(args, ['page', 'per_page']);
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/imports${q}` }));
  }

  if (cmd === 'holdings:list') {
    return print(await request({ baseUrl, apiKey, method: 'GET', path: '/api/v1/holdings' }));
  }

  if (cmd === 'trades:list') {
    const q = qsFromArgs(args, ['page', 'per_page']);
    return print(await request({ baseUrl, apiKey, method: 'GET', path: `/api/v1/trades${q}` }));
  }

  // ----------------------
  // WRITES (guarded)
  // ----------------------

  const requireYes = () => {
    if (!yes) {
      throw new Error('Write operation blocked: pass --yes to confirm');
    }
  };

  if (cmd === 'transactions:create') {
    requireYes();
    const payload = {
      transaction: {
        account_id: args.account_id,
        date: args.date,
        amount: args.amount != null ? Number(args.amount) : undefined,
        name: args.name,
        description: args.description,
        notes: args.notes,
        currency: args.currency,
        category_id: args.category_id,
        merchant_id: args.merchant_id,
        nature: args.nature,
        tag_ids: args.tag_ids ? String(args.tag_ids).split(',').map(x => x.trim()).filter(Boolean) : undefined,
      },
    };

    // drop undefineds shallowly
    for (const k of Object.keys(payload.transaction)) {
      if (payload.transaction[k] === undefined) delete payload.transaction[k];
    }

    if (dryRun) return print({ dryRun: true, request: { method: 'POST', path: '/api/v1/transactions', body: payload } });
    return print(await request({ baseUrl, apiKey, method: 'POST', path: '/api/v1/transactions', body: payload }));
  }

  if (cmd === 'transactions:update') {
    requireYes();
    const id = args.id || args._[0];
    if (!id) throw new Error('transactions:update requires --id <uuid>');
    const payload = { transaction: {} };
    const keys = ['account_id','date','amount','name','description','notes','currency','category_id','merchant_id','nature'];
    for (const k of keys) {
      if (args[k] != null) payload.transaction[k] = (k === 'amount') ? Number(args[k]) : args[k];
    }
    if (args.tag_ids != null) {
      payload.transaction.tag_ids = String(args.tag_ids).split(',').map(x => x.trim()).filter(Boolean);
    }
    if (dryRun) return print({ dryRun: true, request: { method: 'PATCH', path: `/api/v1/transactions/${id}`, body: payload } });
    return print(await request({ baseUrl, apiKey, method: 'PATCH', path: `/api/v1/transactions/${id}`, body: payload }));
  }

  if (cmd === 'transactions:delete') {
    requireYes();
    const id = args.id || args._[0];
    if (!id) throw new Error('transactions:delete requires --id <uuid>');
    if (dryRun) return print({ dryRun: true, request: { method: 'DELETE', path: `/api/v1/transactions/${id}` } });
    return print(await request({ baseUrl, apiKey, method: 'DELETE', path: `/api/v1/transactions/${id}` }));
  }

  if (cmd === 'tags:create') {
    requireYes();
    const payload = { tag: { name: args.name } };
    if (!payload.tag.name) throw new Error('tags:create requires --name');
    if (dryRun) return print({ dryRun: true, request: { method: 'POST', path: '/api/v1/tags', body: payload } });
    return print(await request({ baseUrl, apiKey, method: 'POST', path: '/api/v1/tags', body: payload }));
  }

  if (cmd === 'tags:update') {
    requireYes();
    const id = args.id || args._[0];
    if (!id) throw new Error('tags:update requires --id <uuid>');
    const payload = { tag: {} };
    if (args.name != null) payload.tag.name = args.name;
    if (dryRun) return print({ dryRun: true, request: { method: 'PATCH', path: `/api/v1/tags/${id}`, body: payload } });
    return print(await request({ baseUrl, apiKey, method: 'PATCH', path: `/api/v1/tags/${id}`, body: payload }));
  }

  if (cmd === 'tags:delete') {
    requireYes();
    const id = args.id || args._[0];
    if (!id) throw new Error('tags:delete requires --id <uuid>');
    if (dryRun) return print({ dryRun: true, request: { method: 'DELETE', path: `/api/v1/tags/${id}` } });
    return print(await request({ baseUrl, apiKey, method: 'DELETE', path: `/api/v1/tags/${id}` }));
  }

  throw new Error(`Unknown command: ${cmd}`);
})().catch(err => {
  console.error(String(err.message || err));
  if (err.data) {
    console.error(JSON.stringify(err.data, null, 2));
  }
  process.exit(1);
});
