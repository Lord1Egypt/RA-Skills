#!/usr/bin/env node

const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const DEFAULT_PACKAGE = "superpowers-ai";
const DEFAULT_CACHE = path.join(os.tmpdir(), "superpowers-npm-cache");
const PACKAGE_NPM_URL = "https://www.npmjs.com/package/superpowers-ai";
const PACKAGE_PUBLISHER = "superpowersai";
const PACKAGE_MAINTAINER_EMAIL = "rohan@getsupers.com";
const SKILL_ROOT = path.resolve(__dirname, "..");
const STATE_ROOT = path.join(SKILL_ROOT, ".superpowers");
const INSTALL_ROOT = path.join(STATE_ROOT, "npm");
const LOCAL_PACKAGE_ROOT = path.join(INSTALL_ROOT, "node_modules", DEFAULT_PACKAGE);
const LOCAL_ENTRYPOINT = path.join(LOCAL_PACKAGE_ROOT, "bin", "supers.js");

function printHelp() {
  console.log(`SuperPowers ClawHub helper

Usage:
  node scripts/install_and_run.js
  node scripts/install_and_run.js --install-only
  node scripts/install_and_run.js --start
  node scripts/install_and_run.js --stop
  node scripts/install_and_run.js --whoami
  node scripts/install_and_run.js --logout

Options:
  --install-only   Install the npm package locally and stop
  --start          Start the streamer instead of running login
  --stop           Stop the locally installed streamer
  --whoami         Show the saved account from the local install
  --logout         Remove the saved login from the local install
  --help           Show this help

This helper installs a published third-party npm package and runs its CLI
inside this skill's .superpowers state directory using your current npm config
and normal local permissions. It does not perform a global npm install.

Expected package provenance:
  npm page: ${PACKAGE_NPM_URL}
  npm publisher: ${PACKAGE_PUBLISHER}
  maintainer email: ${PACKAGE_MAINTAINER_EMAIL}

Local install path:
  ${INSTALL_ROOT}
`);
}

function parseArgs(argv) {
  const options = {
    action: "login",
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      options.action = "help";
    } else if (arg === "--install-only") {
      options.action = "install";
    } else if (arg === "--start") {
      options.action = "start";
    } else if (arg === "--stop") {
      options.action = "stop";
    } else if (arg === "--whoami") {
      options.action = "whoami";
    } else if (arg === "--logout") {
      options.action = "logout";
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return options;
}

function commandName(base) {
  return process.platform === "win32" ? `${base}.cmd` : base;
}

function run(command, args, extraEnv = {}) {
  const result = spawnSync(command, args, {
    stdio: "inherit",
    env: { ...process.env, ...extraEnv },
  });

  if (result.error) {
    throw result.error;
  }

  return result.status || 0;
}

function ensureCommand(name) {
  const result = spawnSync(commandName(name), ["--version"], {
    stdio: "ignore",
    env: process.env,
  });
  return result.status === 0;
}

function installPackage() {
  fs.mkdirSync(INSTALL_ROOT, { recursive: true });
  console.log(`Expected package provenance:
  package: ${DEFAULT_PACKAGE}
  npm page: ${PACKAGE_NPM_URL}
  npm publisher: ${PACKAGE_PUBLISHER}
  maintainer email: ${PACKAGE_MAINTAINER_EMAIL}`);
  console.log(`Installing ${DEFAULT_PACKAGE} into ${INSTALL_ROOT}...`);
  let status = run(commandName("npm"), [
    "install",
    "--prefix",
    INSTALL_ROOT,
    "--no-audit",
    "--no-fund",
    DEFAULT_PACKAGE
  ]);
  if (status === 0) {
    return;
  }

  console.log(`Retrying install with temp npm cache at ${DEFAULT_CACHE}...`);
  status = run(
    commandName("npm"),
    [
      "install",
      "--prefix",
      INSTALL_ROOT,
      "--no-audit",
      "--no-fund",
      DEFAULT_PACKAGE
    ],
    { npm_config_cache: DEFAULT_CACHE },
  );
  if (status !== 0) {
    process.exit(status);
  }
}

function ensureLocalPackageInstalled() {
  if (fs.existsSync(LOCAL_ENTRYPOINT)) {
    return;
  }
  console.error("The local SuperPowers package is not installed yet.");
  console.error(`Run: node ${path.relative(process.cwd(), path.join(__dirname, "install_and_run.js"))} --install-only`);
  process.exit(1);
}

function runLocalCLI(args) {
  ensureLocalPackageInstalled();
  process.exit(run(commandName("node"), [LOCAL_ENTRYPOINT, ...args]));
}

function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    printHelp();
    process.exit(1);
  }

  if (options.action === "help") {
    printHelp();
    return;
  }

  if (!ensureCommand("node")) {
    console.error("Node.js is required but was not found on PATH.");
    process.exit(1);
  }

  if (!ensureCommand("npm")) {
    console.error("npm is required but was not found on PATH.");
    process.exit(1);
  }

  installPackage();

  if (options.action === "install") {
    console.log("Local install complete.");
    return;
  }

  const args = options.action === "start"
    ? ["start"]
    : options.action === "stop"
      ? ["stop"]
      : options.action === "whoami"
        ? ["whoami"]
        : options.action === "logout"
          ? ["logout"]
          : ["login"];
  runLocalCLI(args);
}

main();
