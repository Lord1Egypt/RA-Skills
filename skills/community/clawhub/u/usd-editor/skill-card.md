## Description: <br>
Guide for modifying and reviewing USD ASCII (.usda) files, including prims, properties, composition arcs, variants, and transforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomkrikorian](https://clawhub.ai/user/tomkrikorian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical artists use this skill to make targeted .usda edits and review USD structure while preserving composition, paths, formatting, transforms, and property types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Following editing guidance or commands can change USD assets in ways that are difficult to undo. <br>
Mitigation: Keep important assets in version control or backups before applying changes, and use usdedit --noeffect when only inspecting a file. <br>
Risk: Incorrect paths, specifiers, composition arcs, transform order, or property types can break USD composition or downstream asset behavior. <br>
Mitigation: Inspect the stage before editing, make the smallest targeted change, preserve unrelated structure, and validate touched files with USD tools such as usdchecker. <br>


## Reference(s): <br>
- [USD Syntax Essentials](references/usd-syntax.md) <br>
- [Prims and Properties](references/prims-properties.md) <br>
- [Composition Arcs and Variants](references/composition-variants.md) <br>
- [Transforms and Units](references/transforms-units.md) <br>
- [Time Samples](references/time-samples.md) <br>
- [USD Command-Line Tools](references/command-line-tools.md) <br>
- [usdcat](references/usdcat.md) <br>
- [usdchecker](references/usdchecker.md) <br>
- [usdedit](references/usdedit.md) <br>
- [usdrecord](references/usdrecord.md) <br>
- [usdtree](references/usdtree.md) <br>
- [usdzip](references/usdzip.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with USD snippets and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include minimal .usda edits, validation steps, and USD command-line tool suggestions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
