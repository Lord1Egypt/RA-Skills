#!/usr/bin/env node
// CDP-based closed shadow DOM cascade trace
// Usage: node cdp-trace.js --url <URL> --parts "name1,name2,..." [--login user:pass]
//
// Requires: playwright (npm install playwright)
//   cd <repo>/.tmp && npm init -y && npm install playwright
//   npx playwright install chromium
//
// User visibility required: headless: false, slowMo: 800 (web-ui-test "user visibility first" rule)

const { chromium } = require('playwright');

function parseArgs() {
  const args = { parts: [], url: null, login: null };
  const argv = process.argv.slice(2);
  function takeValue(flag, i) {
    if (i + 1 >= argv.length) {
      console.error(`ERROR: ${flag} requires a value (e.g. ${flag} <value>)`);
      process.exit(2);
    }
    return argv[i + 1];
  }
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--url') { args.url = takeValue('--url', i); i++; }
    // Accept both --parts (canonical, plural) and --part (legacy/singular) so the
    // Quick Reference example in cdp-trace.md does not silently fall through.
    else if (argv[i] === '--parts' || argv[i] === '--part') {
      args.parts = takeValue(argv[i], i).split(',').map(s => s.trim()).filter(Boolean);
      i++;
    }
    else if (argv[i] === '--login') { args.login = takeValue('--login', i); i++; }
    else if (argv[i] === '--help' || argv[i] === '-h') {
      console.log('Usage: node cdp-trace.js --url <URL> --parts "name1,name2,..." [--login user:pass]');
      process.exit(0);
    }
    else {
      console.error(`ERROR: unknown argument: ${argv[i]}`);
      process.exit(2);
    }
  }
  if (!args.url) { console.error('ERROR: --url required'); process.exit(1); }
  return args;
}

async function loginIfNeeded(page, login) {
  if (!login) return;
  // Use the first ':' as the separator only — split(':') loses everything
  // after the second ':' if the password itself contains ':'.
  const sep = login.indexOf(':');
  if (sep < 0) {
    console.error('ERROR: --login must be in user:pass form');
    process.exit(2);
  }
  const user = login.slice(0, sep);
  const pass = login.slice(sep + 1);
  await page.waitForTimeout(3000);

  async function fillAndSubmit(value, fieldType) {
    return await page.evaluate(({ value, fieldType }) => {
      function deepQS(root, predicate) {
        if (predicate(root)) return root;
        const all = root.querySelectorAll ? root.querySelectorAll('*') : [];
        for (const el of all) {
          if (predicate(el)) return el;
          if (el.shadowRoot) { const f = deepQS(el.shadowRoot, predicate); if (f) return f; }
        }
        return null;
      }
      const inp = deepQS(document, el => el.tagName === 'INPUT' && (
        (fieldType === 'text' && (el.type === 'text' || el.type === 'email')) ||
        (fieldType === 'password' && el.type === 'password')
      ));
      if (!inp) return { ok: false };
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(inp, value);
      inp.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
      inp.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
      const btn = deepQS(document, el => el.tagName === 'BUTTON' && el.type === 'submit');
      if (btn) { btn.click(); return { ok: true }; }
      return { ok: false };
    }, { value, fieldType });
  }

  await fillAndSubmit(user, 'text');
  await page.waitForTimeout(4000);
  await fillAndSubmit(pass, 'password');
  await page.waitForTimeout(6000);
}

(async () => {
  const args = parseArgs();

  // User visibility — headless: false required
  const browser = await chromium.launch({
    headless: false,
    slowMo: 800,
    args: ['--start-maximized']
  });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: true, viewport: null });
  const page = await ctx.newPage();

  console.log(`[1] navigate ${args.url}`);
  await page.goto(args.url, { waitUntil: 'domcontentloaded', timeout: 30000 });

  if (args.login) {
    console.log('[2] login');
    await loginIfNeeded(page, args.login);
  }

  console.log('[3] CDP session start (pierce=true)');
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');
  const { root } = await cdp.send('DOM.getDocument', { depth: -1, pierce: true });

  function attrsToObj(arr) {
    if (!arr) return {};
    const o = {};
    for (let i = 0; i < arr.length; i += 2) o[arr[i]] = arr[i + 1];
    return o;
  }

  function walk(node, found = []) {
    if (!node) return found;
    const a = attrsToObj(node.attributes);
    if (a.part) found.push({ id: node.nodeId, name: node.nodeName, part: a.part, class: a.class || '' });
    if (node.children) node.children.forEach(c => walk(c, found));
    if (node.shadowRoots) node.shadowRoots.forEach(s => walk(s, found));
    return found;
  }

  const all = walk(root);
  const targets = args.parts.length ? all.filter(t => args.parts.includes(t.part)) : all;

  console.log(`[4] found ${all.length} part-bearing elements; inspecting ${targets.length}`);

  const interesting = ['width', 'height', 'max-width', 'grid-template-columns', 'justify-content',
                        '--app-card-min-width', '--app-list-column-count', '--app-group-template-columns'];

  for (const t of targets) {
    console.log(`\n[part="${t.part}"] (nodeId=${t.id}, tag=${t.name}):`);
    try {
      const cs = await cdp.send('CSS.getComputedStyleForNode', { nodeId: t.id });
      for (const prop of interesting) {
        const v = cs.computedStyle.find(p => p.name === prop);
        if (v && v.value !== '' && v.value !== 'normal') console.log(`  ${prop}: ${v.value}`);
      }

      const matched = await cdp.send('CSS.getMatchedStylesForNode', { nodeId: t.id });
      console.log(`  matched CSS rules:`);
      for (const r of matched.matchedCSSRules || []) {
        const props = r.rule.style.cssProperties.filter(p => !p.disabled && interesting.some(i => p.name === i));
        if (!props.length) continue;
        console.log(`    [${r.rule.origin}] ${r.rule.selectorList.text} (sheet=${r.rule.styleSheetId})`);
        for (const p of props) {
          console.log(`      ${p.name}: ${p.value}${p.important ? ' !important' : ''}`);
        }
      }
    } catch (e) {
      console.log(`  ERROR: ${e.message}`);
    }
  }

  console.log('\n[5] done — browser open (close with X, force exit with Ctrl+C)');
  await new Promise(() => {}); // indefinite
})().catch(err => { console.error('ERR:', err.message); process.exit(1); });
