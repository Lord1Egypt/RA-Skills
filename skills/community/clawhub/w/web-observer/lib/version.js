/**
 * The version, in one place.
 *
 * Declared here rather than read from package.json at runtime, because an
 * installed skill is a directory copy and nothing guarantees which files came
 * with it. A test asserts this string matches package.json and SKILL.md, so the
 * three cannot drift.
 */
export const VERSION = "0.2.1";
