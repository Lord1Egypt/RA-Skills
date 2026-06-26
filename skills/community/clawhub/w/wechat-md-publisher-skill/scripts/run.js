#!/usr/bin/env node

/**
 * wechat-md-publisher-skill launcher
 *
 * In-process launcher. Loads the pinned 'wechat-md-publisher' npm package
 * as an ES module via dynamic import and invokes its CLI entry by
 * injecting a validated, allow-listed argv. The launcher uses no
 * sub-process APIs and no shell.
 *
 * Security posture (mapping to applied codeguard-0-* rules):
 *
 * 1. Input validation & injection defense (codeguard-0-input-validation-injection):
 *    - Subcommands allow-listed via Set
 *    - Theme names allow-listed via strict regex
 *    - File paths rejected if they begin with '-' (option-injection guard)
 *    - All forwarded args length-bounded and stripped of NUL/control chars
 *    - argv is INJECTED into the imported module; it is never rendered
 *      into a command string for any external runner.
 *
 * 2. Supply chain (codeguard-0-supply-chain-security):
 *    - Pinned to REQUIRED_VERSION (EXACT match, no caret/range). Before
 *      dynamic import the launcher reads the resolved package.json,
 *      verifies "name" and "version" match the expected pins, and aborts
 *      otherwise. This blocks loading a different/unexpected local or
 *      global install that happens to expose a "wechat-md-publisher"
 *      directory.
 *    - Resolution paths are restricted to platform-standard *global*
 *      node_modules locations and the launcher's own bundled
 *      node_modules. The current working directory (CWD) is NOT searched,
 *      so running the launcher from an untrusted project directory cannot
 *      cause a malicious local node_modules to win resolution.
 *    - The skill does NOT auto-install or auto-update; module-not-found
 *      yields an actionable install command. Eliminates any "registry
 *      fetch on every run" supply-chain exposure.
 *
 * 3. Authorization & access control (codeguard-0-authorization-access-control):
 *    - Deny-by-default dispatcher: any unknown action falls through to
 *      showHelp() and never reaches the dynamic-import sink.
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const PINNED_PACKAGE = 'wechat-md-publisher';
// EXACT pinned version. Do NOT relax to a caret/range without re-audit:
// see codeguard-0-supply-chain-security and ClawScan finding regarding
// loose package resolution.
const REQUIRED_VERSION = '1.0.7';

// Allow-list of dispatcher actions handled by this launcher.
const ACTIONS = new Set([
  'publish',
  'draft',
  'wrapper',
  'list-drafts',
  'list-published',
  'themes',
  'help',
]);

// Theme allow-list pattern: lowercase letters, digits, hyphen, underscore.
// 64-char cap matches the upstream theme-name length limit.
const THEME_PATTERN = /^[a-z0-9][a-z0-9_-]{0,63}$/i;

const MAX_ARG_LEN = 1024;
const CONTROL_CHAR_RE = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/;

// ---------- Validation helpers ----------

const failWith = (message) => {
  console.error(JSON.stringify({ success: false, error: message }));
  process.exit(1);
};

const assertSafeArg = (value, label) => {
  if (typeof value !== 'string' || value.length === 0) {
    failWith(`Invalid ${label}: empty or non-string`);
  }
  if (value.length > MAX_ARG_LEN) {
    failWith(`Invalid ${label}: exceeds ${MAX_ARG_LEN} characters`);
  }
  if (CONTROL_CHAR_RE.test(value)) {
    failWith(`Invalid ${label}: contains control characters`);
  }
};

const validateTheme = (theme) => {
  assertSafeArg(theme, 'theme');
  if (!THEME_PATTERN.test(theme)) {
    failWith(`Invalid theme name: ${theme}`);
  }
  return theme;
};

const validateFilePath = (file) => {
  assertSafeArg(file, 'file path');
  if (file.startsWith('-')) {
    failWith('Invalid file path: must not start with "-"');
  }
  return path.normalize(file);
};

const validatePassthroughArgs = (extra) => {
  for (const item of extra) {
    assertSafeArg(item, 'argument');
  }
  return extra;
};

// ---------- Pinned-package resolution (no shell, no exec) ----------

/**
 * Trusted candidate roots for resolving the pinned package.
 *
 * Deliberately EXCLUDES process.cwd()/node_modules: an agent invoked from
 * an untrusted project directory must not be able to substitute its own
 * "wechat-md-publisher" by dropping a directory under ./node_modules.
 * See ClawScan finding: Agentic Supply Chain Vulnerabilities (run.js).
 */
