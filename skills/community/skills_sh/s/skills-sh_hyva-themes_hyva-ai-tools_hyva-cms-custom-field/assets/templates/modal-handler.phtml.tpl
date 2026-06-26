<?php
/**
 * Modal-Based Field Handler - Handler Modal Template
 * 
 * Use this template for the modal part of a modal-based handler.
 * This template is registered in layout XML and rendered once on the page.
 * 
 * Replace placeholders:
 * - {{EVENT_NAME}} - Event name to listen for (e.g., toggle-product-select)
 * - {{HANDLER_NAME}} - Alpine.js component function name (e.g., initProductSelectHandler)
 * - {{MODAL_TITLE}} - Dialog header text
 * - {{SELECTION_UI}} - Your selection interface HTML
 * - {{SAVE_LOGIC}} - Additional logic in save method (optional)
 */

declare(strict_types=1);

use Magento\Backend\Block\Template;
use Magento\Framework\Escaper;

/** @var Template $block */
/** @var Escaper $escaper */
?>

<!-- IMPORTANT: Use 'open:flex' NOT 'flex' to prevent modal from always displaying -->
<dialog class="max-w-screen-xl w-screen bg-white shadow-xl rounded-lg open:flex flex-col"
        style="max-height: 90vh;"
        x-data="{{HANDLER_NAME}}()"
        x-htmldialog="open = false"
        closeby="any"
        x-show="open"
        x-transition
        @{{EVENT_NAME}}.window="initializeModal($event.detail)">
    
    <!-- Header -->
    <div class="p-4 border-b flex items-center justify-between">
        <h2 class="text-xl font-semibold"><?= $escaper->escapeHtml(__('{{MODAL_TITLE}}')) ?></h2>
        <button type="button" @click="open = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    </div>
    
    <!-- Search/Filters (optional) -->
    <div class="p-4 border-b">
        <input type="text"
               x-model="searchTerm"
               @input.debounce.300ms="search()"
               placeholder="Search..."
               class="w-full px-4 py-2 border rounded-md">
    </div>
    
    <!-- Content Area -->
    <div class="flex-1 overflow-y-auto p-4">
        {{SELECTION_UI}}
        <!-- Example: Grid of items
        <div class="grid grid-cols-3 gap-4">
            <template x-for="item in items" :key="item.id">
                <div class="border rounded-lg p-4 cursor-pointer"
                     :class="{ 'border-blue-500 bg-blue-50': isSelected(item.id) }"
                     @click="toggleItem(item)">
                    <h3 x-text="item.name"></h3>
                </div>
            </template>
        </div>
        
        <div x-show="items.length === 0" class="text-center py-8 text-gray-500">
            No items found
        </div>
        -->
    </div>
    
    <!-- Footer -->
    <div class="p-4 border-t flex items-center justify-between">
        <div class="text-sm text-gray-600">
            <span x-text="selectedItems.length"></span> selected
        </div>
        <div class="flex gap-4">
            <button type="button" 
                    class="btn" 
                    @click="open = false">
                <?= $escaper->escapeHtml(__('Cancel')) ?>
            </button>
            <button type="button" 
                    class="btn btn-primary" 
                    @click="saveSelection()">
                <?= $escaper->escapeHtml(__('Save')) ?>
            </button>
        </div>
    </div>
</dialog>

<script>
function {{HANDLER_NAME}}() {
    return {
        open: false,
        uid: null,
        fieldName: null,
        searchTerm: '',
        items: [],
        selectedItems: [],
        
        /**
         * Initialize modal when field template dispatches event
         */
        initializeModal({ isOpen, uid, fieldName, fieldValue } = {}) {
            // Store context
            this.uid = uid;
            this.fieldName = fieldName;
            
            // Parse current field value with error handling
            try {
                this.selectedItems = JSON.parse(fieldValue || '[]');
            } catch (e) {
                console.error('Failed to parse field value:', e);
                this.selectedItems = [];
            }
            
            // Load/initialize data
            this.loadItems();
            
            // Open the modal
            this.open = isOpen;
        },
        
        /**
         * Load items (replace with real API call)
         */
        async loadItems() {
            // Example: Fetch from Magento API
            // const response = await fetch('/rest/V1/your-endpoint');
            // this.items = await response.json();
            
            // Mock data for demonstration
            this.items = [];
        },
        
        /**
         * Search/filter items
         */
        search() {
            // Implement search logic
            this.loadItems();
        },
        
        /**
         * Check if item is selected
         */
        isSelected(itemId) {
            return this.selectedItems.some(item => item.id === itemId);
        },
        
        /**
         * Toggle item selection
         */
        toggleItem(item) {
            const index = this.selectedItems.findIndex(i => i.id === item.id);
            
            if (index >= 0) {
                this.selectedItems.splice(index, 1);
            } else {
                this.selectedItems.push(item);
            }
        },
        
        /**
         * Save selection and close modal
         */
        saveSelection() {
            {{SAVE_LOGIC}}
            // Optional: Add validation here
            // if (this.selectedItems.length === 0) {
            //     alert('Please select at least one item');
            //     return;
            // }
            
            // Dispatch editor-change event with correct property names
            this.$dispatch('editor-change', {
                name: this.uid,              // IMPORTANT: use 'name' for component UID
                field: this.fieldName,       // IMPORTANT: use 'field' for field name
                value: this.selectedItems,   // Your data structure (automatically JSON-encoded)
                saveState: true              // Triggers Magewire sync and validation
            });
            
            // Close modal
            this.open = false;
        }
    }
}
</script>
