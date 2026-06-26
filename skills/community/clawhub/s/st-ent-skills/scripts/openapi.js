#!/usr/bin/env node
'use strict';

const BASE_URL = (process.env.SERVICE_API_BASE_URL || 'https://pre-st-api.699pic.com').replace(/\/+$/, '');
const API_KEY = process.env.SERVICE_API_KEY || '';

function usage() {
  console.error(`Usage:
  openapi.js search-photos <keywords> [limit]
  openapi.js search-videos <keywords> [limit]
  openapi.js check-downloaded <content_id> [type] [year]
  openapi.js download-asset <photo|video> <id> [file_type]
  openapi.js download-records [type] [page] [limit]`);
  console.error('\nRequired environment variables:');
  console.error('  SERVICE_API_KEY=<enterprise API key>');
  console.error('Optional environment variables:');
  console.error(`  SERVICE_API_BASE_URL=<base URL, default: ${BASE_URL}>`);
  process.exit(1);
}

async function request(path, params) {
  const body = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === '') continue;
    if (Array.isArray(value)) {
      for (const item of value) body.append(`${key}[]`, String(item));
    } else {
      body.append(key, String(value));
    }
  }
  const res = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: {
      'content-type': 'application/x-www-form-urlencoded',
      'x-api-key': API_KEY,
    },
    body,
  });
  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { throw new Error(`Non-JSON response (${res.status}): ${text}`); }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${JSON.stringify(data)}`);
  console.log(JSON.stringify(data, null, 2));
}

(async () => {
  const [cmd, ...args] = process.argv.slice(2);
  if (!cmd) usage();
  if (!API_KEY) {
    throw new Error('SERVICE_API_KEY is required');
  }
  switch (cmd) {
    case 'search-photos': {
      const [keywords, limit='10'] = args;
      if (!keywords) usage();
      await request('/openapi/Search/photo', { keywords, limit, page: 1, sort: 'complex', library: 'vip', pic_type: 0, aigc: 0 });
      break;
    }
    case 'search-videos': {
      const [keywords, limit='10'] = args;
      if (!keywords) usage();
      await request('/openapi/Search/video', { keywords, limit, page: 1, order: 'complex', sort: 'desc', source: 0, is_aigc: 0 });
      break;
    }
    case 'check-downloaded': {
      const [content_id, type='1', year] = args;
      if (!content_id) usage();
      await request('/openapi/Record/downloaded', { content_id, type, year });
      break;
    }
    case 'download-asset': {
      const [asset_type, id, file_type] = args;
      if (!asset_type || !id) usage();
      await request('/openapi/Down/asset', { asset_type, asset_id: id, file_type });
      break;
    }
    case 'download-records': {
      const [type='1', page='1', limit='10'] = args;
      await request('/openapi/Record/index', { type, page, limit });
      break;
    }
    default:
      usage();
  }
})().catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
