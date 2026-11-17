#!/usr/bin/env node
/**
 * Regression test for scripts/make_qr.js. Zero dependencies — runs on a bare
 * `node`, like everything else in this skill.
 *
 *   node tests/test_make_qr.js
 *
 * The golden hashes below were verified module-for-module against the `qrcode`
 * npm reference implementation (39/39 matrices identical across versions 1-32
 * and all four ECC levels) and confirmed to decode back to their source text.
 * If a hash moves, the encoder changed — a QR that merely *looks* right can
 * still decode to garbage, so re-verify against an independent encoder rather
 * than refreshing the constants.
 */

'use strict';

const assert = require('assert');
const crypto = require('crypto');
const { encodeText, toSvg, toPathData } = require('../scripts/make_qr.js');

const VCARD = 'BEGIN:VCARD\r\nVERSION:3.0\r\nFN:王楚乔\r\nTEL:13889575677\r\nEND:VCARD\r\n';

// [text, ecc, version, size, mask, sha256-prefix of the flattened matrix]
const GOLDEN = [
    ['A', 'H', 1, 21, 7, 'd38f398db3302bbc'],
    ['A', 'Q', 1, 21, 0, '030c33b9be0e8734'],
    ['https://sudowork.sudoprivacy.com/', 'L', 3, 29, 3, '9229dad37148e00c'],
    ['https://sudowork.sudoprivacy.com/', 'M', 3, 29, 2, '931ab677a0a28131'],
    ['https://sudowork.sudoprivacy.com/', 'Q', 4, 33, 6, '55f06f6d7557acd4'],
    ['https://sudowork.sudoprivacy.com/', 'H', 4, 33, 1, '5738e7f5c0a6c51d'],
    ['https://s.shareone.vip/s/abcd1234', 'Q', 4, 33, 6, 'e0a799b62fb596ab'],
    ['数牍科技 王楚乔 商业化总监', 'Q', 4, 33, 4, 'a9de95a5fd3ee1de'],
    ['数牍科技 王楚乔 商业化总监', 'H', 5, 37, 7, 'd9ba936c3056241b'],
    [VCARD, 'M', 5, 37, 3, 'f4d9ca818ccda67a'],
    ['x'.repeat(120), 'M', 7, 45, 2, '41c119024543b539'], // v7+: version info blocks
    ['x'.repeat(800), 'L', 20, 97, 0, '46e5eec3063e78ea'],
    ['y'.repeat(1500), 'M', 32, 145, 0, 'f6aba75a68c34ec0'], // v32: special alignment step
    ['0123456789'.repeat(20), 'Q', 12, 65, 2, '9aac9d7956697e21'],
];

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

const hashMatrix = (qr) =>
    crypto
        .createHash('sha256')
        .update(qr.modules.map((row) => row.map((c) => (c ? '1' : '0')).join('')).join(''))
        .digest('hex')
        .slice(0, 16);

for (const [text, ecc, version, size, mask, sha] of GOLDEN) {
    const label = `${JSON.stringify(text.length > 20 ? `${text.slice(0, 20)}…` : text)} ${ecc}`;
    check(`golden ${label}`, () => {
        const qr = encodeText(text, ecc);
        assert.strictEqual(qr.version, version, `version ${qr.version} != ${version}`);
        assert.strictEqual(qr.size, size, `size ${qr.size} != ${size}`);
        assert.strictEqual(qr.mask, mask, `mask ${qr.mask} != ${mask}`);
        assert.strictEqual(hashMatrix(qr), sha, `matrix hash ${hashMatrix(qr)} != ${sha}`);
    });
}

