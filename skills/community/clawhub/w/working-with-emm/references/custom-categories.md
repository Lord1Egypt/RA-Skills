# Custom Memory Categories

Guidance on creating and managing custom memory categories beyond the defaults.

## Default Categories

Emm comes with 9 predefined categories: health, travel, work, food, shopping, entertainment, news, notes, personal. These can be deleted or added to by the user or by an AI agent, and are available to all the user's AI agents automatically.

## Creating Custom Categories

Use the `memory_create_type()` tool to create a new category:

```
memory_create_type(
  type_name="recipes",
  display_name="My Recipes",
  description="Cooking recipes and meal ideas I want to remember",
  emoji="chef_hat",
  keywords=["recipe", "cooking", "meal", "dish"]
)
```

Pass the **short form** (`recipes`) — the `memory_` prefix is reserved for IDs and storage. Passing the storage form (`memory_recipes`) returns a -32602 error pointing at the short form.

**Three name-shaped fields on the `memory_types()` response, one rule.** Each category row carries `type_name` (the storage form, e.g. `memory_recipes`), `name` (the display label, e.g. `My Recipes`), and `id_prefix` (the short form, e.g. `recipes`). **Always use `id_prefix` when you call a tool** — `memory_save`, `memory_search` with `in <type>: …`, `memory_create_type`, `memory_delete_type`. `type_name` is for inspecting storage; `name` is for surfacing the category to the user in prose. Don't pass `type_name` to anything that expects a category argument.

Category descriptions should be non-overlapping to the extent possible, so that auto-categorization works well.

**Note:** The default categories already have detailed disambiguation rules in their descriptions. For example, the News category specifies "WHAT you read, follow, subscribe to — NOT your job duties" and the Travel category specifies "Business trips are TRAVEL — NOT entertainment events." Use `memory_types()` to see these descriptions — they're worth reading to understand how auto-categorization decides where to put new memories. When creating custom categories, write similarly clear descriptions with explicit boundaries.

## Auto-Creation via Save

When you save a memory to a non-existent category, it will be automatically created:

```
memory_save(memory_type="projects", content="Project X deadline is March 15th")
```

This auto-creates the `projects` category (stored as `memory_projects`) if it doesn't exist. Pass the short form — the `memory_` prefix is reserved for IDs and is rejected on this parameter.

## Privacy Rules

- Custom categories are **private to you** (the AI agent that created them) by default
- Other AI agents connected to the user's account won't have access unless the user explicitly grants it
- Default categories are available to all the user's AI agents automatically

## Deleting Custom Categories

Use `memory_delete_type()` to remove a custom category that is no longer needed:

```
memory_delete_type(type_name="recipes")
```

Same short-form rule as `memory_create_type` — pass `recipes`, not `memory_recipes`. The storage form on this parameter returns a -32602 error.

**Requirements:**
- The category must be **empty** — list items with `memory_search(query="in recipes: *")` (or via `memory_get(id="type:memory_recipes")`), then `memory_delete(ids=["memory_recipes:1", ...])` before deleting the type
- Works for both custom and predefined categories
- Write permission is required

## Managing Access

To grant other AI agents access to a custom category:

1. Go to Settings in the web interface
2. Select Trust & Connections
3. Select the AI agent
4. Find the custom category in the access list
5. Toggle access on/off
