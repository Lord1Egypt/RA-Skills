# ComboBoxComponent API Reference

This file is a focused extraction of the official Syncfusion React ComboBox API. It lists all public properties, methods, and events, along with related interface models.  
Source: https://ej2.syncfusion.com/react/documentation/api/combo-box/index-default

---

## Properties

- `actionFailureTemplate` (string | Function)
  - Accepts the template and assigns it to the popup list content of the component when the data fetch request from the remote server fails. Default: `'Request failed'`.

- `allowCustom` (boolean)
  - Specifies whether the component allows a user-defined value that does not exist in the data source. Default: `true`.

- `allowFiltering` (boolean)
  - When set to `true`, shows the filter bar (search box) in the component. The filter action retrieves matched items through the `filtering` event based on the characters typed in the search TextBox. If no match is found, the value of `noRecordsTemplate` is displayed. Default: `false`.

- `allowObjectBinding` (boolean)
  - Defines whether object binding is allowed in the component. Default: `false`.

- `allowResize` (boolean)
  - Gets or sets a value that indicates whether the ComboBox popup can be resized. When set to `true`, a resize handle appears in the bottom-right corner of the popup, allowing the user to resize its width and height. Default: `false`.

- `autofill` (boolean)
  - Specifies whether to suggest the first matched item in the input when searching. No action occurs when no matches are found. Default: `false`.

- `cssClass` (string)
  - Sets CSS classes to the root element of the component, allowing customization of appearance. Supports multiple classes. Default: `null`.

