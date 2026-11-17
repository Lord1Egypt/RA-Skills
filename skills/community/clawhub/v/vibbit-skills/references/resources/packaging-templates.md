# Packaging templates

Query [list_templates](../api/list_templates.md) with the relevant filters. Use real returned IDs and available detail/configuration. A list index is not an ID; there is no separate public detail command. Do not invent missing configuration fields.

Keep Vibbit packaging IDs separate from local render-template IDs. Apply the actual selected template through the supported composition configuration. For translation subtitle style `type: 0`, use the actual ID in `template_configs` as described in [translate_video](../api/translate_video.md).
