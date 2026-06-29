#!/usr/bin/env node
/**
 * build-report — inject a report payload into the HTML template.
 *
 * Exists so the agent never has to read or write HTML: it writes a small JSON
 * payload, runs this, and the report is built. Dependency-free (Node 18+).
 *
 * Usage: node build-report.mjs --data <payload.json> --out <slop-report.html> [--template <path>]
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const argv = process.argv.slice(2);
const flag = (name, fallback) => {
    const i = argv.indexOf('--' + name);
    return i !== -1 ? argv[i + 1] : fallback;
};
const here = dirname(fileURLToPath(import.meta.url));
const dataPath = flag('data');
const outPath = resolve(flag('out', 'slop-report.html'));
const templatePath = resolve(flag('template', join(here, '..', 'assets', 'report-template.html')));
if (!dataPath || !existsSync(dataPath)) {
    console.error('build-report: --data <payload.json> is required and must exist');
    process.exit(1);
}
if (!existsSync(templatePath)) {
    console.error(`build-report: template not found: ${templatePath}`);
    process.exit(1);
}
let payload;
try {
    payload = JSON.parse(readFileSync(resolve(dataPath), 'utf8'));
}
catch (e) {
    console.error(`build-report: payload is not valid JSON: ${e.message}`);
    process.exit(1);
}
// Validate just enough to keep a broken report from reaching the user.
const problems = [];
const need = (cond, msg) => { if (!cond)
    problems.push(msg); };
need(payload.project?.name, 'project.name missing');
need(typeof payload.slopPercent === 'number' && Number.isFinite(payload.slopPercent) && payload.slopPercent >= 0 && payload.slopPercent <= 100, 'slopPercent must be a number 0-100');
need(payload.tier?.name && payload.tier?.blurb, 'tier.name / tier.blurb missing');
need(typeof payload.verdict === 'string' && payload.verdict.length > 20, 'verdict missing or too short');
need(typeof payload.fastestClimb === 'string' && payload.fastestClimb.length > 10, 'fastestClimb missing');
need(Array.isArray(payload.categories) && payload.categories.length >= 5, 'categories must list all scored categories');
need(Array.isArray(payload.findings), 'findings must be an array');
need(Array.isArray(payload.fixItPrompts) && payload.fixItPrompts.length >= 1, 'fixItPrompts must have at least one entry');
const weightSum = (payload.categories ?? []).reduce((s, c) => s + (c.weight ?? 0), 0);
need(weightSum === 0 || weightSum === 100, `category weights sum to ${weightSum}, expected 100`);
for (const f of payload.findings ?? []) {
    need(f.file, `finding "${(f.description ?? '').slice(0, 40)}" has no file`);
    need(['minor', 'moderate', 'major'].includes(f.severity), `finding at ${f.file} has invalid severity "${f.severity}"`);
}
if (problems.length) {
    console.error('build-report: payload rejected:\n  - ' + problems.join('\n  - '));
    process.exit(1);
}
const template = readFileSync(templatePath, 'utf8');
// Anchor on the real `const DATA =` assignment so the markers can never be confused
// with any other occurrence (e.g. prose in a comment). The capture group preserves
// the anchor text.
const ANCHOR = /(const DATA = )\/\*SLOP_DATA\*\/[\s\S]*?\/\*END_SLOP_DATA\*\//;
if (!ANCHOR.test(template)) {
    console.error('build-report: could not find the `const DATA = /*SLOP_DATA*/ ... /*END_SLOP_DATA*/` block in the template');
    process.exit(1);
}
const out = template.replace(ANCHOR, '$1/*SLOP_DATA*/' + JSON.stringify(payload, null, 2) + '/*END_SLOP_DATA*/');
// Verify the payload actually landed in const DATA — never trust the replace blindly.
// (A silent mis-injection here is exactly the bug that shipped a blank report once.)
const landed = out.match(/const DATA = \/\*SLOP_DATA\*\/([\s\S]*?)\/\*END_SLOP_DATA\*\//);
let injected = null;
try {
    injected = JSON.parse(landed[1]);
}
catch { /* handled below */ }
if (!injected || injected.slopPercent !== payload.slopPercent || injected.tier?.name !== payload.tier?.name) {
    console.error('build-report: injection verification FAILED — the report would render template defaults. Not writing.');
    process.exit(1);
}
writeFileSync(outPath, out);
console.log(`build-report: wrote ${outPath} (${payload.slopPercent}% slop — ${payload.tier?.name})`);
console.log('build-report: verified the live report renders this payload (not template defaults).');
