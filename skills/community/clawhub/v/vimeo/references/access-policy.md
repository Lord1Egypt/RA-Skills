# Vimeo access policy

An access policy limits which endpoints Vimeo connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/vimeo#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Vimeo: its 163 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create vimeo --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "me/albums"},
    {"method": "GET", "path": "me/albums/{id}"},
    {"method": "GET", "path": "me/albums/{id}/videos"},
    {"method": "GET", "path": "me/albums/{id}/videos/{id}"},
    {"method": "GET", "path": "users/{id}/albums"},
    {"method": "GET", "path": "users/{id}/albums/{id}"},
    {"method": "GET", "path": "users/{id}/albums/{id}/custom_thumbnails"},
    {"method": "GET", "path": "users/{id}/albums/{id}/custom_thumbnails/{id}"},
    {"method": "GET", "path": "users/{id}/albums/{id}/logos"},
    {"method": "GET", "path": "users/{id}/albums/{id}/logos/{id}"},
    {"method": "GET", "path": "users/{id}/albums/{id}/videos"},
    {"method": "GET", "path": "users/{id}/albums/{id}/videos/{id}"},
    {"method": "GET", "path": "me/appearances"},
    {"method": "GET", "path": "users/{id}/appearances"},
    {"method": "GET", "path": "categories"},
    {"method": "GET", "path": "categories/{id}"},
    {"method": "GET", "path": "categories/{id}/channels"},
    {"method": "GET", "path": "categories/{id}/groups"},
    {"method": "GET", "path": "categories/{id}/videos"},
    {"method": "GET", "path": "categories/{id}/videos/{id}"},
    {"method": "GET", "path": "me/categories"},
    {"method": "GET", "path": "me/categories/{id}"},
    {"method": "GET", "path": "users/{id}/categories"},
    {"method": "GET", "path": "users/{id}/categories/{id}"},
    {"method": "GET", "path": "channels"},
    {"method": "GET", "path": "channels/{id}"},
    {"method": "GET", "path": "channels/{id}/categories"},
    {"method": "GET", "path": "channels/{id}/moderators"},
    {"method": "GET", "path": "channels/{id}/moderators/{id}"},
    {"method": "GET", "path": "channels/{id}/privacy/users"},
    {"method": "GET", "path": "channels/{id}/tags"},
    {"method": "GET", "path": "channels/{id}/tags/{id}"},
    {"method": "GET", "path": "channels/{id}/users"},
    {"method": "GET", "path": "channels/{id}/videos"},
    {"method": "GET", "path": "channels/{id}/videos/{id}"},
    {"method": "GET", "path": "channels/{id}/videos/{id}/comments"},
    {"method": "GET", "path": "channels/{id}/videos/{id}/credits"},
    {"method": "GET", "path": "channels/{id}/videos/{id}/likes"},
    {"method": "GET", "path": "channels/{id}/videos/{id}/pictures"},
    {"method": "GET", "path": "channels/{id}/videos/{id}/privacy/users"},
    {"method": "GET", "path": "channels/{id}/videos/{id}/texttracks"},
    {"method": "GET", "path": "me/channels"},
    {"method": "GET", "path": "me/channels/{id}"},
    {"method": "GET", "path": "users/{id}/channels"},
    {"method": "GET", "path": "users/{id}/channels/{id}"},
    {"method": "GET", "path": "contentratings"},
    {"method": "GET", "path": "creativecommons"},
    {"method": "GET", "path": "me/customlogos"},
    {"method": "GET", "path": "me/customlogos/{id}"},
    {"method": "GET", "path": "users/{id}/customlogos"},
    {"method": "GET", "path": "users/{id}/customlogos/{id}"},
    {"method": "GET", "path": "me/presets"},
    {"method": "GET", "path": "me/presets/{id}"},
    {"method": "GET", "path": "me/presets/{id}/videos"},
    {"method": "GET", "path": "users/{id}/presets"},
    {"method": "GET", "path": "users/{id}/presets/{id}"},
    {"method": "GET", "path": "users/{id}/presets/{id}/videos"},
    {"method": "GET", "path": "me/feed"},
    {"method": "GET", "path": "users/{id}/feed"},
    {"method": "GET", "path": "me/followers"},
    {"method": "GET", "path": "users/{id}/followers"},
    {"method": "GET", "path": "me/following"},
    {"method": "GET", "path": "me/following/{id}"},
    {"method": "GET", "path": "users/{id}/following"},
    {"method": "GET", "path": "users/{id}/following/{id}"},
    {"method": "GET", "path": "groups"},
    {"method": "GET", "path": "groups/{id}"},
    {"method": "GET", "path": "groups/{id}/users"},
    {"method": "GET", "path": "groups/{id}/videos"},
    {"method": "GET", "path": "groups/{id}/videos/{id}"},
    {"method": "GET", "path": "me/groups"},
    {"method": "GET", "path": "me/groups/{id}"},
    {"method": "GET", "path": "users/{id}/groups"},
    {"method": "GET", "path": "users/{id}/groups/{id}"},
    {"method": "GET", "path": "languages"},
    {"method": "GET", "path": "me/likes"},
    {"method": "GET", "path": "me/likes/{id}"},
    {"method": "GET", "path": "users/{id}/likes"},
    {"method": "GET", "path": "users/{id}/likes/{id}"},
    {"method": "GET", "path": "oauth/verify"},
    {"method": "GET", "path": "me/ondemand/pages"},
    {"method": "GET", "path": "me/ondemand/purchases"},
    {"method": "GET", "path": "me/ondemand/purchases/{id}"},
    {"method": "GET", "path": "ondemand/genres"},
    {"method": "GET", "path": "ondemand/genres/{id}"},
    {"method": "GET", "path": "ondemand/genres/{id}/pages"},
    {"method": "GET", "path": "ondemand/genres/{id}/pages/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/backgrounds"},
    {"method": "GET", "path": "ondemand/pages/{id}/backgrounds/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/genres"},
    {"method": "GET", "path": "ondemand/pages/{id}/genres/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/likes"},
    {"method": "GET", "path": "ondemand/pages/{id}/pictures"},
    {"method": "GET", "path": "ondemand/pages/{id}/pictures/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/promotions"},
    {"method": "GET", "path": "ondemand/pages/{id}/promotions/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/regions"},
    {"method": "GET", "path": "ondemand/pages/{id}/regions/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/seasons"},
    {"method": "GET", "path": "ondemand/pages/{id}/seasons/{id}"},
    {"method": "GET", "path": "ondemand/pages/{id}/seasons/{id}/videos"},
    {"method": "GET", "path": "ondemand/pages/{id}/videos"},
    {"method": "GET", "path": "ondemand/pages/{id}/videos/{id}"},
    {"method": "GET", "path": "ondemand/regions"},
    {"method": "GET", "path": "ondemand/regions/{id}"},
    {"method": "GET", "path": "users/{id}/ondemand/pages"},
    {"method": "GET", "path": "users/{id}/ondemand/purchases"},
    {"method": "GET", "path": "me/pictures"},
    {"method": "GET", "path": "me/pictures/{id}"},
    {"method": "GET", "path": "users/{id}/pictures"},
    {"method": "GET", "path": "users/{id}/pictures/{id}"},
    {"method": "GET", "path": "me/portfolios"},
    {"method": "GET", "path": "me/portfolios/{id}"},
    {"method": "GET", "path": "me/portfolios/{id}/videos"},
    {"method": "GET", "path": "me/portfolios/{id}/videos/{id}"},
    {"method": "GET", "path": "users/{id}/portfolios"},
    {"method": "GET", "path": "users/{id}/portfolios/{id}"},
    {"method": "GET", "path": "users/{id}/portfolios/{id}/videos"},
    {"method": "GET", "path": "users/{id}/portfolios/{id}/videos/{id}"},
    {"method": "GET", "path": "me/projects"},
    {"method": "GET", "path": "me/projects/{id}"},
    {"method": "GET", "path": "me/projects/{id}/videos"},
    {"method": "GET", "path": "users/{id}/projects"},
    {"method": "GET", "path": "users/{id}/projects/{id}"},
    {"method": "GET", "path": "users/{id}/projects/{id}/videos"},
    {"method": "GET", "path": "tags/{id}"},
    {"method": "GET", "path": "tags/{id}/videos"},
    {"method": "GET", "path": "tutorial"},
    {"method": "GET", "path": "me"},
    {"method": "GET", "path": "users"},
    {"method": "GET", "path": "users/{id}"},
    {"method": "GET", "path": "me/videos"},
    {"method": "GET", "path": "me/videos/{id}"},
    {"method": "GET", "path": "users/{id}/videos"},
    {"method": "GET", "path": "users/{id}/videos/{id}"},
    {"method": "GET", "path": "videos"},
    {"method": "GET", "path": "videos/{id}"},
    {"method": "GET", "path": "videos/{id}/available_albums"},
    {"method": "GET", "path": "videos/{id}/available_channels"},
    {"method": "GET", "path": "videos/{id}/categories"},
    {"method": "GET", "path": "videos/{id}/comments"},
    {"method": "GET", "path": "videos/{id}/comments/{id}"},
    {"method": "GET", "path": "videos/{id}/comments/{id}/replies"},
    {"method": "GET", "path": "videos/{id}/credits"},
    {"method": "GET", "path": "videos/{id}/credits/{id}"},
    {"method": "GET", "path": "videos/{id}/likes"},
    {"method": "GET", "path": "videos/{id}/pictures"},
    {"method": "GET", "path": "videos/{id}/pictures/{id}"},
    {"method": "GET", "path": "videos/{id}/presets/{id}"},
    {"method": "GET", "path": "videos/{id}/privacy/domains"},
    {"method": "GET", "path": "videos/{id}/privacy/users"},
    {"method": "GET", "path": "videos/{id}/tags"},
    {"method": "GET", "path": "videos/{id}/tags/{id}"},
    {"method": "GET", "path": "videos/{id}/texttracks"},
    {"method": "GET", "path": "videos/{id}/texttracks/{id}"},
    {"method": "GET", "path": "videos/{id}/timelinethumbnails/{id}"},
    {"method": "GET", "path": "videos/{id}/videos"},
    {"method": "GET", "path": "me/watched/videos"},
    {"method": "GET", "path": "me/watchlater"},
    {"method": "GET", "path": "me/watchlater/{id}"},
    {"method": "GET", "path": "users/{id}/watchlater"},
    {"method": "GET", "path": "users/{id}/watchlater/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Vimeo endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | me/albums | read | albums | Get all the albums that belong to a user. |
| POST | me/albums | write | albums | Create an album. |
| GET | me/albums/{id} | read | albums | Get a specific album. |
| PATCH | me/albums/{id} | write | albums | Edit an album. |
| DELETE | me/albums/{id} | write | albums | Delete an album. |
| GET | me/albums/{id}/videos | read | albums | Get all the videos in an album. |
| PUT | me/albums/{id}/videos | write | albums | Replace all the videos in an album. |
| GET | me/albums/{id}/videos/{id} | read | albums | Get a specific video in an album. |
| PUT | me/albums/{id}/videos/{id} | write | albums | Add a specific video to an album. |
| DELETE | me/albums/{id}/videos/{id} | write | albums | Remove a video from an album. |
| POST | me/albums/{id}/videos/{id}/set_album_thumbnail | write | albums | Set a video as the album thumbnail. |
| GET | users/{id}/albums | read | albums | Get all the albums that belong to a user. |
| POST | users/{id}/albums | write | albums | Create an album. |
| GET | users/{id}/albums/{id} | read | albums | Get a specific album. |
| PATCH | users/{id}/albums/{id} | write | albums | Edit an album. |
| DELETE | users/{id}/albums/{id} | write | albums | Delete an album. |
| GET | users/{id}/albums/{id}/custom_thumbnails | read | albums | Get all the custom upload thumbnails of an album. |
| POST | users/{id}/albums/{id}/custom_thumbnails | write | albums | Add a custom uploaded thumbnail. |
| GET | users/{id}/albums/{id}/custom_thumbnails/{id} | read | albums | Get a specific custom uploaded album thumbnail. |
| PATCH | users/{id}/albums/{id}/custom_thumbnails/{id} | write | albums | Replace a custom uploaded album thumbnail. |
| DELETE | users/{id}/albums/{id}/custom_thumbnails/{id} | write | albums | Remove a custom uploaded album thumbnail. |
| GET | users/{id}/albums/{id}/logos | read | albums | Get all the custom logos of an album. |
| POST | users/{id}/albums/{id}/logos | write | albums | Add a custom album logo. |
| GET | users/{id}/albums/{id}/logos/{id} | read | albums | Get a specific custom album logo. |
| PATCH | users/{id}/albums/{id}/logos/{id} | write | albums | Replace a custom album logo. |
| DELETE | users/{id}/albums/{id}/logos/{id} | write | albums | Remove a custom album logo. |
| GET | users/{id}/albums/{id}/videos | read | albums | Get all the videos in an album. |
| PUT | users/{id}/albums/{id}/videos | write | albums | Replace all the videos in an album. |
| GET | users/{id}/albums/{id}/videos/{id} | read | albums | Get a specific video in an album. |
| PUT | users/{id}/albums/{id}/videos/{id} | write | albums | Add a specific video to an album. |
| DELETE | users/{id}/albums/{id}/videos/{id} | write | albums | Remove a video from an album. |
| POST | users/{id}/albums/{id}/videos/{id}/set_album_thumbnail | write | albums | Set a video as the album thumbnail. |
| GET | me/appearances | read | appearances | Get all the videos in which a user appears. |
| GET | users/{id}/appearances | read | appearances | Get all the videos in which a user appears. |
| GET | categories | read | categories | Get all categories. |
| GET | categories/{id} | read | categories | Get a specific category. |
| GET | categories/{id}/channels | read | categories | Get all the channels in a category. |
| GET | categories/{id}/groups | read | categories | Get all the groups in a category. |
| GET | categories/{id}/videos | read | categories | Get all the videos in a category. |
| GET | categories/{id}/videos/{id} | read | categories | Check for a video in a category. |
| GET | me/categories | read | categories | Get all the categories that a user follows. |
| GET | me/categories/{id} | read | categories | Check if a user follows a category. |
| PUT | me/categories/{id} | write | categories | Subscribe a user to a single category. |
| DELETE | me/categories/{id} | write | categories | Unsubscribe a user from a category. |
| GET | users/{id}/categories | read | categories | Get all the categories that a user follows. |
| GET | users/{id}/categories/{id} | read | categories | Check if a user follows a category. |
| PUT | users/{id}/categories/{id} | write | categories | Subscribe a user to a single category. |
| DELETE | users/{id}/categories/{id} | write | categories | Unsubscribe a user from a category. |
| GET | channels | read | channels | Get all channels. |
| POST | channels | write | channels | Create a channel. |
| GET | channels/{id} | read | channels | Get a specific channel. |
| PATCH | channels/{id} | write | channels | Edit a channel. |
| DELETE | channels/{id} | write | channels | Delete a channel. |
| GET | channels/{id}/categories | read | channels | Get all the categories in a channel. |
| PUT | channels/{id}/categories | write | channels | Add a list of categories to a channel. |
| PUT | channels/{id}/categories/{id} | write | channels | Categorize a channel. |
| DELETE | channels/{id}/categories/{id} | write | channels | Remove a category from a channel. |
| GET | channels/{id}/moderators | read | channels | Get all the moderators in a channel. |
| PUT | channels/{id}/moderators | write | channels | Add a list of channel moderators. |
| PATCH | channels/{id}/moderators | write | channels | Replace the moderators of a channel. |
| DELETE | channels/{id}/moderators | write | channels | Remove a list of channel moderators. |
| GET | channels/{id}/moderators/{id} | read | channels | Get a specific channel moderator. |
| PUT | channels/{id}/moderators/{id} | write | channels | Add a specific channel moderator. |
| DELETE | channels/{id}/moderators/{id} | write | channels | Remove a specific channel moderator. |
| GET | channels/{id}/privacy/users | read | channels | Get all the users who can view a private channel. |
| PUT | channels/{id}/privacy/users | write | channels | Permit a list of users to view a private channel. |
| PUT | channels/{id}/privacy/users/{id} | write | channels | Permit a specific user to view a private channel. |
| DELETE | channels/{id}/privacy/users/{id} | write | channels | Restrict a user from viewing a private channel. |
| GET | channels/{id}/tags | read | channels | Get all the tags that have been added to a channel. |
| PUT | channels/{id}/tags | write | channels | Add a list of tags to a channel. |
| GET | channels/{id}/tags/{id} | read | channels | Check if a tag has been added to a channel. |
| PUT | channels/{id}/tags/{id} | write | channels | Add a specific tag to a channel. |
| DELETE | channels/{id}/tags/{id} | write | channels | Remove a tag from a channel. |
| GET | channels/{id}/users | read | channels | Get all the followers of a channel. |
| GET | channels/{id}/videos | read | channels | Get all the videos in a channel. |
| PUT | channels/{id}/videos | write | channels | Add a list of videos to a channel. |
| DELETE | channels/{id}/videos | write | channels | Remove a list of videos from a channel. |
| GET | channels/{id}/videos/{id} | read | channels | Get a specific video in a channel. |
| PUT | channels/{id}/videos/{id} | write | channels | Add a specific video to a channel. |
| DELETE | channels/{id}/videos/{id} | write | channels | Remove a specific video from a channel. |
| GET | channels/{id}/videos/{id}/comments | read | channels | Get all the comments on a video. |
| POST | channels/{id}/videos/{id}/comments | write | channels | Add a comment to a video. |
| GET | channels/{id}/videos/{id}/credits | read | channels | Get all the credited users in a video. |
| POST | channels/{id}/videos/{id}/credits | write | channels | Credit a user in a video. |
| GET | channels/{id}/videos/{id}/likes | read | channels | Get all the users who have liked a video. |
| GET | channels/{id}/videos/{id}/pictures | read | channels | Get all the thumbnails of a video. |
| POST | channels/{id}/videos/{id}/pictures | write | channels | Add a video thumbnail. |
| GET | channels/{id}/videos/{id}/privacy/users | read | channels | Get all the users who can view a private video. |
| PUT | channels/{id}/videos/{id}/privacy/users | write | channels | Permit a list of users to view a private video. |
| GET | channels/{id}/videos/{id}/texttracks | read | channels | Get all the text tracks of a video. |
| POST | channels/{id}/videos/{id}/texttracks | write | channels | Add a text track to a video. |
| GET | me/channels | read | channels | Get all the channels to which a user subscribes. |
| GET | me/channels/{id} | read | channels | Check if a user follows a channel. |
| PUT | me/channels/{id} | write | channels | Subscribe a user to a specific channel. |
| DELETE | me/channels/{id} | write | channels | Unsubscribe a user from a specific channel. |
| GET | users/{id}/channels | read | channels | Get all the channels to which a user subscribes. |
| GET | users/{id}/channels/{id} | read | channels | Check if a user follows a channel. |
| PUT | users/{id}/channels/{id} | write | channels | Subscribe a user to a specific channel. |
| DELETE | users/{id}/channels/{id} | write | channels | Unsubscribe a user from a specific channel. |
| GET | contentratings | read | content ratings | Get all content ratings. |
| GET | creativecommons | read | creative commons | Get all Creative Commons licenses. |
| GET | me/customlogos | read | custom logos | Get all the custom logos that belong to a user. |
| POST | me/customlogos | write | custom logos | Add a custom logo. |
| GET | me/customlogos/{id} | read | custom logos | Get a specific custom logo. |
| GET | users/{id}/customlogos | read | custom logos | Get all the custom logos that belong to a user. |
| POST | users/{id}/customlogos | write | custom logos | Add a custom logo. |
| GET | users/{id}/customlogos/{id} | read | custom logos | Get a specific custom logo. |
| GET | me/presets | read | embed presets | Get all the embed presets that a user has created. |
| GET | me/presets/{id} | read | embed presets | Get a specific embed preset. |
| PATCH | me/presets/{id} | write | embed presets | Edit an embed preset. |
| GET | me/presets/{id}/videos | read | embed presets | Get all the videos that have been added to an embed preset. |
| GET | users/{id}/presets | read | embed presets | Get all the embed presets that a user has created. |
| GET | users/{id}/presets/{id} | read | embed presets | Get a specific embed preset. |
| PATCH | users/{id}/presets/{id} | write | embed presets | Edit an embed preset. |
| GET | users/{id}/presets/{id}/videos | read | embed presets | Get all the videos that have been added to an embed preset. |
| GET | me/feed | read | feed | Get all the videos in a user's feed. |
| GET | users/{id}/feed | read | feed | Get all the videos in a user's feed. |
| GET | me/followers | read | followers | Get all the followers of a user. |
| GET | users/{id}/followers | read | followers | Get all the followers of a user. |
| GET | me/following | read | following | Get all the users that a user is following. |
| POST | me/following | write | following | Follow a list of users. |
| GET | me/following/{id} | read | following | Check if a user is following another user. |
| PUT | me/following/{id} | write | following | Follow a specific user. |
| DELETE | me/following/{id} | write | following | Unfollow a user. |
| GET | users/{id}/following | read | following | Get all the users that a user is following. |
| POST | users/{id}/following | write | following | Follow a list of users. |
| GET | users/{id}/following/{id} | read | following | Check if a user is following another user. |
| PUT | users/{id}/following/{id} | write | following | Follow a specific user. |
| DELETE | users/{id}/following/{id} | write | following | Unfollow a user. |
| GET | groups | read | groups | Get all groups. |
| POST | groups | write | groups | Create a group. |
| GET | groups/{id} | read | groups | Get a specific group. |
| DELETE | groups/{id} | write | groups | Delete a group. |
| GET | groups/{id}/users | read | groups | Get all the members of a group. |
| GET | groups/{id}/videos | read | groups | Get all the videos in a group. |
| GET | groups/{id}/videos/{id} | read | groups | Get a specific video in a group. |
| PUT | groups/{id}/videos/{id} | write | groups | Add a video to a group. |
| DELETE | groups/{id}/videos/{id} | write | groups | Remove a video from a group. |
| GET | me/groups | read | groups | Get all the groups that a user has joined. |
| GET | me/groups/{id} | read | groups | Check if a user has joined a group. |
| PUT | me/groups/{id} | write | groups | Add a user to a group. |
| DELETE | me/groups/{id} | write | groups | Remove a user from a group. |
| GET | users/{id}/groups | read | groups | Get all the groups that a user has joined. |
| GET | users/{id}/groups/{id} | read | groups | Check if a user has joined a group. |
| PUT | users/{id}/groups/{id} | write | groups | Add a user to a group. |
| DELETE | users/{id}/groups/{id} | write | groups | Remove a user from a group. |
| GET | languages | read | languages | Get all languages. |
| GET | me/likes | read | likes | Get all the videos that a user has liked. |
| GET | me/likes/{id} | read | likes | Check if a user has liked a video. |
| PUT | me/likes/{id} | write | likes | Cause a user to like a video. |
| DELETE | me/likes/{id} | write | likes | Cause a user to unlike a video. |
| GET | users/{id}/likes | read | likes | Get all the videos that a user has liked. |
| GET | users/{id}/likes/{id} | read | likes | Check if a user has liked a video. |
| PUT | users/{id}/likes/{id} | write | likes | Cause a user to like a video. |
| DELETE | users/{id}/likes/{id} | write | likes | Cause a user to unlike a video. |
| POST | oauth/access_token | write | oauth | Exchange an authorization code for an access token. |
| POST | oauth/authorize/client | write | oauth | Authorize a client with OAuth. |
| POST | oauth/authorize/vimeo_oauth1 | write | oauth | Convert OAuth 1 access tokens to OAuth 2 access tokens. |
| GET | oauth/verify | read | oauth | Verify an OAuth 2 token. |
| DELETE | tokens | write | oauth | Revoke the current access token. |
| GET | me/ondemand/pages | read | on demand | Get all the On Demand pages of a user. |
| POST | me/ondemand/pages | write | on demand | Create an On Demand page. |
| GET | me/ondemand/purchases | read | on demand | Get all the On Demand purchases and rentals that a user has made. |
| GET | me/ondemand/purchases/{id} | read | on demand | Check if a user has made a purchase or rental from an On Demand page. |
| GET | ondemand/genres | read | on demand | Get all On Demand genres. |
| GET | ondemand/genres/{id} | read | on demand | Get a specific On Demand genre. |
| GET | ondemand/genres/{id}/pages | read | on demand | Get all the On Demand pages in a genre. |
| GET | ondemand/genres/{id}/pages/{id} | read | on demand | Get a specific On Demand page in a genre. |
| GET | ondemand/pages/{id} | read | on demand | Get a specific On Demand page. |
| PATCH | ondemand/pages/{id} | write | on demand | Edit an On Demand page. |
| DELETE | ondemand/pages/{id} | write | on demand | Delete a draft of an On Demand page. |
| GET | ondemand/pages/{id}/backgrounds | read | on demand | Get all the backgrounds of an On Demand page. |
| POST | ondemand/pages/{id}/backgrounds | write | on demand | Add a background to an On Demand page. |
| GET | ondemand/pages/{id}/backgrounds/{id} | read | on demand | Get a specific background of an On Demand page. |
| PATCH | ondemand/pages/{id}/backgrounds/{id} | write | on demand | Edit a background of an On Demand page. |
| DELETE | ondemand/pages/{id}/backgrounds/{id} | write | on demand | Remove a background from an On Demand page. |
| GET | ondemand/pages/{id}/genres | read | on demand | Get all the genres of an On Demand page. |
| GET | ondemand/pages/{id}/genres/{id} | read | on demand | Check whether an On Demand page belongs to a genre. |
| PUT | ondemand/pages/{id}/genres/{id} | write | on demand | Add a genre to an On Demand page. |
| DELETE | ondemand/pages/{id}/genres/{id} | write | on demand | Remove a genre from an On Demand page. |
| GET | ondemand/pages/{id}/likes | read | on demand | Get all the users who have liked a video on an On Demand page. |
| GET | ondemand/pages/{id}/pictures | read | on demand | Get all the posters of an On Demand page. |
| POST | ondemand/pages/{id}/pictures | write | on demand | Add a poster to an On Demand page. |
| GET | ondemand/pages/{id}/pictures/{id} | read | on demand | Get a specific poster of an On Demand page. |
| PATCH | ondemand/pages/{id}/pictures/{id} | write | on demand | Edit a poster of an On Demand page. |
| GET | ondemand/pages/{id}/promotions | read | on demand | Get all the promotions on an On Demand page. |
| POST | ondemand/pages/{id}/promotions | write | on demand | Add a promotion to an On Demand page. |
| GET | ondemand/pages/{id}/promotions/{id} | read | on demand | Get a specific promotion on an On Demand page. |
| DELETE | ondemand/pages/{id}/promotions/{id} | write | on demand | Remove a promotion from an On Demand page. |
| GET | ondemand/pages/{id}/promotions/{id}/codes | write | on demand | Get all the codes of a promotion on an On Demand page. Kept out of read: returns redeemable promotion codes. |
| GET | ondemand/pages/{id}/regions | read | on demand | Get all the regions of an On Demand page. |
| PUT | ondemand/pages/{id}/regions | write | on demand | Add a list of regions to an On Demand page. |
| DELETE | ondemand/pages/{id}/regions | write | on demand | Remove a list of regions from an On Demand page. |
| GET | ondemand/pages/{id}/regions/{id} | read | on demand | Get a specific region of an On Demand page. |
| PUT | ondemand/pages/{id}/regions/{id} | write | on demand | Add a specific region to an On Demand page. |
| DELETE | ondemand/pages/{id}/regions/{id} | write | on demand | Remove a specific region from an On Demand page. |
| GET | ondemand/pages/{id}/seasons | read | on demand | Get all the seasons on an On Demand page. |
| GET | ondemand/pages/{id}/seasons/{id} | read | on demand | Get a specific season on an On Demand page. |
| GET | ondemand/pages/{id}/seasons/{id}/videos | read | on demand | Get all the videos in a season on an On Demand page. |
| GET | ondemand/pages/{id}/videos | read | on demand | Get all the videos on an On Demand page. |
| GET | ondemand/pages/{id}/videos/{id} | read | on demand | Get a specific video on an On Demand page. |
| PUT | ondemand/pages/{id}/videos/{id} | write | on demand | Add a video to an On Demand page. |
| DELETE | ondemand/pages/{id}/videos/{id} | write | on demand | Remove a video from an On Demand page. |
| GET | ondemand/regions | read | on demand | Get all the On Demand regions. |
| GET | ondemand/regions/{id} | read | on demand | Get a specific On Demand region. |
| GET | users/{id}/ondemand/pages | read | on demand | Get all the On Demand pages of a user. |
| POST | users/{id}/ondemand/pages | write | on demand | Create an On Demand page. |
| GET | users/{id}/ondemand/purchases | read | on demand | Check if a user has made a purchase or rental from an On Demand page. |
| GET | me/pictures | read | pictures | Get all the pictures that belong to a user. |
| POST | me/pictures | write | pictures | Add a user picture. |
| GET | me/pictures/{id} | read | pictures | Get a specific user picture. |
| PATCH | me/pictures/{id} | write | pictures | Edit a user picture. |
| DELETE | me/pictures/{id} | write | pictures | Delete a user picture. |
| GET | users/{id}/pictures | read | pictures | Get all the pictures that belong to a user. |
| POST | users/{id}/pictures | write | pictures | Add a user picture. |
| GET | users/{id}/pictures/{id} | read | pictures | Get a specific user picture. |
| PATCH | users/{id}/pictures/{id} | write | pictures | Edit a user picture. |
| DELETE | users/{id}/pictures/{id} | write | pictures | Delete a user picture. |
| GET | me/portfolios | read | portfolios | Get all the portfolios that belong to a user. |
| GET | me/portfolios/{id} | read | portfolios | Get a specific portfolio. |
| GET | me/portfolios/{id}/videos | read | portfolios | Get all the videos in a portfolio. |
| GET | me/portfolios/{id}/videos/{id} | read | portfolios | Get a specific video in a portfolio. |
| PUT | me/portfolios/{id}/videos/{id} | write | portfolios | Add a video to a portfolio. |
| DELETE | me/portfolios/{id}/videos/{id} | write | portfolios | Remove a video from a portfolio. |
| GET | users/{id}/portfolios | read | portfolios | Get all the portfolios that belong to a user. |
| GET | users/{id}/portfolios/{id} | read | portfolios | Get a specific portfolio. |
| GET | users/{id}/portfolios/{id}/videos | read | portfolios | Get all the videos in a portfolio. |
| GET | users/{id}/portfolios/{id}/videos/{id} | read | portfolios | Get a specific video in a portfolio. |
| PUT | users/{id}/portfolios/{id}/videos/{id} | write | portfolios | Add a video to a portfolio. |
| DELETE | users/{id}/portfolios/{id}/videos/{id} | write | portfolios | Remove a video from a portfolio. |
| GET | me/projects | read | projects | Get all the projects that belong to a user. |
| POST | me/projects | write | projects | Create a project. |
| GET | me/projects/{id} | read | projects | Get a specific project. |
| PATCH | me/projects/{id} | write | projects | Edit a project. |
| DELETE | me/projects/{id} | write | projects | Delete a project. |
| GET | me/projects/{id}/videos | read | projects | Get all the videos in a project. |
| PUT | me/projects/{id}/videos | write | projects | Add a list of videos to a project. |
| DELETE | me/projects/{id}/videos | write | projects | Remove a list of videos from a project. |
| PUT | me/projects/{id}/videos/{id} | write | projects | Add a specific video to a project. |
| DELETE | me/projects/{id}/videos/{id} | write | projects | Remove a specific video from a project. |
| GET | users/{id}/projects | read | projects | Get all the projects that belong to a user. |
| POST | users/{id}/projects | write | projects | Create a project. |
| GET | users/{id}/projects/{id} | read | projects | Get a specific project. |
| PATCH | users/{id}/projects/{id} | write | projects | Edit a project. |
| DELETE | users/{id}/projects/{id} | write | projects | Delete a project. |
| GET | users/{id}/projects/{id}/videos | read | projects | Get all the videos in a project. |
| PUT | users/{id}/projects/{id}/videos | write | projects | Add a list of videos to a project. |
| DELETE | users/{id}/projects/{id}/videos | write | projects | Remove a list of videos from a project. |
| PUT | users/{id}/projects/{id}/videos/{id} | write | projects | Add a specific video to a project. |
| DELETE | users/{id}/projects/{id}/videos/{id} | write | projects | Remove a specific video from a project. |
| GET | tags/{id} | read | tags | Get a specific tag. |
| GET | tags/{id}/videos | read | tags | Get all the videos with a specific tag. |
| GET | tutorial | read | tutorial | Get started with the Vimeo API. |
| GET | users/{id}/uploads/{id} | write | uploads | Get a user's upload attempt. Kept out of read: response includes the upload link that authorizes uploading. |
| DELETE | users/{id}/uploads/{id} | write | uploads | Complete a user's streaming upload. |
| GET | me | read | users | Get a user. |
| PATCH | me | write | users | Edit a user. |
| GET | users | read | users | Search for users. |
| GET | users/{id} | read | users | Get a user. |
| PATCH | users/{id} | write | users | Edit a user. |
| GET | me/videos | read | videos | Get all the videos that a user has uploaded. |
| POST | me/videos | write | videos | Upload a video. |
| GET | me/videos/{id} | read | videos | Check if a user owns a video. |
| GET | users/{id}/videos | read | videos | Get all the videos that a user has uploaded. |
| POST | users/{id}/videos | write | videos | Upload a video. |
| GET | users/{id}/videos/{id} | read | videos | Check if a user owns a video. |
| GET | videos | read | videos | Search for videos. |
| GET | videos/{id} | read | videos | Get a specific video. |
| PATCH | videos/{id} | write | videos | Edit a video. |
| DELETE | videos/{id} | write | videos | Delete a video. |
| GET | videos/{id}/available_albums | read | videos | Get all the albums to which a user can add or remove a specific video. |
| GET | videos/{id}/available_channels | read | videos | Get all the channels to which a user can add or remove a specific video. |
| GET | videos/{id}/categories | read | videos | Get all the categories to which a video belongs. |
| PUT | videos/{id}/categories | write | videos | Suggest categories for a video. |
| GET | videos/{id}/comments | read | videos | Get all the comments on a video. |
| POST | videos/{id}/comments | write | videos | Add a comment to a video. |
| GET | videos/{id}/comments/{id} | read | videos | Get a specific video comment. |
| PATCH | videos/{id}/comments/{id} | write | videos | Edit a video comment. |
| DELETE | videos/{id}/comments/{id} | write | videos | Delete a video comment. |
| GET | videos/{id}/comments/{id}/replies | read | videos | Get all the replies to a video comment. |
| POST | videos/{id}/comments/{id}/replies | write | videos | Add a reply to a video comment. |
| GET | videos/{id}/credits | read | videos | Get all the credited users in a video. |
| POST | videos/{id}/credits | write | videos | Credit a user in a video. |
| GET | videos/{id}/credits/{id} | read | videos | Get a specific credited user in a video. |
| PATCH | videos/{id}/credits/{id} | write | videos | Edit the credit for a user in a video. |
| DELETE | videos/{id}/credits/{id} | write | videos | Delete the credit for a user in a video. |
| GET | videos/{id}/likes | read | videos | Get all the users who have liked a video. |
| GET | videos/{id}/pictures | read | videos | Get all the thumbnails of a video. |
| POST | videos/{id}/pictures | write | videos | Add a video thumbnail. |
| GET | videos/{id}/pictures/{id} | read | videos | Get a specific video thumbnail. |
| PATCH | videos/{id}/pictures/{id} | write | videos | Edit a video thumbnail. |
| DELETE | videos/{id}/pictures/{id} | write | videos | Delete a video thumbnail. |
| GET | videos/{id}/presets/{id} | read | videos | Check if an embed preset has been added to a video. |
| PUT | videos/{id}/presets/{id} | write | videos | Add an embed preset to a video. |
| DELETE | videos/{id}/presets/{id} | write | videos | Remove an embed preset from a video. |
| GET | videos/{id}/privacy/domains | read | videos | Get all the domains on a video's whitelist. |
| PUT | videos/{id}/privacy/domains/{id} | write | videos | Add a domain to a video's whitelist. |
| DELETE | videos/{id}/privacy/domains/{id} | write | videos | Remove a domain from a video's whitelist. |
| GET | videos/{id}/privacy/users | read | videos | Get all the users who can view a private video. |
| PUT | videos/{id}/privacy/users | write | videos | Permit a list of users to view a private video. |
| PUT | videos/{id}/privacy/users/{id} | write | videos | Permit a specific user to view a private video. |
| DELETE | videos/{id}/privacy/users/{id} | write | videos | Restrict a user from viewing a private video. |
| GET | videos/{id}/tags | read | videos | Get all the tags of a video. |
| PUT | videos/{id}/tags | write | videos | Add a list of tags to a video. |
| GET | videos/{id}/tags/{id} | read | videos | Check if a tag has been added to a video. |
| PUT | videos/{id}/tags/{id} | write | videos | Add a specific tag to a video. |
| DELETE | videos/{id}/tags/{id} | write | videos | Remove a tag from a video. |
| GET | videos/{id}/texttracks | read | videos | Get all the text tracks of a video. |
| POST | videos/{id}/texttracks | write | videos | Add a text track to a video. |
| GET | videos/{id}/texttracks/{id} | read | videos | Get a specific text track. |
| PATCH | videos/{id}/texttracks/{id} | write | videos | Edit a text track. |
| DELETE | videos/{id}/texttracks/{id} | write | videos | Delete a text track. |
| POST | videos/{id}/timelinethumbnails | write | videos | Add a new timeline event thumbnail to a video. |
| GET | videos/{id}/timelinethumbnails/{id} | read | videos | Get a timeline event thumbnail. |
| POST | videos/{id}/versions | write | videos | Add a version to a video. |
| GET | videos/{id}/videos | read | videos | Get all the related videos of a video. |
| GET | me/watched/videos | read | watch history | Get all the videos that a user has watched. |
| DELETE | me/watched/videos | write | watch history | Delete a user's watch history. |
| DELETE | me/watched/videos/{id} | write | watch history | Delete a specific video from a user's watch history. |
| GET | me/watchlater | read | watch later | Get all the videos in a user's Watch Later queue. |
| GET | me/watchlater/{id} | read | watch later | Check if a user has added a specific video to their Watch Later queue. |
| PUT | me/watchlater/{id} | write | watch later | Add a video to a user's Watch Later queue. |
| DELETE | me/watchlater/{id} | write | watch later | Remove a video from a user's Watch Later queue. |
| GET | users/{id}/watchlater | read | watch later | Get all the videos in a user's Watch Later queue. |
| GET | users/{id}/watchlater/{id} | read | watch later | Check if a user has added a specific video to their Watch Later queue. |
| PUT | users/{id}/watchlater/{id} | write | watch later | Add a video to a user's Watch Later queue. |
| DELETE | users/{id}/watchlater/{id} | write | watch later | Remove a video from a user's Watch Later queue. |
