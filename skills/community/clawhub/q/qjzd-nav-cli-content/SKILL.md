---
name: qjzd-nav-cli-content
version: 1.0.0
description: Use when managing QJZD Nav links, categories, and tags from the terminal, including list, create, update, delete operations.
references:
  - ../qjzd-nav-cli
  - ../qjzd-nav-cli-auth
metadata:
  openclaw:
    category: content-management
    requires:
      bins: ["qjzd-nav"]
    cliHelp: "qjzd-nav link --help && qjzd-nav category --help && qjzd-nav tag --help"
---

# QJZD Nav CLI Content

Use this skill for `qjzd-nav link`, `qjzd-nav category`, and `qjzd-nav tag`.

If auth may not be ready, check `qjzd-nav auth current` first or load `qjzd-nav-cli-auth`.

## Commands

```bash
qjzd-nav link --help
qjzd-nav category --help
qjzd-nav tag --help
```

## Links

List and filter links:

```bash
qjzd-nav link list
qjzd-nav link list --category-id <id>
qjzd-nav link list --tag-ids <ids>        # comma-separated
qjzd-nav link list --keyword <keyword>
qjzd-nav link list --page 1 --page-size 20
qjzd-nav link list --json
```

Create a link:

```bash
qjzd-nav link create \
  --title "Google" \
  --url "https://google.com" \
  --category-id <category-id> \
  --description "Search engine" \
  --icon "i-lucide-search" \
  --tags "tag-id-1,tag-id-2" \
  --order 0
```

Update a link:

```bash
qjzd-nav link update --id <link-id> --title "New Title"
qjzd-nav link update --id <link-id> --url "https://new-url.com"
qjzd-nav link update --id <link-id> --category-id <new-category-id>
```

Delete a link:

```bash
qjzd-nav link delete --id <link-id>
```

## Categories

List categories:

```bash
qjzd-nav category list
qjzd-nav category list --keyword <keyword>
qjzd-nav category list --page 1 --page-size 20
qjzd-nav category list --json
```

Create a category:

```bash
qjzd-nav category create \
  --name "Programming" \
  --description "Programming links" \
  --icon "i-lucide-code" \
  --order 0 \
  --parent-id <parent-id>   # optional, for subcategories
```

Update a category:

```bash
qjzd-nav category update --id <cat-id> --name "New Name"
qjzd-nav category update --id <cat-id> --icon "i-lucide-star"
```

Delete a category:

```bash
qjzd-nav category delete --id <cat-id>
qjzd-nav category delete --id <cat-id> --mode only --sub-action promote  # only delete category, move links to parent
```

Reorder categories:

```bash
qjzd-nav category reorder --items '[{"id":"xxx","order":1},{"id":"yyy","order":2}]'
```

## Tags

List tags:

```bash
qjzd-nav tag list
qjzd-nav tag list --keyword <keyword>
qjzd-nav tag list --page 1 --page-size 20
qjzd-nav tag list --json
```

Create a tag:

```bash
qjzd-nav tag create --name "JavaScript" --color "#F7DF1E"
```

Update a tag:

```bash
qjzd-nav tag update --id <tag-id> --name "TypeScript" --color "#3178C6"
```

Delete a tag:

```bash
qjzd-nav tag delete --id <tag-id>
```

## Rules

- Link `categoryId` is required for creating links.
- Tag IDs are comma-separated when multiple tags are needed.
- Category deletion supports `--mode only` to only delete the category (links move to parent/default).
- Use `--json` for automation and scripts.
- Use `--page` and `--page-size` for pagination.

## Common Workflow Example

```bash
# 1. List categories to get IDs
qjzd-nav category list --json

# 2. List tags to get IDs
qjzd-nav tag list --json

# 3. Create a link with category and tags
qjzd-nav link create \
  --title "GitHub" \
  --url "https://github.com" \
  --category-id <cat-id> \
  --tags "<tag-id-1>,<tag-id-2>"
```
