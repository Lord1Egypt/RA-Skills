# Shopify docs: Deploy

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Deploy

### Deploy

When you [deploy a Shopify app](https://shopify.dev/docs/apps/build/authentication-authorization), you're making your code available to merchants. This involves:

* Moving your code from your local development environment to a hosting service
* Connecting your hosted app to Shopify through the Partner Dashboard
* Managing app extensions and configurations separately through app versions

#### Hosting and deployment options

Common hosting providers for Shopify apps:

- [Deploy to Fly.io](http://Fly.io)
- [Deploy to Render](https://render.com/docs/deploy-shopify-app)
- Manual deployment

#### How to deploy manually

##### 1\. Create an app configuration file

Create or link your app to an `app.toml file`. Note down the `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, and `SCOPES` values.

```
shopify app config link
shopify app env show
```

##### 2\. Build your app

The Shopify Remix app template comes set up with Vite, which can build the bundles you'll need to host your app. If your provider doesn't support Docker, then you'll need to build the app yourself.

```
npm ci
npm run build
```

##### 3\. Set up your database

Now you'll decide which database you'll use, and where to host it. There are several cloud platforms that provide specialized database containers. You can use whichever storage strategy you're most comfortable working with.

##### 4\. Set up environment variables

Apps created using Shopify CLI use environment variables for configuration. To deploy your app, you'll need to set these values manually in your hosting provider. You'll need to set the variables that you obtained previously, along with some other values, in your production environment. The following environment variables need to be provided: `SHOPIFY_APP_URL`, `SHOPIFY_API_KEY`, `SHOPIFY_API_SECRET`, `SCOPES,PORT.`

##### 5\. Deploy your app

Before running the app on your hosting provider, you'll need to update your Shopify settings by deploying your TOML file using Shopify CLI.

## Storefront customization

Storefronts on Shopify give you the power to sell the way you want. Use the tools you already know to reach your customers wherever they are.

You can customize your Shopify storefront using different approaches:

1. Using Themes and Theme App Extensions
2. Building Custom Storefronts with Hydrogen and Oxygen, powered by the Storefront API

