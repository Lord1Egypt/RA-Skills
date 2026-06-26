## Description: <br>
Batch Chinese text processing for cleaning, normalization, keyword extraction, and repeated text operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huizong-cpu](https://clawhub.ai/user/huizong-cpu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, developers, and automation pipelines use this skill to clean mixed Chinese and English text, normalize punctuation and character width, extract simple Chinese keyword candidates, and batch-process repeated text items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect advertised translation or richer format-conversion behavior that is not present in the inspected code. <br>
Mitigation: Treat the release as local cleaning, normalization, keyword extraction, and batch text processing unless unsupported features are separately verified. <br>
Risk: Frequency-based Chinese keyword extraction can return approximate or noisy keyword candidates. <br>
Mitigation: Review extracted keywords before using them in publishing, search, tagging, or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huizong-cpu/text-processor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code] <br>
**Output Format:** [Strings and JavaScript arrays returned by local module functions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local processing only; batch mode maps one operation across one or more input text items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
