# twexapi-cli

A command-line client for twexapi APIs.

## What it supports

- Generic HTTP-style requests to twexapi paths
- Saved app configs for API keys and base URLs
- Saved profiles for cookies or `auth_token` values
- Convenience commands for users, about, search, followers/following, lists, tweets, and follow/unfollow
- Modular code layout under `src/` so config, parsing, requests, and commands evolve independently

## Install

Install globally from npm:

```bash
npm install -g twexapi-cli
twexapi --help
```

Requires Node.js 18 or newer.

## Quick start

Get your API key from the twexapi dashboard:

[twexapi dashboard](https://twexapi.io/dashboard)

Save an app config and make a first request:

```bash
twexapi auth apps add --name prod --api-key "twitterx_..."
twexapi auth apps use prod
twexapi --app prod about elonmusk
```

If you are developing from this repository, use:

```bash
cd /Users/jiangyong/code/twexapi-cli
node ./bin/twexapi.js --help
```

If you want a local executable command while developing from source:

```bash
npm link
twexapi --help
```

## Config management

When a request is missing an API key, the CLI will include that URL in the error output.

## Security notes

- The CLI reads `TWEXAPI_KEY`, `TWEXAPI_BASE_URL`, and `TWEXAPI_CONFIG_DIR` from the environment.
- The CLI reads and writes persistent config in `~/.twexapi/config.json` by default, or in the directory set by `--config-dir` or `TWEXAPI_CONFIG_DIR`.
- Saved app configs may contain API keys, and saved profiles may contain cookies, `auth_token`, or `ct0` in plain JSON on disk.
- Avoid storing long-lived credentials on shared machines or CI runners. Prefer an isolated config directory when testing.
- `auth cookie` builds a request path containing the `auth_token`, so treat logs, traces, and network boundaries accordingly.

Save an app config:

```bash
twexapi auth apps add --name prod --api-key "twitterx_..."
twexapi auth apps list
twexapi auth apps use prod
```

Save a write profile:

```bash
twexapi auth profiles add --name founder --cookie "ct0=...; auth_token=..."
twexapi auth profiles use founder
```

Create a profile from `auth_token` via the documented cookie endpoint:

```bash
twexapi auth cookie --auth-token "your_auth_token" --save-as founder
```

Inspect config:

```bash
twexapi config show
twexapi config path
```

By default config is stored in `~/.twexapi/config.json`. For testing, you can isolate it:

```bash
twexapi --config-dir ./.twexapi-local config show
```

## Request examples

Query an endpoint directly:

```bash
twexapi /twitter/elonmusk/about
```

Send a JSON body with a POST:

```bash
twexapi -X POST -d '["elonmusk","sama"]' /twitter/users
```

Preview a request without sending it:

```bash
twexapi --app prod --dry-run users elonmusk sama
twexapi --app prod --profile founder --dry-run tweet create --text "hello"
```

## Convenience commands

Read commands:

```bash
twexapi --app prod users elonmusk sama
twexapi --app prod about elonmusk
twexapi --app prod search tweets "founder" "ai" --count 20 --sort Latest
twexapi --app prod search users "openai" --count 20
twexapi --app prod followers elonmusk --count 100
twexapi --app prod following elonmusk --count 100
twexapi --app prod list search --query "ai founders" --count 20
twexapi --app prod list members 123456789 --count 100
twexapi --app prod list subscribers 123456789 --count 100
twexapi --app prod tweet lookup 1900000000000000000 1900000000000000001
twexapi --app prod tweet replies 1900000000000000000 --count 25 --sort Recency
```

Write commands:

```bash
twexapi --app prod --profile founder tweet create --text "hello from cli"
twexapi --app prod --profile founder tweet create --text "hello with image" --media-url "https://example.com/a.jpg"
twexapi --app prod --profile founder tweet quote --text "worth reading" --quote-url "https://x.com/user/status/123"
twexapi --app prod --profile founder tweet like 1900000000000000000
twexapi --app prod --profile founder tweet unlike 1900000000000000000
twexapi --app prod --profile founder tweet bookmark 1900000000000000000
twexapi --app prod --profile founder tweet unbookmark 1900000000000000000
twexapi --app prod --profile founder tweet retweet 1900000000000000000
twexapi --app prod --profile founder tweet unretweet 1900000000000000000
twexapi --app prod --profile founder list create --name "AI Builders" --description "Interesting builders" --private
twexapi --app prod --profile founder user follow someuser
twexapi --app prod --profile founder user unfollow someuser
```

## Project layout

```text
bin/twexapi.js         # thin executable entrypoint
src/index.js           # main boot flow
src/parser.js          # global option parsing
src/config.js          # config load/save and auth profile helpers
src/request.js         # HTTP execution and dry-run preview
src/commands.js        # command routing and endpoint mapping
src/help.js            # help text
src/constants.js       # defaults and option metadata
src/utils.js           # shared helpers
```

## Notes

- Global options such as `--app`, `--profile`, `--api-key`, and `--dry-run` should be placed before the command.
- For unsupported endpoints, use the generic `twexapi <path>` form.
- The CLI masks secrets in config output and dry-run previews.
- Direct local file upload for media is not included yet; the current CLI supports `--media-url` for tweet creation.
- DM commands are not included yet because I have not found a confirmed public DM endpoint in the twexapi docs we based this CLI on.
