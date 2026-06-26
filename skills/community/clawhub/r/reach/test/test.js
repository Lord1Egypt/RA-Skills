import dotenv from 'dotenv';
dotenv.config();

import { Reach } from '../src/index.js';
import { SessionRecorder, loadRecording, listRecordings, formatTimeline, RECORDINGS_DIR } from '../src/utils/recorder.js';
import { saveForm, recallForm, getAutoFillData, forgetForm, listForms } from '../src/utils/form-memory.js';
import { WebhookServer } from '../src/utils/webhook-server.js';
import { parseCommand, executeCommand, SITE_ALIASES, resolveUrl } from '../src/natural.js';
import { observe } from '../src/primitives/observe.js';
import { pay, KNOWN_TOKENS, ERC20_ABI } from '../src/primitives/pay.js';
import { receiveEmail, getInbox, readEmail, markRead, markUnread, getUnreadCount, deleteEmail, onEmail, clearEmailCallbacks, _resetInbox } from '../src/primitives/email.js';
import fs from 'fs';
import path from 'path';

const reach = new Reach();
let passed = 0;
let failed = 0;

function assert(condition, name) {
  if (condition) {
    console.log(`  PASS: ${name}`);
    passed++;
  } else {
    console.log(`  FAIL: ${name}`);
    failed++;
  }
}

// ==========================================
// Original tests
// ==========================================

async function testPersist() {
  console.log('\n--- persist/recall ---');

  // Store and recall a string
  const r1 = reach.persist('test-key', 'hello world');
  assert(r1.stored === true, 'persist returns stored: true');

  const v1 = reach.recall('test-key');
  assert(v1 === 'hello world', 'recall returns stored string');

  // Store and recall an object
  reach.persist('test-obj', { name: 'ollie', version: 1 });
  const v2 = reach.recall('test-obj');
  assert(v2?.name === 'ollie', 'recall returns stored object');

  // TTL expiry
  reach.persist('test-ttl', 'expires', { ttl: 1 });
  const v3 = reach.recall('test-ttl');
  assert(v3 === 'expires', 'TTL value accessible before expiry');

  // Forget
  const f1 = reach.forget('test-key');
  assert(f1 === true, 'forget returns true for existing key');
  const v4 = reach.recall('test-key');
  assert(v4 === null, 'recall returns null after forget');

  // Not found
  const v5 = reach.recall('nonexistent-key-xyz');
  assert(v5 === null, 'recall returns null for missing key');

  // List keys
  const keys = reach.listKeys();
  assert(keys.length >= 1, 'listKeys returns stored keys');

  // Cleanup
  reach.forget('test-obj');
  reach.forget('test-ttl');
}

async function testFetch() {
  console.log('\n--- fetch (HTTP) ---');

  // Fetch a simple page
  const result = await reach.fetch('https://example.com');
  assert(result.source === 'http' || result.source === 'browser', 'example.com fetched via HTTP or browser fallback');
  assert(result.format === 'markdown', 'returned as markdown');
  assert(result.content.includes('Example Domain'), 'content contains expected text');

  // Fetch JSON
  const json = await reach.fetch('https://httpbin.org/json', { format: 'json' });
  assert(json.format === 'json', 'JSON format returned');
  assert(json.content?.slideshow, 'JSON content has expected structure');
}

async function testSign() {
  console.log('\n--- sign ---');

  const key = process.env.PRIVATE_KEY || process.env.DEPLOYMENT_KEY;
  if (!key) {
    console.log('  SKIP: No PRIVATE_KEY or DEPLOYMENT_KEY in .env');
    return;
  }

  const result = await reach.sign('hello from reach');
  assert(result.signature?.startsWith('0x'), 'signature starts with 0x');
  assert(result.address?.startsWith('0x'), 'address starts with 0x');
  assert(result.type === 'message', 'type is message');

  const addr = reach.getAddress();
  assert(addr === result.address, 'getAddress matches signer');
}

