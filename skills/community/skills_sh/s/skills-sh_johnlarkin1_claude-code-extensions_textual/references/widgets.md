# Textual Widget Reference

## Table of Contents
- [Container Widgets](#container-widgets)
- [Input Widgets](#input-widgets)
- [Display Widgets](#display-widgets)
- [Structural Widgets](#structural-widgets)
- [Widget Messages](#widget-messages)
- [Key Imports](#key-imports)

## Container Widgets

| Widget | Purpose |
|--------|---------|
| `Container` | Basic container |
| `Horizontal` | Horizontal layout |
| `Vertical` | Vertical layout |
| `VerticalScroll` | Scrollable vertical |
| `HorizontalScroll` | Scrollable horizontal |
| `Grid` | Grid layout |
| `ScrollableContainer` | General scrollable container |
| `Center` | Center content horizontally |
| `Middle` | Center content vertically |

## Input Widgets

| Widget | Purpose |
|--------|---------|
| `Button` | Clickable button |
| `Input` | Text input field |
| `MaskedInput` | Formatted input |
| `TextArea` | Multi-line text editor |
| `Checkbox` | Boolean checkbox |
| `Switch` | Toggle switch |
| `RadioButton` | Radio button |
| `RadioSet` | Group of radio buttons |
| `Select` | Dropdown selection |
| `SelectionList` | Multi-select list |
| `OptionList` | Option list |

## Display Widgets

| Widget | Purpose |
|--------|---------|
| `Static` | Static text (cached render) |
| `Label` | Text label |
| `Digits` | Large digit display |
| `Pretty` | Pretty-printed objects |
| `Markdown` | Markdown content |
| `MarkdownViewer` | Scrollable markdown |
| `RichLog` | Scrolling rich text log |
| `Log` | Simple text log |
| `ProgressBar` | Progress indicator |
| `LoadingIndicator` | Loading animation |
| `Sparkline` | Mini line chart |
| `Rule` | Horizontal/vertical rule |
| `Placeholder` | Development placeholder |

## Structural Widgets

| Widget | Purpose |
|--------|---------|
| `Header` | App header |
| `Footer` | App footer with bindings |
| `Tabs` | Tab bar |
| `TabbedContent` | Tabbed panels |
| `ContentSwitcher` | Switch between content |
| `Collapsible` | Collapsible section |
| `Tree` | Tree view |
| `DirectoryTree` | File/folder tree |
| `DataTable` | Data table with sorting |
| `ListView` | List of items |
| `ListItem` | Item in ListView |
| `Toast` | Temporary notification |
| `Tooltip` | Hover tooltip |

## Widget Messages

### Input Widget Messages
```python
Button.Pressed
Input.Changed
Input.Submitted
Switch.Changed
Checkbox.Changed
Select.Changed
```

### Data Widget Messages
```python
DataTable.CellSelected
DataTable.RowSelected
DataTable.CellHighlighted
```

### Tree Widget Messages
```python
Tree.NodeSelected
Tree.NodeExpanded
Tree.NodeCollapsed
DirectoryTree.FileSelected
DirectoryTree.DirectorySelected
```

### Tab Widget Messages
```python
TabbedContent.TabActivated
Tabs.TabActivated
Tabs.Cleared
```

## Key Imports

```python
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import (
    Button, Input, Label, Static, Header, Footer,
    DataTable, Tree, TabbedContent, Markdown,
    Checkbox, Switch, Select, ProgressBar,
    TextArea, RichLog, DirectoryTree, ListView
)
from textual.containers import (
    Container, Horizontal, Vertical, Grid,
    VerticalScroll, HorizontalScroll, Center, Middle
)
from textual.reactive import reactive, var
from textual.message import Message
from textual import on, work
from textual.worker import Worker, get_current_worker
```
