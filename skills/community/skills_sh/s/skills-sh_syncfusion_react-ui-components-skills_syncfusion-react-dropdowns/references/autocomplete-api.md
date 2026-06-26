# API Reference – Syncfusion React AutoComplete

Source: https://ej2.syncfusion.com/react/documentation/api/auto-complete/index-default

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)

---

## Properties

### actionFailureTemplate
`string | Function` — Default: `'Request failed'`

Template assigned to the popup list content when the remote data fetch request fails.

---

### allowCustom
`boolean` — Default: `true`

Specifies whether the component allows a user-defined value that does not exist in the data source.

---

### allowObjectBinding
`boolean` — Default: `false`

Defines whether object binding is allowed. When `true`, the `value` property holds the full selected object rather than a scalar value.

---

### allowResize
`boolean` — Default: `false`

When `true`, a resize handle appears in the bottom-right corner of the popup, allowing users to resize width and height.

---

### autofill
`boolean` — Default: `false`

When `true`, the first matched item is suggested inline in the input while typing. No action occurs when no matches are found.

---

### cssClass
`string` — Default: `null`

Sets CSS classes on the root element for appearance customization.

---

### dataSource
`{ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[]` — Default: `[]`

Accepts list items from local or remote sources. Can be a string array, number array, object array, or a `DataManager` instance.

---

### debounceDelay
`number` — Default: `300`

Delay in milliseconds before the filter operation fires after each keystroke. Set to `0` to disable debounce.

---

### enablePersistence
`boolean` — Default: `false`

When `true`, the component state (value) is persisted across page reloads.

---

### enableRtl
`boolean` — Default: `false`

When `true`, renders the component in right-to-left direction.

---

### enableVirtualization
`boolean` — Default: `false`

When `true`, enables virtual scrolling. Only visible DOM elements are rendered; they are recycled as the user scrolls. Requires `<Inject services={[VirtualScroll]} />`.

---

### enabled
`boolean` — Default: `true`

When `false`, the component is disabled and all user interactions are blocked.

---

### fields
`FieldSettingsModel` — Default: `{ value: null, iconCss: null, groupBy: null }`

Maps data table columns to component fields:
- `value` — Column whose value is shown in the input on selection
- `iconCss` — Column whose value is used as an icon CSS class
- `groupBy` — Column used to group items into categories
- `disabled` — Column that disables specific items when `true`
- `text` — Column for item display text (if different from value)

---

### filterType
`FilterType` — Default: `'Contains'`

Determines the filter strategy:
- `'StartsWith'` — Items beginning with typed characters
- `'EndsWith'` — Items ending with typed characters
- `'Contains'` — Items containing typed characters anywhere

---

### floatLabelType
`FloatLabelType` — Default: `'Never'`

Controls float label behavior:
- `'Never'` — Label never floats
- `'Always'` — Label always floats above input
- `'Auto'` — Label floats when input is focused or has a value

---

### footerTemplate
`string | Function` — Default: `null`

Template for the static footer element at the bottom of the popup list.

---

### groupTemplate
`string | Function` — Default: `null`

Template for group header labels in the popup list.

---

### headerTemplate
`string | Function` — Default: `null`

Template for the static header element at the top of the popup list.

---

### highlight
`boolean` — Default: `false`

When `true`, highlights the typed characters within suggestion list items using the `e-highlight` CSS class.

---

### htmlAttributes
`{ [key: string]: string }` — Default: `{}`

Additional HTML attributes (e.g., `title`, `name`, `maxlength`) applied to the component input element.

---

### ignoreAccent
`boolean` — Default: `false`

When `true`, diacritic characters (accents) are ignored during filtering.

---

### ignoreCase
`boolean` — Default: `true`

When `true` (default), filtering is case-insensitive. Set to `false` for case-sensitive filtering.

---

### isDeviceFullScreen
`boolean` — Default: `true`

When `true`, the popup opens in full-screen mode on mobile devices. Set to `false` for consistent behavior across desktop and mobile.

---

### itemTemplate
`string | Function` — Default: `null`

Template for rendering each individual list item in the popup.

---

### locale
`string` — Default: `'en-US'`

Overrides the global culture and localization for this component. Use with `L10n.load()` to provide translations.

---

### minLength
`number` — Default: `1`

Minimum number of characters the user must type before the filter/search action fires.

---

### noRecordsTemplate
`string | Function` — Default: `'No records found'`

Template shown when no matching items are found in the suggestion list.

---

### placeholder
`string` — Default: `null`

Short hint text displayed inside the input when it is empty.

---

### popupHeight
`string | number` — Default: `'300px'`

Height of the suggestion popup list.

---

### popupWidth
`string | number` — Default: `'100%'`

Width of the suggestion popup list. Defaults to the width of the input component.

---

### query
`Query` — Default: `null`

An external `Query` instance that is executed along with data processing. Used to filter, select, or limit remote data.

---

### readonly
`boolean` — Default: `false`

When `true`, user interactions (typing/selecting) are disabled but the component remains focusable.

---

### showClearButton
`boolean` — Default: `true`

When `true`, shows a clear (×) button. Clicking it resets `value`, `text`, and `index` to `null`.

---

### showPopupButton
`boolean` — Default: `false`

When `true`, shows a dropdown toggle button on the right side of the input.

---

### sortOrder
`SortOrder` — Default: `null`

Sorts the data source:
- `'None'` — No sorting
- `'Ascending'` — A to Z
- `'Descending'` — Z to A

---

