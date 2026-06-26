# Content Rendering Strategies

## Table of Contents
- [Rendering Modes Overview](#rendering-modes-overview)
- [On-Demand Rendering (Default)](#on-demand-rendering-default)
- [Dynamic Rendering](#dynamic-rendering)
- [Initial Rendering](#initial-rendering)
- [Choosing the Right Mode](#choosing-the-right-mode)

## Rendering Modes Overview

The Tab component supports three content rendering strategies, controlled by the `loadOn` property:

| Mode | Property Value | Content Timing | State | Use Case |
|------|----------------|-----------------|-------|----------|
| **On-Demand (Lazy Loading)** | `'Demand'` or omitted | Load when tab selected | Preserved | Default, good balance |
| **Dynamic** | `'Dynamic'` | Load and unload on switch | Not preserved | Performance critical |
| **Initial** | `'Init'` | Load all on component init | Preserved | Few tabs, full access |

## On-Demand Rendering (Default)

**Mode**: Load content only when tab is first selected. Once loaded, content remains in DOM.

### How It Works

1. Tab component initializes with only the first tab's content in DOM
2. When user clicks a tab, its content is rendered and added to DOM
3. Content stays in DOM even after switching to another tab
4. Subsequent clicks on same tab show cached content

### Configuration

```jsx
<TabComponent loadOn="Demand">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
    <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
  </TabItemsDirective>
</TabComponent>
```

> **Note**: `loadOn="Demand"` is the default. You can omit this property and get the same behavior.

### Code Example: On-Demand with React Components

```jsx
import React, { useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';
import { Calendar } from '@syncfusion/ej2-react-calendars';
import { ScheduleComponent, ViewsDirective, ViewDirective, Day, Week, Month, Agenda, Inject } from '@syncfusion/ej2-react-schedule';

export default function OnDemandTab() {
  const [changeLog, setChangeLog] = useState([]);

  const logChange = (action) => {
    setChangeLog(prev => [...prev, `${new Date().toLocaleTimeString()}: ${action}`]);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>On-Demand (Lazy Loading) - Default Mode</h2>
      
      <TabComponent loadOn="Demand">
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Calendar' }}
            content={
              <div>
                <p>Calendar loaded when tab selected</p>
                <Calendar />
              </div>
            }
          />
          <TabItemDirective 
            header={{ text: 'Scheduler' }}
            content={
              <div>
                <p>Scheduler loaded when tab selected</p>
                <ScheduleComponent eventSettings={{ dataSource: [] }}>
                  <ViewsDirective>
                    <ViewDirective option="Day" />
                    <ViewDirective option="Week" />
                    <ViewDirective option="Month" />
                  </ViewsDirective>
                  <Inject services={[Day, Week, Month]} />
                </ScheduleComponent>
              </div>
            }
          />
          <TabItemDirective 
            header={{ text: 'Form' }}
            content={
              <div>
                <p>Form loaded when tab selected</p>
                <form>
                  <input type="text" placeholder="Name" />
                  <input type="email" placeholder="Email" />
                </form>
              </div>
            }
          />
        </TabItemsDirective>
      </TabComponent>

      <div style={{ marginTop: '20px', border: '1px solid #ccc', padding: '10px' }}>
        <h3>Change Log</h3>
        <ul>
          {changeLog.map((log, i) => <li key={i}>{log}</li>)}
        </ul>
      </div>
    </div>
  );
}
```

### Advantages

- **Initial Load**: Very fast—only first tab content loaded
- **State Preservation**: Form inputs, scroll position, component state retained
- **Memory**: Grows as tabs are visited, but not bloated initially
- **Best of Both Worlds**: Combines startup speed with state preservation

### Disadvantages

- **Memory Growth**: Memory increases as more tabs are accessed
- **Not Ideal For**: Many tabs with heavy components (memory could grow large)

### When to Use

- Default choice for most applications
- When you need to preserve user state within tabs
- When you have 3-10 tabs
- When content components maintain internal state you want preserved

### Performance Consideration

```jsx
// Memory usage over time (approximate)
// Initial: ~10KB (first tab only)
// After clicking Tab 2: ~20KB
// After clicking Tab 3: ~30KB
// (Memory doesn't decrease when switching back)
```

## Dynamic Rendering

**Mode**: Load and unload content for each tab selection. Only active tab content in DOM.

### How It Works

1. Tab component initializes with only first tab's content
2. When user switches tabs, previous tab content is removed from DOM
3. New tab content is rendered and added to DOM
4. Previous content is destroyed and memory freed
5. Clicking same tab again reloads (re-renders) content

### Configuration

```jsx
<TabComponent loadOn="Dynamic">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
    <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
  </TabItemsDirective>
</TabComponent>
```

### Code Example: Dynamic with State-Less Content

```jsx
import React, { useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function DynamicTab() {
  const [renderCount, setRenderCount] = useState({});

  const getTabContent = (tabName) => {
    setRenderCount(prev => ({
      ...prev,
      [tabName]: (prev[tabName] || 0) + 1
    }));

    return (
      <div>
        <p>Tab "{tabName}" rendered {renderCount[tabName] || 1} times</p>
        <p>This content will be removed when you switch to another tab.</p>
        <p>Render count increments each time you visit this tab.</p>
      </div>
    );
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Dynamic Rendering Mode</h2>
      <p>Each tab content is loaded/unloaded on switch. Switch tabs and watch the render count.</p>
      
      <TabComponent loadOn="Dynamic">
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Tab 1' }}
            content={getTabContent('Tab 1')}
          />
          <TabItemDirective 
            header={{ text: 'Tab 2' }}
            content={getTabContent('Tab 2')}
          />
          <TabItemDirective 
            header={{ text: 'Tab 3' }}
            content={getTabContent('Tab 3')}
          />
        </TabItemsDirective>
      </TabComponent>
    </div>
  );
}
```

### Advantages

- **Memory Efficient**: Only active tab in DOM, minimal memory footprint
- **Clean State**: Each tab renders fresh (useful for data collection)
- **Performance**: Good for many tabs or heavy components
- **Scalability**: Can handle dozens of tabs without memory concerns

### Disadvantages

- **State Lost**: Form data, scroll position reset on tab switch
- **Reload Latency**: Slight delay when rendering complex components
- **Component Reset**: Components lose their internal state

### When to Use

- Performance-critical applications
- Many tabs (15+) with complex components
- When state isolation between tabs is desired
- Login workflows where each tab should reset state
- Data collection forms where fresh state is important

### Example: Multi-Step Wizard

```jsx
<TabComponent loadOn="Dynamic">
  <TabItemsDirective>
    <TabItemDirective 
      header={{ text: 'Step 1: Personal' }}
      content={<PersonalForm />}
    />
    <TabItemDirective 
      header={{ text: 'Step 2: Address' }}
      content={<AddressForm />}
    />
    <TabItemDirective 
      header={{ text: 'Step 3: Confirm' }}
      content={<ConfirmationForm />}
    />
  </TabItemsDirective>
</TabComponent>
```

Each step reloads, preventing accidental data carryover between wizard stages.

## Initial Rendering

**Mode**: Render all tab content upfront during component initialization.

### How It Works

1. Tab component initializes with ALL tab content rendered and in DOM
2. Clicking tabs switches active display without rendering/unrendering
3. All tab content stays in DOM throughout component lifetime
4. No rendering happens during tab switches

### Configuration

```jsx
<TabComponent loadOn="Init">
  <TabItemsDirective>
    <TabItemDirective header={{ text: 'Tab 1' }} content="Content 1" />
    <TabItemDirective header={{ text: 'Tab 2' }} content="Content 2" />
    <TabItemDirective header={{ text: 'Tab 3' }} content="Content 3" />
  </TabItemsDirective>
</TabComponent>
```

### Code Example: Initial Rendering

```jsx
import React, { useState } from 'react';
import { TabComponent, TabItemsDirective, TabItemDirective } from '@syncfusion/ej2-react-navigations';

export default function InitialTab() {
  const [tab1Input, setTab1Input] = useState('');
  const [tab2Input, setTab2Input] = useState('');
  const [tab3Input, setTab3Input] = useState('');

  return (
    <div style={{ padding: '20px' }}>
      <h2>Initial Rendering Mode</h2>
      <p>All tab content loaded upfront. Form data persists as you switch tabs.</p>
      
      <TabComponent loadOn="Init">
        <TabItemsDirective>
          <TabItemDirective 
            header={{ text: 'Personal Info' }}
            content={
              <div style={{ padding: '10px' }}>
                <label>Name: </label>
                <input 
                  type="text" 
                  value={tab1Input}
                  onChange={(e) => setTab1Input(e.target.value)}
                  placeholder="Enter name"
                />
                <p>Current value: {tab1Input}</p>
              </div>
            }
          />
          <TabItemDirective 
            header={{ text: 'Email' }}
            content={
              <div style={{ padding: '10px' }}>
                <label>Email: </label>
                <input 
                  type="email" 
                  value={tab2Input}
                  onChange={(e) => setTab2Input(e.target.value)}
                  placeholder="Enter email"
                />
                <p>Current value: {tab2Input}</p>
              </div>
            }
          />
          <TabItemDirective 
            header={{ text: 'Phone' }}
            content={
              <div style={{ padding: '10px' }}>
                <label>Phone: </label>
                <input 
                  type="tel" 
                  value={tab3Input}
                  onChange={(e) => setTab3Input(e.target.value)}
                  placeholder="Enter phone"
                />
                <p>Current value: {tab3Input}</p>
              </div>
            }
          />
        </TabItemsDirective>
      </TabComponent>

      <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>
        <h3>Summary (All Data Preserved)</h3>
        <p>Name: {tab1Input}</p>
        <p>Email: {tab2Input}</p>
        <p>Phone: {tab3Input}</p>
      </div>
    </div>
  );
}
```

### Advantages

- **State Preservation**: All form data and component state persists
- **No Reload**: Instant tab switching (no rendering)
- **Full Access**: Can reference components in other tabs
- **Simplicity**: No need to manage state across tab switches

### Disadvantages

- **Initial Load**: Slower startup (all content rendered immediately)
- **Memory**: All content in DOM always (can be large with many tabs)
- **Not Scalable**: Impractical for 10+ tabs with heavy components
- **Performance**: DOM grows with each tab

### When to Use

- Small number of tabs (3-5)
- Lightweight content
- Forms where all data must be preserved and accessible
- When you need to access components across tabs
- Applications where user needs to see all data at once

## Choosing the Right Mode

### Decision Matrix

```
Number of Tabs?
├─ 1-3 tabs        → Use "Init" (initial rendering)
├─ 3-10 tabs       → Use "Demand" (on-demand, default)
└─ 10+ tabs        → Use "Dynamic" (dynamic rendering)

Content Complexity?
├─ Heavy (calendar, scheduler, grid)  → Use "Dynamic" or "Demand"
├─ Moderate                           → Use "Demand"
└─ Light (text, simple forms)         → Use any mode

State Preservation Important?
├─ Yes, preserve all data             → Use "Init" or "Demand"
└─ No, isolate state per tab          → Use "Dynamic"

Performance Priority?
├─ Initial load speed                 → Use "Dynamic" or "Demand"
├─ Tab switch speed                   → Use "Init" or "Demand"
└─ Memory efficiency                  → Use "Dynamic"
```

### Common Scenarios

**Dashboard with 3-4 tabs (grid, chart, table):**
```jsx
<TabComponent loadOn="Demand">  // Good balance
```

**Multi-step form wizard:**
```jsx
<TabComponent loadOn="Dynamic">  // Fresh state each step
```

**User profile with all editable fields:**
```jsx
<TabComponent loadOn="Init">  // Preserve all changes
```

**File manager with many categories:**
```jsx
<TabComponent loadOn="Dynamic">  // Many tabs, memory concern
```

## Performance Comparison

```
Mode         | Initial Load | Tab Switch | Memory | State Preserved
-------------|--------------|------------|--------|----------------
Demand       | Fast         | Instant    | Medium | Yes
Dynamic      | Fast         | Fast       | Low    | No
Init         | Slow         | Instant    | High   | Yes

Example (with 10 tabs of heavy components):
Demand:  Initial: 50ms,  Switch: instant,  Memory: 500MB final
Dynamic: Initial: 50ms,  Switch: 100ms,    Memory: 50MB
Init:    Initial: 500ms, Switch: instant,  Memory: 500MB initial
```
