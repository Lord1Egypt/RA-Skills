# Templates and Dialogs: Custom Content and Card Editing

## Table of Contents
- [Overview](#overview)
- [Card Templates](#card-templates)
- [Column Header Templates](#column-header-templates)
- [Swimlane Header Templates](#swimlane-header-templates)
- [Tooltip Templates](#tooltip-templates)
- [Dialog Configuration](#dialog-configuration)
- [Dialog Custom Fields](#dialog-custom-fields)
- [Dialog Templates](#dialog-templates)
- [Advanced Patterns](#advanced-patterns)

## Overview

Templates let you customize how Kanban renders cards, headers, and dialogs. They accept JSX functions that return custom HTML. Dialogs enable adding and editing cards with form fields.

## Card Templates

Replace default card layout with custom JSX:

### Basic Card Template

```tsx
import { KanbanComponent } from '@syncfusion/ej2-react-kanban';
import { ReactElement } from 'react';

// Card props expected: { Id, Summary, Priority, Type }
const cardTemplate = (props: any): ReactElement => {
  return (
    <div className="custom-card">
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
        Task #{props.Id}
      </div>
      <div style={{ fontSize: '14px', marginBottom: '8px' }}>
        {props.Summary}
      </div>
      <div style={{ display: 'flex', gap: '5px' }}>
        <span style={{ 
          padding: '2px 8px', 
          backgroundColor: '#e3f2fd', 
          borderRadius: '3px',
          fontSize: '12px'
        }}>
          {props.Priority}
        </span>
        <span style={{ 
          padding: '2px 8px', 
          backgroundColor: '#f3e5f5', 
          borderRadius: '3px',
          fontSize: '12px'
        }}>
          {props.Type}
        </span>
      </div>
    </div>
  );
};

<KanbanComponent
  cardSettings={{
    headerField: 'Id',
    template: cardTemplate  // Use custom template
  }}
>
  {/* ... */}
</KanbanComponent>
```

### Card with Assignee Avatar

```tsx
import { ReactElement } from 'react';

// Card props expected: { Id, Summary, AssigneeId, Assignee, CompletionDate, EstimateHours }
const cardTemplate = (props: any): ReactElement => {
  return (
    <div className="card-with-avatar">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontWeight: 'bold' }}>Task {props.Id}</div>
        <img 
          src={`/avatars/${props.AssigneeId}.jpg`}
          alt={props.Assignee}
          style={{ width: '24px', height: '24px', borderRadius: '50%' }}
          title={props.Assignee}
        />
      </div>
      <div style={{ marginTop: '8px', fontSize: '13px' }}>
        {props.Summary}
      </div>
      <div style={{ marginTop: '8px', display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#666' }}>
        <span>{props.CompletionDate}</span>
        <span>{props.EstimateHours}h</span>
      </div>
    </div>
  );
};
```

### Card with Progress Bar

```tsx
import { ReactElement } from 'react';

// Card props expected: { Summary, CompletionPercentage }
const cardTemplate = (props: any): ReactElement => {
  const completion = props.CompletionPercentage || 0;
  
  return (
    <div>
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
        {props.Summary}
      </div>
      <div style={{ 
        height: '4px', 
        backgroundColor: '#e0e0e0',
        borderRadius: '2px',
        overflow: 'hidden'
      }}>
        <div style={{
          height: '100%',
          backgroundColor: completion < 50 ? '#ff9800' : completion < 100 ? '#2196f3' : '#4caf50',
          width: `${completion}%`,
          transition: 'width 0.3s'
        }} />
      </div>
      <div style={{ fontSize: '11px', marginTop: '4px', color: '#666' }}>
        {completion}% Complete
      </div>
    </div>
  );
};
```

## Column Header Templates

Customize column header appearance:

```tsx
import { ReactElement } from 'react';

const columnHeaderTemplate = (props: { [key: string]: string }): ReactElement => {
  const cardCount = props.cardCount || 0;
  const maxCount = props.maxCount || null;
  
  return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div>
        <div style={{ fontWeight: 'bold' }}>{props.headerText}</div>
        <div style={{ fontSize: '12px', color: '#999' }}>
          {cardCount}{maxCount ? `/${maxCount}` : ''} items
        </div>
      </div>
      {cardCount >= (maxCount || 0) && maxCount ? (
        <span style={{ color: 'red', fontWeight: 'bold' }}>!</span>
      ) : null}
    </div>
  );
};

<ColumnsDirective>
  <ColumnDirective 
    keyField="Open" 
    template={columnHeaderTemplate}
  />
</ColumnsDirective>
```

## Swimlane Header Templates

Customize swimlane row headers:

```tsx
import { ReactElement } from 'react';

// Swimlane props expected: { cardCount, AssigneeId, Assignee, AssigneeName }
const swimlaneTemplate = (props: any): ReactElement => {
  // Count tasks in this swimlane
  const taskCount = props.cardCount || 0;
  
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '8px' }}>
      <img
        src={`/avatars/${props.AssigneeId}.png`}
        alt={props.Assignee}
        style={{ width: '32px', height: '32px', borderRadius: '50%' }}
      />
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: '600' }}>{props.AssigneeName}</div>
        <div style={{ fontSize: '12px', color: '#666' }}>
          {taskCount} {taskCount === 1 ? 'task' : 'tasks'}
        </div>
      </div>
      <div style={{
        padding: '4px 12px',
        backgroundColor: taskCount > 5 ? '#ffebee' : '#e8f5e9',
        borderRadius: '4px',
        fontSize: '12px',
        fontWeight: 'bold'
      }}>
        {taskCount > 5 ? 'Overloaded' : 'OK'}
      </div>
    </div>
  );
};

<KanbanComponent
  swimlaneSettings={{
    keyField: 'Assignee',
    template: swimlaneTemplate
  }}
>
  {/* ... */}
</KanbanComponent>
```

## Tooltip Templates

Customize card tooltip on hover:

```tsx
import { ReactElement } from 'react';

// Card props expected: { Summary, Priority, Assignee, DueDate }
const tooltipTemplate = (props: any): ReactElement => {
  return (
    <div style={{ padding: '10px' }}>
      <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
        {props.Summary}
      </div>
      <table style={{ fontSize: '12px', color: '#666' }}>
        <tbody>
          <tr>
            <td><strong>Priority:</strong></td>
            <td>{props.Priority}</td>
          </tr>
          <tr>
            <td><strong>Assignee:</strong></td>
            <td>{props.Assignee}</td>
          </tr>
          <tr>
            <td><strong>Due:</strong></td>
            <td>{props.DueDate}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

<KanbanComponent
  tooltipSettings={{
    template: tooltipTemplate
  }}
>
  {/* ... */}
</KanbanComponent>
```

## Dialog Configuration

Double-click a card to open the default dialog for editing. Use `showAddButton` on columns to enable card addition:

```tsx
import { useRef } from 'react';
import { KanbanComponent, ColumnsDirective, ColumnDirective } from '@syncfusion/ej2-react-kanban';

// Dialog field structure: { key, text, type, dropdownData? }
const kanbanRef = useRef<KanbanComponent>(null);

<KanbanComponent
  id="kanban"
  ref={kanbanRef}
  keyField="Status"
  dataSource={data}
  cardSettings={{ 
    headerField: 'Id',
    contentField: 'Summary'
  }}
  dialogSettings={{
    fields: [
      { key: 'Id', text: 'Task ID', type: 'TextBox' } as DialogField,
      { key: 'Summary', text: 'Summary', type: 'TextArea' } as DialogField,
      { key: 'Status', text: 'Status', type: 'DropDown' } as DialogField,
      { key: 'Priority', text: 'Priority', type: 'DropDown' } as DialogField,
      { key: 'Assignee', text: 'Assigned To', type: 'DropDown' } as DialogField
    ]
  }}
>
  <ColumnsDirective>
    <ColumnDirective keyField="Open" headerText="Open" showAddButton={true} />
    <ColumnDirective keyField="InProgress" headerText="In Progress" showAddButton={true} />
    <ColumnDirective keyField="Closed" headerText="Closed" showAddButton={true} />
  </ColumnsDirective>
</KanbanComponent>
```

**How to enable Add/Edit/Delete operations:**
- **Add Cards**: Click the "+" (`showAddButton`) on any column header
- **Edit Cards**: Double-click any card to open edit dialog
- **Delete Cards**: Use `kanbanRef.current?.deleteCard(cardId)` method or context menu

## Dialog Custom Fields

Define custom fields with specific input types:

```tsx
// Dialog field structure: { key, text, type, dropdownData? }
const dialogSettings = {
  fields: [
    {
      key: 'Id',
      text: 'Task ID',
      type: 'TextBox'
    } as DialogField,
    {
      key: 'Summary',
      text: 'Description',
      type: 'TextArea'
    } as DialogField,
    {
      key: 'Status',
      text: 'Workflow Status',
      type: 'DropDown',
      dropdownData: ['Open', 'InProgress', 'Testing', 'Closed']
    } as DialogField,
    {
      key: 'Priority',
      text: 'Priority Level',
      type: 'DropDown',
      dropdownData: ['Low', 'Medium', 'High', 'Critical']
    } as DialogField,
    {
      key: 'EstimateHours',
      text: 'Effort (hours)',
      type: 'Numeric'
    } as DialogField,
    {
      key: 'DueDate',
      text: 'Due Date',
      type: 'DateTime'
    } as DialogField
  ]
};

<KanbanComponent dialogSettings={dialogSettings}>
  {/* ... */}
</KanbanComponent>
```

### Field Types Available
- **TextBox**: Single-line text input
- **TextArea**: Multi-line text
- **Numeric**: Number input
- **DropDown**: Select list
- **Date**: Date picker

## Dialog Templates

Replace default dialog with custom form:

```tsx
import React, { useState, ReactElement } from 'react';

// Card data shape: { Id, Summary, Status }
const dialogTemplate = (props: any): ReactElement => {
  const [formData, setFormData] = useState(props);

  const handleChange = (field: keyof { [key: string]: Object }, value: string): void => {
    setFormData({ ...formData, [field]: value });
  };

  return (
    <div style={{ padding: '20px' }}>
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
          Task ID
        </label>
        <input 
          type="text" 
          disabled
          value={formData.Id}
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
          Summary
        </label>
        <textarea
          value={formData.Summary}
          onChange={(e): void => handleChange('Summary', e.target.value)}
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc', minHeight: '80px' }}
        />
      </div>

      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
          Status
        </label>
        <select
          value={formData.Status}
          onChange={(e): void => handleChange('Status', e.target.value)}
          style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        >
          <option value="Open">Open</option>
          <option value="InProgress">In Progress</option>
          <option value="Closed">Closed</option>
        </select>
      </div>
    </div>
  );
};

<KanbanComponent
  dialogSettings={{
    template: dialogTemplate
  }}
>
  {/* ... */}
</KanbanComponent>
```

## Advanced Patterns

### Add Rich Text Editor to Dialog

```tsx
import { RichTextEditorComponent } from '@syncfusion/ej2-react-richtexteditor';
import { ReactElement } from 'react';

// Card data shape: { Id, DetailedDescription }
const dialogTemplate = (props: any): ReactElement => {
  return (
    <div>
      {/* ... other fields ... */}
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
          Detailed Description
        </label>
        <RichTextEditorComponent 
          value={props.DetailedDescription}
          onChange={(e: any): void => { props.DetailedDescription = e.value; }}
        />
      </div>
    </div>
  );
};
```

### Card Click to Open Modal

```tsx
import { CardClickEventArgs } from '@syncfusion/ej2-react-kanban';

// Use CardClickEventArgs from Syncfusion library
const handleCardClick = (args: CardClickEventArgs): void => {
  // Open custom modal instead of default dialog
  showCustomEditModal(args.data);
};

<KanbanComponent cardClick={handleCardClick}>
  {/* ... */}
</KanbanComponent>
```

### Prevent Dialog from Opening on Double-Click

```tsx
import { DialogEventArgs } from '@syncfusion/ej2-react-kanban';

// Use DialogEventArgs from Syncfusion library
const handleDialogOpen = (args: DialogEventArgs): void => {
  // Prevent default dialog
  args.cancel = true;
  
  // Open custom form or modal
  openCustomEditForm(args.data);
};

<KanbanComponent dialogOpen={handleDialogOpen}>
  {/* ... */}
</KanbanComponent>
```
