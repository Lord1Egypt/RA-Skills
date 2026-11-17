// @ts-check

/**
 * Context injection hook for SPM v4.
 *
 * Registers a preToolUse hook that reads the current WBS ledger state and
 * injects it as a formatted markdown string into the tool-call context.
 * This gives every downstream tool handler visibility into what the SPM
 * engine is currently tracking — active task, last completed step, and
 * pending tasks — without requiring manual wiring.
 *
 * @module hooks/inject
 */

import { register, unregister } from './index.js';

/**
 * @typedef {Object} WBSState
 * @property {string}   ledgerPath   – Path to the WBS ledger file
 * @property {string}   [activeTask] – Currently active task name or ID
 * @property {string[]} [completed]  – List of completed task names/IDs
 * @property {string[]} [pending]    – List of pending task names/IDs
 */

/**
 * @typedef {Object} InjectConfig
 * @property {number}    [maxChars]  – Maximum characters of injected context (default 1500)
 * @property {() => WBSState} [reader] – Function that returns the current WBS state.
 *           Defaults to calling the WBS module's read function.
 */

/**
 * Default WBS reader that tries to load the WBS module at runtime.
 *
 * Falls back to a stub when the module is not available (e.g. before
 * initialisation).
 *
 * @returns {WBSState}
 */
/** @type {() => Promise<WBSState>} */
let cachedReader = async () => ({ ledgerPath: 'docs/spm/ledger.md' });

/**
 * Default WBS reader that dynamically imports the WBS module at runtime.
 *
 * Falls back to a stub when the module is not available (e.g. before
 * initialisation).
 *
 * @returns {Promise<WBSState>}
 */
async function defaultWBSReader() {
  try {
    const { WBS } = await import('../../wbs/index.js');
    const wbs =
      /** @type {any} */ (globalThis).__SPM_WBS ??
      new WBS({ ledgerPath: 'docs/spm/ledger.md' });
    const ledger = wbs.load ? wbs.load() : null;
    if (ledger) {
      return {
        ledgerPath: wbs.ledgerPath || 'docs/spm/ledger.md',
        activeTask: ledger.activeTask || undefined,
        completed: (ledger.tasks || [])
          .filter((/** @type {{ status: string }} */ t) => t.status === 'done')
          .map((/** @type {{ id: string }} */ t) => t.id),
        pending: (ledger.tasks || [])
          .filter((/** @type {{ status: string }} */ t) => t.status !== 'done')
          .map((/** @type {{ id: string }} */ t) => t.id),
      };
    }
  } catch {
    // WBS module not available yet — return empty state.
  }
  return { ledgerPath: 'docs/spm/ledger.md' };
}

/**
 * Format a WBS state object as a compact markdown snippet.
 *
 * @param {WBSState} state – Current WBS state
 * @param {number}   max   – Maximum character budget
 * @returns {string} Formatted markdown context string
 */
function formatWBSContext(state, max) {
  const lines = ['### SPM WBS Context'];
  lines.push(`**Ledger:** \`${state.ledgerPath}\``);

  if (state.activeTask) {
    lines.push(`**Active:** ${state.activeTask}`);
  }

  if (state.completed && state.completed.length > 0) {
    const completed = state.completed.slice(0, 5); // limit display
    lines.push(`**Completed (${state.completed.length}):**`);
    for (const t of completed) {
      lines.push(`- ✅ ${t}`);
    }
    if (state.completed.length > 5) {
      lines.push(`- … and ${state.completed.length - 5} more`);
    }
  }

  if (state.pending && state.pending.length > 0) {
    const pending = state.pending.slice(0, 5);
    lines.push(`**Pending (${state.pending.length}):**`);
    for (const t of pending) {
      lines.push(`- ${t}`);
    }
    if (state.pending.length > 5) {
      lines.push(`- … and ${state.pending.length - 5} more`);
    }
  }

  let output = lines.join('\n');

  // Trim to fit budget if needed.
  if (output.length > max) {
    output = output.slice(0, max - 3) + '…';
  }

  return output;
}

/**
 * Install the WBS context injection hook into the hook registry.
 *
 * The hook is registered under the name **"wbs-context-inject"** and
 * fires on **preToolUse**.  After calling this function, every tool call
 * that runs through the hook pipeline will receive a
 * `context.wbsContext` string.
 *
 * @param {InjectConfig} [config] – Configuration options
 */
export function install(config = {}) {
  const maxChars = config.maxChars ?? 1500;
  const reader = config.reader ?? defaultWBSReader;

  cachedReader = reader;

  register(
    'wbs-context-inject',
    /** @param {Object} ctx */
    async (ctx) => {
      const state = await cachedReader();
      ctx.wbsContext = formatWBSContext(state, maxChars);
    },
    'preToolUse',
  );
}

/**
 * Remove the WBS context injection hook from the registry.
 */
export function uninstall() {
  unregister('wbs-context-inject');
}