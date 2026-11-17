/**
 * Every environment variable this skill reads, in one place.
 *
 * One list, for one reason: a variable the code reads and the frontmatter does
 * not declare is a publishing problem as well as a documentation one, because
 * ClawHub's security review compares declared metadata against actual
 * behaviour. A test asserts this list and SKILL.md's `envVars` are the same set,
 * and that no `env["..."]` read anywhere in the source names something outside
 * it, so neither can drift.
 */
/** Variables that configure Web Observer itself. */
export const OWN_ENV_VARS = [
    "WEB_OBSERVER_CONFIG",
    "WEB_OBSERVER_STATE",
    "OPENCLAW_STATE_DIR",
    "WEB_OBSERVER_VERCEL_SKILL_DIR",
    "WEB_OBSERVER_GA4_SKILL_DIR",
];
/**
 * Variables read only to hand on to the vercel-insights skill.
 *
 * Read, rather than left to the child to inherit, because a scheduled cron job
 * runs with the Gateway's environment: verified on OpenClaw 2026.7.1-2, a
 * command payload sees no `VERCEL_TOKEN` at all.
 */
export const VERCEL_ENV_VARS = [
    "VERCEL_TOKEN",
    "VERCEL_PROJECT_ID",
    "VERCEL_TEAM_ID",
    "VERCEL_TEAM_SLUG",
    "VERCEL_ORG_ID",
    "VERCEL_OWNER_ID",
];
/** Variables read only to hand on to the open-ga4 skill. */
export const GA4_ENV_VARS = [
    "GA4_CREDENTIALS",
    "GA4_PROPERTY_ID",
    "GOOGLE_APPLICATION_CREDENTIALS",
];
export const ALL_ENV_VARS = [
    ...OWN_ENV_VARS,
    ...VERCEL_ENV_VARS,
    ...GA4_ENV_VARS,
];
