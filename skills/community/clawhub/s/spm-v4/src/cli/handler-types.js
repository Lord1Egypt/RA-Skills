/**
 * SPM v4 — CLI handler type definitions.
 *
 * @module cli/handler-types
 */

/**
 * CLI command handler function.
 *
 * @async
 * @param {string[]} args — Command-line arguments after the command name
 * @param {object} [options] — Parsed options (e.g. { help: boolean, verbose: boolean })
 * @returns {Promise<number>} — Exit code (0 = success, 1 = failure)
 */
export function CommandHandler(args, options) {
  // This is a type definition only; the actual function body is not used.
  throw new Error('Type definition — do not call directly');
}