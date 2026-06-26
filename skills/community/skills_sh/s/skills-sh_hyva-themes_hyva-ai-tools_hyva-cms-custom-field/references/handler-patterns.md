# Field Handler Implementation Patterns

This document describes the three implementation patterns for custom field types in Hyvä CMS, with complete code examples and guidance on when to use each pattern.

## Important Implementation Notes

Based on analysis of built-in Hyvä CMS handlers:

1. **Event Naming**: Modal handlers use `toggle-{type}-select` pattern (e.g., `toggle-product-select`, `toggle-link-select`, NOT `toggle-{type}-handler`)
2. **Handler Functions**: Use `init{Type}Select()` pattern (e.g., `initProductSelect()`, `initLinkSelect()`)
3. **updateField vs updateWireField**:
   - **Most handlers**: Use `updateWireField` (products, link, category) - triggers immediate server validation
   - **Image handler**: Uses `updateField` - defers validation until save
   - **Debounced inputs**: Use `updateField` with `@input.debounce` (color, range)
4. **JSON Encoding**: All complex data must be JSON-encoded in hidden inputs and parsed in handlers
5. **wire:ignore**: Searchable select uses `wire:ignore` wrapper to prevent Livewire conflicts
6. **Separate Handler Files**: Even "inline" handlers like searchable select have handler functions in separate files in `page/js/`
7. **Icons View Model**: Use `Hyva\CmsLiveviewEditor\ViewModel\Icons` for UI icons (trash, pencil, etc.)

See `references/built-in-handlers.md` for complete examples from the actual codebase.

## Pattern Decision Tree

```
Do you need custom UI beyond standard HTML inputs?
├─ NO  → Use built-in field types (text, select, etc.)
└─ YES → Do you need a separate dialog/modal?
    ├─ NO  → Does it fit in the field area?
    │   ├─ YES → Pattern B: Inline Field Handler
    │   └─ NO  → Pattern C: Modal-Based Handler
    └─ YES → Pattern C: Modal-Based Handler
```

## Pattern A: Basic Custom Field Type

**Use when:**
- Custom HTML5 validation patterns
- Specialized input controls (date range, slider, color input)
- Simple enhancements to standard inputs
- No complex UI interactions needed

**Characteristics:**
- Single template file
- No Alpine.js components (or minimal Alpine for state)
- Direct input elements
- Standard field value updates

### Complete Example: Date Range Field

```php
<?php
// view/adminhtml/templates/field-types/date-range.phtml
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

$fieldTypes = $viewModels->require(FieldTypes::class);

$uid = (string) $block->getData('uid');
$fieldName = (string) $block->getData('name');
$fieldValue = $block->getData('value') ?? '';

// Parse stored value (format: "2024-01-01,2024-12-31")
$dates = $fieldValue ? explode(',', $fieldValue) : ['', ''];
$startDate = $dates[0] ?? '';
$endDate = $dates[1] ?? '';

$attributes = (array) $block->getData('attributes') ?? [];
$filteredAttributes = $fieldTypes->getDefinedFieldAttributes($attributes);

$hasError = isset($magewire->errors[$uid][$fieldName]);
?>

<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
    <div class="flex gap-4 items-center" x-data="{ startDate: '<?= $escaper->escapeJs($startDate) ?>', endDate: '<?= $escaper->escapeJs($endDate) ?>' }">
        <div>
            <label class="block text-sm mb-1">Start Date</label>
            <input type="date"
                   x-model="startDate"
                   @change="updateWireField(
                       '<?= $escaper->escapeHtmlAttr($uid) ?>',
                       '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
                       startDate + ',' + endDate
                   )"
                   class="form-input"
                   <?php foreach ($filteredAttributes as $attr => $attrValue): ?>
                       <?= $escaper->escapeHtmlAttr($attr) ?>="<?= $escaper->escapeHtmlAttr($attrValue) ?>"
                   <?php endforeach; ?>>
        </div>
        
        <span class="mt-6">to</span>
        
        <div>
            <label class="block text-sm mb-1">End Date</label>
            <input type="date"
                   x-model="endDate"
                   @change="updateWireField(
                       '<?= $escaper->escapeHtmlAttr($uid) ?>',
                       '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
                       startDate + ',' + endDate
                   )"
                   class="form-input"
                   <?php foreach ($filteredAttributes as $attr => $attrValue): ?>
                       <?= $escaper->escapeHtmlAttr($attr) ?>="<?= $escaper->escapeHtmlAttr($attrValue) ?>"
                   <?php endforeach; ?>>
        </div>
    </div>
    
    <!-- Hidden input for field name requirement -->
    <input type="hidden" 
           name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           value="<?= $escaper->escapeHtmlAttr($fieldValue) ?>">
    
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
        class="validation-messages list-none"></ul>
</div>
```

