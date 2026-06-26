/**
 * Tests for rc.5 pair-qr encoders.
 *
 * Covers:
 *   - encodePng emits a valid PNG (magic header bytes).
 *   - encodeUnicode emits a non-empty block-character string.
 *   - Oversized, empty, and non-string inputs throw `QREncodeError`.
 *   - The default ECC level produces QRs of a predictable size band for
 *     a ~110-char URL (regression guard — if the library silently
 *     changes defaults, we want to see it).
 *
 * Run with: `npx tsx pair-qr.test.ts`
 */

import { encodePng, encodeUnicode, QREncodeError } from './pair-qr.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) { console.log(`ok ${n} - ${name}`); passed++; }
  else { console.log(`not ok ${n} - ${name}`); failed++; }
}

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const SAMPLE_URL =
  'http://127.0.0.1:47321/pair/' +
  'abc123def456abc123def456abc123de' +
  '#pk=Nq7v3pQ8kL_wY1rZ-aXmPqT9yCvB6jH2kLgFeRzK';

// ---------------------------------------------------------------------------
// PNG emits valid header
// ---------------------------------------------------------------------------
{
  const png = await encodePng(SAMPLE_URL);
  assert(png.length > 500, `png: non-trivial size (${png.length} bytes)`);
  assert(png.length < 20_000, `png: within sanity cap (${png.length} bytes)`);
  assert(
    Buffer.compare(png.subarray(0, 8), PNG_MAGIC) === 0,
    `png: starts with PNG magic (got ${png.subarray(0, 8).toString('hex')})`,
  );
}

// ---------------------------------------------------------------------------
// PNG respects scale option
// ---------------------------------------------------------------------------
{
  const small = await encodePng(SAMPLE_URL, { boxSize: 4, border: 2 });
  const big = await encodePng(SAMPLE_URL, { boxSize: 12, border: 4 });
  assert(big.length > small.length, `png: bigger scale → larger PNG (${small.length} < ${big.length})`);
}

// ---------------------------------------------------------------------------
// Unicode emits block chars
// ---------------------------------------------------------------------------
{
  const uni = await encodeUnicode(SAMPLE_URL);
  assert(uni.length > 0, 'unicode: non-empty');
  const hasBlock = /[█▀▄]/.test(uni);
  assert(hasBlock, `unicode: contains block glyphs (first 80 chars: ${JSON.stringify(uni.slice(0, 80))})`);
  const lineCount = uni.split('\n').length;
  assert(lineCount >= 10, `unicode: multi-line (${lineCount} lines)`);
  assert(uni.length < 5000, `unicode: within sanity cap (${uni.length} chars)`);
}

// ---------------------------------------------------------------------------
// Oversized input rejected
// ---------------------------------------------------------------------------
{
  const oversized = 'http://x/' + 'a'.repeat(2050);
  let thrownPng: unknown = null;
  try { await encodePng(oversized); } catch (err) { thrownPng = err; }
  assert(
    thrownPng instanceof QREncodeError && /too large/.test((thrownPng as Error).message),
    'png: rejects oversized URL with QREncodeError',
  );

  let thrownUni: unknown = null;
  try { await encodeUnicode(oversized); } catch (err) { thrownUni = err; }
  assert(
    thrownUni instanceof QREncodeError && /too large/.test((thrownUni as Error).message),
    'unicode: rejects oversized URL with QREncodeError',
  );
}

// ---------------------------------------------------------------------------
// Empty / non-string rejected
// ---------------------------------------------------------------------------
{
  let thrown: unknown = null;
  try { await encodePng(''); } catch (err) { thrown = err; }
  assert(thrown instanceof QREncodeError, 'png: rejects empty string');

  thrown = null;
  try { await encodeUnicode(''); } catch (err) { thrown = err; }
  assert(thrown instanceof QREncodeError, 'unicode: rejects empty string');

  thrown = null;
  try { await encodePng(null as unknown as string); } catch (err) { thrown = err; }
  assert(
    thrown instanceof QREncodeError && /must be a string/.test((thrown as Error).message),
    'png: rejects null',
  );

  thrown = null;
  try { await encodeUnicode(12345 as unknown as string); } catch (err) { thrown = err; }
  assert(
    thrown instanceof QREncodeError && /must be a string/.test((thrown as Error).message),
    'unicode: rejects number',
  );
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------
console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
