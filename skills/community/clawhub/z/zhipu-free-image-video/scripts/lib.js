#!/usr/bin/env node
const https = require('https');

function readJsonArg(index, name) {
  const raw = process.argv[index];
  if (!raw) throw new Error(`Missing JSON argument: ${name}`);
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error(`Invalid JSON for ${name}: ${error.message}`);
  }
}

function requireApiKey() {
  const key = process.env.IMAGE_VIDEO_GENERATION_API_KEY || process.env.ZHIPU_API_KEY;
  if (!key) {
    throw new Error('Missing IMAGE_VIDEO_GENERATION_API_KEY or ZHIPU_API_KEY');
  }
  return key;
}

function postJson(path, body) {
  const apiKey = requireApiKey();
  return request('POST', path, body, apiKey);
}

function getJson(path) {
  const apiKey = requireApiKey();
  return request('GET', path, null, apiKey);
}

function request(method, path, body, apiKey) {
  const payload = body ? JSON.stringify(body) : null;
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'open.bigmodel.cn',
      path: `/api${path}`,
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        ...(payload ? { 'Content-Length': Buffer.byteLength(payload) } : {}),
      },
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = data ? JSON.parse(data) : {};
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(json);
          } else {
            reject(new Error(json?.error?.message || json?.message || `HTTP ${res.statusCode}`));
          }
        } catch (error) {
          reject(new Error(`Invalid JSON response: ${error.message}`));
        }
      });
    });
    req.on('error', reject);
    if (payload) req.write(payload);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function print(data) {
  console.log(JSON.stringify(data, null, 2));
}

function getImageModels() {
  return ['cogview-3-flash', 'cogview-4', 'cogview-4-250304'];
}

function getVideoModels() {
  return ['cogvideox-flash', 'cogvideox-2', 'cogvideox-3'];
}

module.exports = { readJsonArg, postJson, getJson, sleep, print, getImageModels, getVideoModels };
