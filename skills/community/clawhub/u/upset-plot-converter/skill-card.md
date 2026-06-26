## Description: <br>
Converts complex Venn diagrams with more than four sets into clearer Upset Plot visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data scientists use this skill to convert set or list inputs into readable Upset Plot PNGs when Venn diagrams with more than four sets become difficult to interpret. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python execution and plotting dependencies can introduce dependency hygiene risk. <br>
Mitigation: Install and run the skill in a normal sandboxed Python environment, and pin audited versions of matplotlib and numpy for production or repeated use. <br>
Risk: The plotting workflow writes output files to disk. <br>
Mitigation: Keep output paths inside the intended workspace and avoid elevated privileges when running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/upset-plot-converter) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PNG visualization with concise Markdown or command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes plot images to a user-specified output path; defaults include minimum subset size 1 and up to 30 intersections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
