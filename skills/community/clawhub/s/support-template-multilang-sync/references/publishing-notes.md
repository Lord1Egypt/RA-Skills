# Publishing Notes

## Required environment

Set these before attempting external sync or publication:

- `FEISHU_ACCESS_TOKEN` or `FEISHU_APP_ID` + `FEISHU_APP_SECRET`
- `FEISHU_WIKI_SPACE_ID`
- `FEISHU_SUPPORT_TICKETS_NODE_ID` or another target parent node token
- `GITHUB_TOKEN`
- `GITHUB_REPO`
- `CLAWHUB_API_KEY` or an authenticated `clawhub` session

## Minimal release checklist

1. Update the source markdown template.
2. Re-read and verify placeholders and language coverage.
3. Sync the final content to Feishu Wiki.
4. Open a GitHub issue with the exact file path and language additions.
5. Validate the skill.
6. Package the skill.
7. Publish the skill to ClawHub.
