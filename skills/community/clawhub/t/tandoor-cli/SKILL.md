---
name: tandoor-recipe-cli
description: Manage recipes, meal plans, and shopping lists on a Tandoor Recipe Manager instance via CLI.
version: 1.5.0
compatibility: ">=18"
license: MIT
metadata:
  author: dcenatiempo
  repository: https://github.com/dcenatiempo/tandoor-cli
---

## Tandoor CLI Skill

This skill provides AI agents with the ability to interact with a Tandoor Recipe Manager instance using the `tandoor-cli` command-line tool.

### Prerequisites

The `tandoor-cli` tool must be installed and configured.

**Version Compatibility:** This skill documentation corresponds to the version specified in the metadata above. Before using this skill:
1. Verify your installed CLI version: `tandoor -V`
2. Ensure the installed version matches the skill version to avoid unexpected behavior or missing commands
3. If versions don't match, reinstall the CLI tool following the setup instructions in `references/SETUP.md`

If `tandoor -V` produces no valid version, see the setup instructions in `references/SETUP.md`.

### Security & Permission Model

**⚠️ IMPORTANT: This skill provides mutation authority over your Tandoor instance.**

- **Read operations** (list, search, get, random) are safe and require no confirmation
- **Write operations** (add, update, import) modify data but are typically reversible
- **Destructive operations** (delete, clear, household management) require explicit user approval before execution
- **Bulk operations** (shopping check --all, clear) affect multiple items and require confirmation
- **Administrative operations** (household management, user assignment, invite creation) require privileged credentials and explicit approval

**Token Security:**
- Use the **least-privileged token** possible for your use case
- Prefer read-only tokens if you only need to query recipes
- Avoid using space-owner or admin tokens unless household management is required
- Consider short-lived tokens (days/weeks) instead of long-lived tokens (years)
- Store tokens securely and rotate them regularly
- Revoke tokens immediately if compromised or no longer needed

**Supply Chain:**
- This skill uses the `tandoor-cli` npm package
- Verify the package source before first use: https://www.npmjs.com/package/tandoor-cli
- Review the package repository: https://github.com/dcenatiempo/tandoor-cli
- **Recommended:** Pin to the specific version matching this skill (see version in metadata above) to avoid unexpected updates
- Install pinned version: `npm install -g tandoor-cli@<version>` (replace `<version>` with the skill version)

### Invocation

```bash
tandoor <command> [options]
```

### Output formats and deprecated flags

Commands that print data accept **`--format text|json|api`** (default: `text`):

| `--format` | Use for |
|------------|---------|
| `text` | Human-readable output (default) |
| `json` | Slim JSON where supported (recipe add/update shape + `id` on `get`, `list`, `search`, `random`) |
| `api` | Raw Tandoor API JSON |

**Deprecated (output):** `--json` with no file path — alias for **`--format api`**; stderr warning. Do not use in new agent workflows.

**Recommended (input):** `tandoor add --file recipe.json`, `tandoor update <id> --file patch.json`

**Deprecated (input):** `tandoor add --json <file>`, `tandoor update <id> --json <file>` — still work with stderr warning.

| Deprecated | Use instead |
|------------|-------------|
| `tandoor get 1 --json` | `--format api` (full) or `--format json` (slim, for edit round-trips) |
| `tandoor list --json` | `--format api` |
| `tandoor add --json recipe.json` | `--file recipe.json` |
| `tandoor update 42 --json patch.json` | `--file patch.json` |

### Commands

#### Read Operations (Safe)

**Recipes:**
| Command | Description |
|---|---|
| `list [--limit N] [--page N] [--all]` | List recipes (default 20 per page, max 100) |
| `search <query>` | Search recipes by keyword |
| `get <id>` | Get full recipe details |
| `random` | Get a random recipe |

**Meal Plans:**
| Command | Description |
|---|---|
| `mealplan list [--startdate DATE] [--enddate DATE]` | List meal plan entries (optionally filtered by date range) |

**Shopping List:**
| Command | Description |
|---|---|
| `shopping list` | List shopping list entries |

**Food Ingredients:**
| Command | Description |
|---|---|
| `food list [--limit N] [--page N] [--all] [--search TERM] [--ignored] [--onhand]` | List food ingredients |

