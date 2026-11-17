#!/usr/bin/env node
/**
 * make_qr.js — QR Code generator (byte mode, UTF-8). Zero dependencies.
 *
 * Emits an SVG whose dark modules are ONE <path>, so the result can be inlined
 * straight into a published page: no runtime library, no network fetch, no
 * raster artifact that goes blurry when the page is printed or zoomed.
 *
 * This skill ships with no package.json on purpose — every script runs on a
 * bare `node` with builtins only. That is why the encoder lives here in full
 * rather than arriving as an npm dependency.
 *
 * Usage:
 *   node make_qr.js --text "https://s.shareone.vip/s/abc" [options]
 *
 * Options:
 *   --text <string>    Content to encode (or --file <path> to read it).
 *   --file <path>      Read the content from a UTF-8 file (for vCard blobs).
 *   --ecc <L|M|Q|H>    Error correction level. Default Q — survives a printed
 *                      card getting scuffed, and leaves room for a logo knockout.
 *   --format <fmt>     svg (default) | path | json
 *                        svg  — a complete <svg> element
 *                        path — just the `d` attribute value
 *                        json — {version,size,ecc,modules:[[0|1,...]]}
 *   --out <path>       Write to a file instead of stdout.
 *   --margin <n>       Quiet zone in modules. Default 4 (the spec minimum).
 *   --color <css>      Dark module colour. Default #000000.
 *   --bg <css>         Background colour, or `none` (default) for transparent.
 *   --id <string>      Adds an id attribute to the <svg> element.
 *
 * Output is deliberately viewBox-only (no width/height): the caller sizes it in
 * CSS, so the same SVG serves a 20mm print card and a 300px web page.
 */

'use strict';

const fs = require('fs');

// ---------------------------------------------------------------------------
// QR spec tables. Index 0 is unused so the arrays are addressed by version 1-40.
// ---------------------------------------------------------------------------

const ECC_LEVELS = {
    // formatBits is what gets baked into the format information area — it is
    // NOT the same ordering as the table index below. Mixing them up produces a
    // QR that looks perfect and decodes as garbage, so both are named.
    L: { index: 0, formatBits: 1 },
    M: { index: 1, formatBits: 0 },
    Q: { index: 2, formatBits: 3 },
    H: { index: 3, formatBits: 2 },
};

