/**
 * Tool gating predicate for 3.2.0 — the `before_tool_call` hook in index.ts
 * delegates to this module so the logic is testable without standing up a
 * full OpenClaw plugin host.
 *
 * Scope: the 3.2.0 state machine has two states (`fresh`, `active`). Memory
 * tools are blocked when state is anything other than `active`. Billing +
 * setup-adjacent tools remain usable — users need to be able to upgrade,
 * migrate, and start onboarding before their vault is active.
 *
 * This module imports ONLY types + the state resolver. No I/O beyond what
 * `resolveOnboardingState` already does; no network; no env reads.
 */

import type { OnboardingState } from './fs-helpers.js';

/**
 * Tool names gated on `state=active`. Keep in sync with the actual
 * `registerTool` calls in `index.ts`. Anything NOT in this set is always
 * callable (e.g. totalreclaw_upgrade, totalreclaw_migrate,
 * totalreclaw_onboarding_start, totalreclaw_setup).
 */
export const GATED_TOOL_NAMES: readonly string[] = Object.freeze([
  'totalreclaw_remember',
  'totalreclaw_recall',
  'totalreclaw_forget',
  'totalreclaw_export',
  'totalreclaw_status',
  'totalreclaw_consolidate',
  'totalreclaw_pin',
  'totalreclaw_unpin',
  'totalreclaw_retype',
  'totalreclaw_set_scope',
  'totalreclaw_import_from',
  'totalreclaw_import_batch',
]);

export interface GateDecision {
  /** True when the tool call must be blocked. */
  block: boolean;
  /** Non-secret message surfaced to the LLM when `block === true`. */
  blockReason?: string;
}

/**
 * Decide whether a specific tool call should be blocked given the current
 * onboarding state. Does not read any files — caller resolves state first
 * (that lets tests stub state without touching disk).
 */
export function decideToolGate(
  toolName: string | undefined,
  state: OnboardingState | null | undefined,
): GateDecision {
  if (!toolName) return { block: false };
  if (!GATED_TOOL_NAMES.includes(toolName)) return { block: false };
  if (state?.onboardingState === 'active') return { block: false };
  return {
    block: true,
    blockReason:
      'TotalReclaw onboarding required. Run `openclaw totalreclaw onboard` ' +
      'in a terminal (or call the `totalreclaw_onboarding_start` tool for ' +
      'details). Memory tools are gated until the user completes setup.',
  };
}

/**
 * Convenience predicate — useful for tests + documentation.
 */
export function isGatedToolName(toolName: string): boolean {
  return GATED_TOOL_NAMES.includes(toolName);
}
