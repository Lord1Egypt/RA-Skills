## Description: <br>
Generates TOEFL iBT speaking practice sets by selecting varied academic or campus topics and producing four progressive interview questions with stored reference answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saikewei](https://clawhub.ai/user/saikewei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
TOEFL learners and study coaches use this skill to generate varied speaking interview practice, review reference answers, and request feedback on spoken-response quality across fluency, vocabulary, grammar, and content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated questions, reference answers, topic history, and dated archives may remain in local files under toefl/. <br>
Mitigation: Delete the local toefl/ folder when study history should not be retained, and avoid putting sensitive personal material in practice answers. <br>
Risk: The generated TOEFL material is practice content and may not reflect official exam guidance. <br>
Mitigation: Use the output as study practice and confirm official requirements against ETS or other authoritative TOEFL materials. <br>


## Reference(s): <br>
- [prompt-template.md](prompt-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown practice questions with hidden reference answers and JSON topic history] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores latest questions, answers, topic history, and dated archives under the local toefl/ folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
