/**
 * Secret handling — file-based loader with guardrails.
 *
 * Rules enforced here:
 *   1. Secrets come from a file path. If the file is missing, falls back
 *      to STELLAR_SECRET in .env.prod then .env (same directory).
 *   2. The value must match the Stellar strkey pattern (S... 56 chars).
 *   3. We install a stdout/stderr wrapper that replaces any accidental
 *      occurrence of the secret with [REDACTED].
 *   4. No module-level storage — loadSecretFromFile returns the value and
 *      the caller holds it in a local binding only.
 */

import * as fs from "node:fs";
import * as nodePath from "node:path";
import { execFileSync } from "node:child_process";
import * as os from "node:os";

const REDACTED = "[REDACTED:signing-key]";

const STELLAR_SECRET_RE = /^S[A-Z0-9]{55}$/;

/**
 * Env var names that may hold a Stellar secret key. Checked in order;
 * first one that matches the strkey format wins.
 *
 * The canonical name is STELLAR_SECRET. The others are accepted for
 * compatibility with older setups — loadSecretFromFile reports which
 * name was used so callers (e.g. onboard) can offer a migration hint.
 */
export const PREFERRED_SECRET_ENV_KEY = "STELLAR_SECRET";
export const SECRET_ENV_KEYS = [
  "STELLAR_SECRET",
  "STELLAR_SECRET_KEY",
  "STELLAR_PRIVATE_KEY",
  "STELLAR_PRIVATE",
] as const;
export type SecretEnvKey = (typeof SECRET_ENV_KEYS)[number];

export interface SecretSource {
  /** Absolute path where the secret was found. */
  path: string;
  /** "file" = one-secret-per-line file; "env" = dotenv-format KEY=VALUE; "identity" = Stellar CLI identity. */
  kind: "file" | "env" | "identity";
  /** Which env key matched. Only set for kind === "env". */
  envKey?: SecretEnvKey;
  /** Stellar CLI identity name. Only set for kind === "identity". */
  identity?: string;
}

interface DotEnvHit {
  value: string;
  key: SecretEnvKey;
}

function tryLoadFromEnvFile(envPath: string): DotEnvHit | undefined {
  let raw: string;
  try {
    raw = fs.readFileSync(envPath, "utf8");
  } catch {
    return undefined;
  }
  const vars = new Map<string, string>();
  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const m = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)/);
    if (m) {
      const val = m[2].trim().replace(/^['"]|['"]$/g, "");
      vars.set(m[1], val);
    }
  }
  for (const key of SECRET_ENV_KEYS) {
    const val = vars.get(key);
    if (val && STELLAR_SECRET_RE.test(val)) {
      return { value: val, key };
    }
  }
  return undefined;
}

/**
 * Read a Stellar secret key from a file path.
 *
 * The file should contain a single line: the S... strkey. Any surrounding
 * whitespace is trimmed. Blank lines and lines starting with # are ignored
 * so the same file can carry a comment header if desired.
 *
 * Fallback: if the secret file does not exist, checks .env.prod then .env
 * (relative to the secret file's directory) for a STELLAR_SECRET= line.
 */
/**
 * "No secret here" as a distinguishable error. Callers that fall back to
 * another location must be able to tell absence from an unreadable file, so
 * they never quietly switch wallets on a permissions problem.
 */
function notFound(message: string): Error & { code: string } {
  return Object.assign(new Error(message), { code: "ENOENT" as const });
}

export function loadSecretFromFile(path: string): string {
  // A caller of this API passed the path itself, which is the same
  // authorisation --secret-file carries.
  return loadSecretWithSource(path, { mayReadEnvFiles: true }).secret;
}

export function loadSecretFromBase(base: {
  secretFile: string;
  identity?: string;
}): string {
  return loadSecretWithSourceFromBase(base).secret;
}

export function loadSecretWithSourceFromBase(base: {
  secretFile: string;
  secretFileExplicit?: boolean;
  identity?: string;
}): { secret: string; source: SecretSource } {
  if (base.identity) return loadSecretFromIdentity(base.identity);
  if (base.secretFileExplicit) {
    // The user named this path, which authorises reading its directory.
    return loadSecretWithSource(base.secretFile, { mayReadEnvFiles: true });
  }
  // Nothing was named, so only files this skill owns are in scope: a
  // `.stellar-secret` this skill wrote, never a file that belongs to someone
  // else. The working directory comes first because that is where
  // generate-keypair.ts writes by default.
  //
  // Nothing here moves, rewrites or deletes any of those files. Discovery is
  // read-only; a wallet found in an older install stays exactly where it is,
  // and the user is told where it was read from so they can decide.
  let firstError: any;
  for (const candidate of secretFileCandidates(base.secretFile)) {
    try {
      const loaded = loadSecretWithSource(candidate, { mayReadEnvFiles: false });
      if (candidate !== base.secretFile) {
        console.error(
          `ℹ️  No ${base.secretFile} here; using the wallet at ${candidate}.\n` +
            `   Nothing was moved. To make it version-proof, copy it yourself to ` +
            `${ownedSecretPath()}.`,
        );
      }
      return loaded;
    } catch (err: any) {
      // Move on ONLY when the file is genuinely absent. An unreadable file
      // (EACCES, a permission-denied parent directory) must surface as
      // itself: quietly signing with a different wallet than the one the user
      // has in that directory is a worse outcome than failing.
      if (err?.code !== "ENOENT") throw err;
      firstError ??= err;
    }
  }
  throw firstError;
}

