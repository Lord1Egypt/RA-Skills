# Video Asset Gap Audit

Check approved shots against available assets before production and receive an actionable coverage table: covered shots, missing assets, spec mismatches, and items that still need verification. File names alone never count as evidence.

## Input and output

Provide one video's approved shot list (up to 30 shots) and asset inventory (up to 50 assets). A shot needs content, aspect ratio, and duration. An asset also needs content, usable duration, and license status. The Markdown delivery includes per-shot evidence, missing or mismatched requirements, and confirmation gaps.

Copyable fixtures: [success input](fixtures/success.json), [failure input](fixtures/failure.json), [success delivery](fixtures/success.expected.md), and [failure delivery](fixtures/failure.expected.md).

```bash
npx skills add xxjrq/video-asset-gap-audit-cn
node scripts/self-test.mjs
node scripts/audit.mjs fixtures/success.json /tmp/gap-audit.md
```

Coverage requires identical content and aspect ratio, enough duration, and an `owned` or `cleared` license. Missing content, duration, or license is reported as needing confirmation. This Skill audits coverage only; it does not download or generate assets, create storyboards, or schedule production.

## License and source note

The business use was informed by [agentara/skills](https://github.com/agentara/skills/blob/main/skills/aigc/video-storyboard/SKILL.md). This repository's text, code, and fixtures are original and licensed under [MIT-0](LICENSE).
