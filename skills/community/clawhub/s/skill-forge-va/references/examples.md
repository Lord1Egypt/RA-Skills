# Skill Creator Examples

## Basic Skill Creation

### Step 1: Initialize

```bash
# Create a new skill
skill-creator init my-first-skill

# With template
skill-creator init my-browser-skill --template=browser
```

### Step 2: Edit Metadata

Edit `my-first-skill/_meta.json`:

```json
{
  "name": "my-first-skill",
  "version": "1.0.0",
  "description": "My first skill created with Skill Creator",
  "author": "Your Name",
  "keywords": ["example", "skill"],
  "dependencies": {},
  "requires": {
    "bins": [],
    "tools": []
  }
}
```

### Step 3: Write Documentation

Edit `my-first-skill/SKILL.md`:

```yaml
---
name: my-first-skill
description: "My first skill created with Skill Creator"
version: 1.0.0
author: "Your Name"
---

# My First Skill

## Overview

This is my first skill created with Skill Creator.

## Quick Start

```bash
# Usage example
my-first-skill command
```

## Installation

```bash
# Installation instructions
```

## Usage

```bash
# Detailed usage
```

## Examples

```bash
# More examples
```

## Best Practices

- Follow documentation guidelines
- Test thoroughly
- Keep it focused

## Troubleshooting

- Check dependencies
- Verify metadata format
- Test commands

## License

MIT
```

## Advanced Usage

### Creating a Browser Automation Skill

```bash
# Initialize with browser template
skill-creator init web-scraper --template=browser

# Edit SKILL.md to add specific functionality
# Add browser commands and examples
```

### Creating a Search Engine Skill

```bash
# Initialize with search template
skill-creator init custom-search --template=search

# Configure search engines
# Add search parameters
```

### Creating a Self-Improvement Skill

```bash
# Initialize with self-improve template
skill-creator init learning-agent --template=self-improve

# Add learning tracking
# Configure improvement workflows
```

## Quality Assurance

### Run Quality Check

```bash
skill-creator check my-first-skill
```

### Fix Issues

```bash
# Address any issues found
# Update documentation
# Fix metadata format
```

## Packaging for Distribution

```bash
# Package as zip
skill-creator package my-first-skill --zip

# Install to OpenClaw
skill-creator install my-first-skill --openclaw
```

## Integration Examples

### OpenClaw Integration

```bash
# Install to OpenClaw
skill-creator install my-skill --openclaw

# Verify installation
openclaw skills list
```

### Other Platforms

```bash
# Package for general use
skill-creator package my-skill --zip

# Manual installation
unzip my-skill.zip -d ~/.agents/skills/
```

## Template Customization

### Creating a Custom Template

1. Create a template directory
2. Add SKILL.md and _meta.json templates
3. Use with:

```bash
skill-creator init my-skill --template=custom
```

## Troubleshooting Examples

### Common Issues

#### Skill Not Loading

```bash
# Check metadata format
skill-creator check my-skill

# Fix _meta.json issues
```

#### Command Not Found

```bash
# Check installation
skill-creator install my-skill

# Verify PATH
```

#### Dependency Errors

```bash
# Check requires section in _meta.json
# Install missing dependencies
```

## Best Practices Examples

### Documentation

- Use clear, concise language
- Include practical examples
- Follow Markdown best practices
- Keep documentation up-to-date

### Structure

- Use consistent directory structure
- Follow naming conventions
- Include complete metadata
- Use version control

### Functionality

- Focus on one problem
- Test thoroughly
- Support different use cases
- Follow security best practices