# Syncfusion React DropDownList – API Reference

> **Source:** https://ej2.syncfusion.com/react/documentation/api/drop-down-list/index-default  
> **Package:** `@syncfusion/ej2-react-dropdowns`  
> **Selector / Import:** `<DropDownListComponent>` from `@syncfusion/ej2-react-dropdowns`

---

## Table of Contents

- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Interface: FieldSettingsModel](#interface-fieldsettingsmodel)
- [Interface: ChangeEventArgs](#interface-changeeventargs)
- [Interface: SelectEventArgs](#interface-selecteventargs)
- [Interface: PopupEventArgs](#interface-popupeventargs)
- [Interface: FilteringEventArgs](#interface-filteringeventargs)

---

## Properties

### `actionFailureTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `'Request failed'` |

Accepts a template and assigns it to the popup list content when the data fetch request from the remote server fails.

---

### `allowFiltering`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

When set to `true`, shows the filter bar (search box) inside the popup. The filter action retrieves matched items through the `filtering` event based on the characters typed in the search TextBox. If no match is found, the value of the `noRecordsTemplate` property is displayed.

```tsx
<DropDownListComponent dataSource={data} allowFiltering={true} />
```

---

### `allowObjectBinding`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

Defines whether object binding is allowed in the component.

---

### `allowResize`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

When set to `true`, a resize handle appears in the bottom-right corner of the popup, allowing the user to resize the popup width and height.

---

### `cssClass`
| Detail | Value |
|---|---|
| **Type** | `string` |
| **Default** | `null` |

Sets CSS classes on the root element of the component, allowing customization of appearance.

```tsx
<DropDownListComponent cssClass="e-custom-style" dataSource={data} />
```

---

### `dataSource`
| Detail | Value |
|---|---|
| **Type** | `{ [key: string]: Object }[] \| DataManager \| string[] \| number[] \| boolean[]` |
| **Default** | `[]` |

Accepts list items either through a local or remote service and binds them to the component. Can be an array of JSON objects or a `DataManager` instance.

```tsx
// Local string array
<DropDownListComponent dataSource={['Cricket', 'Football', 'Tennis']} />

// JSON object array
<DropDownListComponent dataSource={countryData} fields={{ text: 'Name', value: 'Code' }} />

// Remote DataManager
<DropDownListComponent
  dataSource={new DataManager({ url: 'url', adaptor: new WebApiAdaptor() })}
  fields={{ text: 'Name', value: 'Id' }}
/>
```

---

### `debounceDelay`
| Detail | Value |
|---|---|
| **Type** | `number` |
| **Default** | `300` |

Specifies the delay time in milliseconds applied to filtering operations before the filter query is executed.

---

### `enablePersistence`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

When enabled, the component persists its state (specifically the `value`) between page reloads.

---

### `enableRtl`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

Enables right-to-left (RTL) rendering of the component.

---

### `enableVirtualization`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

Enables virtual scrolling in the component. Use this for large datasets (10,000+ items) to improve rendering performance. Requires the `VirtualScroll` module to be injected.

```tsx
import { DropDownListComponent, Inject, VirtualScroll } from '@syncfusion/ej2-react-dropdowns';

<DropDownListComponent dataSource={largeData} enableVirtualization={true}>
  <Inject services={[VirtualScroll]} />
</DropDownListComponent>
```

---

### `enabled`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

Specifies whether the component is enabled. When set to `false`, the component is disabled and user interactions are blocked.

---

### `fields`
| Detail | Value |
|---|---|
| **Type** | `FieldSettingsModel` |
| **Default** | `{ text: null, value: null, iconCss: null, groupBy: null, disabled: null }` |

Maps the columns of the data source to the component properties:
- `text` – Display text for each list item.
- `value` – Value for each list item.
- `iconCss` – CSS class for item icons.
- `groupBy` – Groups related list items together.
- `disabled` – Marks specific items as disabled.

```tsx
const fields = { text: 'ContactName', value: 'CustomerID', groupBy: 'Region', iconCss: 'FlagIcon' };
<DropDownListComponent dataSource={customers} fields={fields} />
```

---

### `filterBarPlaceholder`
| Detail | Value |
|---|---|
| **Type** | `string` |
| **Default** | `null` |

Accepts the value to display as watermark text on the filter bar when `allowFiltering` is enabled.

---

### `filterType`
| Detail | Value |
|---|---|
| **Type** | `FilterType` |
| **Default** | `'StartsWith'` |

Determines the filter type used when searching. Supported values:

| FilterType | Description | Supported Data Types |
|---|---|---|
| `StartsWith` | Checks whether a value begins with the specified value | `String` |
| `EndsWith` | Checks whether a value ends with the specified value | `String` |
| `Contains` | Checks whether a value contains the specified value | `String` |

```tsx
<DropDownListComponent dataSource={data} allowFiltering={true} filterType="Contains" />
```

---

### `floatLabelType`
| Detail | Value |
|---|---|
| **Type** | `FloatLabelType` |
| **Default** | `'Never'` |

Specifies the behavior of the floating label. Possible values:
- `'Never'` – The label never floats.
- `'Always'` – The label always floats above the input.
- `'Auto'` – The label floats after focusing or entering a value.

---

### `footerTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `null` |

Accepts a template and assigns it to the footer container of the popup list.

```tsx
<DropDownListComponent dataSource={data} footerTemplate={'<div class="footer">Total items: 5</div>'} />
```

---

### `groupTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `null` |

Accepts a template and assigns it to the group headers present in the popup list.

---

### `headerTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `null` |

Accepts a template and assigns it to the header container of the popup list.

```tsx
<DropDownListComponent dataSource={data} headerTemplate={'<div class="header"><b>Country Name</b></div>'} />
```

---

### `htmlAttributes`
| Detail | Value |
|---|---|
| **Type** | `{ [key: string]: string }` |
| **Default** | `{}` |

Allows additional HTML attributes (e.g., `title`, `name`) on the component's root element in key-value pair format.

```tsx
const htmlAttributes = { name: 'country', title: 'DropDownList', placeholder: 'Select a country' };
<DropDownListComponent dataSource={data} htmlAttributes={htmlAttributes} />
```

---

### `ignoreAccent`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

When set to `true`, diacritic characters (accents) are ignored during filtering, enabling accent-insensitive search.

---

### `ignoreCase`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

When set to `false`, filtering becomes case-sensitive. By default, filtering ignores case.

---

### `index`
| Detail | Value |
|---|---|
| **Type** | `number \| null` |
| **Default** | `null` |

Gets or sets the index of the selected item in the component. Zero-based.

```tsx
<DropDownListComponent dataSource={data} index={2} />
```

---

### `isDeviceFullScreen`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `true` |

Defines whether the popup opens in full-screen mode on mobile devices when filtering is enabled. When set to `false`, the popup displays similarly on both mobile and desktop devices.

---

### `itemTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `null` |

Accepts a template and assigns it to each list item in the popup, allowing custom item rendering.

```tsx
const itemTemplate = '<div><span class="${iconCss}"></span> ${text}</div>';
<DropDownListComponent dataSource={data} itemTemplate={itemTemplate} />
```

---

### `locale`
| Detail | Value |
|---|---|
| **Type** | `string` |
| **Default** | `'en-US'` |

Overrides the global culture and localization value for this component.

---

### `noRecordsTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `'No records found'` |

Accepts a template and assigns it to the popup list when no data is available.

```tsx
<DropDownListComponent dataSource={[]} noRecordsTemplate={'<div>No data available</div>'} />
```

---

### `placeholder`
| Detail | Value |
|---|---|
| **Type** | `string` |
| **Default** | `null` |

Specifies a short hint that describes the expected value of the DropDownList component.

```tsx
<DropDownListComponent dataSource={data} placeholder="Select a country" />
```

---

### `popupHeight`
| Detail | Value |
|---|---|
| **Type** | `string \| number` |
| **Default** | `'300px'` |

Specifies the height of the popup list.

```tsx
<DropDownListComponent dataSource={data} popupHeight="200px" />
```

---

### `popupWidth`
| Detail | Value |
|---|---|
| **Type** | `string \| number` |
| **Default** | `'100%'` |

Specifies the width of the popup list. By default, the popup width matches the width of the component.

```tsx
<DropDownListComponent dataSource={data} popupWidth="250px" />
```

---

### `query`
| Detail | Value |
|---|---|
| **Type** | `Query` |
| **Default** | `null` |

Accepts an external `Query` object to execute along with data processing (e.g., filtering, sorting, taking a subset of remote data).

```tsx
import { Query, DataManager, WebApiAdaptor } from '@syncfusion/ej2-data';

const dataSource = new DataManager({
  url: 'url',
  adaptor: new WebApiAdaptor(),
  crossDomain: true
});
const query = new Query().select(['FirstName', 'EmployeeID']).take(10).requiresCount();

<DropDownListComponent
  dataSource={dataSource}
  fields={{ text: 'FirstName', value: 'EmployeeID' }}
  query={query}
  placeholder="Select a name"
/>
```

---

### `readonly`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

When set to `true`, user interactions on the component are disabled (read-only mode). The dropdown displays the current value but cannot be changed.

---

### `showClearButton`
| Detail | Value |
|---|---|
| **Type** | `boolean` |
| **Default** | `false` |

Specifies whether to show or hide the clear (✕) button. When clicked, the `value`, `text`, and `index` properties are reset to `null`.

```tsx
<DropDownListComponent dataSource={data} showClearButton={true} />
```

---

### `sortOrder`
| Detail | Value |
|---|---|
| **Type** | `SortOrder` |
| **Default** | `null` |

Specifies the sort order for the data source. Available values:
- `'None'` – Data source is not sorted.
- `'Ascending'` – Data source is sorted in ascending order.
- `'Descending'` – Data source is sorted in descending order.

```tsx
<DropDownListComponent dataSource={data} sortOrder="Ascending" />
```

---

### `text`
| Detail | Value |
|---|---|
| **Type** | `string \| null` |
| **Default** | `null` |

Gets or sets the display text of the selected item in the component.

---

### `value`
| Detail | Value |
|---|---|
| **Type** | `number \| string \| boolean \| object \| null` |
| **Default** | `null` |

Gets or sets the value of the selected item in the component.

```tsx
<DropDownListComponent dataSource={data} value="Cricket" />
```

---

### `valueTemplate`
| Detail | Value |
|---|---|
| **Type** | `string \| Function` |
| **Default** | `null` |

Accepts a template and assigns it to the selected list item displayed in the input element of the component.

```tsx
const valueTemplate = '<span><img src="${flag}" width="20" /> ${text}</span>';
<DropDownListComponent dataSource={data} valueTemplate={valueTemplate} />
```

---

### `width`
| Detail | Value |
|---|---|
| **Type** | `string \| number` |
| **Default** | `'100%'` |

Specifies the width of the component. By default it matches the width of its parent container. Can be set to pixel or percentage values.

```tsx
<DropDownListComponent dataSource={data} width="250px" />
```

---

### `zIndex`
| Detail | Value |
|---|---|
| **Type** | `number` |
| **Default** | `1000` |

Specifies the z-index value of the component's popup element.

---

## Methods

### `addItem`

Adds a new item to the popup list. By default the new item is appended as the last item, but it can be inserted at a specific position using the `itemIndex` parameter.

**Signature:**
```ts
addItem(
  items: { [key: string]: Object }[] | { [key: string]: Object } | string | boolean | number | string[] | boolean[] | number[],
  itemIndex?: number
): void
```

| Parameter | Type | Description |
|---|---|---|
| `items` | `Object[] \| string \| boolean \| number \| ...` | Specifies an array of JSON data or a single JSON data item to add. |
| `itemIndex` *(optional)* | `number` | Specifies the index at which to insert the new item. |

**Returns:** `void`

```tsx
// Append to end
ddlRef.current.addItem({ text: 'Golf', value: 'golf' });

// Insert at index 1
ddlRef.current.addItem({ text: 'Golf', value: 'golf' }, 1);
```

---

### `clear`

Clears the selected value from the component, resetting `value`, `text`, and `index` to `null`.

**Signature:**
```ts
clear(): void
```

**Returns:** `void`

```tsx
ddlRef.current.clear();
```

---

### `destroy`

Removes the component from the DOM and detaches all related event handlers. Also removes added attributes and classes.

**Signature:**
```ts
destroy(): void
```

**Returns:** `void`

---

### `disableItem`

Disables a specific item in the popup list.

**Signature:**
```ts
disableItem(item: string | number | object | HTMLLIElement): void
```

| Parameter | Type | Description |
|---|---|---|
| `item` | `string \| number \| object \| HTMLLIElement` | Specifies the item to be disabled. |

**Returns:** `void`

```tsx
ddlRef.current.disableItem('Cricket');
```

---

### `filter`

Filters the data from the given data source using a query.

**Signature:**
```ts
filter(
  dataSource: { [key: string]: Object }[] | DataManager | string[] | number[] | boolean[],
  query?: Query,
  fields?: FieldSettingsModel
): void
```

| Parameter | Type | Description |
|---|---|---|
| `dataSource` | `Object[] \| DataManager \| string[] \| ...` | The data source to filter. |
| `query` *(optional)* | `Query` | A query to apply when filtering. |
| `fields` *(optional)* | `FieldSettingsModel` | Field mapping for the data table columns. |

**Returns:** `void`

---

### `focusIn`

Sets the focus on the component for interaction.

**Signature:**
```ts
focusIn(): void
```

**Returns:** `void`

---

### `focusOut`

Moves focus away from the component if it is currently focused.

**Signature:**
```ts
focusOut(): void
```

**Returns:** `void`

---

### `getDataByValue`

Gets the data object that matches the given value.

**Signature:**
```ts
getDataByValue(value: string | number | boolean): { [key: string]: Object } | string | number | boolean
```

| Parameter | Type | Description |
|---|---|---|
| `value` | `string \| number \| boolean` | The value of the list item to retrieve. |

**Returns:** `{ [key: string]: Object } | string | number | boolean`

```tsx
const itemData = ddlRef.current.getDataByValue('au'); // returns { Id: 'au', Country: 'Australia' }
```

---

### `getItems`

Gets all list item elements bound to this component.

**Signature:**
```ts
getItems(): Element[]
```

**Returns:** `Element[]`

```tsx
const items = ddlRef.current.getItems();
console.log(items.length);
```

---

### `hidePopup`

Hides the popup if it is currently in an open state.

**Signature:**
```ts
hidePopup(): void
```

**Returns:** `void`

```tsx
ddlRef.current.hidePopup();
```

---

### `hideSpinner`

Hides the spinner loader that is displayed during data loading.

**Signature:**
```ts
hideSpinner(): void
```

**Returns:** `void`

---

### `showPopup`

Opens the popup that displays the list of items.

**Signature:**
```ts
showPopup(): void
```

**Returns:** `void`

```tsx
ddlRef.current.showPopup();
```

---

### `showSpinner`

Shows the spinner loader (useful for custom loading states).

**Signature:**
```ts
showSpinner(): void
```

**Returns:** `void`

---

## Events

### `actionBegin`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers before fetching data from the remote server.

```tsx
<DropDownListComponent actionBegin={() => console.log('Fetching data...')} dataSource={remoteData} />
```

---

### `actionComplete`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers after data is fetched successfully from the remote server.

```tsx
<DropDownListComponent actionComplete={(e) => console.log('Data loaded', e)} dataSource={remoteData} />
```

---

### `actionFailure`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the data fetch request from the remote server fails.

```tsx
<DropDownListComponent actionFailure={(e) => console.error('Failed to fetch', e)} dataSource={remoteData} />
```

---

### `beforeOpen`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers before the popup opens.

```tsx
<DropDownListComponent beforeOpen={() => console.log('Popup about to open')} dataSource={data} />
```

---

### `blur`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when focus moves out from the component.

```tsx
<DropDownListComponent blur={() => console.log('Blurred')} dataSource={data} />
```

---

### `change`
| Detail | Value |
|---|---|
| **Type** | `EmitType<ChangeEventArgs>` |

Triggers when an item in the popup is selected or when the model value is changed by the user. Useful for cascading dropdowns and value tracking.

```tsx
import { ChangeEventArgs } from '@syncfusion/ej2-react-dropdowns';

function onChange(args: ChangeEventArgs) {
  console.log('Selected value:', args.value);
  console.log('Selected item data:', args.itemData);
}

<DropDownListComponent dataSource={data} change={onChange} />
```

---

### `close`
| Detail | Value |
|---|---|
| **Type** | `EmitType<PopupEventArgs>` |

Triggers when the popup is closed.

```tsx
<DropDownListComponent close={(e) => console.log('Popup closed', e)} dataSource={data} />
```

---

### `created`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the component is created.

```tsx
<DropDownListComponent created={() => console.log('DropDownList created')} dataSource={data} />
```

---

### `dataBound`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the data source is populated in the popup list.

```tsx
<DropDownListComponent dataBound={() => console.log('Data bound to popup')} dataSource={data} />
```

---

### `destroyed`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the component is destroyed.

---

### `filtering`
| Detail | Value |
|---|---|
| **Type** | `EmitType<FilteringEventArgs>` |

Triggers on typing a character in the filter bar when `allowFiltering` is enabled. Use `args.updateData()` to apply custom filtering logic.

```tsx
import { FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';

function onFiltering(args: FilteringEventArgs) {
  let query = new Query();
  query = args.text !== '' ? query.where('Country', 'startswith', args.text, true) : query;
  args.updateData(searchData, query);
}

<DropDownListComponent
  dataSource={searchData}
  allowFiltering={true}
  filtering={onFiltering}
/>
```

---

### `focus`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the component is focused.

```tsx
<DropDownListComponent focus={() => console.log('Focused')} dataSource={data} />
```

---

### `open`
| Detail | Value |
|---|---|
| **Type** | `EmitType<PopupEventArgs>` |

Triggers when the popup opens.

```tsx
<DropDownListComponent open={(e) => console.log('Popup opened', e)} dataSource={data} />
```

---

### `resizeStart`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the user starts resizing the DropDownList popup. Requires `allowResize={true}`.

```tsx
<DropDownListComponent allowResize={true} resizeStart={() => console.log('Resize started')} dataSource={data} />
```

---

### `resizeStop`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers when the user finishes resizing the DropDownList popup.

```tsx
<DropDownListComponent allowResize={true} resizeStop={() => console.log('Resize stopped')} dataSource={data} />
```

---

### `resizing`
| Detail | Value |
|---|---|
| **Type** | `EmitType<Object>` |

Triggers continuously while the DropDownList popup is being resized by the user. Provides live updates on the width and height of the popup.

```tsx
<DropDownListComponent allowResize={true} resizing={(e) => console.log('Resizing', e)} dataSource={data} />
```

---

### `select`
| Detail | Value |
|---|---|
| **Type** | `EmitType<SelectEventArgs>` |

Triggers when an item in the popup is selected by the user via mouse/tap or keyboard navigation.

```tsx
import { SelectEventArgs } from '@syncfusion/ej2-react-dropdowns';

function onSelect(args: SelectEventArgs) {
  console.log('Item selected:', args.itemData);
}

<DropDownListComponent dataSource={data} select={onSelect} />
```

---

## Interface: FieldSettingsModel

Maps the columns of the data source to the DropDownList component.

> **API Ref:** https://ej2.syncfusion.com/react/documentation/api/drop-down-list/fieldSettingsModel

| Property | Type | Description |
|---|---|---|
| `text` | `string` | Maps the text column from the data table for each list item (display label). |
| `value` | `string` | Maps the value column from the data table for each list item. |
| `iconCss` | `string` | Maps the icon CSS class column from the data table for each list item. |
| `groupBy` | `string` | Groups list items with related items by mapping the groupBy field. |
| `disabled` | `string` | Maps the field that determines whether a particular item is disabled. |
| `htmlAttributes` | `string` | Maps additional HTML attributes (e.g., `title`, `disabled`) for configuring list elements. |

```tsx
const fields: FieldSettingsModel = {
  text: 'CountryName',
  value: 'CountryCode',
  iconCss: 'FlagIcon',
  groupBy: 'Continent',
  disabled: 'IsDisabled'
};

<DropDownListComponent dataSource={countryData} fields={fields} />
```

---

## Interface: ChangeEventArgs

Emitted by the `change` event.

> **API Ref:** https://ej2.syncfusion.com/react/documentation/api/drop-down-list/changeEventArgs

| Property | Type | Description |
|---|---|---|
| `value` | `number \| string \| boolean \| object` | Returns the selected value. |
| `item` | `HTMLLIElement` | Returns the selected list item DOM element. |
| `itemData` | `FieldSettingsModel` | Returns the selected item as a JSON object from the data source. |
| `previousItem` | `HTMLLIElement` | Returns the previously selected list item DOM element. |
| `previousItemData` | `FieldSettingsModel` | Returns the previously selected item as a JSON object from the data source. |
| `element` | `HTMLElement` | Returns the root element of the component. |
| `event` | `MouseEvent \| KeyboardEvent \| TouchEvent` | Specifies the original event arguments. |
| `e` | `MouseEvent \| KeyboardEvent \| TouchEvent` | Specifies the original event arguments (alias). |
| `isInteracted` | `boolean` | Returns `true` if the event was triggered by a user interaction, `false` if programmatic. |
| `cancel` | `boolean` | Set to `true` to prevent the default change action. |

```tsx
function onChange(args: ChangeEventArgs) {
  console.log('New value:', args.value);
  console.log('New item data:', args.itemData);
  console.log('Previous item data:', args.previousItemData);
  console.log('User interaction:', args.isInteracted);
}
```

---

## Interface: SelectEventArgs

Emitted by the `select` event.

> **API Ref:** https://ej2.syncfusion.com/react/documentation/api/drop-down-list/selectEventArgs

| Property | Type | Description |
|---|---|---|
| `item` | `HTMLLIElement` | Returns the selected list item DOM element. |
| `itemData` | `FieldSettingsModel` | Returns the selected item as a JSON object from the data source. |
| `e` | `MouseEvent \| KeyboardEvent \| TouchEvent` | Specifies the original event arguments. |
| `isInteracted` | `boolean` | Returns `true` if triggered by user interaction, `false` if programmatic. |
| `cancel` | `boolean` | Set to `true` to cancel the selection action. |

```tsx
function onSelect(args: SelectEventArgs) {
  if (someCondition) {
    args.cancel = true; // Prevent selection
  }
  console.log('Selected item:', args.itemData);
}
```

---

## Interface: PopupEventArgs

Emitted by the `open`, `close`, and `beforeOpen` events.

> **API Ref:** https://ej2.syncfusion.com/react/documentation/api/drop-down-list/popupEventArgs

| Property | Type | Description |
|---|---|---|
| `popup` | `Popup` | Specifies the popup component object. |
| `animation` | `AnimationModel` | Specifies the animation object used for the popup open/close transition. |
| `event` | `MouseEvent \| KeyboardEventArgs \| TouchEvent \| Object` | Specifies the event that triggered the popup action. |
| `cancel` | `boolean` | Set to `true` to cancel the popup open or close action. |

```tsx
function onBeforeOpen(args: PopupEventArgs) {
  args.cancel = true; // Prevent popup from opening
}

function onOpen(args: PopupEventArgs) {
  // Customize animation
  args.animation = { open: { effect: 'FadeIn', duration: 300 } };
}
```

---

## Interface: FilteringEventArgs

Emitted by the `filtering` event.

> **API Ref:** https://ej2.syncfusion.com/react/documentation/api/drop-down-list/filteringEventArgs

| Property | Type | Description |
|---|---|---|
| `text` | `string` | The search text typed in the filter bar. |
| `cancel` | `boolean` | Set to `true` to prevent the default filtering action. |
| `preventDefaultAction` | `boolean` | Set to `true` to prevent the internal filtering action and handle it manually. |
| `baseEventArgs` | `Object` | Gets the underlying `keyup` event arguments. |

### Methods on `FilteringEventArgs`

#### `updateData`
Applies filtered data to the popup list.

```ts
updateData(
  dataSource: { [key: string]: Object }[] | DataManager | string[] | number[] | boolean[],
  query?: Query,
  fields?: FieldSettingsModel
): void
```

| Parameter | Type | Description |
|---|---|---|
| `dataSource` | `Object[] \| DataManager \| string[] \| ...` | The data source to display after filtering. |
| `query` *(optional)* | `Query` | A query to apply on the data source. |
| `fields` *(optional)* | `FieldSettingsModel` | Field mappings for the data table. |

```tsx
function onFiltering(args: FilteringEventArgs) {
  // Prevent default and handle manually
  args.preventDefaultAction = true;
  const query = new Query().where('Name', 'contains', args.text, true);
  args.updateData(myData, query);
}
```

---

## Quick Reference Summary

### Properties at a Glance

| Property | Type | Default | Purpose |
|---|---|---|---|
| `dataSource` | `any[] \| DataManager` | `[]` | Data for the list |
| `fields` | `FieldSettingsModel` | `{}` | Column mapping |
| `value` | `string \| number \| boolean \| object \| null` | `null` | Selected value |
| `text` | `string \| null` | `null` | Selected display text |
| `index` | `number \| null` | `null` | Selected item index |
| `placeholder` | `string` | `null` | Input placeholder |
| `allowFiltering` | `boolean` | `false` | Enable search filter bar |
| `filterType` | `FilterType` | `'StartsWith'` | Filter matching type |
| `filterBarPlaceholder` | `string` | `null` | Filter bar watermark |
| `debounceDelay` | `number` | `300` | Filter debounce (ms) |
| `ignoreCase` | `boolean` | `true` | Case-insensitive filter |
| `ignoreAccent` | `boolean` | `false` | Accent-insensitive filter |
| `sortOrder` | `SortOrder` | `null` | `'None'` / `'Ascending'` / `'Descending'` |
| `enabled` | `boolean` | `true` | Enable/disable component |
| `readonly` | `boolean` | `false` | Read-only mode |
| `showClearButton` | `boolean` | `false` | Show clear button |
| `enableVirtualization` | `boolean` | `false` | Virtual scrolling |
| `allowResize` | `boolean` | `false` | Resizable popup |
| `popupHeight` | `string \| number` | `'300px'` | Popup list height |
| `popupWidth` | `string \| number` | `'100%'` | Popup list width |
| `cssClass` | `string` | `null` | Custom CSS class |
| `htmlAttributes` | `object` | `{}` | Extra HTML attributes |
| `width` | `string \| number` | `'100%'` | Component width |
| `zIndex` | `number` | `1000` | Popup z-index |
| `floatLabelType` | `FloatLabelType` | `'Never'` | Floating label behavior |
| `itemTemplate` | `string \| Function` | `null` | Item render template |
| `valueTemplate` | `string \| Function` | `null` | Selected value template |
| `headerTemplate` | `string \| Function` | `null` | Popup header template |
| `footerTemplate` | `string \| Function` | `null` | Popup footer template |
| `groupTemplate` | `string \| Function` | `null` | Group header template |
| `noRecordsTemplate` | `string \| Function` | `'No records found'` | Empty state template |
| `actionFailureTemplate` | `string \| Function` | `'Request failed'` | Remote failure template |
| `query` | `Query` | `null` | External data query |
| `allowObjectBinding` | `boolean` | `false` | Allow object value binding |
| `enablePersistence` | `boolean` | `false` | Persist state on reload |
| `enableRtl` | `boolean` | `false` | Right-to-left layout |
| `locale` | `string` | `'en-US'` | Locale/culture override |
| `isDeviceFullScreen` | `boolean` | `true` | Full-screen popup on mobile |

### Methods at a Glance

| Method | Returns | Purpose |
|---|---|---|
| `addItem(items, itemIndex?)` | `void` | Add item(s) to the popup list |
| `clear()` | `void` | Clear the selected value |
| `destroy()` | `void` | Remove component from DOM |
| `disableItem(item)` | `void` | Disable a specific list item |
| `filter(dataSource, query?, fields?)` | `void` | Programmatically filter the data |
| `focusIn()` | `void` | Set focus on the component |
| `focusOut()` | `void` | Remove focus from the component |
| `getDataByValue(value)` | `Object \| string \| ...` | Get data object by value |
| `getItems()` | `Element[]` | Get all list item elements |
| `hidePopup()` | `void` | Close the popup |
| `hideSpinner()` | `void` | Hide the loading spinner |
| `showPopup()` | `void` | Open the popup |
| `showSpinner()` | `void` | Show the loading spinner |

### Events at a Glance

| Event | Args Type | Trigger |
|---|---|---|
| `actionBegin` | `Object` | Before remote data fetch starts |
| `actionComplete` | `Object` | After remote data fetch succeeds |
| `actionFailure` | `Object` | When remote data fetch fails |
| `beforeOpen` | `Object` | Before the popup opens |
| `open` | `PopupEventArgs` | When the popup opens |
| `close` | `PopupEventArgs` | When the popup closes |
| `change` | `ChangeEventArgs` | When the selected value changes |
| `select` | `SelectEventArgs` | When an item is selected in the popup |
| `filtering` | `FilteringEventArgs` | On typing in the filter bar |
| `focus` | `Object` | When the component gains focus |
| `blur` | `Object` | When the component loses focus |
| `created` | `Object` | When the component is created |
| `destroyed` | `Object` | When the component is destroyed |
| `dataBound` | `Object` | When data source is bound to popup |
| `resizeStart` | `Object` | When popup resize starts |
| `resizing` | `Object` | While popup is being resized |
| `resizeStop` | `Object` | When popup resize ends |
