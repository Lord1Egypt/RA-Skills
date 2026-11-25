# Packaging templates

Query [list_templates](../api/templates.md#list-templates) with the relevant filters. Use real returned IDs and available detail/configuration. When only an ID or incomplete detail is available, use [get_template](../api/templates.md#get-template), task type VIDEO_PACKING_TEMPLATE_DETAIL. A list index is not an ID. Queries do not create, edit or automatically apply templates; do not invent configuration fields.

Keep Vibbit packaging IDs separate from local render-template IDs. Apply the actual selected template through the supported composition configuration; local project IDs and paths are not cloud packaging IDs.

## Translation template selection

When the user supplies a real template ID, query its details directly without asking them to select again. Otherwise use `list_templates` with `business_type: "mixed_cut"` and `template_type: "video-editor"`, matching ordinary packaging on the current translation page. Add `keyword` for a user-specified name. Omit `scope` unless restricted by the user so public, team and personal templates visible to the account are included. Follow returned pagination for a complete candidate set. See the [list API](../api/templates.md#list-templates) for parameters and searching other categories.

Reuse complete `detail` from the list; call `get_template` only when it is missing. Show actual names, IDs, available configuration and returned previews; a name or list index does not prove a style. Honor an existing explicit selection without adding confirmations for routine list/detail queries.

Submit translation packaging with `template_type: 0` and the selected real ID in `template_configs`. The numeric `0` here and the query string `video-editor` belong to different field contracts. Translation selects an existing template and does not edit its contents. Before enabling translated-title alignment, check for an actual enabled title slot. If absent, continue looking for a suitable template rather than assuming all templates support titles. Read [translate_video](../api/translate_video.md) for application and inheritance rules, then inspect the actual result.

Dynamic subtitle templates remain unavailable. Finding a template in another business category does not establish that the destination translation operation can apply it.
