## Description: <br>
Find and normalize Chinese recipes (中餐菜谱) from structured sources first, then export clean recipe notes to Obsidian markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cylqqqcyl](https://clawhub.ai/user/cylqqqcyl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home cooks, recipe curators, and agents assisting them use this skill to find Chinese recipes from structured sources, compare candidates, normalize measurements and steps, and optionally save polished recipe notes for Obsidian. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe exports may write notes into an Obsidian vault or fallback workspace path, including synced folders. <br>
Mitigation: Confirm the target folder and filenames before exporting recipe notes. <br>
Risk: Recipe guidance can become unreliable if social posts or logged-in pages are treated as authoritative sources. <br>
Mitigation: Prefer public structured recipe pages, avoid login or paywall bypass, and mark social-source details as low confidence unless cross-validated. <br>


## Reference(s): <br>
- [ClawHub Recipe Scout page](https://clawhub.ai/cylqqqcyl/recipe-scout) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [Extraction Schema](references/schema.md) <br>
- [Query Formulation Examples](references/query-examples.md) <br>
- [Obsidian Recipe Note Template](references/obsidian-template.md) <br>
- [HowToCook recipe collection](https://github.com/Anduin2017/HowToCook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown, with optional structured recipe data and Obsidian markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write one markdown file per recipe when export is requested; otherwise returns recipe candidates, summaries, normalized steps, shopping lists, and source confidence in chat.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
