# Accounts, teams, and queues

## Accounts and teams

- `list_accounts` returns every connected account available directly or through a team.
- `search_accounts` finds connected accounts by name.
- `list_teams` and `search_teams` resolve the user's available teams.
- Use returned IDs instead of guessing from names or network handles.

`get_account_connect_url` and `reconnect_account` return an OAuth URL for a supported social network. Give the URL to the user and let them complete the provider authorization in their browser. Do not claim the account is connected until a later account lookup confirms it.

`update_account` changes the SocialBu display name. `delete_account` removes the connection and is destructive, so verify the target account and user intent first.

## Custom queues

- `list_queues` returns recurring publishing queues.
- `list_queue_posts` returns a queue's items in queue order.
- `add_post_to_queue` adds content to a queue and may later result in external publication under that queue's schedule.

Before adding an item, verify the queue, content, media, destination accounts, and network-specific options. Use `get_post_options` when the queue includes accounts whose required options are not already known.
