## Description: <br>
Downloads high-quality anime images from Safebooru by tag search and saves them as local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litousteven](https://clawhub.ai/user/litousteven) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search Safebooru by tags, download matching safe-content anime images, and receive local file paths for downstream personal or workflow use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded images may carry copyright or platform-use restrictions. <br>
Mitigation: Review image rights and any destination platform rules before reusing or sharing downloaded files. <br>
Risk: The tool writes image files to the local output directory selected by the user. <br>
Mitigation: Choose the --out directory deliberately and review downloaded files before using them in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litousteven/safebooru-fetcher) <br>
- [Publisher profile](https://clawhub.ai/user/litousteven) <br>
- [Safebooru](https://safebooru.org) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [Downloaded image files with printed local file paths and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes files to a local output directory, defaulting to ./downloads; supports tag suggestions, sorting, pagination, exclusions, and minimum score filters.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
