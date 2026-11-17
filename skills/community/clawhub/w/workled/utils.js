// Shared utilities for workled skill

import { homedir } from "os";
import { join, dirname, sep, resolve } from "path";
import { spawnSync } from "child_process";
import {
  accessSync,
  constants,
  existsSync,
  readdirSync,
  statSync,
  symlinkSync,
  unlinkSync,
  writeFileSync,
} from "fs";

// Shared async delay, used by index.js (retry/discovery backoff) and
// skill-install.mjs (openclaw config-stabilisation polling).
export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Resolve the hermes home directory (single source of truth, shared by
// index.js and skill-install.mjs):
//   $HERMES_HOME env wins; otherwise Windows uses %LOCALAPPDATA%\hermes,
//   everything else uses ~/.hermes.
export function hermesHome() {
  const env = process.env.HERMES_HOME;
  if (env && env.trim()) return env.trim();
  if (process.platform === "win32") {
    const local = process.env.LOCALAPPDATA;
    return local && local.trim() ? join(local.trim(), "hermes") : join(homedir(), "AppData", "Local", "hermes");
  }
  return join(homedir(), ".hermes");
}

// Resolve the dsh (DeepSeek Harness) home directory, matching dsh's own
// resolveDshHome() (packages/util/home-paths): $DSH_HOME env wins, otherwise
// `~/.dsh` — cross-platform uniform, even on Windows (dsh never uses %APPDATA%).
export function dshHome() {
  const env = process.env.DSH_HOME;
  if (env && env.trim()) return env.trim();
  return join(homedir(), ".dsh");
}

// Resolve trae-cn's global Hooks config directory. trae-cn is a VSCode fork;
// its global Hooks (Settings > Hooks) live in a `.trae-cn` folder under the
// user's home directory — distinct from the per-edition user-data dir
// (%APPDATA%\Trae CN etc.). Windows uses %userprofile%/.trae-cn/hooks.json;
// macOS/Linux use ~/.trae-cn/hooks.json.
export function traeCnHooksHome() {
  return join(homedir(), ".trae-cn");
}

// Resolve trae-cn's per-user data dir, where its GLOBAL MCP config lives at
// <dir>/User/mcp.json (the VSCode convention trae-cn inherits). Tools in that
// file are shared by every workspace, mirroring a Settings > MCP "global"
// entry. Windows uses %APPDATA%\Trae CN; macOS/Linux use the platform config
// dir. Note: trae-cn HTTP-type MCP servers are declared bare `{ url,
// enabled }` here — no `type` field.
export function traeCnUserDir() {
  if (process.platform === "win32") {
    return join(process.env.APPDATA || join(homedir(), "AppData", "Roaming"), "Trae CN");
  }
  if (process.platform === "darwin") {
    return join(homedir(), "Library", "Application Support", "Trae");
  }
  return join(homedir(), ".config", "trae");
}

// Collect the names of variables persisted in the OS user/machine env.
// On Windows these live in the registry (HKCU\Environment +
// HKLM\...\Session Manager\Environment) and are inherited by EVERY process,
// so they can never be a signal that "this process was spawned by client X".
// On non-Windows (macOS/Linux the persistent env comes from shell profiles
// and is indistinguishable via process.env) we return an empty set, i.e. no
// variable is filtered out — detection then relies on process-injected vars
// and the existing MCP-config/sigDir fallbacks. Result is cached.
const _persistentEnvCache = new WeakMap();
export function persistentEnvVarNames() {
  if (_persistentEnvCache.has(process)) return _persistentEnvCache.get(process);
  const names = new Set();
  if (process.platform === "win32") {
    for (const hive of [
      "HKCU\\Environment",
      "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
    ]) {
      try {
        const r = spawnSync("reg", ["query", hive], { encoding: "utf8" });
        if (r.status === 0) {
          for (const line of r.stdout.split(/\r?\n/)) {
            const m = line.match(/^\s*([A-Za-z0-9_]+)\s+REG_/);
            if (m) names.add(m[1]);
          }
        }
      } catch {
        // registry query unavailable — ignore and move on
      }
    }
  }
  _persistentEnvCache.set(process, names);
  return names;
}

/**
 * Strip JSONC (JSON with comments) to valid JSON.
 * Handles line and block comments while preserving string literals.
 * A leading UTF-8 BOM is dropped so JSON.parse never trips on it.
 */
export function stripJsonc(src) {
  let out = "";
  let inStr = false;
  let i = 0;
  if (src.charCodeAt(0) === 0xfeff) i = 1;
  while (i < src.length) {
    const c = src[i];
    if (inStr) {
      out += c;
      if (c === "\\") {
        out += src[i + 1] ?? "";
        i += 2;
        continue;
      }
      if (c === '"') inStr = false;
      i++;
      continue;
    }
    if (c === '"') {
      inStr = true;
      out += c;
      i++;
      continue;
    }
    if (c === ",") {
      // JSONC allows a trailing comma before a closing brace/bracket
      // (`{"a": 1,}`). Drop such a comma. This branch is only reached outside
      // string literals, so a literal `,}` inside a string value is untouched.
      let j = i + 1;
      while (j < src.length && (src[j] === " " || src[j] === "\t" || src[j] === "\n" || src[j] === "\r")) j++;
      if (src[j] === "}" || src[j] === "]") {
        i++;
        continue;
      }
      out += c;
      i++;
      continue;
    }
    if (c === "/" && src[i + 1] === "/") {
      while (i < src.length && src[i] !== "\n") i++;
      continue;
    }
    if (c === "/" && src[i + 1] === "*") {
      i += 2;
      while (i < src.length && !(src[i] === "*" && src[i + 1] === "/")) i++;
      i += 2;
      continue;
    }
  out += c;
  i++;
  }
  return out;
}

// ---------------------------------------------------------------------------
// L1 standard-path writability probe (shared by installer and status).
//
// dsh installs to the L1 standard paths only — no workspace-local fallback and
// no env-only mode. Both the installer (before writing) and `status` (when
// diagnosing a missing dsh install) need the same answer, so it lives here.
// ---------------------------------------------------------------------------

// errno -> human reason, so a message says what is actually wrong instead of
// dumping a bare EACCES at the user.
export const WRITE_ERROR_REASONS = {
  EACCES: "permission denied - the current user may not write here",
  EPERM: "operation not permitted - sandbox, ACL, or a locked-down directory",
  EROFS: "read-only filesystem",
  ENOENT: "path does not exist and cannot be created",
  EBUSY: "path is locked by another process",
  EISDIR: "path is a directory, not a file",
};

// Closest ancestor of `p` that already exists. A not-yet-existing path is
// creatable iff that ancestor is writable, so probe the ancestor rather than
// creating directories just to test them.
export function nearestExistingAncestor(p) {
  let cur = p;
  while (cur && cur !== dirname(cur)) {
    if (existsSync(cur)) return cur;
    cur = dirname(cur);
  }
  return p;
}

// Non-destructive writability probe. An earlier version cleaned up with
// `rmdirSync(p, {recursive:true})`; for dsh one of the probed paths IS the
// installed bundle dir, so every re-install deleted the bundle before copying
// it back. This version only ever creates — and removes — its own uniquely
// named probe file.
export function checkWriteAccess(paths) {
  for (const p of paths) {
    const target = existsSync(p) ? p : nearestExistingAncestor(p);
    try {
      accessSync(target, constants.W_OK);
    } catch (e) {
      return { ok: false, path: toPosix(target), code: e.code || "UNKNOWN" };
    }
    // accessSync reports the ACL, not the effective outcome (sandboxes and
    // Windows directory ACLs disagree with it often enough to matter), so
    // confirm directories with a real write.
    let isDir = false;
    try {
      isDir = statSync(target).isDirectory();
    } catch {
      /* stat raced with a delete - treat as not a directory */
    }
    if (isDir) {
      const probe = join(target, `.workled-write-test-${process.pid}-${Date.now()}`);
      try {
        writeFileSync(probe, "test");
      } catch (e) {
        return { ok: false, path: toPosix(target), code: e.code || "UNKNOWN" };
      } finally {
        try {
          unlinkSync(probe);
        } catch {
          /* nothing to clean up */
        }
      }
    }
  }
  return { ok: true };
}

// Normalize an absolute path to forward slashes so emitted commands and the
// status report read identically on Windows and POSIX. A Windows backslash
// path (`C:\Users\...`) would otherwise (a) differ across platforms and
// (b) break when the byte is parsed by a cross-shell command runner.
export function toPosix(p) {
  return String(p).split(/[\\/]+/).join("/");
}

// ---------------------------------------------------------------------------
// Scoped-install repair: surface a `@namespace/workled` install at the canonical
// flat `skills/workled` entry point.
//
// Some market installers (e.g. skillhub) land a skill under a scoped directory
// `skills/@handle/workled`. Tooling and the workled entry-point convention,
// however, expect a flat `skills/workled`. When the real skill sits under a
// scope, create a cross-platform link at the parent level:
//   - Windows  -> junction (no admin required)
//   - POSIX    -> directory symlink
// Idempotent and non-destructive: if `skills/workled` already exists (real dir
// or link) it is left untouched, so a legitimate flat install is never
// clobbered. Failures (e.g. a sandbox that denies the write) are swallowed so
// the caller — the installer — is never blocked by a link it could not make.
// Link creation is the installer's responsibility alone; `status` only reports
// and never writes. Returns human-readable lines for the report (only when a
// link is actually created).
// ---------------------------------------------------------------------------
export function createSkillJunctions(skillsDir) {
  if (!skillsDir || !existsSync(skillsDir)) return [];
  const msgs = [];
  for (const entry of readdirSync(skillsDir, { withFileTypes: true })) {
    if (!entry.isDirectory() || !entry.name.startsWith("@")) continue;
    const nsDir = join(skillsDir, entry.name);
    // Only process workled: confirm `@namespace/workled/SKILL.md` exists.
    if (!existsSync(join(nsDir, "workled", "SKILL.md"))) continue;
    const linkPath = join(skillsDir, "workled");
    // Already exists (real dir or junction/symlink) — leave it alone.
    if (existsSync(linkPath)) continue;
    const targetPath = join(nsDir, "workled");
    try {
      const absTarget = resolve(targetPath);
      const type = process.platform === "win32" ? "junction" : "dir";
      symlinkSync(absTarget, linkPath, type);
      msgs.push(`Linked ${linkPath} -> ${absTarget}`);
    } catch {
      // junction/symlink creation failed (e.g. sandbox permission) — skip
    }
  }
  return msgs;
}
