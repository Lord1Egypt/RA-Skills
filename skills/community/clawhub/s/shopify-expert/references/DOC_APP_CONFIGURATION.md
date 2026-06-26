# Shopify docs: App Configuration

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Configuration and shopify.app.toml

### Configuration and shopify.app.toml

When you initialize an app using the CLI (shopify app init CLI command) you will receive a folder structure that contains a `shopify.app.toml` file at the root. This file helps you describe what capabilities you want your app to have and Shopify ensures that this app configuration is then instantiated on every shop where the app is installed.

You can use scopes to configure the scopes that your app requires, and webhook subscriptions to detail out what events your app should receive.

```
name = "Example App"
client_id = "a61950a2cbd5f32876b0b55587ec7a27"
application_url = "https://www.app.example.com/"
embedded = true
handle = "example-app"

[access_scopes]
scopes = "read_products, write_products"

[access.admin]
direct_api_mode = "online"

[auth]
redirect_urls = [
  "https://app.example.com/api/auth/callback",
  "https://app.example.com/api/auth/oauth/callback",
]

[webhooks]
api_version = "2024-01"

[[webhooks.subscriptions]]
topics = [ "app/uninstalled" ]
compliance_topics = [ "customers/redact", "customers/data_request", "shop/redact" ]
uri = "/webhooks"

[app_proxy]
url = "https://app.example.com/api/proxy"
subpath = "store-pickup"
prefix = "apps"

[pos]
embedded = false

[app_preferences]
url = "https://www.app.example.com/preferences"

[build]
automatically_update_urls_on_dev = false

```

If you are working with multiple environments (dev, staging, production) it is recommended that you have a different `shopify.app.toml` file for each environment.  The Shopify CLI makes this easy by allowing you to link multiple Shopify apps to your codebase, so that you can dedicate specific apps and their configuration for various development, staging, and production workflows.

You would create a new configuration using the command `shopify app config link` and then you can tell the CLI to use a specific configuration with the use command and so if you had a TOML configuration called `development` you would say `shopify app config use development` in the CLI.

For more, see [App configuration](https://shopify.dev/docs/apps/build/cli-for-apps/app-configuration) and [Manage app config files](https://shopify.dev/docs/apps/build/cli-for-apps/manage-app-config-files).

