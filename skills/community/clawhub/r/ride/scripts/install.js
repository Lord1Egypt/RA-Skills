#!/usr/bin/env node

// <define:__AMB_INSTALL_BUILD_CONFIG__>
var define_AMB_INSTALL_BUILD_CONFIG_default = { mode: "npm", repoBranch: "main", expectedCliSha: "ca68ea69", minimumCliVersion: "1.10.0" };

// src/scripts/install.ts
import os2 from "os";
import path3 from "path";
import fs2 from "fs";

// src/lib/install/cli-bootstrap.ts
import fs from "fs";
import path from "path";
import { execFileSync as nodeExecFileSync } from "child_process";
import os from "os";
import { randomBytes } from "crypto";

// src/lib/install/git-failure.ts
var GIT_STDERR_LIMIT = 2e3;
var SSH_KEY_REJECTION = /Permission denied \(publickey/i;
var GitCommandError = class extends Error {
  command;
  stderr;
  sshKeyRejection;
  constructor(command, stderr, options) {
    const sshKeyRejection = isSshKeyRejection(stderr);
    const truncated = stderr.slice(0, GIT_STDERR_LIMIT);
    super(`${command} failed: ${truncated}`, options);
    this.name = "GitCommandError";
    this.command = command;
    this.stderr = truncated;
    this.sshKeyRejection = sshKeyRejection;
  }
};
function isSshKeyRejection(stderr) {
  return SSH_KEY_REJECTION.test(stderr);
}
function stderrTextOf(e) {
  const stderr = e?.stderr;
  if (typeof stderr === "string" && stderr.length > 0) return stderr;
  if (e instanceof Error) return e.message;
  return String(e);
}
function describeGitFailure(e) {
  if (e instanceof GitCommandError) {
    return { command: e.command, stderr: e.stderr, sshKeyRejection: e.sshKeyRejection };
  }
  const full = stderrTextOf(e);
  return { command: "install", stderr: full.slice(0, GIT_STDERR_LIMIT), sshKeyRejection: isSshKeyRejection(full) };
}

// src/lib/install/cli-bootstrap.ts
function runGit(deps, command, args) {
  try {
    deps.execSync("git", args);
  } catch (e) {
    const stderr = stderrTextOf(e);
    process.stderr.write(stderr.endsWith("\n") ? stderr : `${stderr}
`);
    throw new GitCommandError(command, stderr, { cause: e });
  }
}
function ensureCliClone(opts) {
  const deps = opts.deps ?? {
    execSync: (file, args) => nodeExecFileSync(file, args, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] })
  };
  const gitDir = path.join(opts.cliDir, ".git");
  if (fs.existsSync(gitDir)) {
    runGit(deps, "git fetch", ["-C", opts.cliDir, "fetch"]);
    runGit(deps, "git reset --hard", ["-C", opts.cliDir, "reset", "--hard", `origin/${opts.branch}`]);
    return;
  }
  fs.mkdirSync(path.dirname(opts.cliDir), { recursive: true });
  runGit(deps, "git clone", ["clone", "-b", opts.branch, opts.repoUrl, opts.cliDir]);
}
var BOOTSTRAP_PREFIX = ".amb-cli-bootstrap-";
var OWNER_CLAIM = ".owner-claim.json";
var OWNER_ID_PATTERN = /^[0-9a-f]{32}$/;
function createCliBootstrap(ambientRoot) {
  const parent = path.dirname(ambientRoot);
  fs.mkdirSync(parent, { recursive: true });
  const bootstrapRoot = fs.mkdtempSync(path.join(parent, BOOTSTRAP_PREFIX));
  fs.writeFileSync(
    path.join(bootstrapRoot, OWNER_CLAIM),
    `${JSON.stringify({ schemaVersion: 1, ownerId: randomBytes(16).toString("hex") })}
`,
    { mode: 384, flag: "wx" }
  );
  return path.join(bootstrapRoot, "cli");
}
function validateBootstrapPath(stagedCliDir, ambientRoot) {
  const resolvedAmbient = path.resolve(ambientRoot);
  const resolvedStagedCliDir = path.resolve(stagedCliDir);
  const bootstrapRoot = path.dirname(resolvedStagedCliDir);
  const expectedParent = path.dirname(resolvedAmbient);
  if (path.basename(resolvedStagedCliDir) !== "cli" || path.dirname(bootstrapRoot) !== expectedParent || !path.basename(bootstrapRoot).startsWith(BOOTSTRAP_PREFIX)) {
    throw new Error(`unexpected CLI bootstrap path: ${stagedCliDir}`);
  }
  const rootStat = fs.lstatSync(bootstrapRoot);
  if (!rootStat.isDirectory() || rootStat.isSymbolicLink()) {
    throw new Error("bootstrap owner claim root is not a regular directory");
  }
  if (pathEntryExists(resolvedStagedCliDir)) {
    const stagedStat = fs.lstatSync(resolvedStagedCliDir);
    if (!stagedStat.isDirectory() || stagedStat.isSymbolicLink()) {
      throw new Error("bootstrap owner claim staged path is not a regular directory");
    }
  }
  const claimPath = path.join(bootstrapRoot, OWNER_CLAIM);
  let claimStat;
  try {
    claimStat = fs.lstatSync(claimPath);
  } catch {
    throw new Error("bootstrap owner claim is missing");
  }
  if (!claimStat.isFile() || claimStat.isSymbolicLink()) {
    throw new Error("bootstrap owner claim must be a regular file");
  }
  let claim;
  try {
    claim = JSON.parse(fs.readFileSync(claimPath, "utf8"));
  } catch {
    throw new Error("bootstrap owner claim is malformed");
  }
  if (typeof claim !== "object" || claim === null || Object.keys(claim).sort().join(",") !== "ownerId,schemaVersion" || claim.schemaVersion !== 1 || typeof claim.ownerId !== "string" || !OWNER_ID_PATTERN.test(claim.ownerId)) {
    throw new Error("bootstrap owner claim schema is invalid");
  }
  return { bootstrapRoot, ownerId: claim.ownerId };
}
function cleanupCliBootstrap(stagedCliDir, ambientRoot) {
  const { bootstrapRoot } = validateBootstrapPath(stagedCliDir, ambientRoot);
  fs.rmSync(bootstrapRoot, { recursive: true, force: true });
}
var TRANSACTION_KEYS = [
  "ambientRoot",
  "bootstrapOwnerId",
  "bootstrapRoot",
  "cliDir",
  "displacedCliDir",
  "displacedLinkPath",
  "hadExistingCli",
  "hadExistingLink",
  "linkPath",
  "markerPath",
  "phase",
  "schemaVersion",
  "stagedCliDir"
].sort();
var MAX_MARKER_BYTES = 64 * 1024;
var defaultMarkerIo = {
  openSync: fs.openSync,
  writeFileSync: fs.writeFileSync,
  fsyncSync: fs.fsyncSync,
  closeSync: fs.closeSync,
  renameSync: fs.renameSync,
  linkSync: fs.linkSync,
  rmSync: fs.rmSync
};
var CliPromotionRecoveryRequiredError = class extends Error {
  constructor(transaction, promotionError, rollbackError) {
    super(`CLI promotion recovery required: ${promotionError.message}; rollback failed: ${rollbackError.message}`);
    this.transaction = transaction;
    this.promotionError = promotionError;
    this.rollbackError = rollbackError;
    this.name = "CliPromotionRecoveryRequiredError";
  }
  transaction;
  promotionError;
  rollbackError;
};
function pathEntryExists(candidate) {
  try {
    fs.lstatSync(candidate);
    return true;
  } catch {
    return false;
  }
}
function validatePromotionOpts(opts) {
  const ambientRoot = path.resolve(opts.ambientRoot);
  if (path.resolve(opts.cliDir) !== path.join(ambientRoot, "cli")) {
    throw new Error(`managed CLI target is outside Ambient root: ${opts.cliDir}`);
  }
  return validateBootstrapPath(opts.stagedCliDir, ambientRoot);
}
function validateTransaction(transaction) {
  const { bootstrapRoot: computedBootstrapRoot, ownerId } = validatePromotionOpts(transaction);
  const ambientRoot = path.resolve(transaction.ambientRoot);
  const cliDir = path.resolve(transaction.cliDir);
  const linkPath = path.resolve(transaction.linkPath);
  const expectedMarkerPath = `${ambientRoot}.cli-promotion.json`;
  const cliPrefix = `${cliDir}.replaced-`;
  const resolvedDisplacedCli = path.resolve(transaction.displacedCliDir);
  const backupId = resolvedDisplacedCli.startsWith(cliPrefix) ? resolvedDisplacedCli.slice(cliPrefix.length) : "";
  if (transaction.schemaVersion !== 1 || !["prepared", "state-ready", "promoting"].includes(transaction.phase)) {
    throw new Error("CLI promotion transaction has invalid phase");
  }
  if (transaction.bootstrapRoot !== computedBootstrapRoot) {
    throw new Error("CLI promotion transaction has invalid bootstrap root");
  }
  if (transaction.bootstrapOwnerId !== ownerId) {
    throw new Error("CLI promotion transaction disagrees with bootstrap owner claim");
  }
  if (transaction.markerPath !== expectedMarkerPath) {
    throw new Error("CLI promotion transaction has invalid marker path");
  }
  if (backupId === "" || transaction.displacedCliDir !== `${cliDir}.replaced-${backupId}` || transaction.displacedLinkPath !== `${linkPath}.replaced-${backupId}`) {
    throw new Error("CLI promotion transaction has invalid backup paths");
  }
}
function fsyncParent(candidate, deps) {
  const fd = deps.openSync(path.dirname(candidate), "r");
  try {
    deps.fsyncSync(fd);
  } finally {
    deps.closeSync(fd);
  }
}
function persistCliTransaction(transaction, exclusive = false, deps = defaultMarkerIo) {
  validateTransaction(transaction);
  const payload = `${JSON.stringify(transaction)}
`;
  if (exclusive) {
    const tempPath2 = `${transaction.markerPath}.tmp-${randomBytes(16).toString("hex")}`;
    let fd2;
    try {
      fd2 = deps.openSync(tempPath2, fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL, 384);
      deps.writeFileSync(fd2, payload);
      deps.fsyncSync(fd2);
      deps.closeSync(fd2);
      fd2 = void 0;
      deps.linkSync(tempPath2, transaction.markerPath);
      fsyncParent(transaction.markerPath, deps);
    } catch (error) {
      if (fd2 !== void 0) {
        try {
          deps.closeSync(fd2);
        } catch {
        }
      }
      try {
        deps.rmSync(tempPath2, { force: true });
      } catch {
      }
      throw error;
    }
    try {
      deps.rmSync(tempPath2, { force: true });
    } catch {
    }
    return;
  }
  const tempPath = `${transaction.markerPath}.tmp-${randomBytes(16).toString("hex")}`;
  let fd;
  try {
    fd = deps.openSync(tempPath, fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL, 384);
    deps.writeFileSync(fd, payload);
    deps.fsyncSync(fd);
    deps.closeSync(fd);
    fd = void 0;
    deps.renameSync(tempPath, transaction.markerPath);
    fsyncParent(transaction.markerPath, deps);
  } catch (error) {
    if (fd !== void 0) {
      try {
        deps.closeSync(fd);
      } catch {
      }
    }
    try {
      deps.rmSync(tempPath, { force: true });
    } catch {
    }
    throw error;
  }
}
function removeDurableMarker(markerPath, deps = defaultMarkerIo) {
  deps.rmSync(markerPath, { force: true });
  fsyncParent(markerPath, deps);
}
function prepareCliPromotion(opts) {
  const { bootstrapRoot, ownerId } = validatePromotionOpts(opts);
  if (!fs.existsSync(path.join(opts.stagedCliDir, "amb"))) {
    throw new Error(`staged CLI is incomplete: ${opts.stagedCliDir}`);
  }
  const id = `${process.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  const transaction = {
    ...opts,
    schemaVersion: 1,
    phase: "prepared",
    markerPath: `${path.resolve(opts.ambientRoot)}.cli-promotion.json`,
    bootstrapRoot,
    bootstrapOwnerId: ownerId,
    displacedCliDir: `${opts.cliDir}.replaced-${id}`,
    displacedLinkPath: `${opts.linkPath}.replaced-${id}`,
    hadExistingCli: pathEntryExists(opts.cliDir),
    hadExistingLink: pathEntryExists(opts.linkPath)
  };
  persistCliTransaction(transaction, true);
  return transaction;
}
function markCliStateReady(transaction) {
  validateTransaction(transaction);
  transaction.phase = "state-ready";
  persistCliTransaction(transaction);
}
function loadCliPromotion(opts) {
  const markerPath = `${path.resolve(opts.ambientRoot)}.cli-promotion.json`;
  let markerStat;
  try {
    markerStat = fs.lstatSync(markerPath);
  } catch {
    return null;
  }
  if (!markerStat.isFile() || markerStat.isSymbolicLink() || markerStat.size <= 0 || markerStat.size > MAX_MARKER_BYTES || (markerStat.mode & 63) !== 0) {
    throw new Error("CLI promotion marker is not a sane private regular file");
  }
  const raw = JSON.parse(fs.readFileSync(markerPath, "utf8"));
  if (typeof raw !== "object" || raw === null || Object.keys(raw).sort().join(",") !== TRANSACTION_KEYS.join(",")) {
    throw new Error("CLI promotion marker schema keys are invalid");
  }
  const value = raw;
  const stringKeys = [
    "stagedCliDir",
    "cliDir",
    "ambientRoot",
    "linkPath",
    "markerPath",
    "bootstrapRoot",
    "bootstrapOwnerId",
    "displacedCliDir",
    "displacedLinkPath"
  ];
  if (value["schemaVersion"] !== 1 || !["prepared", "state-ready", "promoting"].includes(value["phase"]) || stringKeys.some((key) => typeof value[key] !== "string") || typeof value["hadExistingCli"] !== "boolean" || typeof value["hadExistingLink"] !== "boolean") {
    throw new Error("CLI promotion marker schema types are invalid");
  }
  const parsed = value;
  if (path.resolve(parsed.ambientRoot) !== path.resolve(opts.ambientRoot) || path.resolve(parsed.cliDir) !== path.resolve(opts.cliDir) || path.resolve(parsed.linkPath) !== path.resolve(opts.linkPath) || path.resolve(parsed.markerPath) !== markerPath) {
    throw new Error("CLI promotion recovery marker disagrees with managed paths");
  }
  validateTransaction(parsed);
  return parsed;
}
function promoteCliTransaction(transaction, deps = { rmSync: fs.rmSync, renameSync: fs.renameSync }) {
  validateTransaction(transaction);
  if (transaction.phase === "prepared") {
    throw new Error("CLI promotion state is not ready");
  }
  transaction.phase = "promoting";
  persistCliTransaction(transaction);
  fs.mkdirSync(path.dirname(transaction.cliDir), { recursive: true });
  fs.mkdirSync(path.dirname(transaction.linkPath), { recursive: true });
  if (transaction.hadExistingCli && !pathEntryExists(transaction.displacedCliDir)) {
    deps.renameSync(transaction.cliDir, transaction.displacedCliDir);
  }
  if (transaction.hadExistingLink && !pathEntryExists(transaction.displacedLinkPath)) {
    deps.renameSync(transaction.linkPath, transaction.displacedLinkPath);
  }
  if (pathEntryExists(transaction.stagedCliDir)) {
    deps.renameSync(transaction.stagedCliDir, transaction.cliDir);
  } else if (!fs.existsSync(path.join(transaction.cliDir, "amb"))) {
    throw new Error("forward promotion has neither staged nor managed CLI");
  }
}
function beginCliPromotion(opts, deps = { rmSync: fs.rmSync, renameSync: fs.renameSync }) {
  const transaction = prepareCliPromotion(opts);
  markCliStateReady(transaction);
  try {
    promoteCliTransaction(transaction, deps);
    return transaction;
  } catch (error) {
    try {
      rollbackCliPromotion(transaction, deps);
    } catch (rollbackError) {
      throw new CliPromotionRecoveryRequiredError(
        transaction,
        error,
        rollbackError
      );
    }
    throw error;
  }
}
function commitCliPromotion(transaction, markerDeps = defaultMarkerIo) {
  validateTransaction(transaction);
  removeDurableMarker(transaction.markerPath, markerDeps);
  try {
    if (transaction.hadExistingCli) fs.rmSync(transaction.displacedCliDir, { recursive: true, force: true });
    if (transaction.hadExistingLink) fs.rmSync(transaction.displacedLinkPath, { recursive: true, force: true });
    fs.rmSync(transaction.bootstrapRoot, { recursive: true, force: true });
  } catch {
  }
}
function rollbackCliPromotion(transaction, deps = { rmSync: fs.rmSync, renameSync: fs.renameSync }, markerDeps = defaultMarkerIo) {
  validateTransaction(transaction);
  if (transaction.hadExistingCli) {
    if (pathEntryExists(transaction.displacedCliDir)) {
      deps.rmSync(transaction.cliDir, { recursive: true, force: true });
      deps.renameSync(transaction.displacedCliDir, transaction.cliDir);
    }
  } else {
    deps.rmSync(transaction.cliDir, { recursive: true, force: true });
  }
  if (transaction.hadExistingLink) {
    if (pathEntryExists(transaction.displacedLinkPath)) {
      if (pathEntryExists(transaction.linkPath)) deps.rmSync(transaction.linkPath, { recursive: true, force: true });
      deps.renameSync(transaction.displacedLinkPath, transaction.linkPath);
    }
  } else if (pathEntryExists(transaction.linkPath)) {
    deps.rmSync(transaction.linkPath, { recursive: true, force: true });
  }
  removeDurableMarker(transaction.markerPath, markerDeps);
  try {
    deps.rmSync(transaction.bootstrapRoot, { recursive: true, force: true });
  } catch {
  }
}
function recoverCliPromotion(opts) {
  const parsed = loadCliPromotion(opts);
  if (parsed) rollbackCliPromotion(parsed);
}
function ensureSymlink(opts) {
  fs.chmodSync(opts.src, 493);
  fs.mkdirSync(path.dirname(opts.dst), { recursive: true });
  try {
    fs.unlinkSync(opts.dst);
  } catch {
  }
  fs.symlinkSync(opts.src, opts.dst);
}
function checkPath(targetDir, pathEnv, home = os.homedir()) {
  const expanded = targetDir.startsWith("~/") ? path.join(home, targetDir.slice(2)) : path.resolve(targetDir);
  const segs = pathEnv.split(":").map((s) => path.resolve(s.replace(/^~\//, home + "/")));
  return segs.includes(expanded);
}

// src/lib/install/cli-verify.ts
function parseVersionLine(line) {
  const trimmed = line.trim();
  const obj = JSON.parse(trimmed);
  if (typeof obj.version !== "string" || typeof obj.git_sha !== "string") {
    throw new Error(`amb --version returned unexpected shape: ${trimmed}`);
  }
  return obj;
}
function cmpSemver(a, b) {
  const parse = (value) => {
    const match = /^(\d+)\.(\d+)\.(\d+)$/.exec(value);
    if (!match) throw new Error(`invalid semantic version: ${value}`);
    return [Number(match[1]), Number(match[2]), Number(match[3])];
  };
  const pa = parse(a);
  const pb = parse(b);
  for (let i = 0; i < 3; i++) {
    const da = pa[i] ?? 0;
    const db = pb[i] ?? 0;
    if (da < db) return -1;
    if (da > db) return 1;
  }
  return 0;
}
function check(opts, version, git_sha) {
  if (opts.mode === "git") {
    if (git_sha === opts.expectedSha) return { ok: true };
    return {
      ok: false,
      error: "SHA_MISMATCH",
      message: `expected git_sha=${opts.expectedSha}, actual git_sha=${git_sha} (version=${version})`
    };
  }
  if (cmpSemver(version, opts.minVersion) >= 0) return { ok: true };
  return {
    ok: false,
    error: "VERSION_MISMATCH",
    message: `expected version >= ${opts.minVersion}, actual version=${version}`
  };
}
function verifyCli(opts) {
  const out1 = opts.deps.runVersion();
  const v1 = parseVersionLine(out1);
  const r1 = check(opts, v1.version, v1.git_sha);
  if (r1.ok) return r1;
  opts.deps.runRetry();
  const out2 = opts.deps.runVersion();
  const v2 = parseVersionLine(out2);
  return check(opts, v2.version, v2.git_sha);
}

// src/lib/install/managed-amb-command.ts
import { spawnSync } from "child_process";

// src/lib/core/fixed-executable-env.ts
import { accessSync, constants, statSync } from "fs";
import path2 from "path";
function fixedExecutableEnv(name, selected, env = process.env) {
  const errorCode = name === "amb" ? "AMB_EXECUTABLE_INVALID" : "RELAY_EXECUTABLE_INVALID";
  const executable = path2.resolve(selected);
  const directory = path2.dirname(executable);
  if (path2.basename(executable) !== name || directory.includes(path2.delimiter) || executable.includes("\0")) {
    throw new Error(`${errorCode}: expected an executable named ${name}`);
  }
  if (!statSync(executable).isFile()) throw new Error(`${errorCode}: not a regular file`);
  accessSync(executable, constants.X_OK);
  return { ...env, PATH: [directory, ...env.PATH ? [env.PATH] : []].join(path2.delimiter) };
}

// src/lib/install/managed-amb-command.ts
function managedAmbEnv(selected) {
  return selected === "amb" ? { ...process.env } : fixedExecutableEnv("amb", selected);
}
function runManagedAmbVersion(selected) {
  return spawnSync("amb", ["--version", "--json"], { shell: false, encoding: "utf8", env: managedAmbEnv(selected) });
}
function runManagedAmbInstall(selected) {
  return spawnSync("amb", ["install"], { shell: false, encoding: "utf8", env: managedAmbEnv(selected) });
}

// src/lib/install/cli-install-delegate.ts
function delegateAmbInstall(opts = {}) {
  const ambCmd = opts.ambCmd ?? "amb";
  const deps = opts.deps ?? {
    spawnSync: () => runManagedAmbInstall(ambCmd)
  };
  const result = deps.spawnSync();
  const code = result.status;
  if (code === 0) {
    return { ok: true, stdout: result.stdout ?? "" };
  }
  const spawnError = result.error;
  const message = (result.stderr ?? "").trim() || (spawnError ? `amb spawn failed: ${spawnError.message}` : `amb install exited with code ${code}`);
  return {
    ok: false,
    error: "AMB_INSTALL_FAILED",
    message
  };
}

// src/lib/install/errors.ts
function writeFatalError(error, message) {
  const flat = message.replace(/\s*[\r\n]+\s*/g, " ");
  process.stderr.write(JSON.stringify({ error, message: flat }) + "\n");
}

// src/lib/install/node-version.ts
var MINIMUM_NODE_VERSION = "22.22.0";
function supportsNodeVersion(version) {
  const match = /^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$/.exec(version);
  if (!match) return false;
  const major = Number(match[1]);
  const minor = Number(match[2]);
  const patch = Number(match[3]);
  const prerelease = match[4];
  if (major !== 22) return major > 22;
  if (minor !== 22) return minor > 22;
  return patch > 0 || patch === 0 && prerelease === void 0;
}
function unsupportedNodeVersionMessage(version) {
  return `Node.js ${MINIMUM_NODE_VERSION} or newer is required; found ${version}. Upgrade Node.js and run the installer again.`;
}

// src/scripts/install.ts
import { execFileSync as nodeExecFileSync2, spawnSync as nodeSpawnSync } from "child_process";

// src/lib/build/amb-install-build-config.ts
var testConfig;
function ambInstallBuildConfig() {
  return testConfig ?? define_AMB_INSTALL_BUILD_CONFIG_default;
}

// src/lib/core/main-module.ts
import { realpathSync } from "fs";
import { pathToFileURL } from "url";
function isMainModule(importMetaUrl) {
  const entry = process.argv[1];
  if (!entry) return false;
  try {
    return importMetaUrl === pathToFileURL(realpathSync(entry)).href;
  } catch {
    return false;
  }
}

// src/scripts/install.ts
var NPM_PACKAGE = "@ambprotocol/ride-cli";
var SYMLINK_DIR = "~/.local/bin";
var SYMLINK_TARGET = "amb";
function defaultDeps() {
  return {
    nodeVersion: process.versions.node,
    createCliBootstrap,
    ensureCliClone,
    beginCliPromotion,
    prepareCliPromotion,
    markCliStateReady,
    loadCliPromotion,
    promoteCliTransaction,
    commitCliPromotion,
    recoverCliPromotion,
    rollbackCliPromotion,
    cleanupCliBootstrap,
    ensureSymlink,
    checkPath,
    verifyCli,
    delegateAmbInstall: (ambCmd) => delegateAmbInstall({ ambCmd }),
    // Intentional: npm registers the bin via package.json, so we don't need a
    // separate symlink step in npm mode. installNpm is one shell call only.
    installNpm: () => {
      nodeExecFileSync2("npm", ["i", "-g", `${NPM_PACKAGE}@latest`], { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"] });
    },
    installDeps: (cliDir) => {
      nodeExecFileSync2("npm", ["install", "--omit=dev", "--silent"], {
        cwd: cliDir,
        encoding: "utf8",
        stdio: ["ignore", "pipe", "inherit"]
      });
    },
    resolveAmb: () => {
      const r = nodeSpawnSync("which", ["amb"], { encoding: "utf8" });
      if (r.status === 0 && r.stdout.trim() !== "") return r.stdout.trim();
      return null;
    },
    npmGlobalBinDir: () => {
      try {
        const prefix = nodeExecFileSync2("npm", ["config", "get", "prefix"], { encoding: "utf8" }).trim();
        if (prefix === "") return null;
        return path3.join(prefix, "bin");
      } catch {
        return null;
      }
    },
    realpath: (candidate) => {
      try {
        return fs2.realpathSync(candidate);
      } catch {
        return null;
      }
    }
  };
}
function expandHome(p) {
  if (p.startsWith("~/")) return path3.join(process.env["HOME"] ?? os2.homedir(), p.slice(2));
  return p;
}
function reportGitFailure(e) {
  const failure = describeGitFailure(e);
  writeFatalError(
    failure.sshKeyRejection ? "SSH_KEY_MISSING" : "AMB_INSTALL_FAILED",
    `${failure.command} failed: ${failure.stderr}`
  );
}
async function runInstall(depsOverride) {
  const deps = depsOverride ?? defaultDeps();
  if (!supportsNodeVersion(deps.nodeVersion)) {
    writeFatalError(
      "AMB_INSTALL_FAILED",
      unsupportedNodeVersionMessage(deps.nodeVersion)
    );
    return 1;
  }
  const install = ambInstallBuildConfig();
  const mode = install.mode;
  const branch = install.repoBranch;
  const repoUrl = install.mode === "git" ? install.repoUrl : void 0;
  const expectedSha = install.expectedCliSha;
  const minVersion = install.minimumCliVersion;
  const cliDir = expandHome("~/.amb/cli");
  const binDir = expandHome(SYMLINK_DIR);
  const linkPath = path3.join(binDir, SYMLINK_TARGET);
  let managedAmb = path3.join(cliDir, "amb");
  let stagedCliDir = null;
  let promotion = null;
  const ambientRoot = expandHome("~/.amb");
  const cleanupStaging = () => {
    if (!stagedCliDir) return;
    try {
      deps.cleanupCliBootstrap(stagedCliDir, ambientRoot);
    } catch (cleanupError) {
      process.stderr.write(`[amb-install] bootstrap cleanup failed: ${cleanupError.message}
`);
    }
  };
  if (mode === "git" && !deps.checkPath(SYMLINK_DIR, process.env["PATH"] ?? "")) {
    writeFatalError(
      "PATH_MISSING",
      `~/.local/bin is not in $PATH. Add 'export PATH="$HOME/.local/bin:$PATH"' to your shell profile (.bashrc / .zshrc) and reopen the shell.`
    );
    return 1;
  }
  if (mode === "git") {
    try {
      promotion = deps.loadCliPromotion({ ambientRoot, cliDir, linkPath });
      if (promotion) {
        stagedCliDir = promotion.stagedCliDir;
        managedAmb = fs2.existsSync(path3.join(stagedCliDir, "amb")) ? path3.join(stagedCliDir, "amb") : path3.join(cliDir, "amb");
      }
    } catch (e) {
      writeFatalError("AMB_INSTALL_FAILED", `CLI promotion recovery failed: ${e.message}`);
      return 1;
    }
    const resolved = deps.resolveAmb();
    if (resolved) {
      const resolvedRealpath = deps.realpath(resolved);
      const existingManagedRealpath = deps.realpath(managedAmb);
      if (path3.resolve(resolved) !== path3.resolve(managedAmb) && (!resolvedRealpath || !existingManagedRealpath || resolvedRealpath !== existingManagedRealpath)) {
        writeFatalError("PATH_MISSING", `'amb' on $PATH is not the managed CLI at ${managedAmb}. Put ~/.local/bin before other PATH entries.`);
        return 1;
      }
    }
  }
  if (mode === "git") {
    if (!promotion) {
      try {
        stagedCliDir = deps.createCliBootstrap(ambientRoot);
      } catch (e) {
        writeFatalError("AMB_INSTALL_FAILED", `CLI bootstrap allocation failed: ${e.message}`);
        return 1;
      }
      managedAmb = path3.join(stagedCliDir, "amb");
      try {
        deps.ensureCliClone({ cliDir: stagedCliDir, branch, repoUrl });
      } catch (e) {
        cleanupStaging();
        reportGitFailure(e);
        return 1;
      }
    }
    try {
      if (!promotion) deps.installDeps(stagedCliDir);
    } catch (e) {
      cleanupStaging();
      writeFatalError("AMB_INSTALL_FAILED", `npm install --omit=dev failed: ${e.message}`);
      return 1;
    }
  } else {
    try {
      deps.installNpm();
    } catch (e) {
      writeFatalError("AMB_INSTALL_FAILED", `npm install failed: ${e.message}`);
      return 1;
    }
    const npmBin = deps.npmGlobalBinDir();
    if (!npmBin) {
      writeFatalError("PATH_MISSING", `Cannot locate npm's global bin dir. Run 'npm config get prefix', append /bin, and add it to your $PATH.`);
      return 1;
    }
    managedAmb = path3.join(npmBin, "amb");
  }
  if (mode === "npm") {
    const resolved = deps.resolveAmb();
    const managedRealpath = deps.realpath(managedAmb);
    const resolvedRealpath = resolved ? deps.realpath(resolved) : null;
    if (!resolved || !managedRealpath || resolvedRealpath !== managedRealpath) {
      const npmBin = deps.npmGlobalBinDir();
      const hint = npmBin ? `'amb' on $PATH is not the managed CLI. Put "${npmBin}" before other PATH entries.` : `'amb' is not on your $PATH after 'npm i -g'. Find npm's global bin dir with 'npm config get prefix' (append /bin), add it to your $PATH in your .bashrc / .zshrc, then reopen the shell.`;
      writeFatalError("PATH_MISSING", hint);
      return 1;
    }
  }
  let verify;
  try {
    verify = deps.verifyCli({
      mode,
      expectedSha,
      minVersion,
      deps: {
        runVersion: () => {
          const r = runManagedAmbVersion(managedAmb);
          if (r.error) {
            throw new Error(`amb --version spawn failed: ${r.error.message}`);
          }
          if (r.status !== 0) {
            throw new Error(`amb --version exited ${r.status}: ${r.stderr}`);
          }
          return r.stdout;
        },
        runRetry: () => {
          if (mode === "git") {
            deps.ensureCliClone({ cliDir: stagedCliDir, branch, repoUrl });
          } else {
            deps.installNpm();
          }
        }
      }
    });
  } catch (e) {
    if (!promotion) cleanupStaging();
    if (e instanceof GitCommandError) {
      reportGitFailure(e);
      return 1;
    }
    writeFatalError("SHA_MISMATCH", `amb --version unparseable or spawn failed: ${e.message}`);
    return 1;
  }
  if (!verify.ok) {
    if (!promotion) cleanupStaging();
    writeFatalError(verify.error, verify.message);
    return 1;
  }
  if (mode === "git" && !promotion) {
    try {
      promotion = deps.prepareCliPromotion({ stagedCliDir, cliDir, ambientRoot, linkPath });
    } catch (e) {
      writeFatalError("AMB_INSTALL_FAILED", `CLI promotion prepare failed: ${e.message}`);
      return 1;
    }
  }
  let delegated;
  try {
    delegated = await deps.delegateAmbInstall(managedAmb);
  } catch (e) {
    writeFatalError("AMB_INSTALL_FAILED", `amb install invocation failed: ${e.message}`);
    return 1;
  }
  if (!delegated.ok) {
    writeFatalError(delegated.error, delegated.message);
    return 1;
  }
  if (mode === "git") {
    try {
      deps.markCliStateReady(promotion);
      deps.promoteCliTransaction(promotion);
      managedAmb = path3.join(cliDir, "amb");
      deps.ensureSymlink({ src: managedAmb, dst: linkPath });
    } catch (e) {
      writeFatalError("SYMLINK_FAILED", e.message);
      return 1;
    }
    const resolved = deps.resolveAmb();
    const managedRealpath = deps.realpath(managedAmb);
    const resolvedRealpath = resolved ? deps.realpath(resolved) : null;
    if (!resolved || !managedRealpath || resolvedRealpath !== managedRealpath) {
      writeFatalError("PATH_MISSING", `'amb' on $PATH is not the managed CLI at ${managedAmb}. Put ~/.local/bin before other PATH entries.`);
      return 1;
    }
    try {
      deps.commitCliPromotion(promotion);
    } catch (e) {
      writeFatalError("AMB_INSTALL_FAILED", `CLI promotion commit failed: ${e.message}`);
      return 1;
    }
    stagedCliDir = null;
    promotion = null;
  }
  process.stdout.write(delegated.stdout);
  return 0;
}
if (isMainModule(import.meta.url)) {
  runInstall().then((code) => process.exit(code));
}
export {
  runInstall
};
