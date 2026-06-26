# Enonic XP Content Type Reference

## XML Structure

Content types are XML files located at:
`/src/main/resources/site/content-types/[name]/[name].xml`

The directory name **must** match the file name (minus the `.xml` extension).

### Root Element

```xml
<content-type>
  <display-name i18n="localization.key">Human-Readable Name</display-name>
  <display-name-label i18n="localization.label.key">Override placeholder</display-name-label>   <!-- optional; since XP 7.1 -->
  <description>Short description</description>                     <!-- optional -->
  <super-type>base:structured</super-type>                         <!-- required -->
  <is-abstract>false</is-abstract>                                 <!-- optional, default false -->
  <is-final>true</is-final>                                        <!-- optional, default false -->
  <is-built-in>false</is-built-in>                                 <!-- optional, default false -->
  <allow-child-content>true</allow-child-content>                  <!-- optional, default true -->
  <allow-child-content-type>base:folder</allow-child-content-type> <!-- optional, repeatable -->
  <form>                                                           <!-- required -->
    <!-- inputs, item-sets, option-sets, field-sets, mixin refs -->
  </form>
</content-type>
```

- `display-name` (required): Human-readable name of the content type. The optional `i18n` attribute maps to a localization key in the application's resource bundle.
- `display-name-label` (optional; since v7.1): Overrides the default `<Display Name>` placeholder shown in the content form when editors create new content of this type.
- `form` (required): The custom form definition containing inputs, item-sets, option-sets, field-sets, and mixin references.

> **Note:** `allow-child-content-type` has no effect if `allow-child-content` is set to `false`.

> **Note:** The optional `i18n` attribute on `<display-name>`, `<display-name-label>`, `<label>`, and `<help-text>` holds a key to a localization phrase defined in the application's resource bundle.