- `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[])
  - Accepts list items either through local data or a remote service and binds them to the component. Can be an array of JSON objects or an instance of `DataManager`. Default: `[]`.

- `debounceDelay` (number)
  - Specifies the delay time in milliseconds for filtering operations. Default: `300`.

- `enablePersistence` (boolean)
  - Enables persisting component's state between page reloads. The `value` property is persisted. Default: `false`.

- `enableRtl` (boolean)
  - Enables right-to-left rendering of the component. Default: `false`.

- `enableVirtualization` (boolean)
  - Defines whether to enable virtual scrolling in the component. **Requires injecting the `VirtualScroll` module** using `<Inject services={[VirtualScroll]} />` inside the `<ComboBoxComponent>`. Import `Inject` and `VirtualScroll` from `@syncfusion/ej2-react-dropdowns`. Default: `false`.

- `enabled` (boolean)
  - Specifies a value that indicates whether the component is enabled or not. Default: `true`.

- `fields` (FieldSettingsModel)
  - The `fields` property maps the columns of the data table and binds the data to the component. Sub-properties:
    - `text` — Maps the text column from the data table for each list item.
    - `value` — Maps the value column from the data table for each list item.
    - `iconCss` — Maps the icon class column from the data table for each list item.
    - `groupBy` — Groups the list items with related items by mapping the groupBy field.
    - `disabled` — Maps the column that defines whether a specific item is disabled.
    - `htmlAttributes` — Allows additional attributes such as `title`, `disabled`, etc., to configure elements.
  - Default: `{ text: null, value: null, iconCss: null, groupBy: null, disabled: null }`.

- `filterType` (FilterType)
  - Determines the filter type to use during the search action. Options:
    - `'StartsWith'` — Checks whether a value begins with the specified value.
    - `'EndsWith'` — Checks whether a value ends with the specified value.
    - `'Contains'` — Checks whether a value contains the specified value.
  - Default: `'StartsWith'`.

- `floatLabelType` (FloatLabelType)
  - Specifies whether to display the floating label above the input element. Options:
    - `'Never'` — The label will never float when a placeholder is available.
    - `'Always'` — The floating label will always float above the input.
    - `'Auto'` — The floating label will float above the input after focusing or entering a value.
  - Default: `'Never'`.

- `footerTemplate` (string | Function)
  - Accepts the template design and assigns it to the footer container of the popup list. Default: `null`.

- `groupTemplate` (string | Function)
  - Accepts the template design and assigns it to the group headers in the popup list. Default: `null`.

- `headerTemplate` (string | Function)
  - Accepts the template design and assigns it to the header container of the popup list. Default: `null`.

- `htmlAttributes` ({ [key: string]: string })
  - Allows additional HTML attributes such as `title`, `name`, etc., and accepts n number of attributes in a key-value pair format. Default: `{}`.

- `ignoreAccent` (boolean)
  - When set to `true`, ignores diacritic characters or accents when filtering. Default: `false`.

- `ignoreCase` (boolean)
  - When set to `false`, considers case-sensitive matching when performing the search to find suggestions. Default: `true`.

- `index` (number | null)
  - Gets or sets the index of the selected item in the component. Default: `null`.

- `isDeviceFullScreen` (boolean)
  - Defines whether the popup opens in fullscreen mode on mobile devices when filtering is enabled. When set to `false`, the popup displays similarly on both mobile and desktop devices. Default: `true`.

- `itemTemplate` (string | Function)
  - Accepts the template design and assigns it to each list item in the popup. Default: `null`.

- `locale` (string)
  - Overrides the global culture and localization value for this component. Default: `'en-US'`.

- `noRecordsTemplate` (string | Function)
  - Accepts the template design and assigns it to the popup list when no data is available. Default: `'No records found'`.

- `placeholder` (string)
  - Specifies a short hint that describes the expected value of the ComboBox component. Default: `null`.

- `popupHeight` (string | number)
  - Specifies the height of the popup list. Default: `'300px'`.

- `popupWidth` (string | number)
  - Specifies the width of the popup list. By default, the popup width is based on the width of the component. Default: `'100%'`.

- `query` (Query)
  - Accepts an external `Query` that executes along with data processing. Default: `null`.

- `readonly` (boolean)
  - When set to `true`, user interactions on the component are disabled. Default: `false`.

- `showClearButton` (boolean)
  - Specifies whether to show or hide the clear button. When clicked, `value`, `text`, and `index` properties are reset to `null`. Default: `true`.

- `sortOrder` (SortOrder)
  - Specifies the sort order to sort the data source. Options:
    - `'None'` — The data source is not sorted.
    - `'Ascending'` — The data source is sorted in ascending order.
    - `'Descending'` — The data source is sorted in descending order.
  - Default: `null`.

- `text` (string | null)
  - Gets or sets the display text of the selected item in the component. Default: `null`.

- `value` (number | string | boolean | object | null)
  - Gets or sets the value of the selected item in the component. Default: `null`.

- `width` (string | number)
  - Specifies the width of the component. By default, the component width is based on the width of its parent container. Default: `'100%'`.

- `zIndex` (number)
  - Specifies the z-index value of the component popup element. Default: `1000`.

---

## Methods

- `addItem(items, itemIndex?)`
  - Adds a new item to the ComboBox popup list. By default, the new item is appended as the last item, but you can insert it based on the optional index parameter.
  - **Parameters:**
    - `items` ({ [key: string]: Object }[] | { [key: string]: Object } | string | boolean | number | string[] | boolean[] | number[]) — Specifies an array of JSON data or a single JSON data object.
    - `itemIndex` (number, optional) — Specifies the index to place the newly added item in the popup list.
  - Returns `void`.

- `clear()`
  - Allows you to clear the selected values from the component.
  - Returns `void`.

- `destroy()`
  - Removes the component from the DOM and detaches all its related event handlers. Also removes the attributes and classes.
  - Returns `void`.

- `disableItem(item)`
  - Method to disable a specific item in the popup.
  - **Parameters:**
    - `item` (string | number | object | HTMLLIElement) — Specifies the item to be disabled.
  - Returns `void`.

- `filter(dataSource, query?, fields?)`
  - Filters the data from the given data source by using a query.
  - **Parameters:**
    - `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[]) — Sets the data source to filter.
    - `query` (Query, optional) — Specifies the query to filter the data.
    - `fields` (FieldSettingsModel, optional) — Specifies the fields to map the columns in the data table.
  - Returns `void`.

- `focusIn()`
  - Sets the focus to the component for interaction.
  - Returns `void`.

- `focusOut()`
  - Moves the focus from the component if the component is already focused.
  - Returns `void`.

- `getDataByValue(value)`
  - Gets the data object that matches the given value.
  - **Parameters:**
    - `value` (string | number | boolean) — Specifies the value of the list item.
  - Returns `{ [key: string]: Object } | string | number | boolean`.

- `getItems()`
  - Gets all the list items bound to this component.
  - Returns `Element[]`.

