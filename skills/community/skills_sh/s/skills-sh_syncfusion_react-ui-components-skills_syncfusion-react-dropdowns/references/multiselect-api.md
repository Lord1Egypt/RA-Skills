```markdown
# MultiSelectComponent API

This file is a focused extraction of the official Syncfusion React MultiSelect API. It lists all public properties, methods, and events. Source: https://ej2.syncfusion.com/react/documentation/api/multi-select/index-default

## Properties

- `actionFailureTemplate` (string | Function)
  - Template assigned to the popup list content when data fetch from remote server fails. Default: `'Request failed'`.

- `addTagOnBlur` (boolean)
  - When enabled, typed value is converted into a chip or updated as a component value when focus leaves the component (instead of on Enter key). Default: `false`.

- `allowCustomValue` (boolean)
  - Allows users to add a custom value that is not present in the suggestion list. Default: `false`.

- `allowFiltering` (boolean)
  - Enables the filtering/search option in the component. Fires the `filtering` event when text is typed in the search box. Default: `null`.

- `allowObjectBinding` (boolean)
  - Defines whether object binding is allowed in the component. When enabled, full objects are used as values instead of primitives. Default: `false`.

- `allowResize` (boolean)
  - When set to `true`, a resize handle appears in the bottom-right corner of the popup, allowing the user to resize popup width and height. Default: `false`.

- `changeOnBlur` (boolean)
  - When `true`, the `change` event fires on focus-out. When `false`, `change` fires on every selection and removal. Default: `true`.

- `closePopupOnSelect` (boolean)
  - Controls popup visibility when an item is selected. Default: `true`.

- `cssClass` (string)
  - Custom CSS classes applied to the root element for style customization. Default: `null`.

- `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[])
  - Accepts list items via local array or remote `DataManager` instance. Default: `[]`.

- `debounceDelay` (number)
  - Specifies the delay in milliseconds for filtering operations. Default: `300`.

- `delimiterChar` (string)
  - Sets the delimiter character used in `Default` and `Delimiter` visibility modes. Default: `','`.

- `enableGroupCheckBox` (boolean)
  - When `true`, renders a checkbox for group headers in checkbox mode, allowing all items in a group to be selected/deselected at once. Default: `false`.

- `enableHtmlSanitizer` (boolean)
  - Defines whether to sanitize HTML to prevent cross-site scripting (XSS). Default: `true`.

- `enablePersistence` (boolean)
  - Enables persisting the component's `value` state between page reloads. Default: `false`.

- `enableRtl` (boolean)
  - Enables right-to-left rendering of the component. Default: `false`.

- `enableSelectionOrder` (boolean)
  - Reorders the selected items in the popup visibility state. Default: `true`.

- `enableVirtualization` (boolean)
  - Enables virtual scrolling for improved performance with large datasets. Default: `false`.

- `enabled` (boolean)
  - Specifies whether the MultiSelect component is enabled or disabled. Default: `true`.

- `fields` (FieldSettingsModel)
  - Maps data table columns to the component. Key sub-properties:
    - `text` — column mapped to display text.
    - `value` — column mapped to item value.
    - `iconCss` — column mapped to icon CSS class.
    - `groupBy` — column used to group list items.
    - `disabled` — column used to disable specific items.
  - Default: `{ text: null, value: null, iconCss: null, groupBy: null }`.

- `filterBarPlaceholder` (string)
  - Watermark text displayed in the filter search box. Default: `null`.

- `filterType` (FilterType)
  - Determines the filter strategy applied during search. Options: `'StartsWith'` | `'EndsWith'` | `'Contains'`. Default: `'StartsWith'`.

- `floatLabelType` (FloatLabelType)
  - Controls floating label behavior. Options: `'Never'` | `'Always'` | `'Auto'`. Default: `Never`.

- `footerTemplate` (string | Function)
  - Template assigned to the footer container of the popup list. Default: `null`.

- `groupTemplate` (string | Function)
  - Template assigned to the group headers in the popup list. Default: `null`.

- `headerTemplate` (string | Function)
  - Template assigned to the header container of the popup list. Default: `null`.

- `hideSelectedItem` (boolean)
  - When `true`, hides already-selected items from the dropdown list. Default: `true`.

- `htmlAttributes` ({ [key: string]: string })
  - Additional HTML attributes (e.g., `name`, `title`) applied to the input element as key-value pairs. Default: `{}`.

