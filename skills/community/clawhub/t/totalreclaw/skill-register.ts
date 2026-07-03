/**
 * skill-register — mirror the bundled SKILL.md + skill.json into the
 * OpenClaw workspace skills directory on plugin load so the skill is
 * auto-discovered without a separate `openclaw skills install` step.
 *
 * Why this file exists
 * --------------------
 * Historically `openclaw plugins install @totalreclaw/totalreclaw`
 * installed only the plugin code; the SKILL.md instructions had to be
 * installed via a second `openclaw skills install totalreclaw` command
 * that agents frequently skipped — leaving the agent without the
 * pairing / recall playbook. With the skill files copied into
 * `~/.openclaw/workspace/skills/totalreclaw/` at register() time, the
 * workspace skill scanner picks them up on the next gateway load, so a
 * single `openclaw plugins install` is enough for both plugin + skill.
 *
 * Scanner note (MANDATORY — do not regress)
 * -----------------------------------------
 * This file is held scanner-clean by construction:
 *   - NO `process.env` reads. The home / workspace path arrives as a
 *     parameter from the caller, so the env-harvesting rule (env + net
 *     in the same file) can never fire here.
 *   - NO outbound-network primitives or trigger words. Disk-only. The
 *     potential-exfiltration rule (disk read + net in the same file)
 *     therefore cannot fire either.
 * Do NOT add network-capable imports or trigger-word comments to this
 * file — see `../scripts/check-scanner.mjs` for the exact rule set.
 */

import fs from 'node:fs';
import path from 'node:path';

/**
 * Minimal logger surface matching the slice of the host plugin logger
 * this helper uses. Declared locally so the module has no heavy type
 * dependency on the plugin API shape.
 */
export interface SkillRegisterLogger {
  info(...args: unknown[]): void;
  warn(...args: unknown[]): void;
}

export interface EnsureSkillRegisteredOptions {
  /**
   * The running plugin directory — i.e. the compiled `dist/` dir where
   * the plugin executes. SKILL.md and skill.json are resolved ONE level
   * up from this (the package root), matching the shipped tarball layout
   * (`dist/index.js` + `SKILL.md` + `skill.json` at the package root).
   */
  pluginDir: string;
  /**
   * The workspace `skills/` parent directory (typically
   * `~/.openclaw/workspace/skills`). A `totalreclaw/` subdirectory is
   * created / updated inside it. Passed in by the caller (resolved from
   * `CONFIG.openclawWorkspace`) so this file never reads the env.
   */
  skillsDir: string;
  /** Best-effort logger. Never throws. */
  logger: SkillRegisterLogger;
  /**
   * Override list of filenames to mirror. Defaults to SKILL.md +
   * skill.json. Exposed for tests; production callers omit it.
   */
  files?: readonly string[];
}

const DEFAULT_FILES: readonly string[] = ['SKILL.md', 'skill.json'];
const SKILL_SUBDIR = 'totalreclaw';

/**
 * Copy the bundled skill files (SKILL.md + skill.json) from the plugin
 * package root into `<skillsDir>/totalreclaw/` so the workspace skill
 * scanner discovers them on the next gateway load.
 *
 * Contract:
 *   - Creates `<skillsDir>/totalreclaw/` if missing (recursive).
 *   - Idempotent: a destination file whose bytes already match the
 *     source is left untouched (no rewrite, no mtime bump) so a healthy
 *     reload is a no-op.
 *   - A destination file whose content differs is overwritten with the
 *     bundled source — keeps the skill in sync with the installed
 *     plugin version across upgrades.
 *   - Missing source files are skipped (logged at warn) — a stripped or
 *     minimal install must not fail plugin load.
 *   - NEVER throws. All filesystem errors are swallowed and logged;
 *     this helper runs inside register() and a failure here must not
 *     block plugin activation.
 */
export function ensureSkillRegistered(opts: EnsureSkillRegisteredOptions): void {
  const { pluginDir, skillsDir, logger } = opts;
  const files = opts.files ?? DEFAULT_FILES;

  // Package root is one level up from the compiled `dist/` dir. This
  // mirrors the readPluginVersion() resolution in fs-helpers.ts.
  const packageRoot = path.dirname(pluginDir);
  const destDir = path.join(skillsDir, SKILL_SUBDIR);

  try {
    fs.mkdirSync(destDir, { recursive: true });
  } catch (err) {
    logger.warn(
      `TotalReclaw: skill auto-register skipped — could not create ${destDir}: ${
        err instanceof Error ? err.message : String(err)
      }`,
    );
    return;
  }

  for (const file of files) {
    const src = path.join(packageRoot, file);
    const dest = path.join(destDir, file);
    try {
      if (!fs.existsSync(src)) {
        // Bundled file absent (trimmed tarball / dev source tree). Skip
        // rather than failing register().
        logger.warn(
          `TotalReclaw: skill auto-register — bundled source not found, skipping: ${file}`,
        );
        continue;
      }

      // Idempotent fast path: identical bytes already on disk — leave
      // the destination untouched so a healthy reload is a no-op.
      if (fs.existsSync(dest)) {
        try {
          const srcBuf = fs.readFileSync(src);
          const destBuf = fs.readFileSync(dest);
          if (srcBuf.equals(destBuf)) {
            continue;
          }
        } catch {
          // Compare failed — fall through to the overwrite below.
        }
      }

      fs.copyFileSync(src, dest);
      logger.info(`TotalReclaw: skill auto-register — installed ${file} -> ${destDir}`);
    } catch (err) {
      logger.warn(
        `TotalReclaw: skill auto-register failed for ${file}: ${
          err instanceof Error ? err.message : String(err)
        }`,
      );
    }
  }
}
