## Description:

Collects Xueqiu user posts, extracts full text and images with optional OCR, analyzes investment-related signals with local rules, and exports the results to SQLite, JSON, and Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjia-ie](https://clawhub.ai/user/zhangjia-ie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and individual investors use this skill to archive posts from a specified Xueqiu user, preserve associated images and OCR text, and classify investment-related content for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives a logged-in Edge browser session for Xueqiu collection.

Mitigation: Use a dedicated Edge profile and least-privilege Xueqiu account, and collect only content you are authorized to process.

Risk: User-provided authors, Xueqiu URLs, and discovered image URLs can cause unintended navigation, fetching, or collection.

Mitigation: Review the author and profile URL before execution, avoid untrusted inputs, and confirm the target is the intended Xueqiu profile.

Risk: Collected posts, OCR text, images, logs, and exports can accumulate sensitive local data.

Mitigation: Choose a controlled output directory, restrict local access, monitor storage growth, and review outputs before sharing.

Risk: The environment checker can install optional local packages when run with --fix.

Mitigation: Run the checker without --fix first and approve any package changes before enabling automatic fixes.

## Reference(s):

- [README](README.md)
- [Skill definition](SKILL.md)
- [Category keywords](references/category_keywords.json)
- [ClawHub skill page](https://clawhub.ai/zhangjia-ie/skills/xueqiu-collector)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [SQLite database rows, JSON exports, Markdown backups, downloaded image files, OCR text, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under the configured data directory, grouped by Xueqiu author, with full and per-category JSON and Markdown exports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
