## Description: <br>
Generates black or white SVG text and symbol compositions from Font Awesome glyphs or user-provided SVG symbols, with sequence, permutation, Cartesian-product, and limited-length batch modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to compose SVG glyphs, icons, logos, badges, and batch-generated symbol sets from text or custom SVG inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch modes can generate large numbers of SVG files, especially Cartesian-product combinations. <br>
Mitigation: Start with small input sets and explicit output directories, then scale batch size deliberately. <br>
Risk: Generated preview HTML can expose local output paths through file links if shared. <br>
Mitigation: Use preview HTML locally and remove or avoid sharing files that reveal sensitive local paths. <br>
Risk: Custom SVG symbol loading reads local SVG files from a user-selected folder. <br>
Mitigation: Load symbols only from intended local directories and review generated outputs before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/svg-composer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ldxs001) <br>
- [Font Awesome Free license](https://fontawesome.com/license/free) <br>
- [tscircuit alphabet source](https://github.com/tscircuit/alphabet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and generated SVG or HTML file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SVG strings and batch files may include Font Awesome attribution comments; optional preview HTML can include local file links.] <br>

## Skill Version(s): <br>
3.2.2 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