### suggestionCount
`number` — Default: `20`

Maximum number of items shown in the suggestion popup at a time.

---

### value
`number | string | boolean | object | null` — Default: `null`

Gets or sets the selected value. When `allowObjectBinding` is `true`, accepts and returns a full object.

---

### width
`string | number` — Default: `'100%'`

Width of the component input element.

---

### zIndex
`number` — Default: `1000`

z-index of the popup element.

---

## Methods

### addItem
Adds a new item to the popup list. By default appended at the end; use `itemIndex` to insert at a specific position.

```ts
autocomplete.addItem({ id: 'Game9', game: 'Tennis' });
autocomplete.addItem({ id: 'Game0', game: 'Archery' }, 0); // insert at index 0
```

| Parameter | Type | Description |
|---|---|---|
| `items` | `object \| object[] \| string \| number \| boolean \| string[] \| number[]` | Item(s) to add |
| `itemIndex` _(optional)_ | `number` | Index at which to insert the new item |

Returns: `void`

---

### clear
Clears the selected value from the component.

```ts
autocomplete.clear();
```

Returns: `void`

---

### destroy
Removes the component from the DOM and detaches all event handlers, attributes, and classes.

```ts
autocomplete.destroy();
```

Returns: `void`

---

### disableItem
Disables a specific item in the popup. If the selected item is disabled, the selection is cleared.

```ts
autocomplete.disableItem('Tennis');           // by value string
autocomplete.disableItem(liElement);          // by HTMLLIElement
```

| Parameter | Type | Description |
|---|---|---|
| `item` | `string \| number \| object \| HTMLLIElement` | Item to disable |

Returns: `void`

---

### filter
Filters the data from the given data source using a query.

```ts
autocomplete.filter(dataSource, query, fields);
```

| Parameter | Type | Description |
|---|---|---|
| `dataSource` | `object[] \| DataManager \| string[] \| number[] \| boolean[]` | Data source to filter |
| `query` _(optional)_ | `Query` | Query to apply |
| `fields` _(optional)_ | `FieldSettingsModel` | Field mapping |

Returns: `void`

---

### focusIn
Sets focus on the component input.

```ts
autocomplete.focusIn();
```

Returns: `void`

---

### focusOut
Removes focus from the component input.

```ts
autocomplete.focusOut();
```

Returns: `void`

---

### getDataByValue
Returns the data object that matches the given value.

```ts
const item = autocomplete.getDataByValue('Tennis');
```

| Parameter | Type | Description |
|---|---|---|
| `value` | `string \| number \| boolean` | Value to look up |

Returns: `{ [key: string]: Object } | string | number | boolean`

---

### getItems
Returns all list item DOM elements currently bound to the component.

```ts
const items = autocomplete.getItems();
console.log(items.length);
```

Returns: `Element[]`

---

### hidePopup
Closes the suggestion popup if it is open.

```ts
autocomplete.hidePopup();
```

| Parameter | Type | Description |
|---|---|---|
| `e` _(optional)_ | `MouseEvent \| KeyboardEventArgs \| TouchEvent` | Event object |

Returns: `void`

---

### hideSpinner
Hides the loading spinner.

```ts
autocomplete.hideSpinner();
```

Returns: `void`

---

### showPopup
Opens the suggestion popup and shows matching items for the current input value.

```ts
autocomplete.showPopup();
```

| Parameter | Type | Description |
|---|---|---|
| `e` _(optional)_ | `MouseEvent \| KeyboardEventArgs \| TouchEvent` | Event object |

Returns: `void`

---

### showSpinner
Shows the loading spinner.

```ts
autocomplete.showSpinner();
```

Returns: `void`

---

## Events

### actionBegin
`EmitType<Object>`

Fires before data is fetched from a remote server.

---

### actionComplete
`EmitType<Object>`

Fires after data is successfully fetched from a remote server.

---

### actionFailure
`EmitType<Object>`

Fires when the remote data fetch request fails.

---

### beforeOpen
`EmitType<Object>`

Fires before the popup opens.

---

### blur
`EmitType<Object>`

Fires when focus moves out of the component.

---

### change
`EmitType<ChangeEventArgs>`

Fires when an item is selected from the popup or when the model value changes. Use this event for cascading scenarios.

---

### close
`EmitType<PopupEventArgs>`

Fires when the popup is closed.

---

### created
`EmitType<Object>`

Fires when the component is created.

---

### customValueSpecifier
`EmitType<CustomValueSpecifierEventArgs>`

Fires when a custom value (not in the data source) is set. Relevant when `allowCustom={true}`.

---

### dataBound
`EmitType<Object>`

Fires when the data source is populated in the popup list.

---

### destroyed
`EmitType<Object>`

Fires when the component is destroyed.

---

### filtering
`EmitType<FilteringEventArgs>`

Fires on every character typed in the component (subject to `debounceDelay`). Use `args.updateData()` to provide custom filtered results.

---

### focus
`EmitType<Object>`

Fires when the component gains focus.

---

### open
`EmitType<PopupEventArgs>`

Fires when the popup opens.

---

### resizeStart
`EmitType<Object>`

Fires when the user starts resizing the popup (requires `allowResize={true}`).

---

### resizeStop
`EmitType<Object>`

Fires when the user finishes resizing the popup.

---

### resizing
`EmitType<Object>`

Fires continuously while the popup is being resized. Provides live width and height updates.

---

### select
`EmitType<SelectEventArgs>`

Fires when the user selects an item from the popup via mouse, tap, or keyboard navigation.