async function testRouter() {
  console.log('\n--- router ---');

  // Read task — default
  const r1 = reach.route({ type: 'read', url: 'https://example.com' });
  assert(r1.primitive === 'fetch', 'read routes to fetch');
  assert(r1.layer === 'http', 'unknown site defaults to http');

  // Read task — known API
  const r2 = reach.route({ type: 'read', url: 'https://api.github.com/repos/Potdealer/exoskeletons' });
  assert(r2.layer === 'api', 'github routes to api layer');

  // Interact task
  const r3 = reach.route({ type: 'interact', url: 'https://example.com' });
  assert(r3.primitive === 'act', 'interact routes to act');
  assert(r3.layer === 'browser', 'interact uses browser');

  // Auth task
  const r4 = reach.route({ type: 'auth', url: 'https://cantina.xyz', params: { service: 'cantina', method: 'login' } });
  assert(r4.primitive === 'authenticate', 'auth routes to authenticate');

  // Sign task
  const r5 = reach.route({ type: 'sign' });
  assert(r5.primitive === 'sign', 'sign routes to sign');

  // Store task
  const r6 = reach.route({ type: 'store', params: { key: 'test' } });
  assert(r6.primitive === 'persist', 'store routes to persist');

  // Learn and re-route
  reach.learnSite('https://spa-app.example.com', { needsJS: true });
  const r7 = reach.route({ type: 'read', url: 'https://spa-app.example.com/page' });
  assert(r7.params?.javascript === true, 'learned JS-needed site routes with javascript:true');

  // Monitor routes to observe
  const r8 = reach.route({ type: 'monitor', url: 'https://example.com' });
  assert(r8.primitive === 'observe', 'monitor routes to observe');

  // Pay routes to pay
  const r9 = reach.route({ type: 'pay', params: { recipient: '0x1234', amount: '0.01' } });
  assert(r9.primitive === 'pay', 'pay routes to pay');
}

async function testAuthenticate() {
  console.log('\n--- authenticate ---');

  // Cookie auth with no saved cookies
  const r1 = await reach.authenticate('nonexistent-service', 'cookie');
  assert(r1.success === false, 'cookie auth fails for unknown service');

  // API key auth
  const r2 = await reach.authenticate('test-service', 'apikey', { apiKey: 'test-key-123', headerName: 'X-API-Key' });
  assert(r2.success === true, 'apikey auth succeeds');
  assert(r2.session.type === 'apikey', 'session type is apikey');

  // Verify session was saved
  const session = reach.getSession('test-service');
  assert(session?.type === 'apikey', 'saved session is retrievable');
}

// ==========================================
// New tests: observe
// ==========================================

async function testObserve() {
  console.log('\n--- observe ---');

  // Test poll observer creation
  let callbackFired = false;
  const observer = await observe('https://httpbin.org/uuid', {
    method: 'poll',
    interval: 100,
  }, (event) => {
    callbackFired = true;
  });

  assert(observer.id.startsWith('obs-poll-'), 'poll observer has correct id prefix');
  assert(observer.method === 'poll', 'observer method is poll');
  assert(typeof observer.stop === 'function', 'observer has stop method');
  assert(typeof observer.getState === 'function', 'observer has getState method');

  // Wait for a couple of polls
  await new Promise(r => setTimeout(r, 500));
  assert(observer.getPollCount() >= 1, 'poll count incremented');

  // Stop observer
  const stopResult = observer.stop();
  assert(stopResult.stopped === true, 'stop returns stopped: true');

  // Wait and verify no more polls
  const countAtStop = observer.getPollCount();
  await new Promise(r => setTimeout(r, 300));
  assert(observer.getPollCount() === countAtStop, 'no more polls after stop');

  // Test contract observer creation (no actual events expected)
  const contractObs = await observe('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', {
    method: 'contract',
  }, () => {});
  assert(contractObs.method === 'contract', 'contract observer has correct method');
  assert(typeof contractObs.stop === 'function', 'contract observer has stop method');
  contractObs.stop();

  // Test auto-detection: URL -> poll
  const autoObs = await observe('https://example.com', { interval: 60000 }, () => {});
  assert(autoObs.method === 'poll', 'URL auto-detects to poll');
  autoObs.stop();

  // Test auto-detection: 0x address -> contract
  const autoContract = await observe('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', {}, () => {});
  assert(autoContract.method === 'contract', 'address auto-detects to contract');
  autoContract.stop();

  // Test webhook observer
  const webhookObs = await observe('https://example.com', {
    method: 'webhook',
    path: '/test-hook',
  }, () => {});
  assert(webhookObs.method === 'webhook', 'webhook observer has correct method');
  assert(webhookObs.path === '/test-hook', 'webhook path is set');
  webhookObs.stop();
}

