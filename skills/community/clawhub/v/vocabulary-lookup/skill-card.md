## Description:

Looks up vocabulary details from a GPT-4 dictionary, including meanings, example sentences, roots, and memory aids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effeceee](https://clawhub.ai/user/effeceee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language-learning agents use this skill to query a local GPT-4 vocabulary dictionary for word definitions, examples, etymology, history, and memory aids.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional, unpinned edge-tts package install adds supply-chain exposure even though the lookup script does not require it for local dictionary reads.

Mitigation: Review or decline the optional edge-tts install unless audio output is needed and the dependency is trusted.

Risk: The lookup script reads the dictionary path supplied by the user or environment.

Mitigation: Configure the dictionary path only to local files intended for vocabulary lookup.

Risk: Users should expect Chinese-language vocabulary output.

Mitigation: Confirm the output language is appropriate for the target workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effeceee/skills/vocabulary-lookup)
- [Publisher profile](https://clawhub.ai/user/effeceee)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-formatted CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; requires a local dictionary file configured by command-line path, VOCABULARY_DICT_PATH, current directory, or skill directory.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
