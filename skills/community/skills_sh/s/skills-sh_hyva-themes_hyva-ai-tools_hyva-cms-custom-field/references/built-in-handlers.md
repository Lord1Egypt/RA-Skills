# Built-In Field Handlers Reference

Hyvä CMS includes several built-in field handlers that serve as reference implementations and are available for use in custom components. These handlers demonstrate proven patterns and best practices for custom field types.

All built-in handlers are located in the Hyvä CMS Liveview Editor module:
- **Field Templates**: `Hyva_CmsLiveviewEditor::liveview/field-types/`
- **Handler Modals/Scripts**: `Hyva_CmsLiveviewEditor::page/js/`

## Handler Overview

| Handler | Type | Event Name | Use Case | Key Features |
|---------|------|------------|----------|--------------|
| Product | Modal | `toggle-product-select` | Product selection | Image grid, search, drag-and-drop ordering, active/available split |
| Link | Modal | `toggle-link-select` | Link configuration | Multi-type selection, entity pickers, inline label editing |
| Category | Modal | `toggle-category-select` | Category selection | Tree view, image support, path display, max selection limit |
| Image | Modal | `toggle-image-select` | Image/media selection | Media browser integration, image preview, alt text |
| Searchable Select | Inline (separate handler file) | N/A | Enhanced dropdown | Keyboard navigation, client-side filtering, wire:ignore |

## Product Handler

**Field Template**: `Hyva_CmsLiveviewEditor::liveview/field-types/products.phtml`  
**Handler Modal**: `Hyva_CmsLiveviewEditor::page/js/product-handler.phtml`  
**Handler Function**: `initProductSelect()`

### Overview

A modal-based handler for selecting products with visual images. Displays products in a grid with search, filtering, and a split view between selected and available products with drag-and-drop reordering using Sortable.js.

### Event Protocol

**Initialization Event** (dispatched by field template):
```javascript
$dispatch('toggle-product-select', {
    isOpen: true,
    uid: '<?= $escaper->escapeHtmlAttr($uid) ?>',
    fieldName: '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
    fieldValue: '<?= $escaper->escapeJs(json_encode($fieldValue)) ?>'  // JSON string
})
```

**Handler Initialization**:
```javascript
function initProductSelect() {
    return {
        async initializeModal({ isOpen, uid, fieldName, fieldValue } = {}) {
            const activeProducts = JSON.parse(fieldValue);  // Parse JSON string
            this.uid = uid;
            this.fieldName = fieldName;
            this.activeProducts = activeProducts || [];
            // ... initialize Sortable.js and load products
        }
    }
}
```

**Save Event** (dispatched by handler):
```javascript
$dispatch('editor-change', {
    name: this.uid,              // Component UID
    field: this.fieldName,       // Field name
    value: this.activeProducts,  // Array of product objects
    saveState: true
})
```

### Data Structure

```javascript
// Stored in field (JSON-encoded)
[
    {
        "id": 1,
        "name": "Product Name",
        "sku": "SKU001",
        "thumbnail": {
            "url": "https://example.com/image.jpg"
        }
    }
]
```

### Field Template Pattern

```php
<input type="hidden"
       value="<?= $escaper->escapeHtmlAttr(json_encode($fieldValue)) ?>"
       @change="updateWireField(
           '<?= $escaper->escapeHtmlAttr($uid) ?>',
           '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
           JSON.parse($event.target.value)  // Parse JSON from handler
       )">
```

### Key Features

1. **Image Grid Layout**: Products displayed in a grid with thumbnails
2. **Search Functionality**: Real-time debounced search by product name/SKU
3. **Active/Available Split**: Two-section layout showing selected vs available products
4. **Drag-and-Drop Ordering**: Reorder selected products with Sortable.js
5. **API Integration**: Fetches products from Magento REST API
6. **Display Summary**: Shows selected products with thumbnails in field area

### Usage Example

```json
{
    "product_carousel": {
        "label": "Product Carousel",
        "content": {
            "products": {
                "type": "products",
                "label": "Select Products"
            }
        }
    }
}
```

## Link Handler

**Field Template**: `Hyva_CmsLiveviewEditor::liveview/field-types/link.phtml`  
**Handler Modal**: `Hyva_CmsLiveviewEditor::page/js/link-handler.phtml`  
**Handler Function**: `initLinkSelect()`

### Overview

A modal-based handler for configuring links with multiple types (CMS page, category, product, custom URL, Magento page). Provides radio button selection for link types with conditional fields and searchable entity dropdowns.

