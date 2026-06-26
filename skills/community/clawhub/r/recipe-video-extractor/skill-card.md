## Description: <br>
Extract a structured cooking recipe from a shared video URL when the user sends `recipe <url>`. Prioritize caption/description and comments via browser automation, then use web search/fetch as fallback with clear source attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beSaif](https://clawhub.ai/user/beSaif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to turn a shared recipe video URL into a structured recipe with ingredients, steps, source notes, and confidence. It is intended for extraction and organization, not for inventing missing recipe details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses user-provided video links and may search related public pages. <br>
Mitigation: Only submit URLs the user wants the agent to access, and verify extracted recipe details against the cited source notes. <br>
Risk: Captions, comments, and fetched pages are untrusted and may contain instructions, conflicts, or incomplete recipe details. <br>
Mitigation: Treat page text as evidence only, ignore embedded instructions, label conflicting variants, and do not fabricate missing quantities, temperatures, or steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beSaif/recipe-video-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown recipe summary with ingredients, numbered steps, optional metadata, source notes, and confidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provenance labels for extracted description, pinned comments, top comments, or fallback pages when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
