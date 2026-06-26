# Hyvä CMS Component Field Types Reference

Complete reference for all field types supported in Hyvä CMS component declarations.

**IMPORTANT:** This document covers field types used within `content`, `design`, and `advanced` sections. The `children` property is NOT a field type - it is a root-level component property. See the main SKILL.md for children configuration.

## Field Structure

Every field in `content`, `design`, or `advanced` sections follows this structure:

```json
{
    "field_name": {
        "type": "field_type",
        "label": "Display Label",
        "default_value": "optional default",
        "attributes": {},
        "config": {},
        "options": [],
        "show_if": {},
        "hide_if": {}
    }
}
```

## Text Fields

### text

Single-line text input.

```json
{
    "title": {
        "type": "text",
        "label": "Title",
        "default_value": "Default Title",
        "attributes": {
            "placeholder": "Enter title",
            "required": true,
            "minlength": "3",
            "maxlength": "100",
            "pattern": "^[A-Za-z ]+$",
            "data-required-msg": "Title is required",
            "data-pattern-msg": "Only letters and spaces allowed"
        }
    }
}
```

### textarea

Multi-line text input.

```json
{
    "description": {
        "type": "textarea",
        "label": "Description",
        "attributes": {
            "placeholder": "Enter description",
            "rows": "4"
        }
    }
}
```

### richtext

WYSIWYG rich text editor with formatting options.

```json
{
    "content": {
        "type": "richtext",
        "label": "Content",
        "default_value": "<p>Default content</p>"
    }
}
```

### html

Raw HTML code input (no formatting toolbar).

```json
{
    "custom_html": {
        "type": "html",
        "label": "Custom HTML"
    }
}
```

## Numeric Fields

### number

Numeric input with optional constraints.

```json
{
    "quantity": {
        "type": "number",
        "label": "Quantity",
        "default_value": 1,
        "attributes": {
            "min": "0",
            "max": "100",
            "step": "1"
        }
    }
}
```

### range

Slider input for numeric values.

```json
{
    "gap_size": {
        "type": "range",
        "label": "Gap Size",
        "default_value": 1,
        "attributes": {
            "min": "0",
            "max": "10",
            "step": "0.25"
        },
        "config": {
            "value_suffix": "rem"
        }
    }
}
```

## Boolean

Toggle switch for true/false values.

```json
{
    "show_title": {
        "type": "boolean",
        "label": "Show Title",
        "default_value": true
    }
}
```

## Selection Fields

### select

Dropdown selection with single choice.

```json
{
    "style": {
        "type": "select",
        "label": "Style",
        "default_value": "primary",
        "options": [
            {"value": "primary", "label": "Primary"},
            {"value": "secondary", "label": "Secondary"},
            {"value": "default", "label": "Default"}
        ]
    }
}
```

### select with source model

Use a PHP class for dynamic options.

```json
{
    "btn_style": {
        "type": "select",
        "label": "Button Style",
        "default_value": "btn-primary",
        "options": "Hyva\\CmsBase\\Model\\Config\\Source\\ButtonBackground"
    }
}
```

### multiselect

Multiple selection dropdown.

```json
{
    "categories": {
        "type": "multiselect",
        "label": "Categories",
        "options": [
            {"value": "cat1", "label": "Category 1"},
            {"value": "cat2", "label": "Category 2"},
            {"value": "cat3", "label": "Category 3"}
        ]
    }
}
```

### searchable_select

Searchable dropdown for large option lists.

```json
{
    "cms_block": {
        "type": "searchable_select",
        "label": "CMS Block",
        "options": "Hyva\\CmsBase\\Model\\Config\\Source\\CmsBlocks"
    }
}
```

## Media Fields

### image

Image upload field.

```json
{
    "image": {
        "type": "image",
        "label": "Image",
        "config": {
            "allowed_extensions": ["jpg", "jpeg", "png", "gif", "webp", "svg"]
        }
    }
}
```

### color

Color picker input.

```json
{
    "background_color": {
        "type": "color",
        "label": "Background Color",
        "default_value": "transparent",
        "attributes": {
            "data-pattern": "^#?[a-zA-Z0-9,().\\-\\s%]+$",
            "data-pattern-msg": "Value must be a valid CSS background-color"
        }
    }
}
```

## Link Field

URL/link configuration with target options.

```json
{
    "link": {
        "type": "link",
        "label": "Link"
    }
}
```

Returns an array with: `url`, `title`, `target`, `type`

## Date Fields

### date

Date picker.

```json
{
    "start_date": {
        "type": "date",
        "label": "Start Date"
    }
}
```

### datetime

Date and time picker.

```json
{
    "publish_at": {
        "type": "datetime",
        "label": "Publish At"
    }
}
```

## Special Fields

### text-align

Text alignment selector (left, center, right, justify).

```json
{
    "text_align": {
        "type": "text-align",
        "label": "Text Align",
        "default_value": "text-left"
    }
}
```

### variant

Template variant selector - allows different templates for the same component.

```json
{
    "variant": {
        "type": "variant",
        "label": "Variant",
        "default_value": "default",
        "options": [
            {
                "value": "default",
                "label": "Default",
                "template": "Vendor_Module::elements/component/default.phtml"
            },
            {
                "value": "compact",
                "label": "Compact",
                "template": "Vendor_Module::elements/component/compact.phtml"
            },
            {
                "value": "wide",
                "label": "Wide",
                "template": "Vendor_Module::elements/component/wide.phtml"
            }
        ]
    }
}
```

