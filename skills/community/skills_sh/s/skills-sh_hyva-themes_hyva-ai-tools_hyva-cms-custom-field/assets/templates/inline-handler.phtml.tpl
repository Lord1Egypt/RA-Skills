<?php
/**
 * Inline Field Handler Template
 * 
 * Use this template for enhanced controls that remain in the field area
 * (searchable dropdowns, color pickers, inline selectors).
 * 
 * Replace placeholders:
 * - {{HANDLER_NAME}} - Alpine.js component function name (e.g., searchableSelectHandler)
 * - {{HANDLER_UI}} - Your enhanced control HTML
 * - {{HANDLER_LOGIC}} - Alpine.js component implementation
 */

declare(strict_types=1);

use Magento\Backend\Block\Template;
use Magento\Framework\Escaper;
use Hyva\CmsLiveviewEditor\Magewire\LiveviewComposer;
use Hyva\Theme\Model\ViewModelRegistry;

/** @var Template $block */
/** @var Escaper $escaper */
/** @var LiveviewComposer $magewire */
/** @var ViewModelRegistry $viewModels */

$uid = (string) $block->getData('uid');
$fieldName = (string) $block->getData('name');
$fieldValue = $block->getData('value') ?? '';
$options = (array) $block->getData('options');

$hasError = isset($magewire->errors[$uid][$fieldName]);
?>

<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
    <div x-data="{{HANDLER_NAME}}(
            '<?= $escaper->escapeJs($uid) ?>',
            '<?= $escaper->escapeJs($fieldName) ?>',
            '<?= $escaper->escapeJs($fieldValue) ?>',
            <?= $escaper->escapeHtmlAttr(json_encode($options)) ?>
        )"
         x-on:click.outside="open = false"
         class="relative">
        
        {{HANDLER_UI}}
        <!-- Example: Searchable dropdown
        <button type="button"
                @click="open = !open"
                class="w-full flex items-center justify-between px-3 py-2 border rounded-md">
            <span x-text="selectedLabel || 'Select...'"></span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        </button>
        
        <div x-show="open" x-transition class="absolute z-50 w-full mt-1 bg-white border rounded-md shadow-lg">
            <input type="text"
                   x-model="search"
                   @input="filterOptions()"
                   placeholder="Search..."
                   class="w-full px-3 py-2 border-b">
            
            <div class="max-h-60 overflow-auto">
                <template x-for="option in filteredOptions" :key="option.value">
                    <button type="button"
                            @click="selectOption(option)"
                            class="w-full text-left px-4 py-2 hover:bg-gray-100">
                        <span x-text="option.label"></span>
                    </button>
                </template>
            </div>
        </div>
        -->
    </div>
    
    <!-- Hidden input for field name requirement -->
    <input type="hidden" 
           id="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           value="<?= $escaper->escapeHtmlAttr($fieldValue) ?>">
    
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
        class="validation-messages list-none"></ul>
</div>

<script>
{{HANDLER_LOGIC}}
/* Example: Searchable select component
function {{HANDLER_NAME}}(uid, fieldName, initialValue, options) {
    return {
        open: false,
        search: '',
        selectedValue: initialValue,
        selectedLabel: '',
        allOptions: options,
        filteredOptions: options,
        
        init() {
            this.updateSelectedLabel();
        },
        
        filterOptions() {
            const searchLower = this.search.toLowerCase();
            this.filteredOptions = this.allOptions.filter(option => 
                option.label.toLowerCase().includes(searchLower)
            );
        },
        
        selectOption(option) {
            this.selectedValue = option.value;
            this.selectedLabel = option.label;
            this.open = false;
            this.search = '';
            this.filteredOptions = this.allOptions;
            
            // Update field value using global function
            updateWireField(uid, fieldName, option.value);
        },
        
        updateSelectedLabel() {
            const selected = this.allOptions.find(o => o.value === this.selectedValue);
            this.selectedLabel = selected ? selected.label : '';
        }
    }
}
*/
</script>
