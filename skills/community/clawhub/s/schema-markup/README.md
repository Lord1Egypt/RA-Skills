# Schema Markup

Implement schema.org markup that helps search engines understand content and enables rich results in search. Add, fix, or optimize structured data using JSON-LD format.

## What's Inside

- Core principles (accuracy first, use JSON-LD, follow Google's guidelines, validate everything)
- Common schema types: Organization, WebSite, Article, Product, SoftwareApplication, FAQPage, HowTo, BreadcrumbList, LocalBusiness, Event
- Quick reference for required and recommended properties per type
- Multiple schema combination using `@graph` and `@id` references
- Validation tools and common errors with fixes
- Implementation patterns for static sites, React/Next.js, and CMS/WordPress
- Testing checklist
- Implementation workflow (identify, start with homepage, add per-page, validate, monitor)
- Reference file with complete JSON-LD examples

## When to Use

- Adding structured data to new or existing pages
- Fixing schema validation errors
- Optimizing for specific rich results (FAQ, product, article)
- Implementing JSON-LD in React/Next.js applications
- Auditing existing schema markup

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/writing/schema-markup
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install schema-markup
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/writing/schema-markup .cursor/skills/schema-markup
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/writing/schema-markup ~/.cursor/skills/schema-markup
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/writing/schema-markup .claude/skills/schema-markup
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/writing/schema-markup ~/.claude/skills/schema-markup
```

---

Part of the [Writing](..) skill category.
