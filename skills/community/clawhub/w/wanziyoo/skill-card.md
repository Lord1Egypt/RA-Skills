## Description: <br>
Automates publishing, drafting, tagging, categorizing, and building Markdown posts for the Astro Koharu blog at /www/wwwroot/www.wanziyoo.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctf010300-commits](https://clawhub.ai/user/ctf010300-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to create Astro Koharu blog posts with complete frontmatter, generated Chinese descriptions, tags, categories, and a production build check. It is intended for the specific blog server and path named in the skill evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental use on the wrong host or blog path could create unwanted public content or run an unintended build. <br>
Mitigation: Install and invoke the skill only on the intended Astro Koharu blog server, and confirm the configured project path before publishing. <br>
Risk: A formal publish request can create a new Markdown post and rebuild the static site. <br>
Mitigation: Treat publish requests as real site changes, review the generated title, body, category, tags, and draft state, and rely on the documented no-overwrite rule for existing files. <br>
Risk: The build command executes the blog project's pnpm build script. <br>
Mitigation: Confirm the target repository and build script are trusted before first use, and stop at reporting the build error if the build fails. <br>


## Reference(s): <br>
- [Astro Koharu Blog Publish Rules](references/blog-publish-rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/ctf010300-commits/wanziyoo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Chinese status text plus Markdown blog files with YAML frontmatter and optional fenced shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates new Markdown posts only under the configured blog content path and may run the configured pnpm build command for formal posts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
