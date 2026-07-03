/**
 * Tool gating predicate — the `before_tool_call` hook in index.ts delegates
 * to this module so the logic is testable without standing up a full
 * OpenClaw plugin host.
 *
 * Scope (Phase 3.3 — OpenClaw native integration): the agent-facing memory
 * tools are now the bundled NATIVE tools `memory_search` / `memory_get`
 * (registered via the MemoryPluginCapability in index.ts). The legacy
 * `totalreclaw_*` agent tools were retired in Task 3.2. This gate now
 * blocks the NATIVE memory tools until onboarding state is `active`, so
 * that an unpaired agent receives an actionable non-secret pointer to the
 * CLI pair surface instead of silently seeing "no memories found" from the
 * adapter's fail-soft empty-result path.
 *
 * Why gate the natives rather than rely on adapter fail-soft:
 *   - The adapter's `recall()` closure returns `[]` when `needsSetup`, which
 *     surfaces to the agent as "no memories matched" — indistinguishable
 *     from an empty vault. The gate intercepts BEFORE the tool runs and
 *     returns a blockReason telling the agent exactly how to onboard
 *     (`tr pair --url-pin`). Without the gate, a fresh user asking the
 *     agent "what do you remember about me?" gets a confident "nothing"
 *     with no path forward.
 *
 * State machine: `fresh` → `active`. Memory tools are blocked unless state
 * is `active`. The pair surface itself (`tr pair`, the `/pair/start` HTTP
 * route) is NOT gated — users must be able to start onboarding before
 * their vault is active.
 *
 * This module imports ONLY types + the state resolver. No I/O beyond what
 * `resolveOnboardingState` already does; no network; no env reads.
 */

import type { OnboardingState } from './fs-helpers.js';

/**
 * Tool names gated on `state=active`. These are the bundled NATIVE memory
 * tools the agent sees after the Phase 2 MemoryPluginCapability registration.
 * Anything NOT in this set is always callable.
 *
 * Keep in sync with the `registerNativeMemory` registration in `index.ts`
 * (the two `api.registerTool` calls with `names: ['memory_search']` and
 * `names: ['memory_get']`).
 */
export const GATED_TOOL_NAMES: readonly string[] = Object.freeze([
  'memory_search',
  'memory_get',
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
      'TotalReclaw setup pending — memory_search/memory_get are disabled until the user pairs. ' +
      'Tell the user to run `tr pair --url-pin` on the gateway host and open the returned URL ' +
      'in a browser (the recovery phrase is generated and encrypted in-browser; it never enters ' +
      'this chat). Once paired, memory tools unlock automatically. Do NOT attempt to generate, ' +
      'display, or relay a recovery phrase yourself.',
  };
}

/**
 * Convenience predicate — useful for tests + documentation.
 */
export function isGatedToolName(toolName: string): boolean {
  return GATED_TOOL_NAMES.includes(toolName);
}
