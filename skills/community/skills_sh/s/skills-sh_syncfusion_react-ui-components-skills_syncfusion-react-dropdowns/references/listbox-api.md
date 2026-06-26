````markdown
```markdown
# ListBoxComponent API

This file is a focused extraction of the official Syncfusion React ListBox API. It lists all public properties, methods, and events. Source: https://ej2.syncfusion.com/react/documentation/api/list-box/index-default

## Properties

- `allowDragAndDrop` (boolean)
  - When `true`, enables drag-and-drop reordering of list items. ListBoxes sharing the same `scope` value can drag-and-drop items between each other. Default: `false`.

- `allowFiltering` (boolean)
  - Enables the filtering/search option in the component. The `filtering` event fires when text is typed in the search box. If no match is found, `noRecordsTemplate` is shown. Default: `false`.

- `cssClass` (string)
  - Sets CSS classes on the root element to customize the component styles. Default: `''`.

- `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[])
  - Accepts list items via a local array of JSON objects, primitive arrays, or a remote `DataManager` instance. Default: `[]`.

- `enablePersistence` (boolean)
  - Enables persisting the component's `value` state between page reloads. Default: `false`.

- `enableRtl` (boolean)
  - Enables right-to-left rendering of the component. Default: `false`.

- `enabled` (boolean)
  - Specifies whether the component is enabled or disabled. Default: `true`.

- `fields` (FieldSettingsModel)
  - Maps data table columns to the component. Key sub-properties:
    - `text` (string) — Maps the text column from the data table for each list item.
    - `value` (string) — Maps the value column from the data table for each list item.
    - `iconCss` (string) — Maps the icon CSS class column from the data table for each list item.
    - `groupBy` (string) — Groups list items with related items by mapping the groupBy field.
    - `disabled` (string) — Defines whether a particular field value is disabled or not.
    - `htmlAttributes` (string) — Allows additional attributes such as `title`, `disabled`, etc., to configure elements.
  - Default: `{ text: null, value: null, iconCss: null, groupBy: null, disabled: null }`.

- `filterBarPlaceholder` (string)
  - Watermark text displayed in the filter search bar. Default: `null`.

- `filterType` (FilterType)
  - Determines the filter strategy applied during search. Options:
    - `'StartsWith'` — Checks whether a value begins with the specified value. Supported for `string` types.
    - `'EndsWith'` — Checks whether a value ends with the specified value. Supported for `string` types.
    - `'Contains'` — Checks whether a value contains the specified value. Supported for `string` types.
  - Default: `'StartsWith'`.

- `height` (number | string)
  - Sets the height of the ListBox component. Default: `''`.

- `itemTemplate` (string | Function)
  - Template design assigned to each list item in the list. Supports template strings or executable functions. Default: `null`.

- `locale` (string)
  - Overrides the global culture and localization value for this component. Default: `'en-US'`.

- `maximumSelectionLength` (number)
  - Limits the number of items that can be selected. Selection is prevented once the limit is reached. Default: `1000`.

- `noRecordsTemplate` (string | Function)
  - Template displayed in the list when no data is available or no matching records are found. Default: `'No records found'`.

- `query` (Query)
  - External `Query` object executed along with the data processing. Default: `null`.

- `scope` (string)
  - Defines the scope value to group sets of draggable and droppable ListBoxes. A draggable item with the same scope value is accepted by the droppable ListBox. Default: `''`.

- `selectionSettings` (SelectionSettingsModel)
  - Specifies the selection mode and type. Key sub-properties:
    - `mode` (SelectionMode) — Selection mode: `'Single'` | `'Multiple'`. Default: `'Multiple'`.
    - `type` (SelectionType) — Selection type. Default: `'Default'`.
    - `showCheckbox` (boolean) — When `true`, renders a checkbox alongside each list item. **Requires injecting the `CheckBoxSelection` service** (see example below). Default: `false`.
    - `showSelectAll` (boolean) — Shows or hides the "Select All" option. Default: `false`.
    - `checkboxPosition` (CheckBoxPosition) — Sets the position of the checkbox.
  - Default: `{ mode: 'Multiple', type: 'Default' }`.

- `sortOrder` (SortOrder)
  - Specifies the sort order applied to the data source. Options:
    - `'None'` — Data source is not sorted.
    - `'Ascending'` — Data source is sorted in ascending order.
    - `'Descending'` — Data source is sorted in descending order.
  - Default: `null`.

