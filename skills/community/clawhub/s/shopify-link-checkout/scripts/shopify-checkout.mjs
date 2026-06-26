#!/usr/bin/env node
/**
 * Shopify Autonomous Checkout via Playwright
 *
 * Handles both single-page and multi-step Shopify checkouts.
 * Uses cart permalink to bypass Cloudflare.
 *
 * Usage:
 *   node shopify-checkout.mjs <store-domain> <variant-id> <card-number> <MM/YY> <cvc> [options]
 *
 * Options:
 *   --email <email>          Buyer email
 *   --first <name>           First name
 *   --last <name>            Last name
 *   --address "<street>"     Street address
 *   --apt "<unit>"           Apartment/suite (optional)
 *   --city "<city>"          City
 *   --state <ST>             State code (e.g. FL)
 *   --zip <zip>              ZIP/postal code
 *   --phone <phone>          Phone number (digits only, no dashes)
 *   --card-name "<name>"     Name on card (defaults to first + last)
 *
 * Example:
 *   node shopify-checkout.mjs krink.com 943039957 4866560007880691 04/29 850 \
 *     --email me@example.com --first Stephen --last Liriano \
 *     --address "11 Plaza Real S" --apt "Apt 218" \
 *     --city "Boca Raton" --state FL --zip 33432 --phone 4843325580
 *
 * Requires: playwright (npm install playwright), Chromium installed
 * Set LD_LIBRARY_PATH if using manually extracted Chromium deps (see references/chromium-deps.md)
 */

import { chromium } from 'playwright';

// Parse CLI args
const args = process.argv.slice(2);
const positional = [];
const opts = {};

for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--') && i + 1 < args.length) {
    opts[args[i].replace('--', '')] = args[++i];
  } else {
    positional.push(args[i]);
  }
}

const [storeDomain, variantId, cardNumber, cardExp, cardCvc] = positional;

if (!storeDomain || !variantId || !cardNumber || !cardExp || !cardCvc) {
  console.error('Usage: node shopify-checkout.mjs <domain> <variant-id> <card-num> <MM/YY> <cvc> --email ... --first ... --last ... --address ... --city ... --state ... --zip ... --phone ...');
  process.exit(1);
}

const BUYER = {
  email: opts.email || '',
  firstName: opts.first || '',
  lastName: opts.last || '',
  address: opts.address || '',
  apt: opts.apt || '',
  city: opts.city || '',
  state: opts.state || '',
  zip: opts.zip || '',
  phone: opts.phone || '',
  cardName: opts['card-name'] || `${opts.first || ''} ${opts.last || ''}`.trim(),
};

// Validate required fields
const missing = [];
for (const [k, v] of Object.entries(BUYER)) {
  if (!v && !['apt', 'phone'].includes(k)) missing.push(k);
}
if (missing.length > 0) {
  console.error(`Missing required buyer info: ${missing.join(', ')}`);
  process.exit(1);
}

