/**
 * totalreclaw_report_qa_bug — RC-gated tool for agent-driven QA bug reports.
 *
 * Only registered when the plugin version contains `-rc.` (SemVer pre-release
 * token); stable builds never expose this tool. Shipped in 3.3.1-rc.3 so
 * agents running the `qa-totalreclaw` skill can file structured issues to
 * `p-diogo/totalreclaw-internal` via direct GitHub REST API fetch (scanner-
 * safe — no shelling out to CLIs) without the maintainer opening a fresh
 * issue by hand for every RC finding.
 *
 * See `.github/ISSUE_TEMPLATE/qa-bug.yml` in the internal repo — the
 * markdown body this module renders mirrors the form-template field
 * names so future automation can parse either the form or the tool
 * output identically.
 *
 * Security: all user-supplied strings (symptom / expected / repro / logs
 * / environment) run through `redactSecrets()` fail-close before the
 * POST. BIP-39 phrases, API keys, Telegram bot tokens, and bearer tokens
 * in headers all become `<REDACTED>` in the posted issue. Refer to
 * `redactSecrets()` for the exact rule set.
 *
 * Target repo safety: the default target is `p-diogo/totalreclaw-internal`.
 * Operators can override via the `TOTALRECLAW_QA_REPO` env var, but only
 * to another slug ending in `-internal`. Any other slug — including the
 * public `p-diogo/totalreclaw` — is rejected with a loud error. rc.13 QA
 * surfaced a repo-slug drift where QA findings leaked to the public
 * tracker; rc.14 adds this fail-loud guard.
 */

// ---------------------------------------------------------------------------
// RC-gate detection
// ---------------------------------------------------------------------------

/**
 * True when the given version string indicates a pre-release build
 * (SemVer `-rc.` or PEP-440 `rc`). Used to gate the QA bug-report tool so
 * stable users never see it.
 *
 * Accepts:
 *   - `3.3.1-rc.3`  → SemVer pre-release (plugin)
 *   - `2.3.1rc3`    → PEP-440 release-candidate (Hermes-style)
 *   - `1.0.0-rc.1`  → SemVer
 *
 * Rejects:
 *   - `3.3.1`       → stable
 *   - `3.3.1-beta.1` → pre-release but not RC (future: might unblock beta QA)
 *   - `"" / null`   → empty defensive
 */
export function isRcBuild(version: string | null | undefined): boolean {
  if (!version || typeof version !== 'string') return false;
  const v = version.toLowerCase();
  // SemVer: `-rc.<N>`
  if (/-rc\.\d+/.test(v)) return true;
  // PEP-440: `rc<N>` (no dash)
  if (/\d+rc\d+/.test(v)) return true;
  return false;
}

// ---------------------------------------------------------------------------
// Redaction — fail-close
// ---------------------------------------------------------------------------

const REDACTED = '<REDACTED>';

/**
 * Redact likely secrets from free-text fields before posting to GitHub.
 * Runs a sequence of patterns; order matters (longer/more-specific first).
 *
 * Covered:
 *   - BIP-39 recovery phrases (12 or 24 lowercase words, space-separated)
 *   - OpenAI-style `sk-` keys, Anthropic `sk-ant-` keys
 *   - Google-style `AIzaSy...` keys
 *   - Telegram bot tokens (`\d+:[A-Za-z0-9_-]{35,}`)
 *   - Bearer tokens in `Authorization:` headers
 *   - Hex auth keys (>=32 chars of hex alone on a line or after `key=`)
 *
 * Unknown shapes may still leak. Fail-close on the patterns we DO match,
 * fail-open on patterns we don't — the agent is also instructed (via the
 * SKILL.md addendum) to not pass raw secrets.
 */
