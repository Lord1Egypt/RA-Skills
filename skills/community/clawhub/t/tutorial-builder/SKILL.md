---
name: tutorial-builder
description: Generate comprehensive step-by-step tutorials for tools, workflows, and technical topics. Use when the user asks to create a tutorial, write a guide, explain how to use something, or document a process. Includes structure for prerequisites, installation, steps, examples, and troubleshooting.
---

# Tutorial Builder

## Overview

Create clear, actionable tutorials that guide readers through complex tasks. Structure content logically with prerequisites, step-by-step instructions, code examples, and troubleshooting tips.

## Tutorial Structure

Always include these sections (adapt to the topic):

### 1. Title and Description
- Clear, descriptive title
- One-sentence summary of what the tutorial covers
- Target audience (beginner, intermediate, advanced)
- Estimated time to complete

### 2. Prerequisites
- List required skills, knowledge, or tools
- Include version numbers if applicable
- Add links to prerequisite tutorials or documentation

### 3. Installation/Setup (if applicable)
- Step-by-step installation instructions
- Include commands with expected output examples
- Address common installation issues
- Verification step to confirm setup worked

### 4. Core Tutorial Steps
Numbered steps with:
- Clear action verbs ("Create", "Configure", "Deploy")
- Command examples with prompts (`$` for user commands, `#` for root)
- Code blocks with syntax highlighting notes
- Explanation of what each step does and why
- Expected outputs or results

### 5. Examples and Use Cases
- Real-world examples
- Variations and common modifications
- Integration examples with other tools

### 6. Troubleshooting
- Common errors and solutions
- Debugging tips
- Where to get help (forums, docs, community)

### 7. Next Steps
- Recommended follow-up tutorials
- Advanced topics to explore
- Related resources

## Writing Guidelines

### Tone and Style
- Be direct and concise. Avoid filler words.
- Assume the reader is smart but unfamiliar with the topic.
- Explain the "why" behind steps, not just the "how."
- Use consistent terminology throughout.

### Code and Commands
- Show the complete command, not fragments.
- Include prompts (`$`, `#`, `>`) to distinguish command types.
- Add comments for complex commands (`# comment`).
- Show expected output when it helps verify success.

### Examples
```bash
# Install the package
$ npm install package-name

# Verify installation
$ package-name --version
v1.2.3
```

```yaml
# Configure settings in config.yaml
database:
  host: localhost
  port: 5432
```

### Formatting
- Use **bold** for key commands, file names, and important terms
- Use `code` for inline code, variables, and short commands
- Use blockquotes for warnings or notes:
  > **Note:** This step requires sudo privileges.
- Use numbered lists for sequential steps
- Use bullet points for non-sequential items

### Common Patterns

#### For Software Installation
1. Check for existing installation
2. Download or clone
3. Install with package manager or build from source
4. Configure if needed
5. Verify installation
6. Add to PATH if required

#### For Configuration Tasks
1. Locate configuration file
2. Backup existing configuration
3. Edit with specific settings
4. Validate configuration
5. Reload or restart service
6. Test configuration

#### For Development Workflows
1. Set up development environment
2. Create project structure
3. Write initial code/templates
4. Test basic functionality
5. Add features incrementally
6. Document and commit

## Quality Checklist

Before finalizing a tutorial, verify:

- [ ] All steps are numbered and sequential
- [ ] Every command is complete and copy-paste ready
- [ ] Code examples match the text description
- [ ] Troubleshooting section addresses common issues
- [ ] Prerequisites are clearly listed
- [ ] Links and references are accurate
- [ ] Steps are tested and verified to work
- [ ] Language is clear and jargon-free (or jargon is explained)

## Output Format

Deliver the tutorial in a format matching the user's preference:
- Markdown (default) - for documentation sites, Git repos, wikis
- Plain text - for simple documentation
- HTML - if creating web content

Ask the user if they have a preferred output format if not specified.
