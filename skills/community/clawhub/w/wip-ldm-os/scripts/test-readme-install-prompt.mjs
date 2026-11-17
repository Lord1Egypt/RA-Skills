import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const readme = readFileSync(new URL("../README.md", import.meta.url), "utf8");
const promptTemplate = readFileSync(
  new URL("../shared/templates/install-prompt.md", import.meta.url),
  "utf8",
);
const skill = readFileSync(new URL("../SKILL.md", import.meta.url), "utf8");

const promptStart = readme.indexOf("Read https://wip.computer/install/wip-ldm-os.txt");
const promptEnd = readme.indexOf("```", promptStart);

assert(promptStart >= 0, "README install prompt must point at the public install document");
assert(promptEnd > promptStart, "README install prompt must be fenced");

const readmePrompt = readme.slice(promptStart, promptEnd);

for (const [label, prompt] of [
  ["README install prompt", readmePrompt],
  ["shared install prompt template", promptTemplate],
]) {
  assert(
    prompt.includes("Read https://wip.computer/install/wip-ldm-os.txt"),
    `${label} must delegate to the public install document`,
  );

  assert(
    prompt.includes("Use the install document and live local checks as the source of truth."),
    `${label} must name the install document as source of truth`,
  );

  assert(
    prompt.includes("use the selected track's dry-run path from the install document"),
    `${label} must delegate dry-run command mapping to SKILL.md`,
  );

  assert(
    prompt.includes("use the selected track's install path from the install document"),
    `${label} must delegate install command mapping to SKILL.md`,
  );

  for (const forbidden of [
    "Track choices:",
    "ldm install --alpha",
    "ldm install --beta",
    "ldm install --dry-run",
  ]) {
    assert(!prompt.includes(forbidden), `${label} must not include ${forbidden}`);
  }
}

for (const required of [
  "## Tracks",
  "npm view @wipcomputer/wip-ldm-os dist-tags --json",
  "stable/current/latest: `ldm install --dry-run`",
  "beta/latest beta: `ldm install --beta --dry-run`",
  "alpha/latest alpha: `ldm install --alpha --dry-run`",
  "beta/latest beta: `npm install -g @wipcomputer/wip-ldm-os@beta`",
  "alpha/latest alpha: `npm install -g @wipcomputer/wip-ldm-os@alpha`",
  "The README prompt should stay short. This install document owns the detailed track rules.",
]) {
  assert(skill.includes(required), `SKILL.md must own track-selection logic: ${required}`);
}

console.log("readme-install-prompt: prompt stays short and delegates track rules to SKILL.md");
