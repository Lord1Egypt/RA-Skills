# Which tool carries which operation

On hosts served the grouped catalog, call these as the `action` of the tool
in the left column. On Claude Code each operation is a tool of its own with
the same name. `describe_actions` returns any operation's full schema.

The full, generated list: https://scripe.io/developers/api/v1/mcp-catalog

## Planning (tools of their own on every host)

`get_planning_overview`, `get_profile_planning_context`,
`get_planning_signals`, `check_plan_ideas`, `preview_plan`, `commit_plan`,
`draft_planned_posts`, `get_post_media_options`, `add_post_media`,
`check_post_readiness`, `tag_post_mentions`, `request_review`,
`list_waiting_for_me`

## Domain tools

| Tool | Main operations |
|---|---|
| `workspace_read` | `get_workspace_context`, `list_workspaces`, `list_projects`, `get_project`, `list_team`, `get_usage`, `get_job` |
| `workspace_write` | `switch_workspace`, `create_upload_url`, `cancel_job` |
| `posts_read` | `list_posts`, `get_post`, `list_post_statuses`, `get_draft_run` |
| `posts_write` | `generate_post`, `create_post_draft`, `update_post`, `schedule_post`, `publish_post`, `attach_media_to_post`, `set_up_team_engagement` |
| `posts_delete` | `delete_post` |
| `ideas_read` | `list_ideas`, `get_idea`, `list_for_you_ideas`, `get_for_you_idea` |
| `ideas_write` | `create_idea`, `update_idea`, `schedule_idea`, `generate_post_ideas`, `save_for_you_idea`, `dismiss_for_you_idea` |
| `calendar_read` | `list_calendar`, `list_calendar_slots`, `get_goals`, `get_next_free_slot`, `get_posting_times`, `list_notes` |
| `calendar_write` | `fill_calendar_slot`, `create_note`, `update_posting_schedule` |
| `knowledge_read` | `search_knowledge`, `read_knowledge_document`, `list_knowledge`, `get_knowledge_ingest` |
| `knowledge_write` | `add_to_knowledge_base`, `create_source_text`, `create_source_file` |
| `analytics_read` | `get_analytics_overview`, `list_post_analytics`, `get_analytics_report`, `search_viral_posts` |
| `brand_read` | `get_settings`, `get_positioning`, `get_personal_dna`, `list_content_topics` |
| `brand_write` | `update_positioning`, `update_personal_dna`, `update_tone_of_voice` |
| `media_read` / `media_write` | `search_media` / `generate_image`, `generate_carousel`, `create_media_asset` |
| `organize_read` / `organize_write` | labels, campaigns and content questions |
| `community_read` / `community_write` | profile watchlists, anonymised comments under your own posts |
| `links_read` / `links_write` | tracked links |

Deletes live in the matching `*_delete` tool and are two-phase.

## Prompts

`plan_content`, `fill_calendar`, `weekly_planning`, `repurpose`,
`inbox_zero`
