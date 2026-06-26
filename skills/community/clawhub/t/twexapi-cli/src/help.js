export function printHelp() {
  console.log(`twexapi - command-line client for twexapi APIs

Usage:
  twexapi [global options] <path>
  twexapi [global options] users <username...>
  twexapi [global options] about <screen_name>
  twexapi [global options] search tweets <term...> [--count <n>] [--sort Latest|Top]
  twexapi [global options] search users <keyword> [--count <n>]
  twexapi [global options] followers <screen_name> [--count <n>]
  twexapi [global options] following <screen_name> [--count <n>]
  twexapi [global options] list search --query <text> [--count <n>]
  twexapi [global options] list create --name <name> --description <text> [--private]
  twexapi [global options] list members <list_id> [--count <n>]
  twexapi [global options] list subscribers <list_id> [--count <n>]
  twexapi [global options] tweet create --text <content> [--media-url <url>]
  twexapi [global options] tweet quote --text <content> --quote-url <url>
  twexapi [global options] tweet lookup <tweet_id...>
  twexapi [global options] tweet replies <tweet_id> [--count <n>] [--sort Relevance|Recency|Likes]
  twexapi [global options] tweet like <tweet_id>
  twexapi [global options] tweet unlike <tweet_id>
  twexapi [global options] tweet bookmark <tweet_id>
  twexapi [global options] tweet unbookmark <tweet_id>
  twexapi [global options] tweet retweet <tweet_id>
  twexapi [global options] tweet unretweet <tweet_id>
  twexapi [global options] user follow <username>
  twexapi [global options] user unfollow <username>
  twexapi [global options] auth apps add --name <name> --api-key <key> [--base-url <url>]
  twexapi [global options] auth profiles add --name <name> [--cookie <value> | --auth-token <value>]
  twexapi [global options] auth cookie --auth-token <token> [--save-as <profile>]
  twexapi [global options] config show

Examples:
  twexapi --app prod users elonmusk sama
  twexapi --profile founder tweet create --text "hello world" --media-url "https://example.com/image.jpg"
  twexapi --profile founder tweet like 1900000000000000000
  twexapi --app prod -X POST -d '["1900000000000000000"]' /twitter/tweets/lookup
  twexapi auth apps add --name prod --api-key "twitterx_..."
  twexapi auth profiles add --name founder --cookie "ct0=...; auth_token=..."
  twexapi auth cookie --auth-token "<auth_token>" --save-as founder
  twexapi config show

Global options:
  -X, --method <METHOD>       HTTP method for generic path requests, default GET
  -d, --data <JSON>           JSON body for generic path requests
  -H, --header <K:V>          Extra header for generic path requests, can be repeated
  --app <NAME>                Use a saved app config
  --profile <NAME>            Use a saved profile config
  --api-key <KEY>             Override API key for this request
  --base-url <URL>            Override base URL for this request
  --config-dir <DIR>          Override config directory, default ~/.twexapi
  --dry-run                   Print the request payload without sending it
  --raw                       Print response body without pretty JSON formatting
  -h, --help                  Show help

Notes:
  Global options should be placed before the command.
  Saved apps store API keys and base URLs.
  Saved profiles store cookies or auth_token values for write actions.
  Get API keys from https://twexapi.io/dashboard.
  Copy the API key from the dashboard and save it with auth apps add.
`);
}
