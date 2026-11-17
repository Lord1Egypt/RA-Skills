## Description:

Turns subreddit research notes into Reddit ad copy that fits the 300 character headline limit and each community's own rules. Use when the user asks for reddit ads copywriter, reddit ad headline 300 characters, subreddit research for ads. For US DTC brands and SaaS marketers running Reddit promoted posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers use the skill to turn subreddit research into Reddit ad headlines and short post copy, then check the draft against community rules and claims the team can substantiate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated copy may misstate product claims or conflict with subreddit or advertising rules if the supplied research is incomplete or outdated.

Mitigation: Use current community research and substantiated claims, then review the copy and applicable platform rules before use.

Risk: Running the workflow overwrites digest.md when that file already exists in the selected output folder.

Mitigation: Choose a dedicated output folder or preserve any existing digest.md before running the script.

Risk: The optional Windows app is separate from the local workflow and was not assessed with this release.

Mitigation: The local Python workflow does not require the app; assess it independently before downloading or running it.

## Reference(s):

- [Reddit ad rules reference](references/reddit-ad-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/reddit-ads-copywriter)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown containing a research digest, ad headline, short body, community rule checks, and claim checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Headline is limited to 300 characters; body and checks are based on supplied research notes and claims. The generated digest.md overwrites an existing file of the same name in the output folder.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
