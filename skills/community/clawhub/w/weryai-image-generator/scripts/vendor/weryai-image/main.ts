#!/usr/bin/env bun
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { resolveRuntimeContext } from "./runtime-context.mjs";

const sharedScript = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../shared-image-generation/scripts/main.ts");
const runtime = resolveRuntimeContext({
  argv: process.argv.slice(2),
  cwd: process.cwd(),
  skillDir: process.env.IMAGE_SKILL_DIR,
  packageJsonPath: process.env.npm_package_json,
  packageName: process.env.npm_package_name,
  explicitSkillNamespace: process.env.IMAGE_SKILL_NAMESPACE,
  envProjectRoot: process.env.IMAGE_PROJECT_ROOT,
  initCwd: process.env.INIT_CWD,
  fallbackSkillNamespace: "image-generation-2",
});
const packageName = process.env.npm_package_name?.trim();
const skillNamespace = runtime.skillNamespace;
const result = spawnSync(process.execPath, [sharedScript, ...process.argv.slice(2)], {
  stdio: "inherit",
  env: {
    ...process.env,
    IMAGE_PROJECT_ROOT: runtime.projectRoot,
    IMAGE_SKILL_NAMESPACE: skillNamespace,
    IMAGE_SKILL_LABEL: process.env.IMAGE_SKILL_LABEL?.trim() || packageName || skillNamespace,
    IMAGE_SKILL_DIR: runtime.skillDir,
  },
});

process.exit(result.status ?? 1);