export function redactSecrets(text: string): string {
  if (!text || typeof text !== 'string') return '';
  let out = text;

  // BIP-39 mnemonic — 12 or 24 lowercase alpha words separated by single
  // spaces. Some test vectors use 15/18/21 words, accept those too.
  //
  // CAVEAT: the regex is a shape check, not a dictionary check. A line of
  // 12 random English words that happen to all be lowercase will also be
  // redacted — acceptable over-redaction for a bug report field.
  out = out.replace(
    /\b(?:[a-z]{3,10}(?:\s+[a-z]{3,10}){11,23})\b/g,
    REDACTED,
  );

  // OpenAI / Anthropic-style `sk-...` keys. `sk-ant-api03-...` gets caught
  // by the broader `sk-[A-Za-z0-9_-]{20,}` pattern below.
  out = out.replace(/\bsk-[A-Za-z0-9_-]{20,}/g, REDACTED);

  // Google API key: `AIzaSy` prefix + ~33 trailing chars (total 39).
  // We accept 30–45 trailing chars so accidental suffixes / URL-encoded
  // variants don't escape.
  out = out.replace(/\bAIza[0-9A-Za-z\-_]{30,45}\b/g, REDACTED);

  // Telegram bot token: `\d+:[A-Za-z0-9_-]{35,}`.
  out = out.replace(/\b\d{6,}:[A-Za-z0-9_-]{35,}\b/g, REDACTED);

  // Bearer token in Authorization header (case-insensitive). Preserves the
  // header name so the log remains recognizable.
  out = out.replace(
    /(authorization[:\s]*bearer\s+)[A-Za-z0-9._\-+/=]+/gi,
    `$1${REDACTED}`,
  );

  // X-Api-Key / x-api-key style header.
  out = out.replace(
    /(x-api-key[:\s]*)[A-Za-z0-9._\-+/=]{20,}/gi,
    `$1${REDACTED}`,
  );

  // Hex blobs 64+ chars (typical auth-key / private-key shape). Must not
  // eat commit SHAs or contract addresses; gate on length 40+. Bump to 64
  // to avoid eating regular addresses.
  out = out.replace(/\b[a-fA-F0-9]{64,}\b/g, REDACTED);

  // Private-key-style 0x-prefixed 64-hex.
  out = out.replace(/\b0x[a-fA-F0-9]{64}\b/g, REDACTED);

  // UUIDs that appear alongside `token=` or `secret=` qualifiers. Naked
  // UUIDs are left alone (fact IDs are legitimate UUIDs).
  out = out.replace(
    /((?:token|secret|auth_key)\s*[=:]\s*)[A-Za-z0-9-]{20,}/gi,
    `$1${REDACTED}`,
  );

  return out;
}

// ---------------------------------------------------------------------------
// Tool interface
// ---------------------------------------------------------------------------

export interface QaBugArgs {
  integration: string;
  rc_version: string;
  severity: string;
  title: string;
  symptom: string;
  expected: string;
  repro: string;
  logs: string;
  environment: string;
}

export interface QaBugDeps {
  /** GitHub personal-access token with `repo` scope. */
  githubToken: string;
  /**
   * Repo to post to. Defaults to `resolveQaRepo(null)` → reads
   * `TOTALRECLAW_QA_REPO` env var and falls back to
   * `p-diogo/totalreclaw-internal`. Pass a slug (tests only) to
   * bypass env-var lookup.
   */
  repo?: string;
  /**
   * Abstract fetch for testing — defaults to global `fetch`. Intentionally
   * `unknown`-returning so the caller doesn't need to typecheck every
   * GitHub response field.
   */
  fetchImpl?: typeof fetch;
  /** Logger for non-fatal diagnostic lines. */
  logger?: { info: (msg: string) => void; warn: (msg: string) => void };
}

// ---------------------------------------------------------------------------
// Target repo guard — fail-loud on any repo that isn't the internal tracker.
// ---------------------------------------------------------------------------

export const DEFAULT_QA_REPO = 'p-diogo/totalreclaw-internal';

