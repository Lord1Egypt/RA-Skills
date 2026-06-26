## Description: <br>
Save and review notes, quotes, articles, links, images, and video references in a personal commonplace book. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gniting](https://clawhub.ai/user/gniting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Robin through a host agent to save personal notes, quotes, links, images, and video references into a local commonplace-book library, then search or review those entries later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved entries may contain personal notes and copied local images. <br>
Mitigation: Use a dedicated Robin state directory and keep topics_dir and media_dir inside that directory. <br>
Risk: Move, delete, add, and review operations modify the local Robin library or review state. <br>
Mitigation: Run commands intentionally, prefer JSON output for agent parsing, and use doctor or selftest checks when library health is uncertain. <br>
Risk: Scheduled recall can resurface saved personal content automatically. <br>
Mitigation: Enable scheduled recall only when the user wants automatic resurfacing, and keep active rating flows separate from scheduled recall. <br>


## Reference(s): <br>
- [Robin ClawHub Release](https://clawhub.ai/gniting/robin) <br>
- [Robin Guide](docs/guide.md) <br>
- [Robin Configuration Example](references/robin-config-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists entries as local Markdown topic files and JSON review state in the configured Robin state directory.] <br>

## Skill Version(s): <br>
0.3.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
