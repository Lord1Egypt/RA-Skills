'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const { ROOT, validatePlatformUrl, writeOutput, readJson } = require('../scripts/lib/safety');
const { renderTrip } = require('../scripts/generate-trip-page');
const { generateHTML } = require('../scripts/generate-5city-trip');
const { renderQRCodeHTML } = require('../scripts/qrcode');
const { getMockTripData } = require('../scripts/mock-data');
const { validateQuery, buildEnvironment } = require('../scripts/lib/tuniu');
const params = { departureCityName: '杭州', arrivalCityName: '南京', departureDate: '2026-10-01' };
const attack = '</title><script>alert(1)</script><img src=x onerror="alert(2)"> & "\'';

test('all trip text contexts render HTML payloads as inert text', () => {
  const data = getMockTripData();
  for (const key of ['destination', 'tripType', 'duration']) data[key] = attack;
  for (const seg of data.segments) for (const key of Object.keys(seg)) {
    if (typeof seg[key] === 'string' && key !== 'type') seg[key] = attack;
  }
  data.segments.push({ type: 'flight', flightNo: attack, departure: attack, arrival: attack, price: 1 });
  data.dailyPlan = [{ day: attack, title: attack, items: [attack] }]; data.tips = [attack];
  const html = renderTrip(data);
  assert.ok(!html.includes('<script>')); assert.ok(!html.includes('<img src=x'));
  assert.ok(html.includes('&lt;script&gt;')); assert.ok(html.includes('&amp;'));
  assert.ok(html.includes('Content-Security-Policy')); assert.ok(html.includes('rel="noopener noreferrer"'));
  assert.equal(data.destination, attack, 'renderer must not mutate caller data');
});

test('API fields in multi-city comparison are escaped, including nested airport fields', () => {
  const html = generateHTML({ mock: false,
    routes: [{ type: 'flight', from: attack, to: attack, date: attack, options: [{ flightNo: attack,
      departureTime: attack, arrivalTime: attack, duration: attack, departureAirport: attack, arrivalAirport: attack, price: 10 }] }],
    hotels: [{ city: attack, checkIn: attack, checkOut: attack, options: [{ name: attack, business: attack, starName: attack, meal: attack, refund: attack, price: 20, rating: 4 }] }]
  });
  assert.ok(!html.includes('<script>')); assert.ok(!html.includes('<img src=x'));
  assert.ok(html.includes('&lt;script&gt;'));
});

test('trip schema rejects unexpected/transactional fields and malformed data', () => {
  for (const key of ['passenger', 'paymentUrl', 'orderId', '__proto__']) {
    const data = getMockTripData(); Object.defineProperty(data, key, { value: 'blocked', enumerable: true });
    assert.throws(() => renderTrip(data));
  }
  for (const modify of [d => d.segments[0].orderId = 'blocked', d => d.costs.total = attack,
    d => d.segments[0].price = Infinity, d => d.segments[0].departure = {},
    d => d.destination = 'a'.repeat(2001), d => d.dailyPlan = Array(101).fill({}),
    d => d.language = 'en" onload="alert(1)', d => d.mock = 'false']) {
    const data = getMockTripData(); modify(data); assert.throws(() => renderTrip(data));
  }
});

test('URLs reject scripts, phishing, credentials, orders and redirects before QR encoding', async () => {
  for (const value of ['javascript:alert(1)', 'data:text/html,test', 'file:///etc/passwd', 'http://www.tuniu.com/',
    'https://www.tuniu.com.evil.test/', 'https://evil.test/', 'https://u:p@www.tuniu.com/',
    'https://www.tuniu.com:444/', 'https://m.tuniu.com/u/order', 'https://www.tuniu.com/?next=https://evil.test',
    'https://www.tuniu.com/#order', 'https://www.tuniu.com/" onload="x', 'https://www.tuniu.com\\@evil.test/', '']) {
    assert.throws(() => validatePlatformUrl(value));
    await assert.rejects(() => renderQRCodeHTML(value));
  }
  for (const value of ['https://www.tuniu.com/', 'https://m.tuniu.com/', 'https://www.12306.cn/']) assert.equal(validatePlatformUrl(value), value);
});

test('QR image and link share the normalized, validated destination', async () => {
  const result = await renderQRCodeHTML('https://WWW.TUNIU.COM');
  assert.equal(result.url, 'https://www.tuniu.com/');
  assert.equal(result.qrCodeBase64, await require('qrcode').toDataURL(result.url, { margin: 2, width: 300 }));
  assert.ok(result.html.includes('href="https://www.tuniu.com/"'));
  assert.ok(result.html.includes('rel="noopener noreferrer"'));
});

test('query allowlist rejects mutation tools, PII and invalid dates', () => {
  validateQuery('train', 'searchLowestPriceTrain', params);
  validateQuery('hotel', 'tuniu_hotel_search', { cityName: '杭州', checkIn: '2026-10-01', checkOut: '2026-10-03' });
  for (const tool of ['saveOrder', 'create_order', 'bookTrain', 'create_ticket_order', '--help']) assert.throws(() => validateQuery('train', tool, params));
  for (const key of ['passenger', 'mobile', 'apiKey', 'endpoint', 'orderId']) assert.throws(() => validateQuery('train', 'searchLowestPriceTrain', { ...params, [key]: 'blocked' }));
  for (const departureDate of ['2026-02-30', '2026-13-01', '2026-1-1', 'bad']) assert.throws(() => validateQuery('train', 'searchLowestPriceTrain', { ...params, departureDate }));
});