### Event Protocol

**Initialization Event**:
```javascript
$dispatch('toggle-link-select', {  // Note: 'toggle-link-select' not 'toggle-link-handler'
    isOpen: true,
    uid: '<?= $escaper->escapeHtmlAttr($uid) ?>',
    fieldName: '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
    fieldValue: JSON.stringify(linkValues),  // JSON stringified object
    hideLabel: <?= $hideLabel ? 'true' : 'false' ?>  // Optional config
})
```

### Data Structure

```javascript
{
    "type": "cms_page|category|product|custom_url|magento",
    "label": "Link Text",
    "value": "page-identifier-or-id",
    "src": "/generated/url/path",  // Generated by backend
    "open_in_new_tab": false,
    "prefix": "",  // For custom_url type
    "suffix": "",
    "placeholder": ""
}
```

### Key Features

1. **Multi-Type Support**: CMS page, category, product, custom URL, Magento page
2. **Radio Button Interface**: Visual selection of link type with icons
3. **Conditional Fields**: Fields show/hide based on selected link type
4. **Entity Selectors**: Searchable dropdowns for CMS pages, categories, products
5. **Inline Label Editing**: Edit link text directly in field template
6. **Auto URL Generation**: Backend generates `src` from selected entity
7. **Copy Label Button**: Copy entity name to label field

### Field Template Pattern

```php
<div x-data="{
    linkValues: null,
    saveValue() {
        updateWireField('<?= $escaper->escapeHtmlAttr($uid) ?>', 
                       '<?= $escaper->escapeHtmlAttr($fieldName) ?>', 
                       this.linkValues);
    }
}">
    <input type="hidden"
           :value="JSON.stringify(linkValues)"
           @change="updateWireField(...)">
    
    <!-- Inline label editing -->
    <input type="text"
           x-model="linkValues.label"
           @input.debounce.500="saveValue()">
    
    <!-- Button to open handler -->
    <button @click="$dispatch('toggle-link-select', {...})">
        Select Link
    </button>
</div>
```

### Usage Example

```json
{
    "call_to_action": {
        "label": "Call to Action",
        "content": {
            "button_link": {
                "type": "link",
                "label": "Button Link",
                "config": {
                    "hide_label": false
                }
            }
        }
    }
}
```

## Category Handler

**Field Template**: `Hyva_CmsLiveviewEditor::liveview/field-types/category.phtml`  
**Handler Modal**: `Hyva_CmsLiveviewEditor::page/js/category-handler.phtml`  
**Handler Function**: `initCategorySelect()`

### Overview

A modal-based handler for selecting categories from the Magento category tree. Displays categories with optional images, hierarchical paths, and supports maximum selection limits.

### Event Protocol

**Initialization Event**:
```javascript
$dispatch('toggle-category-select', {
    isOpen: true,
    uid: '<?= $escaper->escapeHtmlAttr($uid) ?>',
    fieldName: '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
    fieldValue: '<?= $escaper->escapeJs(json_encode($fieldValue)) ?>',  // JSON string
    maxSelected: <?= $escaper->escapeHtmlAttr($maxSelected) ?>  // Optional config
})
```

### Data Structure

```javascript
[
    {
        "id": 3,
        "name": "Gear",
        "path": "Default Category/Gear",
        "image": "https://example.com/category.jpg"  // Optional
    }
]
```

### Key Features

1. **Category Tree Navigation**: Browse Magento category hierarchy
2. **Category Images**: Display category images if available
3. **Path Display**: Show full category path for context
4. **Max Selection**: Configurable limit via `config.max_selected`
5. **Search**: Filter categories by name
6. **Display Cards**: Show selected categories with image, name, ID, and path

### Usage Example

```json
{
    "category_showcase": {
        "label": "Category Showcase",
        "content": {
            "featured_categories": {
                "type": "category",
                "label": "Featured Categories",
                "config": {
                    "max_selected": 6
                }
            }
        }
    }
}
```

## Image Handler

**Field Template**: `Hyva_CmsLiveviewEditor::liveview/field-types/image.phtml`  
**Handler Modal**: `Hyva_CmsLiveviewEditor::page/js/image-handler.phtml`  
**Handler Function**: `initImageSelect()`

### Overview

A modal-based handler for selecting images from Magento media gallery. Integrates with Magento's media browser and provides image configuration options (alt text, dimensions, CSS classes).

### Event Protocol