function trustedCandidateRoots() {
  const nodeBinDir = path.dirname(process.execPath);
  return [
    // Unix layout: <prefix>/bin/node -> <prefix>/lib/node_modules
    path.join(nodeBinDir, '..', 'lib', 'node_modules'),
    // Windows layout: node.exe sits next to npm's node_modules
    path.join(nodeBinDir, 'node_modules'),
    // Launcher-local node_modules (shipped/audited alongside the skill).
    path.join(__dirname, '..', 'node_modules'),
  ];
}

/**
 * Resolve and verify the pinned 'wechat-md-publisher' package.
 *
 * Returns { cliEntry, packageRoot, manifest } on success.
 * On any failure (missing, name mismatch, version mismatch, manifest
 * unreadable / malformed) the function exits the process with an
 * actionable error and never returns.
 *
 * Verification steps (all required, in order):
 *   1. Resolve the package's package.json via Node's resolver, restricted
 *      to the trusted roots (no CWD).
 *   2. Read and parse the manifest (size-capped, JSON.parse, no eval).
 *   3. Require manifest.name === PINNED_PACKAGE (exact string match) to
 *      prevent a maliciously renamed shadow package.
 *   4. Require manifest.version === REQUIRED_VERSION (exact, no range).
 *   5. Resolve a known CLI sub-path inside that same package root, so the
 *      file we import is guaranteed to belong to the verified package.
 */
function resolveAndVerifyPinnedPackage() {
  const candidateRoots = trustedCandidateRoots();

  let manifestPath = null;
  try {
    manifestPath = require.resolve(`${PINNED_PACKAGE}/package.json`, {
      paths: candidateRoots,
    });
  } catch (_) {
    failWith(
      `'${PINNED_PACKAGE}' not found in any trusted node_modules location. ` +
      `Install the exact pinned version first: ` +
      `npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}`,
    );
  }

  // Size cap: any well-formed npm manifest is far smaller than this.
  // Prevents pathological reads if the file has been replaced.
  const MAX_MANIFEST_BYTES = 256 * 1024;
  let raw;
  try {
    const stat = fs.statSync(manifestPath);
    if (!stat.isFile()) {
      failWith(`Resolved package.json is not a regular file: ${manifestPath}`);
    }
    if (stat.size > MAX_MANIFEST_BYTES) {
      failWith(`Resolved package.json exceeds size cap (${stat.size} bytes)`);
    }
    raw = fs.readFileSync(manifestPath, 'utf8');
  } catch (err) {
    failWith(
      `Failed to read manifest for ${PINNED_PACKAGE}: ` +
      `${err && err.message ? err.message : err}`,
    );
  }

  let manifest;
  try {
    manifest = JSON.parse(raw);
  } catch (err) {
    failWith(
      `Failed to parse manifest for ${PINNED_PACKAGE}: ` +
      `${err && err.message ? err.message : err}`,
    );
  }

  if (manifest.name !== PINNED_PACKAGE) {
    failWith(
      `Refusing to load package: manifest.name='${manifest.name}' ` +
      `does not match pinned name '${PINNED_PACKAGE}'.`,
    );
  }
  if (manifest.version !== REQUIRED_VERSION) {
    failWith(
      `Refusing to load package: resolved version '${manifest.version}' ` +
      `does not match pinned version '${REQUIRED_VERSION}'. ` +
      `Re-audit upstream changes and update REQUIRED_VERSION explicitly, ` +
      `then run: npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}`,
    );
  }

  const packageRoot = path.dirname(manifestPath);

  // Known CLI sub-paths observed across published versions of the pinned
  // package. We resolve via require.resolve restricted to THIS package's
  // own root so we can't accidentally cross into a different copy.
  const subpaths = [
    `${PINNED_PACKAGE}/dist/cli.js`,
    `${PINNED_PACKAGE}/dist/cli/index.js`,
  ];
  for (const sub of subpaths) {
    try {
      const cliEntry = require.resolve(sub, { paths: candidateRoots });
      // Defense-in-depth: ensure the CLI entry lives inside the verified
      // package directory (prevents resolver edge cases from returning a
      // file outside packageRoot).
      const normalizedEntry = path.resolve(cliEntry);
      const normalizedRoot = path.resolve(packageRoot) + path.sep;
      if (!normalizedEntry.startsWith(normalizedRoot)) {
        failWith(
          `Resolved CLI entry '${normalizedEntry}' is outside verified ` +
          `package root '${normalizedRoot}'.`,
        );
      }
      return { cliEntry: normalizedEntry, packageRoot, manifest };
    } catch (_) {
      // sub-path not present in this version; try the next layout
    }
  }

  failWith(
    `'${PINNED_PACKAGE}@${REQUIRED_VERSION}' is installed but no known CLI ` +
    `entry was found. The upstream package layout may have changed; ` +
    `re-audit and update the skill before continuing.`,
  );
}

