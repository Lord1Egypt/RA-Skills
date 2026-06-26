import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const skillPath = path.join(root, "SKILL.md");
const licensePath = path.join(root, "LICENSE");

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

if (!fs.existsSync(skillPath)) {
  fail("SKILL.md not found");
}

const skill = fs.readFileSync(skillPath, "utf8");
const frontmatterMatch = skill.match(/^---\n([\s\S]*?)\n---\n/);

if (!frontmatterMatch) {
  fail("Missing YAML frontmatter");
}

const frontmatter = frontmatterMatch[1];

const requiredChecks = [
  [/^name:\s*sprintx-openclaw-handoff$/m, "name must be sprintx-openclaw-handoff"],
  [/^description:\s*.+$/m, "description is required"],
  [/^version:\s*\d+\.\d+\.\d+$/m, "version must be semver"],
  [/^metadata:\s*$/m, "metadata block is required"],
  [/^\s+openclaw:\s*$/m, "metadata.openclaw block is required"],
  [/^\s+requires:\s*$/m, "metadata.openclaw.requires block is required"],
  [/^\s+bins:\s*$/m, "requires.bins block is required"],
  [/^\s+-\s+sx$/m, "requires.bins must declare sx"],
  [/^\s+install:\s*$/m, "install block is required"],
  [/^\s+-\s+kind:\s+node$/m, "install must declare node kind"],
  [/^\s+package:\s+"@sprint-x\/cli"$/m, "install must declare @sprint-x/cli"],
  [/^\s+homepage:\s+https:\/\/www\.sprintx\.co\.kr\/docs\/getting-started\/openclaw-handoff-quickstart$/m, "homepage must point to the public handoff quickstart"]
];

for (const [pattern, message] of requiredChecks) {
  if (!pattern.test(frontmatter)) {
    fail(message);
  }
}

if (!fs.existsSync(licensePath)) {
  fail("LICENSE not found");
}

const license = fs.readFileSync(licensePath, "utf8");
if (!license.includes("MIT No Attribution")) {
  fail("LICENSE must be MIT-0 / MIT No Attribution");
}

console.log("SKILL frontmatter and license checks passed.");
