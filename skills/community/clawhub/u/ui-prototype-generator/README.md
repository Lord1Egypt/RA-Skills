# UI Prototype Generator

Transform reference images or descriptions into interactive prototypes. Generate HTML by default, or Figma designs via API when explicitly requested.

## Overview

**Skill Name**: `ui-prototype-generator`

**Version**: 1.0.0

**Author**: OpenClaw Community

**License**: MIT

## Description

UI Prototype Generator is a comprehensive skill for creating interactive prototypes from reference images or text descriptions. It supports two output formats:

1. **HTML (Default)**: Self-contained web prototypes with CSS/JS
2. **Figma (Optional)**: Design files via Figma API

## Features

### Core Capabilities

- ✅ **Image Analysis**: Parse screenshots to extract UI components
- ✅ **HTML Generation**: Semantic HTML5 with modern CSS
- ✅ **Figma Integration**: API-based design generation
- ✅ **Component Library**: Forms, tables, modals, navigation
- ✅ **Responsive Design**: Mobile-friendly layouts
- ✅ **Interactive States**: Hover, focus, active states
- ✅ **Rapid Iteration**: Quick modifications based on feedback

### Output Formats

| Format | Default | Use Case | Requirements |
|--------|---------|----------|--------------|
| HTML | ✅ Yes | Web preview, testing, sharing | None |
| Figma | ❌ No | Design handoff, collaboration | Figma API token |

## Installation

### Via OpenClaw CLI

```bash
openclaw skills install ui-prototype-generator
```

### Manual Installation

1. Download `ui-prototype-generator.skill`
2. Copy to OpenClaw skills directory:
   ```bash
   cp ui-prototype-generator.skill ~/.openclaw/skills/
   ```
3. Restart OpenClaw:
   ```bash
   openclaw gateway restart
   ```

## Configuration

### Figma API Setup (Optional)

For Figma output format:

1. Get Figma Personal Access Token:
   - Visit: https://www.figma.com/settings
   - Generate new token

2. Create auth-profiles.json:
   ```bash
   # Location: ~/.openclaw/agents/main/agent/auth-profiles.json
   {
     "profiles": {
       "figma": {
         "provider": "figma",
         "access_token": "YOUR_TOKEN_HERE",
         "token_type": "Bearer"
       }
     }
   }
   ```

## Usage

### Basic Usage (HTML - Default)

```
User: "Create a prototype from this screenshot"
→ Generates HTML file
```

### Figma Usage (Explicit)

```
User: "Create a Figma prototype from this image"
→ Calls Figma API → Returns Figma file URL
```

### Examples

#### Example 1: Admin Dashboard

**Input**: Screenshot of admin panel

**Output**: `admin-dashboard.html`

**Features**:
- Sidebar navigation
- Data table with filters
- Responsive layout

#### Example 2: Form Modal

**Input**: "Create a modal form with name, email, and submit button"

**Output**: `modal-form.html`

**Features**:
- Form validation
- Interactive buttons
- Clean styling

#### Example 3: Figma Design

**Input**: "Generate Figma design for this login page"

**Output**: Figma file URL

**Features**:
- Component structure
- Auto-layout
- Design tokens

## File Structure

```
ui-prototype-generator/
├── SKILL.md                          # Skill definition
├── README.md                         # This file
├── CHANGELOG.md                      # Version history
├── LICENSE                           # MIT License
├── auth-profiles.template.json       # Auth template
├── references/
│   ├── EXAMPLES.md                   # Usage examples
│   ├── HTML_COMPONENTS.md            # HTML component docs
│   └── FIGMA_COMPONENTS.md           # Figma component docs
├── scripts/
│   ├── html_generator.py             # HTML generation
│   └── figma_generator.py            # Figma API integration
└── plugins/
    └── figma-plugin/                 # Figma import plugin
        ├── manifest.json
        ├── code.js
        └── ui.html
```

## API Reference

### HTML Generator

```python
from scripts.html_generator import HTMLPrototypeGenerator

generator = HTMLPrototypeGenerator()
generator.generate_from_description(
    description="Admin dashboard with sidebar",
    output_name="dashboard"
)
```

### Figma Generator

```python
from scripts.figma_generator import FigmaPrototypeGenerator

generator = FigmaPrototypeGenerator()
generator.create_prototype(
    name="My Design",
    nodes=[...]
)
```

## Components

### HTML Components

- **Forms**: Input, Select, Radio, Checkbox, Textarea
- **Tables**: Sortable, filterable, with actions
- **Navigation**: Header, Sidebar, Breadcrumbs, Tabs
- **Feedback**: Modals, Tooltips, Alerts, Progress
- **Data Display**: Cards, Lists, Badges, Tags

### Figma Components

- **Frames**: Layout containers
- **Shapes**: Rectangle, Ellipse, Line
- **Text**: Labels, Headings, Paragraphs
- **Effects**: Shadows, Blur
- **Auto-layout**: Responsive containers

## Design System

### Colors

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| Primary | #1890ff | rgb(24,144,255) | Buttons, links |
| Success | #52c41a | rgb(82,196,26) | Success states |
| Warning | #faad14 | rgb(250,173,20) | Warnings |
| Error | #ff4d4f | rgb(255,77,79) | Errors |
| Text | #333333 | rgb(51,51,51) | Body text |
| Border | #e8e8e8 | rgb(232,232,232) | Borders |

### Typography

- **Font Family**: Inter, -apple-system, BlinkMacSystemFont
- **Base Size**: 14px
- **Scale**: 12px, 14px, 16px, 18px, 20px, 24px

### Spacing

- **Base Unit**: 8px
- **Scale**: 4px, 8px, 16px, 24px, 32px, 48px

## Troubleshooting

### Common Issues

#### HTML not rendering
- Check browser console for errors
- Ensure CSS is embedded in `<style>` tag
- Verify file encoding is UTF-8

#### Figma API errors
- Verify token in auth-profiles.json
- Check token permissions in Figma settings
- Ensure token hasn't expired

#### Plugin not working
- Verify manifest.json format
- Check Figma plugin API version
- Review browser console for errors

### Debug Mode

Enable debug logging:

```bash
export UI_PROTOTYPE_DEBUG=1
python3 scripts/html_generator.py --input image.png
```

## Contributing

### Development Setup

```bash
git clone https://github.com/openclaw/ui-prototype-generator.git
cd ui-prototype-generator
pip install -r requirements.txt
```

### Testing

```bash
python3 -m pytest tests/
```

### Submitting Changes

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## Roadmap

### v1.1.0 (Planned)
- [ ] Sketch format support
- [ ] Adobe XD integration
- [ ] Component variants
- [ ] Animation support

### v1.2.0 (Planned)
- [ ] Design token export
- [ ] Theme customization
- [ ] Batch processing
- [ ] API rate limiting

## Support

### Documentation
- Full docs: https://docs.openclaw.ai/skills/ui-prototype-generator
- Examples: See `references/EXAMPLES.md`

### Community
- Discord: https://discord.gg/clawd
- GitHub Issues: https://github.com/openclaw/ui-prototype-generator/issues

### Commercial Support
- Enterprise licensing available
- Custom development services
- Training and consulting

## Credits

### Contributors
- OpenClaw Community
- Figma API Team
- Open source contributors

### Third-Party
- Inter font family
- Figma Plugin API
- OpenClaw Framework

## License

MIT License - see LICENSE file for details

## Changelog

See CHANGELOG.md for version history

---

**Made with ❤️ by the OpenClaw Community**