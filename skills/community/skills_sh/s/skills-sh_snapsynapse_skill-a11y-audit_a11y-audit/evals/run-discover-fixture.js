#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

function usage() {
  console.error('Usage: node a11y-audit/evals/run-discover-fixture.js --fixture <dir>');
  process.exit(1);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function installHttpMocks(responses) {
  const makeGet = () => (url, options, cb) => {
    if (typeof options === 'function') cb = options;
    const href = (url && url.href) || String(url);
    const entry = responses[href] || { statusCode: 404, body: 'missing', headers: {} };
    const req = new EventEmitter();
    req.destroy = () => {};
    req.on = req.addListener.bind(req);
    process.nextTick(() => {
      const res = new EventEmitter();
      res.statusCode = entry.statusCode || 200;
      res.headers = entry.headers || {};
      res.resume = () => {};
      cb(res);
      process.nextTick(() => {
        if (entry.body) res.emit('data', Buffer.from(entry.body));
        res.emit('end');
      });
    });
    return req;
  };

  const http = require('http');
  const https = require('https');
  http.get = makeGet();
  https.get = makeGet();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.fixture) usage();

  const fixtureDir = path.resolve(args.fixture);
  const configPath = path.join(fixtureDir, 'config.json');
  const responsesPath = path.join(fixtureDir, 'responses.json');
  const expectedPath = path.join(fixtureDir, 'expected.json');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const responses = JSON.parse(fs.readFileSync(responsesPath, 'utf8'));
  const expected = JSON.parse(fs.readFileSync(expectedPath, 'utf8'));

  installHttpMocks(responses);
  const { discover } = require(path.resolve(__dirname, '..', 'scripts', 'discover.js'));

  const runs = [];
  const runCount = config.repeat || 1;
  for (let i = 0; i < runCount; i += 1) {
    runs.push(await discover(config.runtimeUrl, config.options || {}));
  }

  const actual = runCount === 1 ? runs[0] : {
    repeatIdentical: JSON.stringify(runs[0]) === JSON.stringify(runs[1]),
    runs,
  };

  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    console.error(JSON.stringify({ expected, actual }, null, 2));
    process.exit(1);
  }

  console.log(JSON.stringify(actual, null, 2));
}

main().catch((err) => {
  console.error(err.stack || String(err));
  process.exit(1);
});
