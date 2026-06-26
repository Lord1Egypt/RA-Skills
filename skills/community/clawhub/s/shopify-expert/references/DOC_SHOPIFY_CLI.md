# Shopify docs: Shopify Cli

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Shopify CLI

### Shopify CLI

The [Shopify CLI](https://shopify.dev/docs/api/shopify-cli) is a command-line interface tool that helps you generate and work with Shopify apps, themes and custom storefronts. You can also use it to automate many common development tasks. Using the CLI makes it faster and easier to build on Shopify.

The general syntax for CLI commands is:

```
shopify [topic] [command]
```

Here are some examples of common commands:

* Install the Shopify CLI: `npm install -g @shopify/cli@latest`
* Create a new app: `shopify app init`
* Serve your app locally: `shopify app dev`
* Deploy your app: `shopify app deploy`
* Retrieve your theme files from Shopify: `shopify theme pull`
* Upload your theme to preview it: `shopify theme dev`
* Generate an extension: `shopify app generate extension`

You can find all the commands in the Shopify dev docs:

* [App commands](https://shopify.dev/docs/api/shopify-cli/app)
* [Theme commands](https://shopify.dev/docs/api/shopify-cli/theme)
* [Hydrogen commands](https://shopify.dev/docs/api/shopify-cli/hydrogen)
* [General commands](https://shopify.dev/docs/api/shopify-cli/general-commands)

You can also use `shopify help` to get help within the CLI.

