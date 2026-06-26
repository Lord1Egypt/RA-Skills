## Description: <br>
Looks up English vocabulary details from a local GPT-4 dictionary, including meanings, examples, roots, memory aids, and related learning notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[effeceee](https://clawhub.ai/user/effeceee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and language-learning users can use this skill to query a configured local vocabulary dictionary for word definitions, examples, roots, history, memory tips, and short bilingual learning material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The lookup content depends on the local dictionary file selected by --dict-path, VOCABULARY_DICT_PATH, or default file locations. <br>
Mitigation: Use a trusted dictionary file and point --dict-path only at the intended vocabulary data. <br>
Risk: The optional edge-tts package is a third-party dependency if installed. <br>
Mitigation: Install optional dependencies only from trusted package sources and review them under the same process used for other third-party packages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/effeceee/vocabulary-lookup) <br>
- [Publisher Profile](https://clawhub.ai/user/effeceee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-formatted vocabulary entries and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and a trusted local dictionary file; edge-tts is documented as an optional package.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
