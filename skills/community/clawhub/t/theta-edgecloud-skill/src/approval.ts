// Code-enforced approval and spend bounds for network-client mutations and inference.
// confirm:true is supplied by the calling agent: it records, but cannot verify, that the user
// approved this exact action. Use least-privilege keys and provider-side quotas as well.

import type { ThetaConfig } from './config.js';

function operatorDryRun(): boolean {
  return ['1', 'true', 'yes', 'on'].includes(String(process.env.THETA_DRY_RUN ?? '').trim().toLowerCase());
}

export function assertLive(cfg: ThetaConfig, action: string): void {
  if (cfg.dryRun || operatorDryRun()) throw new Error(`${action} blocked by THETA_DRY_RUN`);
}

export function assertApproved(cfg: ThetaConfig, confirm: unknown, action: string): void {
  assertLive(cfg, action);
  if (confirm !== true) {
    throw new Error(`${action} creates, changes, bills or deletes remote resources. Preview with THETA_DRY_RUN=1, get explicit user approval for this exact action, then pass confirm:true.`);
  }
}

// Plain JSON copy taken once at the client boundary. Getters, toJSON and prototypes run here, before
// any check, and only this validated copy is ever serialized and sent.
export function snapshotBody(value: unknown): Record<string, unknown> {
  let copy: unknown;
  try { copy = JSON.parse(JSON.stringify(value)); } catch { throw new Error('Request body must be JSON-serializable'); }
  if (!copy || typeof copy !== 'object' || Array.isArray(copy)) throw new Error('Request body must be an object');
  return copy as Record<string, unknown>;
}

const CALLBACK_KEY = /webhook|callback/i;

// Returns every webhook/callback field found at any depth of a (snapshotted) body.
export function findCallbackFields(value: unknown, path = ''): Array<{ path: string; value: unknown }> {
  if (!value || typeof value !== 'object') return [];
  const found: Array<{ path: string; value: unknown }> = [];
  for (const [key, item] of Object.entries(value)) {
    const here = path ? `${path}.${key}` : key;
    if (CALLBACK_KEY.test(key)) found.push({ path: here, value: item });
    else found.push(...findCallbackFields(item, here));
  }
  return found;
}

export const MAX_CHAT_TOKENS = 5000;
const FANOUT_OR_LENGTH_KEY = /^(?:max|min)_?.*tokens?$|^maxtokens$|^n$|^best_of$|^num_(?:beams|return_sequences|outputs|images)$|^max_length$/i;

// Bounds one chat call: max_tokens is clamped to 1..5000 (default 500) and alternative length or
// fan-out fields are removed, so a single call cannot request unbounded output.
export function boundChatParams<T extends Record<string, unknown>>(input: T, defaultMaxTokens = 500): T {
  if (!input || typeof input !== 'object' || Array.isArray(input)) return input;
  const out: Record<string, unknown> = { ...input };
  for (const key of Object.keys(out)) if (FANOUT_OR_LENGTH_KEY.test(key) && key !== 'max_tokens') delete out[key];
  if (Array.isArray(out.messages) || out.max_tokens !== undefined) {
    const requested = Number(out.max_tokens);
    const value = Number.isFinite(requested) ? Math.trunc(requested) : defaultMaxTokens;
    out.max_tokens = Math.min(Math.max(value, 1), MAX_CHAT_TOKENS);
  }
  return out as T;
}
