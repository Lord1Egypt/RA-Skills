---
title: Workflow templates
description: Patterns, structures, and best practices for working with Knock workflows and templates via the CLI
tags:
  - knock
  - cli
  - workflows
  - templates
  - email
  - liquid
  - gotchas
  - best-practices
category: knock-cli
last_updated: 2026-02-16
---

# Workflow templates

## Critical rules

### Always read before writing

Before modifying any workflow or template file, always read the existing content first. This prevents:

- Losing existing data or configuration
- Breaking the current structure
- Overwriting uncommitted changes

```bash
# Read the current state before making changes
cat knock/workflows/my-workflow/workflow.json
```

### Always push after modifying

**Local file changes are not synced to Knock until you push.** Editing files in the knock directory does nothing in Knock until you run the appropriate push command.

```bash
# After modifying a workflow
knock workflow push <workflow-key>

# After modifying other resources
knock email-layout push <layout-key>
knock partial push <partial-key>
knock push --all   # Push everything
```

If you don't push, your changes exist only on disk—Knock will continue using the previous version.

### Channel keys are project-specific

Channel keys (e.g., `knock-email`, `in-app`) are configured per-project. Don't assume keys from schema examples or other projects—they may not exist in your project.

Before creating workflows that use channels:

1. Run `knock channel list` to see available channel keys
2. Use the exact `key` values from the output for `channel_key` in workflow steps

### Workflows do not support guide steps

**Never add guide or message-type steps to a workflow.** Guides and workflows are completely separate systems in Knock:

- **Workflows** send notifications (email, SMS, push, in-app feed, webhook) and use function steps (delay, batch, branch, fetch).
- **Guides** power lifecycle UI (banners, modals, cards) and are configured separately via `knock guide` commands.

There is no `guide` or `message-type` step type in `workflow.json`. If a user asks for in-app lifecycle messaging (announcements, upgrade prompts, onboarding), use guides (`rules/guides-and-message-types.md`), not workflows. If they want in-app notifications (e.g., "Someone commented on your post"), use a workflow with an `in_app_feed` step.

## Email template modes

Knock emails support two mutually exclusive modes: visual blocks and HTML.

**Always use visual blocks for new emails.** When creating a new email step, default to visual blocks mode. Only use HTML mode if the user explicitly requests it.

When modifying an existing email, preserve the current mode unless asked to change it.

### Visual blocks mode (default for new emails)

A structured array of blocks for the email body. Use this for all new emails.

**Structure:**

```
workflows/my-workflow/
└── email-step/
    ├── visual_blocks.json         # Block structure
    └── visual_blocks/
        ├── 1.content.md           # First block content (1-indexed)
        ├── 2.content.md           # Second block content
        └── ...
```

**visual_blocks.json example:**

```json
[
  {
    "type": "markdown",
    "content@": "visual_blocks/1.content.md"
  },
  {
    "type": "button_set",
    "buttons": [
      {
        "label": "View Order",
        "action": "{{ data.order_url }}",
        "variant": "solid"
      }
    ]
  },
  {
    "type": "divider"
  },
  {
    "type": "markdown",
    "content@": "visual_blocks/2.content.md"
  }
]
```

**Block types:**

| Type | Description |
|------|-------------|
| `markdown` | Markdown content block |
| `button_set` | One or more buttons (requires `variant` per button) |
| `divider` | Horizontal divider |
| `image` | Image block |
| `html` | Raw HTML block |
| `row` | Multi-column row |

### Button_set: variant requirement

Each button in a `button_set` block must include a `variant` field. Valid values are `solid` and `outline`.

### HTML mode

Raw HTML template when full control is needed. **Do not use HTML mode unless the user explicitly requests it.** Visual blocks should be the default for all new emails.

**Structure:**

```
workflows/my-workflow/
└── email-step/
    └── html_body.html             # Raw HTML template
```

**In workflow.json:**

```json
{
  "ref": "email-step",
  "type": "email",
  "template": {
    "subject": "Your order is confirmed",
    "html_body@": "email-step/html_body.html"
  }
}
```

### Preserving template mode

When modifying an existing email:

1. Check which mode is currently used (visual blocks vs HTML)
2. Preserve that mode in your changes
3. Don't convert between modes unless explicitly requested

## File path reference rules

### The @ suffix convention

Knock uses `@` suffix to indicate file path references:

```json
{
  "content@": "visual_blocks/1.content.md",
  "html_body@": "body.html",
  "visual_blocks@": "email-step/visual_blocks.json"
}
```

When the field name ends with `@`, the value is a file path, and the actual content lives in the referenced file.

### Path resolution

**Critical rule:** Paths are relative to the file containing the reference.

**Example directory:**

```
workflows/order-confirmation/
├── workflow.json
└── email-step/
    ├── visual_blocks.json
    └── visual_blocks/
        └── 1.content.md
```

**In workflow.json (at workflow root):**

```json
{
  "visual_blocks@": "email-step/visual_blocks.json"
}
```

**In email-step/visual_blocks.json (inside step directory):**

```json
{
  "content@": "visual_blocks/1.content.md"
}
```

### Common mistake: Doubling the step directory

When editing `{step_ref}/visual_blocks.json`, paths are already relative to that step directory.

**Wrong:**

```json
{
  "content@": "email-step/visual_blocks/1.content.md"
}
```

**Correct:**

```json
{
  "content@": "visual_blocks/1.content.md"
}
```

## Liquid templating

Knock templates use Liquid syntax for dynamic content. Understanding the correct namespaces is critical.

### Variable namespaces

| Namespace | Description | Use for |
|-----------|-------------|---------|
| `data` | Trigger payload | Dynamic data passed when workflow is triggered |
| `vars` | Environment variables | Static values configured at environment level |
| `recipient` | Notification recipient | Recipient properties like name, email |
| `actor` | Triggering user | User who triggered the action |
| `tenant` | Tenant information | Multi-tenancy data |

### Common mistake: Using vars for trigger data

**Wrong:**

```liquid
Your order {{ vars.order_id }} has shipped.
```

**Correct:**

```liquid
Your order {{ data.order_id }} has shipped.
```

**Rule:** If the value comes from the API trigger payload, use `data.`, not `vars.`.

- `data.order_id` - Value passed when triggering the workflow
- `vars.app_name` - Static environment variable like "Acme Corp"

### Liquid syntax examples

**Variables:**

```liquid
{{ recipient.name }}
{{ data.order_id }}
{{ vars.support_email }}
```

**Filters:**

```liquid
{{ recipient.name | default: "there" }}
{{ data.amount | currency }}
{{ data.date | date: "%B %d, %Y" }}
```

**Conditionals:**

```liquid
{% if data.items.size > 0 %}
  You have {{ data.items.size }} items in your order.
{% else %}
  Your cart is empty.
{% endif %}
```

**Loops:**

```liquid
{% for item in data.items %}
  - {{ item.name }}: {{ item.price | currency }}
{% endfor %}
```

### Default values

Always provide defaults for optional values:

```liquid
Hi {{ recipient.name | default: "there" }},
```

## Step types

### Channel steps (have template content)

Channel steps use `"type": "channel"` with a `channel_key` and `channel_type`. They send notifications and can have extracted template content in step directories. The `channel_type` values are:

| `channel_type` | Description |
|------|-------------|
| `email` | Email notifications |
| `sms` | SMS text messages |
| `push` | Push notifications |
| `chat` | Chat app messages (Slack, Teams) |
| `in_app_feed` | In-app notification feed |
| `webhook` | Webhook calls |

### Function steps (no template directories)

These step types control workflow logic and never have step directories. Function steps use `settings` (not `template`) for their configuration.

| Type | Description |
|------|-------------|
| `delay` | Wait for a specified time |
| `batch` | Batch multiple triggers |
| `throttle` | Limit notification frequency |
| `branch` | Conditional branching |
| `http_fetch` | Fetch external data via HTTP |
| `trigger_workflow` | Trigger another workflow |
| `update_user` | Update recipient user properties |
| `update_object` | Update an object |
| `update_tenant` | Update tenant properties |
| `update_data` | Update workflow run data |
| `random_cohort` | Randomly assign recipients to cohorts |
| `ai_agent` | AI agent step |

**Important:** The HTTP fetch step type is `http_fetch`, not `fetch`. The API will reject `fetch` as an invalid type.

## Delay steps

Delay steps pause the workflow for a specified duration before continuing to the next step. Use them to space out notifications, wait for user action windows, or time follow-up messages.

### Delay step configuration

