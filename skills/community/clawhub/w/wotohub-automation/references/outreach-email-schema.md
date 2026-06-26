# Outreach Email Draft Schema

Each generated email draft should contain:

- `bloggerId`: selected creator id
- `nickname`: creator display name
- `language`: output language code, default `en`
- `style`: short style label, e.g. `commerce-natural`
- `subject`: final email subject
- `htmlBody`: HTML email body using lightweight tags only
- `plainTextBody`: plain text fallback
- `styleReason`: optional short explanation for why this tone/style was chosen

Batch write-back should also contain metadata:

- `selectedCreatorCount`: number of creators selected for this cycle
- `generatedDraftCount`: number of draft items actually written back
- `uniqueBloggerIdCount`: unique bloggerId count inside returned drafts
- `missingBloggerIds`: selected creator ids with no draft returned
- `duplicateBloggerIds`: blogger ids that appear more than once in returned drafts
- `unexpectedBloggerIds`: blogger ids returned by host but not present in this cycle's selected creators

## Notes
- HTML body is the primary send format.
- Plain text body is the compatibility fallback.
- Model output should be preferred; script output is fallback-only.
- For real outbound sends, use model-first personalized drafts by default; do not treat fallback script drafts as the default send path just to save time.
- Default language policy: subject + body must be English unless the user explicitly requests another supported language.
- Host write-back should be one-draft-per-selected-creator. Do not return fewer drafts silently, and do not reuse the same bloggerId or full email content across different creators.