**Grocery Categories:**
| Command | Description |
|---|---|
| `category list` | List all supermarket categories (sorted A-Z) |
| `category uncategorised [--search TERM]` | List food items with no category assigned |

**Cook Logs:**
| Command | Description |
|---|---|
| `cooklog list [--recipe ID] [--limit N] [--page N] [--all] [--startdate YYYY-MM-DD] [--enddate YYYY-MM-DD] [--min-rating 1-5] [--max-rating 1-5]` | List cook log entries (sorted by most recent first) |
| `cooklog ingredient <name> [--limit N] [--startdate YYYY-MM-DD] [--enddate YYYY-MM-DD] [--min-rating 1-5] [--max-rating 1-5]` | Find cook logs by ingredient name (e.g., "when did we last have eggs?") |

**Households & Users:**
| Command | Description |
|---|---|
| `household list` | List all households |
| `household get <id>` | Get household details by ID |
| `household users list` | List all users in the space |
| `household users memberships` | List user-space memberships |
| `household invite list` | List all invite links |

#### Write Operations (Require Confirmation)

| Command | Description | Approval Required |
|---|---|---|
| `add [--file file] [--interactive]` | Create a recipe (`--json <file>` deprecated) | ✓ Before execution |
| `update <id> --file file` | Patch an existing recipe (`--json <file>` deprecated) | ✓ Before execution |
| `import <url> [--dry-run]` | Import a recipe from a URL | ✓ Before execution |
| `image <recipeId> <imagePath>` | Upload an image to a recipe | ✓ Before execution |
| `mealplan add --recipe ID --date YYYY-MM-DD --meal-type N` | Add a meal plan entry | ✓ Before execution |
| `shopping add --food NAME --amount N --unit UNIT` | Add a shopping list item | ✓ Before execution |
| `shopping check <id>` | Mark a shopping item as checked | ✓ Before execution |
| `food edit <id\|name> --ignore-shopping <true\|false>` | Edit a food's ignore_shopping flag | ✓ Before execution |
| `food ignore <id\|name> [--unset]` | Set or clear ignore_shopping by ID or name | ✓ Before execution |
| `food onhand <id\|name> [--unset]` | Set or clear the on-hand flag by ID or name | ✓ Before execution |
| `category set <food-id\|name> --category <name\|id>` | Assign a grocery category to a food item | ✓ Before execution |
| `category set <food-id\|name> --unset` | Remove the category from a food item | ✓ Before execution |
| `cooklog add --recipe ID --servings N [--rating 1-5] [--comment TEXT] [--date ISO8601]` | Add a cook log entry | ✓ Before execution |
| `cooklog update <id> [--recipe ID] [--servings N] [--rating 1-5] [--comment TEXT] [--date ISO8601]` | Update a cook log entry | ✓ Before execution |

#### Destructive Operations (Require Explicit Confirmation)

| Command | Description | Approval Required |
|---|---|---|
| `delete <id> [--force]` | Delete a recipe | ✓✓ Explicit confirmation required |
| `mealplan delete <id>` | Delete a meal plan entry | ✓✓ Explicit confirmation required |
| `shopping clear [--force]` | Clear all checked items | ✓✓ Explicit confirmation (bulk operation) |
| `shopping check --all` | Mark all items as checked | ✓✓ Explicit confirmation (bulk operation) |
| `cooklog delete <id>` | Delete a cook log entry | ✓✓ Explicit confirmation required |

#### Administrative Operations (Require Privileged Token + Explicit Confirmation)

**Important:** Tandoor uses **households** to organize users and recipes. Users are added to households via **invite links** — you cannot create users directly via the API.

> **Permission Requirements:** Household management commands require special permissions in Tandoor. Most operations need admin/staff privileges. The `household invite create` command specifically requires **space owner** authentication — even superusers or staff members will receive a 403 Permission Denied error if they're not the space owner. If you encounter permission errors, you must use the space owner's API token or contact your Tandoor administrator.

| Command | Description | Approval Required |
|---|---|---|
| `household add <name>` | Create a new household | ✓✓ Admin token + explicit confirmation |
| `household edit <id> --name <name>` | Rename a household | ✓✓ Admin token + explicit confirmation |
| `household delete <id> [--force]` | Delete a household | ✓✓ Admin token + explicit confirmation |
| `household users assign <user-space-id> <household-id>` | Assign user to household | ✓✓ Admin token + explicit confirmation |
| `household invite create <household-id> [--email EMAIL] [--expires DATE] [--group-id ID]` | Create invite link | ✓✓ Space-owner token + explicit confirmation |
| `household invite delete <id> [--force]` | Delete invite link | ✓✓ Admin token + explicit confirmation |

