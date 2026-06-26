# Next.js Integration Reference - Syncfusion React Pivot Table

## Overview

Next.js is a React framework for building fast, SEO-friendly web applications with server-side rendering. Syncfusion Pivot Table works seamlessly in Next.js with the App Router.

## Key Requirements

| Requirement | Details |
|-------------|---------|
| Node.js | 18.17.0 or later (LTS recommended) |
| Package Manager | NPM or Yarn |
| Framework | Next.js with App Router |

## Setup Steps

### 1. Create Next.js Application

```bash
npx create-next-app@latest
# or
yarn create next-app
```

When prompted, select **Yes, use recommended defaults** (TypeScript, ESLint, Tailwind CSS, App Router).

### 2. Install Syncfusion Package

```bash
npm install @syncfusion/ej2-react-pivotview --save
# or
yarn add @syncfusion/ej2-react-pivotview
```

### 3. Import CSS Styles

In **app/globals.css**, add Tailwind 3 theme imports:

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-grids/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-lists/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-splitbuttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-calendars/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-react-pivotview/styles/tailwind3.css';
```

> Other themes available: Material, Bootstrap, Fabric, High Contrast. See [themes documentation](https://ej2.syncfusion.com/react/documentation/appearance/theme).

### 4. Create Data Source

Create **app/datasource.tsx**:

```typescript
export let pivotData: object[] = [
    { 'In_Stock': 42, 'Sold': 80, 'Amount': 2460, 'Country': 'Germany', 'Product_Categories': 'Accessories', 'Products': 'Hydration Packs', 'Order_Source': 'Retail Outlets', 'Year': 'FY 2015', 'Quarter': 'Q1' },
    { 'In_Stock': 19, 'Sold': 16, 'Amount': 184, 'Country': 'Germany', 'Product_Categories': 'Accessories', 'Products': 'Fenders', 'Order_Source': 'Retail Outlets', 'Year': 'FY 2015', 'Quarter': 'Q1' }
];
```

### 5. Create Page Component

Create **app/page.tsx** with `'use client'` directive:

```typescript
'use client'
import { CalculatedField, FieldList, IDataSet, Inject, PivotViewComponent } from '@syncfusion/ej2-react-pivotview';
import { DataSourceSettingsModel } from '@syncfusion/ej2-pivotview/src/model/datasourcesettings-model';
import { pivotData } from './datasource';

export default function Home() {
  const dataSourceSettings: DataSourceSettingsModel = {
    columns: [{ name: 'Year', caption: 'Production Year' }, { name: 'Quarter' }],
    dataSource: pivotData as IDataSet[],
    expandAll: false,
    filters: [],
    drilledMembers: [{ name: 'Country', items: ['Germany'] }],
    formatSettings: [{ name: 'Amount', format: 'C0' }],
    rows: [{ name: 'Country' }, { name: 'Products' }],
    values: [{ name: 'Sold', caption: 'Units Sold' }, { name: 'Amount', caption: 'Sold Amount' }]
  };

  return (
    <>
      <h2>Syncfusion React Pivot Table Component</h2>
      <PivotViewComponent
        id="PivotView"
        height={350}
        dataSourceSettings={dataSourceSettings}
        allowCalculatedField={true}
        showFieldList={true}
      >
        <Inject services={[CalculatedField, FieldList]} />
      </PivotViewComponent>
    </>
  );
}
```

### 6. Run the Application

```bash
npm run dev
# or
yarn run dev
```

## Key Points

- **`'use client'` is required** for interactive Syncfusion components in App Router
- **Module injection** is needed for features like `CalculatedField` and `FieldList`
- **CSS imports** must be in globals.css for themes to work

## Run Commands

| Package Manager | Command |
|-----------------|---------|
| NPM | `npm run dev` |
| Yarn | `yarn run dev` |

## Related Features

- **Getting Started**: Basic setup without Next.js
- **Field List**: Interactive field configuration UI
- **Calculated Field**: Create custom calculated fields
- **Module Injection**: Required service injections

## See Also

- [Next.js Pivot Table Sample](https://github.com/SyncfusionExamples/ej2-nextjs-pivotview)
- [Module Injection Documentation](https://ej2.syncfusion.com/react/documentation/pivotview/getting-started#module-injection)
