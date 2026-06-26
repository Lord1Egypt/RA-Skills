# Deployment Reference

> Source: https://vitepress.dev/guide/deploy

## Build

```sh
npm run docs:build
npm run docs:preview  # http://localhost:4173
```

## Public Base Path

```typescript
// for https://mywebsite.com/blog/
export default {
  base: '/blog/'
}
```

## HTTP Cache Headers

For hashed assets in `/assets/`:

```
Cache-Control: max-age=31536000,immutable
```

### Netlify

Create `docs/public/_headers`:

```
/assets/*
  cache-control: max-age=31536000
  cache-control: immutable
```

### Vercel

Create `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "max-age=31536000, immutable" }]
    }
  ]
}
```

## GitHub Pages

### deploy.yml

```yaml
name: Deploy VitePress site to Pages
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5
        with:
          fetch-depth: 0
      - name: Setup Node
        uses: actions/setup-node@v6
        with:
          node-version: 24
          cache: npm
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Install
        run: npm ci
      - name: Build
        run: npm run docs:build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        uses: actions/deploy-pages@v4
```

Then in repo settings → Pages → Source: GitHub Actions

## Generic (Netlify/Vercel/Cloudflare/AWS/Render)

- Build Command: `npm run docs:build`
- Output Directory: `docs/.vitepress/dist`
- Node Version: `20`

## GitLab Pages

Set `outDir: '../public'` in config.

```yaml
image: node:24
pages:
  script:
    - npm install
    - npm run docs:build
  artifacts:
    paths:
      - public
  only:
    - main
```

## Azure

```json
{
  "app_location": "/",
  "output_location": "docs/.vitepress/dist",
  "app_build_command": "npm run docs:build"
}
```

## Firebase

```json
{
  "hosting": {
    "public": "docs/.vitepress/dist",
    "ignore": []
  }
}
```

## Heroku

```json
{ "root": "docs/.vitepress/dist" }
```

## Nginx

```nginx
server {
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    listen 80;
    server_name _;
    index index.html;

    location / {
        root /app;
        try_files $uri $uri.html $uri/ =404;
        error_page 404 /404.html;
        location ~* ^/assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

Note: Don't default to `index.html`.

## Surge

```sh
npx surge docs/.vitepress/dist
```