- `toolbarSettings` (ToolbarSettingsModel)
  - Specifies the toolbar items and their position for dual ListBox operations. Key sub-properties:
    - `items` (string[]) — List of toolbar tools. Predefined tools: `'moveUp'`, `'moveDown'`, `'moveTo'`, `'moveFrom'`, `'moveAllTo'`, `'moveAllFrom'`.
    - `position` (ToolBarPosition) — Positions the toolbar relative to the ListBox: `'Left'` | `'Right'`.
  - Default: `{ items: [], position: 'Right' }`.

- `value` (string[] | number[] | boolean[])
  - Sets the specified item(s) to the selected state or retrieves the currently selected item(s) in the ListBox. Default: `[]`.

## Methods

- `addItems(items, itemIndex?)`
  - Adds a new item or array of items to the list. By default, appends to the end of the list, but can be inserted at a specific index.
  - **Parameters:**
    - `items` (obj[] | obj) — Specifies an array of JSON data or a single JSON data object.
    - `itemIndex` (number, optional) — Specifies the index at which to place the newly added item.
  - Returns `void`.

- `enableItems(items, enable?, isValue?)`
  - Enables or disables items in the ListBox based on the provided item texts (or values) and the `enable` argument.
  - **Parameters:**
    - `items` (string[]) — Text items to enable or disable.
    - `enable` (boolean, optional) — Set `true` to enable, `false` to disable the items.
    - `isValue` (boolean, optional) — Set `true` if the `items` parameter is an array of unique values instead of text.
  - Returns `void`.