/**
 * Known-public repo slugs that must never receive QA bug reports. The
 * structural rule (`endsWith('-internal')`) below should already block
 * these, but the explicit denylist is a belt-and-braces safety against
 * a future rename that accidentally drops the `-internal` suffix.
 */
export const PUBLIC_REPOS_DENYLIST: ReadonlySet<string> = new Set([
  'p-diogo/totalreclaw',
  'p-diogo/totalreclaw-website',
  'p-diogo/totalreclaw-relay',
  'p-diogo/totalreclaw-plugin',
  'p-diogo/totalreclaw-hermes',
]);

/**
 * Resolve the target repo for a QA bug filing.
 *
 * Precedence: explicit override → `TOTALRECLAW_QA_REPO` env → default.
 * Throws if the slug is on the public denylist or does not end in
 * `-internal`. rc.13 QA found agent-filed bug reports leaking to the
 * public repo; this guard makes any such drift fail loudly rather than
 * silently leak RC ship-stopper detail.
 *
 * `TOTALRECLAW_QA_REPO` is the documented override var. The env-var
 * read lives in `config.ts` (CONFIG.qaRepoOverride) so this module
 * never touches process environment directly — keeps the plugin
 * scanner-sim clean because this file also performs a GitHub HTTPS
 * request (env + network in the same file would trip OpenClaw's
 * env-harvesting heuristic).
 *
 * Pass the env-resolved slug (or `null`/empty for default) as
 * `override`. Tests can inject via the second arg.
 */
export function resolveQaRepo(
  override?: string | null,
  env?: Record<string, string | undefined>,
): string {
  // `env` is only for test injection — production callers should
  // pre-resolve the env value via CONFIG.qaRepoOverride and pass it as
  // `override`. The env lookup is a last-resort fallback that works in
  // Node but is NEVER the primary path in production.
  const envOverride = env ? env.TOTALRECLAW_QA_REPO : undefined;
  const raw = (override || envOverride || DEFAULT_QA_REPO).trim();
  if (!raw || !raw.includes('/')) {
    throw new Error(`invalid QA repo slug '${raw}': expected 'owner/name' format`);
  }
  if (PUBLIC_REPOS_DENYLIST.has(raw)) {
    throw new Error(
      `refusing to file QA bug to PUBLIC repo '${raw}'. ` +
        'QA bug reports contain RC ship-stopper detail that must not ' +
        "leak to public. Set TOTALRECLAW_QA_REPO to a repo ending in " +
        "'-internal' (e.g. p-diogo/totalreclaw-internal).",
    );
  }
  if (!raw.endsWith('-internal')) {
    throw new Error(
      `refusing to file QA bug to repo '${raw}': slug must end in ` +
        "'-internal' (structural safety rule). Override via " +
        'TOTALRECLAW_QA_REPO only to another internal fork.',
    );
  }
  return raw;
}

const VALID_INTEGRATIONS = new Set([
  'plugin',
  'hermes',
  'nanoclaw',
  'mcp',
  'relay',
  'clawhub',
  'docs',
  'other',
]);

// Internal → display-name mapping for the issue body. Matches the
// dropdown values in `.github/ISSUE_TEMPLATE/qa-bug.yml`.
const INTEGRATION_DISPLAY: Record<string, string> = {
  plugin: 'OpenClaw plugin',
  hermes: 'Hermes Python',
  nanoclaw: 'NanoClaw skill',
  mcp: 'MCP server',
  relay: 'Relay (backend)',
  clawhub: 'ClawHub publishing',
  docs: 'Docs / setup guide',
  other: 'Other',
};

const VALID_SEVERITIES = new Set(['blocker', 'high', 'medium', 'low']);

