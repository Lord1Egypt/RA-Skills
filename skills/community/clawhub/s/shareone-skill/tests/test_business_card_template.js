#!/usr/bin/env node
/**
 * Structural regression for templates/business-card.html.
 *
 *   node tests/test_business_card_template.js
 *
 * These are the invariants that break silently — a card whose QR still points at
 * the previous slug, or whose vCard quietly stopped matching the printed phone
 * number, looks perfect in a screenshot and is wrong in someone's hand.
 */

'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { encodeText, toPathData } = require('../scripts/make_qr.js');

const TEMPLATE = path.join(__dirname, '..', 'templates', 'business-card.html');
const html = fs.readFileSync(TEMPLATE, 'utf8');

// The URL the shipped template's QR is supposed to encode. Change the template's
// placeholder slug and this test tells you the QR was left behind.
const PLACEHOLDER_URL = 'https://s.shareone.vip/s/your-slug-here';

const FIELDS = ['name', 'title', 'org', 'tel', 'email', 'address', 'url'];

let failures = 0;
const check = (name, fn) => {
    try {
        fn();
        console.log(`  PASS  ${name}`);
    } catch (error) {
        failures++;
        console.log(`  FAIL  ${name}\n        ${error.message}`);
    }
};

// The script queries [data-field="name"] by selector, so field counting has to
// look at the markup only — otherwise the selector reads as a second card face.
const markup = html.slice(0, html.lastIndexOf('<script>'));

check('every data-field the script reads exists exactly once in the markup', () => {
    for (const f of FIELDS) {
        const hits = markup.match(new RegExp(`data-field="${f}"`, 'g')) || [];
        assert.strictEqual(hits.length, 1, `data-field="${f}" appears ${hits.length} times in markup, want 1`);
    }
});

check('the script reads the card face rather than duplicating values', () => {
    for (const f of FIELDS) {
        assert.ok(html.includes(`field('${f}')`) || f === 'name' || f === 'tel' || f === 'email',
            `script never reads field('${f}')`);
    }
    // A literal phone number anywhere in the <script> would mean the vCard has
    // its own copy of a value the card face already owns.
    const script = html.slice(html.lastIndexOf('<script>'));
    assert.ok(!/\b1[3-9]\d{9}\b/.test(script), 'a phone number is hard-coded in the script');
    assert.ok(!/@[\w.-]+\.(com|cn|io)\b/.test(script), 'an email address is hard-coded in the script');
});

check('data-surname is declared so the vCard can split a Chinese name', () => {
    const m = html.match(/data-field="name" data-surname="(\d+)"/);
    assert.ok(m, 'name element must carry data-surname');
    assert.ok(Number(m[1]) >= 1, 'data-surname must be at least 1');
});

check('QR matches what make_qr.js produces for the placeholder URL', () => {
    const m = html.match(/<path fill="#1A1A18" d="([^"]+)"\/>\s*<\/svg>\s*<\/span>/);
    assert.ok(m, 'could not find the QR path inside the chip');
    const expected = toPathData(encodeText(PLACEHOLDER_URL, 'Q'), 4);
    assert.strictEqual(
        m[1],
        expected,
        'the QR in the template is stale — regenerate it with make_qr.js after changing the slug',
    );
});

check('QR viewBox matches the generated module count', () => {
    const qr = encodeText(PLACEHOLDER_URL, 'Q');
    const dimension = qr.size + 8; // 4-module quiet zone on each side
    assert.ok(
        html.includes(`viewBox="0 0 ${dimension} ${dimension}"`),
        `chip viewBox should be ${dimension}; a mismatched viewBox silently crops or pads the code`,
    );
});

check('QR is dark-on-light (inverted codes defeat some scanners)', () => {
    assert.ok(/class="chip"/.test(html), 'QR must sit on its own light chip');
    assert.ok(/\.chip \{[^}]*background: #fff/.test(html), '.chip must be white');
    assert.ok(/<path fill="#1A1A18" d="M/.test(html), 'QR modules must be dark');
});

check('print page is exactly a 90x54mm card with no margin', () => {
    assert.ok(/@page \{ size: 90mm 54mm; margin: 0; \}/.test(html), 'missing exact @page rule');
    assert.ok(/--card-w: 90mm/.test(html) && /--card-h: 54mm/.test(html), 'card size vars missing');
    assert.ok(/print-color-adjust: exact/.test(html), 'the dark face would print blank without this');
});

check('no external resources — the page must work in a stranger browser offline', () => {
    const external = [...html.matchAll(/\b(?:src|href)\s*=\s*"(https?:)?\/\/[^"]*"/g)].map((m) => m[0]);
    const offenders = external.filter((s) => !/xmlns/.test(s));
    assert.deepStrictEqual(offenders, [], `external resource(s): ${offenders.join(', ')}`);
    assert.ok(!/@import|fonts\.googleapis/.test(html), 'no webfont imports');
});

check('no real personal data shipped in the template', () => {
    for (const leak of ['数牍', '王楚乔', 'sudoprivacy', '13889575677']) {
        assert.ok(!html.includes(leak), `template leaks "${leak}"`);
    }
});

console.log();
if (failures) {
    console.log(`${failures} FAILED`);
    process.exit(1);
}
console.log('ALL 9 CHECKS PASS');
