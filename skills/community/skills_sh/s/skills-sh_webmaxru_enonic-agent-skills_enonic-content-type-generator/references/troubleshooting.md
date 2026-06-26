# Enonic XP Content Type Troubleshooting

## Common XML Errors

### Missing `<super-type>`

**Symptom:** Content type fails to register or throws a schema validation error.

**Fix:** Every content type **must** declare a `<super-type>`. For custom types, use:
```xml
<super-type>base:structured</super-type>
```

### Missing `<display-name>`

**Symptom:** Content type does not appear in Content Studio or throws a validation error.

**Fix:** `<display-name>` is the only truly required child element. Add it as the first child:
```xml
<content-type>
  <display-name>My Content Type</display-name>
  ...
</content-type>
```

### Input `name` Contains Invalid Characters

**Symptom:** Schema fails to compile.

**Fix:** The `name` attribute on `<input>`, `<item-set>`, and `<option-set>` must be a valid XML name — alphanumeric with no spaces. Use camelCase or underscores:
```xml
<!-- Good -->
<input name="firstName" type="TextLine">
<input name="phone_number" type="TextLine">

<!-- Bad -->
<input name="first name" type="TextLine">
<input name="first-name" type="TextLine">
```

### Incorrect `type` Case

**Symptom:** Unknown input type error.

**Fix:** Input type names are case-sensitive. Use exact casing from the catalog:
- `TextLine` (not `textline` or `Textline`)
- `HtmlArea` (not `htmlarea` or `HTMLArea`)
- `ImageSelector` (not `imageselector`)
- `ContentSelector` (not `contentselector`)
- `ComboBox` (not `combobox` or `Combobox`)
- `RadioButton` (not `radiobutton`)
- `CheckBox` (not `checkbox`)
- `DateTime` (not `datetime` or `Datetime`)
- `GeoPoint` (not `geopoint`)
- `AttachmentUploader` (not `attachmentuploader`)
- `MediaSelector` (not `mediaselector`)
- `CustomSelector` (not `customselector`)
- `ContentTypeFilter` (not `contenttypefilter`)

### Duplicate `name` Attributes

**Symptom:** Only one field shows up in the form, or data is overwritten.

**Fix:** Every `name` attribute must be unique within the same nesting level. Rename one of the duplicates.

### ComboBox Without Options

**Symptom:** An empty dropdown appears with no choices.

**Fix:** ComboBox requires at least one `<option>` inside `<config>`:
```xml
<config>
  <option value="opt1">Option 1</option>
  <option value="opt2">Option 2</option>
</config>
```

### Option Set `options/@maximum` Set Wrong

**Symptom:** Option set behaves as multi-select when single-select was intended, or vice versa.

**Fix:**
- Single-select: `<options minimum="1" maximum="1">`
- Multi-select: `<options minimum="0" maximum="N">` where N > 1

### File Not Found in Content Studio

**Symptom:** Content type does not appear in the content creation dropdown.

**Fix:** Verify the file is at the correct path:
```
src/main/resources/site/content-types/[name]/[name].xml
```
The directory name and file name (without `.xml`) must match exactly.

### Mixin Not Found

**Symptom:** Error referencing a mixin from a content type.

**Fix:**
1. Verify the mixin file exists at `src/main/resources/site/mixins/[name]/[name].xml`
2. The `name` in `<mixin name="..."/>` must match the mixin directory name exactly
3. The mixin must belong to the same application or be qualified with the app namespace

### Occurrences Confusion

**Symptom:** Field validation does not work as expected.

**Fix:** Remember the distinction:
- `<occurrences>` on an `<input>` — controls how many values the input accepts
- `<occurrences>` on an `<item-set>` — controls how many instances of the set
- `<occurrences>` on an `<option-set>` — controls how many instances of the whole option set
- `<options minimum="..." maximum="...">` — controls how many options can be selected within one option-set instance

### DateTime Stores Without Timezone

**Symptom:** DateTime values lose timezone information when saved, or API returns `LocalDateTime` instead of `Instant`.

**Fix:** By default DateTime stores values without timezone. Add `<timezone>true</timezone>` in the config to store timezone-aware values:
```xml
<config>
  <timezone>true</timezone>
</config>
```

### ImageSelector `allowContentType` Ignored

**Symptom:** `<allowContentType>` in an ImageSelector config has no effect.

**Fix:** ImageSelector does not support `allowContentType` — it is always limited to `media:image`. Use `allowPath` to restrict which images are selectable. If you need to select non-image media, use `MediaSelector` instead.
