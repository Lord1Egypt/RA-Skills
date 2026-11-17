## Description:

Cut your LLM costs by 200x. Offload parallel, batch, and research work to Gemini Flash workers instead of burning your expensive primary model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chair4ce](https://clawhub.ai/user/chair4ce)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Swarm to split independent prompts, research tasks, batch analyses, long-form drafting, structured extraction, and majority-vote checks across parallel LLM workers while tracking cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated local daemon can expose paid provider API use if port 9999 is reachable by untrusted clients.

Mitigation: Run it only in a controlled local environment, keep port 9999 off untrusted networks, and use provider-side spending limits.

Risk: Cached LLM responses may retain sensitive prompt or response content on disk.

Mitigation: Disable caching for sensitive work, protect the cache directory, and clear the cache when handling confidential prompts.

Risk: Curl-to-bash or unpinned installation can execute code before review.

Mitigation: Inspect the source first, pin the expected release, and install only when the publisher is trusted.

## Reference(s):

- [ClawHub Swarm skill page](https://clawhub.ai/chair4ce/skills/swarm)
- [Swarm project homepage](https://github.com/Chair4ce/node-scaling)
- [README](artifact/README.md)
- [Install guide](artifact/INSTALL.md)
- [Swarm Roadmap](artifact/docs/ROADMAP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, command-line output, and streaming text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include web-grounded research, structured JSON, benchmark scores, cost metrics, cache statistics, and daemon status.]

## Skill Version(s):

1.3.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
