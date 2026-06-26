## Description: <br>
中阿翻译工具。将中文词汇翻译成符合沙特当地使用习惯的阿拉伯语。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanwangfuhan-coder](https://clawhub.ai/user/freemanwangfuhan-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to translate supported Chinese product and shopping terms into Arabic phrasing intended for Saudi usage. It is best suited for quick offline dictionary lookups and batch translation of known built-in terms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The built-in dictionary has limited coverage, so unsupported Chinese terms may remain untranslated. <br>
Mitigation: Check output for the untranslated marker and verify important translations before use. <br>
Risk: The skill executes local JavaScript from a third-party publisher. <br>
Mitigation: Install only when the publisher is trusted and review the bundled files before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freemanwangfuhan-coder/zh-to-ar-translator) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text translation lines from a local Node.js command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline dictionary lookup; unsupported terms are returned with an untranslated marker.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
