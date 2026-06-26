## Description: <br>
Voice Match Humanizer helps agents build local writing voice profiles from user-provided samples, score AI-like patterns, and rewrite text to match a saved profile while preserving meaning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, creators, and teams use this skill to create reusable local voice profiles from their own samples, rewrite drafts into an established personal voice, compare profiles, and check for voice drift or AI-like writing patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writing samples and voice profiles may contain unpublished drafts, internal documents, or personal correspondence. <br>
Mitigation: Use only samples the user provides or explicitly points to, keep profile files local, and avoid quoting large sample excerpts in shareable outputs. <br>
Risk: Generated rewrites or profile updates may change meaning, tone, or attribution in ways the user did not intend. <br>
Mitigation: Review rewritten text, comparison reports, drift reports, and saved profile changes before publishing or relying on them. <br>
Risk: AI-pattern scoring and rewriting could be misused for detector evasion in academic-integrity contexts. <br>
Mitigation: Follow the documented refusal scope for detector-evasion requests and keep the workflow framed around legitimate personal voice matching. <br>
Risk: Local profile writes can overwrite or update existing voice profiles. <br>
Mitigation: Confirm the intended profile name and update target before saving changes under profiles/. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chris-openclaw/voice-match-humanizer) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports, rewritten text, and local markdown voice profile files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Profiles are written under a local profiles/ directory; sample handling is local-only according to the artifact documentation.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, release evidence, CHANGELOG released 2026-06-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
