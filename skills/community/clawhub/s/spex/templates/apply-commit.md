---
version: "0.1.0"
required:
  - spec_content_concise
  - current_task_description
optional:
  - spex_root
  - completed_tasks_concise
  - future_tasks_concise
  - user_name
  - user_email
---

Act as a senior software engineer creating a precise, meaningful git
commit. Your task is to stage the relevant file changes and create a
single commit with a well-crafted message.

## Commit Message Guidelines

- Follow the **Conventional Commits** format.
- **Title line** (first line): aim for 50 characters or fewer
  (recommended). Must NOT exceed 72 characters (hard limit). Never
  wrap the title across multiple lines. Use the body for details.
- **Body lines**: wrap at 72 characters. Separate from the title
  with a blank line.
- Convey WHY the change was made and the core technical reasoning —
  not an exhaustive list of HOW things were modified.
- Derive context from the Specification below; derive scope from the
  Current Task.
{% if user_name and user_email -%}
- Use HereDoc to pass the commit message, and set the author identity
  to `{{ user_name }} <{{ user_email }}>`:

  ```bash
  git -c user.name="{{ user_name }}" \
      -c user.email="{{ user_email }}" \
      commit -F- <<'EOF'
  <commit message>
  EOF
  ```
{% else -%}
- Use HereDoc to pass the commit message:

  ```bash
  git commit -F- <<'EOF'
  <commit message>
  EOF
  ```
{% endif -%}
{% if spex_root -%}
- **Do NOT stage or commit any files under `{{ spex_root }}/`.**
{% endif %}

## Requirement

The following is the user's requirement description. Use it to
understand the project scope and derive commit context.

<requirement>
{{ spec_content_concise }}
</requirement>

{% if completed_tasks_concise -%}
## Completed Steps

The following steps have already been implemented and committed. Use
them to understand prior work — the commit message can reference this
context but should not duplicate their content.

<completed-steps>
{{ completed_tasks_concise }}
</completed-steps>

{% endif -%}
## Current Changes

The current working tree changes are based on the following task
description. The commit message should describe THIS work specifically.

<current-task>
{{ current_task_description }}
</current-task>
{% if future_tasks_concise %}

## Future Steps

The following steps have NOT been implemented yet. They provide
context for understanding why the current change is structured the
way it is (e.g., preparing for a future refactor), but typically
do not need to appear in the commit message.

{{ future_tasks_concise }}
{% endif %}
