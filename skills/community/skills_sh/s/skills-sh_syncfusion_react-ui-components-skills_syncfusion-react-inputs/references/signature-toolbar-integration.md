# Toolbar Integration with Syncfusion React Signature

## Table of Contents
- [Overview](#overview)
- [Required Packages](#required-packages)
- [Wiring Undo, Redo, and Clear](#wiring-undo-redo-and-clear)
- [Save Button Integration](#save-button-integration)
- [Stroke Color Picker](#stroke-color-picker)
- [Background Color Picker](#background-color-picker)
- [Stroke Width Dropdown](#stroke-width-dropdown)
- [Full Toolbar Example](#full-toolbar-example)

---

## Overview

Integrate `SignatureComponent` with `ToolbarComponent` to provide a rich editing interface. The Signature's `change` event drives toolbar button state — enabling/disabling undo, redo, clear, and save based on the current signature state.

**Key pattern:**
- Call `canUndo()`, `canRedo()`, and `isEmpty()` inside the `change` handler to update button states.
- Use the toolbar's `clicked` event to dispatch actions to the Signature component.

---

## Required Packages

```bash
npm install @syncfusion/ej2-react-inputs @syncfusion/ej2-react-navigations @syncfusion/ej2-react-buttons @syncfusion/ej2-react-splitbuttons @syncfusion/ej2-react-dropdowns --save
```

---

## Wiring Undo, Redo, and Clear

Use `tooltipText` on `ItemDirective` to identify toolbar button actions inside the `clicked` handler:

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { ToolbarComponent, ItemsDirective, ItemDirective, ClickEventArgs } from '@syncfusion/ej2-react-navigations';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  function onClicked(args: ClickEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    switch (args.item.tooltipText) {
      case 'Undo (Ctrl + Z)':
        if (signature.canUndo()) signature.undo();
        break;
      case 'Redo (Ctrl + Y)':
        if (signature.canRedo()) signature.redo();
        break;
      case 'Clear':
        signature.clear();
        break;
    }
  }

  return (
    <div>
      <ToolbarComponent clicked={onClicked}>
        <ItemsDirective>
          <ItemDirective text="Undo" prefixIcon="e-icons e-undo" tooltipText="Undo (Ctrl + Z)" />
          <ItemDirective text="Redo" prefixIcon="e-icons e-redo" tooltipText="Redo (Ctrl + Y)" />
          <ItemDirective text="Clear" prefixIcon="e-sign-icons e-clear" tooltipText="Clear" />
        </ItemsDirective>
      </ToolbarComponent>
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

---

## Save Button Integration

Use a `SplitButtonComponent` inside a toolbar template to let users choose the save format (PNG, JPEG, SVG):

```tsx
import { SignatureComponent, SignatureFileType } from '@syncfusion/ej2-react-inputs';
import { SplitButtonComponent } from '@syncfusion/ej2-react-splitbuttons';
import { MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const saveItems = [{ text: 'Png' }, { text: 'Jpeg' }, { text: 'Svg' }];

  function onSelect(args: MenuEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    signature.save(args.item.text as SignatureFileType, 'Signature');
  }

  function saveTemplate() {
    return (
      <SplitButtonComponent
        content="Save"
        id="save-option"
        iconCss="e-sign-icons e-save"
        items={saveItems}
        select={onSelect}
        disabled={true}
      />
    );
  }

  return (
    <div>
      {saveTemplate()}
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

Enable the save button by calling `saveBtn.disabled = false` inside the `change` handler when `!signature.isEmpty()`.

---

## Stroke Color Picker

Use `ColorPickerComponent` in a toolbar template to let users change the stroke color dynamically:

```tsx
import { ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const strokePresets = {
    custom: ['#000000', '#e91e63', '#9c27b0', '#673ab7', '#2196f3', '#03a9f4',
      '#00bcd4', '#009688', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107']
  };

  function onStrokeColorChanged(args: ColorPickerEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    if (!signature.disabled) {
      signature.strokeColor = args.currentValue.rgba;
    }
  }

  return (
    <div>
      <ColorPickerComponent
        id="stroke-color"
        mode="Palette"
        modeSwitcher={false}
        showButtons={false}
        columns={4}
        presetColors={strokePresets}
        change={onStrokeColorChanged}
      />
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

---

## Background Color Picker

Use a second `ColorPickerComponent` to change the canvas background color:

```tsx
import { ColorPickerComponent, ColorPickerEventArgs, SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const bgPresets = {
    custom: ['#ffffff', '#f44336', '#e91e63', '#9c27b0', '#673ab7', '#2196f3',
      '#03a9f4', '#00bcd4', '#009688', '#8bc34a', '#cddc39', '#ffeb3b']
  };

  function onBgColorChanged(args: ColorPickerEventArgs): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    if (!signature.disabled) {
      signature.backgroundColor = args.currentValue.rgba;
    }
  }

  return (
    <div>
      <ColorPickerComponent
        id="bg-color"
        noColor={true}
        mode="Palette"
        modeSwitcher={false}
        showButtons={false}
        columns={4}
        presetColors={bgPresets}
        change={onBgColorChanged}
      />
      <SignatureComponent id="signature" />
    </div>
  );
}
export default App;
```

---

## Stroke Width Dropdown

Use a `DropDownListComponent` to let users select the maximum stroke width:

```tsx
import { SignatureComponent } from '@syncfusion/ej2-react-inputs';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import { getComponent } from '@syncfusion/ej2-base';
import * as React from 'react';

function App() {
  const widthData: number[] = [1, 2, 3, 4, 5];

  function onWidthChanged(args: any): void {
    const signature: any = getComponent(document.getElementById('signature'), 'signature');
    signature.maxStrokeWidth = args.value;
  }

  return (
    <div>
      <DropDownListComponent
        id="stroke-width-ddl"
        dataSource={widthData}
        value={2}
        width="60"
        change={onWidthChanged}
      />
      <SignatureComponent id="signature" maxStrokeWidth={2} />
    </div>
  );
}
export default App;
```

---

## Full Toolbar Example

Complete integration using `ToolbarComponent` with undo, redo, save (split button), stroke color picker, background color picker, stroke width dropdown, clear, and a disabled toggle:

```tsx
import * as React from 'react';
import { SignatureComponent, SignatureFileType, ColorPickerComponent, ColorPickerEventArgs } from '@syncfusion/ej2-react-inputs';
import { ToolbarComponent, ItemsDirective, ItemDirective, ClickEventArgs } from '@syncfusion/ej2-react-navigations';
import { SplitButtonComponent, MenuEventArgs } from '@syncfusion/ej2-react-splitbuttons';
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import { CheckBoxComponent } from '@syncfusion/ej2-react-buttons';
import { getComponent } from '@syncfusion/ej2-base';
import { ChangeEventArgs } from '@syncfusion/ej2-buttons';

function App() {
  const saveItems = [{ text: 'Png' }, { text: 'Jpeg' }, { text: 'Svg' }];
  const widthData = [1, 2, 3, 4, 5];
  const strokePresets = { custom: ['#000000','#e91e63','#9c27b0','#673ab7','#2196f3','#03a9f4','#00bcd4','#009688','#8bc34a','#cddc39','#ffeb3b','#ffc107'] };
  const bgPresets = { custom: ['#ffffff','#f44336','#e91e63','#9c27b0','#673ab7','#2196f3','#03a9f4','#00bcd4','#009688','#8bc34a','#cddc39','#ffeb3b'] };

  function onClicked(args: ClickEventArgs): void {
    const sig: any = getComponent(document.getElementById('signature'), 'signature');
    if (sig.disabled && args.item.tooltipText !== 'Disabled') return;
    switch (args.item.tooltipText) {
      case 'Undo (Ctrl + Z)': if (sig.canUndo()) sig.undo(); break;
      case 'Redo (Ctrl + Y)': if (sig.canRedo()) sig.redo(); break;
      case 'Clear': sig.clear(); break;
    }
  }

  function onChange(): void {
    const sig: any = getComponent(document.getElementById('signature'), 'signature');
    // Update undo/redo/clear/save button states based on sig.canUndo(), sig.canRedo(), sig.isEmpty()
  }

  function onDisabledChange(args: ChangeEventArgs): void {
    const sig: any = getComponent(document.getElementById('signature'), 'signature');
    sig.disabled = args.checked;
  }

  function saveTemplate() {
    return (
      <SplitButtonComponent content="Save" id="save-option" iconCss="e-sign-icons e-save" items={saveItems}
        select={(args: MenuEventArgs) => {
          const sig: any = getComponent(document.getElementById('signature'), 'signature');
          sig.save(args.item.text as SignatureFileType, 'Signature');
        }} disabled={true} />
    );
  }

  function strokeColorTemplate() {
    return (
      <ColorPickerComponent id="stroke-color" mode="Palette" modeSwitcher={false} showButtons={false}
        columns={4} presetColors={strokePresets}
        change={(args: ColorPickerEventArgs) => {
          const sig: any = getComponent(document.getElementById('signature'), 'signature');
          if (!sig.disabled) sig.strokeColor = args.currentValue.rgba;
        }} />
    );
  }

  function bgColorTemplate() {
    return (
      <ColorPickerComponent id="bg-color" noColor={true} mode="Palette" modeSwitcher={false} showButtons={false}
        columns={4} presetColors={bgPresets}
        change={(args: ColorPickerEventArgs) => {
          const sig: any = getComponent(document.getElementById('signature'), 'signature');
          if (!sig.disabled) sig.backgroundColor = args.currentValue.rgba;
        }} />
    );
  }

  function strokeWidthTemplate() {
    return (
      <DropDownListComponent id="stroke-width-ddl" dataSource={widthData} value={2} width="60"
        change={(args: any) => {
          const sig: any = getComponent(document.getElementById('signature'), 'signature');
          sig.maxStrokeWidth = args.value;
        }} />
    );
  }

  return (
    <div>
      <ToolbarComponent id="toolbar" clicked={onClicked}>
        <ItemsDirective>
          <ItemDirective text="Undo" prefixIcon="e-icons e-undo" tooltipText="Undo (Ctrl + Z)" />
          <ItemDirective text="Redo" prefixIcon="e-icons e-redo" tooltipText="Redo (Ctrl + Y)" />
          <ItemDirective type="Separator" />
          <ItemDirective tooltipText="Save (Ctrl + S)" type="Button" template={saveTemplate} />
          <ItemDirective type="Separator" />
          <ItemDirective tooltipText="Stroke Color" template={strokeColorTemplate} />
          <ItemDirective type="Separator" />
          <ItemDirective tooltipText="Background Color" template={bgColorTemplate} />
          <ItemDirective type="Separator" />
          <ItemDirective tooltipText="Stroke Width" template={strokeWidthTemplate} />
          <ItemDirective type="Separator" />
          <ItemDirective text="Clear" prefixIcon="e-sign-icons e-clear" tooltipText="Clear" />
          <ItemDirective tooltipText="Disabled" type="Input"
            template={<CheckBoxComponent label="Disabled" change={onDisabledChange} />} align="Right" />
        </ItemsDirective>
      </ToolbarComponent>
      <SignatureComponent id="signature" maxStrokeWidth={2} change={onChange} />
    </div>
  );
}
export default App;
```
