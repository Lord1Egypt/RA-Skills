/**
 * rl-runtime-guard — Drop-in adapter for OpenClaw hook systems
 * ============================================================
 *
 * This file shows how to wire `applyGuards()` into an OpenClaw hook
 * lifecycle. Copy to ~/.openclaw/hooks/rl-runtime-guard/handler.js (or
 * the location your OpenClaw install expects).
 *
 * Usage with the CommonJS OpenClaw hook contract:
 */

// CommonJS adapter for legacy hook systems
const { applyGuards, DEFAULT_CONFIG } = await import('./handler.mjs');
const sessionStore = new Map();

async function requestBeforeHandler(ctx) {
  try {
    return applyGuards(ctx, sessionStore, DEFAULT_CONFIG);
  } catch (err) {
    console.error('[rl-runtime-guard] error:', err.message);
    return [];
  }
}

module.exports = { requestBeforeHandler, applyGuards, DEFAULT_CONFIG };