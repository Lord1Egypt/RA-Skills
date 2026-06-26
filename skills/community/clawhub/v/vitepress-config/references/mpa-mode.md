# MPA Mode

> Source: https://vitepress.dev/guide/mpa-mode

MPA (Multi-Page Application) mode: no JavaScript by default.

## Enable

CLI: `vitepress build --mpa`

Config: `mpa: true` in site config

## Trade-offs

**Pros:**
- Better initial visit performance scores
- Simpler deployment

**Cons:**
- Full page reloads on navigation
- No client-side interactivity by default

## Client Scripts

Use `<script client>` for interactivity:

```html
<script client>
document.querySelector('h1').addEventListener('click', () => {
  console.log('clicked!')
})
</script>

# Hello
```

`<script client>` is VitePress-only, works in `.md` and `.vue` files, only in MPA mode.

Client scripts in theme components are bundled together. Page-specific scripts are split for that page.

Note: `<script client>` is not evaluated as Vue component code - it's a plain JavaScript module.

## When to Use

MPA mode is best when:
- Site requires absolutely minimal client-side interactivity
- You want maximum simplicity and performance
- Most content is static

For most documentation sites, default SPA mode is recommended.
