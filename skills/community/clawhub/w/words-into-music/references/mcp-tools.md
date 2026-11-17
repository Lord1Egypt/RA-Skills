# MCP tool reference

Endpoint: `https://mcp.wordsintomusic.com/mcp`, using Streamable HTTP and OAuth. These are MCP tool names, not REST routes. With the connection named `words-into-music`, mcporter calls use `words-into-music.TOOL_NAME`. An MCP-capable host can call the tools directly instead.

Read the live schemas with `mcporter list words-into-music --schema` if the server reports an argument mismatch. Read the MCP result's `structuredContent` or JSON text content. Check `isError` before using response fields.

| Tool | Arguments | Result and credit behavior |
| --- | --- | --- |
| `get_account_usage` | `{}` | Available/reserved credits, supported languages and account links. No song-credit cost. |
| `prepare_song` | `requestId`, `input`, `uiLocale` | Returns `preparedRequestId`, normalized `input`, `songCreditCost: 1` and `expiresAt`. Saves a preparation for one hour without spending a song credit. |
| `start_song` | `preparedRequestId` | Returns `jobId`, `status` and `nextCheckAfterSeconds`. Reserves one existing credit. Repeating the same prepared ID returns the same job. |
| `get_song_job` | `jobId` | Reports progress. `ready` includes `song` with a private `url`. No song-credit cost. |
| `list_songs` | Optional `limit` 1–20, default 10; optional `cursor` | Paginated private library, newest first. No song-credit cost. |
| `get_song` | `id`; optional `includeLyrics`, default false | One owned song and private page URL. Lyrics only when requested. No song-credit cost. |

## Song input

| Field | Value |
| --- | --- |
| `mode` | `idea` or `lyrics`, default `idea` |
| `idea` | Up to 2,000 characters. Supply a brief in idea mode. |
| `lyrics` | Up to 4,000 characters. Supply the user's own words in lyrics mode. |
| `direction` | Required musical direction, at most 400 characters. |
| `language` | `en`, `es`, `de`, `fr`, `pt-BR`. Set it explicitly. |
| `instrumental` | Boolean, default false. When true, no sung lyrics are needed. |
| `title` | Optional, at most 100 characters. |
| `duration` | Integer seconds, 60–180, default 120. Target length, not an exact timing guarantee. |

`uiLocale` is outside `input`, uses the same language codes and controls existing completion-email localization. Emails remain subject to the user's account preference.

## Example calls

Read usage:

```sh
mcporter call words-into-music.get_account_usage --args '{}' --output json
```

Prepare the user's requested song. The literal ID below is an illustration; generate a new unique ID for each new brief and retain it for retries. Use a JSON serializer or a JSON file for actual user-provided lyrics rather than interpolating them into shell commands.

```sh
mcporter call words-into-music.prepare_song --args '{"requestId":"example-birthday-song-0001","input":{"mode":"idea","idea":"A birthday song for a friend who repairs everybody\u0027s bicycles and never asks for thanks.","lyrics":"","direction":"Warm acoustic pop, gentle drums, clear storytelling vocals, 96 BPM","language":"en","instrumental":false,"title":"The Spare Bicycle","duration":120},"uiLocale":"en"}' --output json
```

After showing the brief and one-credit cost and obtaining generation authorization, substitute the returned ID:

```sh
mcporter call words-into-music.start_song --args '{"preparedRequestId":"RETURNED_PREPARATION_ID"}' --output json
```

After at least 15 seconds, or the longer delay returned by the service:

```sh
mcporter call words-into-music.get_song_job --args '{"jobId":"RETURNED_JOB_ID"}' --output json
```

List a small page of existing songs only when requested:

```sh
mcporter call words-into-music.list_songs --args '{"limit":5}' --output json
```

Get one song. Use the ID from the library or job result; include lyrics only for a lyric request:

```sh
mcporter call words-into-music.get_song --args '{"id":"RETURNED_SONG_ID","includeLyrics":false}' --output json
```

## Completion and errors

`queued`, `generating` and `saving` are progress states. `ready` is completion; use the returned `song.url`. `failed` and `needs-attention` require stopping and reporting the outcome. If the host cannot poll across turns, preserve the job ID for the user's next check.

OAuth errors require reauthorization through the MCP client. Do not request the user's password or copy a website session cookie. Ownership errors do not authorize trying more IDs. Do not call private Convex or billing endpoints; this integration uses only the public MCP service.
