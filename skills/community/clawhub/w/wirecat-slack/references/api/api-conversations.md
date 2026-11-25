<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Slack API: conversations

## `slk api conversations archive [options]`

- What: conversations\_archive — destructive (POST /conversations.archive)
- Call: `POST /conversations.archive`, effect: destructive
- Permission keys: `chats.archive`, `slack.delete`
- Body: `ConversationsArchiveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations close [options]`

- What: conversations\_close — write (POST /conversations.close)
- Call: `POST /conversations.close`, effect: write
- Body: `ConversationsCloseRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations create [options]`

- What: conversations\_create — write (POST /conversations.create)
- Call: `POST /conversations.create`, effect: write
- Permission keys: `chats.create`
- Body: `ConversationsCreateRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations history [options]`

- What: conversations\_history — read (GET /conversations.history)
- Call: `GET /conversations.history`, effect: read
- Permission keys: `messages.list`
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `messages`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | yes | Conversation ID to fetch history for. |
| `--latest <value>` | no | End of time range of messages to include in results. |
| `--oldest <value>` | no | Start of time range of messages to include in results. |
| `--inclusive <value>` | no | Include messages with latest or oldest timestamp in results only when either timestamp is specified. |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the users list hasn't been reached. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--all` | no | read every page, as the API pages it |

## `slk api conversations info [options]`

- What: conversations\_info — read (GET /conversations.info)
- Call: `GET /conversations.info`, effect: read

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | yes | Conversation ID to learn more about |
| `--include-locale <value>` | no | Set this to \`true\` to receive the locale for this conversation. Defaults to \`false\` |
| `--include-num-members <value>` | no | Set to \`true\` to include the member count for the specified conversation. Defaults to \`false\` |

## `slk api conversations invite [options]`

- What: conversations\_invite — write (POST /conversations.invite)
- Call: `POST /conversations.invite`, effect: write
- Permission keys: `chats.members.add`
- Body: `ConversationsInviteRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations join [options]`

- What: conversations\_join — write (POST /conversations.join)
- Call: `POST /conversations.join`, effect: write
- Permission keys: `chats.join`
- Body: `ConversationsJoinRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations kick [options]`

- What: conversations\_kick — destructive (POST /conversations.kick)
- Call: `POST /conversations.kick`, effect: destructive
- Permission keys: `chats.members.remove`, `slack.delete`
- Body: `ConversationsKickRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations leave [options]`

- What: conversations\_leave — destructive (POST /conversations.leave)
- Call: `POST /conversations.leave`, effect: destructive
- Permission keys: `chats.leave`, `slack.delete`
- Body: `ConversationsLeaveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations list [options]`

- What: conversations\_list — read (GET /conversations.list)
- Call: `GET /conversations.list`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `channels`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--exclude-archived <value>` | no | Set to \`true\` to exclude archived channels from the list |
| `--types <value>` | no | Mix and match channel types by providing a comma-separated list of any combination of \`public\_channel\`, \`private\_channel\`, \`mpim\`, \`im\` |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the list hasn't been reached. Must be an integer no larger than 1000. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--all` | no | read every page, as the API pages it |

## `slk api conversations mark [options]`

- What: conversations\_mark — write (POST /conversations.mark)
- Call: `POST /conversations.mark`, effect: write
- Permission keys: `chats.mark-read`
- Body: `ConversationsMarkRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations members [options]`

- What: conversations\_members — read (GET /conversations.members)
- Call: `GET /conversations.members`, effect: read
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `members`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | yes | ID of the conversation to retrieve members for |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the users list hasn't been reached. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--all` | no | read every page, as the API pages it |

## `slk api conversations open [options]`

- What: conversations\_open — write (POST /conversations.open)
- Call: `POST /conversations.open`, effect: write
- Body: `ConversationsOpenRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations rename [options]`

- What: conversations\_rename — write (POST /conversations.rename)
- Call: `POST /conversations.rename`, effect: write
- Permission keys: `chats.update`
- Body: `ConversationsRenameRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations replies [options]`

- What: conversations\_replies — read (GET /conversations.replies)
- Call: `GET /conversations.replies`, effect: read
- Permission keys: `messages.list`
- Pages: cursor: send `cursor` (query), read the next one from `response_metadata.next_cursor`; items in `messages`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--channel <value>` | yes | Conversation ID to fetch thread from. |
| `--ts <value>` | yes | Unique identifier of a thread's parent message. \`ts\` must be the timestamp of an existing message with 0 or more replies. If there are no replies then just the single message referenced by \`ts\` will return - it is just an ordinary, unthreaded message. |
| `--latest <value>` | no | End of time range of messages to include in results. |
| `--oldest <value>` | no | Start of time range of messages to include in results. |
| `--inclusive <value>` | no | Include messages with latest or oldest timestamp in results only when either timestamp is specified. |
| `--limit <value>` | no | The maximum number of items to return. Fewer than the requested number of items may be returned, even if the end of the users list hasn't been reached. |
| `--cursor <value>` | no | Paginate through collections of data by setting the \`cursor\` parameter to a \`next\_cursor\` attribute returned by a previous request's \`response\_metadata\`. Default value fetches the first "page" of the collection. See \[pagination\](https://api.slack.com/docs/pagination) for more detail. |
| `--all` | no | read every page, as the API pages it |

## `slk api conversations set-purpose [options]`

- What: conversations\_setPurpose — write (POST /conversations.setPurpose)
- Call: `POST /conversations.setPurpose`, effect: write
- Permission keys: `chats.update`
- Body: `ConversationsSetPurposeRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations set-topic [options]`

- What: conversations\_setTopic — write (POST /conversations.setTopic)
- Call: `POST /conversations.setTopic`, effect: write
- Permission keys: `chats.update`
- Body: `ConversationsSetTopicRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `slk api conversations unarchive [options]`

- What: conversations\_unarchive — write (POST /conversations.unarchive)
- Call: `POST /conversations.unarchive`, effect: write
- Permission keys: `chats.unarchive`
- Body: `ConversationsUnarchiveRequest`

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
