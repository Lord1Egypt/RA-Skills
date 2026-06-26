# Hyvä CMS Component Schema Reference

> **Fallback snapshot.** When Hyvä Commerce is installed, read the live schema
> directly from the project instead of this file. To refresh this snapshot, read the
> `jsonschema/*.json` files below and regenerate the tables — no helper script needed.
>
> Schema source: `vendor/hyva-themes/commerce-module-cms/src/liveview-editor/etc/hyva_cms/jsonschema/`

## Component Declaration Properties

**IMPORTANT:** Only these properties are allowed at the component level. Using any other property will cause a schema validation error.

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `label` | string | Yes* | - | The label of the component, this gives a user friendly name for the component in the page builder. If not set the name will be used instead. |
| `disabled` | boolean | No | `false` | If true the component will be disabled and not available in the HYVA CMS Liveview Editor. |
| `category` | string | No | `"Other"` | The category of the component, this will be used to group components in the UI of the page builder. |
| `template` | string/boolean | No | Auto | Template path in format `Vendor_Module::path/to/template.phtml`, or `false` for child-only components. If not set, defaults to `[Vendor]_[Module]::elements/[component-name].phtml` |
| `icon` | string | No | Default | Icon path in format `Vendor_Module::path/to/icon.svg`. Supports: jpg, jpeg, png, gif, webp, svg, avif. Defaults to `Hyva_CmsLiveviewEditor::images/components/default.svg` |
| `children` | object/boolean | No | - | Set to `true` to enable children, or an object with `config` for specific configuration. |
| `content` | object | No | - | Field definitions for the Content tab. |
| `design` | object | No | - | Field definitions for the Design tab. |
| `advanced` | object | No | - | Field definitions for the Advanced tab. |
| `custom_properties` | array | No | - | Array for extending the component schema by developers. |
| `require_parent` | boolean | No | `false` | If true the component can only be added as a child of a parent component which can accept it. |

*Required unless `disabled: true` is set.

### Component Name Rules

Component names (the JSON object keys) must:
- Be alphanumeric with dashes and underscores only
- Be at least 3 characters long
- Match pattern: `^[a-zA-Z0-9-_]+$`

## Field Declaration Properties

Fields within `content`, `design`, and `advanced` sections support these properties:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | The field type (see Field Types below) |
| `custom_type` | string | No | Custom type identifier when `type` is `custom_type` |
| `label` | string | Yes | The label for the field in the editor form |
| `default_value` | any | No | The initial value when a new component is created |
| `show_if` | object | No | Optionally defines conditional visibility rules. The field is displayed only when the referenced field's value matches any value in the specified array. |
| `hide_if` | object | No | Optionally defines conditional visibility rules. The field is hidden when the referenced field's value matches any value in the specified array. |
| `attributes` | object/string/number/integer/boolean/null/array | No | The attributes property sets HTML input attributes (placeholder, validation rules, etc.) for compatible field types. Any type allowed, below is expected format. |
| `options` | any | No | For select fields: array of {value, label} or source model class |
| `config` | object | No | Additional configuration (accepts, excludes, max_children for children) |
| `custom_properties` | array | No | Array for extending the field schema |

### Special Property: includes

The `includes` property in `content`, `design`, or `advanced` sections allows inheriting fields from another file:

```json
{
    "design": {
        "includes": "Hyva_CmsBase::etc/hyva_cms/default_design.json"
    }
}
```

Or multiple files:

```json
{
    "design": {
        "includes": [
            "Hyva_CmsBase::etc/hyva_cms/default_design.json",
            "Hyva_CmsBase::etc/hyva_cms/default_design_typography.json"
        ]
    }
}
```

## Field Types

| Type | Description |
|------|-------------|
| `boolean` | Toggle switch for true/false values |
| `color` | Color picker input |
| `date` | Date picker |
| `datetime` | Date and time picker |
| `html` | Raw HTML code input |
| `image` | Image upload field |
| `link` | URL/link configuration with target options |
| `multiselect` | Multiple selection dropdown |
| `number` | Numeric input |
| `range` | Slider input for numeric values |
| `products` | Product selector |
| `richtext` | WYSIWYG rich text editor |
| `select` | Dropdown selection |
| `searchable_select` | Searchable dropdown for large option lists |
| `text` | Single-line text input |
| `text-align` | Text alignment selector |
| `textarea` | Multi-line text input |
| `variant` | Template variant selector |
| `widget` | Magento widget selector |
| `custom_type` | Custom field type (requires `custom_type` property) |

## Validation Attributes

Common attributes for field validation:

| Attribute | Description |
|-----------|-------------|
| `required` | Field must have a value (boolean) |
| `minlength` | Minimum text length |
| `maxlength` | Maximum text length |
| `min` | Minimum numeric value |
| `max` | Maximum numeric value |
| `step` | Numeric step increment |
| `pattern` | Regex pattern for validation |
| `placeholder` | Placeholder text |
| `comment` | Help text displayed below the field |

### Custom Validation Messages

| Attribute | Description |
|-----------|-------------|
| `data-required-msg` | Custom message for required validation |
| `data-min-msg` | Custom message for minimum validation |
| `data-max-msg` | Custom message for maximum validation |
| `data-pattern-msg` | Custom message for pattern validation |

## Invalid Properties

The following properties do **NOT** exist and will cause schema errors:

- `hidden` - Use `require_parent: true` for child-only components, or `disabled: true` to hide from editor
- Any property not listed in the Component Declaration Properties table above
