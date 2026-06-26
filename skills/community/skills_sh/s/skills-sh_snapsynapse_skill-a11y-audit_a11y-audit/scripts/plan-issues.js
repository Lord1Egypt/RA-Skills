#!/usr/bin/env node
/*
skill_bundle: a11y-audit
file_role: script
version: 2
version_date: 2026-05-31
previous_version: 1
change_summary: Escapes target-derived Markdown fields and hardens issue dedupe comments.
*/

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function priorityForImpact(impact) {
  switch (impact) {
    case 'critical':
      return 'P0';
    case 'serious':
      return 'P1';
    case 'moderate':
      return 'P2';
    default:
      return 'P3';
  }
}

function thresholdAllows(priority, threshold) {
  const order = ['P0', 'P1', 'P2', 'P3'];
  return order.indexOf(priority) <= order.indexOf(threshold);
}

function routeFromUrl(url) {
  try {
    return new URL(url).pathname || '/';
  } catch {
    return url;
  }
}

function parseCsv(value) {
  if (!value) return [];
  return value.split(',').map((entry) => entry.trim()).filter(Boolean);
}

function parseProjectContext(content) {
  const data = {};
  let currentKey = null;

  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trimEnd();
    const keyMatch = line.match(/^- ([a-z0-9_]+):\s*(.*)$/i);
    if (keyMatch) {
      const [, key, value] = keyMatch;
      if (value === '') {
        data[key] = [];
        currentKey = key;
      } else {
        data[key] = value.trim();
        currentKey = null;
      }
      continue;
    }

    const itemMatch = line.match(/^\s*- (.+)$/);
    if (itemMatch && currentKey) {
      if (!Array.isArray(data[currentKey])) data[currentKey] = [];
      data[currentKey].push(itemMatch[1].trim());
    }
  }

  return data;
}

function principleLabelForWcag(wcagList, labels) {
  const principles = new Set();
  for (const sc of wcagList) {
    const major = String(sc).split('.')[0];
    if (major === '1') principles.add('wcag-perceivable');
    if (major === '2') principles.add('wcag-operable');
    if (major === '3') principles.add('wcag-understandable');
    if (major === '4') principles.add('wcag-robust');
  }
  return labels.filter((label) => principles.has(label));
}

function wcagFromTags(tags) {
  return [...new Set((tags || [])
    .map((tag) => {
      const match = tag.match(/^wcag(\d)(\d)(\d+)$/);
      if (!match) return null;
      return `${match[1]}.${match[2]}.${match[3]}`;
    })
    .filter(Boolean))];
}

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

function htmlCommentSafe(value) {
  return String(value ?? '')
    .replace(/--/g, '- -')
    .replace(/[<>]/g, '')
    .replace(/\r?\n/g, ' ')
    .trim();
}

const args = parseArgs(process.argv.slice(2));
const inputPath = path.resolve(args.input || '');
const outputPath = path.resolve(args.output || 'issue-plan.md');
const contextPath = args.context ? path.resolve(args.context) : null;
const context = contextPath && fs.existsSync(contextPath)
  ? parseProjectContext(fs.readFileSync(contextPath, 'utf8'))
  : {};
const threshold = args.threshold || context.issue_severity_threshold || 'P1';
const existingPath = args.existing ? path.resolve(args.existing) : null;
const existingKeys = existingPath && fs.existsSync(existingPath)
  ? new Set(JSON.parse(fs.readFileSync(existingPath, 'utf8')))
  : new Set();
const priorityLabels = parseCsv(context.issue_labels_priority);
const statusLabels = parseCsv(context.issue_labels_status);
const wcagLabels = parseCsv(context.issue_labels_wcag);
const additionalStandards = parseCsv(context.additional_standards);

if (!inputPath || !fs.existsSync(inputPath)) {
  console.error('Missing --input path to helper scan JSON');
  process.exit(1);
}

const input = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const byRule = new Map();

for (const result of input.results || []) {
  const route = routeFromUrl(result.url);
  const axe = result.axe || {};
  for (const violation of axe.violations || []) {
    const key = `${violation.id}::${route}`;
    const priority = priorityForImpact(violation.impact || 'minor');
    if (!thresholdAllows(priority, threshold)) continue;
    if (!byRule.has(key)) {
      const wcag = wcagFromTags(violation.tags || []);
      const labels = [];
      const priorityIndex = ['P0', 'P1', 'P2', 'P3'].indexOf(priority);
      if (priorityIndex >= 0 && priorityLabels[priorityIndex]) labels.push(priorityLabels[priorityIndex]);
      labels.push(...statusLabels);
      labels.push(...principleLabelForWcag(wcag, wcagLabels));
      byRule.set(key, {
        key,
        rule: violation.id,
        priority,
        impact: violation.impact || 'minor',
        route,
        help: violation.help,
        helpUrl: violation.helpUrl,
        instances: 0,
        wcag,
        labels,
        duplicate: existingKeys.has(key),
      });
    }
    byRule.get(key).instances += (violation.nodes || []).length;
  }
}

const issues = [...byRule.values()].sort((a, b) => a.key.localeCompare(b.key));
const planned = issues.filter((issue) => !issue.duplicate);
const duplicates = issues.filter((issue) => issue.duplicate);
const lines = [
  '# Accessibility Issue Plan',
  '',
  `Input: \`${inputPath}\``,
  `Threshold: \`${threshold}\``,
  contextPath ? `Context: \`${contextPath}\`` : 'Context: none',
  `Planned tickets: ${planned.length}`,
  `Skipped duplicates: ${duplicates.length}`,
  '',
  '| Status | Priority | Rule | Route | Instances | WCAG | Labels | Dedup Key | Summary |',
  '|---|---|---|---|---:|---|---|---|---|'
];

for (const issue of issues) {
  const dedupKey = `<!-- a11y-audit-key: ${htmlCommentSafe(issue.rule)}::${htmlCommentSafe(issue.route)} -->`;
  const status = issue.duplicate ? 'duplicate' : 'create';
  const wcag = issue.wcag.length > 0 ? issue.wcag.join(', ') : '-';
  const labels = issue.labels.length > 0 ? issue.labels.join(', ') : '-';
  lines.push(`| ${normalizeCell(status)} | ${normalizeCell(issue.priority)} | ${normalizeCell(issue.rule)} | ${normalizeCell(issue.route)} | ${issue.instances} | ${normalizeCell(wcag)} | ${normalizeCell(labels)} | \`${escapeInlineCode(dedupKey)}\` | ${normalizeCell(issue.help || 'Accessibility issue')} |`);
}

lines.push('');
if (additionalStandards.length > 0) {
  lines.push(`Additional standards: ${additionalStandards.map(normalizeCell).join(', ')}`);
  lines.push('');
}
lines.push('Use this plan for user review, label verification, standards mapping review, and deduplication checks before live ticket creation.');

fs.writeFileSync(outputPath, `${lines.join('\n')}\n`);
console.log(outputPath);
