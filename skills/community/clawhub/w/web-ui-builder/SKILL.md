---
name: web-ui-builder
description: Generate complete frontend page code using React 19 + Vite 8 + Tailwind CSS 4 + lucide-react from UI descriptions or images. Outputs project structure, component code, and start commands.
---

# Web UI Builder

Automatically generate complete frontend page code from visual descriptions or image references. Fixed tech stack: React 19 + Vite 8 + Tailwind CSS 4 + lucide-react.

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 19+ | UI framework |
| Vite | 8+ | Build tool |
| Tailwind CSS | 4+ | Styling (CSS-driven, no tailwind.config.js) |
| lucide-react | 1.17+ | Icon library |
| @vitejs/plugin-react | latest | Vite React plugin |

## Tailwind CSS 4 Notes

Tailwind CSS 4 uses **CSS-driven configuration**, no `tailwind.config.js` or `postcss.config.js` needed:

```css
/* src/index.css — replaces tailwind.config.js + postcss */
@import "tailwindcss";

/* Custom theme colors */
@theme {
  --color-brand-50: #eef2ff;
  --color-brand-100: #e0e7ff;
  --color-brand-500: #6366f1;
  --color-brand-600: #4f46e5;
  --color-brand-700: #4338ca;
}

/* Custom component classes */
@layer components {
  .card { @apply rounded-xl bg-white p-6 shadow-sm border border-gray-100; }
  .btn-primary { @apply rounded-lg bg-brand-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-700 transition-colors; }
}
```

Key changes:
- `@tailwind base/components/utilities` → `@import "tailwindcss"`
- Custom themes use `@theme` directive instead of `tailwind.config.js` `theme.extend`
- Custom components use `@layer components`
- No `postcss.config.js` needed (handled by Vite)
- No `tailwind.config.js` `content` configuration needed

## package.json Dependencies

```json
{
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "lucide-react": "^1.17.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^latest",
    "tailwindcss": "^4.0.0",
    "vite": "^8.0.0"
  }
}
```

## Project Structure

```
project/
├── package.json
├── vite.config.js
├── index.html
└── src/
    ├── main.jsx          # React entry point
    ├── index.css         # @import "tailwindcss" + @theme customization
    ├── App.jsx           # Root component
    ├── LoginPage.jsx     # (on demand) Login page
    ├── DashboardPage.jsx # (on demand) Dashboard
    ├── Sidebar.jsx       # (on demand) Sidebar
    ├── Header.jsx        # (on demand) Header
    └── ...               # (on demand) Other components
```

## vite.config.js

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

## Workflow

```
User input (description/image) → Extract functional modules → Compose skeleton + content modules → Generate files → Return directory + start command
```

## Component-Driven Strategy

Instead of predefined page types, identify **functional modules** from user descriptions and compose them on demand:

### Skeleton Components (generated as needed)

| Component | Use Case |
|-----------|----------|
| `TopNav` | Page top navigation (links/brand/search/user menu) |
| `Sidebar` | Side menu (icons+labels/hierarchy/user info) |
| `Header` | Content area top bar (title/breadcrumbs/actions/notifications) |
| `Footer` | Page footer (links/copyright/social) |

### Content Modules (generated as needed)

| Module | Detection Keywords |
|--------|--------------------|
| `HeroBanner` | "banner/hero/welcome/featured" |
| `FormSection` | "form/input/register/login/feedback" |
| `StatsCards` | "statistics/metrics/KPI/overview" |
| `DataTable` | "table/list/data rows/records" |
| `CardGrid` | "cards/grid/gallery/showcase" |
| `ChartSection` | "chart/trend/distribution/visualization" |
| `Timeline` | "timeline/progress/flow/steps" |
| `Modal` | "modal/dialog/confirmation" |
| `Tabs` | "tabs/switch/categories" |
| `SearchBar` | "search/filter/filtering" |

### Planning Method

1. Extract functional keywords from user description → match corresponding modules
2. Arrange modules in layout order (top to bottom, left to right)
3. Generate individual component files for each module
4. Main page component composes all modules

Examples:
- "A dashboard with sidebar, stats cards, and a data table" → `Sidebar + StatsCards + DataTable`
- "A login page with email/password inputs and gradient background" → `FormSection(login) + background decoration`
- "A product showcase with top nav and card grid" → `TopNav + CardGrid + Footer`

## Generation Guidelines

### Style Conventions

- All Tailwind CSS 4 utility classes, customize palette via `@theme` in `index.css`
- Default theme: indigo/violet
- Border radius: cards `rounded-xl`, buttons `rounded-lg`, inputs `rounded-lg`
- Shadows: cards `shadow-sm`
- Icons: all from lucide-react

### Code Standards

- Functional components, JSX syntax
- Comment annotations for module sections
- Placeholder images: `https://images.unsplash.com/photo-{id}` or `picsum.photos`

### Responsive

- Sidebar: 240-280px fixed on desktop, hidden/hamburger on mobile
- Content: responsive, max-w-7xl centered
- Card grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

## Notes

- Do not generate `node_modules/`
- Start command: `npm install && npm run dev`
- Tailwind CSS 4 does not use `tailwind.config.js` or `postcss.config.js`
- All icons from lucide-react, no external paid icon libraries
- Use mock data, no real API calls