Read commands accept **`--format json`** (slim, where supported) or **`--format api`** (raw). Deprecated: `--json` (same as `--format api`).

### Agent Behavior Rules

**Before executing any command, the agent MUST:**

1. **For read operations:** Proceed without confirmation
2. **For write operations:** Describe the action and wait for user approval
3. **For destructive operations:** 
   - Clearly explain what will be deleted/modified
   - Warn that the action cannot be easily reversed
   - Wait for explicit user confirmation (e.g., "yes, delete recipe 42")
4. **For bulk operations:**
   - State how many items will be affected
   - Wait for explicit confirmation
5. **For administrative operations:**
   - Verify the user has provided an admin/space-owner token
   - Explain the scope of the change (e.g., "this will move user X to household Y")
   - Wait for explicit confirmation

**The agent MUST NOT:**
- Execute delete, force, bulk, household, invite, or user-assignment commands without explicit user approval
- Assume the user wants destructive actions even if implied by context
- Use `--force` flags without explicit user instruction
- Log or display the `TANDOOR_API_TOKEN` value in any output

### Configuration

The CLI supports three configuration methods (in precedence order):

1. **Environment variables** — `TANDOOR_URL` and `TANDOOR_API_TOKEN` in the current shell
2. **Config file** — `~/.config/tandoor-cli/config.json` (created by `tandoor configure`)
3. **`.env` file** — a `.env` file in the current working directory

Run `tandoor configure` once to save credentials interactively.

### Examples

**Configure credentials:**
```bash
tandoor configure
```

**Read example — list recipes as JSON:**
```bash
tandoor list --limit 5 --format api
```

**Read example — get recipe for editing:**
```bash
tandoor get 42 --format json
```

**Write example — create a recipe from a JSON file:**
```bash
# Agent should first ask: "I will create a new recipe from recipe.json. Proceed?"
# Only after user confirms:
tandoor add --file recipe.json
```

### Recipe JSON Schema

When creating recipes with `tandoor add --file <file>` (or deprecated `--json <file>`), the JSON file must conform to the following structure:

**TypeScript Definition:**
```typescript
interface RecipeCreatePayload {
  name: string;                    // Required: Recipe name
  description?: string;            // Optional: Recipe description
  servings?: number;               // Optional: Number of servings
  working_time?: number;           // Optional: Active cooking time in minutes
  waiting_time?: number;           // Optional: Passive time (baking, marinating) in minutes
  steps: StepCreatePayload[];      // Required: At least one step
}

interface StepCreatePayload {
  instruction: string;             // Required: Step instructions
  order: number;                   // Required: Step order (1, 2, 3, ...)
  ingredients: IngredientCreatePayload[];  // Required: Can be empty array
}

interface IngredientCreatePayload {
  food: { name: string };          // Required: Ingredient name
  unit: { name: string } | null;   // Optional: Unit of measurement (null if not applicable)
  amount: number;                  // Required: Quantity
  note?: string;                   // Optional: Additional notes (e.g., "finely chopped")
  order?: number | null;           // Optional: Order within the step
}
```

**Example Recipe JSON:**
```json
{
  "name": "Scrambled Eggs",
  "description": "Quick and easy scrambled eggs",
  "servings": 2,
  "working_time": 5,
  "steps": [
    {
      "instruction": "Crack eggs into a bowl, add milk and salt. Whisk until well combined.",
      "order": 1,
      "ingredients": [
        {
          "food": { "name": "eggs" },
          "unit": { "name": "whole" },
          "amount": 4
        },
        {
          "food": { "name": "milk" },
          "unit": { "name": "tbsp" },
          "amount": 2
        },
        {
          "food": { "name": "salt" },
          "unit": null,
          "amount": 1,
          "note": "to taste"
        }
      ]
    },
    {
      "instruction": "Heat butter in a pan over medium heat. Pour in egg mixture and stir gently until cooked to desired consistency.",
      "order": 2,
      "ingredients": [
        {
          "food": { "name": "butter" },
          "unit": { "name": "tbsp" },
          "amount": 1
        }
      ]
    }
  ]
}
```

