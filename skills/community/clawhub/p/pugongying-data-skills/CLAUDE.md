# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **蒲公英数据开发工程师Skill套件** (Pugongying Data Engineering Skills Suite), a collection of AI skills for data engineering workflows. It contains 7 specialized skill modules that can work independently or in combination through a skill connection system.

**Repository Type**: Skill package repository (markdown-based, no build system)
**Primary Language**: Chinese
**Package Manager**: SkillHub / ClawHub compatible

## Project Structure

```
pugongying-data-skills/
├── SKILL.md                      # Main skill definition (entry point)
├── README.md                     # Comprehensive documentation
├── skill-connections.yaml        # Inter-skill connection configuration
├── skill-hub.md                  # Skill hub workflow definitions
├── package.json                  # NPM metadata for SkillHub indexing
├── _meta.json                    # SkillHub publication metadata
├── requirement-analyst/          # Business requirement analysis
├── architecture-designer/        # Data architecture design
├── modeling-assistant/           # Data modeling (dimensional models)
├── sql-assistant/                # SQL development and optimization
├── etl-assistant/                # ETL pipeline development
├── dq-assistant/                 # Data quality management
└── test-engineer/                # Data testing and validation
```

Each module follows this structure:
```
{module-name}/
├── SKILL.md          # Module skill definition
├── references/       # Standards, best practices, guidelines
├── examples/         # Example scenarios and outputs
└── scripts/          # Initialization scripts
```

## Skill Module Reference

| Module | Entry Command | Core Purpose |
|--------|---------------|--------------|
| requirement-analyst | `/requirement-analyst` | Parse business requirements into technical specs |
| architecture-designer | `/architecture-designer` | Design data architecture and tech stack |
| modeling-assistant | `/modeling-assistant` | Dimensional modeling and dbt development |
| sql-assistant | `/sql-assistant` | SQL generation, review, and optimization |
| etl-assistant | `/etl-assistant` | ETL pipeline development |
| dq-assistant | `/dq-assistant` | Data quality rules and monitoring |
| test-engineer | `/test-engineer` | Data testing and validation |

## Key Architectural Concepts

### 1. Skill Connection System

The `skill-connections.yaml` file defines how modules exchange data. Each skill can output a standardized YAML package that serves as input to downstream skills.

**Package File Convention**:
- `requirement_package.yaml` - requirement-analyst output
- `architecture_package.yaml` - architecture-designer output
- `modeling_package.yaml` - modeling-assistant output
- `sql_package.yaml` - sql-assistant output
- `etl_package.yaml` - etl-assistant output
- `dq_package.yaml` - dq-assistant output
- `test_package.yaml` - test-engineer output

### 2. Standard Package Format

```yaml
version: "1.0"
metadata:
  project_name: string
  generated_by: string
  generated_at: timestamp
  upstream_package: string  # Reference to input package
content: object
downstream_specs: array
```

### 3. Workflow Patterns

Defined in `skill-connections.yaml` under `workflows:`:

- **end_to_end_warehouse**: 7-stage complete data warehouse construction
- **sql_to_etl**: Quick pipeline generation from SQL
- **quality_to_test**: Generate tests from quality rules
- **delivery_checklist**: Pre-delivery validation

## Working with This Repository

### Adding a New Skill Module

1. Create new directory: `mkdir {module-name}/`
2. Add `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: {module-id}
   description: |
     Description for skill discovery...
     Trigger words: keyword1, keyword2
   ---
   ```
3. Add subdirectories: `references/`, `examples/`, `scripts/`
4. Update `skill-connections.yaml` to define connections
5. Update `package.json` files array

### Modifying Skill Connections

Edit `skill-connections.yaml`:
- Add new connections under `connections:`
- Define workflows under `workflows:`
- Update shortcuts for quick commands

### Skill Development Guidelines

Each SKILL.md should include:
1. Frontmatter with `name` and `description`
2. Architecture diagram or overview
3. Usage examples with command syntax
4. Reference file navigation table
5. Input/output specifications
6. Fault troubleshooting section

## Reference Files

Key specification documents by module:

- `requirement-analyst/references/requirement-standards.md` - Requirement classification and standards
- `sql-assistant/references/sql-standards.md` - SQL naming conventions and anti-patterns
- `modeling-assistant/references/` - Dimensional modeling patterns, SCD strategies
- `etl-assistant/references/` - Pipeline patterns and best practices
- `dq-assistant/references/` - Data quality rule categories
- `test-engineer/references/` - Data testing methodologies

## Important Notes

- This is a **skill repository**, not a code repository - changes are primarily to markdown files
- No build, test, or lint commands exist - validation is manual
- Skills are invoked via slash commands (`/skill-name`)
- Module interactions are defined declaratively in YAML
- All skill documentation is in Chinese
- Use `skill-connections.yaml` as the source of truth for skill relationships
