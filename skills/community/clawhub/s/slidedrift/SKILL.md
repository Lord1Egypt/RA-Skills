---
name: slidedrift
description: Turn notes, articles, links and ideas into LinkedIn posts in your brand with SlideDrift (carousels, image posts, captions), then export them or schedule them to LinkedIn. Use when the user wants a LinkedIn carousel or post made from their own material, wants to edit an existing SlideDrift carousel, or wants to plan, export or schedule LinkedIn content.
---

# SlideDrift

SlideDrift is a LinkedIn content studio. It turns what the user already knows (a blog post, notes, a PDF or an idea) into designed LinkedIn carousels and posts in their brand, ready to edit, export or schedule.

This skill uses SlideDrift's remote MCP server:

```text
https://slidedrift.com/mcp
```

It uses OAuth. There is no API key. The first time a tool is called, the user signs in to SlideDrift (or creates a free account) and chooses **Allow connection**.

## When to use it

- "Turn this article into a LinkedIn carousel: <link>"
- "Make a 7-slide carousel from these notes"
- "Plan four weeks of LinkedIn posts from my newsletter"
- "Change the headline on slide 3 of my newest carousel"
- "Export my newest carousel as a PDF"
- "Schedule this carousel to my LinkedIn for Tuesday at 9am"

## How to work

1. **Create from the user's own material.** Pass the link or text straight to `create_carousel`. A separate outline is optional: call `plan_carousel` first only if the user wants to review the story.
2. **Pick a design when it matters.** `search_templates` finds designs, and `inspect_template` shows one. Without a template, SlideDrift uses a sensible default and the user's Brand Kit.
3. **Use their brand.** `list_brand_kits` shows saved kits. `import_brand_kit` builds one from the user's website.
4. **Long jobs run in the background.** Ask for `execution: "async"` and poll `get_job` until it finishes.
5. **Edit in place.** `edit_slide_text`, `style_slide_text`, `replace_slide_image` and `arrange_slide` change an existing carousel. Edits show a preview first and cost no generation credits.
6. **Deliver.** `export_carousel` returns a PDF, PNG files or image links. `create_share_link` makes a public link.
7. **Plan many posts.** `plan_campaign` and `create_campaign` draft a run of posts. Campaign posts start as drafts.
8. **Schedule.** `list_social_accounts`, then `schedule_social_post`. Scheduling needs a paid plan or a trial.

## Rules

- SlideDrift shows the credit cost before it generates or exports, and waits for the user's approval. Show the quote to the user; never approve on their behalf.
- Scheduling or publishing needs a separate, explicit approval.
- Only the user's own SlideDrift work is reachable.
- After creating something, give the user the editor link so they can review it.
- Keep the user's words. Don't invent facts, numbers or quotes for their slides.

## Tools at a glance

| Group | Tools |
| --- | --- |
| Create | `search_templates`, `inspect_template`, `plan_carousel`, `create_carousel`, `create_carousel_batch`, `get_job` |
| Brand and images | `list_brand_kits`, `import_brand_kit`, `list_source_images`, `prepare_source_image_upload`, `finalize_source_image_upload` |
| Carousels | `get_carousel`, `list_carousels`, `duplicate_carousel`, `get_credit_balance`, `export_carousel`, `create_share_link`, `disable_share_link` |
| Campaigns | `plan_campaign`, `create_campaign`, `get_campaign`, `retry_campaign_items`, `promote_campaign_posts`, `cancel_campaign` |
| Edit | `edit_slide_text`, `style_slide_text`, `replace_slide_image`, `put_source_image_on_slide`, `arrange_slide` |
| Scheduling | `list_social_accounts`, `schedule_social_post`, `list_scheduled_posts`, `update_scheduled_post`, `cancel_scheduled_post`, `add_first_comment` |

## If something goes wrong

- **Upgrade required:** the action needs a paid plan (for example, scheduling on a Free account).
- **Daily limit reached:** a Free account has used today's allowance for that action.
- **Confirmation required:** show the user the action and ask them to approve it.
- **Job still running:** call `get_job` again.
- **Authorization expired:** reconnect from the assistant.

Docs: https://slidedrift.com/docs/integrations/mcp · Developer page: https://slidedrift.com/developers/mcp