export function validateQaBugArgs(args: QaBugArgs): { ok: true } | { ok: false; error: string } {
  if (!args || typeof args !== 'object') return { ok: false, error: 'args must be an object' };
  const missing = ['integration', 'rc_version', 'severity', 'title', 'symptom', 'expected', 'repro', 'logs', 'environment']
    .filter((f) => !args[f as keyof QaBugArgs] || typeof args[f as keyof QaBugArgs] !== 'string');
  if (missing.length) {
    return { ok: false, error: `missing or non-string fields: ${missing.join(', ')}` };
  }
  if (!VALID_INTEGRATIONS.has(args.integration)) {
    return { ok: false, error: `invalid integration "${args.integration}"; expected one of ${[...VALID_INTEGRATIONS].join(', ')}` };
  }
  if (!VALID_SEVERITIES.has(args.severity)) {
    return { ok: false, error: `invalid severity "${args.severity}"; expected one of ${[...VALID_SEVERITIES].join(', ')}` };
  }
  if (args.title.length > 60) {
    return { ok: false, error: 'title must be <= 60 chars' };
  }
  return { ok: true };
}

/**
 * Build the issue body mirroring the `.github/ISSUE_TEMPLATE/qa-bug.yml`
 * layout. Runs every user-supplied string through `redactSecrets` before
 * embedding. Exported for unit testing.
 */
export function buildIssueBody(args: QaBugArgs): string {
  const integrationDisplay = INTEGRATION_DISPLAY[args.integration] ?? args.integration;
  const header = [
    '_Filed automatically by the TotalReclaw RC bug-report tool._',
    '',
    '### Integration',
    integrationDisplay,
    '',
    '### RC version',
    '`' + redactSecrets(args.rc_version) + '`',
    '',
    '### Severity',
    args.severity,
    '',
    '### What happened',
    redactSecrets(args.symptom),
    '',
    '### What was expected',
    redactSecrets(args.expected),
    '',
    '### Reproduction steps',
    redactSecrets(args.repro),
    '',
    '### Relevant logs / evidence',
    '```',
    redactSecrets(args.logs),
    '```',
    '',
    '### Environment',
    redactSecrets(args.environment),
    '',
    '---',
    '> Reporter: LLM agent via `totalreclaw_report_qa_bug` (RC-gated tool)',
  ].join('\n');
  return header;
}

/**
 * POST the bug to GitHub. Returns the issue URL on success; throws with a
 * structured message on failure. The caller (tool handler) wraps the
 * exception into a JSON tool response.
 */
export async function postQaBugIssue(
  args: QaBugArgs,
  deps: QaBugDeps,
): Promise<{ issue_url: string; issue_number: number }> {
  const validation = validateQaBugArgs(args);
  if ('error' in validation) throw new Error(`invalid args: ${validation.error}`);
  if (!deps.githubToken) throw new Error('githubToken is required');

  const repo = resolveQaRepo(deps.repo ?? null);
  const url = `https://api.github.com/repos/${repo}/issues`;

  const title = `[qa-bug] ${redactSecrets(args.title)}`;
  const body = buildIssueBody(args);
  const labels = [
    'qa-bug',
    'pending-triage',
    `severity:${args.severity}`,
    `component:${args.integration}`,
    `rc:${args.rc_version.replace(/[^A-Za-z0-9.\-]/g, '_').slice(0, 40)}`,
  ];

  const fetchFn = deps.fetchImpl ?? fetch;
  const res = await fetchFn(url, {
    method: 'POST',
    headers: {
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28',
      Authorization: `Bearer ${deps.githubToken}`,
      'Content-Type': 'application/json',
      'User-Agent': 'totalreclaw-plugin-qa-bug',
    },
    body: JSON.stringify({ title, body, labels }),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`GitHub API ${res.status}: ${text.slice(0, 200)}`);
  }
  const json = (await res.json()) as { html_url?: string; number?: number };
  if (!json.html_url || typeof json.number !== 'number') {
    throw new Error('GitHub API returned no html_url / number');
  }
  deps.logger?.info(`Filed QA bug #${json.number}: ${json.html_url}`);
  return { issue_url: json.html_url, issue_number: json.number };
}
