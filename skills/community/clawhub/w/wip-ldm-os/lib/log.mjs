/**
 * lib/log.mjs
 * Lightweight debug logger for LDM OS.
 * Opt-in via LDM_DEBUG=1 environment variable.
 */

const DEBUG = process.env.LDM_DEBUG === '1';

export function debug(context, msg, err) {
  if (DEBUG) {
    const ts = new Date().toISOString().slice(11, 19);
    const errMsg = err?.message || '';
    console.error(`[ldm:${context}] ${ts} ${msg}${errMsg ? ' ... ' + errMsg : ''}`);
  }
}
