# Troubleshooting Guide

Common issues when creating Hyvä CMS components and their solutions.

## Schema Validation Errors

**Symptom:** Component doesn't appear in the editor, or console shows JSON schema errors.

**Common causes:**
1. **Invalid property at component level** - Check `component-schema.md` for allowed properties. Common mistake: using `hidden` instead of `require_parent: true`.
2. **Invalid field type** - Verify the `type` value exists in `field-types.md`.
3. **Malformed JSON** - Validate JSON syntax (missing commas, trailing commas, unquoted keys).
4. **Component name too short** - Names must be at least 3 characters.

**Resolution:** Run schema validation:
```bash
# Check JSON syntax
cat etc/hyva_cms/components.json | python3 -m json.tool
```

## Component Not Visible in Editor

**Symptom:** Component created but doesn't appear in the Hyvä CMS editor.

**Checklist:**
1. **Cache:** Clear Magento cache after creating/modifying components:
   ```bash
   bin/magento cache:clean config full_page
   ```
2. **Disabled flag:** Ensure `"disabled": true` is not set on the component.
3. **require_parent:** If `"require_parent": true`, component only appears as child option in parent components.
4. **Category:** Component may be in a different category tab in the editor.
5. **File location:** Verify `components.json` is in `etc/hyva_cms/` directory (not `etc/`).

## Template Not Rendering

**Symptom:** Component appears in editor but shows blank or error on frontend.

**Common causes:**
1. **Template path mismatch** - Verify `template` value in `components.json` matches actual file location.
2. **PHP syntax error** - Check Magento/PHP logs for parse errors.

**Resolution:**
1. Check template path format: `Vendor_Module::elements/component-name.phtml`
2. Verify file exists at: `view/frontend/templates/elements/component-name.phtml`
3. Check Magento logs:
   ```bash
   tail -f var/log/exception.log var/log/system.log
   ```

## Live Editor Not Working

**Symptom:** Changes in the live editor don't reflect, or fields aren't editable.

**Common causes:**
1. **Missing `getEditorAttrs()`** - Root element must have `$block->getEditorAttrs()`.
2. **Missing field attributes** - Editable fields need `$block->getEditorAttrs('field_name')`.

**Correct pattern:**
```php
<div <?= /** @noEscape */ $block->getEditorAttrs() ?>>
    <h2 <?= /** @noEscape */ $block->getEditorAttrs('title') ?>>
        <?= $escaper->escapeHtml($title) ?>
    </h2>
</div>
```

## Image Not Displaying

**Symptom:** Image field has value but nothing renders.

**Checklist:**
1. **Null check:** Always check if image data exists before rendering:
   ```php
   <?php if ($image): ?>
   ```
2. **Media view model:** Ensure `Media` class is imported and instantiated.
3. **For children with `template: false`:** Check `!empty($image['src'])` not just `$image`.

## Dependent Skills Unavailable

If referenced skills (`hyva-exec-shell-cmd`, `hyva-create-module`, `hyva-render-media-image`) are not available:

- **hyva-exec-shell-cmd:** Manually determine environment. For Warden: prefix commands with `warden shell -c "..."`. For local: run commands directly.
- **hyva-create-module:** Manually create module files (registration.php, composer.json, etc/module.xml) following the structure in `example-component.md`.
- **hyva-render-media-image:** Use basic `<img>` tag or reference Hyvä Theme documentation for `\Hyva\Theme\ViewModel\Media` API.