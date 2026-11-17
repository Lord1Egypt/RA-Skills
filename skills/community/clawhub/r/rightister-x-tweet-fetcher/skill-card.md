## Description:

Fetches X/Twitter tweets, replies, timelines, X Lists, Chinese-platform content, Google search results, and tweet growth signals, with basic tweet fetching available without login or API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rightister](https://clawhub.ai/user/rightister)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve structured social-media content, monitor mentions or tweet growth, and integrate X/Twitter and supported Chinese-platform data into agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad outbound scraping and search behavior can access unexpected external or internal targets through the local browser helper.

Mitigation: Use only trusted URLs and queries, avoid cookies or sensitive searches, and restrict Camofox/browser access to intended destinations.

Risk: The security summary flags under-disclosed router command queuing and weak URL controls.

Mitigation: Disable or remove the router-agent fallback unless intentionally operating that external command queue and its home-network path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rightister/skills/rightister-x-tweet-fetcher)
- [Publisher Profile](https://clawhub.ai/user/rightister)
- [FxEmbed / FxTwitter](https://github.com/FxEmbed/FxEmbed)
- [Camoufox](https://camoufox.com)
- [Camofox Browser Plugin](https://github.com/jo-inc/camofox-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI and Python examples; fetched content is typically JSON, text, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some advanced workflows require a local Camofox browser service; basic single-tweet and tweet-growth workflows are documented as zero dependency.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
