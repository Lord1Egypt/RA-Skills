## Description: <br>
Guide users buying resistance training equipment - free weights, barbells, racks, cables, or machines - through space, load, safety, and goal questions to get the exact specs they need. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbazex](https://clawhub.ai/user/arbazex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to choose resistance training equipment for a purchase or upgrade by answering questions about goals, space, loading, safety, region, and equipment preferences. The agent produces brand-neutral specifications first, then a small set of product research starting points that match the confirmed requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Equipment recommendations can affect user safety and purchasing decisions if dimensions, load ratings, or local availability are stale or incomplete. <br>
Mitigation: Require users to verify current manufacturer specifications, floor loading constraints, safety mechanisms, warranty coverage, and regional certifications before purchase or installation. <br>
Risk: The skill can produce product research suggestions after specification gathering, which may be mistaken for endorsements. <br>
Mitigation: Keep product suggestions explicitly framed as research starting points and prioritize non-negotiable specifications over brand or model preference. <br>
Risk: Solo barbell training without appropriate safety mechanisms can create serious injury risk. <br>
Mitigation: Preserve the artifact guardrail that solo bench press and squat recommendations must include spotter arms, safety straps, Smith machine rails, or another suitable safety mechanism. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arbazex/resistance-training-equipment-buying-consultant) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown consultation with grouped questions, prioritized specification lists, and up to five product research suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Brand-neutral; no external APIs, environment variables, or runtime dependencies required] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
