---
name: svg-generator
description: Generate customizable SVG backgrounds and graphics with multiple styles (tech, minimal, geometric, abstract) and color schemes. Use when creating website backgrounds, presentation slides, social media graphics, or UI decorative elements.
---

# SVG Generator Skill

Generate beautiful, customizable SVG backgrounds and graphics for websites, presentations, and more.

## Features
- **4 Styles**: tech, minimal, geometric, abstract
- **5 Color Schemes**: blue-purple, gray-blue, teal-cyan, green-blue, custom
- **Local Execution**: No API costs, completely free
- **Web Ready**: Responsive design, optimized for web use

## Quick Start

```bash
# Generate tech-style background
svg-generator --style tech --colors blue-purple --output hero-bg.svg

# Generate minimal background
svg-generator --style minimal --colors gray-blue --output simple-bg.svg

# Generate geometric pattern
svg-generator --style geometric --colors teal-cyan --output pattern-bg.svg

# Generate abstract art
svg-generator --style abstract --colors green-blue --output art-bg.svg
```

## Styles Available

| Style | Description | Best For |
|-------|-------------|----------|
| `tech` | Abstract tech elements (data flows, nodes, circuits) | Tech websites, SaaS landing pages |
| `minimal` | Clean, simple gradients and shapes | Professional sites, portfolios |
| `geometric` | Mathematical patterns and geometric shapes | Modern designs, dashboards |
| `abstract` | Artistic abstract compositions | Creative projects, social media |

## Color Schemes

| Scheme | Colors | Use Case |
|--------|--------|----------|
| `blue-purple` | Tech blue to purple gradient | SaaS, tech products |
| `gray-blue` | Professional gray to blue | Corporate, business |
| `teal-cyan` | Modern teal to cyan | Fresh, modern designs |
| `green-blue` | Nature-inspired green to blue | Eco, wellness brands |
| `custom` | Specify your own hex colors | Brand-specific needs |

## Advanced Usage

### Custom Colors
```bash
svg-generator --style tech --colors "#FF6B6B-#4ECDC4" --output custom.svg
```

### Generate PNG
```bash
# First generate SVG, then convert
svg-to-png input.svg output.png --width 1920 --height 1080
```

## Bundled Resources

### Scripts
- `scripts/generate-svg.js` - Main SVG generation script
- `scripts/svg-to-png.js` - Convert SVG to PNG
- `scripts/ppt-image-generator.js` - Generate images for PPT templates

### Assets
- `assets/` - Sample SVG outputs for reference

## Integration Examples

### Website Hero Background
```bash
svg-generator --style tech --colors blue-purple --output public/hero-bg.svg
```

### Social Media Post
```bash
svg-generator --style abstract --colors teal-cyan --output social-post.svg
svg-to-png social-post.svg social-post.png --width 1080 --height 1080
```

### Presentation Slide
```bash
ppt-image-generator --template modern --output slide-bg.svg
```

## Related Skills
- `pptx-2` - For integrating SVG into PowerPoint presentations
- `diagram` - For generating diagrams alongside backgrounds
