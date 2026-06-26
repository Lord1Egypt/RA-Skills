## Description: <br>
Autonomously fetches BigCommerce products, generates optimized titles and HTML descriptions, updates catalog entries, and tracks progress across pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veevortexiq](https://clawhub.ai/user/veevortexiq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Store operators and ecommerce teams use this skill to bulk rewrite and optimize BigCommerce product titles and descriptions while preserving page-by-page progress. Agents can fetch product data, prepare update JSON, push changes through the BigCommerce API, and report completion status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite many live BigCommerce product listings with a write-capable token. <br>
Mitigation: Use a temporary least-privilege Products token, back up or export the catalog first, and run the workflow on a small subset before broader use. <br>
Risk: The documented autonomous workflow has no built-in approval checkpoint before pushing generated catalog updates. <br>
Mitigation: Review each generated page_N_updates.json file and require explicit approval for each batch before running the update command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veevortexiq/viq-bc-optimiser) <br>
- [BigCommerce API endpoint used by the helper script](https://api.bigcommerce.com/stores/{store_hash}/v3) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, API calls, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON progress or update files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates progress.json, page_N_products.json, and page_N_updates.json during normal operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
