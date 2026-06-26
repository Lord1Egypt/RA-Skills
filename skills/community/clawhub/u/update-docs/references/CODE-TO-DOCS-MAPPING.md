# Code to Documentation Mapping for OpenClaw

Maps OpenClaw source code directories to their corresponding documentation files.

## Core Mappings

### Skills
| Source Path | Documentation Path |
|-------------|-------------------|
| `skills/browser-hosting/` | `docs/skills/browser-hosting.md` |
| `skills/weather/` | `docs/skills/weather.md` |
| `skills/pptx-creator/` | `docs/skills/pptx-creator.md` |
| `skills/feishu-doc/` | `docs/skills/feishu-doc.md` |

### Core Components
| Source Path | Documentation Path |
|-------------|-------------------|
| `src/core/agent.ts` | `docs/api/agent.md` |
| `src/core/tools.ts` | `docs/api/tools.md` |
| `src/core/memory.ts` | `docs/api/memory.md` |
| `src/core/browser.ts` | `docs/api/browser.md` |

### API Reference
| Source Path | Documentation Path |
|-------------|-------------------|
| `src/api/browser.ts` | `docs/api/browser.md` |
| `src/api/tools.ts` | `docs/api/tools.md` |
| `src/api/memory.ts` | `docs/api/memory.md` |
| `src/api/skills.ts` | `docs/api/skills.md` |

### Configuration
| Source Path | Documentation Path |
|-------------|-------------------|
| `src/config/gateway.ts` | `docs/config/gateway.md` |
| `src/config/browser.ts` | `docs/config/browser.md` |
| `src/config/skills.ts` | `docs/config/skills.md` |

### Guides and Tutorials
| Source Path | Documentation Path |
|-------------|-------------------|
| `examples/basic-agent/` | `docs/guides/basic-agent.md` |
| `examples/browser-automation/` | `docs/guides/browser-automation.md` |
| `examples/skill-creation/` | `docs/guides/skill-creation.md` |

## Directory Pattern Mappings

### By Feature Area
| Source Directory | Documentation Area | Notes |
|------------------|-------------------|-------|
| `skills/` | `docs/skills/` | Individual skill documentation |
| `src/api/` | `docs/api/` | Core API reference |
| `src/config/` | `docs/config/` | Configuration guides |
| `examples/` | `docs/guides/` | Tutorial and example guides |
| `src/core/` | `docs/architecture/` | Core architecture documentation |

### File Type Mappings
| Source Extension | Documentation Extension | Notes |
|------------------|------------------------|-------|
| `.ts` / `.js` | `.md` | TypeScript/JavaScript to Markdown |
| `.py` | `.md` | Python scripts to Markdown |
| Directories | Index files (`index.md`) | Directory structure to navigation |

## Finding Related Documentation

### Step 1: Identify the changed export
Look at what's exported from the changed file:
- Public API exports → API Reference docs
- Skill implementations → Skill documentation  
- Configuration options → Config docs
- Examples → Guide documentation

### Step 2: Search for existing docs
Use OpenClaw's built-in tools for searching:
- **Find docs mentioning a term**: Use web search or file grep with pattern and `docs/` path
- **List docs in a directory**: Use file glob patterns like `docs/skills/*.md`

### Step 3: Check for shared content
For skills that have both implementation and documentation:
- Skill source: `skills/my-skill/SKILL.md`
- Documentation: `docs/skills/my-skill.md`

## Common Patterns

### New Skill
1. Create skill in `skills/new-skill/`
2. Create documentation at `docs/skills/new-skill.md`
3. Update skill index page if applicable

### New API Function
1. Add function to `src/api/`
2. Create/update doc at `docs/api/function-name.md`
3. Update API index page

### New Configuration Option
1. Add option to config file in `src/config/`
2. Update corresponding config doc in `docs/config/`
3. Add examples and use cases

### Behavioral Change
1. Logic changed in any source file
2. Find all docs that describe this behavior
3. Update descriptions and examples to match new behavior
4. Add migration notes if breaking change

## Quick Search Commands

Use OpenClaw's built-in tools for efficient searching:

- **Find all docs mentioning a term**: Use `web_search` or file operations with pattern in `docs/`
- **List all skill docs**: Look for files in `docs/skills/`
- **Find docs by filename pattern**: Use file glob patterns
- **Read a doc's frontmatter**: Check the top of markdown files for metadata

## Validation Checklist

Before committing documentation changes:

- [ ] Frontmatter has `title` and `description`
- [ ] Code blocks are properly formatted with language specification
- [ ] Links point to valid paths
- [ ] Spelling and grammar are correct
- [ ] Examples are tested and working
- [ ] Documentation matches current code behavior

This mapping guide helps ensure that OpenClaw's documentation stays synchronized with code changes, making it easier for developers and users to understand the current state of the system.