```json
{
  "ref": "delay_1",
  "name": "Wait 5 minutes",
  "type": "delay",
  "settings": {
    "delay_for": {
      "unit": "minutes",
      "value": 5
    }
  }
}
```

| Setting | Description |
|---------|-------------|
| `delay_for` | Object with `unit` and `value` specifying how long to wait |
| `delay_until_field_path` | Path to a recipient or data field containing a datetime to wait until (alternative to `delay_for`) |

Valid `unit` values for `delay_for`: `seconds`, `minutes`, `hours`, `days`, `weeks`.

### delay_until example

To delay until a datetime stored on the recipient or in the trigger payload:

```json
{
  "ref": "delay_until_appointment",
  "type": "delay",
  "settings": {
    "delay_until_field_path": "data.appointment_at"
  }
}
```

### Common mistake: Using a duration string

The `settings` object requires a `delay_for` key with a nested `unit`/`value` object. A flat `duration` string is **not** a valid format and will be rejected by the API.

**Wrong:**

```json
{
  "settings": {
    "duration": "5 minutes"
  }
}
```

**Correct:**

```json
{
  "settings": {
    "delay_for": {
      "unit": "minutes",
      "value": 5
    }
  }
}
```

## Batch steps

Batch steps collect multiple triggers over a time window before continuing. Use them for commenting, likes, or any high-volume activity where you want to send one notification instead of many.

### Batch step configuration

```json
{
  "ref": "batch_comments",
  "type": "batch",
  "name": "Batch comments",
  "settings": {
    "batch_key": "data.content_id",
    "batch_window": {
      "unit": "minutes",
      "value": 5
    },
    "batch_order": "asc"
  }
}
```

| Setting | Description |
|---------|-------------|
| `batch_key` | Data path to group batches (e.g. `data.content_id`). Batches are per-recipient; the key further segments by value. Omit to batch all triggers for a recipient together. |
| `batch_window` | Duration object with `unit` (seconds, minutes, hours, days) and `value` (number) |
| `batch_order` | `"asc"` (first 10 items) or `"desc"` (last 10 items) for which activities appear in templates. Default: `"asc"` |

### Batch variables in templates

After a batch step, these variables are available in subsequent channel step templates:

| Variable | Description |
|----------|-------------|
| `total_activities` | Number of items in the batch |
| `total_actors` | Number of unique actors who triggered the batch |
| `activities` | Array of batched activities (up to 10 by default). Each has `data` and `actor`. |
| `actors` | Array of unique actors (up to 10 by default) |

These are in the workflow run scope—use them directly in Liquid, not under `data.` or `run.`.

### Single vs plural copy

Use `total_activities` and `total_actors` to vary copy for one vs many:

```liquid
{% if total_activities > 1 %}
  **{{ total_actors }} people** left {{ total_activities }} comments on {{ data.content_title | default: 'your content' }}
{% else %}
  **{{ actors[0].name | default: 'Someone' }}** left a comment on {{ data.content_title | default: 'your content' }}
{% endif %}
```

### Accessing per-activity data

Each item in `activities` has its own `data` and `actor`. Use this for per-trigger content:

```liquid
{% for activity in activities %}
  {{ activity.actor.name }}: {{ activity.data.comment_text }}
{% endfor %}
```

### Data after batching

When a batch step runs, `data` is merged from all triggers (last value wins for shared keys). For per-trigger data, reference `activities` instead of `data`. The merged `data` is useful for shared context (e.g. `data.content_url`) that is the same across the batch.

### Using actors for single-activity batches

When `total_activities` is 1, use `actors[0]` with a default:

```liquid
{{ actors[0].name | default: "Someone" }}
```

### Batch variables in conditions

Use `run.total_activities` in branch step conditions to branch on batch size:

```json
{
  "variable": "run.total_activities",
  "operator": "greater_than",
  "argument": 1
}
```

## Throttle steps

Throttle steps limit how often a workflow run proceeds for a given recipient within a time window. When a recipient has already passed a throttle step `throttle_limit` times within the `throttle_window`, subsequent runs are stopped at that step. Use throttle steps at the beginning of workflows to prevent over-notification.

### Throttle step configuration

```json
{
  "name": "Throttle 1 per 24 hours",
  "ref": "throttle_1",
  "type": "throttle",
  "settings": {
    "throttle_limit": 1,
    "throttle_window": {
      "unit": "hours",
      "value": 24
    }
  }
}
```