- `filter(dataSource, query?, fields?)`
  - Filters data from the given data source using a query.
  - **Parameters:**
    - `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[]) — The data source to filter.
    - `query` (Query, optional) — Query to filter the data.
    - `fields` (FieldSettingsModel, optional) — Field mappings for the data table columns.
  - Returns `void`.

- `getDataByValue(value)`
  - Gets the data object that matches the given value.
  - **Parameters:**
    - `value` (string | number | boolean | object) — Specifies the value of the list item.
  - Returns `{ [key: string]: Object } | string | number | boolean`.

- `getDataByValues(value)`
  - Gets an array of data objects that match the given array of values.
  - **Parameters:**
    - `value` (string[] | number[] | boolean[]) — Specifies the array of values for the list items.
  - Returns `{ [key: string]: Object }[]`.

- `getDataList()`
  - Gets the updated data source currently bound to the ListBox.
  - Returns `{ [key: string]: Object }[] | string[] | boolean[] | number[]`.

- `getItems()`
  - Gets all list item elements currently rendered in the component.
  - Returns `Element[]`.

- `getSortedList()`
  - Returns the sorted data currently in the ListBox.
  - Returns `{ [key: string]: Object }[] | string[] | boolean[] | number[]`.

- `moveAllTo(targetId?, index?)`
  - Moves all values from the current ListBox to the scoped ListBox.
  - **Parameters:**
    - `targetId` (string, optional) — Specifies the ID of the scoped target ListBox.
    - `index` (number, optional) — Specifies the index position where items are moved in the target.
  - Returns `void`.

- `moveBottom(value?)`
  - Moves the given value(s) or currently selected value(s) to the bottom of the list.
  - **Parameters:**
    - `value` (string[] | number[] | boolean[], optional) — Specifies the value(s) to move.
  - Returns `void`.

- `moveDown(value?)`
  - Moves the given value(s) or currently selected value(s) one position downwards.
  - **Parameters:**
    - `value` (string[] | number[] | boolean[], optional) — Specifies the value(s) to move.
  - Returns `void`.

- `moveTo(value?, index?, targetId?)`
  - Moves the given value(s) or currently selected value(s) to the given or default scoped ListBox.
  - **Parameters:**
    - `value` (string[] | number[] | boolean[], optional) — Specifies the value or array of values of the list items to move.
    - `index` (number, optional) — Specifies the index position in the target where items are inserted.
    - `targetId` (string, optional) — Specifies the ID of the target ListBox.
  - Returns `void`.

- `moveTop(value?)`
  - Moves the given value(s) or currently selected value(s) to the top of the list.
  - **Parameters:**
    - `value` (string[] | number[] | boolean[], optional) — Specifies the value(s) to move.
  - Returns `void`.

- `moveUp(value?)`
  - Moves the given value(s) or currently selected value(s) one position upwards.
  - **Parameters:**
    - `value` (string[] | number[] | boolean[], optional) — Specifies the value(s) to move.
  - Returns `void`.

- `removeItem(items?, itemIndex?)`
  - Removes a single item from the list. By default removes the last item, but can remove based on index or item reference.
  - **Parameters:**
    - `items` ({ [key: string]: Object }[] | { [key: string]: Object } | string | boolean | number | string[] | boolean[] | number[], optional) — Specifies the JSON data, array of JSON data, or primitive value(s) to remove.
    - `itemIndex` (number, optional) — Specifies the index of the item to remove.
  - Returns `void`.

- `removeItems(items?, itemIndex?)`
  - Removes items from the list. By default removes the last item, but can remove based on index.
  - **Parameters:**
    - `items` (obj[] | obj, optional) — Specifies an array of JSON data or a single JSON data object.
    - `itemIndex` (number, optional) — Specifies the index of the item to remove.
  - Returns `void`.

- `selectAll(state?)`
  - Selects or deselects all list items based on the `state` parameter.
  - **Parameters:**
    - `state` (boolean, optional) — Set `true` to select all items; `false` to deselect all items.
  - Returns `void`.

- `selectItems(items, state?, isValue?)`
  - Selects or deselects specified list items based on the `state` parameter.
  - **Parameters:**
    - `items` (string[]) — Array of text values of the items to select/deselect.
    - `state` (boolean, optional) — Set `true` to select, `false` to deselect the specified items.
    - `isValue` (boolean, optional) — Set `true` if the `items` parameter is an array of unique values instead of text.
  - Returns `void`.

## Events

- `actionBegin` (EmitType\<Object\>)
  - Triggered before fetching data from the remote server.

- `actionComplete` (EmitType\<Object\>)
  - Triggered after data is fetched successfully from the remote server.

- `actionFailure` (EmitType\<Object\>)
  - Triggered when the data fetch request from the remote server fails.

- `beforeDrop` (EmitType\<DropEventArgs\>)
  - Triggered before dropping the list item onto another list item. Event args:
    - `cancel` (boolean) — Set `true` to prevent the drop action.
    - `currentIndex` (number) — Returns the current index of the selected list item.
    - `droppedElement` (Element) — Returns the selected list element to be dropped.
    - `helper` (Element) — Returns the dragged list element.
    - `items` (Object[]) — Returns the selected list items.
    - `previousIndex` (number) — Returns the previous index of the selected list item.
    - `target` (Element) — Returns the target list element where the item will be dropped.

- `beforeItemRender` (EmitType\<BeforeItemRenderEventArgs\>)
  - Triggered while rendering each list item. Event args:
    - `element` (Element) — Returns the list element before rendering.
    - `item` ({ [key: string]: Object }) — Returns the list item data before rendering.
    - `name` (string) — Specifies the name of the event.

- `change` (EmitType\<ListBoxChangeEventArgs\>)
  - Triggered when a list item is selected or unselected. Event args:
    - `elements` (Element[]) — Returns the selected list elements.
    - `event` (Event) — Specifies the native event.
    - `items` (Object[]) — Returns the selected list items.
    - `name` (string) — Specifies the name of the event.
    - `value` (number[] | string[] | boolean[]) — Returns the selected state or selected list item values.

- `created` (EmitType\<Object\>)
  - Triggered when the component is created.

- `dataBound` (EmitType\<Object\>)
  - Triggered when the data source is populated in the list.

- `destroyed` (EmitType\<Object\>)
  - Triggered when the component is destroyed.

- `drag` (EmitType\<DragEventArgs\>)
  - Triggered while dragging a list item. Event args:
    - `cancel` (boolean) — Set `true` to prevent the drag action.
    - `currentIndex` (number) — Returns the current index of the selected list item.
    - `destination` (SourceDestinationModel) — Returns the previous and current list items of the destination ListBox. Contains `previousData` and `currentData`.
    - `dragSelected` (boolean) — Returns `true` if the list element is dragged from the ListBox; otherwise `false`.
    - `elements` (Element[]) — Returns the selected list elements.
    - `event` (Event) — Specifies the native event.
    - `items` (Object[]) — Returns the selected list items.
    - `previousIndex` (number) — Returns the previous index of the selected list item.
    - `previousItem` (object[]) — Returns the previous list item data.
    - `source` (SourceDestinationModel) — Returns the previous and current list items of the source ListBox. Contains `previousData` and `currentData`.
    - `target` (Element) — Returns the target list element where the dragged item will be dropped.

- `dragStart` (EmitType\<DragEventArgs\>)
  - Triggered after initiating the drag of a list item. Uses the same `DragEventArgs` as the `drag` event.

- `drop` (EmitType\<DragEventArgs\>)
  - Triggered before dropping the list item onto another list item. Uses the same `DragEventArgs` as the `drag` event.

- `filtering` (EmitType\<FilteringEventArgs\>)
  - Triggered when a character is typed in the filter search box. Event args:
    - `baseEventArgs` (Object) — Gets the native `keyup` event arguments.
    - `cancel` (boolean) — Set `true` to prevent the filtering action.
    - `preventDefaultAction` (boolean) — Set `true` to prevent the internal default filtering action.
    - `text` (string) — The current search text value entered in the filter bar.
    - `updateData(dataSource, query?, fields?)` (method) — Filters the data from the given data source using a query. Use this in the `filtering` event handler to apply custom remote filtering.

## Sub-Interfaces

### SelectionSettingsModel
Interface for the `selectionSettings` property.

| Property | Type | Description |
|---|---|---|
| `checkboxPosition` | CheckBoxPosition | Sets the position of the checkbox. |
| `mode` | SelectionMode | Selection mode: `'Single'` or `'Multiple'`. |
| `showCheckbox` | boolean | When `true`, renders a checkbox for each list item. Requires injecting `CheckBoxSelection` service. |
| `showSelectAll` | boolean | Shows or hides the "Select All" option. |

### ToolbarSettingsModel
Interface for the `toolbarSettings` property.

| Property | Type | Description |
|---|---|---|
| `items` | string[] | List of toolbar tools. Predefined values: `'moveUp'`, `'moveDown'`, `'moveTo'`, `'moveFrom'`, `'moveAllTo'`, `'moveAllFrom'`. |
| `position` | ToolBarPosition | Positions the toolbar: `'Left'` or `'Right'`. |

### FieldSettingsModel
Interface for the `fields` property.

| Property | Type | Description |
|---|---|---|
| `disabled` | string | Maps the column that determines whether each item is disabled. |
| `groupBy` | string | Maps the column used to group list items. |
| `htmlAttributes` | string | Maps the column for additional HTML attributes (e.g., `title`, `disabled`). |
| `iconCss` | string | Maps the column for the icon CSS class for each list item. |
| `text` | string | Maps the column displayed as the text for each list item. |
| `value` | string | Maps the column used as the value for each list item. |

### SourceDestinationModel
Interface used within `DragEventArgs` for both `source` and `destination`.

| Property | Type | Description |
|---|---|---|
| `currentData` | string[] \| boolean[] \| number[] \| { [key: string]: Object }[] \| DataManager | List items after the drag or drop action. |
| `previousData` | string[] \| boolean[] \| number[] \| { [key: string]: Object }[] \| DataManager | List items before the drag or drop action. |

## Notes
- Use `scope` property to enable drag-and-drop between multiple ListBox components.
- The `toolbarSettings.items` array supports predefined tool names: `'moveUp'`, `'moveDown'`, `'moveTo'`, `'moveFrom'`, `'moveAllTo'`, `'moveAllFrom'`.
- Event arg types such as `ListBoxChangeEventArgs`, `DragEventArgs`, `DropEventArgs`, `BeforeItemRenderEventArgs`, and `FilteringEventArgs` are available from `@syncfusion/ej2-react-dropdowns`.
- The `filtering` event's `updateData()` method is used for custom remote filtering by passing a custom data source and query.
- `selectionSettings.showCheckbox` renders checkboxes alongside items; combine with `selectionSettings.showSelectAll` for a "select all" control. **When `showCheckbox` is `true`, you must inject the `CheckBoxSelection` service:**
```tsx
import { ListBoxComponent, SelectionSettingsModel, Inject, CheckBoxSelection } from '@syncfusion/ej2-react-dropdowns';

const selectionSettings: SelectionSettingsModel = { showCheckbox: true };

<ListBoxComponent dataSource={data} selectionSettings={selectionSettings}>
  <Inject services={[CheckBoxSelection]} />
</ListBoxComponent>
```
```
````
