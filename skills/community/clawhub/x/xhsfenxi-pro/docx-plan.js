#!/usr/bin/env node
/**
 * xhsfenxi — docx-plan.js
 * Purpose: Print the Word generation plan for a completed Xiaohongshu analysis,
 *          including which build_docx*.py script to use, the full workflow steps,
 *          and TOC fix guidance from the workflow archive.
 * Usage:
 *   node scripts/docx-plan.js <creator-name>
 *   node scripts/docx-plan.js <creator-name> --mode comparison
 *   node scripts/docx-plan.js --toc-fix
 */

const ARCHIVE_BASE = '~/Desktop/cosmocloud/Deeplumen/cosmowork/openclaw_cosmo/afa/小红书分析与工作流归档/02-Word生成与目录修复脚本';

const args = process.argv.slice(2);
const tocFix = args.includes('--toc-fix');
const modeIdx = args.indexOf('--mode');
const mode = modeIdx !== -1 ? args[modeIdx + 1] : 'single';
const name = args.filter((a, i) => {
  if (a.startsWith('--')) return false;
  if (modeIdx !== -1 && i === modeIdx + 1) return false;
  return true;
})[0];

if (tocFix) {
  console.log(`
=== xhsfenxi Word TOC Fix Guide ===

Archive scripts location:
  ${ARCHIVE_BASE}/

STEP-BY-STEP FIX PROCESS

1. Run inspect_docx.py to diagnose the issue:
   python3 ${ARCHIVE_BASE}/inspect_docx.py <your-file.docx>
   → Check: bookmark names, link types, heading structure

2. Verify the following are correct:
   - Bookmark names follow format: _TocH1_XXX  (NOT #_TocH1_XXX)
   - Internal TOC links use Word-native anchor, NOT external http:// rels
   - No duplicate headings accidentally inserted in document body
   - Namespace attributes written as: elem.set('{' + W_NS + '}id', value)

3. Run the appropriate fix script:
   - For attribute/namespace errors:  python3 fix_attrs.py <file.docx>
   - For final TOC + heading cleanup:  python3 fix_final2.py <file.docx>
   - For known wrong output patterns:  python3 fix_wrong.py <file.docx>

4. Verify with check_it.py:
   python3 ${ARCHIVE_BASE}/check_it.py <your-fixed-file.docx>

5. Open in Word and test: click each TOC entry to confirm internal jump works.

COMMON ERROR TABLE
  Bookmark format wrong     → rename using fix_attrs.py
  anchor contains #         → strip # prefix in fix_final2.py
  TOC uses external rels    → switch to w:instr field or Word anchor
  Duplicate headings        → fix_wrong.py
  XML namespace error       → use full namespace URI in elem.set()
`);
  process.exit(0);
}

if (!name && !tocFix) {
  console.error('Usage: node scripts/docx-plan.js <creator-name> [--mode comparison]');
  console.error('       node scripts/docx-plan.js --toc-fix');
  process.exit(1);
}

const isComparison = mode === 'comparison';
const mdFile = isComparison
  ? `选题公式学习-综合版.md`
  : `${name}-结构化总结报告.md`;
const docxFile = isComparison
  ? `选题公式学习-综合版.docx`
  : `${name}-结构化总结报告-商业版.docx`;

console.log(`
=== xhsfenxi Word generation plan: ${name || 'comparison'} ===

Mode: ${isComparison ? 'comparison / 综合版' : 'single creator'}

─────────────────────────────────────────────
STEP 1 — Confirm Markdown is complete
─────────────────────────────────────────────
Make sure this file is finalized:
  ${mdFile}

─────────────────────────────────────────────
STEP 2 — Run build_docx6.py (recommended)
─────────────────────────────────────────────
Primary script (most stable):
  python3 ${ARCHIVE_BASE}/build_docx6.py ${mdFile} ${docxFile}

If build_docx6.py fails, fall back to earlier versions:
  build_docx5.py → build_docx4.py → build_docx3.py

─────────────────────────────────────────────
STEP 3 — Inspect the output
─────────────────────────────────────────────
  python3 ${ARCHIVE_BASE}/inspect_docx.py ${docxFile}

Check for:
  ✓ Headings have _TocH1_XXX bookmarks
  ✓ TOC links are internal (not external URL rels)
  ✓ No duplicate heading text in body
  ✓ Page count and section structure look correct

─────────────────────────────────────────────
STEP 4 — Fix if needed
─────────────────────────────────────────────
Run: node scripts/docx-plan.js --toc-fix
for the full TOC fix checklist.

Most common fix:
  python3 ${ARCHIVE_BASE}/fix_final2.py ${docxFile}

─────────────────────────────────────────────
STEP 5 — Final check
─────────────────────────────────────────────
  python3 ${ARCHIVE_BASE}/check_it.py ${docxFile}
  → Open in Word, click TOC entries, verify internal jumps work

─────────────────────────────────────────────
EXPECTED OUTPUT FILES
─────────────────────────────────────────────
  ${docxFile}
${isComparison ? '' : `  ${name}-结构化总结报告.md (keep as source of truth)\n  ${name}-爆款选题公式.md (if also produced)`}
─────────────────────────────────────────────
ARCHIVE LOCATION
─────────────────────────────────────────────
Scripts: ${ARCHIVE_BASE}/
Stable production script: build_docx6.py
Inspection tool: inspect_docx.py
`);
