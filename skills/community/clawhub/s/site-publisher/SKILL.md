---
name: site-publisher
description: Serve and package static websites for preview and deployment. Use when you need to preview a static site, serve HTML files locally, or package a site for sharing/deployment.
---

# Site Publisher

Serve static websites locally and package them for deployment.

## Usage

```bash
# Serve a static site directory
node skills/site-publisher/scripts/serve.js [port] [directory]

# Package a site for deployment
node skills/site-publisher/scripts/package.js [directory] [output]
```

## Examples

```bash
# Serve the farewell site on port 3000
node skills/site-publisher/scripts/serve.js 3000 projects/farewell-school

# Package the site
node skills/site-publisher/scripts/package.js projects/farewell-school
```

## API

```js
const { serveSite, packageSite } = require('./skills/site-publisher');

// Serve a site
serveSite(3000, './projects/farewell-school');

// Package a site
packageSite('./projects/farewell-school', './dist');
```
