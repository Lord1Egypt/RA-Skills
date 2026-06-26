## Description: <br>
xiaofeng-skills creates restaurant visit posts by generating AI storefront photos, collecting selected Dianping dish images, drafting promotional copy, and publishing the result to Tencent Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turkyden](https://clawhub.ai/user/turkyden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Restaurant marketers and operators use this skill to assemble Tencent Docs-ready promotional visit notes from store photos, Dianping links, generated imagery, dish images, and short-form marketing copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use existing local Tencent Docs authorization and upload selected images and note text to Tencent Docs. <br>
Mitigation: Use an explicit, intended Tencent Docs account or token, review the content before publishing, and choose the destination folder deliberately. <br>
Risk: Generated Tencent Docs may be made publicly editable by the included publishing workflow. <br>
Mitigation: Change sharing to private or view-only unless public editing is intentional, and verify document permissions after publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turkyden/xiaofeng-skills) <br>
- [Tencent Docs MCP endpoint](https://docs.qq.com/openapi/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown copy, shell-command workflow, and Tencent Docs document URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REPLICATE_API_TOKEN plus installed tencent-docs and tandian-image-skills skills; the included workflow may publish Tencent Docs with public edit permissions.] <br>

## Skill Version(s): <br>
1.1.10 (source: server release evidence; artifact frontmatter says 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
