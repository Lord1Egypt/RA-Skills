# Shopify docs: Headless Storefront

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Headless and custom storefronts

### Headless and custom storefronts

#### Storefront GraphQL API

The [Storefront API](https://shopify.dev/docs/api/storefront) is the foundational layer of custom storefronts. It provides you the commerce primitives to build custom, scalable, and performant shopping experiences.

##### How it works

The Storefront API provides access to Shopify's primitives and capabilities such as displaying products and collections, adding items to the cart, calculating contextual pricing, and more. You can use the Storefront API to build unique commerce experiences on any platform, including the web, native apps, games, and social media, using the frontend tools of your choice.

Because the Storefront API uses the Shopify backend, you can focus on building a unique and customized shopping experience with strong brand representation. You can create custom pages, themes, and order management experiences that are fully integrated with a storefront.

##### Authentication and authorization

There are two methods of authentication for the Storefront API:

* **Public authentication**: The public token is used for client side queries and mutations. As every buyer has a different IP, the token scales to support large amounts of traffic.
* **Private access**: The private token provides authenticated access to the Storefront API and is used for server-side queries and mutations.

##### Endpoints and queries

The Storefront API is available only in GraphQL. All Storefront API queries are made on a single GraphQL endpoint, which only accepts POST requests:

```
https://{store_name}.myshopify.com/api/2025-01/graphql.json
```

The Storefront API is versioned, with new releases four times a year. To keep your app stable, make sure that you specify a supported version in the URL.

##### Example query

```
# Get the ID and title of the three most recently added products
curl -X POST \
  https://{store_name}.myshopify.com/api/2024-10/graphql.json \
  -H 'Content-Type: application/json' \
  -H 'X-Shopify-Storefront-Access-Token: {storefront_access_token}' \
  -d '{
    "query": "{
      products(first: 3) {
        edges {
          node {
            id
            title
          }
        }
      }
    }"
  }'
```

#### Hydrogen apps

Hydrogen and Oxygen make up Shopify's recommended stack for headless commerce. The different parts of the system work together to make it faster and easier to build and deploy headless Shopify stores.

[Hydrogen](https://shopify.dev/docs/api/hydrogen) is a set of components, utilities, and design patterns that make it easier to work with Shopify APIs. Hydrogen projects are Remix apps that are preconfigured with Shopify-specific features and functionality. Hydrogen handles API client credentials, provides off-the-shelf components that are pre-wired for Shopify API data, and includes CLI tooling for local development, testing, and deployment.

##### Project structure

Hydrogen projects are structured like typical Remix apps and you can configure them to your preferences. The following is the default quickstart project structure:

```
📂 hydrogen-quickstart/
├── 📁 app/
│   ├── 📁 assets/
│   ├── 📁 components/
│   ├── 📁 graphql/
│   ├── 📁 lib/
│   ├── 📁 routes/
│   ├── 📁 styles/
│   ├── entry.client.jsx
│   ├── entry.server.jsx
│   └── root.jsx
├── 📁 public/
├── CHANGELOG.md
├── README.md
├── customer-accountapi.generated.d.ts
├── env.d.ts
├── jsconfig.json
├── package.json
├── postcss.config.js
├── server.js
├── storefrontapi.generated.d.ts
└── vite.config.js
```

##### Packages and dependencies

Hydrogen bundles a set of dependencies that work together to enable end-to-end development and deployment:

| Package | Description |
| :---- | :---- |
| `@shopify/hydrogen` | Main Hydrogen package. Contains Remix-specific components and utilities for interacting with Shopify APIs. Extends the framework-agnostic `@shopify/hydrogen-react` package. |
| `@shopify/hydrogen-cli` | CLI tool for working with Hydrogen projects |
| `@shopify/mini-oxygen` | Local development server based on Oxygen |
| `@shopify/remix-oxygen` | Remix adapter that enables Hydrogen to be served on Oxygen |

##### Hydrogen channel

The Hydrogen sales channel app needs to be installed on your Shopify store to enable the following features:

* A Hydrogen sales channel where you can publish product inventory.
* Oxygen hosting, to deploy your Hydrogen projects.
* Managing storefronts and deployment environments, including environment variable management.
* Access to deployment logs.

#### Deploy to Oxygen

A deployment is an immutable snapshot of your Hydrogen app, running on [Oxygen](https://shopify.dev/docs/storefronts/headless/hydrogen/getting-started). Every deployment has its own unique preview URL so that you can view, test, or approve changes before merging them and deploying to production. You can also deploy to specific environments.

##### Continuous deployment

Developers typically prefer automated systems that deploy their app whenever they update its code base. These types of workflows are broadly known as continuous integration or continuous delivery/deployment (CI/CD) systems. Hydrogen and Oxygen support CI/CD with GitHub out of the box. You can also create your own CI/CD workflows using the Hydrogen CLI.

##### Manual deployment

You can create a new deployment from your local development environment with the Hydrogen CLI deploy command. The Hydrogen CLI builds, uploads, and deploys your app, then returns the deployment's unique URL.

```
npx shopify hydrogen deploy
```

Consult the Hydrogen CLI reference for the complete list of options for the `deploy` command.

##### Shareable links

Deployments are private by default, which means that you need to be logged in to your store to view them. You can create shareable links that allow anyone to view deployments, even if they’re not logged in.

##### Deployment rollbacks

By default, environment URLs point to the environment’s most recent deployment. If the most recent update contains a bug or other error, you can temporarily roll back to a previous deployment while you work on a fix. Rolling back doesn't redeploy or delete any deployments; it simply changes which deployment the environment URL points to.

Oxygen deployments are immutable, which means that their environment variables could be outdated. Always verify that a previous deployment works as expected before rolling back to it.

##### Redeployments

Redeploying an Oxygen environment creates a new deployment that re-uses the original deployment's immutable code, but injects the current set of environment variables. Redeployments are available for production and custom environments, but not the preview environment. When you edit an environment variable in the Shopify admin, you'll be prompted with the option to redeploy the relevant environments, but you can redeploy at any time.

##### Deployment immutability

Every deployment in Oxygen is immutable: each deployment is a snapshot of your Hydrogen project's codebase at a specific point in time. Typically, that snapshot is an individual Git commit. Deployments retain all the environment variables that they had when they were first deployed. If you update your environment variables, then older deployments won't use the updated values until you redeploy.

