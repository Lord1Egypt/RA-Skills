<?php
/**
 * Modal-Based Field Handler - Field Template
 * 
 * Use this template for the field part of a modal-based handler.
 * This template displays the current selection and a button to open the handler modal.
 * 
 * Replace placeholders:
 * - {{EVENT_NAME}} - Custom event name to dispatch (e.g., toggle-product-select)
 * - {{BUTTON_LABEL}} - Button text (e.g., "Select Products")
 * - {{DISPLAY_VALUE}} - Code to display current selection summary
 */

declare(strict_types=1);

use Magento\Backend\Block\Template;
use Magento\Framework\Escaper;
use Hyva\CmsLiveviewEditor\Magewire\LiveviewComposer;

/** @var Template $block */
/** @var Escaper $escaper */
/** @var LiveviewComposer $magewire */

$uid = (string) $block->getData('uid');
$fieldName = (string) $block->getData('name');
$fieldValue = $block->getData('value') ?? '';

// Get custom attributes from component configuration
$attributes = (array) $block->getData('attributes') ?? [];

$hasError = isset($magewire->errors[$uid][$fieldName]);

// Parse current field value for display (handle both array and JSON string)
// Adjust this based on your data structure
$selectedItems = [];
if ($fieldValue) {
    if (is_array($fieldValue)) {
        $selectedItems = $fieldValue;
    } elseif (is_string($fieldValue)) {
        try {
            $decoded = json_decode($fieldValue, true);
            if (is_array($decoded)) {
                $selectedItems = $decoded;
            }
        } catch (\Exception $e) {
            // Keep default empty array
        }
    }
}

// Ensure field value is always a JSON string for the hidden input
$fieldValueJson = is_array($fieldValue) ? json_encode($fieldValue) : $fieldValue;
?>

<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
    {{DISPLAY_VALUE}}
    <!-- Example: Display selected items summary
    <div class="mb-2">
        <?php if (!empty($selectedItems)): ?>
            <div class="text-sm text-gray-600">
                Selected: <?= count($selectedItems) ?> item<?= count($selectedItems) > 1 ? 's' : '' ?>
            </div>
            <div class="flex flex-wrap gap-2 mt-2">
                <?php foreach ($selectedItems as $item): ?>
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                        <?= $escaper->escapeHtml($item['name'] ?? $item['label'] ?? 'Item') ?>
                    </span>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <div class="text-sm text-gray-500">No items selected</div>
        <?php endif; ?>
    </div>
    -->
    
    <!-- Trigger button to open handler modal -->
    <button type="button"
            class="btn btn-primary"
            @click="$dispatch('{{EVENT_NAME}}', {
                isOpen: true,
                uid: '<?= $escaper->escapeJs($uid) ?>',
                fieldName: '<?= $escaper->escapeJs($fieldName) ?>',
                fieldValue: document.getElementById('<?= $escaper->escapeJs("{$uid}_{$fieldName}") ?>').value
                <?php foreach ($attributes as $attrKey => $attrValue): ?>
                    , <?= $escaper->escapeJs($attrKey) ?>: <?= json_encode($attrValue) ?>
                <?php endforeach; ?>
            })">
        {{BUTTON_LABEL}}
    </button>
    
    <!-- Hidden input stores the field value -->
    <input type="hidden"
           id="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           value="<?= $escaper->escapeHtmlAttr($fieldValueJson) ?>"
           @change="updateWireField(
               '<?= $escaper->escapeHtmlAttr($uid) ?>',
               '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
               $event.target.value
           )"
           class="<?= $hasError ? 'error field-error' : '' ?>">
    
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
        class="validation-messages list-none"></ul>
</div>
