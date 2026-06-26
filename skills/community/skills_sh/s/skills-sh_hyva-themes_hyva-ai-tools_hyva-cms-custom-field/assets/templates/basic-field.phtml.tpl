<?php
/**
 * Basic Custom Field Type Template
 * 
 * Use this template for simple custom field types with specialized validation
 * or input controls that don't require complex UI interactions.
 * 
 * Replace placeholders:
 * - {{FIELD_INPUTS}} - Your input element(s) HTML
 * - {{CUSTOM_VALIDATION}} - Optional custom validation logic
 */

declare(strict_types=1);

use Magento\Backend\Block\Template;
use Magento\Framework\Escaper;
use Hyva\CmsLiveviewEditor\Magewire\LiveviewComposer;
use Hyva\Theme\Model\ViewModelRegistry;
use Hyva\CmsLiveviewEditor\ViewModel\Adminhtml\FieldTypes;

/** @var Template $block */
/** @var Escaper $escaper */
/** @var LiveviewComposer $magewire */
/** @var ViewModelRegistry $viewModels */

/** @var FieldTypes $fieldTypes */
$fieldTypes = $viewModels->require(FieldTypes::class);

// Component and field identifiers passed by Hyvä CMS editor
$uid = (string) $block->getData('uid');
$fieldName = (string) $block->getData('name');
$fieldValue = $block->getData('value') ?? '';

// Options from component configuration (if using options like select)
$options = (array) $block->getData('options');

// HTML attributes from component configuration (e.g., validation patterns)
$attributes = (array) $block->getData('attributes') ?? [];
$filteredAttributes = $fieldTypes->getDefinedFieldAttributes($attributes);

// Validation state from Magewire component
$hasError = isset($magewire->errors[$uid][$fieldName]);
$errorMessage = $hasError ? $magewire->errors[$uid][$fieldName] : '';

?>
<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
    {{FIELD_INPUTS}}
    <!-- Example:
    <input type="text"
           name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           value="<?= $escaper->escapeHtmlAttr($fieldValue) ?>"
           @change="updateWireField(
               '<?= $escaper->escapeHtmlAttr($uid) ?>',
               '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
               $event.target.value
           )"
           class="form-input <?= $hasError ? 'error field-error' : '' ?>"
           <?php foreach ($filteredAttributes as $attr => $attrValue): ?>
               <?= $escaper->escapeHtmlAttr($attr) ?>="<?= $escaper->escapeHtmlAttr($attrValue) ?>"
           <?php endforeach; ?>>
    -->
    
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
        class="validation-messages list-none">
        <?php if ($hasError): ?>
            <li class="error-message text-red-600 text-sm mt-1">
                <?= $escaper->escapeHtml($errorMessage) ?>
            </li>
        <?php endif; ?>
    </ul>
</div>

{{CUSTOM_VALIDATION}}
<!-- Optional: Add custom validation logic here
<script>
// Custom validation or UI enhancements
</script>
-->
