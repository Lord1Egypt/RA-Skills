#!/bin/bash

# VitePress site initialization script
# Usage: ./init-vitepress-site.sh <project-name>

set -e

PROJECT_NAME=${1:-my-vitepress-site}

echo "🚀 Creating VitePress project: $PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize npm project
echo "📦 Initializing npm project..."
npm init -y

# Install VitePress
echo "⬇️  Installing VitePress..."
npm add -D vitepress

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p docs/.vitepress
mkdir -p docs/guide

# Create configuration file
cat > docs/.vitepress/config.mts << 'CONFIG'
import { defineConfig } from 'vitepress'

export default defineConfig({  
  title: 'My Site',
  description: 'A static website built with VitePress',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' }
    ],
    sidebar: {
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Quick Start', link: '/guide/getting-started' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ]
  }
})
CONFIG

# Create home page
cat > docs/index.md << 'INDEX'
---
layout: home

hero:
  name: My Site
  text: Built with VitePress
  tagline: Fast, simple, and powerful static site generator
  actions:
    - theme: brand
      text: Quick Start
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com

features:
  - icon: ⚡️
    title: 'Fast'
    details: Blazing fast development experience powered by Vite
  - icon: 📝
    title: 'Simple'
    details: Focus on content with Markdown
  - icon: 🎨
    title: 'Customizable'
    details: Flexible theme and style customization
---
INDEX

# Create guide page
cat > docs/guide/getting-started.md << 'GUIDE'
# Quick Start

Welcome to VitePress!

## What is VitePress

VitePress is a static site generator built on top of Vite and Vue, designed specifically for technical documentation.

## Key Features

- ⚡️ **Blazing Fast**: Hot reload powered by Vite
- 📝 **Markdown First**: Focus on content creation
- 🎨 **Theme System**: Easily customizable appearance
- 📱 **Responsive**: Perfect mobile experience

## Next Steps

- Check out the [Configuration Guide](/config) for more settings
- Learn how to customize the appearance in [Theme Customization](/theme)
GUIDE

# Update package.json with scripts
echo "📝 Configuring scripts..."
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.scripts = pkg.scripts || {};
pkg.scripts['docs:dev'] = 'vitepress dev docs';
pkg.scripts['docs:build'] = 'vitepress build docs';
pkg.scripts['docs:preview'] = 'vitepress preview docs';
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"

# Create README
cat > README.md << 'README'
# My VitePress Site
A static website built with [VitePress](https://vitepress.dev).

## Quick Start

```bash
# Install dependencies
npm install

# Start local development
npm run docs:dev

# Build for production
npm run docs:build

# Preview the build
npm run docs:preview
```

## Directory Structure

```
.
├── docs/
│   ├── .vitepress/     # VitePress configuration
│   ├── index.md        # Home page
│   └── guide/          # Documentation pages
├── package.json
└── README.md
```

## Deployment

Build artifacts are located in `docs/.vitepress/dist/` and can be deployed to any static hosting service.

See Deployment Guide for more details.
README

echo ""
echo "✅ Project created successfully!"
echo ""
echo "📂 Project location: $(pwd)"
echo ""
echo "🚀 Next steps:"
echo " cd $PROJECT_NAME"
echo " npm run docs:dev"
echo ""
echo "📖 Visit http://localhost:4173 to preview your site"
