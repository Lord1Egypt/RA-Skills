# Reference generation

Use references to create new content with specified visual or audio guidance. Record each asset's type, array index, subject, and role. Preserve the order between the prompt and request.

For example, image 1 can define the product, image 2 the setting, video 1 the camera movement, and audio 1 the sound. A rough motion reference does not establish final product materials or scene appearance: describe those separately.

Use the `reference_*` arrays with `omni_reference_task_type: "reference"` and at least one reference. Do not combine this with single-image or first/last-frame fields. For the separate `auto` mode, use adaptive aspect ratio and duration `-1`; reference videos must meet the 4–30-second constraints in the [API](../../api/seedance.md).

Check the returned result for correct subject and role binding. A failed binding is a quality issue, not permission for unlimited paid retries. Editing an existing video has a different [workflow](editing-and-extension.md).