// ==========================================
// New tests: pay
// ==========================================

async function testPay() {
  console.log('\n--- pay ---');

  // Test known tokens exist
  assert(KNOWN_TOKENS.USDC !== undefined, 'USDC token address defined');
  assert(KNOWN_TOKENS.WETH !== undefined, 'WETH token address defined');
  assert(KNOWN_TOKENS.DAI !== undefined, 'DAI token address defined');

  // Test ERC20 ABI exists
  assert(Array.isArray(ERC20_ABI), 'ERC20_ABI is an array');
  assert(ERC20_ABI.length >= 4, 'ERC20_ABI has expected functions');

  // Test invalid address rejection
  try {
    await pay('not-an-address', '0.01', { privateKey: '0x' + '1'.repeat(64) });
    assert(false, 'should reject invalid address');
  } catch (e) {
    assert(e.message.includes('Invalid recipient'), 'rejects invalid address with correct error');
  }

  // Test missing private key
  const origKey = process.env.PRIVATE_KEY;
  const origDeployKey = process.env.DEPLOYMENT_KEY;
  delete process.env.PRIVATE_KEY;
  delete process.env.DEPLOYMENT_KEY;
  try {
    await pay('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', '0.01');
    assert(false, 'should reject without private key');
  } catch (e) {
    assert(e.message.includes('No private key'), 'rejects with no key error');
  }
  process.env.PRIVATE_KEY = origKey;
  if (origDeployKey) process.env.DEPLOYMENT_KEY = origDeployKey;

  // Test x402 — non-402 URL just returns content
  const result = await pay('https://httpbin.org/get', '0.01');
  assert(result.type === 'x402', 'URL triggers x402 flow');
  assert(result.paid === false, 'non-402 URL means no payment');
  assert(result.status === 200, 'returns 200 status');
}

// ==========================================
// New tests: session recorder
// ==========================================

async function testRecorder() {
  console.log('\n--- session recorder ---');

  // Create and start recorder
  const recorder = new SessionRecorder({ name: 'test-recording' });
  recorder.start();
  assert(recorder.isRecording(), 'recorder is recording after start');

  // Record some actions
  recorder.record('fetch', { url: 'https://example.com' }, { content: 'hello', source: 'http' });
  recorder.record('act', { url: 'https://example.com', action: 'click', text: 'Button' }, { success: true });
  recorder.recordError('fetch', { url: 'https://bad.url' }, new Error('Connection refused'));

  assert(recorder.getEntries().length === 3, 'recorder has 3 entries');

  // Stop and save
  const session = recorder.stop();
  assert(!recorder.isRecording(), 'recorder stopped');
  assert(session.entryCount === 3, 'session has 3 entries');
  assert(session.name === 'test-recording', 'session name is correct');
  assert(session.file, 'session was saved to file');
  assert(fs.existsSync(session.file), 'recording file exists');

  // Load recording
  const loaded = loadRecording('test-recording');
  assert(loaded.entryCount === 3, 'loaded recording has 3 entries');
  assert(loaded.entries[2].error, 'error entry has error field');

  // Format timeline
  const timeline = formatTimeline(loaded);
  assert(timeline.includes('Session: test-recording'), 'timeline includes session name');
  assert(timeline.includes('FETCH'), 'timeline includes FETCH action');
  assert(timeline.includes('ERROR'), 'timeline includes ERROR');

  // List recordings
  const recordings = listRecordings();
  assert(recordings.some(r => r.name === 'test-recording'), 'recording appears in list');

  // Test sensitive data redaction
  const recorder2 = new SessionRecorder({ name: 'test-redaction' });
  recorder2.start();
  recorder2.record('authenticate', { service: 'test', password: 'secret123', apiKey: 'key-456' }, { success: true });
  const session2 = recorder2.stop();
  const entry = session2.entries[0];
  assert(entry.input.password === '[REDACTED]', 'password is redacted in recording');
  assert(entry.input.apiKey === '[REDACTED]', 'apiKey is redacted in recording');

  // Cleanup
  try { fs.unlinkSync(session.file); } catch {}
  try { fs.unlinkSync(session2.file); } catch {}
}

