# Variant Support Reference

Template variants allow a single component to offer multiple layout options. Users select a variant in the editor, and the corresponding template renders.

## Directory Structure

When using variants, templates are organized in a subdirectory named after the component:

```
view/frontend/templates/elements/
└── feature-card/
    ├── default.phtml
    ├── compact.phtml
    └── wide.phtml
```

## Component Configuration

Use the `variant` field type in the `content` section. Each option specifies its own template path.

```json
{
    "feature_card": {
        "label": "Feature Card",
        "category": "Elements",
        "content": {
            "variant": {
                "type": "variant",
                "label": "Layout",
                "default_value": "default",
                "options": [
                    {
                        "value": "default",
                        "label": "Default",
                        "template": "Vendor_Module::elements/feature-card/default.phtml"
                    },
                    {
                        "value": "compact",
                        "label": "Compact",
                        "template": "Vendor_Module::elements/feature-card/compact.phtml"
                    },
                    {
                        "value": "wide",
                        "label": "Wide",
                        "template": "Vendor_Module::elements/feature-card/wide.phtml"
                    }
                ]
            },
            "title": {"type": "text", "label": "Title"},
            "description": {"type": "textarea", "label": "Description"}
        },
        "design": {
            "includes": [
                "Hyva_CmsBase::etc/hyva_cms/default_design.json"
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

**Important:** When using the `variant` field type, omit the top-level `template` property. Each variant option specifies its own template.

## Variant Field Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Must be `"variant"` |
| `label` | string | Yes | Display label in editor (e.g., "Layout", "Style") |
| `default_value` | string | Yes | The `value` of the default variant option |
| `options` | array | Yes | Array of variant options |

### Variant Option Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `value` | string | Yes | Unique identifier for the variant |
| `label` | string | Yes | Display label in the variant selector |
| `template` | string | Yes | Full template path for this variant |

## Template Implementation

Each variant template is a standard PHTML file with the same field access:

```php
<?php
declare(strict_types=1);

use Hyva\CmsLiveviewEditor\Block\Element;
use Hyva\Theme\Model\ViewModelRegistry;
use Magento\Framework\Escaper;

/** @var Element $block */
/** @var Escaper $escaper */
/** @var ViewModelRegistry $viewModels */

$title = $block->getData('title');
$description = $block->getData('description');
?>
<div <?= /** @noEscape */ $block->getEditorAttrs() ?> class="variant-specific-classes">
    <?php if ($title): ?>
        <h3 <?= /** @noEscape */ $block->getEditorAttrs('title') ?>>
            <?= $escaper->escapeHtml($title) ?>
        </h3>
    <?php endif; ?>

    <?php if ($description): ?>
        <p <?= /** @noEscape */ $block->getEditorAttrs('description') ?>>
            <?= $escaper->escapeHtml($description) ?>
        </p>
    <?php endif; ?>
</div>
```

All variant templates share the same field data - only the HTML structure and styling differ.

## Common Variant Patterns

### Layout Variants
- `default`, `compact`, `wide`, `full-width`
- Use for different spacing/sizing options

### Style Variants
- `light`, `dark`, `outlined`, `filled`
- Use for different visual treatments

### Alignment Variants
- `left`, `center`, `right`
- Use when image/content positioning varies significantly

## Best Practices

1. **Consistent field access** - All variants use the same `$block->getData()` calls
2. **Meaningful names** - Use descriptive variant values (`compact` not `v2`)
3. **Default first** - List the default variant as the first option
4. **Shared styles** - Extract common Tailwind classes to reduce duplication
5. **Preview consideration** - Ensure each variant is visually distinct in the editor