const ECC_CODEWORDS_PER_BLOCK = [
    // L
    [-1, 7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28, 28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    // M
    [-1, 10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26, 26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
    // Q
    [-1, 13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28, 26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    // H
    [-1, 17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28, 26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
];

const NUM_ERROR_CORRECTION_BLOCKS = [
    // L
    [-1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],
    // M
    [-1, 1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17, 18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],
    // Q
    [-1, 1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23, 23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65, 68],
    // H
    [-1, 1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25, 34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77, 81],
];

const MIN_VERSION = 1;
const MAX_VERSION = 40;

// ---------------------------------------------------------------------------
// GF(256) arithmetic for Reed-Solomon, modulo x^8 + x^4 + x^3 + x^2 + 1.
// ---------------------------------------------------------------------------

function gfMultiply(x, y) {
    let z = 0;
    for (let i = 7; i >= 0; i--) {
        z = (z << 1) ^ ((z >>> 7) * 0x11d);
        z ^= ((y >>> i) & 1) * x;
    }
    return z & 0xff;
}

function rsComputeDivisor(degree) {
    const result = new Uint8Array(degree);
    result[degree - 1] = 1;
    let root = 1;
    for (let i = 0; i < degree; i++) {
        for (let j = 0; j < degree; j++) {
            result[j] = gfMultiply(result[j], root);
            if (j + 1 < degree) result[j] ^= result[j + 1];
        }
        root = gfMultiply(root, 0x02);
    }
    return result;
}

function rsComputeRemainder(data, divisor) {
    const result = new Uint8Array(divisor.length);
    for (const b of data) {
        const factor = b ^ result[0];
        result.copyWithin(0, 1);
        result[result.length - 1] = 0;
        for (let i = 0; i < result.length; i++) {
            result[i] ^= gfMultiply(divisor[i], factor);
        }
    }
    return result;
}

// ---------------------------------------------------------------------------
// Capacity maths
// ---------------------------------------------------------------------------

function getNumRawDataModules(version) {
    let result = (16 * version + 128) * version + 64;
    if (version >= 2) {
        const numAlign = Math.floor(version / 7) + 2;
        result -= (25 * numAlign - 10) * numAlign - 55;
        if (version >= 7) result -= 36;
    }
    return result;
}

function getNumDataCodewords(version, eccIndex) {
    return (
        Math.floor(getNumRawDataModules(version) / 8) -
        ECC_CODEWORDS_PER_BLOCK[eccIndex][version] * NUM_ERROR_CORRECTION_BLOCKS[eccIndex][version]
    );
}

function getAlignmentPatternPositions(version) {
    if (version === 1) return [];
    const numAlign = Math.floor(version / 7) + 2;
    const size = version * 4 + 17;
    const step = version === 32 ? 26 : Math.ceil((version * 4 + 4) / (numAlign * 2 - 2)) * 2;
    const result = [6];
    for (let pos = size - 7; result.length < numAlign; pos -= step) {
        result.splice(1, 0, pos);
    }
    return result;
}

// ---------------------------------------------------------------------------
// Encoding
// ---------------------------------------------------------------------------

function encodeSegmentBits(bytes, version) {
    const bits = [];
    const push = (value, length) => {
        for (let i = length - 1; i >= 0; i--) bits.push((value >>> i) & 1);
    };
    push(0x4, 4); // byte mode indicator
    push(bytes.length, version <= 9 ? 8 : 16); // character count indicator
    for (const b of bytes) push(b, 8);
    return bits;
}

function buildCodewords(bytes, version, eccIndex) {
    const dataCapacityBits = getNumDataCodewords(version, eccIndex) * 8;
    const bits = encodeSegmentBits(bytes, version);

    // Terminator, then pad to a byte boundary, then alternating pad codewords.
    for (let i = 0; i < 4 && bits.length < dataCapacityBits; i++) bits.push(0);
    while (bits.length % 8 !== 0) bits.push(0);
    const dataCodewords = new Uint8Array(dataCapacityBits / 8);
    for (let i = 0; i < bits.length; i++) {
        dataCodewords[i >>> 3] |= bits[i] << (7 - (i & 7));
    }
    for (let i = bits.length / 8, pad = 0xec; i < dataCodewords.length; i++, pad ^= 0xec ^ 0x11) {
        dataCodewords[i] = pad;
    }

    // Split into blocks, append RS codewords, then interleave.
    const numBlocks = NUM_ERROR_CORRECTION_BLOCKS[eccIndex][version];
    const blockEccLen = ECC_CODEWORDS_PER_BLOCK[eccIndex][version];
    const rawCodewords = Math.floor(getNumRawDataModules(version) / 8);
    const numShortBlocks = numBlocks - (rawCodewords % numBlocks);
    const shortBlockLen = Math.floor(rawCodewords / numBlocks);

    const blocks = [];
    const divisor = rsComputeDivisor(blockEccLen);
    for (let i = 0, k = 0; i < numBlocks; i++) {
        const datLen = shortBlockLen - blockEccLen + (i < numShortBlocks ? 0 : 1);
        const dat = dataCodewords.slice(k, k + datLen);
        k += datLen;
        const ecc = rsComputeRemainder(dat, divisor);
        blocks.push({ dat, ecc });
    }

    const result = [];
    for (let i = 0; i < shortBlockLen - blockEccLen + 1; i++) {
        blocks.forEach((block, j) => {
            // The longer blocks carry one extra data codeword; it is interleaved
            // last, after every short block has been exhausted.
            if (i < block.dat.length && !(i === shortBlockLen - blockEccLen && j < numShortBlocks)) {
                result.push(block.dat[i]);
            }
        });
    }
    for (let i = 0; i < blockEccLen; i++) {
        for (const block of blocks) result.push(block.ecc[i]);
    }
    return result;
}

// ---------------------------------------------------------------------------
// Matrix construction
// ---------------------------------------------------------------------------

function createMatrix(version, eccLevel, codewords) {
    const size = version * 4 + 17;
    const modules = Array.from({ length: size }, () => new Array(size).fill(false));
    const isFunction = Array.from({ length: size }, () => new Array(size).fill(false));

    const setFunctionModule = (x, y, isDark) => {
        modules[y][x] = isDark;
        isFunction[y][x] = true;
    };

    // Timing patterns
    for (let i = 0; i < size; i++) {
        setFunctionModule(6, i, i % 2 === 0);
        setFunctionModule(i, 6, i % 2 === 0);
    }

    // Finder patterns (plus their separators, drawn as a 9x9 block)
    const drawFinder = (cx, cy) => {
        for (let dy = -4; dy <= 4; dy++) {
            for (let dx = -4; dx <= 4; dx++) {
                const dist = Math.max(Math.abs(dx), Math.abs(dy));
                const x = cx + dx;
                const y = cy + dy;
                if (x >= 0 && x < size && y >= 0 && y < size) {
                    setFunctionModule(x, y, dist !== 2 && dist !== 4);
                }
            }
        }
    };
    drawFinder(3, 3);
    drawFinder(size - 4, 3);
    drawFinder(3, size - 4);

    // Alignment patterns, skipping the three finder corners
    const alignPositions = getAlignmentPatternPositions(version);
    const numAlign = alignPositions.length;
    for (let i = 0; i < numAlign; i++) {
        for (let j = 0; j < numAlign; j++) {
            if ((i === 0 && j === 0) || (i === 0 && j === numAlign - 1) || (i === numAlign - 1 && j === 0)) {
                continue;
            }
            for (let dy = -2; dy <= 2; dy++) {
                for (let dx = -2; dx <= 2; dx++) {
                    setFunctionModule(
                        alignPositions[i] + dx,
                        alignPositions[j] + dy,
                        Math.max(Math.abs(dx), Math.abs(dy)) !== 1,
                    );
                }
            }
        }
    }

    // Version information (version 7 and up), BCH(18,6)
    if (version >= 7) {
        let rem = version;
        for (let i = 0; i < 12; i++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1f25);
        const bits = (version << 12) | rem;
        for (let i = 0; i < 18; i++) {
            const isDark = ((bits >>> i) & 1) !== 0;
            const a = size - 11 + (i % 3);
            const b = Math.floor(i / 3);
            setFunctionModule(a, b, isDark);
            setFunctionModule(b, a, isDark);
        }
    }

    // Reserve the format information area (written for real after masking).
    drawFormatBits(modules, isFunction, size, eccLevel, 0, true);

    // Data placement: two-module-wide columns, right to left, zigzagging.
    let i = 0;
    for (let right = size - 1; right >= 1; right -= 2) {
        if (right === 6) right = 5; // skip the vertical timing column
        for (let vert = 0; vert < size; vert++) {
            for (let j = 0; j < 2; j++) {
                const x = right - j;
                const upward = ((right + 1) & 2) === 0;
                const y = upward ? size - 1 - vert : vert;
                if (!isFunction[y][x] && i < codewords.length * 8) {
                    modules[y][x] = ((codewords[i >>> 3] >>> (7 - (i & 7))) & 1) !== 0;
                    i++;
                }
            }
        }
    }

    // Try all eight masks, keep the one the spec's penalty rules like best.
    let bestMask = 0;
    let minPenalty = Infinity;
    for (let mask = 0; mask < 8; mask++) {
        applyMask(modules, isFunction, size, mask);
        drawFormatBits(modules, isFunction, size, eccLevel, mask, false);
        const penalty = getPenaltyScore(modules, size);
        if (penalty < minPenalty) {
            minPenalty = penalty;
            bestMask = mask;
        }
        applyMask(modules, isFunction, size, mask); // XOR is its own inverse
    }
    applyMask(modules, isFunction, size, bestMask);
    drawFormatBits(modules, isFunction, size, eccLevel, bestMask, false);

    return { size, modules, mask: bestMask };
}

function drawFormatBits(modules, isFunction, size, eccLevel, mask, reserveOnly) {
    const data = (ECC_LEVELS[eccLevel].formatBits << 3) | mask;
    let rem = data;
    for (let i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
    const bits = ((data << 10) | rem) ^ 0x5412; // BCH(15,5) then the spec's mask

    const put = (x, y, bitIndex) => {
        modules[y][x] = reserveOnly ? false : ((bits >>> bitIndex) & 1) !== 0;
        isFunction[y][x] = true;
    };

    // Copy 1, around the top-left finder
    for (let i = 0; i <= 5; i++) put(8, i, i);
    put(8, 7, 6);
    put(8, 8, 7);
    put(7, 8, 8);
    for (let i = 9; i < 15; i++) put(14 - i, 8, i);

    // Copy 2, split between the other two finders
    for (let i = 0; i < 8; i++) put(size - 1 - i, 8, i);
    for (let i = 8; i < 15; i++) put(8, size - 15 + i, i);

    // The dark module is always set, and is never part of the format data.
    modules[size - 8][8] = true;
    isFunction[size - 8][8] = true;
}

function applyMask(modules, isFunction, size, mask) {
    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            if (isFunction[y][x]) continue;
            let invert;
            switch (mask) {
                case 0: invert = (x + y) % 2 === 0; break;
                case 1: invert = y % 2 === 0; break;
                case 2: invert = x % 3 === 0; break;
                case 3: invert = (x + y) % 3 === 0; break;
                case 4: invert = (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0; break;
                case 5: invert = ((x * y) % 2) + ((x * y) % 3) === 0; break;
                case 6: invert = (((x * y) % 2) + ((x * y) % 3)) % 2 === 0; break;
                case 7: invert = (((x + y) % 2) + ((x * y) % 3)) % 2 === 0; break;
                default: throw new Error(`unreachable mask ${mask}`);
            }
            if (invert) modules[y][x] = !modules[y][x];
        }
    }
}

function getPenaltyScore(modules, size) {
    const N1 = 3;
    const N2 = 3;
    const N3 = 40;
    const N4 = 10;
    let result = 0;

    // Rule 1: runs of five or more same-coloured modules along a row or column.
    for (let i = 0; i < size; i++) {
        let sameCountRow = 0;
        let sameCountCol = 0;
        let lastRow = null;
        let lastCol = null;
        for (let j = 0; j < size; j++) {
            const rowModule = modules[i][j];
            if (rowModule === lastRow) {
                sameCountRow++;
            } else {
                if (sameCountRow >= 5) result += N1 + (sameCountRow - 5);
                lastRow = rowModule;
                sameCountRow = 1;
            }
            const colModule = modules[j][i];
            if (colModule === lastCol) {
                sameCountCol++;
            } else {
                if (sameCountCol >= 5) result += N1 + (sameCountCol - 5);
                lastCol = colModule;
                sameCountCol = 1;
            }
        }
        if (sameCountRow >= 5) result += N1 + (sameCountRow - 5);
        if (sameCountCol >= 5) result += N1 + (sameCountCol - 5);
    }

    // Rule 2: 2x2 blocks of a single colour.
    for (let y = 0; y < size - 1; y++) {
        for (let x = 0; x < size - 1; x++) {
            const c = modules[y][x];
            if (c === modules[y][x + 1] && c === modules[y + 1][x] && c === modules[y + 1][x + 1]) {
                result += N2;
            }
        }
    }

    // Rule 3: the finder's 1:1:3:1:1 ratio flanked by four light modules,
    // matched as an 11-module sliding window in both orientations. This literal
    // bit-window form (0x5D0 / 0x05D) is what ZXing and the common encoders use;
    // the generalised run-history reading of the same clause picks a different
    // mask on ties, which would make our output differ from every other encoder
    // for no benefit.
    for (let i = 0; i < size; i++) {
        let bitsRow = 0;
        let bitsCol = 0;
        for (let j = 0; j < size; j++) {
            bitsRow = ((bitsRow << 1) & 0x7ff) | (modules[i][j] ? 1 : 0);
            if (j >= 10 && (bitsRow === 0x5d0 || bitsRow === 0x05d)) result += N3;
            bitsCol = ((bitsCol << 1) & 0x7ff) | (modules[j][i] ? 1 : 0);
            if (j >= 10 && (bitsCol === 0x5d0 || bitsCol === 0x05d)) result += N3;
        }
    }

    // Rule 4: deviation of the dark-module proportion from 50%, in 5% steps.
    let dark = 0;
    for (const row of modules) for (const cell of row) if (cell) dark++;
    const k = Math.abs(Math.ceil((dark * 100) / (size * size) / 5) - 10);
    result += k * N4;

    return result;
}

// ---------------------------------------------------------------------------
// Public encode
// ---------------------------------------------------------------------------

function encodeText(text, eccLevel) {
    const level = ECC_LEVELS[eccLevel];
    if (!level) throw new Error(`UNKNOWN_ECC:${eccLevel}`);
    const bytes = Buffer.from(text, 'utf8');

    let version = -1;
    for (let v = MIN_VERSION; v <= MAX_VERSION; v++) {
        const capacityBits = getNumDataCodewords(v, level.index) * 8;
        const headerBits = 4 + (v <= 9 ? 8 : 16);
        if (headerBits + bytes.length * 8 <= capacityBits) {
            version = v;
            break;
        }
    }
    if (version < 0) throw new Error(`TEXT_TOO_LONG:${bytes.length}_bytes_exceeds_ecc_${eccLevel}_capacity`);

    const codewords = buildCodewords(bytes, version, level.index);
    const qr = createMatrix(version, eccLevel, codewords);
    return { ...qr, version, ecc: eccLevel };
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------

function toPathData(qr, margin) {
    // One <path> for every dark module. Horizontal runs are merged into a single
    // rect so the output stays small; `h<n> v1 h-<n> z` is the compact form.
    const parts = [];
    for (let y = 0; y < qr.size; y++) {
        let x = 0;
        while (x < qr.size) {
            if (!qr.modules[y][x]) {
                x++;
                continue;
            }
            let run = 0;
            while (x + run < qr.size && qr.modules[y][x + run]) run++;
            parts.push(`M${x + margin} ${y + margin}h${run}v1h-${run}z`);
            x += run;
        }
    }
    return parts.join('');
}

function toSvg(qr, opts) {
    const margin = opts.margin;
    const dimension = qr.size + margin * 2;
    const path = toPathData(qr, margin);
    const idAttr = opts.id ? ` id="${escapeXml(opts.id)}"` : '';
    const background =
        opts.bg && opts.bg !== 'none'
            ? `<rect width="${dimension}" height="${dimension}" fill="${escapeXml(opts.bg)}"/>`
            : '';
    return (
        `<svg${idAttr} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${dimension} ${dimension}" ` +
        `shape-rendering="crispEdges" role="img" aria-label="QR code">` +
        background +
        `<path fill="${escapeXml(opts.color)}" d="${path}"/>` +
        `</svg>`
    );
}

function escapeXml(value) {
    return String(value).replace(/[<>&"']/g, (c) => `&#${c.charCodeAt(0)};`);
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

const USAGE = `Usage: node make_qr.js --text <string> | --file <path> [options]

  --ecc <L|M|Q|H>   error correction level (default Q)
  --format <fmt>    svg | path | json          (default svg)
  --out <path>      write to a file instead of stdout
  --margin <n>      quiet zone in modules      (default 4)
  --color <css>     dark module colour         (default #000000)
  --bg <css>        background colour or none  (default none)
  --id <string>     id attribute on the <svg>`;

function parseArgs(argv) {
    const opts = {
        text: null,
        file: null,
        ecc: 'Q',
        format: 'svg',
        out: null,
        margin: 4,
        color: '#000000',
        bg: 'none',
        id: null,
    };
    for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (arg === '--help' || arg === '-h') {
            console.log(USAGE);
            process.exit(0);
        }
        const key = arg.replace(/^--/, '');
        if (!arg.startsWith('--') || !(key in opts)) {
            console.error(`ERROR:UNKNOWN_ARGUMENT:${arg}`);
            console.error(USAGE);
            process.exit(1);
        }
        const value = argv[++i];
        if (value === undefined) {
            console.error(`ERROR:MISSING_VALUE:${arg}`);
            process.exit(1);
        }
        opts[key] = key === 'margin' ? Number(value) : value;
    }
    return opts;
}

function main() {
    const opts = parseArgs(process.argv.slice(2));

    let text = opts.text;
    if (opts.file) {
        if (text !== null) {
            console.error('ERROR:TEXT_AND_FILE_ARE_MUTUALLY_EXCLUSIVE');
            process.exit(1);
        }
        text = fs.readFileSync(opts.file, 'utf8');
    }
    if (text === null || text === '') {
        console.error('ERROR:MISSING_TEXT');
        console.error(USAGE);
        process.exit(1);
    }
    if (!Number.isInteger(opts.margin) || opts.margin < 0) {
        console.error(`ERROR:INVALID_MARGIN:${opts.margin}`);
        process.exit(1);
    }

    const qr = encodeText(text, opts.ecc.toUpperCase());

    let output;
    if (opts.format === 'svg') {
        output = toSvg(qr, opts);
    } else if (opts.format === 'path') {
        output = toPathData(qr, opts.margin);
    } else if (opts.format === 'json') {
        output = JSON.stringify({
            version: qr.version,
            ecc: qr.ecc,
            size: qr.size,
            mask: qr.mask,
            modules: qr.modules.map((row) => row.map((cell) => (cell ? 1 : 0))),
        });
    } else {
        console.error(`ERROR:UNKNOWN_FORMAT:${opts.format}`);
        process.exit(1);
    }

    if (opts.out) {
        fs.writeFileSync(opts.out, output, 'utf8');
        console.log(`QR_WRITTEN:${opts.out}:v${qr.version}:${qr.ecc}:${qr.size}x${qr.size}`);
    } else {
        process.stdout.write(output);
    }
}

if (require.main === module) {
    try {
        main();
    } catch (error) {
        console.error(`ERROR:${error.message}`);
        process.exit(1);
    }
}

module.exports = { encodeText, toSvg, toPathData };
