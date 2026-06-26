## Description: <br>
Taobao Image Search helps an agent use a product image to search Taobao for similar items, compare candidates, and optionally add a selected item to the shopping cart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lazygunner](https://clawhub.ai/user/lazygunner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to search Taobao from a local product image, review similar product candidates, and add an explicitly requested item to the cart. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default flow can use a saved Taobao login session to add items to a real shopping cart without a separate confirmation step. <br>
Mitigation: Run only on a trusted machine and instruct the agent to stop after search or comparison unless you explicitly want a specific item added to the cart. <br>
Risk: Browser session artifacts may contain active Taobao login tokens. <br>
Mitigation: Treat saved storage and profile artifacts as sensitive credentials and delete them after use. <br>
Risk: Images supplied to the skill are uploaded to Taobao during image search. <br>
Mitigation: Provide only images you intend to upload to Taobao. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lazygunner/taobao-image-search) <br>
- [Publisher profile](https://clawhub.ai/user/lazygunner) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON results, logs, and screenshots from the automation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local verification artifacts, including result.json, run-log.txt, screenshots, and browser storage state.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
