import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = fileURLToPath(new URL("..", import.meta.url));

const files = [
  "README.md",
  "SKILL.md",
  "shared/templates/install-prompt.md",
];

const contents = Object.fromEntries(
  files.map((file) => [file, readFileSync(join(repoRoot, file), "utf8")]),
);

const failures = [];

for (const file of ["README.md", "shared/templates/install-prompt.md"]) {
  const text = contents[file];
  for (const phrase of [
    "Use the install document and live local checks as the source of truth.",
    "Do not search memory or prior notes for this install. Do not pre-load context from `MEMORY.md`, `crystal_search`, local skill dev guides, or other local memory before fetching the install document.",
    "Do not run GitHub commands during this install flow. Do not run or request approval for `gh release`, `gh api`, or `gh search`.",
    "If release notes are not available from local or npm metadata, say that and do not fetch them from GitHub.",
    "If installed: run `ldm status`",
    "check available npm tracks from the install document",
    "If yes to dry run, use the selected track's dry-run path from the install document.",
    "If I say install, use the selected track's install path from the install document, then run `ldm doctor`.",
    "install the CLI first using the selected track's bootstrap command from the install document",
    "Then run:\n`ldm init --dry-run`",
    "If I say install, run:\n`ldm init`",
  ]) {
    if (!text.includes(phrase)) {
      failures.push(`${file} missing install prompt phrase: ${phrase}`);
    }
  }
  if (text.includes("If it is, run ldm install --dry-run")) {
    failures.push(`${file} still tells installed users to start with ldm install --dry-run`);
  }
}

const skill = contents["SKILL.md"];
for (const phrase of [
  "Memory policy for install flows: do not consult `MEMORY.md`, do not run `crystal_search`, and do not search prior notes when this skill is invoked, including in any parallel or batched exploration step.",
  "The only context sources for this install flow are `https://wip.computer/install/wip-ldm-os.txt` and the live local commands that document prescribes.",
  "Read that document and run those commands. Do not pre-load other context.",
  "Do not run GitHub commands during the install-state flow.",
  "Do not run or request approval for `gh release list`, `gh release view`, `gh api repos/*`, `gh search`, or any other GitHub query unless the user explicitly asks for release notes.",
  "npm view @wipcomputer/wip-ldm-os dist-tags --json",
  "The README prompt should stay short. This install document owns the detailed track rules.",
  "stable/current/latest: `ldm install --dry-run`",
  "beta/latest beta: `ldm install --beta --dry-run`",
  "alpha/latest alpha: `ldm install --alpha --dry-run`",
  "beta/latest beta: `npm install -g @wipcomputer/wip-ldm-os@beta`",
  "alpha/latest alpha: `npm install -g @wipcomputer/wip-ldm-os@alpha`",
  "Use the output of `ldm status`, installed package metadata, and npm metadata.",
  "Do not use GitHub commands here.",
  "If npm metadata for a package does not include release notes:",
  "Say \"release notes not available from local metadata.\"",
  "Do not infer release-note content from package descriptions, commit messages, or repo READMEs.",
  "An approval dialog is not a user request.",
]) {
  if (!skill.includes(phrase)) {
    failures.push(`SKILL.md missing install policy phrase: ${phrase}`);
  }
}

if (/gh release (list|view) --repo/.test(skill)) {
  failures.push("SKILL.md still includes concrete gh release commands in the install flow");
}

const temporalMemoryPolicyPhrase = "your first action is " + "to fetch";
if (skill.includes(temporalMemoryPolicyPhrase)) {
  failures.push("SKILL.md still uses temporal first-action memory-policy phrasing");
}

if (failures.length > 0) {
  console.error("install prompt policy checks failed:");
  for (const failure of failures) console.error(`  - ${failure}`);
  process.exit(1);
}

console.log("install-prompt-policy: LDM OS prompt and install doc agree");