| Setting | Description |
|---------|-------------|
| `throttle_limit` | Maximum number of times a recipient can pass this step within the window. Almost always `1`. |
| `throttle_window` | Duration object with `unit` and `value` specifying the rolling window length. |
| `throttle_key` | Optional. A data path (e.g. `"object_key"`) to segment the throttle beyond per-recipient. Useful when throttling per-recipient-per-object rather than globally per recipient. |

Valid `unit` values for `throttle_window`: `seconds`, `minutes`, `hours`, `days`, `weeks`.

### Throttle key: per-object throttling

By default, a throttle step is scoped per recipient. Add `throttle_key` to further segment by a data value—for example, to allow one notification per recipient per content item rather than one notification per recipient globally:

```json
{
  "ref": "throttle_1",
  "type": "throttle",
  "settings": {
    "throttle_key": "data.content_id",
    "throttle_limit": 1,
    "throttle_window": {
      "unit": "hours",
      "value": 24
    }
  }
}
```

### Placement

Place throttle steps at the **beginning** of the workflow so that throttled runs are stopped before any channel steps execute. Placing a throttle mid-workflow is valid but means earlier steps will still fire on throttled runs.

### Common mistake: Using throttle instead of trigger_frequency

`throttle` steps control frequency at runtime within a workflow run. `trigger_frequency` in `workflow.json` is a separate setting that controls whether a workflow can be triggered at all for a recipient (`every_trigger` vs `once_per_recipient`). Use both when appropriate—`trigger_frequency` for enrollment gating, throttle steps for send-rate limiting.

## Branch steps

The `branch` step type enables if/else logic within workflows. It evaluates conditions against the workflow run scope and executes the first branch whose conditions are true. A default branch runs when no other branch matches.

### Branch step JSON structure

**Critical rules:**
- The `branches` array must contain **at least 2 entries** (including the default branch)
- Exactly one branch must have `"default": true` — this is the fallback when no conditions match
- Every non-default branch must have at least one condition
- Maximum 10 branches per branch step (including default)
- Maximum nesting depth of 5 levels for nested branch steps

```json
{
  "name": "Branch by plan type",
  "ref": "plan_branch",
  "type": "branch",
  "branches": [
    {
      "name": "Free plan",
      "ref": "free_plan",
      "conditions": {
        "all": [
          {
            "variable": "recipient.plan_type",
            "operator": "equal_to",
            "argument": "free"
          }
        ]
      },
      "steps": [
        {
          "channel_key": "knock-email",
          "channel_type": "email",
          "name": "Free welcome email",
          "ref": "free_email",
          "template": {
            "settings": { "layout_key": "default" },
            "subject": "Get started with free features",
            "visual_blocks@": "free_email/visual_blocks.json"
          },
          "type": "channel"
        }
      ]
    },
    {
      "name": "Default",
      "ref": "default_branch",
      "default": true,
      "steps": [
        {
          "channel_key": "knock-email",
          "channel_type": "email",
          "name": "Paid welcome email",
          "ref": "paid_email",
          "template": {
            "settings": { "layout_key": "default" },
            "subject": "Getting started with your plan",
            "visual_blocks@": "paid_email/visual_blocks.json"
          },
          "type": "channel"
        }
      ]
    }
  ]
}
```

### Common mistake: Using a separate default_branch key

The default branch must be inside the `branches` array with `"default": true`. Do not use a separate `default_branch` top-level key — the API will reject the payload with "must have at least 2 branches" if only one branch is in the array.

**Wrong:**

```json
{
  "type": "branch",
  "branches": [
    { "name": "Free plan", "ref": "free", "conditions": {...}, "steps": [...] }
  ],
  "default_branch": { "name": "Default", "ref": "default", "steps": [...] }
}
```

**Correct:**

```json
{
  "type": "branch",
  "branches": [
    { "name": "Free plan", "ref": "free", "conditions": {...}, "steps": [...] },
    { "name": "Default", "ref": "default", "default": true, "steps": [...] }
  ]
}
```

### Terminating branches

Each branch can optionally terminate the workflow so no subsequent steps run after the branch. Set `"terminates": true` on the branch:

```json
{
  "name": "Inactive user",
  "ref": "inactive",
  "terminates": true,
  "conditions": { "all": [{ "variable": "recipient.is_active", "operator": "equal_to", "argument": "false" }] },
  "steps": []
}
```

