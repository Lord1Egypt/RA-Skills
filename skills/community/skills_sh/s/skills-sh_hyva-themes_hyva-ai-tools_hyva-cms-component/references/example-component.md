# Complete Example: Feature Card Component

This example shows a complete Hyvä CMS component from definition to template.

## Component Definition

**File:** `app/code/Acme/CmsComponents/etc/hyva_cms/components.json`

```json
{
    "feature_card": {
        "label": "Feature Card",
        "category": "Elements",
        "template": "Acme_CmsComponents::elements/feature-card.phtml",
        "content": {
            "image": {
                "type": "image",
                "label": "Image"
            },
            "title": {
                "type": "text",
                "label": "Title",
                "default_value": "Feature Title",
                "attributes": {
                    "placeholder": "Enter feature title",
                    "required": true
                }
            },
            "description": {
                "type": "textarea",
                "label": "Description",
                "attributes": {
                    "placeholder": "Enter description",
                    "rows": "3"
                }
            },
            "link": {
                "type": "link",
                "label": "Link"
            },
            "style": {
                "type": "select",
                "label": "Card Style",
                "default_value": "default",
                "options": [
                    {"value": "default", "label": "Default"},
                    {"value": "outlined", "label": "Outlined"},
                    {"value": "elevated", "label": "Elevated"}
                ]
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

## PHTML Template

**File:** `app/code/Acme/CmsComponents/view/frontend/templates/elements/feature-card.phtml`

```php
<?php
declare(strict_types=1);

use Hyva\CmsLiveviewEditor\Block\Element;
use Hyva\Theme\Model\ViewModelRegistry;
use Hyva\Theme\ViewModel\Media;
use Magento\Framework\Escaper;

/** @var Element $block */
/** @var Escaper $escaper */
/** @var ViewModelRegistry $viewModels */

// Content fields
$image = $block->getData('image');
$title = $block->getData('title');
$description = $block->getData('description');
$link = $block->getData('link');
$linkData = $link ? $block->getLinkData($link) : null;
$style = $block->getData('style') ?: 'default';

// Design fields (from includes)
$textAlign = $block->getData('text_align') ?: 'text-left';
$textColor = $block->getData('text_color') ?: '';
$backgroundColor = $block->getData('background_color') ?: 'transparent';

// Advanced fields (from includes)
$classes = $block->getData('classes') ?: '';
$blockId = $block->getData('block_id') ?: '';

// Style classes based on selection
$styleClasses = match($style) {
    'outlined' => 'border border-gray-300',
    'elevated' => 'shadow-lg',
    default => 'bg-white'
};

// Media view model for responsive images
/** @var Media $mediaViewModel */
$mediaViewModel = $viewModels->require(Media::class);
?>
<div <?= /** @noEscape */ $block->getEditorAttrs() ?>
     <?php if ($blockId): ?>id="<?= $escaper->escapeHtmlAttr($blockId) ?>"<?php endif; ?>
     class="p-6 rounded-lg <?= $escaper->escapeHtmlAttr($styleClasses) ?> <?= $escaper->escapeHtmlAttr($textAlign) ?> <?= $escaper->escapeHtmlAttr($classes) ?>"
     style="background-color: <?= $escaper->escapeHtmlAttr($backgroundColor) ?>;<?php if ($textColor): ?> color: <?= $escaper->escapeHtmlAttr($textColor) ?>;<?php endif; ?>">

    <?php if ($image): ?>
        <div class="mb-4">
            <?= /** @noEscape */ $mediaViewModel->getResponsivePictureHtml(
                $image,
                ['class' => 'w-full h-auto rounded', 'loading' => 'lazy']
            ) ?>
        </div>
    <?php endif; ?>

    <?php if ($title): ?>
        <h3 <?= /** @noEscape */ $block->getEditorAttrs('title') ?>
            class="text-xl font-semibold mb-2">
            <?= $escaper->escapeHtml($title) ?>
        </h3>
    <?php endif; ?>

    <?php if ($description): ?>
        <p <?= /** @noEscape */ $block->getEditorAttrs('description') ?>
           class="text-gray-600 mb-4">
            <?= $escaper->escapeHtml($description) ?>
        </p>
    <?php endif; ?>

    <?php if ($linkData): ?>
        <a href="<?= $escaper->escapeUrl($linkData['url']) ?>"
           <?php if (!empty($linkData['target'])): ?>target="<?= $escaper->escapeHtmlAttr($linkData['target']) ?>"<?php endif; ?>
           class="inline-block text-blue-600 hover:text-blue-800 font-medium">
            <?= $escaper->escapeHtml($linkData['title'] ?: 'Learn more') ?> &rarr;
        </a>
    <?php endif; ?>

</div>
```

## Module Files

For completeness, here are the supporting module files created by the `hyva-create-module` skill:

**File:** `app/code/Acme/CmsComponents/registration.php`

```php
<?php
declare(strict_types=1);

use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    'Acme_CmsComponents',
    __DIR__
);
```

**File:** `app/code/Acme/CmsComponents/etc/module.xml`

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:framework:Module/etc/module.xsd">
    <module name="Acme_CmsComponents">
        <sequence>
            <module name="Hyva_CmsBase"/>
        </sequence>
    </module>
</config>
```

**File:** `app/code/Acme/CmsComponents/composer.json`

```json
{
    "name": "acme/module-cms-components",
    "description": "Custom Hyvä CMS components",
    "type": "magento2-module",
    "require": {
        "magento/framework": "*",
        "hyva-themes/commerce-module-cms": "^1.0"
    },
    "autoload": {
        "files": [
            "registration.php"
        ],
        "psr-4": {
            "Acme\\CmsComponents\\": ""
        }
    }
}
```

## Directory Structure

```
app/code/Acme/CmsComponents/
├── registration.php
├── composer.json
├── etc/
│   ├── module.xml
│   └── hyva_cms/
│       └── components.json
└── view/
    └── frontend/
        └── templates/
            └── elements/
                └── feature-card.phtml
```

## Key Points Demonstrated

1. **Editor attributes** - `$block->getEditorAttrs()` on root, `$block->getEditorAttrs('field_name')` on editable fields
2. **Field type handling** - Text, textarea, image, link, and select fields
3. **Conditional rendering** - Only render elements when data exists
4. **Proper escaping** - `escapeHtml()` for text, `escapeHtmlAttr()` for attributes, `escapeUrl()` for URLs
5. **Design/Advanced includes** - Standard styling options via JSON includes
6. **Responsive images** - Using the Media view model for image rendering
7. **Link data extraction** - Using `$block->getLinkData()` for link fields