**Registration in di.xml:**

```xml
<type name="Hyva\CmsLiveviewEditor\Model\CustomField">
    <arguments>
        <argument name="customTypes" xsi:type="array">
            <item name="date_range" xsi:type="string">
                Vendor_Module::field-types/date-range.phtml
            </item>
        </argument>
    </arguments>
</type>
```

**Usage in components.json:**

```json
{
    "event_card": {
        "label": "Event Card",
        "content": {
            "event_dates": {
                "type": "custom_type",
                "custom_type": "date_range",
                "label": "Event Dates",
                "attributes": {
                    "required": true
                }
            }
        }
    }
}
```

## Pattern B: Inline Field Handler

**Use when:**
- Enhanced UI that fits in field area
- Searchable/filterable dropdowns
- Color pickers with swatches
- Inline toggles or button groups
- Progressive disclosure UI

**Characteristics:**
- Single template file with Alpine.js component
- Enhanced UI rendered inline
- No separate modal
- State managed within Alpine component
- No layout XML registration needed

### Complete Example: Searchable Select Handler

```php
<?php
// view/adminhtml/templates/field-types/searchable-select.phtml
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

// Get selected option label
$selectedLabel = '';
foreach ($options as $option) {
    if ($option['value'] === $fieldValue) {
        $selectedLabel = $option['label'];
        break;
    }
}
?>

<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
    <div x-data="searchableSelectHandler(
            '<?= $escaper->escapeJs($uid) ?>',
            '<?= $escaper->escapeJs($fieldName) ?>',
            '<?= $escaper->escapeJs($fieldValue) ?>',
            <?= $escaper->escapeHtmlAttr(json_encode($options)) ?>
        )"
         x-on:click.outside="open = false"
         class="relative">
        
        <!-- Display button -->
        <button type="button"
                @click="open = !open"
                class="w-full flex items-center justify-between px-3 py-2 border rounded-md bg-white <?= $hasError ? 'border-red-500' : 'border-gray-300' ?>">
            <span x-text="selectedLabel || 'Select an option'"></span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        </button>
        
        <!-- Dropdown -->
        <div x-show="open"
             x-transition
             class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
            
            <!-- Search input -->
            <div class="p-2 border-b">
                <input type="text"
                       x-model="search"
                       @input="filterOptions()"
                       placeholder="Search..."
                       class="w-full px-3 py-2 border rounded-md">
            </div>
            
            <!-- Options list -->
            <div class="py-1">
                <template x-for="option in filteredOptions" :key="option.value">
                    <button type="button"
                            @click="selectOption(option)"
                            class="w-full text-left px-4 py-2 hover:bg-gray-100"
                            :class="{ 'bg-blue-50': selectedValue === option.value }">
                        <span x-text="option.label"></span>
                    </button>
                </template>
                
                <div x-show="filteredOptions.length === 0" class="px-4 py-2 text-gray-500">
                    No options found
                </div>
            </div>
        </div>
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
function searchableSelectHandler(uid, fieldName, initialValue, options) {
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
            
            // Update field value
            updateWireField(uid, fieldName, option.value);
        },
        
        updateSelectedLabel() {
            const selected = this.allOptions.find(o => o.value === this.selectedValue);
            this.selectedLabel = selected ? selected.label : '';
        }
    }
}
</script>
```

**Registration (same as Pattern A):**

```xml
<type name="Hyva\CmsLiveviewEditor\Model\CustomField">
    <arguments>
        <argument name="customTypes" xsi:type="array">
            <item name="searchable_select" xsi:type="string">
                Vendor_Module::field-types/searchable-select.phtml
            </item>
        </argument>
    </arguments>
</type>
```

## Pattern C: Modal-Based Field Handler

**Use when:**
- Complex selection interfaces requiring more space
- Product/category selectors with images
- Multi-step data entry workflows
- Link builders with multiple options
- Media galleries or file browsers
- Any UI that benefits from a dedicated modal

**Characteristics:**
- Two template files: field template + handler modal
- Field template: trigger button + hidden input
- Handler modal: separate dialog with full UI
- Layout XML registration required
- Event-based communication

### Complete Example: Product Selector Handler

**Step 1: Field Template**