**Key Points for Agents:**
- `name` and `steps` are required fields
- Each step must have `instruction`, `order`, and `ingredients` (can be empty array)
- Each ingredient must have `food.name` and `amount`
- Use `null` for `unit` when no unit applies (e.g., "to taste", "pinch")
- Common units: `g`, `kg`, `ml`, `l`, `cup`, `tbsp`, `tsp`, `whole`, `pinch`
- Times are in minutes
- Steps should be ordered sequentially (1, 2, 3, ...)

**Destructive example — delete a recipe:**
```bash
# Agent should first ask: "This will permanently delete recipe 42. This cannot be undone. Confirm deletion?"
# Only after explicit user confirmation:
tandoor delete 42 --force
```

**Image example — upload an image to a recipe:**
```bash
# Agent should first ask: "I will upload my-recipe-photo.jpg to recipe 42. Proceed?"
# Only after user confirms:
tandoor image 42 ./my-recipe-photo.jpg
```

**Household example — create a household and generate an invite link:**
```bash
# Agent should first ask: "I will create a new household named 'My Family'. This requires admin privileges. Proceed?"
# Only after user confirms:
tandoor household add "My Family"

# Agent should first ask: "I will create an invite link for household 1. This requires space-owner token. Proceed?"
# Only after user confirms:
tandoor household invite create 1 --email user@example.com --expires 2026-12-31
```

**Shopping list example — add items and check them off:**
```bash
# Agent should first ask: "I will add flour (500g) to the shopping list. Proceed?"
# Only after user confirms:
tandoor shopping add --food flour --amount 500 --unit g

# Agent should first ask: "This will mark ALL shopping items as checked. Confirm?"
# Only after explicit confirmation:
tandoor shopping check --all
```

**Grocery category example — organise foods for a better shopping list:**
```bash
# Read example — see what categories exist:
tandoor category list

# Read example — find foods with no category yet:
tandoor category uncategorised
tandoor category uncategorised --search pasta

# Agent should first ask: "I will assign 'milk' to the Dairy category. Proceed?"
# Only after user confirms:
tandoor category set milk --category Dairy
tandoor category set "olive oil" --category Oils
tandoor category set 42 --category "Canned Goods"   # by food ID

# Agent should first ask: "I will remove the category from 'milk'. Proceed?"
# Only after user confirms:
tandoor category set milk --unset
```

**Cook log example — track when you cook a recipe:**
```bash
# Agent should first ask: "I will add a cook log entry for recipe 42 (4 servings, rating 5). Proceed?"
# Only after user confirms:
tandoor cooklog add --recipe 42 --servings 4 --rating 5
tandoor cooklog add --recipe 42 --servings 4 --rating 5 --comment "Kids loved it"

# Read example — list cook logs for a specific recipe:
tandoor cooklog list --recipe 42 --format api

# Read example — find when you last had eggs:
tandoor cooklog ingredient eggs

# Read example — count how many times you had chicken last month:
tandoor cooklog ingredient chicken --startdate 2026-04-01 --enddate 2026-04-30

# Read example — find highly-rated egg recipes (4-5 stars):
tandoor cooklog ingredient eggs --min-rating 4

# Read example — find poorly-rated recipes from last month (1-2 stars):
tandoor cooklog list --startdate 2026-04-01 --enddate 2026-04-30 --max-rating 2

# Agent should first ask: "I will update cook log 2 with a new comment. Proceed?"
# Only after user confirms:
tandoor cooklog update 2 --comment "Next time add more garlic"

# Agent should first ask: "This will delete cook log entry 2. Confirm?"
# Only after explicit confirmation:
tandoor cooklog delete 2
```

### Installation & Setup

**Before first use:**
1. Verify the npm package: https://www.npmjs.com/package/tandoor-cli
2. Review the source code: https://github.com/dcenatiempo/tandoor-cli
3. **Recommended:** Install the pinned version matching this skill: `npm install -g tandoor-cli@<version>` (see version in metadata above)
4. Generate a token with minimal required permissions (see SECURITY.md)
5. Consider using a test Tandoor instance first

### Reference

- See `references/SETUP.md` for detailed setup documentation including authentication configuration
- See `SECURITY.md` for comprehensive security guidelines and token management best practices
