# Enonic XP Controller Troubleshooting

## Part Returns 404

**Symptoms:** The part renders as blank or returns a 404 in Content Studio.

**Causes:**
1. The descriptor file name does not match the parent directory name.
   - Fix: Ensure `parts/my-part/my-part.xml` — both names must be identical.
2. The controller file name does not match the descriptor.
   - Fix: Ensure `parts/my-part/my-part.ts` (or `.js`) matches the descriptor directory.
3. The part is not added to a region on the page.
   - Fix: In Content Studio, add the part to a region using the page editor.

## Missing Regions in Page

**Symptoms:** Content Studio does not show the expected regions in the visual editor.

**Causes:**
1. The `<regions>` section is missing from the page XML descriptor.
   - Fix: Add `<regions><region name="main"/></regions>` to the page descriptor.
2. The controller does not pass region data to the view or does not use `data-portal-region`.
   - Fix: Ensure the Thymeleaf view includes `data-portal-region="<name>"` on the container element.
3. The page descriptor is not in the correct path.
   - Fix: Verify the descriptor is at `src/main/resources/site/pages/<page-name>/<page-name>.xml`.

## Layout Regions Not Rendering

**Symptoms:** The layout appears in the page but its drop-zones (regions) are missing.

**Causes:**
1. The layout descriptor is missing region definitions.
   - Fix: Add regions to the `<layout>` XML.
2. The layout controller does not read `component.regions` via `getComponent()`.
   - Fix: Call `getComponent()` and pass each region to the view model.
3. The Thymeleaf view does not iterate over region components.
   - Fix: Use `data-th-each="component : ${region.components}"` with `data-portal-component="${component.path}"`.

## Thymeleaf View Not Found

**Symptoms:** Error `Could not resolve view` when rendering.

**Causes:**
1. The view file is not in the same directory as the controller.
   - Fix: Place the `.html` file alongside the controller and use `resolve('view.html')`.
2. File name mismatch in the `resolve()` call.
   - Fix: Check the exact filename (case-sensitive on Linux).

## Response Processor Not Executing

**Symptoms:** The processor function never runs; no page contributions are injected.

**Causes:**
1. The processor is not declared in `site.xml`.
   - Fix: Add `<response-processor name="<name>" order="10"/>` inside `<processors>`.
2. The controller does not export `responseProcessor`.
   - Fix: Ensure `exports.responseProcessor = function (req, res) { ... }`.
3. The application is not added to the site in Content Studio.
   - Fix: Go to the site content and add the application under the applications list.

## Config Values Are Undefined

**Symptoms:** `component.config.fieldName` returns `undefined`.

**Causes:**
1. The field name in the descriptor does not match the property accessed in the controller.
   - Fix: Ensure `<input name="heading">` in the XML matches `config.heading` in the controller.
2. The form field has `minimum="0"` and the editor did not fill it in.
   - Fix: Add a null check or default: `config.heading || 'Default Heading'`.
