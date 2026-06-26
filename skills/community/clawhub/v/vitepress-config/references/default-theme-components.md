# Default Theme Components Reference

> Source: https://vitepress.dev/reference/default-theme-config

Components available from `vitepress/theme`.

## Nav

### Site Title and Logo

```typescript
themeConfig: {
  siteTitle: 'My Custom Title',
  logo: '/my-logo.svg',
  logo: { light: '/logo-light.svg', dark: '/logo-dark.svg', alt: 'Logo' }
}
```

### Navigation Links

```typescript
nav: [
  { text: 'Guide', link: '/guide' },
  { text: 'Config', link: '/config' },
  { text: 'GitHub', link: 'https://github.com/...', target: '_self', rel: 'sponsored' },
  {
    text: 'Dropdown',
    items: [
      { text: 'Item A', link: '/item-1' },
      { text: 'Item B', link: '/item-2' }
    ]
  },
  {
    text: 'Sections',
    items: [
      {
        text: 'Section Title',
        items: [
          { text: 'Item A', link: '/a' },
          { text: 'Item B', link: '/b' }
        ]
      }
    ]
  }
]
```

### activeMatch

```typescript
{ text: 'Guide', link: '/guide', activeMatch: '/config/' }
```

### Custom Components

```typescript
// config.js
themeConfig: {
  nav: [
    {
      text: 'My Menu',
      items: [{ component: 'MyComponent', props: { title: 'Hi' } }]
    }
  ]
}

// theme/index.js
app.component('MyComponent', MyComponent)
```

## Sidebar

### Basic

```typescript
sidebar: [
  {
    text: 'Section Title',
    items: [
      { text: 'Item A', link: '/item-a' },
      { text: 'Item B', link: '/item-b' }
    ]
  }
]
```

### Multiple Sidebars

```typescript
sidebar: {
  '/guide/': [
    { text: 'Guide', items: [{ text: 'Index', link: '/guide/' }] }
  ],
  '/config/': [
    { text: 'Config', items: [{ text: 'Index', link: '/config/' }] }
  ]
}
```

### Collapsible

```typescript
{
  text: 'Section',
  collapsed: true,  // closed by default
  items: [...]
}
```

## Home Page

### Hero

```typescript
hero: {
  name?: string           // top text with brand color
  text: string            // main h1 text
  tagline?: string        // below text
  image?: ThemeableImage   // next to text
  actions?: HeroAction[]
}

interface HeroAction {
  theme?: 'brand' | 'alt'
  text: string
  link: string
  target?: string
  rel?: string
}

// Custom name color:
:root { --vp-home-hero-name-color: blue; }
:root { --vp-home-hero-name-background: -webkit-linear-gradient(120deg, #bd34fe, #41d1ff); }
```

### Features

```typescript
features: [
  {
    icon: '🛠️',  // or { src: '/icon.svg' } or { light: '/a.svg', dark: '/b.svg' }
    title: string,
    details: string,
    link?: string,
    linkText?: string,
    rel?: string,
    target?: string
  }
]
```

## Badge

```vue
### Title <Badge type="info" text="default" />
### Title <Badge type="tip" text="^1.9.0" />
### Title <Badge type="warning" text="beta" />
### Title <Badge type="danger" text="caution" />

<!-- Custom children -->
<Badge type="info">custom</Badge>
```

Props: `text?: string`, `type?: 'info' | 'tip' | 'warning' | 'danger'`

## Search

### Local

```typescript
search: {
  provider: 'local',
  options: {
    locales: { zh: { translations: { button: { buttonText: '搜索' } } } },
    miniSearch: {
      options: { /* MiniSearch options */ },
      searchOptions: { fuzzy: 0.2, prefix: true, boost: { title: 4 } }
    }
  }
}
```

### Algolia

```typescript
search: {
  provider: 'algolia',
  options: {
    appId: '...',
    apiKey: '...',
    indexName: '...',
    locales: { /* translations */ },
    askAi?: {
      assistantId: 'XXX',
      sidePanel?: { /* panel options */ }
    }
  }
}
```

## Team Page

### VPTeamMembers

```vue
<script setup>
import { VPTeamMembers } from 'vitepress/theme'

const members = [
  {
    avatar: 'https://www.github.com/yyx990803.png',
    name: 'Evan You',
    title: 'Creator',
    links: [{ icon: 'github', link: 'https://github.com/yyx990803' }]
  }
]
</script>

<VPTeamMembers size="small" :members />
```

### Full Team Page

```vue
<script setup>
import { VPTeamPage, VPTeamPageTitle, VPTeamMembers } from 'vitepress/theme'
</script>

<VPTeamPage>
  <VPTeamPageTitle>
    <template #title>Our Team</template>
    <template #lead>Development guided by...</template>
  </VPTeamPageTitle>
  <VPTeamMembers :members />
</VPTeamPage>
```

### With Sections

```vue
<VPTeamPage>
  <VPTeamPageTitle>...</VPTeamPageTitle>
  <VPTeamMembers :members="coreMembers" />
  <VPTeamPageSection>
    <template #title>Partners</template>
    <template #lead>...</template>
    <template #members>
      <VPTeamMembers :members="partners" />
    </template>
  </VPTeamPageSection>
</VPTeamPage>
```

## Layout Slots

### doc Layout

```
doc-top, doc-bottom
doc-footer-before, doc-before, doc-after
sidebar-nav-before, sidebar-nav-after
aside-top, aside-bottom
aside-outline-before, aside-outline-after
aside-ads-before, aside-ads-after
```

### home Layout

```
home-hero-before, home-hero-info, home-hero-info-after
home-hero-actions-before, home-hero-actions-after
home-hero-image, home-hero-after
home-features-before, home-features-after
```

### page Layout

```
page-top, page-bottom
```

### Always Available

```
layout-top, layout-bottom
nav-bar-title-before, nav-bar-title-after
nav-bar-content-before, nav-bar-content-after
nav-screen-content-before, nav-screen-content-after
not-found
```

### Example

```vue
<template>
  <Layout>
    <template #aside-outline-before>
      My custom sidebar content
    </template>
  </Layout>
</template>
```
