## Description:

Fetches skills.sh trending rankings. Use when asking about skill rankings or popular tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjw21century](https://clawhub.ai/user/hjw21century)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to fetch current skills.sh trending rankings and, when optional dependencies are installed, summarize individual skill details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs live network and browser-based fetches whose scope may be too broad for sensitive environments.

Mitigation: Run it in an isolated environment with limited filesystem and network access, and keep SKILLS_BASE_URL restricted to trusted values.

Risk: The rankings fetcher launches Playwright Chromium with no-sandbox flags.

Mitigation: Review the browser sandbox configuration before running it on sensitive hosts or in privileged contexts.

Risk: Installation steps are not pinned and may produce non-reproducible dependency or browser versions.

Mitigation: Pin Playwright, Chromium, and optional parsing dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjw21century/skills/trending-skills)
- [skills.sh](https://skills.sh)
- [skills.sh trending rankings](https://skills.sh/trending)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and summaries with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live public skills.sh data; detail lookups may require optional packages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
