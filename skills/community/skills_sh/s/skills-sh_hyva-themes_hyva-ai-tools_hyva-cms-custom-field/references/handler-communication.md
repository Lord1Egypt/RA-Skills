# Field Handler Communication Protocol

This document describes the event-based communication protocol between field templates and handler modals in Hyvä CMS custom field types.

**Note:** This protocol applies only to **modal-based field handlers (Pattern C)**. Inline handlers (Pattern B) and basic fields (Pattern A) do not use this event system.

## Communication Flow

```
Field Template                Handler Modal
     |                             |
     |--- Dispatch Init Event ---->|
     |    (toggle-handler-name)    |
     |                             |
     |                        Initialize
     |                        (parse data,
     |                         open modal,
     |                         render UI)
     |                             |
     |                        User makes
     |                        selection
     |                             |
     |<--- Dispatch Save Event ----|
     |    (editor-change)          |
     |                             |
Update hidden input             Close
Trigger Magewire sync          modal
Update preview                   |
```

## Initialization Event

The field template dispatches a custom event to open the handler modal and pass initialization data.

### Event Structure

```javascript
$dispatch('toggle-handler-name', {
    isOpen: true,                // Boolean: open the modal
    uid: 'component_123',        // String: component unique ID
    fieldName: 'products',       // String: field name from component config
    fieldValue: '[]',            // String: current field value (JSON-encoded)
    // ... any additional config parameters
    maxSelected: 25,
    allowMultiple: true
})
```

### Field Template Code

```php
<button type="button"
        class="btn btn-primary"
        @click="$dispatch('toggle-product-select', {
            isOpen: true,
            uid: '<?= $escaper->escapeJs($uid) ?>',
            fieldName: '<?= $escaper->escapeJs($fieldName) ?>',
            fieldValue: document.getElementById('<?= $escaper->escapeJs("{$uid}_{$fieldName}") ?>').value,
            maxProducts: <?= (int) $maxProducts ?>
        })">
    Select Products
</button>
```

**Key points:**
- Event name should be descriptive: `toggle-{handler-name}`
- `fieldValue` is read from the hidden input element
- Pass any configuration from component attributes
- All values must be properly escaped

### Handler Modal Listener

```php
<dialog x-data="initProductSelectHandler()"
        @toggle-product-select.window="initializeModal($event.detail)">
```

**Key points:**
- Use `.window` modifier to listen to window events
- Access data via `$event.detail`
- Call initialization method to process data

### Handler Initialization Method

```javascript
initializeModal({ isOpen, uid, fieldName, fieldValue, maxProducts } = {}) {
    // Store context
    this.uid = uid;
    this.fieldName = fieldName;
    this.maxProducts = maxProducts || 10;
    
    // Parse current field value with error handling
    try {
        this.selectedProducts = JSON.parse(fieldValue || '[]');
    } catch (e) {
        console.error('Failed to parse field value:', e);
        this.selectedProducts = [];
    }
    
    // Initialize UI state
    this.searchProducts();
    this.resetFilters();
    
    // Open the modal
    this.open = isOpen;
}
```

**Key points:**
- Always use destructuring with defaults for safety
- **Always parse `fieldValue` with try/catch** - it may contain invalid JSON
- Store `uid` and `fieldName` for the save event
- Initialize UI state before opening modal
- Set `this.open` last to trigger modal display

## Save Event

The handler modal dispatches the `editor-change` event to update the field value and close the modal.

### Event Structure

```javascript
$dispatch('editor-change', {
    name: this.uid,              // String: component UID (NOT fieldName!)
    field: this.fieldName,       // String: field name (NOT name!)
    value: this.selectedData,    // Any: new field value (will be JSON-encoded)
    saveState: true              // Boolean: true triggers Magewire sync
})
```

**CRITICAL:** Note the property names:
- `name` receives the component UID (NOT the field name)
- `field` receives the field name (NOT name)

This is the correct structure. Using `fieldName` or incorrect property names will cause silent failures.

### Handler Modal Save Method

