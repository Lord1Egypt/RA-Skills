## Description:

Parse schematics and netlists (Altium, Cadence, KiCad, EasyEDA, OrCAD, EAGLE, netlist.json) into pin-level netlists — query components, nets and connectivity, run ERC enumeration. Facts only; judgment left to the model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and electrical engineers use this skill to turn supported schematic and netlist files into structured component, net, connectivity, and ERC facts for an agent to inspect. It can also provide a limited text-label preview from vector PDFs; it does not assess design quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked this release suspicious based on reported purpose and behavior mismatches, heuristic judgments, and installation and execution risks; it says no clear malicious intent is established.

Mitigation: Install only if you need these capabilities and have reviewed the reported concerns.

Risk: ERC triage could hide findings, and the scan coverage is partial because some local references were unresolved.

Mitigation: Review ERC results against the original design and inspect relevant files before relying on triage or assuming unreported behavior is absent.

Risk: PDF probing may involve optional package installation, while the external MCP package and package mirror are unpinned.

Mitigation: Check whether PDF probing is needed and review the package source and mirror before allowing installation or networked execution.

## Reference(s):

- [ClawHub release](https://clawhub.ai/liujycode/skills/schematic-reader)
- [Publisher profile](https://clawhub.ai/user/liujycode)
- [Universal Netlist installer referenced by the skill](https://raw.githubusercontent.com/IntelligentElectron/universal-netlist/main/install.ps1)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Readable text or JSON containing component, net, connectivity, and ERC facts; PDF previews contain text labels and page information.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF previews do not contain connectivity; supported project formats provide different levels of detail.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