// ==========================================
// New tests: form memory
// ==========================================

async function testFormMemory() {
  console.log('\n--- form memory ---');

  const testUrl = 'https://test-form.example.com/signup';

  // Save form data
  const saved = saveForm(testUrl, [
    { name: 'email', value: 'ollie@exoagent.xyz', selector: '#email', type: 'email' },
    { name: 'username', value: 'olliebot', selector: '#username', type: 'text' },
    { name: 'password', value: 'secret', selector: '#password', type: 'password' },
  ]);
  assert(saved.saved === true, 'form data saved');
  assert(saved.fieldCount >= 2, 'field count is correct');

  // Recall form data
  const recalled = recallForm(testUrl);
  assert(recalled !== null, 'form data recalled');
  assert(recalled.fields.email?.value === 'ollie@exoagent.xyz', 'email field value correct');
  assert(recalled.fields.username?.value === 'olliebot', 'username field value correct');
  assert(recalled.fields.password?.sensitive === true, 'password marked as sensitive');
  assert(recalled.fields.password?.value === undefined, 'password value not stored');

  // Auto-fill suggestions
  const suggestions = getAutoFillData(testUrl, [
    { name: 'email', selector: '#email', type: 'email' },
    { name: 'username', selector: '#username', type: 'text' },
    { name: 'password', selector: '#password', type: 'password' },
  ]);
  assert(suggestions.length >= 2, 'auto-fill returns suggestions');
  assert(suggestions.some(s => s.name === 'email'), 'email in suggestions');
  assert(!suggestions.some(s => s.name === 'password'), 'password NOT in suggestions (sensitive)');

  // List forms
  const forms = listForms();
  assert(forms.some(f => f.url === testUrl), 'form appears in list');

  // Recall for unknown URL
  const unknown = recallForm('https://unknown.example.com/page');
  assert(unknown === null, 'unknown URL returns null');

  // Forget form
  const forgot = forgetForm(testUrl);
  assert(forgot === true, 'form data forgotten');
  assert(recallForm(testUrl) === null, 'recalled after forget is null');
}

// ==========================================
// New tests: webhook server
// ==========================================

async function testWebhookServer() {
  console.log('\n--- webhook server ---');

  const server = new WebhookServer({ port: 8431 }); // Use non-default port for test

  // Register handlers
  let receivedPayload = null;
  server.on('/test-hook', (payload) => {
    receivedPayload = payload;
  });

  assert(server.listPaths().includes('/test-hook'), 'handler registered');

  // Start server
  await server.start();

  // Send a webhook
  const response = await fetch('http://localhost:8431/test-hook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event: 'test', data: 'hello' }),
  });
  const result = await response.json();
  assert(result.received === true, 'webhook received confirmation');
  assert(receivedPayload?.event === 'test', 'handler received correct payload');

  // Health check
  const healthResponse = await fetch('http://localhost:8431/health');
  const health = await healthResponse.json();
  assert(health.status === 'ok', 'health check returns ok');
  assert(health.handlers.includes('/test-hook'), 'health lists registered handlers');

  // 404 for unknown path
  const notFoundResponse = await fetch('http://localhost:8431/unknown');
  assert(notFoundResponse.status === 404, '404 for unknown path');

  // Request log
  const log = server.getLog();
  assert(log.length >= 2, 'request log has entries');

  // Unregister handler
  server.off('/test-hook');
  assert(!server.listPaths().includes('/test-hook'), 'handler unregistered');

  await server.stop();
}

