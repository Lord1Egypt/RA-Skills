# Critical Patterns and Common Mistakes

This document highlights the most important patterns to follow and common mistakes to avoid when creating Hyvä CMS components.

## 1. Children Configuration

### ❌ INCORRECT - Children as a field type in content

```json
{
    "my_component": {
        "label": "My Component",
        "content": {
            "items": {
                "type": "children",
                "label": "Items",
                "config": {
                    "accepts": ["child_component"]
                }
            }
        }
    }
}
```

**Why this is wrong:** `children` is NOT a field type. It cannot be used in `content`, `design`, or `advanced` sections.

### ✅ CORRECT - Children as root-level property

```json
{
    "my_component": {
        "label": "My Component",
        "children": {
            "config": {
                "accepts": ["child_component"],
                "max_children": 10
            }
        },
        "content": {
            "title": {
                "type": "text",
                "label": "Title"
            }
        }
    }
}
```

**Template access:**
```php
$children = $block->getData('children') ?: [];

foreach ($children as $child) {
    echo $block->createChildHtml($child, 'child-' . $index);
}
```

## 2. Field Validation Attributes

### ❌ INCORRECT - Validation as direct field property

```json
{
    "title": {
        "type": "text",
        "label": "Title",
        "required": true,
        "minlength": "3",
        "maxlength": "100"
    }
}
```

**Why this is wrong:** Validation attributes must be inside the `attributes` object, not as direct properties on the field.

### ✅ CORRECT - Validation in attributes object

```json
{
    "title": {
        "type": "text",
        "label": "Title",
        "attributes": {
            "required": true,
            "minlength": "3",
            "maxlength": "100",
            "pattern": "^[A-Za-z ]+$",
            "placeholder": "Enter title"
        }
    }
}
```

**All validation attributes that go in `attributes`:**
- `required` (boolean)
- `minlength` / `maxlength` (string)
- `min` / `max` (for number/range fields)
- `pattern` (regex string)
- `placeholder` (string)
- `comment` (help text)
- Custom data attributes (e.g., `data-validation-message`)

## 3. Default Values

### ❌ INCORRECT - Using "default" key

```json
{
    "title": {
        "type": "text",
        "label": "Title",
        "default": "My Title"
    }
}
```

### ✅ CORRECT - Using "default_value" key

```json
{
    "title": {
        "type": "text",
        "label": "Title",
        "default_value": "My Title"
    }
}
```

## 4. Root-Level Component Properties

These properties go at the component root level (same level as `label`, `content`, etc.):

- `label` (required)
- `category`
- `template`
- `icon`
- `children` ← Root-level property, NOT a field type
- `require_parent`
- `content`
- `design`
- `advanced`
- `disabled`
- `visible`
- `custom_properties`

## 5. Field Properties vs Attributes

### Field Properties (direct on field object):
- `type` (required)
- `label` (required)
- `default_value`
- `attributes` (object for validation/HTML attributes)
- `config` (object for field-specific configuration)
- `options` (array for select/multiselect)
- `show_if` / `hide_if` (conditional visibility)

### Attributes (inside `attributes` object):
- HTML5 validation: `required`, `minlength`, `maxlength`, `min`, `max`, `pattern`
- Input attributes: `placeholder`, `rows`, `cols`
- Custom data attributes: `data-*`
- Help text: `comment`

## Quick Checklist

Before committing a component definition, verify:

- [ ] `children` is at root level, NOT in `content`/`design`/`advanced`
- [ ] All validation uses `attributes.required`, NOT direct `required` property
- [ ] Default values use `default_value`, NOT `default`
- [ ] Component has `label` (required)
- [ ] Template path is correct or omitted for default path
- [ ] All field types are valid (no `"type": "children"`)
- [ ] Template accesses children via `$block->getData('children')`
- [ ] Template uses `$block->getEditorAttrs()` on root and editable elements
- [ ] Proper escaping in template: `escapeHtml()`, `escapeHtmlAttr()`, `escapeUrl()`

## References

- [Official Hyvä Docs - Creating Components](https://docs.hyva.io/hyva-commerce/features/cms/creating-components.html)
- [Official Hyvä Docs - Child Components](https://docs.hyva.io/hyva-commerce/features/cms/creating-components.html#child-components)
- [Official Hyvä Docs - Field Validation](https://docs.hyva.io/hyva-commerce/features/cms/creating-components.html#custom-field-validation)
