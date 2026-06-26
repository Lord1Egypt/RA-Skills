***

name: skill-forge
description: "A powerful tool for forging high-quality skills with best practices, templates, and intelligent guidance. Includes structure templates, documentation standards, and quality assurance checklists."
author: "@Variya"
-----------------

# Skill Forge

A powerful tool for forging high-quality skills with best practices, templates, and intelligent guidance.

## Overview

Skill Forge helps you build professional-grade skills by providing:

- Standardized directory structure templates
- Comprehensive documentation guidelines
- Quality assurance checklists
- Best practices from top-performing skills
- Step-by-step creation workflow

## Quick Start

```bash
# Create a new skill
skill-forge init <skill-name>

# Wrap existing tool
skill-forge wrap <skill-name> --script=<path> or --binary=<path>

# Add documentation
skill-forge docs <skill-name>

# Run quality check
skill-forge check <skill-name>

# Package for distribution
skill-forge package <skill-name>
```

## Directory Structure

### Recommended Structure

```
skill-name/
├── SKILL.md             # Main documentation
├── _meta.json           # Skill metadata
├── references/          # Additional documentation
│   └── examples.md      # Usage examples
├── assets/              # Static assets
├── scripts/             # Helper scripts
└── hooks/               # Integration hooks
```

### Structure Components

| Component     | Purpose                                     | Required |
| ------------- | ------------------------------------------- | -------- |
| `SKILL.md`    | Main documentation and usage guide          | ✅ Yes    |
| `_meta.json`  | Skill metadata (name, version, description) | ✅ Yes    |
| `references/` | Additional documentation and examples       | ❌ No     |
| `assets/`     | Static assets like templates or images      | ❌ No     |
| `scripts/`    | Helper scripts for installation or usage    | ❌ No     |
| `hooks/`      | Integration hooks for agent platforms       | ❌ No     |

## SKILL.md Template

### Frontmatter

```yaml
---
name: skill-name
description: "Brief description of what the skill does and when to use it"
version: 1.0.0
author: "Your Name"
metadata: {"clawdbot":{"emoji":"🔧"}}
allowed-tools: Bash(skill-name:*)
---
```

### Content Sections

1. **Overview** - Brief introduction and purpose
2. **Quick Start** - Basic usage examples
3. **Installation** - Setup instructions
4. **Usage** - Detailed usage guide
5. **Examples** - Practical use cases
6. **Best Practices** - Recommended approaches
7. **Troubleshooting** - Common issues and solutions
8. **License** - Licensing information

## \_meta.json Template

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "Brief description of the skill",
  "author": "Your Name",
  "keywords": ["skill", "category", "functionality"],
  "dependencies": {},
  "requires": {
    "bins": [],
    "tools": []
  }
}
```

## Creation Workflow

### Step 1: Initialize

```bash
# Create basic structure
skill-forge init <skill-name>

# With template
skill-forge init <skill-name> --template=browser
```

### Step 2: Define Metadata

Edit `_meta.json` with your skill's details:

- Name (must match directory name)
- Version (semantic versioning)
- Description (clear and concise)
- Author information
- Dependencies and requirements

### Step 3: Write Documentation

Create comprehensive `SKILL.md` with:

- Clear frontmatter
- Detailed overview
- Installation instructions
- Usage examples
- Best practices
- Troubleshooting guide

### Step 4: Add Examples

Create `references/examples.md` with:

- Practical use cases
- Code examples
- Common workflows

### Step 5: Quality Assurance

Run quality checks:

```bash
skill-forge check <skill-name>
```

### Step 6: Package for Distribution

```bash
skill-forge package <skill-name>
```

## Wrapping Existing Tools

You can wrap existing scripts or binary files into a skill using the `wrap` command:

### Basic Usage

```bash
# Wrap a script
skill-forge wrap <skill-name> --script=/path/to/script.sh

# Wrap a binary
skill-forge wrap <skill-name> --binary=/path/to/binary
```

### Advanced Usage

```bash
# Wrap a GitHub repository
skill-forge wrap <skill-name> --github=https://github.com/username/repository

# With custom options
skill-forge wrap <skill-name> --script=/path/to/script.py --description="Custom skill description"
```

### What it does

1. **Analyzes the tool** - Examines the script or binary to understand its functionality
2. **Creates skill structure** - Generates the complete skill directory structure
3. **Generates wrapper script** - Creates a script that calls the original tool
4. **Creates documentation** - Generates SKILL.md with usage examples
5. **Adds metadata** - Creates \_meta.json with tool dependencies

### Example: Wrapping a Backup Script

```bash
# Create skill from backup script
skill-forge wrap backup-skill --script=./backup.sh

# Check the skill
skill-forge check backup-skill

# Install to OpenClaw
skill-forge install backup-skill --openclaw
```

### Example: Wrapping a System Tool

```bash
# Create skill from curl
skill-forge wrap curl-skill --binary=curl

# Use the skill
curl-skill --help
curl-skill https://example.com
```

## Dependency Management

Skill Forge provides tools to manage dependencies and find alternatives for missing tools:

### Checking Dependencies

```bash
# Check skill dependencies
skill-forge check <skill-name>

# Example output
# 🔍 Checking dependencies...
# ✅ Dependency found: python3
# ❌ Dependency missing: excel
#    Suggested solution: Install excel or use alternative
```

### Installing Dependencies

```bash
# Install dependencies for a skill
skill-forge install-deps <skill-name>