// ==========================================
// New tests: natural language
// ==========================================

async function testNatural() {
  console.log('\n--- natural language ---');

  // Navigation
  const p1 = parseCommand('go to github');
  assert(p1?.primitive === 'fetch', '"go to github" → fetch');
  assert(p1?.params?.url === 'https://github.com', '"go to github" resolves to github.com');

  const p2 = parseCommand('open https://example.com');
  assert(p2?.primitive === 'fetch', '"open url" → fetch');
  assert(p2?.params?.url === 'https://example.com', 'URL preserved');

  // Search
  const p3 = parseCommand('search upwork for solidity jobs');
  assert(p3?.primitive === 'site', '"search upwork" → site primitive');
  assert(p3?.site === 'upwork', 'site is upwork');
  assert(p3?.params?.query === 'solidity jobs', 'query is correct');

  // Click
  const p4 = parseCommand('click "Sign Up"');
  assert(p4?.primitive === 'act', '"click" → act');
  assert(p4?.method === 'click', 'method is click');
  assert(p4?.params?.text === 'Sign Up', 'text is correct');

  // Email
  const p5 = parseCommand('email client@company.com about Audit Proposal');
  assert(p5?.primitive === 'email', '"email" → email');
  assert(p5?.params?.to === 'client@company.com', 'recipient correct');
  assert(p5?.params?.subject === 'Audit Proposal', 'subject correct');

  // Send ETH
  const p6 = parseCommand('send 0.01 ETH to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913');
  assert(p6?.primitive === 'pay', '"send ETH" → pay');
  assert(p6?.params?.amount === '0.01', 'amount correct');
  assert(p6?.params?.recipient?.startsWith('0x'), 'recipient is address');

  // Send USDC
  const p7 = parseCommand('send 100 USDC to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913');
  assert(p7?.primitive === 'pay', '"send USDC" → pay');
  assert(p7?.params?.token === 'USDC', 'token is USDC');

  // Watch
  const p8 = parseCommand('watch api.coingecko.com every 60s');
  assert(p8?.primitive === 'observe', '"watch" → observe');

  // Remember / recall
  const p9 = parseCommand('remember favorite color as blue');
  assert(p9?.primitive === 'persist', '"remember" → persist');
  assert(p9?.params?.key === 'favorite color', 'key correct');
  assert(p9?.params?.value === 'blue', 'value correct');

  const p10 = parseCommand('what is favorite color');
  assert(p10?.primitive === 'persist', '"what is" → recall');
  assert(p10?.method === 'recall', 'method is recall');

  // Screenshot
  const p11 = parseCommand('screenshot basescan.org');
  assert(p11?.primitive === 'see', '"screenshot" → see');

  // Login
  const p12 = parseCommand('login to cantina');
  assert(p12?.primitive === 'authenticate', '"login" → authenticate');
  assert(p12?.params?.service === 'cantina', 'service is cantina');

  // Sign
  const p13 = parseCommand('sign hello world');
  assert(p13?.primitive === 'sign', '"sign" → sign');
  assert(p13?.params?.payload === 'hello world', 'payload correct');

  // URL resolution
  assert(resolveUrl('github') === 'https://github.com', 'resolveUrl: alias');
  assert(resolveUrl('https://example.com') === 'https://example.com', 'resolveUrl: full URL');
  assert(resolveUrl('example.com') === 'https://example.com', 'resolveUrl: bare domain');

  // Unknown command
  const p14 = parseCommand('');
  assert(p14 === null, 'empty string returns null');

  const p15 = parseCommand('asdjkfhaskdjfh gibberish');
  // Should return something (Google search fallback) or null
  assert(p15 === null || p15?.primitive === 'fetch', 'gibberish returns null or Google search');

  // Site aliases exist
  assert(Object.keys(SITE_ALIASES).length >= 5, 'multiple site aliases defined');
}

