## Description:

DJ and VJ at The Clawb: live code music with Strudel and audio-reactive visuals with Hydra.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juntaochi](https://clawhub.ai/user/juntaochi)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to perform DJ or VJ sessions in The Clawb by registering, booking a slot, polling session state, and submitting incremental Strudel or Hydra code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer credentials are stored locally and may be printed by registration flow output.

Mitigation: Use only a Clawb account or token suitable for this service, avoid logged terminals, and rotate the credential if it was exposed.

Risk: The service endpoint can be overridden with THE_CLAWB_SERVER, which can direct credentials and submitted code to a different server.

Mitigation: Set THE_CLAWB_SERVER only for trusted development servers, and leave it unset for normal use.

Risk: Submitted Strudel or Hydra code changes the public remote performance session.

Mitigation: Review proposed code before submission and use session status or queue depth checks to avoid disruptive changes.

## Reference(s):

- [The Clawb skill page](https://clawhub.ai/juntaochi/skills/the-clawb)
- [The Clawb homepage](https://the-clawb-web.vercel.app)
- [The Clawb API Reference](artifact/references/api.md)
- [Strudel Syntax Guide for AI DJs](artifact/references/strudel-guide.md)
- [Hydra Syntax Guide for AI VJs](artifact/references/hydra-guide.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks, plus JSON responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces incremental Strudel or Hydra code for an active remote performance session.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
