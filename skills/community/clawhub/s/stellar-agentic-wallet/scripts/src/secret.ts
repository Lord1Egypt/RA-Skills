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
export function loadSecretFromFile(path: string): string {
  return loadSecretWithSource(path).secret;
}

export function loadSecretFromBase(base: {
  secretFile: string;
  identity?: string;
}): string {
  return loadSecretWithSourceFromBase(base).secret;
}

export function loadSecretWithSourceFromBase(base: {
  secretFile: string;
  identity?: string;
}): { secret: string; source: SecretSource } {
  if (base.identity) return loadSecretFromIdentity(base.identity);
  return loadSecretWithSource(base.secretFile);
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
 * Like loadSecretFromFile but also returns where the secret came from.
 * onboard uses the source info to suggest a migration from legacy env
 * key names to the canonical STELLAR_SECRET.
 */
export function loadSecretWithSource(
  path: string,
): { secret: string; source: SecretSource } {
  let raw: string;
  try {
    raw = fs.readFileSync(path, "utf8");
  } catch (err: any) {
    if (err?.code === "ENOENT") {
      const dir = nodePath.dirname(nodePath.resolve(path));
      const envFallbacks = [
        nodePath.join(dir, ".env.prod"),
        nodePath.join(dir, ".env"),
      ];
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
          return {
            secret: hit.value,
            source: { path: envPath, kind: "env", envKey: hit.key },
          };
        }
      }
      throw new Error(
        `Secret file not found at ${path}. Generate one with:\n` +
          `  npx tsx scripts/generate-keypair.ts\n` +
          `or pass an existing file via --secret-file <path>,\n` +
          `or set one of ${SECRET_ENV_KEYS.join(", ")} in .env.prod or .env.`,
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
  return {
    secret: line,
    source: { path: nodePath.resolve(path), kind: "file" },
  };
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