- `hidePopup()`
  - Hides the popup if it is in open state.
  - Returns `void`.

- `hideSpinner()`
  - Hides the spinner loader.
  - Returns `void`.

- `showPopup()`
  - Opens the popup that displays the list of items.
  - Returns `void`.

- `showSpinner()`
  - Shows the spinner loader.
  - Returns `void`.

---

## Events

- `actionBegin` (EmitType\<Object\>)
  - Triggered before fetching data from the remote server.

- `actionComplete` (EmitType\<Object\>)
  - Triggered after data is fetched successfully from the remote server.

- `actionFailure` (EmitType\<Object\>)
  - Triggered when the data fetch request from the remote server fails.

- `beforeOpen` (EmitType\<Object\>)
  - Triggered when the popup is about to open, before animation begins.

- `blur` (EmitType\<Object\>)
  - Triggered when the focus moves out of the component.

- `change` (EmitType\<ChangeEventArgs\>)
  - Triggered when an item in the popup is selected or when the model value is changed by the user. Use this event to configure cascading dropdowns.

- `close` (EmitType\<PopupEventArgs\>)
  - Triggered when the popup is closed.

- `created` (EmitType\<Object\>)
  - Triggered when the component is created.

- `customValueSpecifier` (EmitType\<CustomValueSpecifierEventArgs\>)
  - Triggered when a custom value (not in the list) is set in the component. Use `allowCustom: true` to enable this behavior.

- `dataBound` (EmitType\<Object\>)
  - Triggered when the data source is populated in the popup list.

- `destroyed` (EmitType\<Object\>)
  - Triggered when the component is destroyed.

- `filtering` (EmitType\<FilteringEventArgs\>)
  - Triggered when the user types a character in the component. Use this event to apply custom filtering logic, especially for remote data sources.

- `focus` (EmitType\<Object\>)
  - Triggered when the component receives focus.

- `open` (EmitType\<PopupEventArgs\>)
  - Triggered when the popup opens.

- `resizeStart` (EmitType\<Object\>)
  - Triggered when the user starts resizing the popup (requires `allowResize: true`).

- `resizeStop` (EmitType\<Object\>)
  - Triggered when the user finishes resizing the popup.

- `resizing` (EmitType\<Object\>)
  - Triggered continuously while the popup is being resized by the user, providing live updates on the width and height of the popup.

- `select` (EmitType\<SelectEventArgs\>)
  - Triggered when an item in the popup is selected by the user via mouse, tap, or keyboard navigation.

---

## Related Interface Models

### FieldSettingsModel

Interface for mapping data columns to the ComboBox component.

| Property | Type | Description |
|---|---|---|
| `text` | string | Maps the text column from the data table for each list item. |
| `value` | string | Maps the value column from the data table for each list item. |
| `iconCss` | string | Maps the icon class column from the data table for each list item. |
| `groupBy` | string | Groups the list items with related items by mapping this field. |
| `disabled` | string | Defines whether a particular field value is disabled or not. |
| `htmlAttributes` | string | Allows additional attributes such as `title`, `disabled`, etc., to configure elements. |

---

### ChangeEventArgs

Event arguments for the `change` event.

| Property | Type | Description |
|---|---|---|
| `cancel` | boolean | Illustrates whether the current action needs to be prevented or not. |
| `e` | MouseEvent \| KeyboardEvent \| TouchEvent | Specifies the original event arguments. |
| `element` | HTMLElement | Returns the root element of the component. |
| `event` | MouseEvent \| KeyboardEvent \| TouchEvent | Specifies the original event arguments. |
| `isInteracted` | boolean | Returns `true` if the event was triggered by user interaction, otherwise `false`. |
| `item` | HTMLLIElement | Returns the selected list item element. |
| `itemData` | FieldSettingsModel | Returns the selected item as a JSON object from the data source. |
| `previousItem` | HTMLLIElement | Returns the previously selected list item element. |
| `previousItemData` | FieldSettingsModel | Returns the previously selected item as a JSON object from the data source. |
| `value` | number \| string \| boolean \| object | Returns the selected value. |

---

### SelectEventArgs

Event arguments for the `select` event.