/**
 * Invoke the pinned 'wechat-md-publisher' module in-process.
 *
 * Safety invariants (must all hold; do NOT relax without re-review):
 *   - cliArgs has already been validated by assertSafeArg / theme & file
 *     guards in the dispatcher.
 *   - this function re-checks length and control-char invariants as
 *     defense-in-depth in case a caller bypasses the upstream validators.
 *   - the imported entry is loaded via file:// URL derived from a path
 *     resolved AND verified by resolveAndVerifyPinnedPackage(), which
 *     checks manifest.name and manifest.version against the exact pins
 *     before any code is loaded.
 *   - we mutate process.argv only with our validated argv prepended by
 *     [process.execPath, cliEntry] (the standard Node argv shape that
 *     commander expects).
 */
async function safeRunWmp(cliArgs) {
  if (!Array.isArray(cliArgs) || cliArgs.some((a) => typeof a !== 'string')) {
    failWith('Internal error: cliArgs must be an array of strings');
  }
  for (const a of cliArgs) {
    if (a.length > MAX_ARG_LEN || CONTROL_CHAR_RE.test(a)) {
      failWith('Internal error: cliArgs failed final safety check');
    }
  }

  const { cliEntry } = resolveAndVerifyPinnedPackage();

  // The imported module reads process.argv via commander's program.parse().
  // Inject our validated argv shape: [node, cliEntry, ...validated].
  process.argv = [process.execPath, cliEntry, ...cliArgs];

  try {
    await import(pathToFileURL(cliEntry).href);
  } catch (err) {
    failWith(
      `Failed to invoke ${PINNED_PACKAGE}: ${err && err.message ? err.message : err}`,
    );
  }
  // Do NOT call process.exit() here: commander action handlers may still be
  // running asynchronously. The upstream CLI is responsible for terminating
  // (or letting the event loop drain naturally on success).
}

const runWechatPub = safeRunWmp;

// ---------- Help ----------

function showHelp() {
  console.log(`WeChat Publisher - 使用说明

用法:
  publish <file> [theme]     - 发布文章
  draft <file> [theme]       - 创建草稿
  wrapper <args...>          - 透传 wrapper 子命令
  list-drafts                - 列出草稿
  list-published             - 列出已发布文章
  themes                     - 列出可用主题
  help                       - 显示帮助

安装（必须使用精确版本，启动器会在导入前校验 name/version）:
  npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION}

示例:
  publish article.md orangeheart
  draft article.md lapis
`);
}

// ---------- Dispatch ----------

async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  if (!action) {
    showHelp();
    process.exit(0);
  }

  if (!ACTIONS.has(action)) {
    showHelp();
    process.exit(0);
  }

  switch (action) {
    case 'publish': {
      if (!args[0]) {
        console.error('错误: 请提供文件路径');
        console.error('用法: publish <file> [theme]');
        process.exit(1);
      }
      const file = validateFilePath(args[0]);
      const theme = validateTheme(args[1] || 'default');
      console.log('正在发布文章...');
      await runWechatPub(['publish', 'create', '--file', file, '--theme', theme]);
      return;
    }

    case 'draft': {
      if (!args[0]) {
        console.error('错误: 请提供文件路径');
        console.error('用法: draft <file> [theme]');
        process.exit(1);
      }
      const file = validateFilePath(args[0]);
      const theme = validateTheme(args[1] || 'default');
      console.log('正在创建草稿...');
      await runWechatPub(['draft', 'create', '--file', file, '--theme', theme]);
      return;
    }

    case 'wrapper': {
      const passthrough = validatePassthroughArgs(args);
      await runWechatPub(['wrapper', ...passthrough]);
      return;
    }

    case 'list-drafts':
      console.log('草稿列表:');
      await runWechatPub(['draft', 'list']);
      return;

    case 'list-published':
      console.log('已发布文章:');
      await runWechatPub(['publish', 'list']);
      return;

    case 'themes':
      console.log('可用主题:');
      await runWechatPub(['theme', 'list']);
      return;

    case 'help':
    default:
      showHelp();
      return;
  }
}

main().catch((err) => {
  process.stderr.write(`[wmp-skill] fatal: ${err && err.message ? err.message : err}\n`);
  process.exit(1);
});
