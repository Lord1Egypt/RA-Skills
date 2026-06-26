# Default Theme Config Reference

> Source: https://vitepress.dev/reference/default-theme-config

Theme config via `themeConfig` option.

## Basic Options

### i18nRouting
- **Type:** `boolean`
- Changes locale URL from `/foo` to `/zh/foo`

### logo

```typescript
type ThemeableImage =
  | string
  | { src: string; alt?: string }
  | { light: string; dark: string; alt?: string }

// Examples:
logo: '/logo.svg'
logo: { light: '/logo-light.svg', dark: '/logo-dark.svg' }
```

### siteTitle
- **Type:** `string | false`
- Replace default site title in navbar

## Navigation

### nav

```typescript
type NavItem = NavItemWithLink | NavItemWithChildren

interface NavItemWithLink {
  text: string
  link: string | ((payload: PageData) => string)
  activeMatch?: string  // regex string for active state
  target?: string
  rel?: string
  noIcon?: boolean
}

interface NavItemWithChildren {
  text?: string
  items: (NavItemChildren | NavItemWithLink)[]
  activeMatch?: string
}
```

### socialLinks

```typescript
interface SocialLink {
  icon: string | { svg: string }
  link: string
  ariaLabel?: string
}

// Icons from simple-icons.org
socialLinks: [
  { icon: 'github', link: 'https://github.com/vuejs/vitepress' },
  { icon: 'twitter', link: 'https://twitter.com/evanyou' }
]
```

## Sidebar

### sidebar

```typescript
export type Sidebar = SidebarItem[] | SidebarMulti

export interface SidebarMulti {
  [path: string]: SidebarItem[] | { items: SidebarItem[]; base: string }
}

export type SidebarItem = {
  text?: string
  link?: string
  items?: SidebarItem[]
  collapsed?: boolean  // true = collapsed by default
  base?: string
  docFooterText?: string
  rel?: string
  target?: string
}
```

## Page Layout

### aside
- **Type:** `boolean | 'left'`
- **Default:** `true`
- Position of outline aside

### outline

```typescript
interface Outline {
  level?: number | [number, number] | 'deep'  // default: 2
  label?: string  // default: 'On this page'
}
```

## Content Footer

### footer

```typescript
interface Footer {
  message?: string   // e.g., 'Released under the MIT License'
  copyright?: string // e.g., 'Copyright © 2019-present Evan You'
}
```

### docFooter

```typescript
interface DocFooter {
  prev?: string | false
  next?: string | false
}
```

## Features

### editLink

```typescript
interface EditLink {
  pattern: string | ((pageData: PageData) => string)
  text?: string
}

// Pattern example:
pattern: 'https://github.com/vuejs/vitepress/edit/main/:path'
```

### lastUpdated

```typescript
interface LastUpdatedOptions {
  text?: string  // default: 'Last updated'
  formatOptions?: Intl.DateTimeFormatOptions
}
```

### carbonAds

```typescript
interface CarbonAdsOptions {
  code: string
  placement: string
}
```

## Search

### algolia

```typescript
interface AlgoliaSearchOptions extends DocSearchProps {
  locales?: Record<string, Partial<DocSearchProps>>
}
```

## Labels

| Option | Type | Default |
|--------|------|---------|
| `darkModeSwitchLabel` | `string` | `Appearance` |
| `lightModeSwitchTitle` | `string` | `Switch to light theme` |
| `darkModeSwitchTitle` | `string` | `Switch to dark theme` |
| `sidebarMenuLabel` | `string` | `Menu` |
| `returnToTopLabel` | `string` | `Return to top` |
| `langMenuLabel` | `string` | `Change language` |
| `skipToContentLabel` | `string` | `Skip to content` |

### externalLinkIcon
- **Type:** `boolean`
- **Default:** `false`
- Show icon next to external links

## useLayout Composable

```typescript
const {
  isHome: ComputedRef<boolean>
  sidebar: Readonly<ShallowRef<SidebarItem[]>>
  sidebarGroups: ComputedRef<SidebarItem[]>
  hasSidebar: ComputedRef<boolean>
  isSidebarEnabled: ComputedRef<boolean>
  hasAside: ComputedRef<boolean>
  leftAside: ComputedRef<boolean>
  headers: Readonly<ShallowRef<OutlineItem[]>>
  hasLocalNav: ComputedRef<boolean>
} = useLayout()
```