| Property | Type | Description |
|---|---|---|
| `cancel` | boolean | Illustrates whether the current action needs to be prevented or not. |
| `e` | MouseEvent \| KeyboardEvent \| TouchEvent | Specifies the original event arguments. |
| `isInteracted` | boolean | Returns `true` if the event was triggered by user interaction, otherwise `false`. |
| `item` | HTMLLIElement | Returns the selected list item element. |
| `itemData` | FieldSettingsModel | Returns the selected item as a JSON object from the data source. |

---

### FilteringEventArgs

Event arguments for the `filtering` event.

| Property | Type | Description |
|---|---|---|
| `baseEventArgs` | Object | Gets the `keyup` event arguments. |
| `cancel` | boolean | Illustrates whether the current action needs to be prevented or not. |
| `preventDefaultAction` | boolean | Set to `true` to prevent the internal filtering action. |
| `text` | string | The search text value typed by the user. |

**Methods on FilteringEventArgs:**

- `updateData(dataSource, query?, fields?)`
  - Filters the data from the given data source using a query.
  - **Parameters:**
    - `dataSource` ({ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[]) — Sets the data source to filter.
    - `query` (Query, optional) — Specifies the query to filter the data.
    - `fields` (FieldSettingsModel, optional) — Specifies the fields to map the columns in the data table.
  - Returns `void`.

---

### PopupEventArgs

Event arguments for the `open`, `close`, and `beforeOpen` events.

| Property | Type | Description |
|---|---|---|
| `animation` | AnimationModel | Specifies the animation object applied to the popup. |
| `cancel` | boolean | Illustrates whether the current action needs to be prevented or not. |
| `event` | MouseEvent \| KeyboardEventArgs \| TouchEvent \| Object | Specifies the event that triggered the popup action. |
| `popup` | Popup | Specifies the popup object instance. |

---

### CustomValueSpecifierEventArgs

Event arguments for the `customValueSpecifier` event.

| Property | Type | Description |
|---|---|---|
| `item` | { [key: string]: string \| Object } | Sets the text custom format data for assigning `value` and `text`. |
| `text` | string | Gets the typed custom text to create a custom text format and assign it to the `item` argument. |

---

## Notes

- To use `enableVirtualization`, inject the `VirtualScroll` module. Always place `<Inject services={[VirtualScroll]} />` as a child of `<ComboBoxComponent>`:

  **Functional Component:**
  ```tsx
  import { ComboBoxComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

  export default function App() {
    const records = Array.from({ length: 150 }, (_, i) => ({
      id: 'id' + (i + 1),
      text: `Item ${i + 1}`,
    }));
    const fields = { text: 'text', value: 'id' };

    return (
      <ComboBoxComponent
        id="datas"
        dataSource={records}
        fields={fields}
        placeholder="e.g. Item 1"
        enableVirtualization={true}
        allowFiltering={false}
        popupHeight="200px"
      >
        <Inject services={[VirtualScroll]} />
      </ComboBoxComponent>
    );
  }
  ```

  **Class Component:**
  ```tsx
  import { ComboBoxComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';
  import * as React from 'react';
  import * as ReactDOM from 'react-dom';

  export default class App extends React.Component {
    constructor(props) {
      super(props);
      this.records = Array.from({ length: 150 }, (_, i) => ({
        id: 'id' + (i + 1),
        text: `Item ${i + 1}`,
      }));
    }
    fields = { text: 'text', value: 'id' };

    render() {
      return (
        <ComboBoxComponent
          id="datas"
          dataSource={this.records}
          fields={this.fields}
          placeholder="e.g. Item 1"
          enableVirtualization={true}
          allowFiltering={false}
          popupHeight="200px"
        >
          <Inject services={[VirtualScroll]} />
        </ComboBoxComponent>
      );
    }
  }

  ReactDOM.render(<App />, document.getElementById('sample'));
  ```
- Event argument types (`ChangeEventArgs`, `SelectEventArgs`, `FilteringEventArgs`, `PopupEventArgs`, `CustomValueSpecifierEventArgs`) are importable from `@syncfusion/ej2-react-dropdowns`.
- The `customValueSpecifier` event requires `allowCustom: true` to be effective.
- The `filtering` event requires `allowFiltering: true` to be triggered.
- Use `autofill: true` together with `allowFiltering: true` for auto-complete behavior.
