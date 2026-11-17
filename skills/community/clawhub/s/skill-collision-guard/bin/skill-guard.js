#!/usr/bin/env node
'use strict';

const { analyzeCandidates, clusters, compareSkills, requiresInstallDecision } = require('../src/analyzer');
const { loadCandidate } = require('../src/candidate');
const { discoverSkills } = require('../src/discovery');
const { comparisonSummary, formatComparisons, formatInventory, skillSummary } = require('../src/report');
const { readSession, restore, suppress } = require('../src/state');

function usage() {
  return `skill-guard - detect conflicting coding-agent skills

Usage:
  skill-guard scan [--agent NAME] [--json] [--cwd DIR] [--home DIR]
  skill-guard check-install <path|github-url|owner/repo|plugin@marketplace> [--agent NAME] [--json]
  skill-guard compare <skill-or-plugin> <skill-or-plugin> [--json]
  skill-guard suppress <name-or-path>... --session ID [--json]
  skill-guard restore [name-or-path]... --session ID [--json]
  skill-guard status --session ID [--json]

check-install exits 2 when a critical/high conflict or behavioral overlay needs a decision.`;
}

function parseArgs(argv) {
  const options = { _: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--json') options.json = true;
    else if (['--cwd', '--home', '--session', '--agent'].includes(value)) options[value.slice(2)] = argv[++index];
    else options._.push(value);
  }
  return options;
}

function emit(value, json) {
  process.stdout.write(`${json ? JSON.stringify(value, null, 2) : value}\n`);
}

function inspectionOptions(options) {
  return {
    ...options,
    onRemoteInspection({ reference }) {
      process.stderr.write(
        `skill-guard: inspecting remote candidate '${reference}' with a temporary shallow Git clone; no candidate code will be executed.\n`,
      );
    },
  };
}

function needSession(options) {
  if (options.session) return options.session;
  process.stderr.write('Missing required --session ID.\n');
  process.exitCode = 64;
  return null;
}

function commandScan(options) {
  const skills = discoverSkills(options);
  const conflicts = clusters(skills);
  if (options.json) emit({ skills: skills.map(skillSummary), conflicts: conflicts.map(comparisonSummary) }, true);
  else emit(`${formatInventory(skills)}\n\n${formatComparisons(conflicts)}`, false);
}

function commandCheck(reference, options) {
  const candidate = loadCandidate(reference, inspectionOptions(options));
  try {
    const state = options.session ? readSession(options.session) : { suppressed: [] };
    const installed = discoverSkills(options);
    const conflicts = analyzeCandidates(candidate.skills, installed, { ignorePaths: state.suppressed });
    if (options.json) {
      emit({
        source: candidate.source,
        candidate: candidate.skills.map(skillSummary),
        conflicts: conflicts.map((item) => comparisonSummary(item, { sessionId: options.session, context: 'install' })),
      }, true);
    } else {
      emit(`Candidate: ${candidate.source}\n${formatComparisons(conflicts, { sessionId: options.session, context: 'install' })}`, false);
    }
    if (conflicts.some(requiresInstallDecision)) process.exitCode = 2;
  } finally {
    candidate.cleanup();
  }
}

function commandCompare(leftReference, rightReference, options) {
  const inspectOptions = inspectionOptions(options);
  let left;
  let right;
  try {
    left = loadCandidate(leftReference, inspectOptions);
    right = loadCandidate(rightReference, inspectOptions);
    const comparisons = [];
    for (const leftSkill of left.skills) for (const rightSkill of right.skills) comparisons.push(compareSkills(leftSkill, rightSkill));
    if (options.json) emit(comparisons.map(comparisonSummary), true);
    else emit(formatComparisons(comparisons.filter((item) => item.severity !== 'none')), false);
  } finally {
    if (left) left.cleanup();
    if (right) right.cleanup();
  }
}

function main(argv = process.argv.slice(2)) {
  const options = parseArgs(argv);
  const [command, ...values] = options._;
  try {
    if (!command || command === 'help' || command === '--help') return emit(usage(), false);
    if (command === 'scan') return commandScan(options);
    if (command === 'check-install' && values[0]) return commandCheck(values[0], options);
    if (command === 'compare' && values.length >= 2) return commandCompare(values[0], values[1], options);
    if (command === 'suppress') {
      const session = needSession(options);
      if (!session) return;
      if (!values.length) throw new Error('suppress requires at least one skill name or path');
      const value = suppress(session, values);
      return emit(options.json ? value : `Suppressed for session ${session}: ${value.suppressed.join(', ')}`, options.json);
    }
    if (command === 'restore') {
      const session = needSession(options);
      if (!session) return;
      const value = restore(session, values);
      return emit(options.json ? value : `Active suppressions for session ${session}: ${value.suppressed.join(', ') || '(none)'}`, options.json);
    }
    if (command === 'status') {
      const session = needSession(options);
      if (!session) return;
      const value = readSession(session);
      return emit(options.json ? value : `Suppressed for session ${session}: ${value.suppressed.join(', ') || '(none)'}`, options.json);
    }
    process.stderr.write(`${usage()}\n`);
    process.exitCode = 64;
  } catch (error) {
    if (options.json) emit({ error: error.message, code: error.code || 'ERROR' }, true);
    else process.stderr.write(`skill-guard: ${error.message}\n`);
    process.exitCode = 1;
  }
}

if (require.main === module) main();

module.exports = { inspectionOptions, main, parseArgs };
