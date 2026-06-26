---
name: udon
description: >
  Search and browse 100 curated Japanese udon noodle recipes from Cookpad.
  Use when the user asks about udon recipes, wants udon dish ideas, searches for
  udon by ingredient (e.g. curry, miso, egg, kimchi, salmon), or mentions udon cooking.
  Covers grilled udon (yaki-udon), cold udon, nabeyaki, curry udon, miso udon, and more.
---

# Udon Recipe Search

Search 100 Japanese udon recipes by keyword, ingredient, category, or recipe number.

## Quick Start

Run the search script:

```bash
python <skill_dir>/scripts/search_udon.py [keyword]
```

### Examples
- List all 100 recipes: `python search_udon.py`
- Search by ingredient: `python search_udon.py curry`
- Search by style: `python search_udon.py cold`
- Search by protein: `python search_udon.py salmon`
- Get a specific recipe: `python search_udon.py 42`

Common categories: `grilled`, `cold`, `simmered`, `curry`, `miso`, `egg`, `meat`, `seafood`, `natto`, `kimchi`, `vegetable`, `quick`.

## Workflow

1. Run `search_udon.py` with the user's keyword(s).
2. If no matches, suggest browsing all recipes or trying a broader keyword.
3. If multiple matches, show the top results and offer to narrow down.
4. If user picks a number, show that specific recipe with ingredients and link.

## Resources

### references/recipes.md
Full recipe list with ingredients and Cookpad links. Loaded only when browsing all recipes or when deep context is needed.

### scripts/search_udon.py
Search script — parse recipes, filter by keyword, format output. No dependencies beyond Python 3 stdlib.
