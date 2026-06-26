# OpenClaw Documentation Conventions

Complete reference for documentation formatting, structure, and best practices.

## Frontmatter Schema

All documentation files must start with YAML frontmatter enclosed in `---` delimiters.

### Required Fields

| Field         | Description                                 | Example                                          |
| ------------- | ------------------------------------------- | ------------------------------------------------ |
| `title`       | Page title for SEO and headings (2-3 words) | `title: Browser Hosting`                         |
| `description` | Brief description (1-2 sentences)           | `description: Learn how to use OpenClaw's browser hosting capabilities.` |

### Optional Fields

| Field       | Description                                        | Example                                      |
| ----------- | -------------------------------------------------- | -------------------------------------------- |
| `nav_title` | Shorter title for navigation sidebar               | `nav_title: Browser`                           |
| `source`    | Pull content from another page (avoid duplication) | `source: skills/browser-hosting`             |
| `related`   | Next steps section with related links              | See below                                    |
| `version`   | Development stage indicator                        | `version: experimental`                      |

### Related Links Format

```yaml
---
title: My Feature
description: Description here.
related:
  title: Next Steps
  description: Learn more about related features.
  links:
    - skills/browser-hosting
    - tools/browser
    - guides/automation
---
```

### Version Field Values

- `experimental` - Experimental feature, may change
- `legacy` - Legacy feature, consider alternatives  
- `unstable` - Unstable API, not recommended for production
- `RC` - Release candidate

## Code Block Conventions

### Basic Syntax

````
```language filename="path/to/file.ext"
code here
```
````

### Required Attributes

| Attribute   | When to Use                       | Example                   |
| ----------- | --------------------------------- | ------------------------- |
| `filename`  | Always for code examples          | `filename="skills/my-skill/SKILL.md"` |
| `switcher`  | When providing multiple variants  | `switcher`                |
| `highlight` | To highlight specific lines       | `highlight={1,3-5}`       |

### Language Examples

**Python:**
```python filename="scripts/example.py"
#!/usr/bin/env python3
print("Hello, OpenClaw!")
```

**JSON:**
```json filename="config/openclaw.json"
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw"
  }
}
```

**Bash:**
```bash
openclaw browser --browser-profile openclaw start
```

### Highlighting Lines

```
highlight={1}        # Single line
highlight={1,3}      # Multiple lines  
highlight={1-5}      # Range
highlight={1,3-5,8}  # Combined
```

## File Structure

### Skill Documentation

Skills should be documented in the `docs/skills/` directory with the following structure:

```
docs/skills/
├── skill-name.md          # Main documentation
└── references/            # Reference materials (optional)
    ├── api-reference.md
    └── examples.md
```

### Guide Documentation

Guides should be organized by category in the `docs/guides/` directory:

```
docs/guides/
├── getting-started.md
├── automation/
│   ├── browser-automation.md
│   └── web-scraping.md
└── configuration/
    ├── browser-config.md
    └── security.md
```

## Writing Style

### Voice

- **Guides:** Instructional, use "you" to address users
- **API Reference:** Technical, use imperative verbs ("create", "pass", "return")
- **Skill Docs:** Practical, focus on use cases and examples

### Clarity

- Use plain words over complex alternatives
- Be specific: "the `profile` parameter" not "this parameter"
- Avoid jargon unless explaining it
- Include concrete examples for all concepts

### Structure

Typical page structure:

1. **Brief introduction** (what and why)
2. **Quick start example** (minimal working example)
3. **Detailed reference/options** (comprehensive coverage)
4. **Advanced examples** (different use cases)
5. **Related links** (via frontmatter)

## Validation Commands

```bash
# Check documentation formatting
openclaw docs validate

# Lint all markdown files  
openclaw docs lint

# Build documentation site
openclaw docs build
```

## Common Patterns

### New Skill Documentation

1. Create file at `docs/skills/skill-name.md`
2. Include YAML frontmatter with title and description
3. Add quick start section with basic usage
4. Provide detailed reference with all options
5. Include practical examples
6. Add related links in frontmatter

### API Reference Updates

1. Identify changed exports or parameters
2. Update the props table or parameter list
3. Add new sections explaining changes
4. Include migration guidance for breaking changes
5. Update examples to reflect new behavior

### Configuration Documentation

1. Document new configuration options
2. Provide default values and valid ranges
3. Include example configurations
4. Explain security implications if applicable
5. Link to related configuration sections

This documentation convention ensures consistency across all OpenClaw documentation while maintaining flexibility for different types of content.