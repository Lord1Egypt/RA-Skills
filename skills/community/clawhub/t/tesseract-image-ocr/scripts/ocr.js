#!/usr/bin/env node
/**
 * Tesseract.js OCR runner — supports recognition, orientation detection,
 * region cropping, character whitelist, PSM/OEM, and output formats.
 *
 * Usage:
 *   node ocr.js <image> [options]
 *
 * Options:
 *   --lang <code>      Language code(s), "+"-separated (default: eng)
 *   --psm <n>          Page Segmentation Mode (0-13)
 *   --oem <n>          OCR Engine Mode (0-3)
 *   --whitelist <s>    Character whitelist (e.g. "0123456789")
 *   --rectangle <t,l,w,h>  Region to recognize
 *   --output <fmt>     Output format: text | hocr | blocks | tsv (default: text)
 *   --detect           Orientation & script detection (no OCR)
 *   --dpi <n>          Manual DPI override
 */

const { createWorker, PSM } = require('tesseract.js');

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    process.exit(0);
  }

  const opts = { image: args[0], lang: 'eng', output: 'text' };
  for (let i = 1; i < args.length; i++) {
    const val = args[i + 1];
    switch (args[i]) {
      case '--lang':     opts.lang = val; i++; break;
      case '--psm':      opts.psm = parseInt(val, 10); i++; break;
      case '--oem':      opts.oem = parseInt(val, 10); i++; break;
      case '--whitelist':opts.whitelist = val; i++; break;
      case '--rectangle':opts.rectangle = val; i++; break;
      case '--output':   opts.output = val; i++; break;
      case '--detect':   opts.detect = true; break;
      case '--dpi':      opts.dpi = parseInt(val, 10); i++; break;
      default:
        console.error(`Unknown option: ${args[i]}`);
        process.exit(1);
    }
  }
  return opts;
}

function printHelp() {
  console.error(`tesseract-ocr — Extract text from images

Usage: node ocr.js <image> [options]

Options:
  --lang <code>       Language codes, "+"-separated (default: eng)
                      e.g. --lang chi_sim+eng
  --psm <n>           Page Segmentation Mode (0-13, see PSM table)
  --oem <n>           OCR Engine Mode (0-3)
  --whitelist <s>     Only recognize these characters (e.g. "0123456789")
  --rectangle t,l,w,h Restrict OCR to this region
  --output <fmt>      Output format: text (default), hocr, blocks, tsv
  --detect            Orientation & script detection (no OCR)
  --dpi <n>           Manual DPI override
`);
}

async function main() {
  const opts = parseArgs();
  const langs = opts.lang.includes('+') ? opts.lang.split('+').join(',') : opts.lang;

  // Build createWorker options
  const workerOpts = { logger: m => console.error(`[tesseract] ${m.status}: ${Math.round(m.progress * 100)}%`) };
  if (opts.detect) {
    workerOpts.legacyCore = true;
    workerOpts.legacyLang = true;
  }

  const worker = await createWorker(langs, opts.oem, workerOpts);

  // Set PSM if specified
  if (opts.psm !== undefined) {
    await worker.setParameters({ tessedit_pageseg_mode: String(opts.psm) });
  }

  // Set character whitelist
  if (opts.whitelist) {
    await worker.setParameters({ tessedit_char_whitelist: opts.whitelist });
  }

  // Set manual DPI
  if (opts.dpi) {
    await worker.setParameters({ user_defined_dpi: String(opts.dpi) });
  }

  if (opts.detect) {
    // Orientation & Script Detection
    console.error(`[tesseract] Detecting orientation for: ${opts.image}`);
    const { data } = await worker.detect(opts.image);
    console.log(JSON.stringify(data, null, 2));
  } else {
    // OCR Recognition
    const recognizeOpts = {};
    if (opts.rectangle) {
      const [top, left, width, height] = opts.rectangle.split(',').map(Number);
      recognizeOpts.rectangle = { top, left, width, height };
    }

    const outputOpts = {};
    if (opts.output === 'text') {
      // text is enabled by default
    } else {
      outputOpts[opts.output] = true;
    }

    console.error(`[tesseract] Recognizing (lang=${langs}, psm=${opts.psm ?? 'default'}, output=${opts.output}): ${opts.image}`);
    const { data } = await worker.recognize(opts.image, recognizeOpts, outputOpts);

    if (opts.output === 'text') {
      console.log(data.text);
    } else {
      console.log(JSON.stringify(data, null, 2));
    }
  }

  await worker.terminate();
  console.error('[tesseract] Done.');
}

main().catch(err => {
  console.error('[tesseract] Error:', err.message);
  process.exit(1);
});