`allow-child-content-type` supports pattern matching (the same syntax as ContentSelector's MATCH mode). Examples:

- `${app}:article` — match `article` type from the current application
- `${app}:article-*` — match all types starting with `article-` from the current application
- `base:folder` — match the built-in folder type
- `*:quote` — match `quote` from any application

### Content Type Icon

A content type may optionally have its own icon. Add a PNG or SVG file with the same name in the content type directory:

```
src/main/resources/site/content-types/my-type/my-type.svg
```

### XSD Validation Attributes

Add these attributes to `<content-type>` for editor validation:

```xml
<content-type
    xmlns="urn:enonic:xp:model:1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="urn:enonic:xp:model:1.0 https://raw.githubusercontent.com/enonic/xp/master/modules/core/core-api/src/main/resources/META-INF/xsd/model.xsd">
```

## Super-Types

| Super-Type | Purpose |
|---|---|
| `base:structured` | Default for custom content types with a form |
| `base:folder` | Container with no custom fields |
| `base:unstructured` | Schema-less, API-only content |
| `base:shortcut` | Redirect to another content item |
| `base:media` | Abstract base for uploaded files |

Always use `base:structured` unless the content type has a specific reason to inherit from another.

## Input Types Catalog

### Text Inputs

| Type | Value Type | Description |
|---|---|---|
| `TextLine` | String | Single-line text |
| `TextArea` | String | Multi-line plain text |
| `HtmlArea` | String | Rich-text editor (HTML) |

#### TextLine Config

```xml
<input name="socialsecuritynumber" type="TextLine">
  <label>My SSN</label>
  <config>
    <max-length>11</max-length>
    <show-counter>true</show-counter>
    <regexp>\b\d{3}-\d{2}-\d{4}\b</regexp>
  </config>
</input>
```

- `max-length` — maximum allowed characters (default: unlimited)
- `show-counter` — show text length counter (default: hidden)
- `regexp` — regular expression for validation

#### TextArea Config

```xml
<input name="mytextarea" type="TextArea">
  <label>My TextArea</label>
  <config>
    <max-length>500</max-length>
    <show-counter>true</show-counter>
  </config>
</input>
```

- `max-length` — maximum allowed characters (default: unlimited)
- `show-counter` — show text length counter (default: hidden)

#### HtmlArea Config

```xml
<input name="myhtmlarea" type="HtmlArea">
  <label>My HtmlArea</label>
  <config>
    <exclude>*</exclude>
    <include>JustifyLeft JustifyRight | Bold Italic</include>
    <allowHeadings>h2 h4 h6</allowHeadings>
  </config>
</input>
```

- `exclude` — remove tools from toolbar (use `*` to remove all)
- `include` — add tools to toolbar (separate with space, group with `|`)
- `allowHeadings` — space-separated list of allowed heading tags (`h1` through `h6`; all allowed by default)

Default toolbar: `Format | JustifyBlock JustifyLeft JustifyCenter JustifyRight | BulletedList NumberedList Outdent Indent | FindAndReplace SpecialChar Anchor Image Macro Link Unlink | Table | PasteModeSwitcher`

Complete list of available editor tools:

| Tool | Description |
|---|---|
| `Format` | Text format menu |
| `Bold` | Bold text |
| `Italic` | Italic text |
| `Underline` | Underline text |
| `JustifyBlock` | Justify content |
| `JustifyLeft` | Left align content |
| `JustifyCenter` | Center content |
| `JustifyRight` | Right align content |
| `BulletedList` | Insert a bullet list |
| `NumberedList` | Insert a numbered list |
| `Outdent` | Decrease indent |
| `Indent` | Increase indent |
| `FindAndReplace` | Find and Replace dialog |
| `SpecialChar` | Insert a special character |
| `Anchor` | Insert an anchor |
| `Image` | Insert/Edit an image |
| `Macro` | Insert a macro |
| `Link` | Insert/Edit a link |
| `Unlink` | Remove link |
| `Table` | Table format menu |
| `PasteModeSwitcher` | Paste mode (formatted/plain text) |
| `BGColor` | Background color |
| `Blockquote` | Quotation |
| `Copy` | Copy selected text into buffer |
| `CopyFormatting` | Copy formatting |
| `CreateDiv` | Wrap with div |
| `Cut` | Cut selected text into buffer |
| `Font` | Font menu |
| `FontSize` | Font size menu |
| `HorizontalRule` | Insert a horizontal line |
| `Language` | Set language for parts of the text |
| `ListStyle` | Change style of BulletedList |
| `NewPage` | Clean editor's content |
| `Preview` | Preview HTML Area contents |
| `Redo` | Repeat the last action |
| `RemoveFormat` | Remove formatting |
| `SelectAll` | Select editor's content |
| `Strike` | Strikethrough over text |
| `Styles` | Text styles menu |
| `Subscript` | Subscript text |
| `Superscript` | Superscript text |
| `TextColor` | Text color |
| `Undo` | Undo the last action |

### Numeric Inputs

| Type | Value Type | Description |
|---|---|---|
| `Long` | Long | Integer number |
| `Double` | Double | Decimal number |

#### Long Config

```xml
<input name="degrees" type="Long">
  <label>Degrees</label>
  <config>
    <min>0</min>
    <max>360</max>
  </config>
</input>
```

- `min` — minimum allowed value
- `max` — maximum allowed value

#### Double Config

```xml
<input name="angle" type="Double">
  <label>Angle (rad)</label>
  <config>
    <min>0</min>
    <max>3.14159</max>
  </config>
</input>
```

- `min` — minimum allowed value
- `max` — maximum allowed value

### Date/Time Inputs

| Type | Value Type | Description |
|---|---|---|
| `Date` | LocalDate | Date only (no time) |
| `DateTime` | LocalDateTime / Instant | Date and time (local by default; timezone via config) |
| `Time` | LocalTime | Time only |

### Date Config

```xml
<input name="mydate" type="Date">
  <label>My Date</label>
  <default>2011-09-12</default>
</input>
```

- `default` supports ISO 8601 date format (`yyyy-MM-dd`) or relative expressions (e.g., `+1year -12days`, `now`)

#### DateTime Config

```xml
<input name="mydatetime" type="DateTime">
  <label>My DateTime</label>
  <config>
    <timezone>true</timezone>
  </config>
  <default>2011-09-12</default>
</input>
```

- `timezone` — set to `true` to store value with timezone (produces `Instant`); default is `false` (produces `LocalDateTime`)
- `default` supports ISO 8601 format (`yyyy-MM-ddThh:mm`, with optional timezone offset like `+01:00` or `Z`) or relative expressions (e.g., `+1year -12hours`, `now`)

**Relative expression unit strings:**

| Singular | Plural | Initial letter |
|---|---|---|
| `year` | `years` | `y` |
| `month` | `months` | `M` |
| `week` | `weeks` | `w` |
| `day` | `days` | `d` |
| `hour` | `hours` | `h` |
| `minute` | `minutes` | `m` |

A relative expression is one or more offsets (e.g., `+3days -2hours`). The keyword `now` means current date and time.

#### Time Config

```xml
<input name="mytime" type="Time">
  <label>My Time</label>
  <default>13:22</default>
</input>
```

- `default` supports 24h format (`hh:mm`) or relative expressions (e.g., `+1hour -12minutes`, `now`)

### Selection Inputs

| Type | Value Type | Description |
|---|---|---|
| `ComboBox` | String | Dropdown with predefined static options |
| `RadioButton` | String | Radio buttons for single selection |
| `CheckBox` | Boolean | Single true/false toggle |

> **Note:** CheckBox is a single boolean toggle. Occurrences are typically left at the default (`0..1`) or omitted entirely.

| `ContentSelector` | Reference (content ID) | Select existing content items |
| `ContentTypeFilter` | String | Select a content type |
| `CustomSelector` | String | Custom service-backed selector |

#### CheckBox Config

```xml
<input name="mycheckbox" type="CheckBox">
  <label>My Checkbox</label>
  <default>checked</default>
  <config>
    <alignment>right</alignment>
  </config>
</input>
```

- `alignment` — placement relative to label: `left` (default), `right`, `top`, `bottom`
- `default` — use `checked` to pre-select; default is unchecked

#### ContentTypeFilter Config

```xml
<input name="myctyfilter" type="ContentTypeFilter">
  <label>My ContentTypeFilter</label>
  <config>
    <context>true</context>
  </config>
</input>
```

- `context` — `true` limits content types to applications configured for the current site (default: `false`)

#### CustomSelector Config

```xml
<input name="mycustomselector" type="CustomSelector">
  <label>My Custom Selector</label>
  <config>
    <service>my-custom-selector</service>
    <param value="genre">classic</param>
    <galleryMode>true</galleryMode>
  </config>
</input>
```

- `service` — name of a JavaScript service at `/resources/services/[name]/[name].js`; can reference another app with `com.myapp:servicename`
- `param` — optional name-value parameters passed to the service as query params (repeatable)
- `galleryMode` — `true` displays options as a three-column image gallery

#### CustomSelector Service Request

In addition to `param` values, the service receives these query parameters:

- `ids` — array of item IDs already selected (service should return those items)
- `start` — index of the first item expected (pagination)
- `count` — maximum number of items expected (pagination)
- `query` — search text typed by the user

#### CustomSelector Service Response

The service controller must return JSON with `total`, `count`, and `hits` properties:

```json
{
  "total": 10,
  "count": 2,
  "hits": [
    {
      "id": "1",
      "displayName": "Option number 1",
      "description": "Optional description",
      "iconUrl": "/some/path/images/icon.svg"
    },
    {
      "id": "2",
      "displayName": "Option number 2",
      "icon": {
        "data": "<svg xmlns=\"http://www.w3.org/2000/svg\"/>",
        "type": "image/svg+xml"
      }
    }
  ]
}
```

Each hit must have `id` and `displayName`. Optional fields: `description`, `iconUrl`, `icon`.

### Media Inputs

| Type | Value Type | Description |
|---|---|---|
| `ImageSelector` | Reference (content ID) | Select image content |
| `MediaSelector` | Reference (content ID) | Select any media content |
| `AttachmentUploader` | String (attachment name) | Upload directly to the content |

### Other Inputs

| Type | Value Type | Description |
|---|---|---|
| `GeoPoint` | GeoPoint | Latitude/longitude coordinates |
| `Tag` | String | Free-form tags |

#### GeoPoint Config

```xml
<input name="mygeopoint" type="GeoPoint">
  <label>My GeoPoint</label>
  <occurrences minimum="0" maximum="1"/>
  <default>51.5,-0.1</default>
</input>
```

- `default` specifies a default coordinate as two comma-separated decimal numbers (latitude, longitude)

### Common Input Attributes

```xml
<input name="fieldName" type="InputType">
  <label i18n="key">Display Label</label>        <!-- required -->
  <help-text>Explanation for editors</help-text>   <!-- optional -->
  <occurrences minimum="0" maximum="1"/>           <!-- optional; defaults 0..1 -->
  <default>value</default>                         <!-- optional -->
  <config>
    <!-- type-specific configuration -->
  </config>
</input>
```

**Occurrences rules:**
- `minimum="0"` — field is optional
- `minimum="1"` — field is mandatory
- `maximum="0"` — unlimited values (multi-value)
- `maximum="1"` — single value

### ComboBox Config Example

```xml
<input name="category" type="ComboBox">
  <label>Category</label>
  <occurrences minimum="1" maximum="1"/>
  <config>
    <option value="electronics">Electronics</option>
    <option value="clothing">Clothing</option>
    <option value="home">Home</option>
  </config>
  <default>electronics</default>
</input>
```

- `default` is optional and may be equal to one of the option `@value` attributes

### RadioButton Config Example

```xml
<input name="priority" type="RadioButton">
  <label>Priority</label>
  <occurrences minimum="1" maximum="1"/>
  <config>
    <option value="low" i18n="priority.low">Low</option>
    <option value="medium" i18n="priority.medium">Medium</option>
    <option value="high" i18n="priority.high">High</option>
  </config>
  <default>medium</default>
</input>
```

- `default` is optional and may be equal to one of the option `@value` attributes
- `i18n` on `<option>` is optional and holds the key to a localization phrase
- Occurrences only supports `minimum` of 0 or 1; `maximum` is always 1

### ContentSelector Config Example

```xml
<input name="relatedArticles" type="ContentSelector">
  <label>Related Articles</label>
  <occurrences minimum="0" maximum="0"/>
  <config>
    <allowContentType>myapp:article</allowContentType>
    <allowPath>${site}/*</allowPath>
    <treeMode>true</treeMode>
    <hideToggleIcon>true</hideToggleIcon>
  </config>
</input>
```

- `allowContentType` — restrict selectable content types (repeatable; supports `${app}:name` shorthand)
- `allowPath` — restrict content by path (repeatable; supports `${site}/*`, `./*`, `../*`)
- `treeMode` — `true` shows content tree instead of flat list (default: `false`)
- `hideToggleIcon` — `true` hides the flat/tree toggle icon (default: `false`)

By default, ContentSelector only displays content from the same site.

#### Allow Content Type Pattern Matching

XP uses one of two modes for content type patterns:

- **`LEGACY`** — substring matching within the content type name (default before XP 7.7.0)
- **`MATCH`** — regex-based pattern matching (current default since XP 7.7.0); the whole content type name must match

Special cases in XP pattern matching:

- `${app}` — template expression replaced with the current application name
- `*` — treated as "0 or more of any character(s) except line breaks" (glob-style, not regex `*`)

#### allowContentType Samples

```xml
<!-- Content type "citation" within your current application -->
<allowContentType>citation</allowContentType>

<!-- Content type "quote" from the application "my.other.app" -->
<allowContentType>my.other.app:quote</allowContentType>

<!-- Content types "quote" from any application -->
<allowContentType>*:quote</allowContentType>

<!-- Any content types from current application -->
<allowContentType>${app}:*</allowContentType>

<!-- All content types starting with "banana" -->
<allowContentType>*:banana*</allowContentType>

<!-- All content types except "base:folder" -->
<allowContentType>^(?!base:folder$)*</allowContentType>
```

#### allowPath Samples

```xml
<!-- All content starting from the root -->
<allowPath>*</allowPath>

<!-- Only content from the current site -->
<allowPath>${site}/*</allowPath>

<!-- All children of <site>/people -->
<allowPath>${site}/people/*</allowPath>

<!-- All children of the current content -->
<allowPath>./*</allowPath>

<!-- All children of the current content's parent -->
<allowPath>../*</allowPath>
```

### ImageSelector Config Example

```xml
<input name="images" type="ImageSelector">
  <label>Images</label>
  <occurrences minimum="0" maximum="0"/>
  <config>
    <allowPath>${site}/*</allowPath>
    <treeMode>true</treeMode>
    <hideToggleIcon>true</hideToggleIcon>
  </config>
</input>
```

ImageSelector supports the same config options as ContentSelector **except** `allowContentType` (it is always limited to `media:image`). By default, ImageSelector displays all images from the root.

### MediaSelector Config Example

```xml
<input name="mymedia" type="MediaSelector">
  <label>My Media</label>
  <occurrences minimum="0" maximum="1"/>
  <config>
    <allowContentType>media:archive</allowContentType>
    <allowPath>${site}/*</allowPath>
    <treeMode>true</treeMode>
    <hideToggleIcon>true</hideToggleIcon>
  </config>
</input>
```

MediaSelector supports the same config options as ContentSelector, but `allowContentType` is limited to `media:*` types. By default, MediaSelector displays all media from the root.

## Item Sets

Group repeatable nested form fields into a property set.

```xml
<item-set name="contact_info">
  <label>Contact Info</label>
  <occurrences minimum="0" maximum="0"/>
  <items>
    <input name="label" type="TextLine">
      <label>Label</label>
    </input>
    <input name="phone_number" type="TextLine">
      <label>Phone Number</label>
    </input>
  </items>
</item-set>
```

- `name` — used as the property key in persisted data
- `<items>` — contains input types, nested item-sets, or option-sets
- Item sets can be nested inside other item sets

## Option Sets

Present a set of mutually exclusive or multi-select options, each with optional sub-forms.

### Single-Select (radio-style)

```xml
<option-set name="blockType">
  <label>Block Type</label>
  <help-text>Select the type of content block</help-text>
  <occurrences minimum="0" maximum="0"/>
  <help-text>Create content with optional blocks</help-text>
  <options minimum="1" maximum="1">
    <option name="text">
      <label>Text Block</label>
      <help-text>A rich text content block</help-text>
      <items>
        <input name="body" type="HtmlArea">
          <label>Body</label>
          <occurrences minimum="1" maximum="1"/>
        </input>
      </items>
    </option>
    <option name="image">
      <label>Image Block</label>
      <items>
        <input name="image" type="ImageSelector">
          <label>Image</label>
          <occurrences minimum="1" maximum="1"/>
        </input>
      </items>
    </option>
  </options>
</option-set>
```

- `options/@maximum="1"` — single-select mode
- Each option can be empty or contain `<items>`
- `<help-text>` can be added to the option-set itself and to individual `<option>` elements

### Multi-Select (checkbox-style)

```xml
<option-set name="features">
  <label>Features</label>
  <expanded>true</expanded>
  <occurrences minimum="1" maximum="1"/>
  <options minimum="0" maximum="3">
    <option name="wifi">
      <label>WiFi</label>
      <help-text>Wireless internet access included</help-text>
      <default>true</default>
    </option>
    <option name="parking">
      <label>Parking</label>
    </option>
    <option name="pool">
      <label>Pool</label>
    </option>
  </options>
</option-set>
```

- `options/@maximum` > 1 — multi-select mode
- `<expanded>true</expanded>` — shows all options expanded by default
- `<default>true</default>` on an option — pre-selects it

## Mixins

Reusable form fragments stored at `src/main/resources/site/mixins/[name]/[name].xml`.

### Mixin Definition

```xml
<mixin>
  <display-name>Address</display-name>
  <form>
    <input type="TextLine" name="street">
      <label>Street</label>
    </input>
    <input type="TextLine" name="city">
      <label>City</label>
      <occurrences minimum="1" maximum="1"/>
    </input>
  </form>
</mixin>
```

### Mixin Reference (in content type)

```xml
<form>
  <input type="TextLine" name="name">
    <label>Name</label>
  </input>
  <mixin name="address"/>
</form>
```

The mixin fields are merged inline at the position of `<mixin name="..."/>`.

## X-Data

Extra data schemas that can be attached to any content type.

Location: `src/main/resources/site/x-data/[name]/[name].xml`

```xml
<x-data>
  <display-name>SEO Metadata</display-name>
  <form>
    <input type="TextLine" name="metaTitle">
      <label>Meta Title</label>
    </input>
    <input type="TextArea" name="metaDescription">
      <label>Meta Description</label>
    </input>
  </form>
</x-data>
```

### X-Data Registration in site.xml

X-data schemas are registered for use in `src/main/resources/site/site.xml`. Use `allowContentTypes` to restrict by content type pattern and `optional` to let editors enable it manually:

```xml
<site>
  <x-data name="my-x-data-1" />
  <x-data name="my-x-data-2" allowContentTypes="^(?!base:folder$).*" />
  <x-data name="my-x-data-3" allowContentTypes="portal:site" optional="true" />
  <form/>
</site>
```

- Without `allowContentTypes` and `optional`, x-data is enabled for all content types with no option to remove it
- `allowContentTypes` accepts a regular expression to match content type names
- `optional="true"` requires editors to manually enable the x-data in Content Wizard

## Field Sets (Decorative Grouping)

Group fields visually without affecting data structure:

```xml
<field-set>
  <label>Personal Information</label>
  <items>
    <input name="firstName" type="TextLine">
      <label>First Name</label>
    </input>
    <input name="lastName" type="TextLine">
      <label>Last Name</label>
    </input>
  </items>
</field-set>
```

Field sets do **not** need a `name` attribute since they are only visual and do **not** affect the data model — fields inside remain at the same property level.

## Documentation Links

- Content Types: https://developer.enonic.com/docs/xp/7.x/cms/content-types
- Input Types: https://developer.enonic.com/docs/xp/7.x/cms/schemas/input-types
- Option Sets: https://developer.enonic.com/docs/xp/7.x/cms/schemas/option-set
- Item Sets: https://developer.enonic.com/docs/xp/7.x/cms/schemas/item-set
- Mixins: https://developer.enonic.com/docs/xp/7.x/cms/schemas/mixins
- X-Data: https://developer.enonic.com/docs/xp/7.x/cms/x-data
- Schema System: https://developer.enonic.com/docs/xp/7.x/cms/schemas
