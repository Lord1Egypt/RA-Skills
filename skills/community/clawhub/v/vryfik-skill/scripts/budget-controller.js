#!/usr/bin/env node
'use strict';

/**
 * Token Budget Controller — Stateless budget calculator
 *
 * ClawHub Security: NO network access. NO file system access.
 * Caller passes current state; script returns updated state.
 * Pure synchronous computation.
 *
 * Commands:
 *   node scripts/budget-controller.js init [totalBudget]
 *   node scripts/budget-controller.js check  '{"state":{...},"component":"l1_grep","amount":50}'
 *   node scripts/budget-controller.js consume '{"state":{...},"component":"l1_grep","amount":50}'
 *   node scripts/budget-controller.js report  '{"state":{...}}'
 */

// ---------------------------------------------------------------------------
// Default limits per component (tokens)
// ---------------------------------------------------------------------------
const DEFAULT_LIMITS = {
  intent_parse:   50,
  cache_check:    20,
  query_rewrite:  30,
  l1_grep:       100,
  l2_fragment:   400,
  l3_web:       1500,
  credibility:   300,
  assembly:      500
};

const DEFAULT_TOTAL = 4000;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function sumConsumed(consumed) {
  return Object.values(consumed).reduce((s, v) => s + v, 0);
}

function initState(total = DEFAULT_TOTAL) {
  return {
    total: Number(total) || DEFAULT_TOTAL,
    limits: { ...DEFAULT_LIMITS },
    consumed: {},
    remaining: Number(total) || DEFAULT_TOTAL
  };
}

function checkBudget(state, component, amount) {
  if (!state || typeof state !== 'object') return { allowed: false, reason: 'Invalid state' };
  const limit   = state.limits?.[component];
  const already = state.consumed?.[component] || 0;
  const globalRemaining = state.total - sumConsumed(state.consumed || {});

  if (limit !== undefined && already + amount > limit) {
    return { allowed: false, reason: `Component limit exceeded (${already}+${amount} > ${limit})` };
  }
  if (globalRemaining < amount) {
    return { allowed: false, reason: `Global budget exhausted (need ${amount}, have ${globalRemaining})` };
  }
  return { allowed: true, globalRemaining: globalRemaining - amount };
}

function consumeBudget(state, component, amount) {
  const check = checkBudget(state, component, amount);
  if (!check.allowed) return { error: check.reason, state };

  const newConsumed = {
    ...state.consumed,
    [component]: (state.consumed[component] || 0) + amount
  };
  const totalConsumed = sumConsumed(newConsumed);

  return {
    state: {
      ...state,
      consumed: newConsumed,
      remaining: state.total - totalConsumed
    }
  };
}

function reportBudget(state) {
  const totalConsumed = sumConsumed(state.consumed || {});
  const breakdown = {};
  for (const [comp, limit] of Object.entries(state.limits || DEFAULT_LIMITS)) {
    breakdown[comp] = {
      limit,
      consumed: state.consumed?.[comp] || 0,
      remaining: limit - (state.consumed?.[comp] || 0)
    };
  }
  return {
    total: state.total,
    totalConsumed,
    totalRemaining: state.total - totalConsumed,
    utilizationPct: +((totalConsumed / state.total) * 100).toFixed(1),
    breakdown
  };
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------
function main() {
  const cmd = process.argv[2];
  const arg = process.argv[3];

  if (cmd === 'init') {
    console.log(JSON.stringify({ state: initState(arg) }));
    return;
  }

  if (!arg) {
    console.error('Usage: node scripts/budget-controller.js <init|check|consume|report> [json]');
    process.exit(1);
  }

  let input;
  try {
    input = JSON.parse(arg);
  } catch {
    console.log(JSON.stringify({ error: 'Invalid JSON input' }));
    process.exit(1);
  }

  switch (cmd) {
    case 'check':
      console.log(JSON.stringify(checkBudget(input.state, input.component, input.amount)));
      break;
    case 'consume':
      console.log(JSON.stringify(consumeBudget(input.state, input.component, input.amount)));
      break;
    case 'report':
      console.log(JSON.stringify(reportBudget(input.state)));
      break;
    default:
      console.log(JSON.stringify({ error: `Unknown command: ${cmd}` }));
      process.exit(1);
  }
}

main();
