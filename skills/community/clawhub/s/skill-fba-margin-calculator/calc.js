#!/usr/bin/env node
/**
 * skill-fba-margin-calculator
 * Amazon UAE FBA fee estimator + margin ranker for CJ Dropshipping candidates.
 *
 * Usage:
 *   node calc.js --input products.json [--exchange 3.67] [--output report.md]
 *   node calc.js --sku CJLE2170569 --price 12.96 --weight 400 --target 129 --shipping 4
 *   cat products.json | node calc.js
 *
 * Input JSON (array):
 *   [{ sku, name, cj_price_usd, weight_g, target_aed, shipping_usd?, dg_risk?, referral_pct? }]
 *
 * Output: ranked markdown table + JSON
 */

const fs = require('fs');

// --- FBA fee tiers for Amazon UAE (Q1 2026 estimates) ---
const FBA_TIERS = [
  { label: 'Small Standard', maxWeight: 150, maxDims: [30, 20, 5], fee: 10 },
  { label: 'Standard S',     maxWeight: 350, fee: 13.5 },
  { label: 'Standard M',     maxWeight: 700, fee: 16.5 },
  { label: 'Standard L',     maxWeight: 1000, fee: 20 },
  { label: 'Large Standard', maxWeight: 2000, fee: 26 },
  { label: 'Oversize',       maxWeight: Infinity, fee: 38 },
];

const STORAGE_PER_UNIT = 0.75; // AED/unit/month avg

function getFbaFee(weightG) {
  for (const tier of FBA_TIERS) {
    if (weightG <= tier.maxWeight) return { fee: tier.fee, tier: tier.label };
  }
  return { fee: 38, tier: 'Oversize' };
}

function calcMargin(product, exchangeRate = 3.67) {
  const {
    sku,
    name,
    cj_price_usd,
    weight_g,
    target_aed,
    shipping_usd = 3.5,
    dg_risk = false,
    referral_pct = 8,
  } = product;

  const cj_aed = (parseFloat(cj_price_usd) + parseFloat(shipping_usd)) * exchangeRate;
  const { fee: fba_fee, tier } = getFbaFee(parseFloat(weight_g));
  const referral_fee = (target_aed * referral_pct) / 100;
  const total_fees = fba_fee + referral_fee + STORAGE_PER_UNIT;
  const net_margin_aed = target_aed - cj_aed - total_fees;
  const margin_pct = ((net_margin_aed / target_aed) * 100).toFixed(1);

  const recommendation =
    dg_risk
      ? '⚠️ DG RISK — WooCommerce-only (no FBA until DG cleared)'
      : net_margin_aed >= 30 && parseFloat(margin_pct) >= 25
      ? '✅ FBA-safe — READY'
      : net_margin_aed >= 15
      ? '🟡 MARGINAL — consider WooCommerce-only'
      : '❌ Too thin for FBA';

  return {
    sku,
    name: name || sku,
    cj_price_usd,
    shipping_usd,
    cj_landed_aed: +cj_aed.toFixed(1),
    fba_tier: tier,
    fba_fee,
    referral_fee: +referral_fee.toFixed(1),
    storage_fee: STORAGE_PER_UNIT,
    total_fees: +total_fees.toFixed(1),
    target_aed,
    net_margin_aed: +net_margin_aed.toFixed(1),
    margin_pct: +margin_pct,
    dg_risk: !!dg_risk,
    recommendation,
  };
}

function toMarkdown(results, exchangeRate) {
  const date = new Date().toISOString().split('T')[0];
  let md = `# Amazon UAE FBA Margin Report\n_Generated: ${date} | Exchange rate: 1 USD = ${exchangeRate} AED_\n\n`;

  md += `## Ranked Results (by margin %)\n\n`;
  md += `| Rank | SKU | Name | CJ+Ship (AED) | FBA Tier | Net Margin | Margin % | DG | Verdict |\n`;
  md += `|------|-----|------|--------------|----------|------------|----------|----|---------|\n`;

  results.forEach((r, i) => {
    md += `| ${i + 1} | ${r.sku} | ${r.name.substring(0, 35)} | ${r.cj_landed_aed} AED | ${r.fba_tier} | ${r.net_margin_aed} AED | ${r.margin_pct}% | ${r.dg_risk ? '⚠️' : '✅'} | ${r.recommendation} |\n`;
  });

  md += `\n## Detail\n\n`;
  results.forEach((r, i) => {
    md += `### ${i + 1}. ${r.name} (${r.sku})\n`;
    md += `- CJ price: $${r.cj_price_usd} + $${r.shipping_usd} shipping = **${r.cj_landed_aed} AED** landed\n`;
    md += `- FBA fee (${r.fba_tier}): ${r.fba_fee} AED\n`;
    md += `- Referral fee: ${r.referral_fee} AED\n`;
    md += `- Storage (avg): ${r.storage_fee} AED\n`;
    md += `- Total fees: ${r.total_fees} AED\n`;
    md += `- Target price: ${r.target_aed} AED → **Net margin: ${r.net_margin_aed} AED (${r.margin_pct}%)**\n`;
    md += `- **${r.recommendation}**\n\n`;
  });

  return md;
}

// --- CLI entrypoint ---
async function main() {
  const args = process.argv.slice(2);
  const exchangeRate = parseFloat(getArg(args, '--exchange') || '3.67');
  const outputFile = getArg(args, '--output');

  let products = [];

  // Single product via flags
  if (hasArg(args, '--sku')) {
    products = [{
      sku: getArg(args, '--sku'),
      name: getArg(args, '--name') || getArg(args, '--sku'),
      cj_price_usd: parseFloat(getArg(args, '--price')),
      weight_g: parseFloat(getArg(args, '--weight')),
      target_aed: parseFloat(getArg(args, '--target')),
      shipping_usd: parseFloat(getArg(args, '--shipping') || '3.5'),
      dg_risk: hasArg(args, '--dg'),
      referral_pct: parseFloat(getArg(args, '--referral') || '8'),
    }];
  } else {
    // JSON from --input file or stdin
    const inputFile = getArg(args, '--input');
    let raw = '';
    if (inputFile) {
      raw = fs.readFileSync(inputFile, 'utf8');
    } else if (!process.stdin.isTTY) {
      raw = fs.readFileSync('/dev/stdin', 'utf8');
    } else {
      console.error('Usage: node calc.js --input products.json OR pipe JSON via stdin');
      process.exit(1);
    }
    products = JSON.parse(raw);
  }

  const results = products
    .map(p => calcMargin(p, exchangeRate))
    .sort((a, b) => b.margin_pct - a.margin_pct);

  const md = toMarkdown(results, exchangeRate);
  const json = JSON.stringify(results, null, 2);

  if (outputFile) {
    const base = outputFile.replace(/\.(md|json)$/, '');
    fs.writeFileSync(base + '.md', md);
    fs.writeFileSync(base + '.json', json);
    console.log(`✅ Wrote ${base}.md + ${base}.json`);
  } else {
    console.log(md);
    console.log('\n--- JSON ---\n' + json);
  }
}

function getArg(args, flag) {
  const i = args.indexOf(flag);
  return i >= 0 && args[i + 1] ? args[i + 1] : null;
}
function hasArg(args, flag) {
  return args.includes(flag);
}

main().catch(e => { console.error(e); process.exit(1); });
