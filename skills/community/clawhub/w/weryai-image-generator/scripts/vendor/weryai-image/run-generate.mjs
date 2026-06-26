#!/usr/bin/env node
import path from "node:path";
import process from "node:process";
import { spawnSync } from "node:child_process";
import { resolveRuntimeContext } from "./runtime-context.mjs";

function hasProjectArg(args) {
  return args.some((arg) => arg === "--project" || arg.startsWith("--project="));
}

const [entryArg, ...forwardedArgs] = process.argv.slice(2);
if (!entryArg) {
  console.error("Usage: node ./run-generate.mjs <entry-script> [generate args...]");
  process.exit(1);
}

const entryScript = path.resolve(process.cwd(), entryArg);
const runtime = resolveRuntimeContext({
  argv: forwardedArgs,
  cwd: process.cwd(),
  skillDir: process.cwd(),
  packageJsonPath: process.env.npm_package_json,
  packageName: process.env.npm_package_name,
  explicitSkillNamespace: process.env.IMAGE_SKILL_NAMESPACE,
  envProjectRoot: process.env.IMAGE_PROJECT_ROOT,
  initCwd: process.env.INIT_CWD,
});
const projectRoot = runtime.projectRoot;
const skillNamespace = runtime.skillNamespace;
const args = hasProjectArg(forwardedArgs)
  ? forwardedArgs
  : [...forwardedArgs, "--project", projectRoot];

const npxCommand = process.platform === "win32" ? "npx.cmd" : "npx";
const result = spawnSync(npxCommand, ["-y", "bun", entryScript, ...args], {
  stdio: "inherit",
  env: {
    ...process.env,
    IMAGE_PROJECT_ROOT: projectRoot,
    IMAGE_SKILL_NAMESPACE: skillNamespace || process.env.IMAGE_SKILL_NAMESPACE,
    IMAGE_SKILL_LABEL: process.env.IMAGE_SKILL_LABEL || skillNamespace,
    IMAGE_SKILL_DIR: runtime.skillDir,
    INIT_CWD: process.env.INIT_CWD || projectRoot,
  },
});

process.exit(result.status ?? 1);
