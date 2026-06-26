## Description: <br>
Return Policy Generator. Use when you need return policy capabilities. Triggers on: return policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate return and refund policy text, HTML policy pages, Chinese-language policy text, and industry comparison output for stores or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated return and refund policy text may not match a business's actual obligations, jurisdictions, or product categories. <br>
Mitigation: Have a qualified reviewer check generated policy content before publishing or using it with customers. <br>
Risk: The helper may store entries and command history locally under ~/.local/share/return-policy when RETURN_POLICY_DIR is not set. <br>
Mitigation: Set RETURN_POLICY_DIR to an approved local path and avoid passing sensitive customer or order data into helper commands. <br>
Risk: The skill requires a shell and python3 to run its generator scripts. <br>
Mitigation: Install only in environments where shell execution and python3 are expected and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/return-policy) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [Source repository declared by artifact](https://github.com/bytesagain/ai-skills) <br>
- [Homepage declared by artifact](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or HTML printed to stdout, with command examples in Markdown documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script may write local history and data under RETURN_POLICY_DIR or ~/.local/share/return-policy.] <br>

## Skill Version(s): <br>
2.3.6 (source: server release evidence; artifact frontmatter and scripts declare 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
