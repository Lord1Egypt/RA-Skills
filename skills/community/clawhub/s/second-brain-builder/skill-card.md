## Description: <br>
Expand, compile, and write back a user's second-brain notes around a knowledge point with concept definitions, lineage, related concepts, reading recommendations, and AI-annotated note edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to research a concept, connect it to existing local notes, create a bounded concept packet, and optionally write annotated additions back to a second-brain vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search and modify local second-brain notes when the user asks for writeback. <br>
Mitigation: Set SECOND_BRAIN_WIKI_ROOT or SECOND_BRAIN_ROOT to the intended vault, request a preview or diff before edits, and verify that generated additions are visibly AI-annotated. <br>
Risk: Concept origin, reading recommendations, or lineage claims may be wrong if sources are weak or ambiguous. <br>
Mitigation: Use primary or high-quality sources for origin and reading-list claims, and mark uncertainty directly in the generated annotation when evidence is limited. <br>
Risk: Writeback could clutter a knowledge graph by expanding too many related concepts at once. <br>
Mitigation: Keep the first pass bounded to one central concept, a curated related-concept set, and a short reading path; expand additional topics only when explicitly requested. <br>


## Reference(s): <br>
- [Research Packet](references/research-packet.md) <br>
- [Writeback Policy](references/writeback-policy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/second-brain-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with optional shell commands and file-change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local note files when the user explicitly asks for writeback; additions are expected to be visibly AI-annotated.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
