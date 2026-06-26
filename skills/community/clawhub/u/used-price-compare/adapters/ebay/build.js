#!/usr/bin/env node
/**
 * Generate per-country eBay adapters from _template.js.
 *
 * Usage:  node adapters/ebay/build.js
 * Output: adapters/ebay/search-{us,uk,au,ca}.js
 */
const fs = require('fs');
const path = require('path');

const SITES = [
  { country: 'us', domain: 'www.ebay.com',    currency: '$',  region: 'US (nationwide)', source: 'ebay.com' },
  { country: 'uk', domain: 'www.ebay.co.uk',  currency: '£',  region: 'UK (nationwide)', source: 'ebay.co.uk' },
  { country: 'au', domain: 'www.ebay.com.au', currency: 'A$', region: 'AU (nationwide)', source: 'ebay.com.au' },
  { country: 'ca', domain: 'www.ebay.ca',     currency: 'C$', region: 'CA (nationwide)', source: 'ebay.ca' },
];

const dir = path.dirname(__filename || __dirname);
const templatePath = path.join(dir, '_template.js');
const template = fs.readFileSync(templatePath, 'utf-8');

let generated = 0;
for (const site of SITES) {
  const content = template
    .replace(/\{\{COUNTRY\}\}/g, site.country)
    .replace(/\{\{DOMAIN\}\}/g, site.domain)
    .replace(/\{\{CURRENCY\}\}/g, site.currency)
    .replace(/\{\{REGION\}\}/g, site.region)
    .replace(/\{\{SOURCE\}\}/g, site.source);

  const outFile = path.join(dir, `search-${site.country}.js`);
  fs.writeFileSync(outFile, content, 'utf-8');
  generated++;
  console.log(`  ✓ ${path.basename(outFile)}  →  ${site.domain}`);
}

console.log(`\nGenerated ${generated} eBay adapter(s).`);
