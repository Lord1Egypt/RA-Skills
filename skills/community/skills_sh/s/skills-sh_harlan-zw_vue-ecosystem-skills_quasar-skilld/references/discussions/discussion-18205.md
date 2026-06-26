---
number: 18205
title: 103 Early Hints for main css + renderToNodeStream/pipeToNodeWritable
category: CLI - SSR mode
created: 2025-12-24
url: "https://github.com/quasarframework/quasar/discussions/18205"
upvotes: 1
comments: 0
answered: false
---

# 103 Early Hints for main css + renderToNodeStream/pipeToNodeWritable

We can to make render function more better if add this flow (ssr-prod-webserver.js)
But we need to separate render-template.js

We need to cut render-template into small pieces
```js
  async #writeRenderTemplate (clientDir) {
    const htmlFile = join(clientDir, 'index.html')
    const html = this.readFile(htmlFile)

    const templateFn = await getProdSsrTemplateFn(html, this.quasarConf)

    this.writeFile(
      'render-template.js',
      `export default ${ templateFn.source }`
    )

    ...
  }
  ```
  
  And we need reorganizate render:
  ```js
      const runtimePageContent = await renderToString(renderFn, ssrContext)

    onRenderedList.forEach(fn => { fn() })

    // maintain compatibility with some well-known Vue plugins
    // like @vue/apollo-ssr:
    typeof ssrContext.rendered === 'function' && ssrContext.rendered()

    ssrContext._meta.runtimePageContent = runtimePageContent

    <% if (metaConf.hasStore && ssr.manualStoreSerialization !== true) { %>
      if (ssrContext.state !== void 0) {
        ssrContext._meta.headTags = renderStoreState(ssrContext) + ssrContext._meta.headTags
      }
    <% } %>
  ```...