async function run() {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-blink-features=AutomationControlled'],
  });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    viewport: { width: 1440, height: 900 },
  });
  const page = await ctx.newPage();
  page.setDefaultTimeout(25000);

  const storeUrl = storeDomain.startsWith('http') ? storeDomain : `https://${storeDomain}`;

  try {
    // ── Cart permalink → checkout (bypasses Cloudflare) ──
    console.log(`1. Checkout on ${storeDomain}...`);
    await page.goto(`${storeUrl}/cart/${variantId}:1`, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await page.waitForTimeout(6000);

    if ((await page.title()).includes('moment')) {
      throw new Error('CLOUDFLARE_BLOCKED');
    }

    // Dismiss any modal overlays (Shop Pay, login, etc.)
    await page.keyboard.press('Escape');
    await page.waitForTimeout(500);
    await page.evaluate(() => {
      document.querySelectorAll('[data-type="modal"], [data-variant="checkoutModal"]').forEach(el => el.remove());
    });

    await page.waitForSelector('#email', { timeout: 15000 });

    // Detect checkout type
    const isMultiStep = (await page.locator('button:has-text("Continue to shipping")').count()) > 0
      && !page.frames().some(f => f.url().includes('card-fields'));
    console.log(`   ${isMultiStep ? 'Multi-step' : 'Single-page'} checkout`);

    // ── Fill contact + shipping ──
    console.log('2. Filling info...');
    await page.fill('#email', BUYER.email);

    // Dismiss modal again after email (some stores trigger it on email blur)
    await page.waitForTimeout(500);
    await page.evaluate(() => {
      document.querySelectorAll('[data-type="modal"]').forEach(el => el.remove());
    });

    const fillVisible = async (name, value) => {
      for (const inp of await page.locator(`input[name="${name}"]`).all()) {
        if (await inp.isVisible()) { await inp.fill(value); return true; }
      }
      return false;
    };

    await fillVisible('firstName', BUYER.firstName);
    await fillVisible('lastName', BUYER.lastName);

    // Address: type with city for autocomplete suggestions
    const addrInput = page.locator('#shipping-address1');
    await addrInput.click();
    await addrInput.pressSequentially(`${BUYER.address}, ${BUYER.city}`, { delay: 60 });
    await page.waitForTimeout(2500);
    const suggestion = page.locator('[role="option"]').first();
    if (await suggestion.count() > 0) {
      await suggestion.click();
      await page.waitForTimeout(2000);
    } else {
      await page.keyboard.press('Escape');
      await page.waitForTimeout(500);
      await fillVisible('city', BUYER.city);
      await page.selectOption('select[name="zone"]', BUYER.state);
      await fillVisible('postalCode', BUYER.zip);
    }

    // Apartment
    const aptField = page.locator('input[name="address2"]:visible').first();
    if (BUYER.apt && await aptField.count() > 0 && (await aptField.inputValue()) === '') {
      await aptField.fill(BUYER.apt);
    }

    // Phone (type, don't fill)
    if (BUYER.phone) {
      const phoneField = page.locator('input[name="phone"]:visible').first();
      if (await phoneField.count() > 0) {
        await phoneField.click();
        await phoneField.pressSequentially(BUYER.phone, { delay: 50 });
        await page.keyboard.press('Tab');
        await page.waitForTimeout(500);
      }
    }

    // ── Navigate checkout steps ──
    if (isMultiStep) {
      console.log('3. → Shipping...');
      await page.locator('button:has-text("Continue to shipping"):not([aria-hidden="true"])').first().click({ force: true });
      await page.waitForTimeout(10000);
      if (!page.url().includes('shipping')) throw new Error('STUCK_AT_INFO');

      await page.waitForTimeout(3000);
      const sr = await page.locator('input[name="shipping_methods"]').all();
      console.log(`   ${sr.length} shipping options`);
      if (sr.length > 0) await sr[0].click();
      await page.waitForTimeout(1000);

      console.log('4. → Payment...');
      await page.locator('button:has-text("Continue to payment"):not([aria-hidden="true"])').first().click({ force: true });
      await page.waitForTimeout(10000);
      if (!page.url().includes('payment')) throw new Error('STUCK_AT_SHIPPING');
      await page.waitForTimeout(3000);
    } else {
      console.log('3. Waiting for shipping rates...');
      await page.waitForTimeout(6000);
      const sr = await page.locator('input[name="shipping_methods"]').all();
      if (sr.length > 0) await sr[0].click();
      await page.waitForTimeout(2000);

      const ccRadio = page.locator('input[aria-label="Credit card"]');
      if (await ccRadio.count() > 0) await ccRadio.click();
      await page.waitForTimeout(3000);
    }

    // ── Fill card in PCI iframes ──
    console.log('5. Card...');
    const fillFrame = async (urlPart, selector, value) => {
      const frame = page.frames().find(f => f.url().includes(urlPart));
      if (frame) { await frame.fill(selector, value); return true; }
      return false;
    };

    await fillFrame('number-ltr', '#number', cardNumber);
    await fillFrame('name-ltr', '#name', BUYER.cardName);
    await fillFrame('expiry-ltr', '#expiry', cardExp);
    await fillFrame('verification_value-ltr', '#verification_value', cardCvc);

    await page.waitForTimeout(2000);

    // ── Pay ──
    console.log('6. PAY!');
    await page.locator('button:has-text("Pay now")').first().click();
    console.log('   Clicked Pay now');

    // The click IS the purchase. Wait for confirmation.
    await page.waitForTimeout(20000);
    const finalUrl = page.url();

    if (finalUrl.includes('thank_you') || finalUrl.includes('thank-you')) {
      const bodyText = await page.evaluate(() => document.body.innerText).catch(() => '');
      const orderMatch = bodyText.match(/[Cc]onfirmation\s*#?(\w+)/) || bodyText.match(/#(\w+)/);
      console.log(`\n✅ ORDER CONFIRMED${orderMatch ? ` — ${orderMatch[0]}` : ''}`);
    } else {
      const errors = await page.evaluate(() =>
        Array.from(document.querySelectorAll('[role="alert"], [class*="banner"]'))
          .map(e => e.textContent.trim()).filter(t => t.length > 5 && t.length < 300)
      ).catch(() => []);

      if (errors.some(e => e.includes('declined') || e.includes('issue'))) {
        console.log(`\n❌ PAYMENT FAILED: ${errors.join(' | ')}`);
      } else {
        console.log('\n⚠️  Check email — order may have been placed (browser did not redirect)');
      }
    }

  } catch (err) {
    console.error(`\n❌ ${err.message}`);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
