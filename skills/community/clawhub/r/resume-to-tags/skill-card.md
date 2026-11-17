## Description:

Resume To Tags helps agents turn resume text or files into normalized talent tags, expand synonyms, and structure the results for a searchable Feishu talent tag table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sourcers, and HR operations teams use this skill to extract standardized candidate tags from resumes and create a searchable Feishu talent tag matrix for matching roles to candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes resumes and may expose sensitive candidate data, including contact details and employment history.

Mitigation: Use only resumes you are allowed to process, avoid retaining unnecessary contact details, and apply the organization's candidate-data handling policy before sharing outputs.

Risk: LLM-generated tags can be inaccurate, overbroad, or biased if imported without review.

Mitigation: Review and validate extracted tags against source resumes before using them for screening, matching, or Feishu import.

Risk: The workflow can create, delete, or batch-import Feishu table fields and records.

Mitigation: Confirm the target Feishu app and table, then inspect planned create, delete, and batch import actions before execution.

## Reference(s):

- [Synonym mapping reference](references/synonyms.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tag extraction output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve Feishu table creation and batch record import when the agent has appropriate tool access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
