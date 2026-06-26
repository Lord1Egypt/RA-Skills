# UI/UX CraftKit ⚡

Design intelligence for AI coding assistants — by **Hardik Amal**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.dev)

## What It Is

**UI/UX CraftKit** is a comprehensive, searchable design database optimized for AI-assisted development. Instead of wasting tokens on generic design advice, leverage pre-researched, ranked design patterns for rapid UI decisions.

Includes:
- **50+ UI Styles** (glassmorphism, neumorphism, minimalism, brutalism, claymorphism, and more)
- **161 Color Palettes** organized by product type and use case
- **57 Font Pairings** with Google Fonts integration
- **161 Product Types** with style recommendations and reasoning
- **99 UX Guidelines** covering accessibility, interaction, and feedback
- **25 Chart Types** with accessibility and library recommendations
- **10 Technology Stacks** (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, HTML/CSS)

All data is **token-optimized for AI** and ranked by priority.

## Features

✅ **BM25 Full-Text Search** — Find design patterns by query  
✅ **Domain-Specific Search** — style, color, typography, product, ux, charts, landing, icons, react, web, google-fonts  
✅ **Stack-Specific Guidelines** — Stack-optimized performance and best practices  
✅ **Design System Generation** — Generate a complete design system from a single query  
✅ **Accessibility-First** — Every recommendation includes WCAG compliance notes  
✅ **Open Source** — MIT licensed, contributions welcome  

## Installation

### Option 1: OpenClaw Integration (Recommended)

```bash
clawhub install ui-ux-craft-kit
```

### Option 2: Clone from GitHub

```bash
git clone https://github.com/hardikamal/ui-ux-craft-kit.git
cd ui-ux-craft-kit
```

## Usage

### Basic Search

```bash
python3 scripts/search.py "SaaS dashboard" --domain product
```

### Search by Domain

```bash
# Get color palettes
python3 scripts/search.py "fintech app" --domain color

# Get font pairings
python3 scripts/search.py "modern minimal" --domain typography

# Get UI styles with AI prompts
python3 scripts/search.py "brutalism" --domain style

# Get accessibility guidelines
python3 scripts/search.py "form validation" --domain ux

# Get chart recommendations
python3 scripts/search.py "time series data" --domain chart
```

### Stack-Specific Search

```bash
python3 scripts/search.py "dark mode dashboard" --stack react-native
```

### Generate Complete Design System

```bash
python3 scripts/search.py "fitness tracking mobile app" --design-system -p "FitTrack"
```

### Limit Results

```bash
python3 scripts/search.py "gradient buttons" --domain style -n 5
```

## Data Included

### Domains

| Domain | File | Records | Purpose |
|--------|------|---------|---------|
| `style` | styles.csv | 50+ | UI styles with AI prompts, best practices, frameworks |
| `color` | colors.csv | 161 | Color palettes by product type and use case |
| `typography` | typography.csv | 57 | Font pairings with Google Fonts integration |
| `product` | products.csv | 161 | Product types with recommended styles |
| `ux` | ux-guidelines.csv | 99 | UX best practices and anti-patterns |
| `chart` | charts.csv | 25 | Chart types with accessibility notes |
| `landing` | landing.csv | 12 | Landing page patterns and conversions |
| `icons` | icons.csv | 8 | Icon library recommendations |
| `design` | design.csv | 100+ | General design system guidelines |
| `app-interface` | app-interface.csv | 50+ | Mobile app interface patterns |
| `react` | react-performance.csv | 25 | React/Next.js performance tips |
| `google-fonts` | google-fonts.csv | 1000+ | Google Fonts catalog |

### Stack-Specific Data

```
data/stacks/
└── react-native.csv    # React Native optimization and best practices
```

## When to Use This Skill

### ✅ Must Use
- Designing new pages (Landing, Dashboard, Admin, SaaS, Mobile App)
- Creating or refactoring UI components (buttons, modals, forms, tables, charts)
- Choosing color schemes, typography, spacing, or layout systems
- Reviewing UI code for accessibility or consistency
- Implementing navigation, animations, or responsive behavior
- Making product-level design decisions

### ❌ Skip
- Pure backend logic
- API/database design only
- Infrastructure or DevOps work

## Quick Reference: Priority Rules

| Priority | Category | Key Checks |
|----------|----------|------------|
| 1 | **Accessibility** | 4.5:1 contrast, focus rings, alt text, aria-labels |
| 2 | **Touch & Interaction** | 44×44px min, 8px gaps, loading states |
| 3 | **Performance** | WebP/AVIF, width/height, font-display: swap |
| 4 | **Style Selection** | Match product type, SVG icons, single CTA |
| 5 | **Layout & Responsive** | Mobile-first, no h-scroll, 4pt grid |
| 6 | **Typography & Color** | 16px+ body, 1.5–1.75 line-height, semantic tokens |
| 7 | **Animation** | 150–300ms, transform/opacity only |
| 8 | **Forms & Feedback** | Visible labels, error placement, 3–5s toasts |
| 9 | **Navigation** | Bottom nav ≤5, predictable back, deep links |
| 10 | **Charts & Data** | Match type to data, legend, tooltips |

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add new design patterns'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

MIT License © 2026 Hardik Amal

See [LICENSE](LICENSE) for details.

## Support

For issues, feature requests, or questions:
- GitHub Issues: [github.com/hardikamal/ui-ux-craft-kit/issues](https://github.com/hardikamal/ui-ux-craft-kit/issues)
- Author: [Hardik Amal](https://github.com/hardikamal)

---

Made with ⚡ by [Hardik Amal](https://github.com/hardikamal)
