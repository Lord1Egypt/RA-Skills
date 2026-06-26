import dotenv from 'dotenv';
dotenv.config({ path: new URL('../.env', import.meta.url).pathname });

import { Reach } from '../src/index.js';

const reach = new Reach();
const results = [];

function report(name, pass, detail) {
  const status = pass ? 'PASS' : 'FAIL';
  console.log(`\n${'='.repeat(60)}`);
  console.log(`[${status}] Test: ${name}`);
  console.log(detail);
  console.log('='.repeat(60));
  results.push({ name, pass, detail });
}

async function test1() {
  console.log('\n--- Test 1: fetch — Read a webpage (HTTP) ---');
  try {
    const result = await reach.fetch('https://docs.base.org', { format: 'markdown' });
    const content = typeof result === 'object' ? (result.content || JSON.stringify(result)) : result;
    const preview = String(content).substring(0, 500);
    const pass = preview.length > 50;
    report('Test 1: fetch HTTP', pass, `Source: ${result.source || 'unknown'}\nLength: ${String(content).length}\nPreview:\n${preview}`);
  } catch (e) {
    report('Test 1: fetch HTTP', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test2() {
  console.log('\n--- Test 2: fetch — JavaScript-required page ---');
  try {
    const result = await reach.fetch('https://cantina.xyz/competitions', { format: 'markdown', javascript: true });
    const content = typeof result === 'object' ? (result.content || JSON.stringify(result)) : result;
    const preview = String(content).substring(0, 500);
    const pass = preview.length > 50;
    report('Test 2: fetch JS page', pass, `Source: ${result.source || 'unknown'}\nLength: ${String(content).length}\nPreview:\n${preview}`);
  } catch (e) {
    report('Test 2: fetch JS page', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test3() {
  console.log('\n--- Test 3: authenticate — Login to Cantina ---');
  try {
    const session = await reach.authenticate('https://cantina.xyz', 'login', {
      url: 'https://cantina.xyz',
      email: process.env.CANTINA_EMAIL,
      password: process.env.CANTINA_PASSWORD
    });
    const pass = session && session.success === true;
    report('Test 3: authenticate login', pass, `Result: ${JSON.stringify(session, null, 2)}`);
  } catch (e) {
    report('Test 3: authenticate login', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test4() {
  console.log('\n--- Test 4: act — Click and navigate ---');
  try {
    const result = await reach.act('https://cantina.xyz/competitions', 'click', { text: 'Competitions' });
    const pass = result && result.success === true;
    report('Test 4: act click', pass, `Result: ${JSON.stringify(result, null, 2)}`);
  } catch (e) {
    report('Test 4: act click', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test5() {
  console.log('\n--- Test 5: sign — Sign a message ---');
  try {
    const sig = await reach.sign({ message: 'Hello from Reach' });
    const pass = sig && sig.signature && sig.address;
    report('Test 5: sign message', !!pass, `Result: ${JSON.stringify(sig, null, 2)}`);
  } catch (e) {
    report('Test 5: sign message', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test6() {
  console.log('\n--- Test 6: persist/recall — State storage ---');
  try {
    const stored = reach.persist('test_key', { hello: 'world', timestamp: Date.now() });
    const recalled = reach.recall('test_key');
    const pass = recalled && recalled.hello === 'world';
    report('Test 6: persist/recall', !!pass, `Stored: ${JSON.stringify(stored)}\nRecalled: ${JSON.stringify(recalled)}`);
  } catch (e) {
    report('Test 6: persist/recall', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test7() {
  console.log('\n--- Test 7: Router — Check routing decisions ---');
  try {
    const route1 = reach.route({ type: 'read', url: 'https://api.twitter.com/2/tweets' });
    const route2 = reach.route({ type: 'read', url: 'https://cantina.xyz/competitions' });
    const route3 = reach.route({ type: 'read', url: 'https://docs.base.org/get-started' });
    const pass = route1 && route1.primitive === 'fetch' && route2 && route3;
    report('Test 7: router', !!pass, `Twitter API: ${JSON.stringify(route1)}\nCantina: ${JSON.stringify(route2)}\nBase docs: ${JSON.stringify(route3)}`);
  } catch (e) {
    report('Test 7: router', false, `Error: ${e.message}\n${e.stack}`);
  }
}

async function test10() {
  console.log('\n--- Test 10: Screenshot ---');
  try {
    const result = await reach.fetch('https://example.com', { format: 'screenshot' });
    const content = result.content || result;
    const pass = typeof content === 'string' && content.includes('screenshot') && content.endsWith('.png');
    report('Test 10: screenshot', !!pass, `Result: ${JSON.stringify(result, null, 2)}`);
  } catch (e) {
    report('Test 10: screenshot', false, `Error: ${e.message}\n${e.stack}`);
  }
}

// Run all tests
async function main() {
  console.log('Starting Reach real-world tests...\n');

  await test1();
  await test2();
  await test3();
  await test4();
  await test5();
  await test6();
  await test7();
  await test10();

  console.log('\n\n=== SUMMARY ===');
  for (const r of results) {
    console.log(`  [${r.pass ? 'PASS' : 'FAIL'}] ${r.name}`);
  }
  console.log(`\nTotal: ${results.filter(r => r.pass).length}/${results.length} passed`);

  await reach.close();

  // Output JSON for parsing
  console.log('\n---JSON---');
  console.log(JSON.stringify(results));
}

main().catch(e => {
  console.error('Fatal:', e);
  process.exit(1);
});