- `ignoreAccent` (boolean)
  - When `true`, ignores diacritic characters/accents during filtering. Default: `false`.

- `ignoreCase` (boolean)
  - Enables case-insensitive filtering when `true`. Default: `true`.

- `isDeviceFullScreen` (boolean)
  - Defines whether the popup opens in fullscreen mode on mobile devices when filtering is enabled. Default: `true`.

- `itemTemplate` (string | Function)
  - Template assigned to each list item in the popup. Default: `null`.

- `locale` (string)
  - Overrides the global culture/locale for this component. Default: `'en-US'`.

- `maximumSelectionLength` (number)
  - Limits the number of items that can be selected. Selection is prevented once the limit is reached. Default: `1000`.

- `mode` (visualMode)
  - Configures how selected items are displayed. Options:
    - `'Box'` — selected items shown as chips.
    - `'Delimiter'` — selected items shown as delimited text.
    - `'Default'` — `Box` mode on focus-in, `Delimiter` mode on blur.
    - `'CheckBox'` — checkboxes rendered in list items.
  - Default: `'Default'`.

- `noRecordsTemplate` (string | Function)
  - Template shown in the popup when no data matches. Default: `'No records found'`.

- `openOnClick` (boolean)
  - Automatically opens the popup when the control is clicked. Default: `true`.

- `placeholder` (string)
  - Placeholder text shown in the input when no item is selected. Default: `null`.

- `popupHeight` (string | number)
  - Height of the popup list. Default: `'300px'`.

- `popupWidth` (string | number)
  - Width of the popup list. Percentage values are relative to input width. Default: `'100%'`.

- `query` (Query)
  - External `Query` object executed along with data processing. Default: `null`.

- `readonly` (boolean)
  - Makes the input read-only (allows copy/highlight but not editing). Default: `false`.

- `selectAllText` (string)
  - Label text displayed for the "Select All" option. Default: `'select All'`.

- `showClearButton` (boolean)
  - Shows a close/remove icon on each selected chip. Default: `true`.

- `showDropDownIcon` (boolean)
  - Shows or hides the dropdown arrow button on the component. Default: `false`.

- `showSelectAll` (boolean)
  - Shows or hides the "Select All" option in the dropdown. Default: `false`.

- `sortOrder` (SortOrder)
  - Sort order for the data source. Options: `'None'` | `'Ascending'` | `'Descending'`. Default: `null`.

- `text` (string | null)
  - Selects the list item matching the given display text value. Default: `null`.

- `unSelectAllText` (string)
  - Label text displayed for the "Unselect All" option. Default: `'select All'`.

- `value` (number[] | string[] | boolean[] | object[] | null)
  - Pre-selects list items matching the given value(s). Default: `null`.

- `valueTemplate` (string | Function)
  - Template assigned to the selected item chip displayed inside the input element. Default: `null`.

- `width` (string | number)
  - Width of the component. Default: `'100%'`.

- `zIndex` (number)
  - z-index value of the popup element. Default: `1000`.

## Methods

- `addItem(items, itemIndex?)`
  - Adds a new item to the multiselect popup list.
  - **Parameters:**
    - `items` ({ [key: string]: Object }[] | string | boolean | number | string[] | boolean[] | number[]) — JSON data or array to add.
    - `itemIndex` (number, optional) — Index at which to insert the new item.
  - Returns `void`.

- `clear()`
  - Clears all selected values from the MultiSelect component.
  - Returns `void`.

- `destroy()`
  - Removes the component from the DOM and detaches all related event handlers, attributes, and classes.
  - Returns `void`.

- `disableItem(item)`
  - Disables a specific item in the popup list.
  - **Parameters:**
    - `item` (string | number | object | HTMLLIElement) — The item to disable.
  - Returns `void`.