/**
 * Every place this skill may have written a `.stellar-secret`, in order.
 *
 * The third group is why this list exists. A plugin install is versioned —
 * `.../stellar-agent-wallet/1.8.2/` — and the next version is a SIBLING
 * directory, so a wallet generated under the default in one version is
 * invisible to the next. Those are still this skill's own files in this
 * skill's own install directories, so finding them is fair game; a generic
 * `~/.env` or any other file belonging to the user is not, and never appears
 * here.
 *
 * Newest sibling first, so an upgrade path that has been through several
 * versions lands on the most recently used wallet rather than the oldest.
 */
export function secretFileCandidates(secretFile: string): string[] {
  const out = [secretFile, ownedSecretPath()];
  for (const dir of siblingInstallDirs()) {
    const p = nodePath.join(dir, ".stellar-secret");
    if (!out.includes(p)) out.push(p);
  }
  return out.filter((p, i) => out.indexOf(p) === i);
}

/** Other installed versions of this skill, newest first. Never throws. */
function siblingInstallDirs(): string[] {
  try {
    const here = nodePath.resolve(process.env.CLAUDE_PLUGIN_ROOT ?? process.cwd());
    const parent = nodePath.dirname(here);
    // Only when the layout really is <...>/stellar-agent-wallet/<version>/.
    if (nodePath.basename(parent) !== "stellar-agent-wallet") return [];
    return fs
      .readdirSync(parent, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .map((e) => nodePath.join(parent, e.name))
      .filter((p) => p !== here)
      .sort((a, b) => compareVersionDesc(nodePath.basename(a), nodePath.basename(b)));
  } catch {
    return [];
  }
}

/** Sort version-like directory names newest first; non-versions sort last. */
function compareVersionDesc(a: string, b: string): number {
  const parse = (v: string) =>
    /^\d+(\.\d+)*$/.test(v) ? v.split(".").map(Number) : null;
  const pa = parse(a);
  const pb = parse(b);
  if (!pa && !pb) return a < b ? 1 : a > b ? -1 : 0;
  if (!pa) return 1;
  if (!pb) return -1;
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const d = (pb[i] ?? 0) - (pa[i] ?? 0);
    if (d !== 0) return d;
  }
  return 0;
}

/**
 * This skill's own place for a secret, used when no path was given.
 *
 * The default `.stellar-secret` is relative, so it lands in the working
 * directory — which, when the documented commands are followed, is the
 * versioned plugin install (`.../stellar-agent-wallet/1.8.2/`). A wallet
 * generated there becomes invisible to the next version, whose install is a
 * sibling directory. This location does not move with the version.
 */
export function ownedSecretPath(): string {
  return nodePath.join(os.homedir(), ".stellar-agent-wallet", ".stellar-secret");
}

export function loadSecretFromIdentity(
  identity: string,
): { secret: string; source: SecretSource } {
  let raw: string;
  try {
    raw = execFileSync("stellar", ["keys", "secret", identity], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });
  } catch (err: any) {
    const detail = err?.stderr ? String(err.stderr).trim() : String(err);
    throw new Error(
      `Could not read Stellar CLI identity "${identity}". ` +
        `Check it with: stellar keys public-key ${identity}` +
        (detail ? `\n${detail}` : ""),
    );
  }

  const line = raw
    .split(/\r?\n/)
    .map((l) => l.trim())
    .find((l) => l.length > 0 && !l.startsWith("#"));
  if (!line || !STELLAR_SECRET_RE.test(line)) {
    throw new Error(
      `Stellar CLI identity "${identity}" did not return a valid Stellar secret key.`,
    );
  }

  installRedactor(line);
  const configHome =
    process.env.XDG_CONFIG_HOME ?? nodePath.join(os.homedir(), ".config");
  return {
    secret: line,
    source: {
      path: nodePath.join(configHome, "stellar", "identity", `${identity}.toml`),
      kind: "identity",
      identity,
    },
  };
}

/**
 * Print a one-line reminder that the loaded key is sitting in plaintext,
 * with a pointer to the safer alternative.
 *
 * Both supported non-identity sources — a `.stellar-secret` file and a
 * `STELLAR_SECRET`-style dotenv entry — are unencrypted: whoever reads
 * the file owns the wallet. That is a deliberate trade-off for an agent
 * skill, but it should never be invisible at runtime, so every process
 * that loads such a key says so once on stderr.
 *
 * `--identity <name>` delegates to Stellar CLI key management instead
 * and does not warn.
 */