test('missing comparison prices display as unknown instead of free', () => {
  const html = generateHTML({ mock: false, routes: [{ type: 'train', from: 'A', to: 'B', date: '2026-10-01',
    options: [{ trainNo: 'G1', price: null }] }], hotels: [] });
  assert.ok(html.includes('<td class="price">未知</td>'));
  assert.ok(html.includes('未含缺失报价'));
});

test('child environment excludes unrelated secrets, loaders and routing overrides', () => {
  const env = buildEnvironment({ TUNIU_API_KEY: 'test-key', SystemRoot: 'C:\\Windows', AWS_SECRET_ACCESS_KEY: 'secret',
    PASSENGER_NAME: 'private', NODE_OPTIONS: '--import evil', HTTP_PROXY: 'http://evil', PATH: 'evil', HOME: 'private',
    TUNIU_CLI_PATH: 'evil', TUNIU_DISCOVERY_ENABLED: 'true' });
  assert.equal(env.TUNIU_API_KEY, 'test-key'); assert.equal(env.TUNIU_DISCOVERY_ENABLED, 'false');
  assert.deepEqual(Object.keys(env).sort(), (process.platform === 'win32' ? ['SystemRoot', 'TUNIU_API_KEY', 'TUNIU_DISCOVERY_ENABLED'] : ['TUNIU_API_KEY', 'TUNIU_DISCOVERY_ENABLED']).sort());
});

test('actual query wrapper uses locked local entry, safe argv and sanitizes failures', t => {
  const modulePath = require.resolve('../scripts/lib/tuniu');
  const oldKey = process.env.TUNIU_API_KEY;
  process.env.TUNIU_API_KEY = 'test-only-key';
  t.after(() => { if (oldKey === undefined) delete process.env.TUNIU_API_KEY; else process.env.TUNIU_API_KEY = oldKey; delete require.cache[modulePath]; });
  let calls = [];
  const spawn = t.mock.method(cp, 'spawnSync', (cmd, args, options) => {
    calls.push({ cmd, args, options });
    return { status: 0, stdout: JSON.stringify({ result: { content: [{ text: '{"data":[]}' }] } }) };
  });
  delete require.cache[modulePath]; const wrapper = require('../scripts/lib/tuniu');
  assert.deepEqual(wrapper.callTuniu('train', 'searchLowestPriceTrain', params), { data: [] });
  assert.equal(calls[0].cmd, process.execPath);
  assert.equal(calls[0].args[0], path.join(ROOT, 'node_modules/tuniu-cli/dist/index.js'));
  assert.equal(calls[0].options.shell, false); assert.equal(calls[0].options.windowsHide, true);
  assert.ok(calls[0].args.includes(path.join(ROOT, 'scripts/tuniu-config.json')));
  assert.deepEqual(JSON.parse(calls[0].args.at(-1)), params);
  assert.throws(() => wrapper.callTuniu('train', 'bookTrain', params)); assert.equal(calls.length, 1);
  spawn.mock.mockImplementation(() => ({ status: 1, stderr: 'test-only-key', stdout: 'test-only-key' }));
  assert.throws(() => wrapper.callTuniu('train', 'searchLowestPriceTrain', params), e => !e.message.includes('test-only-key'));
  const realRead = fs.readFileSync;
  t.mock.method(fs, 'readFileSync', (file, ...args) => String(file) === path.join(ROOT, 'node_modules/tuniu-cli/package.json') ? '{"name":"tuniu-cli","version":"0.0.0"}' : realRead(file, ...args));
  assert.throws(() => wrapper.callTuniu('train', 'searchLowestPriceTrain', params), /Local tuniu-cli/);
  assert.equal(calls.length, 1);
});

test('output remains under skill root regardless of cwd or malicious destination', async t => {
  const cwd = process.cwd(); process.chdir(require('node:os').tmpdir()); t.after(() => process.chdir(cwd));
  const data = getMockTripData(); data.destination = '../../outside';
  const file = writeOutput(renderTrip(data)); t.after(() => fs.unlinkSync(file));
  assert.equal(path.dirname(file), path.join(ROOT, 'output'));
  assert.ok(fs.readFileSync(file, 'utf8').includes('../../outside'));
  assert.throws(() => writeOutput('x', '../outside'));
  await assert.rejects(() => require('../scripts/generate-trip-page').main(['--mock', '--open']));
});

test('all locked registry dependencies have integrity and match manifest pins', () => {
  const lock = readJson(path.join(ROOT, 'package-lock.json'));
  const pkg = readJson(path.join(ROOT, 'package.json'));
  assert.deepEqual(lock.packages[''].dependencies, pkg.dependencies);
  for (const [name, dep] of Object.entries(lock.packages)) {
    if (!name) continue;
    assert.ok(dep.resolved.startsWith('https://registry.npmjs.org/'), name);
    assert.ok(dep.integrity.startsWith('sha512-'), name);
  }
});