check('finder patterns in all three corners', () => {
    const qr = encodeText('https://s.shareone.vip/s/test', 'Q');
    const n = qr.size;
    for (const [ox, oy] of [[0, 0], [n - 7, 0], [0, n - 7]]) {
        for (let dy = 0; dy < 7; dy++) {
            for (let dx = 0; dx < 7; dx++) {
                const ring = Math.max(Math.abs(dx - 3), Math.abs(dy - 3));
                assert.strictEqual(
                    qr.modules[oy + dy][ox + dx],
                    ring !== 2,
                    `finder at ${ox},${oy} wrong at ${dx},${dy}`,
                );
            }
        }
    }
});

check('timing patterns alternate', () => {
    const qr = encodeText('timing', 'M');
    for (let i = 8; i < qr.size - 8; i++) {
        assert.strictEqual(qr.modules[6][i], i % 2 === 0, `row timing broken at ${i}`);
        assert.strictEqual(qr.modules[i][6], i % 2 === 0, `col timing broken at ${i}`);
    }
});

check('dark module is always set', () => {
    for (const ecc of ['L', 'M', 'Q', 'H']) {
        const qr = encodeText('dark module', ecc);
        assert.strictEqual(qr.modules[qr.size - 8][8], true, `dark module unset for ${ecc}`);
    }
});

check('svg path describes exactly the dark modules', () => {
    const qr = encodeText('https://s.shareone.vip/s/path-check', 'Q');
    const margin = 4;
    const d = toPathData(qr, margin);
    const cells = new Set();
    for (const m of d.matchAll(/M(\d+) (\d+)h(\d+)v1h-\d+z/g)) {
        for (let i = 0; i < Number(m[3]); i++) {
            cells.add(`${Number(m[1]) - margin + i},${Number(m[2]) - margin}`);
        }
    }
    const expected = new Set();
    for (let y = 0; y < qr.size; y++) {
        for (let x = 0; x < qr.size; x++) if (qr.modules[y][x]) expected.add(`${x},${y}`);
    }
    assert.strictEqual(cells.size, expected.size, `path has ${cells.size} cells, matrix has ${expected.size}`);
    for (const cell of expected) assert.ok(cells.has(cell), `path missing module ${cell}`);
});

check('svg viewBox accounts for the quiet zone', () => {
    const qr = encodeText('quiet zone', 'M');
    const svg = toSvg(qr, { margin: 4, color: '#000000', bg: 'none', id: null });
    const expected = qr.size + 8;
    assert.ok(
        svg.includes(`viewBox="0 0 ${expected} ${expected}"`),
        `viewBox should be ${expected}, got: ${svg.slice(0, 160)}`,
    );
    // No width/height: the caller sizes it in CSS so one SVG serves print and web.
    assert.ok(!/\swidth="/.test(svg), 'svg must not hard-code a width');
});

check('svg escapes attacker-controlled colour and id', () => {
    const qr = encodeText('escaping', 'L');
    const svg = toSvg(qr, { margin: 4, color: '"><script>alert(1)</script>', bg: 'none', id: 'a"b' });
    assert.ok(!svg.includes('<script>'), 'colour must not break out of the attribute');
    assert.ok(!svg.includes('id="a"b"'), 'id must be escaped');
});

check('utf-8 is encoded by byte length, not character count', () => {
    // 21 chars but 63 UTF-8 bytes — sizing on `.length` would silently truncate.
    const text = '数'.repeat(21);
    const qr = encodeText(text, 'L');
    assert.strictEqual(qr.version, 4, `expected v4 for 63 bytes, got v${qr.version}`);
});

check('over-capacity input fails loudly', () => {
    assert.throws(
        () => encodeText('z'.repeat(3000), 'H'),
        /TEXT_TOO_LONG/,
        'should reject text past version 40 capacity',
    );
});

check('unknown ecc level fails loudly', () => {
    assert.throws(() => encodeText('x', 'Z'), /UNKNOWN_ECC/);
});

console.log();
if (failures) {
    console.log(`${failures} FAILED`);
    process.exit(1);
}
console.log(`ALL ${GOLDEN.length + 9} CHECKS PASS`);