```php
<?php
// view/adminhtml/templates/field-types/product-selector.phtml
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

$hasError = isset($magewire->errors[$uid][$fieldName]);

// Parse selected products (handle both array and JSON string)
$selectedProducts = [];
if ($fieldValue) {
    if (is_array($fieldValue)) {
        $selectedProducts = $fieldValue;
    } elseif (is_string($fieldValue)) {
        try {
            $decoded = json_decode($fieldValue, true);
            if (is_array($decoded)) {
                $selectedProducts = $decoded;
            }
        } catch (\Exception $e) {
            // Keep default empty array
        }
    }
}

$maxProducts = (int) ($block->getData('attributes')['max_products'] ?? 10);

// Ensure field value is always a JSON string for the hidden input
$fieldValueJson = is_array($fieldValue) ? json_encode($fieldValue) : $fieldValue;
?>

<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
    <!-- Display selected products -->
    <div class="mb-2">
        <?php if (!empty($selectedProducts)): ?>
            <div class="text-sm text-gray-600">
                Selected: <?= count($selectedProducts) ?> product<?= count($selectedProducts) > 1 ? 's' : '' ?>
            </div>
            <div class="flex flex-wrap gap-2 mt-2">
                <?php foreach ($selectedProducts as $product): ?>
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800">
                        <?= $escaper->escapeHtml($product['name'] ?? 'Product #' . ($product['id'] ?? '')) ?>
                    </span>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <div class="text-sm text-gray-500">No products selected</div>
        <?php endif; ?>
    </div>
    
    <!-- Trigger button -->
    <button type="button"
            class="btn btn-primary"
            @click="$dispatch('toggle-product-select', {
                isOpen: true,
                uid: '<?= $escaper->escapeJs($uid) ?>',
                fieldName: '<?= $escaper->escapeJs($fieldName) ?>',
                fieldValue: document.getElementById('<?= $escaper->escapeJs("{$uid}_{$fieldName}") ?>').value,
                maxProducts: <?= (int) $maxProducts ?>
            })">
        <?= $escaper->escapeHtml(__('Select Products')) ?>
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
```

**Step 2: Handler Modal Template**

```php
<?php
// view/adminhtml/templates/handlers/product-selector-handler.phtml
declare(strict_types=1);

use Magento\Backend\Block\Template;
use Magento\Framework\Escaper;

/** @var Template $block */
/** @var Escaper $escaper */
?>

<dialog class="max-w-screen-xl w-screen bg-white shadow-xl rounded-lg open:flex flex-col"
        style="max-height: 90vh;"
        x-data="initProductSelectHandler()"
        x-htmldialog="open = false"
        closeby="any"
        x-show="open"
        x-transition
        @toggle-product-select.window="initializeModal($event.detail)">
    
    <!-- Header -->
    <div class="p-4 border-b flex items-center justify-between">
        <h2 class="text-xl font-semibold"><?= $escaper->escapeHtml(__('Select Products')) ?></h2>
        <button type="button" @click="open = false" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    </div>
    
    <!-- Search and filters -->
    <div class="p-4 border-b">
        <input type="text"
               x-model="searchTerm"
               @input.debounce.300ms="searchProducts()"
               placeholder="Search products..."
               class="w-full px-4 py-2 border rounded-md">
    </div>
    
    <!-- Product grid -->
    <div class="flex-1 overflow-y-auto p-4">
        <div class="grid grid-cols-3 gap-4">
            <template x-for="product in availableProducts" :key="product.id">
                <div class="border rounded-lg p-4 cursor-pointer hover:border-blue-500"
                     :class="{ 'border-blue-500 bg-blue-50': isSelected(product.id) }"
                     @click="toggleProduct(product)">
                    <img :src="product.image" 
                         :alt="product.name"
                         class="w-full h-32 object-cover rounded mb-2">
                    <h3 class="font-medium text-sm" x-text="product.name"></h3>
                    <p class="text-xs text-gray-500" x-text="product.sku"></p>
                </div>
            </template>
        </div>
        
        <div x-show="availableProducts.length === 0" class="text-center py-8 text-gray-500">
            <?= $escaper->escapeHtml(__('No products found')) ?>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="p-4 border-t flex items-center justify-between">
        <div class="text-sm text-gray-600">
            <span x-text="selectedProducts.length"></span> / 
            <span x-text="maxProducts"></span> selected
        </div>
        <div class="flex gap-4">
            <button type="button" 
                    class="btn" 
                    @click="open = false">
                <?= $escaper->escapeHtml(__('Cancel')) ?>
            </button>
            <button type="button" 
                    class="btn btn-primary" 
                    @click="saveProducts()">
                <?= $escaper->escapeHtml(__('Save Selection')) ?>
            </button>
        </div>
    </div>
</dialog>

<script>
function initProductSelectHandler() {
    return {
        open: false,
        uid: null,
        fieldName: null,
        maxProducts: 10,
        searchTerm: '',
        selectedProducts: [],
        availableProducts: [],
        
        // Initialize modal when field template dispatches event
        initializeModal({ isOpen, uid, fieldName, fieldValue, maxProducts } = {}) {
            this.uid = uid;
            this.fieldName = fieldName;
            this.maxProducts = maxProducts || 10;
            
            // Parse current selection
            try {
                this.selectedProducts = JSON.parse(fieldValue || '[]');
            } catch (e) {
                this.selectedProducts = [];
            }
            
            // Load products
            this.searchProducts();
            
            // Open modal
            this.open = isOpen;
        },
        
        // Search/load products (mock implementation - replace with real API call)
        async searchProducts() {
            // In real implementation, fetch from Magento API:
            // const response = await fetch(`/rest/V1/products?searchCriteria[filterGroups][0][filters][0][field]=name&searchCriteria[filterGroups][0][filters][0][value]=${this.searchTerm}`);
            
            // Mock data for demonstration
            this.availableProducts = [
                { id: 1, name: 'Product 1', sku: 'SKU001', image: 'https://via.placeholder.com/150' },
                { id: 2, name: 'Product 2', sku: 'SKU002', image: 'https://via.placeholder.com/150' },
                { id: 3, name: 'Product 3', sku: 'SKU003', image: 'https://via.placeholder.com/150' },
            ].filter(p => p.name.toLowerCase().includes(this.searchTerm.toLowerCase()));
        },
        
        // Check if product is selected
        isSelected(productId) {
            return this.selectedProducts.some(p => p.id === productId);
        },
        
        // Toggle product selection
        toggleProduct(product) {
            const index = this.selectedProducts.findIndex(p => p.id === product.id);
            
            if (index >= 0) {
                // Remove product
                this.selectedProducts.splice(index, 1);
            } else if (this.selectedProducts.length < this.maxProducts) {
                // Add product
                this.selectedProducts.push(product);
            }
        },
        
        // Save selection and dispatch editor-change event
        saveProducts() {
            // Dispatch event to update field value
            this.$dispatch('editor-change', {
                name: this.uid,              // IMPORTANT: use 'name' not 'uid'
                field: this.fieldName,       // IMPORTANT: use 'field' not 'fieldName'
                value: this.selectedProducts,
                saveState: true
            });
            
            this.open = false;
        }
    }
}
</script>
```

