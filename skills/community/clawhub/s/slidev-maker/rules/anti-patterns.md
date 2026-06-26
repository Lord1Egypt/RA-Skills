# Slidev Anti-Patterns

Critical mistakes to avoid when generating Slidev code.

## Asset Paths

Assets in frontmatter MUST use absolute paths from the `public` folder.`````yaml
# ❌ WRONG - Will break after build
---
background: ./images/photo.png
---

# ✅ CORRECT - Use absolute path from public folder
---
background: /images/photo.png
---
`````

Place assets in the `public` folder at your project root. Vite cannot statically analyze relative paths in frontmatter.

## Prism Highlighter is REMOVED

Do NOT configure or reference the Prism highlighter. It was completely removed in Slidev v0.50.
`````yaml
# ❌ WRONG - Prism no longer exists
---
highlighter: prism
---

# ✅ CORRECT - Shiki is the only highlighter (and is default)
---
highlighter: shiki
---
`````

Shiki is the default highlighter. No configuration is needed unless customizing themes.

## Non-Existent Layouts

These layouts DO NOT EXIST. Never use them:

- `title-slide`
- `split`
- `code-left`
- `code-right`
- `columns`
- `title`
- `blank`

Use these actual built-in layouts:
`````yaml
layout: cover      # Cover/title page (default for first slide)
layout: center     # Centered content
layout: default    # Default layout
layout: two-cols   # Two columns (use ::right:: slot)
layout: image      # Full image background
layout: image-left # Image on left, content on right
layout: image-right # Image on right, content on left
layout: iframe     # Embed iframe
layout: iframe-left
layout: iframe-right
layout: intro      # Introduction slide
layout: quote      # Quote display
layout: section    # Section divider
layout: statement  # Statement emphasis
layout: fact       # Fact display
layout: full       # Full page content
layout: end        # End slide
layout: none       # No layout wrapper
`````

## Internal Client Imports

Do NOT import from internal `@slidev/client` paths. They break between versions.
`````javascript
// ❌ WRONG - Internal paths are unstable
import { isDark } from '@slidev/client/logic/dark'
import { clicks } from '@slidev/client/logic/nav'

// ✅ CORRECT - Use public API exports
import { useDarkMode, useNav, useSlideContext } from '@slidev/client'
`````

## Click Animation Syntax

Relative click values MUST be quoted strings.
`````html
<!-- ❌ WRONG - Unquoted relative values -->
<div v-click="+2">content</div>
<div v-click.hide="-1">content</div>

<!-- ✅ CORRECT - Quote relative values -->
<div v-click="'+2'">content</div>
<v-click at="'+2'"><div>content</div></v-click>
`````

Absolute values can be unquoted: `v-click="3"` is valid.

## Code Block Line Highlighting

Line numbers MUST be inside curly braces `{}`.
`````markdown
<!-- ❌ WRONG - Missing curly braces -->
````ts 2,3
const x = 1
````

<!-- ✅ CORRECT - Use curly braces -->
````ts {2,3}
const x = 1
````

<!-- Multi-step highlighting with clicks -->
````ts {2-3|5|all}
// Click 1: highlights lines 2-3
// Click 2: highlights line 5
// Click 3: highlights all
````
`````

## Monaco Editor Syntax

The `monaco` flag MUST be inside curly braces.
`````markdown
<!-- ❌ WRONG -->
````js monaco
console.log('wrong')
````

<!-- ✅ CORRECT -->
````js {monaco}
console.log('editable')
````

<!-- Monaco with line highlighting -->
````js {monaco}{2,3}
const a = 1
const b = 2  // highlighted
const c = 3  // highlighted
````
`````

## Magic Move Syntax

Magic Move requires a 4-backtick wrapper around the code blocks.
`````markdown
<!-- ❌ WRONG - Only 3 backticks -->
````md magic-move
```js
step1()
```
```js
step2()
```
````

<!-- ✅ CORRECT - Use 4 backticks as wrapper -->
````md magic-move
```js
step1()
```
```js
step2()
```
````
`````

## Two-Column Layout Slots

The `two-cols` layout requires the `::right::` slot separator.
`````markdown
---
layout: two-cols
---

# Left Column

Content on the left side.

::right::

# Right Column

Content on the right side.
`````

Without `::right::`, all content appears in the left column.

## Node.js Version

Slidev requires Node.js >= 18. Do not use older versions.
