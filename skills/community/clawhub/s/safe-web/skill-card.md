## Description:

Safe-Web fetches and searches web content, scans retrieved text with PromptGuard, and blocks content or results that match prompt-injection threat patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamnaghs](https://clawhub.ai/user/adamnaghs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use Safe-Web when untrusted web pages or search results need to enter an AI context with local prompt-injection scanning first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch any URL reachable from the local machine, including internal or sensitive network addresses.

Mitigation: Run it in a restricted network environment and review requested URLs before allowing fetched content into an agent workflow.

Risk: The documented setup can alter system Python packages and create a system-wide command.

Mitigation: Install dependencies in a virtual environment with pinned versions and create a symlink only when system-wide access is required.

Risk: Search sends the query and Brave API key to Brave when the search command is used.

Mitigation: Use the search command only for queries suitable for Brave Search and manage the API key as a secret.

## Reference(s):

- [Safe-Web ClawHub page](https://clawhub.ai/adamnaghs/skills/safe-web)
- [PromptGuard dependency](https://clawhub.ai/seojoonkim/prompt-guard)
- [Brave Search API](https://brave.com/search/api/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON command output, with optional saved text files for clean fetched content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch returns extracted page text or a security alert; search returns scanned result summaries and can filter suspicious entries.]

## Skill Version(s):

1.0.8 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
