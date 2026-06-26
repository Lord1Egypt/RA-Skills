# Custom Field Type Template Requirements

This document describes the required markup patterns and elements for custom field type templates in Hyvä CMS.

## Required Template Structure

Every custom field type template must include specific elements and follow naming patterns to integrate properly with the Hyvä CMS editor's validation, preview updates, and error handling.

## Template Variables

All custom field type templates receive these variables from the CMS editor:

```php
// Component and field identifiers
$uid = (string) $block->getData('uid');           // Component unique ID
$fieldName = (string) $block->getData('name');    // Field name from components.json
$fieldValue = $block->getData('value') ?? '';     // Current field value (use ?? for null safety)

// Field configuration
$options = (array) $block->getData('options');     // Options array (for select-like fields)
$attributes = (array) $block->getData('attributes') ?? [];  // HTML attributes from components.json

// Validation state
$hasError = isset($magewire->errors[$uid][$fieldName]);     // Does field have validation error?
$errorMessage = $hasError ? $magewire->errors[$uid][$fieldName] : '';  // Error message text
```

## Required Template Elements

### 1. Field Container Element

The root element must be a `div` with class `field-container` and a specific ID format:

```php
<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
```

**Requirements:**
- **ID format**: Must be exactly `field-container-{uid}_{fieldName}`
- **data-error attribute**: Must be present when `$hasError` is true
- Both are required for validation highlighting and error styling

### 2. Input Element Name Attribute

All input elements must have a name attribute following this pattern:

```php
<input type="text"
       name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
       value="<?= $escaper->escapeHtmlAttr($fieldValue) ?>">
```

**Requirements:**
- **Name format**: Must be exactly `{uid}_{fieldName}`
- Required for:
  - Frontend HTML5 validation
  - Editor's click-to-focus feature (clicking field value in preview focuses the input)

### 3. Validation Messages Container

Include an element to display validation error messages:

```php
<ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
    class="validation-messages list-none">
    <?php if ($hasError): ?>
        <li class="error-message text-red-600 text-sm mt-1">
            <?= $escaper->escapeHtml($errorMessage) ?>
        </li>
    <?php endif; ?>
</ul>
```

**Requirements:**
- **ID format**: Must be exactly `validation-messages-{uid}_{fieldName}`
- Hyvä CMS injects error messages into this container

**Custom validation message location:**

If you need validation messages elsewhere in the template, add a `data-validation-messages-selector` attribute to the field container:

```php
<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
     data-validation-messages-selector="#my-custom-error-location"
     <?= $hasError ? 'data-error' : '' ?>>
```

Then create the custom location with any ID or class you want:

```php
<div id="my-custom-error-location" class="validation-messages"></div>
```

### 4. Field Value Update Methods

Hyvä CMS provides two Alpine.js methods for updating field values:

#### updateWireField (Recommended Default)

```php
<input type="text"
       @change="updateWireField(
           '<?= $escaper->escapeHtmlAttr($uid) ?>',
           '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
           $event.target.value
       )">
```

**Behavior:**
- Updates preview immediately
- Sends value to server via Magewire
- Triggers server-side validation on every change
- Keeps component state synchronized

**Use when:** Default choice for most fields

#### updateField (Specialized Use)

```php
<input type="text"
       @input="updateField(
           '<?= $escaper->escapeHtmlAttr($uid) ?>',
           '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
           $event.target.value
       )">
```

**Behavior:**
- Updates preview immediately via AJAX
- Does NOT send to server until save
- Stores value in local state
- No server-side validation until save

**Use when:** Implementing debounced inputs or need to minimize server requests for performance

#### Important Limitation

If you add custom Alpine.js components to your field template, you CANNOT set field values through `updateField` or `updateWireField` from within your Alpine component.

**Solution:** Keep input fields outside your Alpine component and update them with vanilla JavaScript:

```php
<div x-data="myCustomComponent()">
    <!-- Your Alpine component UI -->
    <button @click="selectValue('foo')">Select Foo</button>
</div>

<!-- Input OUTSIDE the Alpine component -->
<input type="hidden" 
       id="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
       name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
       value="<?= $escaper->escapeHtmlAttr($fieldValue) ?>">

<script>
function myCustomComponent() {
    return {
        selectValue(value) {
            // Update the input with vanilla JS
            const input = document.getElementById('<?= $escaper->escapeJs("{$uid}_{$fieldName}") ?>');
            input.value = value;
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
}
</script>
```

## Field Attributes and HTML5 Validation

The `FieldTypes` view model provides a method to filter component configuration attributes:

```php
use Hyva\CmsLiveviewEditor\ViewModel\Adminhtml\FieldTypes;

/** @var FieldTypes $fieldTypes */
$fieldTypes = $viewModels->require(FieldTypes::class);

$attributes = (array) $block->getData('attributes') ?? [];
$filteredAttributes = $fieldTypes->getDefinedFieldAttributes($attributes);
```

**What gets filtered:**
- Keeps: `pattern`, `required`, `minlength`, `maxlength`, `min`, `max`, `step`, etc.
- Removes: `class`, `comment`, and other non-validation attributes

**Apply to input elements:**

