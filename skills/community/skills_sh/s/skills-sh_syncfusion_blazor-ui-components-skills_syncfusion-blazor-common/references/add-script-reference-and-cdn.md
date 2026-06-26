# Script References

> **Applies to:** Syncfusion Blazor Components  
> **Framework:** .NET 8, .NET 9, .NET 10 with Blazor Web App  
> **Reference:** [Official Syncfusion Documentation](https://blazor.syncfusion.com/documentation/common/adding-script-references)

---

## Overview

This document covers two critical aspects of Syncfusion Blazor implementation:
- **Adding Script References** — How to reference Syncfusion Blazor scripts in applications


## Adding Script References

### Introduction

JavaScript interop files are required for features that cannot be implemented natively in Blazor. Syncfusion® Blazor scripts must be properly referenced based on your application type and render mode.

### CDN Reference Method

#### Basic CDN Reference
- For .NET 8, .NET 9, and .NET 10 Blazor Web App (any render mode: Server, WebAssembly, or Auto), add scripts in `~/Components/App.razor`
- For Blazor WebAssembly (standalone) App, add scripts in `~/wwwroot/index.html`

**Important:** Ensure the version in the CDN URLs matches the NuGet package version used in the application.

#### Main Script Reference
```html
<head>
    <script src="https://cdn.syncfusion.com/blazor/33.1.44/syncfusion-blazor.min.js" type="text/javascript"></script>
</head>
```

### Static Web Assets Method

#### Enable Static Web Assets
Call `UseStaticFiles()` in the app's `~/Program.cs` file:
- For Blazor Web App (interactive mode: Auto) and Blazor WebAssembly App, call `UseStaticFiles()` in the Server project.

#### Reference Scripts from Static Web Assets
Combined scripts are available in the `Syncfusion.Blazor.Core` package:
```html
<head>
    <script src="_content/Syncfusion.Blazor.Core/scripts/syncfusion-blazor.min.js" type="text/javascript"></script>
</head>
```

### Individual Component Script References

For minimal component usage, reference component-specific scripts directly instead of the full library.

#### Reference Approach
| Usage | Script Reference Format |
|-------|------------------------|
| Static Web Assets | `_content/Syncfusion.Blazor.Core/scripts/<component-script>` |
| CDN | `https://cdn.syncfusion.com/blazor/<version>/<component-script>` |

#### Component Script File Mapping

| Component(s) | Script File |
|---|---|
| TextBox | `sf-textbox.min.js` |
| NumericTextBox | `sf-numerictextbox.min.js` |
| MaskedTextBox | `sf-maskedtextbox.min.js` |
| Uploader | `sf-uploader.min.js` |
| Calendar | `sf-calendar.min.js` |
| DatePicker, DateTimePicker | `sf-datepicker.min.js` |
| DateRangePicker | `sf-daterangepicker.min.js` |
| TimePicker | `sf-timepicker.min.js` |
| AutoComplete, ComboBox, DropDownList | `sf-dropdownlist.min.js` |
| MultiSelect | `sf-multiselect.min.js` |
| DropDownButton, SplitButton | `sf-drop-down-button.min.js` |
| ProgressButton, Spinner | `sf-spinner.min.js` |
| ListBox | `sf-listbox.min.js` |
| ColorPicker | `sf-colorpicker.min.js` |
| Signature | `sf-signature.min.js` |
| ContextMenu | `sf-contextmenu.min.js` |
| Menu | `sf-menu.min.js` |
| Breadcrumb | `sf-breadcrumb.min.js` |
| QueryBuilder | `sf-querybuilder.min.js` |
| Grid | `sf-grid.min.js` |
| Accordion | `sf-accordion.min.js` |
| Tab | `sf-tab.min.js` |
| Toolbar | `sf-toolbar.min.js` |
| Schedule | `sf-schedule.min.js` |
| BarcodeGenerator | `sf-barcode.min.js` |
| Maps | `sf-maps.min.js` |
| CircularGauge | `sf-circulargauge.min.js` |
| LinearGauge | `sf-lineargauge.min.js` |
| Chart | `sf-chart.min.js` |
| CheckBox | `sf-checkbox.min.js` |
| AccumulationChart | `sf-accumulation-chart.min.js` |
| StockChart | `sf-stock-chart.min.js` |
| BulletChart | `sf-bullet-chart.min.js` |
| Sparkline | `sf-sparkline.min.js` |
| TreeMap | `sf-treemap.min.js` |
| ProgressBar | `sf-progressbar.min.js` |
| SmithChart | `sf-smith-chart.min.js` |
| RangeNavigator | `sf-range-navigator.min.js` |
| HeatMap | `sf-heatmap.min.js` |
| FileManager | `sf-filemanager.min.js` |
| Slider | `sf-slider.min.js` |
| Tooltip | `sf-tooltip.min.js` |
| ListView | `sf-listview.min.js` |
| DashboardLayout | `sf-dashboard-layout.min.js` |
| Sidebar | `sf-sidebar.min.js` |
| TreeView | `sf-treeview.min.js` |
| PivotView | `sf-pivotview.min.js` |
| TreeGrid | `sf-treegrid.min.js` |
| Splitter | `sf-splitter.min.js` |
| Switch | `sf-switch.min.js` |
| Toast | `sf-toast.min.js` |
| Dialog | `sf-dialog.min.js` |
| RichTextEditor | `sf-richtexteditor.min.js` |
| InPlaceEditor | `sf-inplaceeditor.min.js` |
| Kanban | `sf-kanban.min.js` |
| Gantt | `sf-gantt.min.js` |
| PdfViewer | `sf-pdfviewer.min.js` |
| ImageEditor | `sf-image-editor.min.js` |
| DocumentEditor | `sf-documenteditor.min.js` |
| Pager | `sf-pager.min.js` |

---

## Summary of Methods

| Method | Best For | Location | Performance |
|--------|----------|----------|-------------|
| **CDN** | Quick setup, always latest version | App.razor / index.html | Medium (network dependent) |
| **Static Web Assets** | Optimal performance, offline support, version control | Static web assets (NuGet package) | Excellent (bundled with app) |
| **Individual Components (CDN)** | Minimal components, specific features | App.razor / index.html | Good (selective loading) |

