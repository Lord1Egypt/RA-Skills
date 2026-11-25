<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: files

## `slk api files comments-delete [options]`

- What: files\_comments\_delete — destructive (POST /files.comments.delete)
- Call: `POST /files.comments.delete`, effect: destructive
- Permission keys: `slack.delete`
- Body: `FilesCommentsDeleteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api files delete [options]`

- What: files\_delete — destructive (POST /files.delete)
- Call: `POST /files.delete`, effect: destructive
- Permission keys: `slack.delete`
- Body: `FilesDeleteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api files info [options]`

- What: files\_info — read (GET /files.info)
- Call: `GET /files.info`, effect: read
- Permission keys: `messages.list`
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--file <value>` | no | Specify a file by providing its ID. |
| `--count <value>` | no | count |
| `--page <value>` | no | page |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached. |
| `--cursor <value>` | no | Parameter for pagination. File comments are paginated for a single file. Set \`cursor\` equal to the \`next\_cursor\` attribute returned by the previous request's \`response\_metadata\`. This parameter is optional, but pagination is mandatory: the default value simply fetches the first "page" of the collection of comments. See \[pagination\](https://api.slack.com/docs/pagination) for more details. |
| `--all` | no | read every page, as the API pages it |

## `slk api files list [options]`

- What: files\_list — read (GET /files.list)
- Call: `GET /files.list`, effect: read
- Permission keys: `messages.list`
- Pages: page number: send `page` (query), one more for each page; items in `files`; page size in `count` (query)

| Flag | Required | What |
|---|---|---|
| `--user <value>` | no | Filter files created by a single user. |
| `--channel <value>` | no | Filter files appearing in a specific channel, indicated by its ID. |
| `--ts-from <value>` | no | Filter files created after this timestamp (inclusive). |
| `--ts-to <value>` | no | Filter files created before this timestamp (inclusive). |
| `--types <value>` | no | Filter files by type (see below). You can pass multiple values in the types argument, like \`types=spaces,snippets\`.The default value is \`all\`, which does not filter the list. |
| `--count <value>` | no | count |
| `--page <value>` | no | page |
| `--show-files-hidden-by-limit <value>` | no | Show truncated file info for files hidden due to being too old, and the team who owns the file being over the file limit. |
| `--all` | no | read every page, as the API pages it |

## `slk api files remote-info [options]`

- What: files\_remote\_info — read (GET /files.remote.info)
- Call: `GET /files.remote.info`, effect: read

| Flag | Required | What |
|---|---|---|
| `--file <value>` | no | Specify a file by providing its ID. |
| `--external-id <value>` | no | Creator defined GUID for the file. |

## `slk api files remote-list [options]`

- What: files\_remote\_list — read (GET /files.remote.list)
- Call: `GET /files.remote.list`, effect: read

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | no | Filter files appearing in a specific channel, indicated by its ID. |
| `--ts-from <value>` | no | Filter files created after this timestamp (inclusive). |
| `--ts-to <value>` | no | Filter files created before this timestamp (inclusive). |
| `--limit <value>` | no | The maximum number of items to return. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |

## `slk api files remote-share [options]`

- What: files\_remote\_share — write (GET /files.remote.share)
- Call: `GET /files.remote.share`, effect: write

| Flag | Required | What |
|---|---|---|
| `--file <value>` | no | Specify a file registered with Slack by providing its ID. Either this field or \`external\_id\` or both are required. |
| `--external-id <value>` | no | The globally unique identifier (GUID) for the file, as set by the app registering the file with Slack.  Either this field or \`file\` or both are required. |
| `--channels <value>` | no | Comma-separated list of channel IDs where the file will be shared. |

## `slk api files revoke-public-url [options]`

- What: files\_revokePublicURL — destructive (POST /files.revokePublicURL)
- Call: `POST /files.revokePublicURL`, effect: destructive
- Permission keys: `slack.delete`
- Body: `FilesRevokePublicURLRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api files shared-public-url [options]`

- What: files\_sharedPublicURL — write (POST /files.sharedPublicURL)
- Call: `POST /files.sharedPublicURL`, effect: write
- Permission keys: `slack.share`
- Body: `FilesSharedPublicURLRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
