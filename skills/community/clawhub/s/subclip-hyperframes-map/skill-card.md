## Description:

Build an editable HyperFrames map after the creator rejects both built-in Remotion map styles or explicitly requests HyperFrames. Use verified geographic geometry with custom SVG, GSAP camera motion, routes, and labels inside Subclip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill in Subclip to build editable animated maps when they explicitly request HyperFrames or reject both built-in map styles. It guides them to use verified coordinates and geography, then create and inspect a seekable map composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because a local path-like reference could not be resolved, so its referenced content was not assessed.

Mitigation: Verify that the referenced host skill is available and review it before relying on its guidance.

Risk: Unverified coordinates or invented geography could produce a misleading map.

Mitigation: Use verified coordinates and source geometry; report missing geographic data instead of approximating it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prosamik/skills/subclip-hyperframes-map)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions and editable HyperFrames HTML/CSS/GSAP source]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A seekable map composition with geographic paths, routes, labels, and camera motion.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