**Step 3: Register Field Type**

```xml
<!-- etc/adminhtml/di.xml -->
<type name="Hyva\CmsLiveviewEditor\Model\CustomField">
    <arguments>
        <argument name="customTypes" xsi:type="array">
            <item name="product_selector" xsi:type="string">
                Vendor_Module::field-types/product-selector.phtml
            </item>
        </argument>
    </arguments>
</type>
```

**Step 4: Register Handler Modal**

```xml
<!-- view/adminhtml/layout/liveview_editor.xml -->
<?xml version="1.0"?>
<page xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="urn:magento:framework:View/Layout/etc/page_configuration.xsd">
    <body>
        <referenceContainer name="before.body.end">
            <block name="product_selector_handler"
                   template="Vendor_Module::handlers/product-selector-handler.phtml"/>
        </referenceContainer>
    </body>
</page>
```

**Usage in components.json:**

```json
{
    "product_showcase": {
        "label": "Product Showcase",
        "content": {
            "featured_products": {
                "type": "custom_type",
                "custom_type": "product_selector",
                "label": "Featured Products",
                "attributes": {
                    "max_products": 6,
                    "required": true
                }
            }
        }
    }
}
```

## Pattern Comparison

| Aspect | Basic Field | Inline Handler | Modal Handler |
|--------|-------------|----------------|---------------|
| **Template Files** | 1 (field) | 1 (field) | 2 (field + modal) |
| **Layout XML** | No | No | Yes |
| **Alpine.js** | Optional | Yes | Yes |
| **Event Communication** | No | No | Yes |
| **UI Complexity** | Low | Medium | High |
| **Screen Space** | Field area | Field area + dropdown | Full modal |
| **Best For** | Validation, simple inputs | Enhanced dropdowns, pickers | Complex selection, galleries |

## Choosing the Right Pattern

1. **Start simple**: Can you use Pattern A (basic field)? If yes, use it.
2. **Need enhancement?**: Does it fit inline (Pattern B)? Use inline handler.
3. **Need space?**: Use Pattern C (modal handler) only when necessary.

The more complex patterns require more code and maintenance, so always use the simplest pattern that meets your needs.
