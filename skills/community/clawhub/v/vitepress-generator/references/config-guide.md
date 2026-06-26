# VitePress Configuration Guide

## Basic Configuration (config.mts)

```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'My Site',
  description: 'Site description',
  
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }]
  ],
  
  themeConfig: {
    // Top navigation
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/getting-started' }
    ],
    
    // Sidebar
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
    
    // Social links
    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-repo' }
    ]
  }
})
```

## Configuration Options

### Site Configuration

| Option | Description | Example |
|--------|------|------|
| `title` | Site title | 'My Docs' |
| `description` | Site description | 'Technical documentation site' |
| `head` | HTML head tags | Add favicon, meta, etc. |

### Theme Configuration

| Option | Description |
|--------|------|
| `nav` | Top navigation menu |
| `sidebar` | Sidebar navigation |
| `socialLinks` | Social link icons |
| `footer` | Footer configuration |

## Multilingual Configuration

```typescript
export default defineConfig({
  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN',
      title: '我的文档'
    },
    en: {
      label: 'English',
      lang: 'en',
      title: 'My Docs',
      link: '/en/'
    }
  }
})
```

## Custom Head Tags

```typescript
head: [
  ['meta', { name: 'keywords', content: 'keywords' }],
  ['meta', { property: 'og:type', content: 'website' }],
  ['link', { rel: 'stylesheet', href: '/custom.css' }]
]
```