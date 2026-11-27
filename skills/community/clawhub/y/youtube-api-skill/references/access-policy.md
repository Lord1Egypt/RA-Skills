# YouTube access policy

An access policy limits which endpoints YouTube connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/youtube#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for YouTube: its 29 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create youtube --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "youtube/v3/activities"},
    {"method": "GET", "path": "youtube/v3/captions"},
    {"method": "GET", "path": "youtube/v3/captions/{id}"},
    {"method": "GET", "path": "youtube/v3/channelSections"},
    {"method": "GET", "path": "youtube/v3/channels"},
    {"method": "GET", "path": "youtube/v3/commentThreads"},
    {"method": "GET", "path": "youtube/v3/comments"},
    {"method": "GET", "path": "youtube/v3/i18nLanguages"},
    {"method": "GET", "path": "youtube/v3/i18nRegions"},
    {"method": "GET", "path": "youtube/v3/liveBroadcasts"},
    {"method": "GET", "path": "youtube/v3/liveChat/messages"},
    {"method": "GET", "path": "youtube/v3/liveChat/moderators"},
    {"method": "GET", "path": "youtube/v3/liveStreams"},
    {"method": "GET", "path": "youtube/v3/members"},
    {"method": "GET", "path": "youtube/v3/membershipsLevels"},
    {"method": "GET", "path": "youtube/v3/playlistImages"},
    {"method": "GET", "path": "youtube/v3/playlistItems"},
    {"method": "GET", "path": "youtube/v3/playlists"},
    {"method": "GET", "path": "youtube/v3/search"},
    {"method": "GET", "path": "youtube/v3/subscriptions"},
    {"method": "GET", "path": "youtube/v3/superChatEvents"},
    {"method": "GET", "path": "youtube/v3/thirdPartyLinks"},
    {"method": "GET", "path": "youtube/v3/liveChat/messages/stream"},
    {"method": "GET", "path": "youtube/v3/videoAbuseReportReasons"},
    {"method": "GET", "path": "youtube/v3/videoCategories"},
    {"method": "GET", "path": "youtube/v3/videoTrainability"},
    {"method": "GET", "path": "youtube/v3/videos"},
    {"method": "GET", "path": "youtube/v3/videos/getRating"},
    {"method": "GET", "path": "youtube/v3/videos:batchGetStats"}
  ],
  "deny": []
}
```

## Endpoints

The YouTube endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| POST | youtube/v3/abuseReports | write | abuseReports | Inserts a new resource into this collection. |
| GET | youtube/v3/activities | read | activities | Retrieves a list of resources, possibly filtered. |
| POST | upload/youtube/v3/captions | write | captions | Inserts a new resource into this collection. (media upload) |
| PUT | upload/youtube/v3/captions | write | captions | Updates an existing resource. (media upload) |
| GET | youtube/v3/captions | read | captions | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/captions | write | captions | Inserts a new resource into this collection. |
| PUT | youtube/v3/captions | write | captions | Updates an existing resource. |
| DELETE | youtube/v3/captions | write | captions | Deletes a resource. |
| GET | youtube/v3/captions/{id} | read | captions | Downloads a caption track. |
| POST | upload/youtube/v3/channelBanners/insert | write | channelBanners | Inserts a new resource into this collection. (media upload) |
| POST | youtube/v3/channelBanners/insert | write | channelBanners | Inserts a new resource into this collection. |
| GET | youtube/v3/channelSections | read | channelSections | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/channelSections | write | channelSections | Inserts a new resource into this collection. |
| PUT | youtube/v3/channelSections | write | channelSections | Updates an existing resource. |
| DELETE | youtube/v3/channelSections | write | channelSections | Deletes a resource. |
| GET | youtube/v3/channels | read | channels | Retrieves a list of resources, possibly filtered. |
| PUT | youtube/v3/channels | write | channels | Updates an existing resource. |
| GET | youtube/v3/commentThreads | read | commentThreads | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/commentThreads | write | commentThreads | Inserts a new resource into this collection. |
| GET | youtube/v3/comments | read | comments | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/comments | write | comments | Inserts a new resource into this collection. |
| PUT | youtube/v3/comments | write | comments | Updates an existing resource. |
| DELETE | youtube/v3/comments | write | comments | Deletes a resource. |
| POST | youtube/v3/comments/markAsSpam | write | comments | Expresses the caller's opinion that one or more comments should be flagged as spam. |
| POST | youtube/v3/comments/setModerationStatus | write | comments | Sets the moderation status of one or more comments. |
| GET | youtube/v3/i18nLanguages | read | i18nLanguages | Retrieves a list of resources, possibly filtered. |
| GET | youtube/v3/i18nRegions | read | i18nRegions | Retrieves a list of resources, possibly filtered. |
| GET | youtube/v3/liveBroadcasts | read | liveBroadcasts | Retrieve the list of broadcasts associated with the given channel. |
| POST | youtube/v3/liveBroadcasts | write | liveBroadcasts | Inserts a new stream for the authenticated user. |
| PUT | youtube/v3/liveBroadcasts | write | liveBroadcasts | Updates an existing broadcast for the authenticated user. |
| DELETE | youtube/v3/liveBroadcasts | write | liveBroadcasts | Delete a given broadcast. |
| POST | youtube/v3/liveBroadcasts/bind | write | liveBroadcasts | Bind a broadcast to a stream. |
| POST | youtube/v3/liveBroadcasts/cuepoint | write | liveBroadcasts | Insert cuepoints in a broadcast |
| POST | youtube/v3/liveBroadcasts/transition | write | liveBroadcasts | Transition a broadcast to a given status. |
| POST | youtube/v3/liveChat/bans | write | liveChatBans | Inserts a new resource into this collection. |
| DELETE | youtube/v3/liveChat/bans | write | liveChatBans | Deletes a chat ban. |
| GET | youtube/v3/liveChat/messages | read | liveChatMessages | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/liveChat/messages | write | liveChatMessages | Inserts a new resource into this collection. |
| DELETE | youtube/v3/liveChat/messages | write | liveChatMessages | Deletes a chat message. |
| POST | youtube/v3/liveChat/messages/transition | write | liveChatMessages | Transitions a durable chat event. |
| GET | youtube/v3/liveChat/moderators | read | liveChatModerators | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/liveChat/moderators | write | liveChatModerators | Inserts a new resource into this collection. |
| DELETE | youtube/v3/liveChat/moderators | write | liveChatModerators | Deletes a chat moderator. |
| GET | youtube/v3/liveStreams | read | liveStreams | Retrieve the list of streams associated with the given channel. |
| POST | youtube/v3/liveStreams | write | liveStreams | Inserts a new stream for the authenticated user. |
| PUT | youtube/v3/liveStreams | write | liveStreams | Updates an existing stream for the authenticated user. |
| DELETE | youtube/v3/liveStreams | write | liveStreams | Deletes an existing stream for the authenticated user. |
| GET | youtube/v3/members | read | members | Retrieves a list of members that match the request criteria for a channel. |
| GET | youtube/v3/membershipsLevels | read | membershipsLevels | Retrieves a list of all pricing levels offered by a creator to the fans. |
| POST | upload/youtube/v3/playlistImages | write | playlistImages | Inserts a new resource into this collection. (media upload) |
| PUT | upload/youtube/v3/playlistImages | write | playlistImages | Updates an existing resource. (media upload) |
| GET | youtube/v3/playlistImages | read | playlistImages | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/playlistImages | write | playlistImages | Inserts a new resource into this collection. |
| PUT | youtube/v3/playlistImages | write | playlistImages | Updates an existing resource. |
| DELETE | youtube/v3/playlistImages | write | playlistImages | Deletes a resource. |
| GET | youtube/v3/playlistItems | read | playlistItems | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/playlistItems | write | playlistItems | Inserts a new resource into this collection. |
| PUT | youtube/v3/playlistItems | write | playlistItems | Updates an existing resource. |
| DELETE | youtube/v3/playlistItems | write | playlistItems | Deletes a resource. |
| GET | youtube/v3/playlists | read | playlists | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/playlists | write | playlists | Inserts a new resource into this collection. |
| PUT | youtube/v3/playlists | write | playlists | Updates an existing resource. |
| DELETE | youtube/v3/playlists | write | playlists | Deletes a resource. |
| GET | youtube/v3/search | read | search | Retrieves a list of search resources |
| GET | youtube/v3/subscriptions | read | subscriptions | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/subscriptions | write | subscriptions | Inserts a new resource into this collection. |
| DELETE | youtube/v3/subscriptions | write | subscriptions | Deletes a resource. |
| GET | youtube/v3/superChatEvents | read | superChatEvents | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/tests | write | tests | POST method. |
| GET | youtube/v3/thirdPartyLinks | read | thirdPartyLinks | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/thirdPartyLinks | write | thirdPartyLinks | Inserts a new resource into this collection. |
| PUT | youtube/v3/thirdPartyLinks | write | thirdPartyLinks | Updates an existing resource. |
| DELETE | youtube/v3/thirdPartyLinks | write | thirdPartyLinks | Deletes a resource. |
| POST | upload/youtube/v3/thumbnails/set | write | thumbnails | As this is not an insert in a strict sense (it supports uploading/setting of a thumbnail for multiple videos, which doesn't result in creation of a single resou (media upload) |
| POST | youtube/v3/thumbnails/set | write | thumbnails | As this is not an insert in a strict sense (it supports uploading/setting of a thumbnail for multiple videos, which doesn't result in creation of a single resou |
| GET | youtube/v3/liveChat/messages/stream | read | v3 | Allows a user to load live chat through a server-streamed RPC. |
| GET | youtube/v3/videoAbuseReportReasons | read | videoAbuseReportReasons | Retrieves a list of resources, possibly filtered. |
| GET | youtube/v3/videoCategories | read | videoCategories | Retrieves a list of resources, possibly filtered. |
| GET | youtube/v3/videoTrainability | read | videoTrainability | Returns the trainability status of a video. |
| POST | upload/youtube/v3/videos | write | videos | Inserts a new resource into this collection. (media upload) |
| GET | youtube/v3/videos | read | videos | Retrieves a list of resources, possibly filtered. |
| POST | youtube/v3/videos | write | videos | Inserts a new resource into this collection. |
| PUT | youtube/v3/videos | write | videos | Updates an existing resource. |
| DELETE | youtube/v3/videos | write | videos | Deletes a resource. |
| GET | youtube/v3/videos/getRating | read | videos | Retrieves the ratings that the authorized user gave to a list of specified videos. |
| POST | youtube/v3/videos/rate | write | videos | Adds a like or dislike rating to a video or removes a rating from a video. |
| POST | youtube/v3/videos/reportAbuse | write | videos | Report abuse for a video. |
| GET | youtube/v3/videos:batchGetStats | read | videos | Retrieves a batch of VideoStat resources, possibly filtered. |
| POST | upload/youtube/v3/watermarks/set | write | watermarks | Allows upload of watermark image and setting it for a channel. (media upload) |
| POST | youtube/v3/watermarks/set | write | watermarks | Allows upload of watermark image and setting it for a channel. |
| POST | youtube/v3/watermarks/unset | write | watermarks | Allows removal of channel watermark. |