### Steps inside branches

Branches can contain any step type: channel steps, delays, batches, throttles, fetches, and even nested branch steps. Step `ref` values must be unique across the entire workflow, not just within a branch.

## Conditions

Conditions are used in branch steps and step-level conditions to control workflow logic. Each condition compares a `variable` against an `argument` using an `operator`.

### Condition structure

```json
{
  "variable": "recipient.plan_type",
  "operator": "equal_to",
  "argument": "free"
}
```

### Combining conditions

Use `"all"` for AND logic (all must be true) or `"any"` for OR logic (at least one must be true):

```json
{
  "conditions": {
    "all": [
      { "variable": "recipient.plan_type", "operator": "equal_to", "argument": "enterprise" },
      { "variable": "data.priority", "operator": "equal_to", "argument": "high" }
    ]
  }
}
```

```json
{
  "conditions": {
    "any": [
      { "variable": "recipient.plan_type", "operator": "equal_to", "argument": "pro" },
      { "variable": "recipient.plan_type", "operator": "equal_to", "argument": "enterprise" }
    ]
  }
}
```

### Condition variable prefixes

These are the same namespaces used in Liquid templates, but formatted as condition variables:

| Prefix | Description | Example |
|--------|-------------|---------|
| `data.` | Trigger payload property | `data.priority` |
| `recipient.` | Recipient property | `recipient.plan_type` |
| `actor.` | Actor property | `actor.role` |
| `vars.` | Environment variable | `vars.feature_flag` |
| `tenant.` | Tenant property | `tenant.plan` |
| `run.` | Workflow run state | `run.total_activities` |
| `workflow.` | Workflow property | `workflow.categories` |
| `refs.<step_ref>.delivery_status` | Message delivery status | `refs.email_1.delivery_status` |
| `refs.<step_ref>.engagement_status` | Message engagement status | `refs.email_1.engagement_status` |

### Condition operators

| Operator | Description |
|----------|-------------|
| `equal_to` | `==` |
| `not_equal_to` | `!=` |
| `greater_than` | `>` |
| `greater_than_or_equal_to` | `>=` |
| `less_than` | `<` |
| `less_than_or_equal_to` | `<=` |
| `contains` | Argument is in variable (strings and lists) |
| `not_contains` | Argument is not in variable |
| `empty` | Variable is empty/null (no argument needed) |
| `not_empty` | Variable is not empty/null (no argument needed) |

## HTTP fetch steps

The `http_fetch` step executes an HTTP request during a workflow run. The JSON response is shallow-merged into the trigger `data`, making it available to all subsequent steps via `{{ data.<field> }}`.

### Fetch step JSON structure

```json
{
  "name": "Fetch user data",
  "ref": "fetch_user",
  "type": "http_fetch",
  "settings": {
    "method": "get",
    "url": "https://api.example.com/v1/users/{{ recipient.id }}",
    "headers": [
      {
        "key": "Authorization",
        "value": "Bearer {{ vars.api_key }}"
      },
      {
        "key": "Content-Type",
        "value": "application/json"
      }
    ]
  }
}
```

### Settings fields

| Field | Description | Required |
|-------|-------------|----------|
| `method` | HTTP method: `get`, `post`, `put`, `delete`, `patch` | Yes |
| `url` | HTTP URL (supports Liquid) | Yes |
| `headers` | Array of `{ "key": "...", "value": "..." }` maps | No |
| `query_params` | Array of `{ "key": "...", "value": "..." }` maps | No |
| `json_body` | JSON request body for POST/PUT (supports Liquid) | No |

### Common mistakes with fetch steps

**Wrong type name:**

The step type is `http_fetch`, not `fetch`. The API will reject `fetch`.

```json
{ "type": "fetch" }
```

Use:

```json
{ "type": "http_fetch" }
```

**Using `template` instead of `settings`:**

Fetch steps are function steps and use `settings`, not `template`. Only channel steps use `template`.

**Headers as a flat object:**

Headers must be an array of key-value maps, not a flat object.

Wrong:

```json
{ "headers": { "Authorization": "Bearer token" } }
```

Correct:

```json
{ "headers": [{ "key": "Authorization", "value": "Bearer token" }] }
```

### Response data merging

Knock uses a shallow-merge strategy:
- Top-level attributes from the response merge into trigger `data`
- Nested attributes are completely overwritten (not deep-merged)
- Response data overwrites original trigger data for matching keys

