## Description: <br>
Turn questionnaire items into clean research codebooks, scoring rules, reverse-scoring checks, variable names, and analysis-ready TSV/Markdown tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mia956](https://clawhub.ai/user/mia956) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and analysts use this skill to convert questionnaire items into codebooks, variable maps, scoring rules, reverse-scoring checks, and QC notes for psychology, education, public-health, and social-science workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script writes codebook.md and variable_map.tsv into the chosen output directory, which can replace existing files with those names. <br>
Mitigation: Choose an output directory where overwriting codebook.md and variable_map.tsv is acceptable. <br>
Risk: Questionnaire CSV files may contain confidential survey content or participant-related information. <br>
Mitigation: Process only CSV files intended for this workflow and avoid shared folders for confidential survey data unless sharing is intended. <br>
Risk: Incorrect or ambiguous questionnaire scoring can lead to misleading codebooks or analysis variables. <br>
Mitigation: Use the skill's QC checklist and keep uncertain reverse-scoring or cutoff decisions marked for review instead of inventing rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mia956/questionnaire-codebook-maker-mia956) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, TSV tables, and optional local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional helper script reads a user-supplied CSV and writes codebook.md and variable_map.tsv to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