**Initialization Event**:
```javascript
$dispatch('toggle-image-select', {
    isOpen: true,
    uid: '<?= $escaper->escapeHtmlAttr($uid) ?>',
    fieldName: '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
    fieldValue: '<?= $escaper->escapeJs(json_encode($fields)) ?>'  // JSON string
})
```

**Important: Image field uses `updateField` (not `updateWireField`)**:
```php
<input type="hidden"
       value="<?= $escaper->escapeHtmlAttr(json_encode($fields)) ?>"
       @change="updateField(  // Uses updateField, not updateWireField!
           '<?= $escaper->escapeHtmlAttr($uid) ?>',
           '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
           JSON.parse($event.target.value)
       )">
```

### Data Structure

```javascript
{
    "src": "media/image.jpg",
    "alt": "Alt text",
    "width": 1920,
    "height": 1080,
    "classes": "custom-class",
    "preview_url": "https://example.com/media/cache/image.jpg",
    "imageOptions": {
        // Additional image configuration
    }
}
```

### Key Features

1. **Media Browser Integration**: Access Magento media gallery
2. **Image Preview**: Display selected image with edit overlay
3. **Click-to-Edit**: Entire image preview is clickable button to reopen handler
4. **Alt Text**: Configure alt text for accessibility
5. **Image Options**: Configure width, height, CSS classes
6. **Cache-Busted Preview**: Timestamp appended to preview URL (`?rand=` + time)
7. **Remove Button**: Overlay trash icon to clear image

### Usage Example

```json
{
    "hero_banner": {
        "label": "Hero Banner",
        "content": {
            "background": {
                "type": "image",
                "label": "Background Image"
            }
        }
    }
}
```

## Searchable Select Handler

**Field Template**: `Hyva_CmsLiveviewEditor::liveview/field-types/searchable_select.phtml`  
**Handler Script**: `Hyva_CmsLiveviewEditor::page/js/searchable-select-handler.phtml`  
**Handler Function**: `initSearchableSelect(config)`

### Overview

An inline enhanced control that extends the standard select field with search functionality and keyboard navigation. Renders as a custom dropdown with client-side filtering.

**Important**: Unlike other handlers, the searchable select handler function is defined in a **separate script file** (not a modal), but the field template calls it inline. The field template uses `wire:ignore` to prevent Livewire conflicts.

### Implementation Pattern

**Field Template Structure**:
```php
<div class="field-container" ...>
    <input type="hidden" 
           id="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
           @change="updateWireField(...)">
    
    <div wire:ignore>  <!-- IMPORTANT: wire:ignore wrapper -->
        <div x-data="initSearchableSelect({
                uid: '<?= $escaper->escapeJs($uid) ?>',
                fieldName: '<?= $escaper->escapeJs($fieldName) ?>',
                initFieldValue: '<?= $escaper->escapeJs($fieldValue) ?>',
                options: <?= $escaper->escapeHtml(json_encode($options)) ?>
            })" 
             @click.away="close()">
            <!-- Dropdown button and menu -->
        </div>
    </div>
</div>
```

**Handler Script** (separate file in `page/js/`):
```javascript
function initSearchableSelect(config) {
    return {
        uid: config.uid,
        fieldName: config.fieldName,
        state: false,  // Dropdown open/close
        filter: '',
        list: config.options.map((item, index) => ({
            id: `${item.value}_${index}`,
            value: item.value,
            label: item.label
        })),
        selectedKey: null,
        selectedLabel: null,
        
        init() {
            // Update hidden input when selection changes
            this.$watch('selectedKey', (id) => {
                const selectedItem = this.list.find(item => item.id === id);
                const value = selectedItem ? selectedItem.value : '';
                document.getElementById(`${this.uid}_${this.fieldName}`).value = value;
                document.getElementById(`${this.uid}_${this.fieldName}`).dispatchEvent(new Event('change'));
            });
        },
        
        // Methods: toggle(), close(), select(), navigateDown(), navigateUp(), etc.
    }
}
```

### Data Structure

```javascript
// Simple string value
"option_value"
```

### Key Features

1. **Separate Handler File**: Handler function in separate script file, not inline
2. **wire:ignore**: Uses Livewire's wire:ignore to prevent state conflicts
3. **Direct DOM Manipulation**: Updates hidden input via vanilla JS and dispatches change
4. **Search Filtering**: Client-side filtering through options
5. **Keyboard Navigation**: Arrow keys, Enter, Escape with focus management and scroll-into-view
6. **Click Outside**: Closes dropdown when clicking outside
7. **Accessibility**: ARIA attributes (listbox, option, selected, controls)
8. **Alpine $watch**: Watches selection and updates hidden input