You can set a response path in the step settings to place the response at a specific location (e.g., `user_data` would make the response available at `data.user_data`).

### Authentication

Use Knock secret variables (`vars`) for API keys and tokens in headers to keep them obfuscated in the dashboard:

```json
{
  "key": "Authorization",
  "value": "Bearer {{ vars.internal_api_key }}"
}
```

## Workflow.json structure

### Minimal workflow

```json
{
  "name": "My Workflow",
  "steps": []
}
```

### Complete workflow example

```json
{
  "name": "Order Confirmation",
  "description": "Sends order confirmation across multiple channels",
  "categories": ["transactional", "orders"],
  "steps": [
    {
      "ref": "email-confirmation",
      "type": "email",
      "template": {
        "subject": "Order #{{data.order_id}} confirmed",
        "visual_blocks@": "email-confirmation/visual_blocks.json"
      }
    },
    {
      "ref": "delay-step",
      "type": "delay",
      "settings": {
        "delay_for": {
          "unit": "hours",
          "value": 1
        }
      }
    },
    {
      "ref": "push-notification",
      "type": "push",
      "template": {
        "title": "Order Shipped!",
        "body": "Your order #{{data.order_id}} is on its way."
      }
    }
  ]
}
```

## Channel-specific templates

### SMS template

```json
{
  "ref": "sms-step",
  "type": "sms",
  "template": {
    "body": "Your code is {{data.code}}. Valid for 10 minutes."
  }
}
```

### Push notification template

```json
{
  "ref": "push-step",
  "type": "push",
  "template": {
    "title": "{{data.title}}",
    "body": "{{data.message}}"
  }
}
```

### In-app feed template

```json
{
  "ref": "in-app-step",
  "type": "in_app_feed",
  "template": {
    "markdown": "**{{actor.name}}** commented on your post",
    "action_url": "{{data.post_url}}"
  }
}
```

### Webhook template

```json
{
  "ref": "webhook-step",
  "type": "webhook",
  "template": {
    "json_body": {
      "event": "order.confirmed",
      "order_id": "{{data.order_id}}",
      "customer_email": "{{recipient.email}}"
    }
  }
}
```

## Validation and debugging

### Check the schema

When encountering validation errors, reference the JSON schema:

```
knock/workflows/workflow.schema.json
```

### Validate before pushing

```bash
knock workflow validate <workflow-key>
```

### Common validation errors

**"Invalid step type"**
- Check that `type` matches a valid step type
- Verify spelling (e.g., `in_app_feed`, not `in-app-feed`)

**"Missing required field"**
- Channel steps require a `template` object
- Templates require specific fields based on channel type

**"Invalid file reference"**
- Check that referenced files exist
- Verify path is relative to the containing file
- Ensure no doubled directory paths

**"buttons[0].variant can't be blank" or "variant is invalid"**
- The `button_set` block requires a `variant` field on each button
- Use `solid` or `outline` for the variant value

**"must have at least 2 branches"**
- The `branches` array in a branch step must contain at least 2 entries
- The default branch must be inside the `branches` array with `"default": true`, not as a separate `default_branch` key

## Testing workflows

### Use the CLI to trigger test runs

```bash
knock workflow run <workflow-key> \
  --recipients='[{"id": "user-123", "email": "test@example.com", "name": "Test User"}]' \
  --data='{"order_id": "12345", "amount": 99.99}'
```

### Test checklist

- [ ] Variables render correctly with real data
- [ ] Default values appear when data is missing
- [ ] Conditional logic works as expected
- [ ] Links and buttons point to correct URLs
- [ ] Email displays properly across clients
- [ ] All channels receive appropriate content

## Best practices summary

1. **Read before writing** - Always check existing structure first
2. **Preserve template modes** - Don't switch between visual blocks and HTML
3. **Use correct namespaces** - `data` for trigger payload, `vars` for environment variables
4. **Paths are relative** - To the file containing the reference
5. **Don't double directories** - Inside step directories, paths are relative to that directory
6. **Always push changes** - Local changes aren't persisted until pushed
7. **Validate first** - Use validate command before pushing to catch errors
8. **Provide defaults** - Use Liquid defaults for optional values
9. **Discover channel keys** - Run `knock channel list` before creating workflows that use channels; use the returned keys for `channel_key`
