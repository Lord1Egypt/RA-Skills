import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const skill = fs.readFileSync(path.join(root, "SKILL.md"), "utf8");
const readme = fs.readFileSync(path.join(root, "README.md"), "utf8");
const references = fs.readFileSync(path.join(root, "references", "source-of-truth.md"), "utf8");

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function assertIncludes(haystack, needle, message) {
  if (!haystack.includes(needle)) {
    fail(message);
  }
}

function assertOrdered(haystack, needles, message) {
  let cursor = -1;
  for (const needle of needles) {
    const next = haystack.indexOf(needle, cursor + 1);
    if (next === -1) {
      fail(message);
    }
    cursor = next;
  }
}

assertOrdered(
  skill,
  ["sx auth", "sx project use", "sx event", "sx artifact add", "sx status", "sx brief"],
  "primary command order must remain sx auth -> sx project use -> sx event -> sx artifact add -> sx status -> sx brief"
);

assertIncludes(
  skill,
  "Only use `sx project list` when the user does not have the `projectId` yet or needs to recover it from shared projects.",
  "skill must keep sx project list as recovery-only guidance"
);

assertIncludes(
  skill,
  "The default path is always browser-approved `sx auth`.",
  "skill must keep browser-approved sx auth as the default path"
);

assertIncludes(
  skill,
  "Do not ask users to paste tokens into chat.",
  "skill must explicitly warn against token paste into chat"
);

assertIncludes(
  skill,
  "Do not use this skill for broad SprintX task management, review workflows, project creation, or generic natural-language control.",
  "skill must preserve the thin handoff boundary"
);

assertIncludes(
  readme,
  "manual ClawHub publish",
  "README must document manual publish"
);

assertIncludes(
  readme,
  "clawhub publish .",
  "README must use the working top-level clawhub publish command"
);

assertIncludes(
  references,
  "https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart",
  "references must include the public handoff quickstart"
);

assertIncludes(
  references,
  "https://raw.githubusercontent.com/openclaw/clawhub/main/docs/skill-format.md",
  "references must include ClawHub skill format docs"
);

console.log("Instruction contract checks passed.");
