# Shopify docs: Platform Authentication

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Authentication

### Authentication

[Authentication](https://shopify.dev/docs/apps/build/authentication-authorization) is the process of verifying the identity of the user or the app. To keep transactions on Shopify’s platform safe and secure, all apps connecting with Shopify APIs must authenticate when making API requests.

Authorization is the process of giving permissions to apps. When an app user installs a Shopify app they authorize the app, enabling the app to acquire an access token. For example, an app might be authorized to access orders and product data in a store.

#### Types of authentication and authorization methods

The authentication and authorization methods that your app needs to use depends on the tool that you used to create your app, and the components that your app uses.

##### Authentication

* Embedded apps need to authenticate their incoming requests with session tokens.
* Apps that are not embedded need to implement their own authentication method for incoming requests.

##### Authorization

Authorization encompasses the installation of an app and the means to acquire an access token.

To avoid unnecessary redirects and page flickers during the app installation process, you should configure your app's required access scopes using Shopify CLI. This allows Shopify to manage the installation process for you.

If you aren't able to use Shopify CLI to configure your app, then your app will install as part of the authorization code grant flow. This provides a degraded user experience.

The following table outlines the supported installation and token acquisition flows for various app configurations. Whenever possible, you should create embedded apps that use Shopify managed installation and token exchange.

| Type of app | Supported installation flows | Supported token acquisition flows |
| :---- | :---- | :---- |
| Embedded app | Shopify managed installation (recommended) Installation during authorization code grant | Token exchange (recommended) Authorization code grant |
| Non-embedded app | Shopify managed installation (recommended) Installation during authorization code grant | Authorization code grant |
| Admin-created custom app | Installed upon generation in the Shopify admin | Generate in the Shopify admin |

