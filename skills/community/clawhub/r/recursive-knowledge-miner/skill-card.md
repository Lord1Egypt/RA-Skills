## Description: <br>
Professional multi-layered knowledge extraction and recursive knowledge graph construction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askxiaozhang](https://clawhub.ai/user/askxiaozhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, educators, and knowledge-management teams use this skill to convert complex professional text into a structured, graph-ready hierarchy of concepts, entities, and relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated entities or relationships may be incomplete, misleading, or too broad for the source material. <br>
Mitigation: Use bounded source material and review the generated graph before treating it as authoritative. <br>
Risk: Recursive expansion can duplicate concepts if existing terms are not supplied or checked carefully. <br>
Mitigation: Provide known entity IDs through existing_terms when available and verify reused IDs during review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/askxiaozhang/recursive-knowledge-miner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON object containing a natural-language reply plus entities and relations for a knowledge graph.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Entity groups use core, primary, and detail layers; relationship labels are concise active-verb descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
