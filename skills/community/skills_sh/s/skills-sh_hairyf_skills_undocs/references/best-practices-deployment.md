---
name: undocs-deployment
description: Deploy undocs documentation sites to various hosting platforms
---

# Deployment

Undocs generates static sites that can be deployed to any static hosting platform.

## Build for Production

Build the static site:

```bash
npx undocs build
```

This generates a static site in `.output/public/`.

## Required Configuration

For production builds, `url` is required:

```yaml
# .config/docs.yaml
url: "https://your-site.example.com"
```

## Deployment Platforms

### Vercel

Deploy to Vercel:

1. Connect your repository
2. Build command: `undocs build`
3. Output directory: `.output/public`

Vercel automatically detects Nuxt and configures deployment.

### Netlify

Deploy to Netlify:

1. Connect your repository
2. Build command: `undocs build`
3. Publish directory: `.output/public`

Netlify automatically detects the `url` from `NETLIFY_URL` environment variable.

### Cloudflare Pages

Deploy to Cloudflare Pages:

1. Connect your repository
2. Build command: `undocs build`
3. Output directory: `.output/public`

Cloudflare Pages automatically detects the branch from `CF_PAGES_BRANCH`.

### GitHub Pages

Deploy to GitHub Pages:

1. Build the site: `undocs build`
2. Copy `.output/public` contents to `gh-pages` branch
3. Configure GitHub Pages to serve from `gh-pages` branch

### Static Hosting

Any static hosting service works:

- AWS S3 + CloudFront
- Azure Static Web Apps
- Google Cloud Storage
- Any CDN or static file host

## Environment Variables

Undocs automatically infers site URL from platform environment variables:

- `NUXT_PUBLIC_SITE_URL` - Explicit site URL
- `NEXT_PUBLIC_VERCEL_URL` - Vercel (auto-detected)
- `URL` - Netlify (auto-detected)
- `CI_PAGES_URL` - GitLab Pages (auto-detected)
- `CF_PAGES_URL` - Cloudflare Pages (auto-detected)

## Branch Detection

Branch is automatically detected for edit links:

- `CF_PAGES_BRANCH` - Cloudflare Pages
- `CI_COMMIT_BRANCH` - GitLab CI
- `VERCEL_BRANCH_URL` - Vercel
- `BRANCH` - Generic
- `GITHUB_REF_NAME` - GitHub Actions
- Git command fallback

## Prerendering

All pages are prerendered by default for optimal performance and SEO.

## Markdown Raw Endpoints

Undocs generates raw markdown endpoints at `/raw/*.md`:

- Accessible via `Accept: text/markdown` header
- Accessible via `curl` user agent
- Useful for LLM consumption

## Key Points

- Build with `undocs build`
- `url` is required for production
- Works with any static hosting platform
- Site URL is auto-detected from environment variables
- Branch is auto-detected for edit links
- All pages are prerendered
- Raw markdown endpoints are available

<!--
Source references:
- https://github.com/unjs/undocs/blob/main/cli/setup.mjs
- https://github.com/unjs/undocs/blob/main/app/modules/md-rewrite.ts
-->
