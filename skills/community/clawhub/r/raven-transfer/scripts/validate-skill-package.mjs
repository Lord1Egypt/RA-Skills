#!/usr/bin/env node

import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));

const REQUIRED_FILES = [
  "SKILL.md",
  "agents/openai.yaml",
  "scripts/raven-transfer.mjs",
  "references/install.md",
  "references/commands.md",
  "references/workflow.md",
  "references/safety.md",
];

function checkRequiredFiles() {
  const missing = REQUIRED_FILES.filter((rel) => !existsSync(resolve(ROOT, rel)));
  return missing.map((file) => ({
    code: "missing_file",
    message: `Required artifact missing from bundle: ${file}`,
  }));
}

function checkPolicyAndEnvMetadata() {
  const issues = [];
  const openAiYamlPath = resolve(ROOT, "agents/openai.yaml");
  if (!existsSync(openAiYamlPath)) {
    return issues;
  }

  const yaml = readFileSync(openAiYamlPath, "utf8");
  if (!/allow_implicit_invocation:\s*false\b/.test(yaml)) {
    issues.push({
      code: "policy_mismatch",
      message: "agents/openai.yaml must set policy.allow_implicit_invocation: false",
    });
  }

  if (!/required:\s*\n\s*-\s*"RAVEN_API_KEY_FILE or RAVEN_API_KEY"/.test(yaml)) {
    issues.push({
      code: "env_required_missing",
      message: "agents/openai.yaml must declare required env: RAVEN_API_KEY_FILE or RAVEN_API_KEY",
    });
  }

  if (!/primary:\s*"RAVEN_API_KEY_FILE"/.test(yaml)) {
    issues.push({
      code: "env_primary_missing",
      message: "agents/openai.yaml must declare primary credential: RAVEN_API_KEY_FILE",
    });
  }

  return issues;
}

const findings = [...checkRequiredFiles(), ...checkPolicyAndEnvMetadata()];
const result = {
  ok: findings.length === 0,
  checked_root: ROOT,
  findings,
};

const out = JSON.stringify(result, null, 2);
if (result.ok) {
  console.log(out);
  process.exit(0);
}

console.error(out);
process.exit(1);
