## Description:

Automates collection, filtering, digest generation, and export of publicly available social media posts across major platforms, with compliance guidance for platform terms and privacy laws.

This skill is ready for commercial/non-commercial use.

## Publisher:

[10oss](https://clawhub.ai/user/10oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to collect public social media posts, filter them by query or engagement, generate digests, and export results to files or note-taking tools. Users should confirm each platform's terms, rate limits, and privacy obligations before collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported scraped content can become local commands in note-app export paths.

Mitigation: Review or fix exporter command construction before installing; avoid Bear and Apple Notes exports when processing untrusted public posts until command handling is safe.

Risk: Browser automation and bot-evasion guidance may conflict with platform terms or trigger enforcement.

Mitigation: Prefer official platform APIs where available, respect robots.txt and rate limits, and stop collection when access is blocked.

Risk: The documented --dry-run spelling may not activate the script's dryRun option.

Mitigation: Do not rely on dry-run behavior until option parsing is corrected and tested.

Risk: External CLI dependencies and note-app integrations can affect local data or accounts.

Mitigation: Pin and review external tools before use and test exports with non-sensitive data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/10oss/skills/skroller)
- [Platform Details](references/platform-details.md)
- [Rate Limits & Best Practices](references/rate-limits.md)
- [CSS Selector Reference](assets/selector-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated JSON, CSV, Markdown, HTML, ENEX, and note-app exports from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local files, screenshots, dedupe state, and note-app exports depending on command options.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
