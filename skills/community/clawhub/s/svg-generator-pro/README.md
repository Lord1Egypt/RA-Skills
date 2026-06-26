# SVG Generator

> 🎨 Generate customizable SVG backgrounds and graphics for websites, presentations, and more

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## ✨ Project Overview

**SVG Generator** is a powerful tool that helps you create beautiful, customizable SVG backgrounds and graphics for various use cases:

- **Website backgrounds** - Hero sections, landing pages, decorative elements
- **Presentation slides** - Professional backgrounds for PowerPoint or Google Slides  
- **Social media graphics** - Eye-catching posts and banners
- **UI decorative elements** - Modern design components for web applications

### 🎯 Key Features

- **4 Distinct Styles** - tech, minimal, geometric, abstract
- **5 Predefined Color Schemes** - plus custom color support
- **Local Execution** - No API costs, completely free and offline-capable
- **Web Ready** - Responsive design optimized for modern web use
- **Easy Integration** - Simple command-line interface with natural language support

### 📐 Output Specifications

| Specification | Details |
|---------------|---------|
| Format | SVG (vector, lossless scaling) |
| Compatibility | All modern browsers, PowerPoint, design tools |
| Responsive | Yes, scales perfectly to any size |
| File Size | Optimized for web performance |

---

## 🚀 Quick Start

### Prerequisites

- Node.js installed on your system
- Basic command-line knowledge

### Basic Usage

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

### Natural Language Support

You can also use natural language commands:
```bash
# Instead of flags, just describe what you want
"Generate a tech-style background with blue-purple colors"
"Create a minimal background for my portfolio website"
"Make an abstract social media post background"
```

---

## 🔧 Available Commands

### `svg-generator` - Main Generation Command

**Purpose**: Generate SVG graphics with specified style and colors

**Syntax**:
```bash
svg-generator --style <style> --colors <scheme> [--output <file>]
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--style` | ✅ | - | Style name: `tech`, `minimal`, `geometric`, or `abstract` |
| `--colors` | ✅ | - | Color scheme or custom hex colors |
| `--output` | ❌ | `./output.svg` | Output file path |

**Style Options**:
- `tech` - Abstract tech elements (data flows, nodes, circuits)
- `minimal` - Clean, simple gradients and shapes  
- `geometric` - Mathematical patterns and geometric shapes
- `abstract` - Artistic abstract compositions

**Color Scheme Options**:
- `blue-purple` - Tech blue to purple gradient
- `gray-blue` - Professional gray to blue
- `teal-cyan` - Modern teal to cyan
- `green-blue` - Nature-inspired green to blue
- `custom` - Specify your own hex colors (e.g., `"#FF6B6B-#4ECDC4"`)

---

### `svg-to-png` - Format Conversion

**Purpose**: Convert SVG files to PNG format for broader compatibility

**Syntax**:
```bash
svg-to-png <input.svg> <output.png> [--width <px>] [--height <px>]
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `<input.svg>` | ✅ | - | Input SVG file |
| `<output.png>` | ✅ | - | Output PNG file |
| `--width` | ❌ | Auto | Output width in pixels |
| `--height` | ❌ | Auto | Output height in pixels |

**Example**:
```bash
# Convert to standard web resolution
svg-to-png hero-bg.svg hero-bg.png --width 1920 --height 1080

# Convert to social media square format
svg-to-png social-post.svg social-post.png --width 1080 --height 1080
```

---

### `ppt-image-generator` - Presentation Integration

**Purpose**: Generate images specifically optimized for presentation templates

**Syntax**:
```bash
ppt-image-generator --template <template> [--output <file>]
```

**Parameters**:

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--template` | ✅ | - | Presentation template style |
| `--output` | ❌ | `./slide-bg.svg` | Output file path |

**Example**:
```bash
# Generate background for modern presentation template
ppt-image-generator --template modern --output slide-bg.svg
```

---

## 🎨 Style Guide

### Tech Style
**Best for**: Technology websites, SaaS products, developer documentation
**Characteristics**: Abstract data flows, node networks, circuit-like patterns
**Recommended colors**: `blue-purple`, `gray-blue`

### Minimal Style  
**Best for**: Professional portfolios, corporate websites, clean designs
**Characteristics**: Simple gradients, subtle shapes, lots of whitespace
**Recommended colors**: `gray-blue`, `teal-cyan`

### Geometric Style
**Best for**: Modern dashboards, data visualization, contemporary designs
**Characteristics**: Mathematical precision, repeating patterns, sharp angles
**Recommended colors**: `teal-cyan`, `green-blue`

### Abstract Style
**Best for**: Creative projects, social media, artistic presentations
**Characteristics**: Organic shapes, flowing forms, artistic compositions  
**Recommended colors**: `green-blue`, custom color combinations

---

## 📁 Project Structure

```
svg-generator-pro/
├── README.md              # Project documentation (this file)
├── SKILL.md               # Skill configuration
├── scripts/               # Core generation scripts
│   ├── generate-svg.js    # Main SVG generation logic
│   ├── svg-to-png.js      # SVG to PNG conversion
│   └── ppt-image-generator.js  # Presentation template integration
├── assets/                # Sample outputs and reference materials
└── _meta.json             # Skill metadata
```

---

## 🔄 Workflow Examples

### Website Hero Background
```bash
# Generate SVG background
svg-generator --style tech --colors blue-purple --output public/hero-bg.svg

# Optional: Convert to PNG for broader compatibility
svg-to-png public/hero-bg.svg public/hero-bg.png --width 1920 --height 1080
```

### Social Media Post
```bash
# Generate abstract background for social media
svg-generator --style abstract --colors teal-cyan --output social-post.svg

# Convert to square format for Instagram/Twitter
svg-to-png social-post.svg social-post.png --width 1080 --height 1080
```

### Presentation Slide
```bash
# Generate background optimized for presentations
ppt-image-generator --template modern --output slide-bg.svg

# Import directly into PowerPoint or Google Slides
```

---

## 💡 Best Practices

### Performance Optimization
- Use SVG format for web backgrounds (smaller file size, perfect scaling)
- Convert to PNG only when necessary for compatibility
- Optimize PNG quality settings based on use case (web vs. print)

### Design Recommendations
- Match style to your brand identity and content type
- Use consistent color schemes across your project
- Consider the readability of text that will be placed over backgrounds

### Integration Tips
- For websites: Use CSS `background-size: cover` for responsive scaling
- For presentations: Test backgrounds with your actual content to ensure readability
- For social media: Always check how backgrounds look on different devices

---

## 📖 Related Skills

- **`pptx-2`** - For advanced PowerPoint integration and automation
- **`diagram`** - For generating complementary diagrams and flowcharts
- **`nima-skill-creator`** - For creating and improving skill documentation

---

## 🤝 Contributing

Contributions are welcome! Common ways to contribute:
- Add new styles or color schemes
- Improve documentation and examples
- Fix bugs or performance issues
- Create new integration scripts

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Special thanks to the OpenCode community and all contributors who make this project possible!

*Built with ❤️ for developers, designers, and creators everywhere.*