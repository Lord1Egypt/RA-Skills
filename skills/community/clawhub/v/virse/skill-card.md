## Description: <br>
Virse Design helps agents work with the Virse AI Design Platform for image generation, canvas layout, workspace management, and asset organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vxcent](https://clawhub.ai/user/vxcent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, and developers use this skill to connect an agent to a Virse account, manage workspaces and canvases, generate image assets, organize visual content, and run creative workflow playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to Virse workspaces, canvases, and assets after authentication. <br>
Mitigation: Install and authenticate only when that account access is intended, and review workspace or canvas changes before allowing broad actions. <br>
Risk: Image generation and batch workflows may consume Virse credits. <br>
Mitigation: Check account balance and confirm larger generation batches before running them. <br>
Risk: Destructive or cross-workspace actions can modify or remove Virse content. <br>
Mitigation: Require explicit user approval for deletes, removals, and cross-workspace scans or collection workflows. <br>
Risk: Persistent account tokens can remain available to future agent sessions. <br>
Mitigation: Remove ~/.virse/token when persistent access is no longer needed, or use a session-scoped VIRSE_API_KEY. <br>
Risk: Self-update behavior may change skill behavior after installation. <br>
Mitigation: Review update prompts and release changes before accepting an update. <br>


## Reference(s): <br>
- [Virse Design on ClawHub](https://clawhub.ai/vxcent/virse) <br>
- [Virse Tools Reference](tools-reference.md) <br>
- [Virse Authentication Guide](auth-guide.md) <br>
- [Product Listing Image Pipeline Example](examples/product-listing-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON tool arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Virse workspaces, canvases, image assets, folders, edges, and groups through authenticated Virse calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