```php
<input type="text"
       name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
       <?php foreach ($filteredAttributes as $attr => $attrValue): ?>
           <?= $escaper->escapeHtmlAttr($attr) ?>="<?= $escaper->escapeHtmlAttr($attrValue) ?>"
       <?php endforeach; ?>>
```

Hyvä CMS automatically validates custom field types against HTML5 validation attributes.

## Complete Template Example

Here's a complete basic custom field type template with all required elements:

```php
<?php
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

// Component and field identifiers
$uid = (string) $block->getData('uid');
$fieldName = (string) $block->getData('name');
$fieldValue = $block->getData('value') ?? '';

// HTML attributes and validation
$attributes = (array) $block->getData('attributes') ?? [];
$filteredAttributes = $fieldTypes->getDefinedFieldAttributes($attributes);

// Validation state
$hasError = isset($magewire->errors[$uid][$fieldName]);
$errorMessage = $hasError ? $magewire->errors[$uid][$fieldName] : '';
?>

<div class="field-container" 
     id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
     <?= $hasError ? 'data-error' : '' ?>>
    
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
    
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" 
        class="validation-messages list-none">
        <?php if ($hasError): ?>
            <li class="error-message text-red-600 text-sm mt-1">
                <?= $escaper->escapeHtml($errorMessage) ?>
            </li>
        <?php endif; ?>
    </ul>
</div>
```

## Common Patterns

### Radio Button Group

```php
<div class="field-container" id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" <?= $hasError ? 'data-error' : '' ?>>
    <div class="radio-group flex gap-4">
        <?php foreach ($options as $option): ?>
            <label class="inline-flex items-center">
                <input type="radio"
                       name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
                       value="<?= $escaper->escapeHtmlAttr($option['value']) ?>"
                       <?= $option['value'] === $fieldValue ? 'checked' : '' ?>
                       @change="updateWireField(
                           '<?= $escaper->escapeHtmlAttr($uid) ?>',
                           '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
                           $event.target.value
                       )"
                       class="form-radio <?= $hasError ? 'error field-error' : '' ?>">
                <span class="ml-2"><?= $escaper->escapeHtml($option['label']) ?></span>
            </label>
        <?php endforeach; ?>
    </div>
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" class="validation-messages list-none"></ul>
</div>
```

### Checkbox Group (Multiple Values)

```php
<?php
$selectedValues = $fieldValue ? explode(',', $fieldValue) : [];
?>
<div class="field-container" id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" <?= $hasError ? 'data-error' : '' ?>>
    <div class="checkbox-group flex flex-col gap-2" x-data="{ selected: <?= $escaper->escapeHtmlAttr(json_encode($selectedValues)) ?> }">
        <?php foreach ($options as $option): ?>
            <label class="inline-flex items-center">
                <input type="checkbox"
                       value="<?= $escaper->escapeHtmlAttr($option['value']) ?>"
                       :checked="selected.includes('<?= $escaper->escapeJs($option['value']) ?>')"
                       @change="
                           if ($event.target.checked) {
                               selected.push('<?= $escaper->escapeJs($option['value']) ?>');
                           } else {
                               selected = selected.filter(v => v !== '<?= $escaper->escapeJs($option['value']) ?>');
                           }
                           updateWireField(
                               '<?= $escaper->escapeHtmlAttr($uid) ?>',
                               '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
                               selected.join(',')
                           );
                       "
                       class="form-checkbox">
                <span class="ml-2"><?= $escaper->escapeHtml($option['label']) ?></span>
            </label>
        <?php endforeach; ?>
    </div>
    <input type="hidden" name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>">
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" class="validation-messages list-none"></ul>
</div>
```

### Range Slider with Live Value Display

```php
<div class="field-container" id="field-container-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" <?= $hasError ? 'data-error' : '' ?>>
    <div x-data="{ value: '<?= $escaper->escapeJs($fieldValue ?: '50') ?>' }">
        <input type="range"
               name="<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>"
               x-model="value"
               @input="updateWireField(
                   '<?= $escaper->escapeHtmlAttr($uid) ?>',
                   '<?= $escaper->escapeHtmlAttr($fieldName) ?>',
                   value
               )"
               min="0" max="100" step="1"
               class="w-full">
        <div class="text-center mt-2">
            <span x-text="value"></span>
        </div>
    </div>
    <ul id="validation-messages-<?= $escaper->escapeHtmlAttr("{$uid}_{$fieldName}") ?>" class="validation-messages list-none"></ul>
</div>
```

## Error State Styling

The CMS editor automatically applies error styling when the `data-error` attribute is present on the field container and the input has the `error field-error` classes.

Custom error styling can be added in your module's admin CSS if needed.

## Testing Checklist

When implementing a custom field type template, verify:

- [ ] Field container has correct ID format: `field-container-{uid}_{fieldName}`
- [ ] Input has correct name format: `{uid}_{fieldName}`
- [ ] Validation messages container has correct ID format: `validation-messages-{uid}_{fieldName}`
- [ ] Field container has `data-error` attribute when `$hasError` is true
- [ ] Field value updates on change using `updateWireField` or `updateField`
- [ ] HTML5 validation attributes are applied via `$filteredAttributes`
- [ ] Clicking field value in preview focuses the input
- [ ] Validation errors display in the validation messages container
- [ ] Field value persists after save and refresh
