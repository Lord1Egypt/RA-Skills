## Description: <br>
Qidian Reader helps agents find, rank, and recommend Qidian novels using browser-rendered public ranking pages with fallback recommendations when live access is blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers and agents use this skill to discover Qidian novels by genre, ranking, completion status, word count, and similarity to books the user already likes. It can use browser automation for live public ranking pages and clearly falls back to taste-based recommendations when live data is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Qidian ranking access may be blocked by anti-bot checks, verification pages, or dynamic rendering failures. <br>
Mitigation: Stop live browsing when verification or blank ranking pages appear, tell the user real-time rankings are unavailable, and switch to clearly labeled fallback recommendations. <br>
Risk: Users could expose Qidian credentials or ask the agent to bypass verification controls. <br>
Mitigation: Do not request credentials, do not attempt to bypass verification pages, and limit browsing to public ranking and catalog pages. <br>


## Reference(s): <br>
- [Qidian ranking URLs](references/urls.md) <br>
- [Qidian categories and tags](references/categories.md) <br>
- [Qidian Reader on ClawHub](https://clawhub.ai/ToBeWin/qidian-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendations with source and fallback notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations may include book titles, authors, categories, status, word counts, summaries, ranking signals, and links when available.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