- `filter(dataSource, query?, fields?)`
  - Filters the multiselect data from a given data source using a query.
  - **Parameters:**
    - `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[]) — Data source to filter.
    - `query` (Query, optional) — Query to filter the data.
    - `fields` (FieldSettingsModel, optional) — Field mappings for the data table.
  - Returns `void`.

- `focusIn()`
  - Sets focus to the component for interaction.
  - Returns `void`.

- `focusOut()`
  - Removes focus from the component if it is currently focused.
  - Returns `void`.

- `getDataByValue(value)`
  - Gets the data object matching the given value.
  - **Parameters:**
    - `value` (string | number | boolean | object) — Value of the list item.
  - Returns `{ [key: string]: Object } | string | number | boolean`.

- `hidePopup(e?)`
  - Hides the popup if it is currently open.
  - **Parameters:**
    - `e` (MouseEvent | KeyboardEventArgs, optional) — Mouse or keyboard event.
  - Returns `void`.

- `hideSpinner()`
  - Hides the spinner loader.
  - Returns `void`.

- `selectAll(state)`
  - Selects or deselects all list items based on the `state` parameter.
  - **Parameters:**
    - `state` (boolean) — `true` to select all; `false` to deselect all.
  - Returns `void`.

- `showPopup(e?)`
  - Shows the popup if it is currently closed.
  - **Parameters:**
    - `e` (MouseEvent | KeyboardEventArgs | TouchEvent, optional) — Mouse, keyboard, or touch event.
  - Returns `void`.

- `showSpinner()`
  - Shows the spinner loader.
  - Returns `void`.

## Events

- `actionBegin` (EmitType\<Object\>)
  - Triggered before fetching data from the remote server.

- `actionComplete` (EmitType\<Object\>)
  - Triggered after data is fetched successfully from the remote server.

- `actionFailure` (EmitType\<Object\>)
  - Triggered when the data fetch request from the remote server fails.

- `beforeOpen` (EmitType\<Object\>)
  - Fires when the popup opens before animation begins.

- `beforeSelectAll` (EmitType\<ISelectAllEventArgs\>)
  - Fires before the select-all process executes.

- `blur` (EmitType\<Object\>)
  - Triggered when the input loses focus.

- `change` (EmitType\<MultiSelectChangeEventArgs\>)
  - Fires each time selection changes in list items after the model and input value are updated.

- `chipSelection` (EmitType\<Object\>)
  - Triggered when a chip (selected item tag) is selected.

- `close` (EmitType\<PopupEventArgs\>)
  - Fires when the popup closes after animation completion.

- `created` (EmitType\<Object\>)
  - Triggered when the component is created.

- `customValueSelection` (EmitType\<CustomValueEventArgs\>)
  - Triggered when a custom value (not in the list) is selected via `allowCustomValue`.

- `dataBound` (EmitType\<Object\>)
  - Triggered when the data source is populated in the popup list.

- `destroyed` (EmitType\<Object\>)
  - Triggered when the component is destroyed.

- `filtering` (EmitType\<FilteringEventArgs\>)
  - Triggered when the user types in the search box. Used to apply custom filtering logic, especially for remote data.

- `focus` (EmitType\<Object\>)
  - Triggered when the input receives focus.

- `open` (EmitType\<PopupEventArgs\>)
  - Fires when the popup opens after animation completion.

- `removed` (EmitType\<RemoveEventArgs\>)
  - Fires after a selected item is removed from the component.

- `removing` (EmitType\<RemoveEventArgs\>)
  - Fires before a selected item is removed from the component.

- `resizeStart` (EmitType\<Object\>)
  - Triggered when the user starts resizing the popup (requires `allowResize: true`).

- `resizeStop` (EmitType\<Object\>)
  - Triggered when the user finishes resizing the popup.

- `resizing` (EmitType\<Object\>)
  - Triggered continuously while the popup is being resized, providing live width/height updates.

- `select` (EmitType\<SelectEventArgs\>)
  - Triggered when an item in the popup is selected via mouse, tap, or keyboard navigation.

- `selectedAll` (EmitType\<ISelectAllEventArgs\>)
  - Fires after the select-all process completes.

- `tagging` (EmitType\<TaggingEventArgs\>)
  - Fires before a selected item is set as a chip in the component. Use this to customize chip content or prevent chip creation.

## Notes
- `CheckBoxSelection` module must be injected via `<Inject services={[CheckBoxSelection]} />` to use `mode="CheckBox"` and `enableGroupCheckBox`.
- `VirtualScroll` module must be injected via `<Inject services={[VirtualScroll]} />` to use `enableVirtualization`.
- Refer to `FieldSettingsModel` for full field mapping options (`text`, `value`, `iconCss`, `groupBy`, `disabled`).
- Event arg types such as `MultiSelectChangeEventArgs`, `SelectEventArgs`, `RemoveEventArgs`, `TaggingEventArgs`, `FilteringEventArgs`, `PopupEventArgs`, `CustomValueEventArgs`, and `ISelectAllEventArgs` are available from `@syncfusion/ej2-react-dropdowns`.
```
