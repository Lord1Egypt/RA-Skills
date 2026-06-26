# Using Vue in Markdown

> Source: https://vitepress.dev/guide/using-vue

Each Markdown file is compiled into a Vue SFC. Use Vue features for dynamic content.

## Interpolation

```md
{{ 1 + 1 }}  <!-- outputs: 2 -->
```

## Directives

```md
`<span v-for="i in 3">{{ i }}</span>`  <!-- outputs: 1 2 3 -->
```

## Script and Style

```html
---
hello: world
---

<script setup>
import { ref } from 'vue'
const count = ref(0)
</script>

## Count: {{ count }}

<button @click="count++">Increment</button>

<style module>
.button { color: red; }
</style>
```

Avoid `<style scoped>` in markdown - it bloats page size. Use `<style module>` instead.

## Using Components

### Import in Markdown

```vue
<script setup>
import CustomComponent from '../components/CustomComponent.vue'
</script>

<CustomComponent />
```

### Register Globally

```javascript
// theme/index.js
export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('MyGlobalComponent', MyGlobalComponent)
  }
}
```

## Components in Headers

| Markdown | Output | Parsed |
|---------|--------|--------|
| `# text <Tag/>` | `<h1>text <Tag/></h1>` | text |
| `# text `<Tag/>`` | `<h1>text <code>&lt;Tag/&gt;</code></h1>` | text `<Tag/>` |

## Escaping

```md
This <span v-pre>{{ will be displayed as-is }}</span>
```

Or use container: `::: v-pre\n{{ raw }}\n:::`

## CSS Pre-processors

```bash
npm install -D sass      # .scss, .sass
npm install -D less       # .less
npm install -D stylus     # .styl, .stylus
```

## Teleports

```vue
<ClientOnly>
  <Teleport to="#modal">
    <div>Modal content</div>
  </Teleport>
</ClientOnly>
```

## VS Code IntelliSense

```json
// tsconfig.json
{
  "include": ["docs/**/*.ts", "docs/**/*.vue", "docs/**/*.md"],
  "vueCompilerOptions": {
    "vitePressExtensions": [".md"]
  }
}
```

```json
// .vscode/settings.json
{
  "vue.server.includeLanguages": ["vue", "markdown"]
}
```
