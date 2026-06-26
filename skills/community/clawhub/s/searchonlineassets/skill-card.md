## Description: <br>
Online asset search tool: queries public stock libraries (Pixabay) for high-quality photos, illustrations, vectors and videos, returning result metadata and URLs for use in the current workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Pixabay-backed public asset libraries from an agent workflow and select relevant image, illustration, vector, or video result URLs with metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store it in a local user configuration file. <br>
Mitigation: Use the DLAZY_API_KEY environment variable for per-invocation credentials when persistent local storage is not desired, and rotate or revoke keys from the dLazy dashboard as needed. <br>
Risk: Pixabay searches are mediated by dLazy services, so query text and filters are sent through that intermediary. <br>
Mitigation: Install only when that SaaS flow is acceptable, avoid sensitive search terms, and review the dLazy CLI source or package before global installation. <br>


## Reference(s): <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy](https://dlazy.com) <br>
- [SearchOnlineAssets on ClawHub](https://clawhub.ai/dlazyai/searchonlineassets) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON result metadata with asset URLs, summarized for the user as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returned asset URLs are hosted by Pixabay; safesearch is forced on server-side.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
