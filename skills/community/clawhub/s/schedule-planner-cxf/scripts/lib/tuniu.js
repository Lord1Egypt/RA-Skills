'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const ROOT = path.resolve(__dirname, '../..');
const VERSION = '1.0.7';
const RULES = Object.freeze({
  'flight/searchLowestPriceFlight': ['departureCityName', 'arrivalCityName', 'departureDate'],
  'train/searchLowestPriceTrain': ['departureCityName', 'arrivalCityName', 'departureDate'],
  'hotel/tuniu_hotel_search': ['cityName', 'checkIn', 'checkOut', 'keyword', 'pageNum']
});

function validateQuery(server, tool, params) {
  const fields = RULES[`${server}/${tool}`];
  if (!fields || !params || Object.getPrototypeOf(params) !== Object.prototype) {
    throw new Error('Unsupported query. Only flight, train and hotel searches are allowed.');
  }
  for (const [key, value] of Object.entries(params)) {
    if (!fields.includes(key)) throw new Error('Unsupported query parameter.');
    if (key === 'pageNum') {
      if (!Number.isInteger(value) || value < 1 || value > 100) throw new Error('Invalid pageNum.');
    } else if (typeof value !== 'string' || !value.trim() || value.length > 200 || /[\x00-\x1f]/.test(value)) {
      throw new Error('Invalid query text.');
    }
  }
  const required = server === 'hotel' ? ['cityName', 'checkIn', 'checkOut'] : fields;
  if (required.some(key => !params[key])) throw new Error('Missing required query parameter.');
  for (const key of ['departureDate', 'checkIn', 'checkOut']) {
    const date = params[key];
    if (date !== undefined && (!/^\d{4}-\d{2}-\d{2}$/.test(date) ||
      !Number.isFinite(Date.parse(date)) || new Date(date).toISOString().slice(0, 10) !== date)) {
      throw new Error('Dates must be valid YYYY-MM-DD values.');
    }
  }
  if (server === 'hotel' && params.checkOut <= params.checkIn) throw new Error('checkOut must follow checkIn.');
}

function resolveTuniu() {
  const packageDir = path.join(ROOT, 'node_modules/tuniu-cli');
  const entry = path.join(packageDir, 'dist/index.js');
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(packageDir, 'package.json'), 'utf8'));
    if (pkg.name !== 'tuniu-cli' || pkg.version !== VERSION || !fs.statSync(entry).isFile()) throw new Error();
  } catch {
    throw new Error(`Local tuniu-cli ${VERSION} is required. Install with npm ci --ignore-scripts. No runtime download is performed.`);
  }
  // Execute the package's built entry directly; its bin wrapper resolves node via PATH.
  return entry;
}

function buildEnvironment(source) {
  const env = { TUNIU_API_KEY: source.TUNIU_API_KEY || '', TUNIU_DISCOVERY_ENABLED: 'false' };
  // Node is invoked by absolute path; no PATH, HOME, NODE_OPTIONS, proxy or other secrets are inherited.
  if (process.platform === 'win32' && source.SystemRoot) env.SystemRoot = source.SystemRoot;
  return env;
}

function callTuniu(server, tool, params) {
  validateQuery(server, tool, params);
  const entry = resolveTuniu();
  const env = buildEnvironment(process.env);
  if (!env.TUNIU_API_KEY || env.TUNIU_API_KEY.startsWith('your_')) throw new Error('Set TUNIU_API_KEY locally before querying.');
  const result = spawnSync(process.execPath, [entry, '--config', path.join(ROOT, 'scripts/tuniu-config.json'),
    'call', server, tool, '-a', JSON.stringify(params)], {
    cwd: ROOT, env, encoding: 'utf8', timeout: 30000, maxBuffer: 2 * 1024 * 1024,
    shell: false, windowsHide: true, stdio: ['ignore', 'pipe', 'pipe']
  });
  // Do not echo CLI diagnostics: they may include request headers or credentials.
  if (result.error || result.status !== 0) throw new Error('Tuniu query failed or timed out. No results were saved.');
  try {
    const parsed = JSON.parse(result.stdout);
    if (parsed.error || parsed.success === false || parsed.result?.isError) throw new Error();
    const inner = parsed.result?.structuredContent?.result ?? parsed.result?.content?.[0]?.text;
    return inner === undefined ? parsed : typeof inner === 'string' ? JSON.parse(inner) : inner;
  } catch {
    throw new Error('Invalid Tuniu response.');
  }
}
module.exports = { callTuniu, validateQuery, resolveTuniu, buildEnvironment };
