## Description: <br>
Generate URL-friendly slugs from English and Chinese text by removing invalid characters and converting supported Chinese characters to pinyin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and site operators use this skill to generate URL-safe slugs for blogs, e-commerce pages, CMS entries, and permalinks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chinese pinyin coverage is limited to the script's built-in character map, so some inputs may produce incomplete or unexpected slugs. <br>
Mitigation: Review generated slugs before production publishing, especially for Chinese or mixed-language content. <br>
Risk: The documentation shows an --uppercase flag, while the script accepts --upper for uppercase output. <br>
Mitigation: Use --upper unless the publisher updates the documentation or script interface. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/darbling/slug-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON from the slug generator script, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a slug string, input echo, and separator metadata; supports custom separators and upper/title-case output modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
