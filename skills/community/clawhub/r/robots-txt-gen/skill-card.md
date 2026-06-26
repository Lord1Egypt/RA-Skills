## Description: <br>
Generate, validate, and analyze robots.txt files for websites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to create robots.txt files from common platform presets, validate local or remote robots.txt content, and check whether a URL is allowed for a selected user-agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script can read local robots.txt files, fetch remote robots.txt URLs, and write generated output to a user-specified path. <br>
Mitigation: Double-check file paths, remote URLs, and output destinations before running commands. <br>
Risk: Generated crawl directives can affect how search engines and other crawlers access a website. <br>
Mitigation: Review generated robots.txt content before publishing it to a production site. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Johnnywang2001/robots-txt-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text robots.txt content, command-line status messages, and validation warnings or errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated robots.txt content may be printed to stdout or written to a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
