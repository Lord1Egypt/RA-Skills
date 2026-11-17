---
name: writestack
description: Draft, schedule and manage Substack Notes and articles through the WriteStack MCP server, using the user's saved writing style, posting queue and note performance stats. Use when the user wants to write, queue, schedule or review Substack Notes or articles, check their posting schedule, or see how their Notes performed.
homepage: https://www.writestack.io
metadata:
  openclaw:
    emoji: "✍️"
---

# WriteStack for Substack

WriteStack is a Substack creator platform. This skill teaches you how to use its MCP server to draft, schedule and review Notes and articles for the user. The skill carries no data of its own: everything comes from the user's own WriteStack account.

Requires a WriteStack account with MCP access enabled (https://www.writestack.io).

## Connect the server (one time)

Check first whether the `writestack` MCP server is already configured: `openclaw mcp doctor writestack --probe`. If it is not, set it up:

1. Add it:
   ```bash
   openclaw mcp add writestack \
     --url https://www.writestack.io/api/mcp/mcp \
     --transport streamable-http
   ```
2. Turn on OAuth for it. In `openclaw.json`, under `mcp.servers.writestack`, add `auth: "oauth"`.
3. Sign in with the user's WriteStack account: Settings → MCP → Sign in, or run `openclaw mcp login writestack` and follow the printed link.
4. Confirm: `openclaw mcp doctor writestack --probe` should list the tools.

Never ask the user to paste their password or an API key into chat. Sign-in happens on the WriteStack page that the link opens.

## What you can do

**Notes**
- Read: `list_notes`, `get_note`, `get_queue`, `get_schedule`, `get_next_available_slots`, `get_schedule_capacity`, `list_tags`, `list_activities`
- Write: `create_note`, `create_many_notes`, `update_note`, `schedule_notes`, `schedule_notes_with_custom_dates`
- Style and performance: `get_writing_style`, `get_notes_statistics`, `get_posts_statistics`
- Cross-posting: `list_buffer_channels` (Buffer channels the user connected)

**Articles**
- Read: `list_articles`, `get_article`, `list_article_newsletters`, `get_article_substack_status`
- Write: `create_article`, `update_article`, `generate_article`, `push_article_to_substack`, `schedule_article_on_substack`, `unschedule_article_on_substack`

**Other**: `get_feature_suggestion_link` only returns the link to the WriteStack features board. It submits nothing. Use it when the user asks for something WriteStack cannot do, then tell them to post the idea there themselves.

The server does not delete notes or articles.

## Rules to follow

1. **Match the user's voice.** Before writing new note content, call `get_writing_style` (unless the user pasted complete style instructions).
2. **Notes are Markdown.** Separate paragraphs with a blank line (two newlines).
3. **Ask before assuming.**
   - Tags: offer `list_tags` and ask which to apply before creating notes. Tags also decide which reserved queue times a note can take.
   - Links: if a note contains a link, ask whether the user wants a link-preview card. Pass `includePreviews: true` only if they say yes.
   - Buffer: call `list_buffer_channels` first if they want cross-posting.
4. **Articles always need a newsletter.** Call `list_article_newsletters`, show the user the options and ask which one to use before `create_article`, `push_article_to_substack` or `schedule_article_on_substack`. Never guess a publication ID.
5. **Read an article before you edit it.** Call `get_article` right before `update_article`, because the user may have changed it in WriteStack. `update_article` needs the `baseVersion` from that read and replaces the article's current content, so never update from an older copy. It saves in WriteStack only and does not push to Substack.
6. **Pushing overwrites.** Pushing an article that already has a Substack draft updates (overwrites) that draft. Say so before you do it.
7. **Check capacity before scheduling notes.** Always call `get_schedule_capacity` before `schedule_notes` or `schedule_notes_with_custom_dates`, and never schedule more notes than `remaining` unless `unlimited` is true. Use `get_next_available_slots` to preview when notes would land.
8. **Prefer the recurring schedule.** `schedule_notes` places notes in the user's next slots from their recurring schedule template and respects tag lanes. Use `schedule_notes_with_custom_dates` only when the user asked for specific dates and times, or has no schedule template yet. Dates must be in the future (ISO 8601).
9. **Confirm before anything that publishes or schedules.** Summarize what will be scheduled (how many, when) and wait for a clear yes.
10. **Keep it private.** Everything returned is the user's own data. Do not quote their notes or stats outside this conversation.

## Example requests

- "Write 5 Notes about my latest article in my writing style and schedule them over the next week."
- "How did my Notes perform this month? Which ones got the most engagement?"
- "Generate a draft article about <topic> and push it to Substack as a draft."
- "What does my posting queue look like for the coming days?"

## Troubleshooting

- **Tools missing or sign-in fails:** run `openclaw mcp doctor writestack --probe`, then `openclaw mcp login writestack`.
- **Access denied:** the account may not have MCP access enabled. Point the user to https://www.writestack.io/settings.
- **Push or schedule queued instead of finishing:** article pushes go through the user's Chrome extension, so they sync the next time WriteStack is open with the extension.
