## Description: <br>
Publish markdown content to Wiki.js with proper formatting and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hugogu](https://clawhub.ai/user/hugogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content maintainers use this skill to create or update Wiki.js pages from markdown, including cleaning frontmatter, setting metadata, suggesting paths, and using the Wiki.js GraphQL API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update pages in a connected Wiki.js instance using WIKI_KEY. <br>
Mitigation: Use the least-privileged Wiki.js token available and treat WIKI_KEY as a sensitive credential. <br>
Risk: Incorrect target paths or unreviewed content could publish misleading or unwanted wiki pages. <br>
Mitigation: Review the target path and markdown content before allowing create, update, or broad page listing operations. <br>


## Reference(s): <br>
- [Wiki.js GraphQL API Reference](references/wiki-js-api.md) <br>
- [GraphQL String Type Specification](https://spec.graphql.org/October2021/#sec-String) <br>
- [Wiki.js API Documentation](https://docs.requarks.io/dev/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/hugogu/publish-wiki-js) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and GraphQL examples plus command-line usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WIKI_URL and a sensitive WIKI_KEY credential for live Wiki.js API operations.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