### widget

Magento widget selector.

```json
{
    "widget": {
        "type": "widget",
        "label": "Widget"
    }
}
```

### products

Product selector (by SKU or category).

```json
{
    "products": {
        "type": "products",
        "label": "Products"
    }
}
```

### children

**IMPORTANT:** `children` is NOT a field type. It is a root-level component property.

Do NOT use this in `content`, `design`, or `advanced` sections:

**INCORRECT ❌:**
```json
{
    "my_component": {
        "content": {
            "items": {
                "type": "children",
                "label": "Items"
            }
        }
    }
}
```

Instead, declare `children` at the component root level:

**CORRECT ✅:**
```json
{
    "my_component": {
        "label": "My Component",
        "children": {
            "config": {
                "accepts": ["button", "text"],
                "excludes": ["slider"],
                "max_children": 10
            }
        }
    }
}
```

In templates, access children data via `$block->getData('children')`. See the main SKILL.md for complete examples.

## Conditional Visibility

Show or hide fields based on other field values.

### show_if

```json
{
    "show_image": {
        "type": "boolean",
        "label": "Show Image",
        "default_value": true
    },
    "image": {
        "type": "image",
        "label": "Image",
        "show_if": {
            "show_image": true
        }
    }
}
```

### hide_if

```json
{
    "use_custom_color": {
        "type": "boolean",
        "label": "Use Custom Color",
        "default_value": false
    },
    "preset_color": {
        "type": "select",
        "label": "Preset Color",
        "hide_if": {
            "use_custom_color": true
        },
        "options": [
            {"value": "red", "label": "Red"},
            {"value": "blue", "label": "Blue"}
        ]
    },
    "custom_color": {
        "type": "color",
        "label": "Custom Color",
        "show_if": {
            "use_custom_color": true
        }
    }
}
```

## Validation Attributes

Common validation attributes for fields:

| Attribute | Description |
|-----------|-------------|
| `required` | Field must have a value |
| `minlength` | Minimum text length |
| `maxlength` | Maximum text length |
| `min` | Minimum numeric value |
| `max` | Maximum numeric value |
| `step` | Numeric step increment |
| `pattern` | Regex pattern for validation |
| `placeholder` | Placeholder text |

### Custom Validation Messages

Use `data-` prefixed attributes for custom messages:

```json
{
    "attributes": {
        "required": true,
        "pattern": "^[A-Za-z]+$",
        "data-required-msg": "This field is required",
        "data-pattern-msg": "Only letters are allowed",
        "data-min-msg": "Value is too small",
        "data-max-msg": "Value is too large"
    }
}
```

## Including Shared Configurations

Use `includes` to inherit common field definitions:

```json
{
    "my_component": {
        "label": "My Component",
        "content": {
            "title": {
                "type": "text",
                "label": "Title"
            }
        },
        "design": {
            "includes": [
                "Hyva_CmsBase::etc/hyva_cms/default_design.json",
                "Hyva_CmsBase::etc/hyva_cms/default_design_typography.json"
            ]
        },
        "advanced": {
            "includes": [
                "Hyva_CmsBase::etc/hyva_cms/default_advanced.json"
            ]
        }
    }
}
```

### Available Include Files

From `Hyva_CmsBase`:

- `Hyva_CmsBase::etc/hyva_cms/default_design.json` - Adds `background_color`
- `Hyva_CmsBase::etc/hyva_cms/default_design_typography.json` - Adds `text_color`, `text_align`
- `Hyva_CmsBase::etc/hyva_cms/default_advanced.json` - Adds `classes`, `block_id`

## Field Presets

Common field combinations for typical components:

### Basic Card
```json
{
    "title": {"type": "text", "label": "Title"},
    "description": {"type": "textarea", "label": "Description"},
    "link": {"type": "link", "label": "Link"}
}
```

### Image Card
```json
{
    "image": {"type": "image", "label": "Image"},
    "title": {"type": "text", "label": "Title"},
    "description": {"type": "textarea", "label": "Description"},
    "link": {"type": "link", "label": "Link"}
}
```

### CTA Block
```json
{
    "heading": {"type": "text", "label": "Heading"},
    "subheading": {"type": "text", "label": "Subheading"},
    "content": {"type": "richtext", "label": "Content"},
    "button_text": {"type": "text", "label": "Button Text", "default_value": "Learn More"},
    "link": {"type": "link", "label": "Button Link"},
    "image": {"type": "image", "label": "Background Image"}
}
```

### Text Block
```json
{
    "title": {"type": "text", "label": "Title"},
    "content": {"type": "richtext", "label": "Content"}
}
```

### Feature Item
```json
{
    "icon": {"type": "image", "label": "Icon"},
    "title": {"type": "text", "label": "Title"},
    "description": {"type": "textarea", "label": "Description"}
}
```

### Accordion Item
```json
{
    "title": {"type": "text", "label": "Title"},
    "content": {"type": "richtext", "label": "Content"},
    "expanded": {"type": "boolean", "label": "Initially Expanded", "default_value": false}
}
```

### Testimonial
```json
{
    "quote": {"type": "textarea", "label": "Quote"},
    "author_name": {"type": "text", "label": "Author Name"},
    "author_title": {"type": "text", "label": "Author Title"},
    "author_image": {"type": "image", "label": "Author Image"}
}
```
