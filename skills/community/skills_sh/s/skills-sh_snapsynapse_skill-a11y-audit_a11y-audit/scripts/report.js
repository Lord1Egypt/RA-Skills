#!/usr/bin/env node
/*
skill_bundle: a11y-audit
file_role: script
version: 2
version_date: 2026-05-31
previous_version: 1
change_summary: Escapes target-derived Markdown fields and discloses discovery origin policy.
*/

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) { args[key] = true; continue; }
    args[key] = next;
    i += 1;
  }
  return args;
}

// ---------------------------------------------------------------------------
// WCAG 2.1 AA Criteria (all 50 Level A + AA)
// ---------------------------------------------------------------------------

const WCAG_CRITERIA = [
  // Principle 1: Perceivable
  { sc: '1.1.1', name: 'Non-text Content', level: 'A', principle: 'Perceivable' },
  { sc: '1.2.1', name: 'Audio-only and Video-only (Prerecorded)', level: 'A', principle: 'Perceivable' },
  { sc: '1.2.2', name: 'Captions (Prerecorded)', level: 'A', principle: 'Perceivable' },
  { sc: '1.2.3', name: 'Audio Description or Media Alternative (Prerecorded)', level: 'A', principle: 'Perceivable' },
  { sc: '1.2.4', name: 'Captions (Live)', level: 'AA', principle: 'Perceivable' },
  { sc: '1.2.5', name: 'Audio Description (Prerecorded)', level: 'AA', principle: 'Perceivable' },
  { sc: '1.3.1', name: 'Info and Relationships', level: 'A', principle: 'Perceivable' },
  { sc: '1.3.2', name: 'Meaningful Sequence', level: 'A', principle: 'Perceivable' },
  { sc: '1.3.3', name: 'Sensory Characteristics', level: 'A', principle: 'Perceivable' },
  { sc: '1.3.4', name: 'Orientation', level: 'AA', principle: 'Perceivable' },
  { sc: '1.3.5', name: 'Identify Input Purpose', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.1', name: 'Use of Color', level: 'A', principle: 'Perceivable' },
  { sc: '1.4.2', name: 'Audio Control', level: 'A', principle: 'Perceivable' },
  { sc: '1.4.3', name: 'Contrast (Minimum)', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.4', name: 'Resize Text', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.5', name: 'Images of Text', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.10', name: 'Reflow', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.11', name: 'Non-text Contrast', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.12', name: 'Text Spacing', level: 'AA', principle: 'Perceivable' },
  { sc: '1.4.13', name: 'Content on Hover or Focus', level: 'AA', principle: 'Perceivable' },
  // Principle 2: Operable
  { sc: '2.1.1', name: 'Keyboard', level: 'A', principle: 'Operable' },
  { sc: '2.1.2', name: 'No Keyboard Trap', level: 'A', principle: 'Operable' },
  { sc: '2.1.4', name: 'Character Key Shortcuts', level: 'A', principle: 'Operable' },
  { sc: '2.2.1', name: 'Timing Adjustable', level: 'A', principle: 'Operable' },
  { sc: '2.2.2', name: 'Pause, Stop, Hide', level: 'A', principle: 'Operable' },
  { sc: '2.3.1', name: 'Three Flashes or Below Threshold', level: 'A', principle: 'Operable' },
  { sc: '2.4.1', name: 'Bypass Blocks', level: 'A', principle: 'Operable' },
  { sc: '2.4.2', name: 'Page Titled', level: 'A', principle: 'Operable' },
  { sc: '2.4.3', name: 'Focus Order', level: 'A', principle: 'Operable' },
  { sc: '2.4.4', name: 'Link Purpose (In Context)', level: 'A', principle: 'Operable' },
  { sc: '2.4.5', name: 'Multiple Ways', level: 'AA', principle: 'Operable' },
  { sc: '2.4.6', name: 'Headings and Labels', level: 'AA', principle: 'Operable' },
  { sc: '2.4.7', name: 'Focus Visible', level: 'AA', principle: 'Operable' },
  { sc: '2.5.1', name: 'Pointer Gestures', level: 'A', principle: 'Operable' },
  { sc: '2.5.2', name: 'Pointer Cancellation', level: 'A', principle: 'Operable' },
  { sc: '2.5.3', name: 'Label in Name', level: 'A', principle: 'Operable' },
  { sc: '2.5.4', name: 'Motion Actuation', level: 'A', principle: 'Operable' },
  // Principle 3: Understandable
  { sc: '3.1.1', name: 'Language of Page', level: 'A', principle: 'Understandable' },
  { sc: '3.1.2', name: 'Language of Parts', level: 'AA', principle: 'Understandable' },
  { sc: '3.2.1', name: 'On Focus', level: 'A', principle: 'Understandable' },
  { sc: '3.2.2', name: 'On Input', level: 'A', principle: 'Understandable' },
  { sc: '3.2.3', name: 'Consistent Navigation', level: 'AA', principle: 'Understandable' },
  { sc: '3.2.4', name: 'Consistent Identification', level: 'AA', principle: 'Understandable' },
  { sc: '3.3.1', name: 'Error Identification', level: 'A', principle: 'Understandable' },
  { sc: '3.3.2', name: 'Labels or Instructions', level: 'A', principle: 'Understandable' },
  { sc: '3.3.3', name: 'Error Suggestion', level: 'AA', principle: 'Understandable' },
  { sc: '3.3.4', name: 'Error Prevention (Legal, Financial, Data)', level: 'AA', principle: 'Understandable' },
  // Principle 4: Robust
  { sc: '4.1.1', name: 'Parsing', level: 'A', principle: 'Robust' },
  { sc: '4.1.2', name: 'Name, Role, Value', level: 'A', principle: 'Robust' },
  { sc: '4.1.3', name: 'Status Messages', level: 'AA', principle: 'Robust' },
];

// axe tag → WCAG SC mapping. Tags like "wcag111" map to "1.1.1".
function axeTagToSC(tag) {
  const m = tag.match(/^wcag(\d)(\d)(\d+)$/);
  if (!m) return null;
  return `${m[1]}.${m[2]}.${m[3]}`;
}

// ---------------------------------------------------------------------------
// Data aggregation
// ---------------------------------------------------------------------------

function aggregateScan(scanData) {
  const violationMap = new Map();   // ruleId → merged violation
  const passTags = new Set();
  const failTags = new Set();
  const inapplicableTags = new Set();
  const pageUrls = [];

  for (const result of scanData.results) {
    pageUrls.push(result.url);
    const axe = result.axe;

    // Violations — full detail, merge across pages
    for (const v of axe.violations || []) {
      if (!violationMap.has(v.id)) {
        violationMap.set(v.id, {
          rule: v.id,
          impact: v.impact,
          description: v.description,
          help: v.help,
          helpUrl: v.helpUrl,
          tags: v.tags || [],
          pages: [],
          nodes: [],
          instances: 0,
        });
      }
      const entry = violationMap.get(v.id);
      entry.pages.push(result.url);
      for (const n of v.nodes || []) {
        entry.nodes.push({ ...n, page: result.url });
        entry.instances += 1;
      }
      for (const t of v.tags || []) failTags.add(t);
    }

    // Passes — tags only
    for (const p of axe.passes || []) {
      for (const t of p.tags || []) passTags.add(t);
    }

    // Inapplicable — tags only
    for (const ia of axe.inapplicable || []) {
      for (const t of ia.tags || []) inapplicableTags.add(t);
    }
  }

  return { violationMap, passTags, failTags, inapplicableTags, pageUrls };
}

// ---------------------------------------------------------------------------
// Shared-template detection (pages with identical violation fingerprints)
// ---------------------------------------------------------------------------

function detectSharedTemplates(scanData, discoverData) {
  // Build per-page violation fingerprint: sorted rule IDs + impact
  const pageFingerprints = new Map();
  for (const result of scanData.results) {
    const rules = (result.axe.violations || [])
      .map((v) => `${v.id}:${v.impact}`)
      .sort();
    const fp = rules.length > 0 ? rules.join('|') : '__clean__';
    pageFingerprints.set(result.url, fp);
  }

  // Group pages by fingerprint
  const fpGroups = new Map();
  for (const [url, fp] of pageFingerprints) {
    if (!fpGroups.has(fp)) fpGroups.set(fp, []);
    fpGroups.get(fp).push(url);
  }

  // Cross-reference with discover groups to find template patterns sharing issues
  const sharedTemplates = [];
  if (discoverData) {
    // Build URL → template pattern lookup
    const urlToPattern = new Map();
    for (const g of discoverData.groups) {
      for (const url of g.selected) {
        urlToPattern.set(url, g.pattern);
      }
    }

    for (const [fp, urls] of fpGroups) {
      if (urls.length < 2) continue;
      const patterns = [...new Set(urls.map((u) => urlToPattern.get(u) || 'unknown'))];
      const rules = fp === '__clean__' ? [] : fp.split('|').map((r) => r.split(':')[0]);
      sharedTemplates.push({
        patterns,
        pages: urls,
        fingerprint: fp === '__clean__' ? 'no violations' : fp,
        rules,
      });
    }
  }

  return sharedTemplates;
}

// ---------------------------------------------------------------------------
// WCAG compliance matrix
// ---------------------------------------------------------------------------

function buildMatrix(passTags, failTags, inapplicableTags) {
  const matrix = {};
  for (const criterion of WCAG_CRITERIA) {
    const scTag = `wcag${criterion.sc.replace(/\./g, '')}`;
    if (failTags.has(scTag)) {
      matrix[criterion.sc] = 'fail';
    } else if (passTags.has(scTag)) {
      matrix[criterion.sc] = 'pass';
    } else if (inapplicableTags.has(scTag)) {
      matrix[criterion.sc] = 'not-applicable';
    } else {
      matrix[criterion.sc] = 'manual';
    }
  }
  return matrix;
}

// ---------------------------------------------------------------------------
// Color-contrast detail extraction
// ---------------------------------------------------------------------------

function extractContrastDetails(violationMap) {
  const cc = violationMap.get('color-contrast');
  if (!cc) return null;
  return cc.nodes.map((n) => {
    const data = n.any && n.any[0] && n.any[0].data;
    return {
      selector: (n.target || [])[0] || n.html,
      page: n.page,
      fgColor: data ? data.fgColor : null,
      bgColor: data ? data.bgColor : null,
      contrastRatio: data ? data.contrastRatio : null,
      expectedRatio: data ? data.expectedContrastRatio : null,
      fontSize: data ? data.fontSize : null,
      fontWeight: data ? data.fontWeight : null,
    };
  });
}

// ---------------------------------------------------------------------------
// Markdown safety
// ---------------------------------------------------------------------------

function normalizeCell(value) {
  return String(value ?? '')
    .replace(/\r?\n/g, ' ')
    .replace(/\|/g, '\\|')
    .replace(/`/g, '\\`')
    .trim();
}

function escapeInlineCode(value) {
  return String(value ?? '')
    .replace(/\r?\n/g, ' ')
    .replace(/`/g, '\\`')
    .replace(/\|/g, '\\|')
    .trim();
}

function escapeLinkLabel(value) {
  return normalizeCell(value).replace(/([\[\]])/g, '\\$1');
}

function safeMarkdownUrl(value) {
  try {
    const url = new URL(String(value));
    if (url.protocol === 'https:' || url.protocol === 'http:') return url.href;
  } catch { /* fall through */ }
  return null;
}

function pathnameOrDash(value) {
  try {
    return new URL(value).pathname || '/';
  } catch {
    return '-';
  }
}

// ---------------------------------------------------------------------------
// Impact summary
// ---------------------------------------------------------------------------

function buildSummary(violationMap) {
  const summary = { critical: 0, serious: 0, moderate: 0, minor: 0 };
  for (const v of violationMap.values()) {
    summary[v.impact] = (summary[v.impact] || 0) + v.instances;
  }
  return summary;
}

// ---------------------------------------------------------------------------
// JSON output (per output-schema.json)
// ---------------------------------------------------------------------------

function buildJson(opts) {
  const { date, projectName, pageUrls, violationMap, matrix, lighthouse, runtimeUrl, expectedUrl } = opts;
  const violations = [];
  for (const v of violationMap.values()) {
    const wcag = v.tags.map(axeTagToSC).filter(Boolean);
    violations.push({
      rule: v.rule,
      impact: v.impact,
      wcag: [...new Set(wcag)],
      pages: [...new Set(v.pages)],
      instances: v.instances,
    });
  }
  const json = {
    date,
    tool: `a11y-audit report.js v1`,
    pages: pageUrls,
    lighthouse: lighthouse || { status: 'skipped', reason: 'Not run by report.js' },
    summary: buildSummary(violationMap),
    violations,
    matrix,
  };
  if (expectedUrl) json.expected_url = expectedUrl;
  if (runtimeUrl) json.runtime_url = runtimeUrl;
  return json;
}

// ---------------------------------------------------------------------------
// Delta comparison
// ---------------------------------------------------------------------------

function computeDelta(currentViolationMap, previousJson) {
  if (!previousJson || !previousJson.violations) return null;

  const prevMap = new Map();
  for (const v of previousJson.violations) {
    prevMap.set(v.rule, {
      ...v,
      pages: [...new Set(v.pages || [])].sort(),
    });
  }

  const fixed = [];      // rules in previous but not current
  const newRules = [];   // rules in current but not previous
  const changed = [];    // rules in both but instance count changed
  const unchanged = [];  // same rule, same count

  const diffPages = (previousPages, currentPages) => {
    const previousSet = new Set(previousPages);
    const currentSet = new Set(currentPages);
    return {
      added: currentPages.filter((page) => !previousSet.has(page)),
      removed: previousPages.filter((page) => !currentSet.has(page)),
    };
  };

  for (const [rule, prev] of prevMap) {
    if (!currentViolationMap.has(rule)) {
      fixed.push({ rule, impact: prev.impact, previousInstances: prev.instances });
    }
  }

  for (const [rule, curr] of currentViolationMap) {
    const prev = prevMap.get(rule);
    const currentPages = [...new Set(curr.pages || [])].sort();
    if (!prev) {
      newRules.push({ rule, impact: curr.impact, instances: curr.instances, pages: currentPages });
    } else {
      const pageDelta = diffPages(prev.pages || [], currentPages);
      const pagesChanged = pageDelta.added.length > 0 || pageDelta.removed.length > 0;
      if (curr.instances !== prev.instances || pagesChanged) {
      changed.push({
        rule,
        impact: curr.impact,
        previousInstances: prev.instances,
        currentInstances: curr.instances,
        delta: curr.instances - prev.instances,
        previousPages: prev.pages || [],
        currentPages,
        addedPages: pageDelta.added,
        removedPages: pageDelta.removed,
      });
      } else {
        unchanged.push({ rule, impact: curr.impact, instances: curr.instances, pages: currentPages });
      }
    }
  }

  const prevTotal = previousJson.violations.reduce((sum, v) => sum + v.instances, 0);
  const currTotal = [...currentViolationMap.values()].reduce((sum, v) => sum + v.instances, 0);

  return {
    previousDate: previousJson.date,
    previousPages: previousJson.pages ? previousJson.pages.length : null,
    fixed,
    newRules,
    changed,
    unchanged,
    previousTotal: prevTotal,
    currentTotal: currTotal,
    netDelta: currTotal - prevTotal,
  };
}

// ---------------------------------------------------------------------------
// Remediation hints for common axe rules
// ---------------------------------------------------------------------------

const REMEDIATION_HINTS = {
  'landmark-one-main': 'Wrap the primary content area in a `<main>` element. This also resolves most `region` violations.',
  'region': 'Ensure all page content is inside a landmark region (`<main>`, `<nav>`, `<header>`, `<footer>`, or `role="..."`).',
  'color-contrast': 'Increase contrast ratio to ≥4.5:1 for normal text or ≥3:1 for large text. See Color Contrast Details below.',
  'dlitem': '`<dt>` and `<dd>` elements must be direct children of a `<dl>`. Wrap definition list items in `<dl>` or remove stray items.',
  'nested-interactive': 'Interactive elements (buttons, links) must not be nested inside other interactive elements. Flatten the hierarchy.',
  'image-alt': 'Add descriptive `alt` attributes to `<img>` elements. Use `alt=""` for purely decorative images.',
  'button-name': 'Buttons must have discernible text. Add visible text, `aria-label`, or `aria-labelledby`.',
  'link-name': 'Links must have discernible text. Add visible text content or `aria-label`.',
  'label': 'Form inputs must have associated labels via `<label for="...">`, `aria-label`, or `aria-labelledby`.',
  'html-has-lang': 'Add a `lang` attribute to the `<html>` element (e.g., `<html lang="en">`).',
  'document-title': 'Add a descriptive `<title>` element inside `<head>`.',
  'list': 'Ensure `<li>` elements are direct children of `<ul>` or `<ol>`. Do not place non-list content directly inside list containers.',
  'heading-order': 'Heading levels should increase by one (h1 → h2 → h3). Do not skip levels.',
  'aria-allowed-attr': 'Remove ARIA attributes that are not valid for the element\'s role.',
  'aria-required-attr': 'Add missing required ARIA attributes for the element\'s role.',
  'duplicate-id': 'Ensure all `id` attribute values are unique within the page.',
  'meta-viewport': 'Do not use `maximum-scale=1` or `user-scalable=no` in the viewport meta tag.',
  'tabindex': 'Avoid `tabindex` values greater than 0. Use `tabindex="0"` or `tabindex="-1"` only.',
};

// ---------------------------------------------------------------------------
// Markdown output (per output-contract.md section order)
// ---------------------------------------------------------------------------

function buildMarkdown(opts) {
  const { date, projectName, pageUrls, violationMap, matrix, summary, contrastDetails, lighthouse, runtimeUrl, expectedUrl, discoverData, sharedTemplates, delta } = opts;
  const lines = [];
  const ln = (s = '') => lines.push(s);

  // 1. Header
  ln('# Accessibility Audit Report');
  ln();
  ln('## Header');
  ln();
  ln('| Field | Value |');
  ln('|---|---|');
  ln(`| Project | ${normalizeCell(projectName)} |`);
  ln(`| Date | ${date} |`);
  ln(`| Standards | WCAG 2.1 AA |`);
  ln(`| Tool Version | axe-core (via scan.js); report.js v1 |`);
  if (runtimeUrl && expectedUrl && runtimeUrl !== expectedUrl) {
    ln(`| Runtime URL | ${normalizeCell(runtimeUrl)} (expected ${normalizeCell(expectedUrl)}) |`);
  }
  ln();

  // 2. Executive Summary
  ln('## Executive Summary');
  ln();
  const total = summary.critical + summary.serious + summary.moderate + summary.minor;
  const ruleCount = violationMap.size;
  ln(`${normalizeCell(projectName)} was audited across ${pageUrls.length} page(s). Automated scanning found **${total} issue instance(s)** across **${ruleCount} rule(s)**.`);
  ln();
  ln(`| Impact | Instances |`);
  ln('|---|---|');
  for (const level of ['critical', 'serious', 'moderate', 'minor']) {
    if (summary[level] > 0) ln(`| ${level} | ${summary[level]} |`);
  }
  ln();
  if (lighthouse && lighthouse.status === 'skipped') {
    ln(`Lighthouse was skipped: ${normalizeCell(lighthouse.reason)}.`);
    ln();
  }

  // 3. Automated Scan Results
  ln('## Automated Scan Results');
  ln();
  ln('### Pages Scanned');
  ln();
  for (const url of pageUrls) ln(`- ${normalizeCell(url)}`);
  ln();
  if (violationMap.size === 0) {
    ln('No automated violations found.');
    ln();
  } else {
    ln('### Findings by Rule');
    ln();
    ln('| Rule | Impact | Instances | Pages | WCAG |');
    ln('|---|---|---|---|---|');
    for (const v of violationMap.values()) {
      const wcag = v.tags.map(axeTagToSC).filter(Boolean);
      const wcagStr = [...new Set(wcag)].map((sc) => `SC ${sc}`).join(', ') || '-';
      const pageCount = new Set(v.pages).size;
      const label = escapeLinkLabel(v.rule);
      const href = safeMarkdownUrl(v.helpUrl);
      const ruleCell = href ? `[${label}](${href})` : label;
      ln(`| ${ruleCell} | ${normalizeCell(v.impact)} | ${v.instances} | ${pageCount} | ${normalizeCell(wcagStr)} |`);
    }
    ln();

    // Remediation hints for detected rules
    const hints = [...violationMap.values()]
      .filter((v) => REMEDIATION_HINTS[v.rule])
      .sort((a, b) => {
        const order = { critical: 0, serious: 1, moderate: 2, minor: 3 };
        return (order[a.impact] ?? 4) - (order[b.impact] ?? 4);
      });
    if (hints.length > 0) {
      ln('### Quick Fixes');
      ln();
      for (const v of hints) {
        ln(`- **${normalizeCell(v.rule)}** (${normalizeCell(v.impact)}, ${v.instances} instances): ${normalizeCell(REMEDIATION_HINTS[v.rule])}`);
      }
      ln();
    }
  }

  // Color-contrast detail
  if (contrastDetails && contrastDetails.length > 0) {
    ln('### Color Contrast Details');
    ln();
    ln('| Selector | Page | Ratio | Expected | FG | BG |');
    ln('|---|---|---|---|---|---|');
    for (const d of contrastDetails) {
      const ratio = d.contrastRatio ? d.contrastRatio.toFixed(2) : '-';
      const expected = d.expectedRatio ? `${d.expectedRatio}:1` : '-';
      const page = d.page ? pathnameOrDash(d.page) : '-';
      ln(`| \`${escapeInlineCode(d.selector)}\` | ${normalizeCell(page)} | ${normalizeCell(`${ratio}:1`)} | ${normalizeCell(expected)} | ${normalizeCell(d.fgColor || '-')} | ${normalizeCell(d.bgColor || '-')} |`);
    }
    ln();
  }

  // 4. WCAG 2.1 AA Compliance Matrix
  ln('## WCAG 2.1 AA Compliance Matrix');
  ln();
  ln('> This is an automation-assisted status view, not a conformance certification.');
  ln();
  let currentPrinciple = '';
  ln('| SC | Name | Level | Status |');
  ln('|---|---|---|---|');
  for (const c of WCAG_CRITERIA) {
    if (c.principle !== currentPrinciple) {
      currentPrinciple = c.principle;
      ln(`| **${c.principle}** | | | |`);
    }
    const status = matrix[c.sc] || 'manual';
    const icon = status === 'pass' ? 'Pass' : status === 'fail' ? '**Fail**' : status === 'not-applicable' ? 'N/A' : 'Manual';
    ln(`| SC ${c.sc} | ${c.name} | ${c.level} | ${icon} |`);
  }
  ln();

  // 5. Delta from Previous Audit
  if (delta) {
    ln('## Delta from Previous Audit');
    ln();
    ln(`Compared against audit from ${normalizeCell(delta.previousDate)}${delta.previousPages ? ` (${delta.previousPages} pages)` : ''}.`);
    ln();
    ln(`| Metric | Previous | Current | Change |`);
    ln('|---|---|---|---|');
    const sign = (n) => n > 0 ? `+${n}` : `${n}`;
    ln(`| Total instances | ${delta.previousTotal} | ${delta.currentTotal} | ${sign(delta.netDelta)} |`);
    ln();

    if (delta.fixed.length > 0) {
      ln('**Fixed** (no longer detected):');
      ln();
      for (const f of delta.fixed) {
        ln(`- ~~${normalizeCell(f.rule)}~~ (${normalizeCell(f.impact)}, was ${f.previousInstances} instances)`);
      }
      ln();
    }

    if (delta.newRules.length > 0) {
      ln('**New** (not in previous audit):');
      ln();
      for (const n of delta.newRules) {
        ln(`- **${normalizeCell(n.rule)}** (${normalizeCell(n.impact)}, ${n.instances} instances)`);
      }
      ln();
    }

    if (delta.changed.length > 0) {
      ln('**Changed**:');
      ln();
      for (const c of delta.changed) {
        const direction = c.delta > 0 ? '↑' : '↓';
        const pageNotes = [];
        if ((c.addedPages || []).length > 0) pageNotes.push(`added pages: ${c.addedPages.map(normalizeCell).join(', ')}`);
        if ((c.removedPages || []).length > 0) pageNotes.push(`removed pages: ${c.removedPages.map(normalizeCell).join(', ')}`);
        const pageSuffix = pageNotes.length > 0 ? `; ${pageNotes.join('; ')}` : '';
        ln(`- ${normalizeCell(c.rule)}: ${c.previousInstances} → ${c.currentInstances} (${direction}${Math.abs(c.delta)})${pageSuffix}`);
      }
      ln();
    }

    if (delta.unchanged.length > 0) {
      ln(`**Unchanged**: ${delta.unchanged.map((u) => normalizeCell(u.rule)).join(', ')}`);
      ln();
    }
  }

  // 6. Project-Specific Standard — placeholder
  // Omitted per output-contract.md: "Omit sections that are truly empty"

  // 7. Manual Testing Recommendations — placeholder for LLM
  ln('## Manual Testing Recommendations');
  ln();
  ln('<!-- report.js: This section should be populated by the auditing agent -->');
  ln('<!-- based on Phase 4 manual check guidance, which requires reasoning -->');
  ln('<!-- about the specific findings pattern. -->');
  ln();

  // 8. Remediation Priority
  ln('## Remediation Priority');
  ln();
  if (violationMap.size === 0) {
    ln('No violations to prioritize.');
  } else {
    ln('| Priority | Rule | Impact | Instances | WCAG |');
    ln('|---|---|---|---|---|');
    const sorted = [...violationMap.values()].sort((a, b) => {
      const order = { critical: 0, serious: 1, moderate: 2, minor: 3 };
      return (order[a.impact] ?? 4) - (order[b.impact] ?? 4);
    });
    sorted.forEach((v, i) => {
      const wcag = v.tags.map(axeTagToSC).filter(Boolean);
      const wcagStr = [...new Set(wcag)].map((sc) => `SC ${sc}`).join(', ') || '-';
      ln(`| P${Math.min(i, 3)} | ${normalizeCell(v.rule)} | ${normalizeCell(v.impact)} | ${v.instances} | ${normalizeCell(wcagStr)} |`);
    });
  }
  ln();

  // 9. Issues Created — placeholder
  ln('## Issues Created');
  ln();
  ln('Issue creation was not executed by the report generator.');
  ln();

  // 10. Methodology
  ln('## Methodology');
  ln();
  ln('| Field | Value |');
  ln('|---|---|');
  ln(`| Scan Date | ${date} |`);
  ln(`| Pages Scanned | ${pageUrls.length} |`);
  ln(`| Viewport | 1280 x 800 |`);
  ln(`| Browser | Headless Chromium (Puppeteer) |`);
  ln(`| Scanner | axe-core via scan.js |`);
  if (lighthouse && lighthouse.status === 'skipped') {
    ln(`| Lighthouse | Skipped: ${normalizeCell(lighthouse.reason)} |`);
  }
  if (runtimeUrl) ln(`| Runtime URL | ${normalizeCell(runtimeUrl)} |`);
  if (expectedUrl && runtimeUrl !== expectedUrl) ln(`| Expected URL | ${normalizeCell(expectedUrl)} |`);
  ln();

  // Sampling strategy (when discover.js was used)
  if (discoverData) {
    ln('### Sampling Strategy');
    ln();
    const originNote = discoverData.discoveredOrigins && discoverData.discoveredOrigins.length > 0
      ? ` Origins: ${discoverData.discoveredOrigins.map(normalizeCell).join(', ')}.`
      : '';
    ln(`Pages were selected via template-aware sampling (discover.js). ${discoverData.totalPages} total pages were classified into ${discoverData.groups.length} template groups; ${discoverData.selectedPages} representative pages were scanned.${originNote}`);
    ln();
    ln('| Template Group | Total Pages | Scanned | Selection |');
    ln('|---|---|---|---|');
    for (const g of discoverData.groups) {
      const entityLabel = g.entity && g.entity.count ? ` (${g.entity.count} ${g.entity.entityType})` : '';
      ln(`| \`${escapeInlineCode(g.pattern)}\`${normalizeCell(entityLabel)} | ${g.count} | ${g.selected.length} | ${normalizeCell(g.reason)} |`);
    }
    ln();
  }

  // Shared template detection
  if (sharedTemplates && sharedTemplates.length > 0) {
    ln('### Shared Template Patterns');
    ln();
    ln('Template groups with identical violation fingerprints share the same underlying issues. Fixing the shared template resolves the issue across all pages in those groups.');
    ln();
    for (const st of sharedTemplates) {
      const patternList = st.patterns.map((p) => `\`${escapeInlineCode(p)}\``).join(', ');
      if (st.fingerprint === 'no violations') {
        ln(`- **Clean:** ${patternList} — no violations detected`);
      } else {
        ln(`- **Shared issues on ${patternList}:** ${st.rules.map(normalizeCell).join(', ')}`);
      }
    }
    ln();
  }

  return lines.join('\n');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

function main() {
  const args = parseArgs(process.argv.slice(2));
  const inputPath = args.input;
  if (!inputPath) {
    console.error('Usage: report.js --input <scan.json> --output-dir <dir> [--project-name <name>] [--expected-url <url>] [--runtime-url <url>] [--discover <discover.json>] [--previous <prior-audit.json>]');
    process.exit(1);
  }

  const scanData = JSON.parse(fs.readFileSync(path.resolve(inputPath), 'utf8'));
  const outputDir = path.resolve(args['output-dir'] || process.cwd());
  const projectName = args['project-name'] || 'Project';
  const expectedUrl = args['expected-url'] || null;
  const runtimeUrl = args['runtime-url'] || null;
  const discoverPath = args.discover || null;
  const discoverData = discoverPath ? JSON.parse(fs.readFileSync(path.resolve(discoverPath), 'utf8')) : null;
  const previousPath = args.previous || null;
  const previousJson = previousPath ? JSON.parse(fs.readFileSync(path.resolve(previousPath), 'utf8')) : null;
  const date = new Date().toISOString().slice(0, 10);

  // Aggregate
  const { violationMap, passTags, failTags, inapplicableTags, pageUrls } = aggregateScan(scanData);
  const matrix = buildMatrix(passTags, failTags, inapplicableTags);
  const summary = buildSummary(violationMap);
  const contrastDetails = extractContrastDetails(violationMap);
  const lighthouse = scanData.results[0]?.lighthouse || { status: 'skipped', reason: 'Not available' };

  // Shared template detection
  const sharedTemplates = discoverData ? detectSharedTemplates(scanData, discoverData) : [];

  // Delta comparison
  const delta = previousJson ? computeDelta(violationMap, previousJson) : null;

  // Generate outputs
  const mdOpts = { date, projectName, pageUrls, violationMap, matrix, summary, contrastDetails, lighthouse, runtimeUrl, expectedUrl, discoverData, sharedTemplates, delta };
  const markdown = buildMarkdown(mdOpts);
  const json = buildJson({ date, projectName, pageUrls, violationMap, matrix, lighthouse, runtimeUrl, expectedUrl });
  if (discoverData) {
    json.sampling = {
      source: discoverData.source,
      originPolicy: discoverData.originPolicy || null,
      discoveredOrigins: discoverData.discoveredOrigins || [],
      blockedFetches: discoverData.blockedFetches || [],
      totalPages: discoverData.totalPages,
      selectedPages: discoverData.selectedPages,
      groups: discoverData.groups.map((g) => ({
        pattern: g.pattern,
        count: g.count,
        scanned: g.selected.length,
        entity: g.entity || null,
      })),
    };
  }
  if (sharedTemplates && sharedTemplates.length > 0) {
    json.sharedTemplates = sharedTemplates.map((st) => ({
      patterns: st.patterns,
      rules: st.rules,
      pageCount: st.pages.length,
    }));
  }
  if (delta) {
    json.delta = {
      previousDate: delta.previousDate,
      previousTotal: delta.previousTotal,
      currentTotal: delta.currentTotal,
      netDelta: delta.netDelta,
      fixed: delta.fixed.map((f) => f.rule),
      newRules: delta.newRules.map((n) => n.rule),
      changed: delta.changed.map((c) => ({
        rule: c.rule,
        delta: c.delta,
        previousPages: c.previousPages,
        currentPages: c.currentPages,
        addedPages: c.addedPages,
        removedPages: c.removedPages,
      })),
    };
  }

  // Write files
  fs.mkdirSync(outputDir, { recursive: true });
  const mdPath = path.join(outputDir, `audit-${date}.md`);
  const jsonPath = path.join(outputDir, `audit-${date}.json`);
  fs.writeFileSync(mdPath, markdown);
  fs.writeFileSync(jsonPath, JSON.stringify(json, null, 2));

  console.log(mdPath);
  console.log(jsonPath);
}

main();
