# Packaging template APIs

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Packaging templates: list_templates](#list-templates)
- [Packaging template details: get_template](#get-template)

<a id="list-templates"></a>

## Packaging templates: list_templates

Task type: `VIDEO_PACKING_TEMPLATE_LIST`. Mode: `sync`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/513300738e0)

Query the list directly and use returned detail; template application must match the destination operation.

<a id="list-templates-inputs"></a>

### Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required | Usage |
| --- | --- | --- | --- |
| `business_type` | string | No | Exact business category; use `mixed_cut` for ordinary packaging matching the current translation page; omit to search all categories |
| `template_type` | string | No | Exact template type; video editor templates use `video-editor` |
| `scope` | string | No | `common` public, `tenant` team shared, or `private` current user's personal templates; omission includes all visible scopes |
| `keyword` | text | No | Fuzzy template-name search; omission or an empty string leaves names unfiltered |
| `page` | integer | No | Request pages start at 1; default 1 |
| `size` | integer | No | Default 10; 1–100 items per page |

Query ordinary translation packaging templates visible to the current account:

~~~json
{
  "business_type": "mixed_cut",
  "template_type": "video-editor",
  "page": 1,
  "size": 100
}
~~~

Omit `scope` unless the user restricts it, so team and personal templates remain discoverable. Do not send the undefined value `scope: "all"`. `scrolling_subtitle` is a separate business category, not the default for ordinary translation packaging. Use the relevant actual category for other workflows; do not force `mixed_cut` onto every template query.

The raw API returns a JSON-encoded string at `data.task_result.result`. The CLI already decodes it into its output `result` object; read `result.content`, `result.totalElements`, and `result.totalPages` directly without parsing the object again. Follow `totalPages` when listing all templates or building a complete candidate set; the first page is not the whole library. An unparseable response is an error, not evidence of zero templates.

If a user-named template is missing from this category, omit `business_type` while retaining `template_type: "video-editor"` and the name filter to search all visible categories. Check the actual configuration against the destination operation. See [translation template selection](../resources/packaging-templates.md#translation-template-selection) for selection and application.

<a id="list-templates-call"></a>

### Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_templates --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" list_templates --input /absolute/path/request.json
~~~

The client uses `input_info.input = JSON.stringify(input)` inside the input_info object. Do not change encoding and automatically resubmit after an error.

Use returned detail directly; when only an ID or incomplete detail is available, query [get_template](#get-template).

[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

<a id="get-template"></a>

## Packaging template details: get_template

[Public API](https://vibbit.apifox.cn/513300739e0). VIDEO_PACKING_TEMPLATE_DETAIL queries an existing template by its real template_id. It is read-only and does not create or edit templates.

```json
{ "template_id": "2100065567327711232" }
```

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" get_template --input /absolute/path/template.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" get_template --input /absolute/path/template.json
```

POST /openapi/v1/tasks uses JSON-text input_info.input. The CLI preserves large template IDs as exact integer tokens. Do not pass names, list positions, pagination or editing fields. Check business code, returned identity and actual detail; response completion follows the real result.

Use an ID from the [list](#list-templates) or the user's actual resource. Query missing detail directly without requiring another selection. Apply it through the target operation's contract, such as ordinary template_configs in [translation](translate_video.md). A query result does not enable unsupported applications or dynamic subtitle workflows.
