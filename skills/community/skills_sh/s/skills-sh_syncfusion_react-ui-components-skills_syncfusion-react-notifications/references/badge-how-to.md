# How-To Guides

## Table of Contents
- [Integrate Badge into ListView](#integrate-badge-into-listview)
- [Dynamic Badge Content](#dynamic-badge-content)

---

## Integrate Badge into ListView

Badges can be embedded directly in `ListViewComponent` item templates to display notification counts or status alongside list entries. The badge automatically scales to match the list item height — no manual size configuration is needed.

**When to use:** Email inboxes, notification panels, sidebar navigation with unread counts.

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";
import { ListViewComponent } from '@syncfusion/ej2-react-lists';

function App() {
    // Each item carries a `badge` field holding the CSS classes, and a `messages` field for display text
    let dataSource: { [key: string]: Object }[] = [
        { id: 'p_01', text: 'Primary',    messages: '3 New',  badge: 'e-badge e-badge-primary',   icons: 'primary',   type: 'Primary' },
        { id: 'p_02', text: 'Social',     messages: '27 New', badge: 'e-badge e-badge-secondary',  icons: 'social',    type: 'Primary' },
        { id: 'p_03', text: 'Promotions', messages: '7 New',  badge: 'e-badge e-badge-success',    icons: 'promotion', type: 'Primary' },
        { id: 'p_04', text: 'Updates',    messages: '13 New', badge: 'e-badge e-badge-info',        icons: 'updates',   type: 'Primary' },
        { id: 'p_05', text: 'Starred',    messages: '',       badge: '',                            icons: 'starred',   type: 'All Labels' },
        { id: 'p_06', text: 'Important',  messages: '2 New',  badge: 'e-badge e-badge-danger',      icons: 'important', type: 'All Labels' },
        { id: 'p_07', text: 'Sent',       messages: '',       badge: '',                            icons: 'sent',      type: 'All Labels' },
        { id: 'p_08', text: 'Outbox',     messages: '',       badge: '',                            icons: 'outbox',    type: 'All Labels' },
        { id: 'p_09', text: 'Drafts',     messages: '7 New',  badge: 'e-badge e-badge-warning',     icons: 'draft',     type: 'All Labels' },
    ];

    let fields: object = { groupBy: 'type' };

    function template(data: any): JSX.Element {
        return (
            <div className='listWrapper' style={{ width: 'inherit', height: 'inherit' }}>
                <span className={`${data.icons} list_svg`}>&nbsp;</span>
                <span className='list_text'>{data.text}</span>
                <span className={`${data.badge}`} style={{ float: 'right', marginTop: '16px', fontSize: '12px' }}>
                    {data.messages}
                </span>
            </div>
        );
    }

    function onActionComplete() {
        let list: HTMLElement = document.getElementById('lists').getElementsByClassName('e-list-group-item')[0] as HTMLElement;
        list.style.display = 'none';
    }

    return (
        <div className="sample_container badge-list">
            <ListViewComponent
                id="lists"
                dataSource={dataSource}
                fields={fields}
                headerTitle='Inbox'
                showHeader={true}
                template={template as any}
                actionComplete={onActionComplete.bind(this)}
            />
        </div>
    );
}
export default App;
ReactDOM.render(<App />, document.getElementById("element"));
```

**Key points:**
- Store badge CSS classes in the data source (`badge` field) so each item controls its own badge color independently.
- Items without a badge have an empty string for the `badge` field — the template renders nothing in that case.
- `onActionComplete` hides the first group header if not needed.
- Install `@syncfusion/ej2-react-lists` for `ListViewComponent`: `npm install @syncfusion/ej2-react-lists --save`

---

## Dynamic Badge Content

Many applications need badge counts that update in response to user actions or incoming data. Because Badge is CSS-only, update the badge text content directly via DOM queries rather than through a React state-driven re-render.

**When to use:** Inbox counters that increment on new messages, notification panels with live updates.

```tsx
import * as React from "react";
import * as ReactDOM from "react-dom";
import { ListViewComponent } from '@syncfusion/ej2-react-lists';

interface IBadgeValuesProps {
    BadgeType: string;
    BadgeContent: string;
}

function BadgePortable(props: IBadgeValuesProps) {
    return (
        <span
            className={props.BadgeType}
            style={{ float: 'right', marginTop: '16px', fontSize: '12px' }}
        >
            {props.BadgeContent} New
        </span>
    );
}

function App() {
    let dataSource: { [key: string]: Object }[] = [
        { id: 'p_01', text: 'Primary',    badge: 'e-badge e-badge-primary',   icons: 'primary',   type: 'Primary' },
        { id: 'p_02', text: 'Social',     badge: 'e-badge e-badge-secondary',  icons: 'social',    type: 'Primary' },
        { id: 'p_03', text: 'Promotions', badge: 'e-badge e-badge-success',    icons: 'promotion', type: 'Primary' },
        { id: 'p_04', text: 'Updates',    badge: 'e-badge e-badge-info',        icons: 'updates',   type: 'Primary' },
        { id: 'p_05', text: 'Starred',    badge: '',                            icons: 'starred',   type: 'All Labels' },
        { id: 'p_06', text: 'Important',  badge: 'e-badge e-badge-danger',      icons: 'important', type: 'All Labels' },
        { id: 'p_07', text: 'Sent',       badge: '',                            icons: 'sent',      type: 'All Labels' },
        { id: 'p_08', text: 'Outbox',     badge: '',                            icons: 'outbox',    type: 'All Labels' },
        { id: 'p_09', text: 'Drafts',     badge: 'e-badge e-badge-warning',     icons: 'draft',     type: 'All Labels' },
    ];

    let fields: object = { groupBy: 'type' };

    // Initial badge values mapped by list item text
    let Values: { [key: string]: number } = {
        Primary: 3,
        Social: 27,
        Promotions: 7,
        Updates: 13,
        Drafts: 7,
        Important: 2
    };

    function listTemplate(data: any): JSX.Element {
        return (
            <div className='listWrapper' style={{ width: 'inherit', height: 'inherit' }}>
                <span className={`${data.icons} list_svg`}>&nbsp;</span>
                <span className='list_text'>{data.text}</span>
                {data.badge !== '' ?
                    <BadgePortable BadgeContent={Values[data.text]} BadgeType={data.badge} /> : ''
                }
            </div>
        );
    }

    // Increment all badge counts by querying the DOM directly
    function onClick(): void {
        let badgeElements = Array.prototype.slice.call(
            document.getElementById('lists').getElementsByClassName('e-badge')
        );
        badgeElements.forEach((element) => {
            element.textContent = (Number(element.textContent.split(' ')[0])) + 1 + ' New';
        });
    }

    return (
        <div className="sample_container badge-list">
            <ListViewComponent
                id="lists"
                dataSource={dataSource}
                fields={fields}
                headerTitle='Inbox'
                showHeader={true}
                template={listTemplate.bind(this) as any}
            />
            <p className='crossline'></p>
            <span className='incr_button'>
                <button className='e-btn e-primary' onClick={onClick.bind(this)}>Increment Badge Count</button>
            </span>
        </div>
    );
}
export default App;
ReactDOM.render(<App />, document.getElementById("element"));
```

**Key points:**
- Badge text follows the pattern `"{count} New"` — the increment splits on the space and parses the number.
- `getElementsByClassName('e-badge')` selects all badge elements within the list container by ID (`lists`).
- The `BadgePortable` sub-component keeps badge rendering isolated and reusable across list items.
- For real-time updates (WebSockets, polling), call the same DOM-update logic inside your data handler instead of the button `onClick`.
