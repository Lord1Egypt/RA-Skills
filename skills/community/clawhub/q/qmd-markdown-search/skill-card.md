## Description: <br>
Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emcmillan80](https://clawhub.ai/user/emcmillan80) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other agent users use this skill to search, retrieve, and maintain indexed local Markdown notes, documentation, and knowledge bases. It helps agents choose fast keyword search by default and escalate to semantic or hybrid search only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install path uses Bun to install an external qmd tool. <br>
Mitigation: Install only after reviewing and trusting the upstream qmd project and the Bun-based install command. <br>
Risk: Broad collections can index private Markdown notes or sensitive documents. <br>
Mitigation: Index only folders intended for agent search, and exclude secrets or highly private notes from qmd collections. <br>
Risk: Automated indexing or embedding refreshes can keep sensitive or unintended content searchable. <br>
Mitigation: Enable scheduled updates deliberately and periodically review configured qmd collections. <br>
Risk: Semantic and hybrid search modes can be slow on cold start because local models may need to load or download. <br>
Mitigation: Use qmd search by default, reserve qmd vsearch or qmd query for cases where keyword search is insufficient, and account for first-run model setup. <br>


## Reference(s): <br>
- [QMD ClawHub release](https://clawhub.ai/emcmillan80/qmd-markdown-search) <br>
- [qmd project homepage](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide JSON-formatted qmd search and retrieval commands when the user or agent needs structured results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
