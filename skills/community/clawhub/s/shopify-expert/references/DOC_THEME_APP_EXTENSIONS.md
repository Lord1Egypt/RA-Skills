# Shopify docs: Theme App Extensions

> Generated from Shopify official LLM documentation snapshot (maintainer export). Prefer live docs at [shopify.dev](https://shopify.dev/) for API versions and current behaviour.

---
## Theme App extensions

### Theme App extensions

[Theme app extensions](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions) allow merchants to easily add dynamic elements to their themes without having to interact with Liquid templates or code. For example, dynamic elements can include product reviews, prices, ratings, or interactive 3D models of products. Theme app extensions can integrate with Online Store 2.0 themes, such as the default Dawn theme, which is Shopify's Online Store 2.0 reference theme.

#### Benefits

* Theme app extensions automatically expose your app in the theme editor. You can leverage the editor’s visual editing capabilities without needing to replicate them in your app.
* You can deploy your app at the same time to all online stores that use it. You also have access to versioning, and asset hosting on the Shopify CDN.
* A single set of integration logic and instructions works for all themes.
* Merchants won't need to manually edit their theme code.

#### Resources

Theme app extensions contain the following resources:

* **Blocks**: Liquid files that act as the entry point for what you want to inject in a theme. The following block types are supported:
  * App blocks
  * App embed blocks
* **Assets**: CSS, JavaScript, and other static app content that gets injected into themes.
* **Snippets**: Reusable Liquid snippets that can be used across multiple blocks.

#### Designing the best merchant experience

Apps built in the theme app extension framework don't edit theme code, which decreases the risk of introducing breaking changes to the theme, makes it easier to iterate on the content of the integration, and provides for a better merchant experience. Merchants can use the theme editor to configure exposed settings and add app blocks in theme sections for precise positioning in a page's layout.

#### Create a new extension

Run the following command:

```
shopify app generate extension
```

#### Configure a theme app extension

When you create a theme app extension, Shopify adds the following `theme-app-extension` directory and subdirectories to your app:

**Newly generated extension**:

```
└── extensions
  └── my-theme-app-extension
      ├── assets
      ├── blocks
      ├── snippets
      ├── locales
      ├── package.json
      └── shopify.extension.toml
```

**Populated extension:**

```
└── extensions
  └── my-theme-app-extension
      ├── assets
      │   ├── image.jpg
      │   ├── icon.svg
      │   ├── app-block.js
      │   ├── app-block.css
      │   ├── app-embed-block.js
      │   └── app-embed-block.css
      ├── blocks
      │   ├── app-block.liquid
      │   └── app-embed-block.liquid
      ├── snippets
      │   ├── app-block-snippet.liquid
      │   └── app-embed-block-snippet.liquid
      ├── locales
      |   ├── en.default.json
      |   ├── en.default.schema.json
      |   ├── fr.json
      |   └── fr.schema.json
      ├── package.json
      └── shopify.extension.toml
```

#### App blocks for themes

Apps that inject inline content on a page extend themes using app blocks. Merchants can add app blocks to a compatible theme section, or as wrapped app blocks that are added at the section level. Create an app block by setting the target in the schema to section.

By default, themes don't include app blocks after an app is installed. Merchants need to add the app blocks to the theme from the Apps section of the theme editor.

Use app blocks for the following types of apps:

* Apps that you want to automatically point to dynamic sources, such as product reviews apps and star ratings apps.
* Apps that merchants might want to reposition on a page.
* Apps that should span the full width of a page.

**Example**

```
<span style="color: {{ block.settings.color }}">
App blocks let you build powerful integrations with online store themes.
</span>

{% render "app_snippet" %}
{% schema %}
  {
    "name": "Hello World",
    "target": "section",
    "enabled_on": {
      "templates": ["index"]
    },
    "stylesheet": "app.css",
    "javascript": "app.js",
    "settings": [
        { "label": "Color", "id": "color", "type": "color", "default": "#000000" }
    ]
  }
{% endschema %}
```

#### App embed blocks

Apps that don't have a UI component, or that add floating or overlaid elements, extend themes using app embed blocks. Shopify renders and injects app embed blocks before HTML `</head>` and `</body>` closing tags. Create an app embed block by setting the `target` in the schema to either `compliance_head`, `head`, or `body`. App embed blocks with `compliance_head` will be included first and should be used only when necessary, for example in cookie consent banners.

By default, app embed blocks are deactivated after an app is installed. Merchants need to activate app embed blocks in the theme editor, from **Theme Settings \> App** embeds. However, your app can provide merchants with a deep link, post installation, to activate an app embed block automatically.

Use app embed blocks for the following types of apps:

* Apps that provide a floating or overlaid component to a page, such as chat bubble apps and product image badge apps.
* Apps that add SEO meta tags, analytics, or tracking pixels.

**Example**

```
<div style="position: fixed; bottom: 0; right: 0">
    {{ "kitten.jpg" | asset_url | img_tag }}
</div>
{% schema %}
  {
    "name": "App Embed",
    "target": "body",
    "settings": []
  }
{% endschema %}

```

#### Condition app blocks

You can control the visibility of an app block or app embed block based on a custom condition. For example, you might want to limit content based on plan tier, or geographic location.

The condition can be included in the block's schema with the `available_if` attribute, and the state of the condition is stored in an app-data metafield. The metafield can be accessed through the Liquid `app` object.

**Example**

```
{% schema %}
 {
   "name": "Conditional App block",
   "target": "section",
   "stylesheet": "app.css",
   "javascript": "app.js",
   "available_if": "{{ app.metafields.conditional.block1 }}",
   "settings": [
      {
        "label": "Colour",
        "id": "colour",
        "type": "color",
        "default": "#000000"
      }
   ]
 }
{% endschema %}
```

