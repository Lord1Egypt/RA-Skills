## Description: <br>
Search Target.com, look up products, check per-store stock and pickup ETAs near a ZIP, and build a deep link that pre-populates a guest cart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[druyang](https://clawhub.ai/user/druyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to search Target products, compare product details and review summaries, check local store availability by ZIP code, and prepare guest-cart handoff links without account login or checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated cart links contain a short-lived bearer token that can allow anyone with the link to modify the guest cart. <br>
Mitigation: Treat cart links and redirect files as private, avoid posting them in shared or long-lived channels, and rely on the local handoff file or per-item product links when possible. <br>
Risk: The skill contacts Target, may open the browser for cart handoff, and can cache a short-lived cart token locally. <br>
Mitigation: Run it only in environments where this browser handoff and local temporary-token cache are acceptable, and remove temporary cart artifacts after use when handling sensitive shopping sessions. <br>
Risk: Prices, stock, pickup ETAs, endpoint shapes, and public web behavior can change without notice. <br>
Mitigation: Confirm final price, availability, and purchase details on Target.com before committing to any transaction. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/druyang/target-shopping) <br>
- [Project homepage](https://github.com/druyang/target-shopper-skill) <br>
- [Public-facing API endpoints used by this skill](references/endpoints.md) <br>
- [Terms of service and etiquette](references/tos-and-etiquette.md) <br>
- [Common Target category N-IDs](references/categories.md) <br>
- [Target API status codes](references/status-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from helper scripts with text or Markdown summaries and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cart handoff output can include a local redirect file, short shopping-list fallback links, item-level add results, and token-expiration metadata.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact frontmatter and pyproject.toml report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
