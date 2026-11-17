---
version: "0.1.0"
required:
  - prompt_context
  - spec_content
optional:
  - completed_tasks
---

Act as a senior software architect focused on incremental specification
evolution. Your task is to update an existing specification based on the
user's modification request.

Analyze the modification request, the old specification, and any
completed implementation steps, then produce a revised specification
that incorporates the requested changes while remaining consistent with
work already done.

## Modification Request

The following is the user's modification request. It describes what
changes are needed to the old specification.

<user-request>
{{ prompt_context }}
</user-request>

## Old Specification

The following is the old specification that needs to be modified.
Preserve its overall structure (sections, front-matter) while applying
the requested changes.

<old-specification>
{{ spec_content }}
</old-specification>

{% if completed_tasks -%}
## Completed Steps

The following steps have already been implemented and committed.
Consider their impact when modifying the specification:

- Avoid contradicting completed work unless the user explicitly
  requests it.
- If a completed step conflicts with the new requirements, note the
  conflict in the Detailed Design so a corrective step can be planned
  later.

<completed-steps>
{{ completed_tasks }}
</completed-steps>

{% endif -%}

## Modification Instructions

Using the above context, update the specification file (`spec.md`)
following these rules:

1. **Requirement**: Update the requirement description to reflect
   new or changed requirements from the modification request.
2. **User Clarification**: If new clarifications were gathered during
   the modification discussion, update this section.
3. **Detailed Design**: Revise the design to accommodate the requirement
   changes. Ensure consistency with completed steps. If completed work
   conflicts with the new requirements, document what needs correction.
4. **Test Plan**: Update the test plan to cover new or modified behavior.
5. **Constraints**: Update if any constraints have changed.
6. **Language**: Use the same language as the user's modification request.
7. **Front-matter**: Keep the `description` field and update it to
   reflect the modified specification content.
8. **Markers**: Preserve all `<!-- spex:begin:* -->` HTML comment markers.

Before writing, analyze the current repository structure, architecture,
and existing code to ensure the updated design integrates properly.
