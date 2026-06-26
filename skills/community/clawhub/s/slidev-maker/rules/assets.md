# Slidev Assets

Images, videos, fonts, and static files.

## Public Folder

Static assets MUST be placed in the `public` folder at project root.
```
your-slidev/
├── public/
│   ├── images/
│   │   └── photo.png
│   ├── videos/
│   │   └── demo.mp4
│   └── favicon.ico
├── slides.md
└── package.json
```

## Asset Paths

Reference assets with absolute paths starting with `/`.
```markdown
![My Image](/images/photo.png)

---
background: /images/background.jpg
---
```

NEVER use relative paths in frontmatter:
```yaml
# ❌ WRONG - Will break after build
background: ./images/photo.png

# ✅ CORRECT
background: /images/photo.png
```

## Images in Markdown

Standard Markdown syntax:
```markdown
![Alt text](/image.png)
```

With custom size and styling using HTML:
```html
<img src="/image.png" class="w-60 rounded shadow" />
```

Using UnoCSS utility classes for sizing:
```html
<img src="/photo.jpg" class="h-40 mx-auto" />
<img src="/diagram.svg" class="w-full max-w-md" />
```

## Background Images

Set in per-slide frontmatter:
```yaml
---
background: /background.jpg
---
```

With sizing options:
```yaml
---
background: /image.png
backgroundSize: cover
backgroundPosition: center
---
```

Using image layouts:
```yaml
---
layout: image
image: /fullscreen.jpg
---

---
layout: image-left
image: /sidebar.png
---

Content appears on the right side.

---
layout: image-right
image: /sidebar.png
---

Content appears on the left side.
```

## Remote Images

Remote URLs work directly:
```markdown
![Remote](/https://example.com/image.png)
```

Remote assets are cached automatically by `vite-plugin-remote-assets` for faster subsequent loads.

## Videos

Use the SlidevVideo component:
```html
<SlidevVideo autoplay controls>
  <source src="/video.mp4" type="video/mp4" />
</SlidevVideo>
```

Or standard HTML video:
```html
<video src="/video.mp4" controls class="w-full"></video>
```

Video files MUST be in the `public` folder.

## Fonts

### Google Fonts

Configure in headmatter for automatic loading:
```yaml
---
fonts:
  sans: Roboto
  serif: Merriweather
  mono: Fira Code
---
```

Fonts are loaded from Google Fonts CDN automatically.

### Custom Font Weights
```yaml
---
fonts:
  sans: Inter
  weights: '400,600,700'
  italic: true
---
```

### Local Fonts

Mark fonts as local to skip CDN loading:
```yaml
---
fonts:
  sans: 'Helvetica Neue, Arial'
  local: Helvetica Neue
---
```

### Font Provider

Change CDN provider:
```yaml
---
fonts:
  provider: google  # default
  # or: coollabs, none
---
```

Set `provider: none` for fully local fonts.

## Icons

Use Iconify icons directly in Markdown:
```html
<mdi-account-circle />
<carbon-badge />
<logos-vue />
<twemoji-cat-with-tears-of-joy />
```

Format: `<{collection}-{icon-name} />`

Style icons with classes:
```html
<mdi-rocket class="text-3xl text-blue-500" />
<mdi-star class="text-yellow-400 animate-pulse" />
```

Browse icons at [icones.js.org](https://icones.js.org).