## Description: <br>
Turns a person's existing materials, answers, or optional interview into a concise Personal OS: a Markdown persona document for AI agents and a polished HTML personal homepage for humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaohuadavidlee](https://clawhub.ai/user/shaohuadavidlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals, creators, founders, and collaborators use this skill to distill public materials, private answers, or an optional interview into reusable identity and collaboration assets. Agents use it to produce a persona file for AI assistance and a human-facing personal homepage while preserving explicit privacy boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary notes that the skill includes copyable installation guidance for cloning an unpinned GitHub skill into a persistent agent directory. <br>
Mitigation: Prefer the reviewed ClawHub package, or inspect and pin the repository before allowing an agent to clone it into a persistent skills directory. <br>
Risk: The skill processes broad personal context and can turn it into shareable persona and homepage outputs. <br>
Mitigation: Provide only intended materials, remove secrets and confidential employer or third-party data, and manually review or redact generated persona, homepage, and card links before sharing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shaohuadavidlee/simaqian-skill) <br>
- [Output Specification](artifact/references/output-spec.md) <br>
- [Intake and Interview Framework](artifact/references/intake-and-interview.md) <br>
- [Skill README](artifact/README.md) <br>
- [Live Experience](https://simaqian.caojuege.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown persona document and single-file HTML homepage, with optional interview questions and revision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default outputs are persona-agent.md and personal-homepage.html; generated content should distinguish facts, inferences, unknowns, and public/private boundaries.] <br>

## Skill Version(s): <br>
1.3.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
