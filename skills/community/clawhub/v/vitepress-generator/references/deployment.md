# VitePress Deployment Guide

## Build Output

After building, the output directory is: `docs/.vitepress/dist/`

This is a pure static website that can be deployed to any static hosting service.

## GitHub Pages

### Using GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy VitePress

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 18
      - run: npm ci
      - run: npm run docs:build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/.vitepress/dist
```

### Manual Deployment

```bash
npm run docs:build
cd docs/.vitepress/dist
git init
git add -A
git commit -m 'deploy'
git push -f git@github.com:username/repo.git main:gh-pages
```

## Vercel

1. Connect your GitHub repository
2. Build settings:
   - Build Command: `npm run docs:build`
   - Output Directory: `docs/.vitepress/dist`
3. Automatic deployment

## Netlify

1. Connect your repository
2. Build settings:
   - Build command: `npm run docs:build`
   - Publish directory: `docs/.vitepress/dist`
3. Automatic deployment

## Docker Deployment

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run docs:build

FROM nginx:alpine
COPY --from=0 /app/docs/.vitepress/dist /usr/share/nginx/html
EXPOSE 80
```

Build and run:

```bash
docker build -t my-vitepress-site .
docker run -p 80:80 my-vitepress-site
```

## Custom Domain

Add a custom domain in your deployment platform, then add a CNAME record with your domain provider.

## Important Notes

1. Ensure the build command is correct
2. Check the output directory path
3. Configure the correct Node.js version
4. Enable HTTPS (most platforms enable it by default)