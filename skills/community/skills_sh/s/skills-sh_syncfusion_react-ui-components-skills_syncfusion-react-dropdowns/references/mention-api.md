# Syncfusion React Mention API Reference

Source: https://ej2.syncfusion.com/react/documentation/api/mention/index-default

## Table of Contents
- [Properties](#properties)
- [Methods](#methods)
- [Events](#events)
- [Type Aliases](#type-aliases)

---

## Properties

### actionFailureTemplate
**Type:** `string | Function`  
**Default:** `'Request failed'`

Template displayed in the popup when a remote data fetch fails.

```tsx
<MentionComponent
  target="#editor"
  dataSource={remoteData}
  actionFailureTemplate="<span>Could not load users. Try again.</span>"
/>
```

---

### allowSpaces
**Type:** `boolean`  
**Default:** `false`

When `true`, spaces within the mention search do not close the popup. Useful for searching full names like "Andrew Fuller".

```tsx
<MentionComponent target="#editor" dataSource={data} fields={fields} allowSpaces={true} />
```

---

### cssClass
**Type:** `string`  
**Default:** `null`

One or more CSS classes (space-separated) applied to the popup element for custom styling.

```tsx
<MentionComponent target="#editor" dataSource={data} cssClass="custom-mention" />
```

---

### dataSource
**Type:** `{ [key: string]: Object }[] | DataManager | string[] | number[] | boolean[]`  
**Default:** `[]`

The data bound to the suggestion list. Accepts local arrays (strings, numbers, objects) or a `DataManager` for remote data.

```tsx
// Local array
<MentionComponent target="#editor" dataSource={['Alice', 'Bob', 'Carol']} />

// DataManager
<MentionComponent target="#editor" dataSource={new DataManager({ url: '...', adaptor: new ODataV4Adaptor })} />
```

---

### debounceDelay
**Type:** `number`  
**Default:** `300`

Delay in milliseconds before a filter operation fires after the user types. Increase for remote data to reduce API calls.

```tsx
<MentionComponent target="#editor" dataSource={remoteData} debounceDelay={500} />
```

---

### displayTemplate
**Type:** `string | Function`  
**Default:** `null`

Template for the text inserted into the editor when an item is selected. Separate from `itemTemplate` (popup appearance).

```tsx
function displayTemplate(data: any): JSX.Element {
  return <span>{data.FirstName} ({data.City})</span>;
}
<MentionComponent target="#editor" dataSource={data} fields={fields} displayTemplate={displayTemplate} />
```

---

### enablePersistence
**Type:** `boolean`  
**Default:** `false`

Persists component state between page reloads when `true`.

---

### enableRtl
**Type:** `boolean`  
**Default:** `false`

Renders the popup in right-to-left direction for RTL locales.

```tsx
<MentionComponent target="#editor" dataSource={data} enableRtl={true} />
```

---

### fields
**Type:** `FieldSettingsModel`  
**Default:** `{ text: null, value: null, iconCss: null, groupBy: null }`

Maps data source object properties to the component's internal fields:
- `text` — Display text in the popup list
- `value` — Hidden unique identifier
- `iconCss` — CSS class for an icon per item
- `groupBy` — Field to group items by category
- `disabled` — Boolean field to disable specific items

```tsx
const fields = { text: 'Name', value: 'ID', groupBy: 'Department', disabled: 'IsDisabled' };
<MentionComponent target="#editor" dataSource={data} fields={fields} />
```

---

### filterType
**Type:** `FilterType` (`'StartsWith' | 'EndsWith' | 'Contains'`)  
**Default:** `'Contains'`

Determines how typed text is matched against data items.

```tsx
<MentionComponent target="#editor" dataSource={data} filterType="StartsWith" />
```

---

### groupTemplate
**Type:** `string | Function`  
**Default:** `null`

Custom template for group header elements in the popup list.

```tsx
function groupTemplate(data: any): JSX.Element {
  return <strong>{data.Department}</strong>;
}
<MentionComponent target="#editor" dataSource={data} fields={fields} groupTemplate={groupTemplate} />
```

---

### highlight
**Type:** `boolean`  
**Default:** `false`

Highlights the searched characters within suggestion list items.

```tsx
<MentionComponent target="#editor" dataSource={data} fields={fields} highlight={true} />
```

---

### ignoreAccent
**Type:** `boolean`  
**Default:** `false` (not set means no accent ignoring)

When `true`, diacritic characters (accents) are ignored during filtering so `é` matches `e`.

---

### ignoreCase
**Type:** `boolean`  
**Default:** `true`

When `true`, filtering is case-insensitive. Set to `false` for case-sensitive search.

---

### itemTemplate
**Type:** `string`  
**Default:** `null`

Custom template for each suggestion list item in the popup.

```tsx
function itemTemplate(data: any): JSX.Element {
  return <span>{data.Name} — {data.Email}</span>;
}
<MentionComponent target="#editor" dataSource={data} fields={fields} itemTemplate={itemTemplate} />
```

---

### locale
**Type:** `string`  
**Default:** `'en-US'`

Overrides the global locale for this component instance. Use with `L10n.load()` for translations.

```tsx
<MentionComponent target="#editor" dataSource={data} locale="fr-BE" />
```

---

### mentionChar
**Type:** `string`  
**Default:** `'@'`

The single character that triggers the suggestion popup. Must be exactly one character.

```tsx
<MentionComponent target="#editor" dataSource={data} mentionChar="#" />
```

---

### minLength
**Type:** `number`  
**Default:** `0`

Minimum number of characters typed after the trigger character before the popup opens.

```tsx
<MentionComponent target="#editor" dataSource={data} minLength={2} />
```

---

### noRecordsTemplate
**Type:** `string`  
**Default:** `'No records found'`

Content shown in the popup when no suggestions match the current search. Accepts HTML string or JSX function.

```tsx
<MentionComponent
  target="#editor"
  dataSource={data}
  noRecordsTemplate="<span>No matching users found</span>"
/>
```

---

### popupHeight
**Type:** `string | number`  
**Default:** `'300px'`

Height of the suggestion popup. Numbers are treated as pixels.

```tsx
<MentionComponent target="#editor" dataSource={data} popupHeight="200px" />
```

---

### popupWidth
**Type:** `string | number`  
**Default:** `'auto'`

Width of the suggestion popup. Numbers are treated as pixels.

```tsx
<MentionComponent target="#editor" dataSource={data} popupWidth="300px" />
```

---

### query
**Type:** `Query`  
**Default:** `null`

An external `Query` object for customizing/filtering remote data requests.

```tsx
import { Query } from '@syncfusion/ej2-data';
const query = new Query().from('Customers').select(['ContactName', 'CustomerID']).take(10);
<MentionComponent target="#editor" dataSource={remoteData} fields={fields} query={query} />
```

---

### requireLeadingSpace
**Type:** `boolean`  
**Default:** `true`

When `true`, a space is required before the trigger character to open the popup. Set to `false` to allow the mention at the beginning of a line.

```tsx
<MentionComponent target="#editor" dataSource={data} requireLeadingSpace={false} />
```

---

### showMentionChar
**Type:** `boolean`  
**Default:** `false`

When `true`, the trigger character (`mentionChar`) is included in the text inserted into the editor.

```tsx
<MentionComponent target="#editor" dataSource={data} showMentionChar={true} />
```

---

### sortOrder
**Type:** `SortOrder` (`'None' | 'Ascending' | 'Descending'`)  
**Default:** `'None'`

Sort order for the suggestion list items.

```tsx
<MentionComponent target="#editor" dataSource={data} fields={fields} sortOrder="Ascending" />
```

---

### spinnerTemplate
**Type:** `string | Function`  
**Default:** `null`

Custom loading indicator displayed while remote data is being fetched.

```tsx
function spinnerTemplate(): JSX.Element {
  return <div className="my-spinner"></div>;
}
<MentionComponent target="#editor" dataSource={remoteData} spinnerTemplate={spinnerTemplate} />
```

---

### suffixText
**Type:** `string`  
**Default:** `null`

Text appended after the selected mention text in the editor. Use `'&nbsp;'` for a space or `'\n'` for a newline.

```tsx
<MentionComponent target="#editor" dataSource={data} suffixText="&nbsp;" />
```

---

### suggestionCount
**Type:** `number`  
**Default:** `25`

Maximum number of items shown in the suggestion popup.

```tsx
<MentionComponent target="#editor" dataSource={data} suggestionCount={10} />
```

---

### target
**Type:** `HTMLElement | string`  
**Required** (no default)

The target editable element where the Mention component listens for input. Accepts a CSS selector string or an `HTMLElement` reference.

```tsx
<MentionComponent target="#commentBox" dataSource={data} />
// or
<MentionComponent target={document.getElementById('commentBox')} dataSource={data} />
```

---

### zIndex
**Type:** `number`  
**Default:** `1000`

Z-index of the popup element. Increase when rendering inside a modal or overlay.

```tsx
<MentionComponent target="#editor" dataSource={data} zIndex={9999} />
```

---

## Methods

Access these methods via a component ref:

```tsx
const mentionRef = React.useRef<MentionComponent>(null);
// Then: mentionRef.current?.methodName(...)
```

### addItem
Adds a new item to the popup list. By default appended at the end; use `itemIndex` to insert at a specific position.

```tsx
mentionRef.current?.addItem({ Name: 'New User', ID: '99' });
mentionRef.current?.addItem({ Name: 'Inserted', ID: '50' }, 2); // insert at index 2
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `items` | `object \| object[] \| string \| boolean \| number \| string[] \| boolean[] \| number[]` | Item(s) to add |
| `itemIndex` (optional) | `number` | Index at which to insert |

**Returns:** `void`

---

### destroy
Removes the component from the DOM and detaches all related event handlers and attributes.

```tsx
mentionRef.current?.destroy();
```

**Returns:** `void`

---

### disableItem
Disables a specific item in the popup, preventing selection.

```tsx
mentionRef.current?.disableItem('ID_VALUE');      // by value
mentionRef.current?.disableItem(2);               // by index
mentionRef.current?.disableItem({ Name: 'Bob' }); // by object
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `item` | `string \| number \| object \| HTMLLIElement` | Item to disable |

**Returns:** `void`

---

### getDataByValue
Returns the data object matching a given value.

```tsx
const item = mentionRef.current?.getDataByValue('game1');
// Returns: { ID: 'game1', Game: 'Badminton' }
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `string \| number \| boolean \| object` | Value to look up |

**Returns:** `{ [key: string]: Object } | string | number | boolean`

---

### getItems
Returns all rendered list item elements in the popup.

```tsx
const items: Element[] = mentionRef.current?.getItems() ?? [];
```

**Returns:** `Element[]`

---

### hidePopup
Closes the suggestion popup if it is open.

```tsx
mentionRef.current?.hidePopup();
```

**Returns:** `void`

---

### search
Triggers a search and shows matching items in the popup.

```tsx
mentionRef.current?.search();
```

**Returns:** `void`

---

### showPopup
Opens the suggestion popup programmatically.

```tsx
mentionRef.current?.showPopup();
```

**Returns:** `void`

---

## Events

Wire events as props on `MentionComponent`:

### actionBegin
Fires before the remote data fetch request is sent.

```tsx
<MentionComponent target="#editor" dataSource={remoteData} actionBegin={(args) => console.log('Fetching...', args)} />
```

---

### actionComplete
Fires after remote data is successfully fetched.

```tsx
<MentionComponent target="#editor" dataSource={remoteData} actionComplete={(args) => console.log('Data loaded', args)} />
```

---

### actionFailure
Fires when the remote data fetch fails.

```tsx
<MentionComponent target="#editor" dataSource={remoteData} actionFailure={(args) => console.error('Fetch failed', args)} />
```

---

### beforeOpen
Fires before the popup opens. Access popup-related data via `args`.

```tsx
import { PopupEventArgs } from '@syncfusion/ej2-react-dropdowns';
<MentionComponent
  target="#editor"
  dataSource={data}
  beforeOpen={(args: PopupEventArgs) => console.log('Before open', args)}
/>
```

---

### change
Fires when an item is selected and its value is inserted into the editor.

```tsx
import { MentionChangeEventArgs } from '@syncfusion/ej2-react-dropdowns';
<MentionComponent
  target="#editor"
  dataSource={data}
  change={(args: MentionChangeEventArgs) => {
    console.log('Changed to:', args.itemData, 'Text:', args.text);
  }}
/>
```

---

### closed
Fires after the popup closes.

```tsx
import { PopupEventArgs } from '@syncfusion/ej2-react-dropdowns';
<MentionComponent
  target="#editor"
  dataSource={data}
  closed={(args: PopupEventArgs) => console.log('Popup closed')}
/>
```

---

### created
Fires when the component is fully initialized.

```tsx
<MentionComponent target="#editor" dataSource={data} created={() => console.log('Mention ready')} />
```

---

### dataBound
Fires when the data source is populated in the popup list.

```tsx
<MentionComponent target="#editor" dataSource={data} dataBound={() => console.log('Data bound')} />
```

---

### destroyed
Fires when the component is destroyed.

```tsx
<MentionComponent target="#editor" dataSource={data} destroyed={() => console.log('Destroyed')} />
```

---

### filtering
Fires on each keystroke during search. Use to apply custom filter logic via `args.updateData()`.

```tsx
import { FilteringEventArgs } from '@syncfusion/ej2-react-dropdowns';
import { Query } from '@syncfusion/ej2-data';

function onFiltering(args: FilteringEventArgs): void {
  let query = new Query();
  query = args.text ? query.where('Name', 'startswith', args.text, true) : query;
  args.updateData(localData, query);
}
<MentionComponent target="#editor" dataSource={localData} fields={fields} filtering={onFiltering} />
```

---

### opened
Fires after the popup opens.

```tsx
import { PopupEventArgs } from '@syncfusion/ej2-react-dropdowns';
<MentionComponent
  target="#editor"
  dataSource={data}
  opened={(args: PopupEventArgs) => console.log('Popup opened')}
/>
```

---

### select
Fires when a suggestion item is selected by mouse, touch, or keyboard.

```tsx
import { SelectEventArgs } from '@syncfusion/ej2-react-dropdowns';
<MentionComponent
  target="#editor"
  dataSource={data}
  fields={fields}
  select={(args: SelectEventArgs) => {
    console.log('Selected:', args.itemData);
    console.log('Text:', args.text);
  }}
/>
```

---

## Type Aliases

| Type | Values | Description |
|------|--------|-------------|
| `FilterType` | `'StartsWith' \| 'EndsWith' \| 'Contains'` | Filter match strategy |
| `SortOrder` | `'None' \| 'Ascending' \| 'Descending'` | Sort direction |
