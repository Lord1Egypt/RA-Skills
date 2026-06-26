# Shopify docs: Embedded App Bridge

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Embedded apps and App bridge

### Embedded apps and App bridge

The primary place where users engage with your app is its app home. This is the location where merchants are directed when they navigate to your app in Shopify.

The Shopify admin provides a surface for apps to render the UX for their app home. On the web, the surface is an iframe and in the Shopify mobile app, the surface is a WebView.

By combining Shopify App Bridge and Polaris, you can make your app display seamlessly in the Shopify admin. Polaris enables apps to match the visual appearance of the admin by using the same design components. App Bridge enables apps to communicate with the Shopify admin and create UI elements outside of the app's surface. Such elements include navigation menus, modals that cover the entire screen, and contextual save bars that prevent users from navigating away from the page when they have unsaved changes.

#### App Bridge

The App Bridge library provides APIs that enable Shopify apps to render UI in the Shopify app home surface.

Apps built with Shopify App Bridge are more performant, flexible, and seamlessly integrate with the Shopify admin. You can use Shopify App Bridge with Polaris to provide a consistent and intuitive user experience that matches the rest of the Shopify admin.

On the web, your app renders in an iframe and in the Shopify mobile app it renders in a WebView.

The latest version of App Bridge is built on top of web components and APIs to provide a flexible and familiar development environment. Your app can invoke these APIs using vanilla JavaScript functions.

App Bridge enables you to do the following from your app home:

* Render a navigation menu on the left of the Shopify admin

```
<ui-nav-menu>
  <a href="/" rel="home">Home</a>
  <a href="/templates">Templates</a>
  <a href="/settings">Settings</a>
</ui-nav-menu>
```

* Render a contextual save bar above the top bar of the Shopify admin

```
<ui-save-bar id="my-save-bar">
  <button variant="primary" id="save-button"></button>
  <button id="discard-button"></button>
</ui-save-bar>

<button onclick="document.getElementById('my-save-bar').show()">Show</button>

<script>
  document.getElementById('save-button').addEventListener('click', () => {
    console.log('Saving');
    document.getElementById('my-save-bar').hide();
  });

  document.getElementById('discard-button').addEventListener('click', () => {
    console.log('Discarding');
    document.getElementById('my-save-bar').hide();
  });
</script>
```

* Render a title bar with primary and secondary actions

```
<ui-title-bar title="Products">
  <button onclick="console.log('Secondary action')">Secondary action</button>
  <button variant="primary" onclick="console.log('Primary action')">
    Primary action
  </button>
</ui-title-bar>
```