```javascript
saveProducts() {
    // Dispatch event with correct property names
    this.$dispatch('editor-change', {
        name: this.uid,              // Component UID
        field: this.fieldName,       // Field name
        value: this.selectedProducts, // Your data structure
        saveState: true
    });
    
    // Close the modal
    this.open = false;
}
```

**Key points:**
- Property names must match exactly: `name`, `field`, `value`, `saveState`
- `value` can be any JSON-serializable data structure
- Hyvä CMS automatically JSON-encodes the value when storing
- Set `saveState: true` to trigger server-side validation
- Close modal after dispatching event

## Data Encoding and Decoding

### Field Value Format

Field values in Hyvä CMS are typically stored as strings, but may be returned as arrays depending on the context:
- **Database/Storage**: Values are stored as JSON strings
- **Runtime/Rendering**: Values may be pre-decoded as arrays by Magento/Magewire
- **After editor-change event**: Values are automatically JSON-encoded

**IMPORTANT**: Always handle BOTH array and string types when retrieving field values, as the type depends on where/when the field is accessed.

**In Field Template (Display):**

```php
<?php
$fieldValue = $block->getData('value') ?? '';

// Decode for display (handle both array and JSON string)
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
?>

<!-- Display selected products -->
<?php foreach ($selectedProducts as $product): ?>
    <span><?= $escaper->escapeHtml($product['name']) ?></span>
<?php endforeach; ?>

<!-- IMPORTANT: Ensure field value is JSON string for hidden input -->
<?php
$fieldValueJson = is_array($fieldValue) ? json_encode($fieldValue) : $fieldValue;
?>
<input type="hidden" 
       id="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
       name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
       value="<?= $escaper->escapeHtmlAttr($fieldValueJson) ?>">
```

**Critical Note:** Always JSON-encode array values before outputting to hidden input `value` attribute. Using an array directly causes "Array to string conversion" errors.

**In Handler Modal (Initialize):**

```javascript
initializeModal({ fieldValue } = {}) {
    // Always parse with error handling
    try {
        this.selectedProducts = JSON.parse(fieldValue || '[]');
    } catch (e) {
        console.error('Failed to parse field value:', e);
        this.selectedProducts = [];
    }
}
```

**In Handler Modal (Save):**

```javascript
saveProducts() {
    // Hyvä CMS automatically JSON-encodes when dispatching editor-change
    this.$dispatch('editor-change', {
        name: this.uid,
        field: this.fieldName,
        value: this.selectedProducts,  // Array/Object - automatically encoded
        saveState: true
    });
}
```

**In Component PHTML Template (Render):**

```php
<?php
$products = $block->getData('products');

// Decode for rendering
$productList = [];
if ($products) {
    try {
        $productList = json_decode($products, true) ?: [];
    } catch (\Exception $e) {
        $productList = [];
    }
}
?>

<?php foreach ($productList as $product): ?>
    <div class="product">
        <h3><?= $escaper->escapeHtml($product['name']) ?></h3>
        <p><?= $escaper->escapeHtml($product['sku']) ?></p>
    </div>
<?php endforeach; ?>
```

### Data Structure Examples

**Simple Array:**

```javascript
// Save
value: ['product-1', 'product-2', 'product-3']

// Stored as
'["product-1","product-2","product-3"]'
```

**Array of Objects:**

```javascript
// Save
value: [
    { id: 1, name: 'Product 1', sku: 'SKU001' },
    { id: 2, name: 'Product 2', sku: 'SKU002' }
]

// Stored as
'[{"id":1,"name":"Product 1","sku":"SKU001"},{"id":2,"name":"Product 2","sku":"SKU002"}]'
```

**Complex Object:**

```javascript
// Save
value: {
    type: 'internal',
    url: '/page/about',
    title: 'About Us',
    target: '_self',
    attributes: {
        class: 'nav-link',
        rel: 'nofollow'
    }
}

// Stored as
'{"type":"internal","url":"/page/about","title":"About Us","target":"_self","attributes":{"class":"nav-link","rel":"nofollow"}}'
```

## Error Handling

### Invalid JSON in Field Value

Always parse with try/catch when reading field values:

```javascript
initializeModal({ fieldValue } = {}) {
    try {
        this.data = JSON.parse(fieldValue || '[]');
    } catch (e) {
        console.error('Failed to parse field value:', e);
        // Fallback to safe default
        this.data = [];
    }
}
```

### Missing Required Data

Provide defaults for all initialization parameters:

```javascript
initializeModal({ 
    isOpen = false, 
    uid = null, 
    fieldName = null, 
    fieldValue = '[]',
    maxItems = 10 
} = {}) {
    // Check required params
    if (!uid || !fieldName) {
        console.error('Missing required parameters');
        return;
    }
    
    // Continue with initialization
    this.uid = uid;
    this.fieldName = fieldName;
    // ...
}
```

### Event Dispatch Failures

If the `editor-change` event doesn't update the field:

1. **Check property names**: Must be `name`, `field`, `value`, `saveState` (not `uid`, `fieldName`, etc.)
2. **Check value serialization**: Ensure value is JSON-serializable (no circular references, functions, etc.)
3. **Check hidden input exists**: The input with `id="{uid}_{fieldName}"` must exist
4. **Check console for errors**: Look for JavaScript errors that might prevent the event

## Common Patterns

### Loading Indicator

Show loading state while fetching data:

```javascript
initializeModal({ isOpen, uid, fieldName, fieldValue } = {}) {
    this.uid = uid;
    this.fieldName = fieldName;
    this.loading = true;
    this.open = isOpen;
    
    // Parse existing selection
    try {
        this.selectedItems = JSON.parse(fieldValue || '[]');
    } catch (e) {
        this.selectedItems = [];
    }
    
    // Fetch data
    this.fetchData().finally(() => {
        this.loading = false;
    });
}
```

### Validation Before Save

Validate selection before dispatching save event:

```javascript
saveSelection() {
    // Validate
    if (this.selectedProducts.length === 0) {
        alert('Please select at least one product');
        return;
    }
    
    if (this.selectedProducts.length > this.maxProducts) {
        alert(`Maximum ${this.maxProducts} products allowed`);
        return;
    }
    
    // Save
    this.$dispatch('editor-change', {
        name: this.uid,
        field: this.fieldName,
        value: this.selectedProducts,
        saveState: true
    });
    
    this.open = false;
}
```

### Confirmation Dialog

Confirm before closing without saving:

```javascript
closeModal() {
    if (this.hasUnsavedChanges()) {
        if (!confirm('You have unsaved changes. Close anyway?')) {
            return;
        }
    }
    
    this.open = false;
}
```

### Reset State on Close

Clean up state when modal closes:

```javascript
// In Alpine component
watch: {
    open(value) {
        if (!value) {
            // Modal closed - reset state
            this.searchTerm = '';
            this.selectedItems = [];
            this.loading = false;
        }
    }
}
```

## Testing Checklist

When implementing modal-based field handlers, verify:

- [ ] Initialization event dispatches with correct event name
- [ ] Initialization event includes all required data (uid, fieldName, fieldValue)
- [ ] Handler modal listens with `.window` modifier
- [ ] Field value parsing has try/catch error handling
- [ ] Save event uses correct property names (`name`, `field`, `value`, `saveState`)
- [ ] Save event dispatches before closing modal
- [ ] Complex data structures JSON encode/decode correctly
- [ ] Field value persists after save and page refresh
- [ ] Preview updates immediately after save
- [ ] Validation errors display correctly
- [ ] Modal state resets properly on open/close

## Built-In Handler Examples

For working examples of the communication protocol, examine these built-in handlers:

### Product Handler
- **Location**: `Hyva_CmsLiveviewEditor::page/js/product-handler.phtml`
- **Event**: `toggle-product-select`
- **Data**: Array of product objects with id, name, sku, image

### Link Handler
- **Location**: `Hyva_CmsLiveviewEditor::page/js/link-handler.phtml`
- **Event**: `toggle-link-handler`
- **Data**: Object with type, url, title, target, attributes

These handlers demonstrate complete implementations of the communication protocol with robust error handling and state management.
