# Automations, curation, and Listen

## Automations

- `list_automations` lists available automations.
- `get_automation` reads one automation's configuration.
- `get_automation_log` reads recent execution logs and can filter by automation.
- `toggle_automation` enables or disables an automation. Verify both the automation ID and requested state because enabling it may cause future external actions.

## Curated content

`get_curated_items` searches curated items by feed, meaning, source scope, or rolling time range. Treat results as source material. Do not imply that a curated item is endorsed, accurate, or already scheduled.

## Social listening

- `list_listen_sources`, `list_listen_streams`, and `get_listen_stream` inspect available sources and stream configuration.
- `list_listen_items` and `get_listen_item` read saved results.
- `archive_listen_item`, `unarchive_listen_item`, `bulk_archive_listen_items`, and `archive_all_listen_items` change item status.
- `delete_listen_item` and `bulk_delete_listen_items` permanently remove saved items and can require team Manage Social Listening permission.

Use stream and item IDs returned by SocialBu. Before bulk archive or deletion, state the stream and item scope clearly and ensure it matches the user's request.