### Usage Example

```json
{
    "custom_component": {
        "label": "Custom Component",
        "content": {
            "style": {
                "type": "searchable_select",
                "label": "Style Variant",
                "options": [
                    { "value": "default", "label": "Default" },
                    { "value": "primary", "label": "Primary Blue" },
                    { "value": "secondary", "label": "Secondary Gray" }
                ]
            }
        }
    }
}
```

## Using Built-In Handlers in Custom Components

Built-in handlers can be used directly in custom components by specifying the appropriate field type.

### Product Handler

```json
{
    "products": {
        "type": "products",
        "label": "Select Products"
    }
}
```

### Link Handler

```json
{
    "link": {
        "type": "link",
        "label": "Button Link",
        "config": {
            "hide_label": false
        }
    }
}
```

### Category Handler

```json
{
    "categories": {
        "type": "category",
        "label": "Select Categories",
        "config": {
            "max_selected": 10
        }
    }
}
```

### Image Handler

```json
{
    "image": {
        "type": "image",
        "label": "Hero Image"
    }
}
```

### Searchable Select

```json
{
    "variant": {
        "type": "searchable_select",
        "label": "Variant",
        "options": [
            { "value": "a", "label": "Option A" },
            { "value": "b", "label": "Option B" }
        ]
    }
}
```

## Key Implementation Patterns

### Event Naming Convention

All modal-based handlers follow the pattern `toggle-{type}-select`:
- `toggle-product-select`
- `toggle-link-select`
- `toggle-category-select`
- `toggle-image-select`

### Handler Function Naming

Handler functions follow the pattern `init{Type}Select()`:
- `initProductSelect()`
- `initLinkSelect()`
- `initCategorySelect()`
- `initImageSelect()`
- `initSearchableSelect(config)` (takes config parameter)

### updateField vs updateWireField

**Use `updateWireField`** (most handlers):
- Products, Link, Category handlers
- Triggers server-side validation immediately
- Sends value to server via Magewire

**Use `updateField`** (specialized cases):
- Image handler
- Color, Range handlers (with debounce)
- Updates preview without server round-trip
- Value persists locally until save

### JSON Encoding Pattern

All complex data (arrays, objects) is JSON-encoded in field values:

**In Field Template**:
```php
value="<?= $escaper->escapeHtmlAttr(json_encode($fieldValue)) ?>"
```

**In Handler Initialization**:
```javascript
const data = JSON.parse(fieldValue);
```

**In @change Handler**:
```php
@change="updateWireField(..., JSON.parse($event.target.value))"
```

### wire:ignore Usage

Use `wire:ignore` when Alpine.js components need to persist without Livewire interference:

```php
<div wire:ignore>
    <div x-data="initSearchableSelect(...)">
        <!-- Alpine component -->
    </div>
</div>
```

## Examining Built-In Handler Code

To study built-in handler implementations:

**Field Templates**:
```bash
# From Magento root
ls vendor/hyva-themes/magento2-hyva-cms-liveview-editor/view/adminhtml/templates/liveview/field-types/
```

**Handler Modals/Scripts**:
```bash
# From Magento root
ls vendor/hyva-themes/magento2-hyva-cms-liveview-editor/view/adminhtml/templates/page/js/
```

Example: Viewing the product handler
```bash
cat vendor/hyva-themes/magento2-hyva-cms-liveview-editor/view/adminhtml/templates/page/js/product-handler.phtml
```

## Key Takeaways

1. **Event Names**: Use `toggle-{type}-select` pattern (not `toggle-{type}-handler`)
2. **Handler Functions**: Use `init{Type}Select()` naming pattern
3. **JSON Encoding**: Always JSON-encode/decode complex field values
4. **updateWireField vs updateField**: Most use `updateWireField`, image uses `updateField`
5. **Separate Handler Files**: Modal handlers in `page/js/`, searchable select also separated
6. **wire:ignore**: Use for Alpine components to prevent Livewire conflicts
7. **Icons View Model**: Use `Hyva\CmsLiveviewEditor\ViewModel\Icons` for UI icons
8. **Direct DOM Manipulation**: Searchable select updates hidden input directly
9. **Sortable.js**: Product handler uses Sortable.js for drag-and-drop
10. **Copy Patterns**: Start with built-in handlers as templates for custom handlers
