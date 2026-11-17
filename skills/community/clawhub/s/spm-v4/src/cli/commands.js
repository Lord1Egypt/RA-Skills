/**
 * SPM v4 — CLI command handler exports.
 *
 * Re-exports all command handler functions for convenient imports.
 * Command registration and dispatch are handled by Commander.js
 * in {@link ../cli.js}.
 *
 * @module cli/commands
 */

export { initCommand } from './init.js';
export { attestCommand } from './attest.js';
export { verifyCommand } from './verify.js';
export { qualityCommand } from './quality.js';
export { statusCommand } from './status.js';
export { doctorCommand } from './doctor.js';