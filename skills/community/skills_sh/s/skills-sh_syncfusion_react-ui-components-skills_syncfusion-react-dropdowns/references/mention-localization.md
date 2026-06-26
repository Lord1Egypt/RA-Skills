# Localization in Syncfusion React Mention

## Overview

The Syncfusion React Mention component supports localization for its static text via the `L10n` class from `@syncfusion/ej2-base`. Currently, the localizable text is:

| Locale Key | Default (en-US) |
|------------|-----------------|
| `noRecordsTemplate` | `No records found` |

Set the `locale` prop on the component to apply a loaded locale.

## Loading a Custom Locale

Use `L10n.load()` to register translations before rendering the component. The translation object uses the namespace `'dropdowns'`:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { L10n } from '@syncfusion/ej2-base';
import { DataManager, ODataV4Adaptor, Query } from '@syncfusion/ej2-data';
import * as React from 'react';

// Load French (Belgium) translations
L10n.load({
  'fr-BE': {
    dropdowns: {
      noRecordsTemplate: 'Aucun enregistrement trouvé',
    },
  },
});

function App() {
  const mentionTarget: string = '#mentionElement';
  const customerData: DataManager = new DataManager({
    url: 'url',
    adaptor: new ODataV4Adaptor,
    crossDomain: true,
  });
  const fields: Object = { text: 'ContactName', value: 'CustomerID' };
  // take(0) so there are no results → triggers noRecordsTemplate
  const query: Query = new Query().select(['ContactName', 'CustomerID']).take(0);

  return (
    <div id="mention_default">
      <table>
        <tr>
          <td>
            <label id="comment">Comments</label>
            <div id="mentionElement" placeholder="Type @ and tag user"></div>
          </td>
        </tr>
      </table>
      <MentionComponent
        target={mentionTarget}
        dataSource={customerData}
        locale="fr-BE"
        fields={fields}
        query={query}
      />
    </div>
  );
}

export default App;
```

## Loading L10n in Class Components

For class components, call `L10n.load()` in `componentWillMount` or before `render`:

```tsx
import { MentionComponent } from '@syncfusion/ej2-react-dropdowns';
import { L10n } from '@syncfusion/ej2-base';
import * as React from 'react';

export default class App extends React.Component<{}, {}> {
  private mentionTarget: string = '#mentionElement';
  private userData: string[] = ['Selma Rose', 'Garth', 'Robert'];

  public componentWillMount() {
    L10n.load({
      'de': {
        dropdowns: {
          noRecordsTemplate: 'Keine Einträge gefunden',
        },
      },
    });
  }

  public render() {
    return (
      <div id="mention_default">
        <table>
          <tr>
            <td>
              <label id="comment">Comments</label>
              <div id="mentionElement" placeholder="Type @ and tag user"></div>
            </td>
          </tr>
        </table>
        <MentionComponent
          target={this.mentionTarget}
          dataSource={[]}
          locale="de"
        />
      </div>
    );
  }
}
```

## Gotchas

- `L10n.load()` must be called **before** the component renders; calling it after mount has no effect on the already-rendered text.
- The locale key is case-sensitive—`'fr-BE'` is different from `'fr-be'`.
- Only `noRecordsTemplate` is localizable via `L10n` in the Mention component. Other text like popup items comes from your data source.
- When using `noRecordsTemplate` as a prop directly (HTML string), it overrides the `L10n` translation for that instance.
