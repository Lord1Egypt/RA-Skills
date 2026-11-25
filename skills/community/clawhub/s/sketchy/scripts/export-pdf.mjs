#!/usr/bin/env node
// export-pdf.mjs: vector PDF of a deck (1920 x 1080 px pages) or a document (A4) through ?print.
import fs from 'node:fs';
import path from 'node:path';
import {
  parseArgs, say, die, rel, baseName, fmtBytes, requireHtmlFile, requirePlaywright, launchChromium,
  openPage, watchPage, waitReady, isDeckPage, slideCount, fileUrl, isMain,
} from './_lib.mjs';

const spec = {
  name: 'sketchy export-pdf', file: 'export-pdf.mjs', usage: '<deck-or-page.html> [-o file.pdf]',
  summary: 'vector PDF through ?print: 1920 x 1080 px pages for decks, A4 for documents.',
  details: [
    'Decks (main.sk-deck) get one page per slide at 1920 x 1080 px with backgrounds printed.',
    'Anything else is printed as an A4 document (a CSS @page size or margin in the file wins).',
    'Text stays text and fonts are embedded. The script counts the pages and warns when they',
    'do not match the slide count.',
  ],
  options: [
    { name: 'out', short: 'o', type: 'string', arg: 'file', help: 'output file (default: out/<name>.pdf next to the input)' },
    { name: 'grain', type: 'boolean', help: 'keep the SVG pencil-grain filters (Chromium turns them into pictures, a deck grows from about 3 MB to about 45 MB)' },
  ],
  positionals: { min: 1, max: 1, name: '<deck-or-page.html>' },
  examples: ['node export-pdf.mjs out/deck.html', 'node export-pdf.mjs report.html -o report.pdf'],
};

/** Count pages and embedded font files in a PDF without parsing it fully. */
function inspectPdf(file) {
  const text = fs.readFileSync(file).toString('latin1');
  const pages = (text.match(/\/Type\s*\/Page(?![s\w])/g) || []).length;
  const fontFiles = (text.match(/\/FontFile[23]?\b/g) || []).length;
  // Chromium draws variable fonts (Caveat) as Type3 vector glyphs with a ToUnicode map, so the text stays selectable
  const type3 = (text.match(/\/Subtype\s*\/Type3/g) || []).length;
  return { pages, fontFiles, type3 };
}

async function main() {
  const { values, positionals } = parseArgs(process.argv.slice(2), spec);
  const file = requireHtmlFile(positionals[0], 'html file');
  let out;
  if (values.out) out = path.resolve(values.out);
  else if (path.basename(path.dirname(file)) === 'out') out = path.join(path.dirname(file), `${baseName(file)}.pdf`);
  else out = path.join(path.dirname(file), 'out', `${baseName(file)}.pdf`);
  fs.mkdirSync(path.dirname(out), { recursive: true });

  const pw = requirePlaywright();
  const browser = await launchChromium(pw);
  const state = { errors: new Map(), failed: new Map(), external: new Map() };
  let isDeck = false, slides = 0, ready = true;
  try {
    const { context, page } = await openPage(browser, { width: 1920, height: 1080 });
    watchPage(page, state);
    await page.goto(fileUrl(file, 'print'), { waitUntil: 'load' });
    ready = await waitReady(page);
    isDeck = await isDeckPage(page);
    slides = isDeck ? await slideCount(page) : 0;
    // SVG filters (pencil grain) are rasterized by Chromium's PDF writer; without them the PDF stays vector and small
    if (!values.grain) await page.addStyleTag({ content: '*, *::before, *::after { filter: none !important; }' });
    if (isDeck && slides === 0) die('deck has no slides', 'add <section class="sk-slide"> elements inside main.sk-deck', 1);
    if (isDeck) {
      // a page break after the last slide makes Chromium add a blank trailing page
      await page.evaluate(() => {
        const all = document.querySelectorAll('main.sk-deck .sk-slide');
        const last = all[all.length - 1];
        if (last) { last.style.setProperty('break-after', 'auto', 'important'); last.style.setProperty('page-break-after', 'auto', 'important'); }
      });
      await page.pdf({ path: out, width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true, margin: { top: '0', right: '0', bottom: '0', left: '0' } });
    } else {
      const hasPageRule = await page.evaluate(() => {
        try { return [...document.styleSheets].some((s) => [...s.cssRules].some((r) => r.constructor.name === 'CSSPageRule')); } catch { return false; }
      });
      await page.pdf({
        path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
        ...(hasPageRule ? {} : { margin: { top: '14mm', right: '14mm', bottom: '14mm', left: '14mm' } }),
      });
    }
    await context.close();
  } finally {
    await browser.close();
  }

  const { pages, fontFiles, type3 } = inspectPdf(out);
  const size = fs.statSync(out).size;
  say.ok(`pdf  ${rel(out)}  ${pages} page${pages === 1 ? '' : 's'}${isDeck ? ' at 1920x1080 px' : ' (A4)'}, ${fmtBytes(size)}, fonts embedded: ${fontFiles} file${fontFiles === 1 ? '' : 's'} + ${type3} vector`);
  let problems = 0;
  if (!ready) say.warn('page was not ready after 15 s; the PDF may miss late content');
  if (isDeck && pages !== slides) {
    problems++;
    say.warn(`PDF has ${pages} pages, the deck has ${slides} slides`);
    say.fix('check the ?print layout: one .sk-slide per page, no extra break after the last slide');
  }
  if (fontFiles + type3 === 0) say.warn('no font files embedded (text may not look the same on other machines)');
  for (const [msg] of state.errors) say.warn(`console: ${msg}`);
  for (const [msg] of state.failed) say.warn(`request failed: ${msg}`);
  for (const [url] of state.external) say.warn(`external request: ${url}`);
  if (state.errors.size || state.failed.size || state.external.size) say.fix('run lint.mjs, fix the page, export again');
  if (problems) process.exit(1);
}

if (isMain(import.meta.url)) main().catch((e) => die(`export failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`, 'node doctor.mjs', 1));
