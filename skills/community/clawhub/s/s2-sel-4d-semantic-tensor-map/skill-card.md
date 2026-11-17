## Description:

S2 Spatial Element Layer & 4D Semantic Tensor Map integrates L0-L4 spatial layers, material physics tensors, and Chronos backward-persistence time-slicing via S2-GeoJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to interpret S2-GeoJSON room layers, material tensor metadata, and Chronos time-slice fields when generating spatial-map guidance or parser-based intervention outputs. It should be treated as map-format guidance rather than an authoritative robot safety layer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Robot-navigation directives may be mistaken for an authoritative safety layer.

Mitigation: Treat the skill as experimental map-format guidance and require independent robotics safety validation before it influences sensors or movement.

Risk: Timestamp and schema assumptions may be used without real validation in downstream integrations.

Mitigation: Add explicit timestamp validation, schema checks, and integration constraints before using outputs in robotics workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-sel-4d-semantic-tensor-map)
- [ClawHub publisher profile](https://clawhub.ai/user/spacesq)
- [S2-SEL 4D Chronos whitepaper](artifact/docs/s2-sel-4d-chronos-whitepaper.md)
- [S2 material tensor library](artifact/data/s2_material_tensor_library.json)
- [Sample S2-GeoJSON room layers](artifact/examples/sample_room_layers.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python and JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce parser-derived intervention dictionaries for S2-GeoJSON features.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