let plaintextNotePrinted = false;

function notePlaintextSecret(source: SecretSource): void {
  if (source.kind === "identity") return;
  if (plaintextNotePrinted) return;
  plaintextNotePrinted = true;

  const what =
    source.kind === "env"
      ? `${source.envKey ?? "STELLAR_SECRET"} in ${source.path}`
      : source.path;
  console.error(
    `⚠️  Signing key loaded from ${what} (plaintext — anyone who reads it can spend this wallet).`,
  );
  console.error(
    "   Safer: keep it in Stellar CLI key management and pass --identity <name>.",
  );
}

/**
 * Like loadSecretFromFile but also returns where the secret came from.
 * onboard uses the source info to suggest a migration from legacy env
 * key names to the canonical STELLAR_SECRET.
 */
export function loadSecretWithSource(
  path: string,
  opts: { mayReadEnvFiles?: boolean } = {},
): { secret: string; source: SecretSource } {
  let raw: string;
  try {
    raw = fs.readFileSync(path, "utf8");
  } catch (err: any) {
    if (err?.code === "ENOENT") {
      const dir = nodePath.dirname(nodePath.resolve(path));
      // `.env.prod` / `.env` are the USER's files and routinely hold
      // credentials for unrelated things. We only look at them when the user
      // named this location with --secret-file; an unnamed default directory
      // is not an invitation to read whatever secrets happen to sit there.
      const envFallbacks = opts.mayReadEnvFiles
        ? [nodePath.join(dir, ".env.prod"), nodePath.join(dir, ".env")]
        : [];
      for (const envPath of envFallbacks) {
        const hit = tryLoadFromEnvFile(envPath);
        if (hit) {
          const legacyNote =
            hit.key === PREFERRED_SECRET_ENV_KEY
              ? ""
              : ` (legacy key name — rename to ${PREFERRED_SECRET_ENV_KEY})`;
          console.error(
            `ℹ️  Secret file ${path} not found; loaded ${hit.key} from ${envPath}${legacyNote}`,
          );
          installRedactor(hit.value);
          const envSource: SecretSource = {
            path: envPath,
            kind: "env",
            envKey: hit.key,
          };
          notePlaintextSecret(envSource);
          return { secret: hit.value, source: envSource };
        }
      }
      throw notFound(
        `Secret file not found at ${path}. Generate one with:\n` +
          `  ./node_modules/.bin/tsx scripts/generate-keypair.ts\n` +
          `or pass an existing file via --secret-file <path>,\n` +
          (opts.mayReadEnvFiles
            ? `or set one of ${SECRET_ENV_KEYS.join(", ")} in .env.prod or .env.`
            : `or put one at ${ownedSecretPath()}.\n` +
              `(.env files are only read from a directory you name with --secret-file.)`),
      );
    }
    throw err;
  }

  // Pick the first non-blank, non-comment line.
  const line = raw
    .split(/\r?\n/)
    .map((l) => l.trim())
    .find((l) => l.length > 0 && !l.startsWith("#"));

  if (!line) {
    throw new Error(
      `Secret file ${path} is empty or only contains comments.`,
    );
  }

  if (!STELLAR_SECRET_RE.test(line)) {
    throw new Error(
      `Secret file ${path} does not contain a valid Stellar secret key ` +
        `(expected 56 characters starting with S).`,
    );
  }

  installRedactor(line);
  const fileSource: SecretSource = {
    path: nodePath.resolve(path),
    kind: "file",
  };
  notePlaintextSecret(fileSource);
  return { secret: line, source: fileSource };
}


/**
 * Wrap process.stdout.write and process.stderr.write so that any
 * accidental occurrence of the secret is replaced with [REDACTED].
 *
 * This is a belt-and-braces defense — code should never pass the
 * secret to a print function in the first place.
 */
function installRedactor(secret: string): void {
  const origStdout = process.stdout.write.bind(process.stdout);
  const origStderr = process.stderr.write.bind(process.stderr);

  const redact = (chunk: any): any => {
    if (typeof chunk === "string") {
      return chunk.includes(secret) ? chunk.split(secret).join(REDACTED) : chunk;
    }
    if (Buffer.isBuffer(chunk)) {
      const s = chunk.toString("utf8");
      if (s.includes(secret)) {
        return Buffer.from(s.split(secret).join(REDACTED), "utf8");
      }
    }
    return chunk;
  };

  process.stdout.write = ((chunk: any, ...rest: any[]) =>
    origStdout(redact(chunk), ...rest)) as typeof process.stdout.write;
  process.stderr.write = ((chunk: any, ...rest: any[]) =>
    origStderr(redact(chunk), ...rest)) as typeof process.stderr.write;
}