# Example output
# Installing dependencies for skill excel-skill...
# Attempting to install excel...
# ✅ Successfully installed excel
# ✅ Dependency installation complete!
```

### Finding Alternatives

```bash
# Find alternatives for missing dependencies
skill-forge find-alternatives <skill-name>

# Example output
# Finding alternatives for skill excel-skill...
# 🔍 Checking for alternatives...
# ❌ Dependency missing: excel
# ✅ Alternative for excel: xlsx
#    Description: Node.js library for Excel file processing
#    Installation: npm install xlsx
```

## Common Dependency Solutions

### Excel Processing

If you need to create a skill for Excel processing but don't have Excel installed:

1. **Use Node.js xlsx library**:
   ```bash
   npm install xlsx
   skill-forge wrap excel-skill --script=./excel-processor.js
   ```
2. **Use Python pandas**:
   ```bash
   pip install pandas openpyxl
   skill-forge wrap excel-skill --script=./excel-processor.py
   ```
3. **Use LibreOffice**:
   ```bash
   winget install TheDocumentFoundation.LibreOffice
   skill-forge wrap excel-skill --binary=soffice
   ```

### Python Scripts

If your skill requires Python but it's not installed:

```bash
# Install Python
winget install Python.Python.3.10

# Create and use Python-based skill
skill-forge wrap python-skill --script=./script.py
```

### Node.js Scripts

If your skill requires Node.js but it's not installed:

```bash
# Install Node.js
winget install OpenJS.NodeJS

# Create and use Node.js-based skill
skill-forge wrap node-skill --script=./script.js
```

## Intelligent Skill Creation

Skill Forge automatically integrates research and analysis into the skill creation process:

### Smart Initialization

When you create a new skill, the system automatically:

1. **Searches for relevant existing projects** - Scans GitHub and ClawHub for similar skills
2. **Analyzes top projects** - Extracts best practices and structural patterns
3. **Provides recommendations** - Offers suggestions based on successful projects
4. **Ensures security** - Scans for potential security issues in referenced code

### Example Workflow

```bash
# 1. Create a new skill (with automatic research)
skill-forge init my-excel-skill

# 2. The system automatically searches for relevant projects
#    and provides recommendations based on best practices

# 3. Implement features with guidance from research
# (edit SKILL.md and other files)

# 4. Test and refine
skill-forge check my-excel-skill
skill-forge package my-excel-skill
```

### How It Works

- **Background Research**: The system searches for existing skills related to your topic
- **Pattern Analysis**: It identifies common structures and successful approaches
- **Security Scanning**: Any referenced code is checked for potential issues
- **Intelligent Recommendations**: You receive tailored suggestions for your skill

This approach ensures you benefit from existing knowledge while maintaining focus on creating your unique skill.

## Best Practices

### Documentation

- **Be clear and concise** - Explain what the skill does and when to use it
- **Include examples** - Provide practical usage scenarios
- **Use consistent formatting** - Follow Markdown best practices
- **Keep it up-to-date** - Update documentation with version changes

### Structure

- **Keep it organized** - Use clear directory structure
- **Follow naming conventions** - Lowercase with hyphens
- **Include metadata** - Complete \_meta.json file
- **Use version control** - Track changes with git

### Functionality

- **Be focused** - Solve one problem well
- **Be reliable** - Test thoroughly
- **Be flexible** - Support different use cases
- **Be secure** - Follow security best practices

## Quality Assurance Checklist

### Required Files

- [ ] `SKILL.md` exists and is complete
- [ ] `_meta.json` exists with correct format
- [ ] All links are valid
- [ ] Examples are working

### Documentation Quality

- [ ] Clear frontmatter with all required fields
- [ ] Detailed overview section
- [ ] Step-by-step installation instructions
- [ ] Comprehensive usage guide
- [ ] Practical examples
- [ ] Troubleshooting section

### Code Quality (if applicable)

- [ ] No syntax errors
- [ ] Proper error handling
- [ ] Consistent coding style
- [ ] No hardcoded values

## Templates

### Browser Automation Template

```bash
skill-forge init my-browser-skill --template=browser
```

### Search Engine Template

```bash
skill-forge init my-search-skill --template=search
```

### Self-Improvement Template

```bash
skill-forge init my-improvement-skill --template=self-improve
```

## Integration

### OpenClaw

```bash
# Install to OpenClaw
skill-forge install <skill-name> --openclaw
```

### Other Platforms

```bash
# Package for general use
skill-forge package <skill-name> --zip
```

## Version Control

### Recommended Git Workflow

1. Initialize git repository
2. Create .gitignore file
3. Commit initial structure
4. Tag releases with semantic versioning

### .gitignore Example

```gitignore
# Dependencies
node_modules/

# Build output
build/
dist/

# Environment variables
.env
.env.local

# IDE files
.vscode/
.idea/

# Local learnings (optional)
.learnings/
```

## Troubleshooting

### Common Issues

| Issue             | Solution                                          |
| ----------------- | ------------------------------------------------- |
| Skill not loading | Check \_meta.json format and SKILL.md frontmatter |
| Command not found | Ensure skill is properly installed and in PATH    |
| Dependency errors | Check requires section in \_meta.json             |

### Debugging

```bash
# Enable verbose mode
skill-forge init <skill-name> --verbose

# Check skill structure
skill-forge check <skill-name> --detailed
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For questions or issues:

- Open an issue on GitHub
- Contact the maintainers
- Check the documentation

***

*Skill Forge - Forging the future of skills, one creation at a time.*