// ==========================================
// New tests: Reach integration (recording)
// ==========================================

async function testReachRecording() {
  console.log('\n--- reach recording integration ---');

  // Start recording on Reach instance
  const recorder = reach.startRecording('test-reach-recording');
  assert(recorder !== null, 'startRecording returns recorder');

  // Do some actions that get recorded
  reach.persist('record-test', 'value1');
  reach.recall('record-test');
  reach.forget('record-test');

  // Stop recording
  const session = reach.stopRecording();
  assert(session !== null, 'stopRecording returns session');
  assert(session.entryCount >= 3, 'session recorded persist, recall, forget');

  // Verify entries
  const actions = session.entries.map(e => e.action);
  assert(actions.includes('persist'), 'recording includes persist');
  assert(actions.includes('recall'), 'recording includes recall');
  assert(actions.includes('forget'), 'recording includes forget');

  // Cleanup
  try { fs.unlinkSync(session.file); } catch {}
}

// ==========================================
// Email inbox tests
// ==========================================

async function testEmailInbox() {
  console.log('\n--- email inbox ---');

  // Clean slate
  _resetInbox();
  const inboxDir = path.join(process.cwd(), 'data', 'inbox');
  // Remove test files if they exist
  if (fs.existsSync(inboxDir)) {
    const files = fs.readdirSync(inboxDir);
    for (const f of files) {
      try { fs.unlinkSync(path.join(inboxDir, f)); } catch {}
    }
  }
  _resetInbox();

  // Test receiveEmail stores correctly
  const email1 = receiveEmail({
    from: 'alice@example.com',
    to: 'ollie@mfer.one',
    subject: 'Hello Ollie',
    body: 'Testing the inbox system.',
    messageId: 'test-msg-001',
    timestamp: '2026-03-22T10:00:00Z',
  });
  assert(email1.messageId === 'test-msg-001', 'receiveEmail returns correct messageId');
  assert(email1.read === false, 'receiveEmail marks as unread');

  // Store a second email
  receiveEmail({
    from: 'bob@example.com',
    to: 'athena@mfer.one',
    subject: 'Security Review Request',
    body: 'Can you review my contract?',
    messageId: 'test-msg-002',
    timestamp: '2026-03-22T11:00:00Z',
    localPart: 'athena',
  });

  // Store a third email
  receiveEmail({
    from: 'alice@example.com',
    to: 'ollie@mfer.one',
    subject: 'Follow up',
    body: 'Just checking in.',
    messageId: 'test-msg-003',
    timestamp: '2026-03-22T12:00:00Z',
  });

  // Test getInbox returns all
  const all = getInbox();
  assert(all.length === 3, 'getInbox returns all 3 emails');

  // Test getInbox sorted newest first
  assert(all[0].messageId === 'test-msg-003', 'getInbox sorts newest first');

  // Test unread filter
  const unread = getInbox({ unread: true });
  assert(unread.length === 3, 'all 3 emails are unread initially');

  // Test from filter
  const fromAlice = getInbox({ from: 'alice' });
  assert(fromAlice.length === 2, 'from filter matches 2 alice emails');

  // Test subject filter
  const security = getInbox({ subject: 'security' });
  assert(security.length === 1, 'subject filter matches 1 email');

  // Test localPart filter
  const athenaEmails = getInbox({ localPart: 'athena' });
  assert(athenaEmails.length === 1, 'localPart filter matches athena email');

  // Test limit
  const limited = getInbox({ limit: 2 });
  assert(limited.length === 2, 'limit works');

  // Test readEmail (full body)
  const fullEmail = readEmail('test-msg-001');
  assert(fullEmail !== null, 'readEmail returns email');
  assert(fullEmail.body === 'Testing the inbox system.', 'readEmail includes body');

  // Test markRead
  const marked = markRead('test-msg-001');
  assert(marked === true, 'markRead returns true');
  const afterMark = getInbox({ unread: true });
  assert(afterMark.length === 2, 'after markRead, 2 unread remain');

  // Test markUnread
  markUnread('test-msg-001');
  const afterUnmark = getInbox({ unread: true });
  assert(afterUnmark.length === 3, 'after markUnread, 3 unread again');

  // Test getUnreadCount
  markRead('test-msg-001');
  const count = getUnreadCount();
  assert(count === 2, 'getUnreadCount returns 2');

  // Test deleteEmail
  const deleted = deleteEmail('test-msg-003');
  assert(deleted === true, 'deleteEmail returns true');
  const afterDelete = getInbox();
  assert(afterDelete.length === 2, 'after delete, 2 emails remain');
  assert(readEmail('test-msg-003') === null, 'deleted email file is gone');

  // Test onEmail callback
  let callbackReceived = null;
  const unsub = onEmail((data) => {
    callbackReceived = data;
  });

  receiveEmail({
    from: 'callback@test.com',
    to: 'ollie@mfer.one',
    subject: 'Callback Test',
    body: 'Did the callback fire?',
    messageId: 'test-msg-004',
  });
  assert(callbackReceived !== null, 'onEmail callback fires');
  assert(callbackReceived.from === 'callback@test.com', 'callback receives correct data');

  // Test unsubscribe
  unsub();
  callbackReceived = null;
  receiveEmail({
    from: 'after-unsub@test.com',
    to: 'ollie@mfer.one',
    subject: 'After Unsub',
    body: 'Should not trigger callback.',
    messageId: 'test-msg-005',
  });
  assert(callbackReceived === null, 'after unsub, callback does not fire');

  // Test disk persistence — reset memory and reload
  _resetInbox();
  const reloaded = getInbox();
  assert(reloaded.length === 4, 'inbox persists to disk and reloads (4 emails)');

  // Test readEmail not found
  const notFound = readEmail('nonexistent-id');
  assert(notFound === null, 'readEmail returns null for unknown ID');

  // Test markRead not found
  const markNotFound = markRead('nonexistent-id');
  assert(markNotFound === false, 'markRead returns false for unknown ID');

  // Test body truncation
  const hugeBody = 'x'.repeat(200 * 1024);
  receiveEmail({
    from: 'big@test.com',
    to: 'ollie@mfer.one',
    subject: 'Huge Email',
    body: hugeBody,
    messageId: 'test-msg-huge',
  });
  const hugeEmail = readEmail('test-msg-huge');
  assert(hugeEmail.body.length < hugeBody.length, 'large body is truncated');
  assert(hugeEmail.body.includes('[... truncated]'), 'truncated body has marker');

  // Cleanup test emails
  clearEmailCallbacks();
  _resetInbox();
  if (fs.existsSync(inboxDir)) {
    const files = fs.readdirSync(inboxDir);
    for (const f of files) {
      try { fs.unlinkSync(path.join(inboxDir, f)); } catch {}
    }
  }
}

// ==========================================
// Run all tests
// ==========================================

async function main() {
  console.log('Reach Test Suite\n================');

  // Unit tests (no network)
  await testPersist();
  await testRouter();
  await testAuthenticate();
  await testRecorder();
  await testFormMemory();
  await testNatural();
  await testReachRecording();
  await testEmailInbox();

  // Integration tests (need network)
  await testFetch();
  await testSign();

  // Component tests (need server/network)
  await testObserve();
  await testPay();
  await testWebhookServer();

  console.log(`\n================`);
  console.log(`${passed} passed, ${failed} failed`);

  await reach.close();
  process.exit(failed > 0 ? 1 : 0);
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
