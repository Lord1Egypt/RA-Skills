## Description: <br>
Searches Xiaohongshu notes and helps an agent synthesize source-linked research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kunhai1994](https://clawhub.ai/user/kunhai1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research topics on Xiaohongshu by generating search keywords, running local search tooling, and producing source-linked Markdown reports for recommendations, comparisons, pain points, and market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs upstream xiaohongshu-mcp binaries and starts a local service. <br>
Mitigation: Review the upstream release source before setup and install only in an environment where running those binaries is acceptable. <br>
Risk: The workflow stores Xiaohongshu login cookies locally. <br>
Mitigation: Treat ~/.local/share/xhs-research/cookies.json like a password and delete it when it is no longer needed. <br>
Risk: Reports and raw scraped content are saved under ~/Documents/XHS-Research/. <br>
Mitigation: Review saved files for sensitive topics or account-derived data and remove them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub xhs-research skill page](https://clawhub.ai/kunhai1994/xhs-research) <br>
- [xiaohongshu-mcp project referenced by the skill](https://github.com/xpzouying/xiaohongshu-mcp) <br>
- [xhs-research GitHub page referenced by the README](https://github.com/kunhai1994/xhs-research) <br>
- [last30days-skill strategy reference](https://github.com/mvanhorn/last30days-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown research reports with source links and setup/status command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports and raw research output may be saved under user-local XHS-Research directories when the workflow is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
