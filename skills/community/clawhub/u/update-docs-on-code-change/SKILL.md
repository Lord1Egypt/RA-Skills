---
name: update-docs-on-code-change
description: 'Automatically update README.md and documentation files when application code changes require documentation updates. Use when adding new features, changing APIs, modifying configuration options, updating installation procedures, or making breaking changes. Triggers on code modifications that affect user-facing documentation, changelog entries, migration guides, or code examples.'
---

# Update Documentation on Code Change

A skill for keeping documentation synchronized with code changes. Automatically detects when README.md, API documentation, configuration guides, and other documentation files need updates based on code modifications.

## When to Use This Skill

- Adding new features or functionality
- Changing API endpoints, methods, or interfaces
- Introducing breaking changes
- Modifying dependencies or requirements
- Changing configuration options or environment variables
- Updating installation or setup procedures
- Modifying CLI commands or scripts
- When code examples in documentation become outdated

## Prerequisites

- Understanding of the project's documentation structure
- Access to code changes being made
- Knowledge of documentation files that may need updates

## Documentation Update Workflows

### README.md Updates

**Update README.md when:**

1. Adding new features or capabilities
   - Add feature description to "Features" section
   - Include usage examples if applicable
   - Update table of contents if present

2. Modifying installation or setup process
   - Update "Installation" or "Getting Started" section
   - Revise dependency requirements
   - Update prerequisite lists

3. Adding new CLI commands or options
   - Document command syntax and examples
   - Include option descriptions and default values
   - Add usage examples

4. Changing configuration options
   - Update configuration examples
   - Document new environment variables
   - Update config file templates

### API Documentation Updates

**Sync API documentation when:**

1. New endpoints are added
   - Document HTTP method, path, parameters
   - Include request/response examples
   - Update OpenAPI/Swagger specs

2. Endpoint signatures change
   - Update parameter lists
   - Revise response schemas
   - Document breaking changes

3. Authentication or authorization changes
   - Update authentication examples
   - Revise security requirements
   - Update API key/token documentation

### Code Example Synchronization

**Verify and update code examples when:**

1. Function signatures change
   - Update all code snippets using the function
   - Verify examples still compile/run
   - Update import statements if needed

2. API interfaces change
   - Update example requests and responses
   - Revise client code examples
   - Update SDK usage examples

### Changelog Management

**Add changelog entries for:**

- New features (under "Added" section)
- Bug fixes (under "Fixed" section)
- Breaking changes (under "Changed" section with **BREAKING** prefix)
- Deprecated features (under "Deprecated" section)
- Removed features (under "Removed" section)
- Security fixes (under "Security" section)

**Changelog format:**

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description with reference to PR/issue

### Changed
- **BREAKING**: Description of breaking change
- Other changes

### Fixed
- Bug fix description
```

### Migration Guides

**Create migration guides when:**

1. Breaking API changes occur
   - Document what changed
   - Provide before/after examples
   - Include step-by-step migration instructions

2. Major version updates
   - List all breaking changes
   - Provide upgrade checklist
   - Include common migration issues and solutions

3. Deprecating features
   - Mark deprecated features clearly
   - Suggest alternative approaches
   - Include timeline for removal

## Documentation File Structure

Maintain these documentation files and update as needed:

- **README.md**: Project overview, quick start, basic usage
- **CHANGELOG.md**: Version history and user-facing changes
- **docs/**: Detailed documentation
  - `installation.md`: Setup and installation guide
  - `configuration.md`: Configuration options and examples
  - `api.md`: API reference documentation
  - `contributing.md`: Contribution guidelines
  - `migration-guides/`: Version migration guides
- **examples/**: Working code examples and tutorials

## Documentation Quality Standards

### Writing Guidelines

- Use clear, concise language
- Include working code examples
- Provide both basic and advanced examples
- Use consistent terminology
- Include error handling examples
- Document edge cases and limitations

### Code Example Format

```markdown
### Example: [Clear description of what example demonstrates]

\`\`\`language
// Include necessary imports/setup
import { function } from 'package';

// Complete, runnable example
const result = function(parameter);
console.log(result);
\`\`\`

**Output:**
\`\`\`
expected output
\`\`\`
```

### API Documentation Format

```markdown
### `functionName(param1, param2)`

Brief description of what the function does.

**Parameters:**
- `param1` (type): Description of parameter
- `param2` (type, optional): Description with default value

**Returns:**
- `type`: Description of return value

**Example:**
\`\`\`language
const result = functionName('value', 42);
\`\`\`

**Throws:**
- `ErrorType`: When and why error is thrown
```

## Best Practices

### Do's

- Update documentation in the same commit as code changes
- Include before/after examples for changes to be reviewed
- Test code examples before committing
- Use consistent formatting and terminology
- Document limitations and edge cases
- Provide migration paths for breaking changes
- Keep documentation DRY (link instead of duplicating)

### Don'ts

- Commit code changes without updating documentation
- Leave outdated examples in documentation
- Document features that don't exist yet
- Use vague or ambiguous language
- Forget to update changelog
- Ignore broken links or failing examples
- Document implementation details users don't need

## Validation Commands

Example scripts for documentation validation:

```json
{
  "scripts": {
    "docs:build": "Build documentation",
    "docs:test": "Test code examples in docs",
    "docs:lint": "Lint documentation files",
    "docs:links": "Check for broken links",
    "docs:spell": "Spell check documentation",
    "docs:validate": "Run all documentation checks"
  }
}
```

## Review Checklist

Before completing documentation updates:

- [ ] README.md reflects current project state
- [ ] All new features are documented
- [ ] Code examples are tested and work
- [ ] API documentation is complete and accurate
- [ ] Configuration examples are up to date
- [ ] Breaking changes are documented with migration guide
- [ ] CHANGELOG.md is updated
- [ ] Links are valid and not broken
- [ ] Installation instructions are current
- [ ] Environment variables are documented

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Outdated code examples | Re-run examples against current code and update |
| Missing API documentation | Review all public interfaces and document each |
| Broken links | Use link checker tools to identify and fix |
| Inconsistent terminology | Create a glossary and standardize usage |
| Missing changelog entry | Add entry following the changelog format |
