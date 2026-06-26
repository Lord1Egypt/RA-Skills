import assert from "node:assert/strict";
import test from "node:test";

import {
  compactDescription,
  parseLiveSkillsPrompt,
  plainLogSkillReads,
  referencedSkillPaths,
  usageEvidence,
} from "./skill-cleaner.ts";

test("parses Codex skill roots and model-visible lines", () => {
  const raw = JSON.stringify([
    {
      role: "developer",
      content: [{
        type: "input_text",
        text: `<skills_instructions>
## Skills
### Skill roots
- \`r0\` = \`/tmp/skills\`
### Available skills
- demo: Demo work. (file: r0/demo/SKILL.md)
### How to use skills
</skills_instructions>`,
      }],
    },
  ]);

  const parsed = parseLiveSkillsPrompt(raw);
  assert.equal(parsed.roots.get("r0"), "/tmp/skills");
  assert.deepEqual(parsed.skillLines, [
    "- demo: Demo work. (file: r0/demo/SKILL.md)",
  ]);
});

test("compacts prose into a readable trigger phrase", () => {
  const compact = compactDescription(
    "Use this skill when the user wants to inspect calendars, compare availability, review conflicts, and schedule a meeting with timezone-aware details.",
    90,
  );
  assert.equal(
    compact,
    "inspect calendars, compare availability, review conflicts, and schedule a meeting with...",
  );
  assert.ok(compact.length <= 90);
  assert.doesNotMatch(compact, /audit, clean, verify/);
});

test("extracts user evidence without counting developer prompt listings", () => {
  assert.deepEqual(
    usageEvidence({ session_id: "abc", text: "use $skill-cleaner", ts: 123 }),
    { userText: "use $skill-cleaner" },
  );
  assert.deepEqual(
    usageEvidence({
      type: "response_item",
      payload: {
        type: "function_call",
        arguments: "{\"cmd\":\"cat /tmp/skills/demo/SKILL.md\"}",
      },
    }),
    { callArgs: "{\"cmd\":\"cat /tmp/skills/demo/SKILL.md\"}" },
  );
  assert.deepEqual(
    usageEvidence({
      type: "response_item",
      payload: { type: "message", role: "developer", content: ["$skill-cleaner"] },
    }),
    {},
  );
});

test("resolves relative skill reads from function-call workdirs", () => {
  assert.deepEqual(
    referencedSkillPaths(JSON.stringify({
      cmd: "cat skills/demo/SKILL.md",
      workdir: "/tmp/repo",
    })),
    ["/tmp/repo/skills/demo/SKILL.md"],
  );
});

test("counts command-like plain-log reads but ignores rendered listings", () => {
  assert.deepEqual(
    plainLogSkillReads([
      "cat skills/demo/SKILL.md",
      "- other: description (file: /tmp/skills/other/SKILL.md)",
    ].join("\n")),
    ["demo"],
  );
});
