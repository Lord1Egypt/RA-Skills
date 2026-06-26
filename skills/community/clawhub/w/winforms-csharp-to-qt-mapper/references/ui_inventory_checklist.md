# UI功能清单与规格检查

迁移前必须详细记录WinForms应用的所有UI细节,确保迁移后的Qt版本实现100%一致的视觉效果和交互体验。

---

## 📋 1. 窗体级别检查清单

### 1.1 主窗体属性

| 属性 | WinForms值 | Qt对应设置 | 验证方法 |
|-----|-----------|-----------|---------|
| 窗体标题 | `Text` | `setWindowTitle()` | 目测对比 |
| 窗体大小 | `Size` | `resize()` | 像素级测量 |
| 最小大小 | `MinimumSize` | `setMinimumSize()` | 测试调整 |
| 最大大小 | `MaximumSize` | `setMaximumSize()` | 测试调整 |
| 起始位置 | `StartPosition` | 无对应 | 手动设置Geometry |
| 窗体状态 | `WindowState` | `showNormal/Maximized/Minimized()` | 测试行为 |
| 图标 | `Icon` | `setWindowIcon()` | 目测对比 |
| 背景色 | `BackColor` | `setPalette/QSS` | 取色器对比 |
| 透明度 | `Opacity` | `setWindowOpacity()` | 对比透明效果 |
| 边框样式 | `FormBorderStyle` | `setWindowFlags()` | 对比边框 |
| 显示/隐藏任务栏 | `ShowInTaskbar` | 无对应 | 系统行为 |
| 是否置顶 | `TopMost` | `setWindowFlags(Qt::WindowStaysOnTopHint)` | 测试置顶 |
| 窗体阴影 | - | QGraphicsDropShadowEffect | 目测对比 |

**记录模板**:
```markdown
### 窗体名称: MainForm

- 标题: "光纤光栅信号处理系统"
- 大小: 1280x768
- 最小大小: 1024x600
- 起始位置: CenterScreen
- 初始状态: Normal
- 图标: assets/icon.ico
- 背景色: RGB(240, 240, 240)
- 边框样式: Sizable
- 窗体阴影: 无
```

---

## 📋 2. 控件级别检查清单

### 2.1 控件通用属性

| 属性 | WinForms值 | Qt对应设置 | 验证方法 |
|-----|-----------|-----------|---------|
| 控件名称 | `Name` | `setObjectName()` | 代码引用 |
| 控件位置 | `Location` (X, Y) | `move()` / Layout | 像素级测量 |
| 控件大小 | `Size` (Width, Height) | `resize()` | 像素级测量 |
| 锚点 | `Anchor` | Layout + sizePolicy | 测试缩放 |
| 停靠 | `Dock` | QDockWidget | 测试停靠 |
| Tab顺序 | `TabIndex` | `setTabOrder()` | 测试Tab键 |
| 可见性 | `Visible` | `setVisible()` | 目测对比 |
| 启用状态 | `Enabled` | `setEnabled()` | 测试交互 |
| 提示文本 | `ToolTipText` | `setToolTip()` | 鼠标悬停 |
| 光标样式 | `Cursor` | `setCursor()` | 目测对比 |
| 背景色 | `BackColor` | QSS/Palette | 取色器对比 |
| 前景色 | `ForeColor` | QSS/Palette | 取色器对比 |
| 背景图 | `BackgroundImage` | QSS `background-image` | 目测对比 |
| 字体 | `Font` | `setFont()` | 对比字体渲染 |
| 文本对齐 | `TextAlign` | QSS `text-align` | 目测对比 |
| 边框样式 | `BorderStyle` | QSS `border` | 目测对比 |
| 圆角半径 | - | QSS `border-radius` | 目测对比 |
| 内边距 | `Padding` | QSS `padding` | 像素级测量 |
| 外边距 | `Margin` | Layout margins | 像素级测量 |

### 2.2 字体详细规格

**必须记录每个控件的字体规格**:

| 字体属性 | WinForms值 | Qt对应设置 | 验证方法 |
|---------|-----------|-----------|---------|
| 字体名称 | `Font.Name` | `QFont.family()` | 对比字体渲染 |
| 字体大小 | `Font.Size` | `QFont.pointSize()` | 像素级测量 |
| 字体粗细 | `Font.Bold` | `QFont.bold()` | 目测对比 |
| 字体样式 | `Font.Italic` | `QFont.italic()` | 目测对比 |
| 下划线 | `Font.Underline` | `QFont.underline()` | 目测对比 |
| 删除线 | `Font.Strikeout` | `QFont.strikeOut()` | 目测对比 |
| 字符集 | `Font.GdiCharSet` | 无对应 | 测试中文显示 |
| 像素高度 | `Font.Height` | QFontMetrics.height() | 测量字符高度 |

**记录模板**:
```markdown
### 控件: btnStart (按钮)

- 位置: (20, 20)
- 大小: 120, 35
- 字体: Microsoft YaHei, 11pt, Bold
- 文本: "启动监测"
- 文本颜色: RGB(255, 255, 255)
- 背景色: RGB(0, 122, 204)
- 边框: None
- 圆角: 4px
- 内边距: 10, 5
- Tab顺序: 1
```

### 2.3 控件特殊属性

#### Button (QPushButton)
| 属性 | WinForms | Qt | 验证 |
|-----|---------|----|-----|
| Flat样式 | `FlatStyle` | QSS `border: none` | 目测 |
| Image | `Image` | QSS `background-image` | 目测 |
| TextImageRelation | `TextImageRelation` | QSS布局 | 目测 |
| DialogResult | `DialogResult` | QDialog::done() | 测试 |

#### TextBox (QLineEdit/QTextEdit)
| 属性 | WinForms | Qt | 验证 |
|-----|---------|----|-----|
| Multiline | `Multiline` | QLineEdit→QTextEdit | 目测 |
| ScrollBars | `ScrollBars` | QScrollBar策略 | 测试 |
| PasswordChar | `PasswordChar` | QLineEdit::setEchoMode() | 测试 |
| MaxLength | `MaxLength` | QLineEdit::setMaxLength() | 测试 |
| ReadOnly | `ReadOnly` | QLineEdit::setReadOnly() | 测试 |
| Placeholder | - | QSS `placeholder-text` | 目测 |

#### ComboBox (QComboBox)
| 属性 | WinForms | Qt | 验证 |
|-----|---------|----|-----|
| DropDownStyle | `DropDownStyle` | QComboBox::setEditable() | 测试 |
| MaxDropDownItems | `MaxDropDownItems` | QComboBox::setMaxVisibleItems() | 测试 |
| AutoCompleteMode | `AutoCompleteMode` | QCompleter | 测试 |
| Sorted | `Sorted` | 排序后添加 | 测试 |

#### DataGridView (QTableView)
| 属性 | WinForms | Qt | 验证 |
|-----|---------|----|-----|
| ColumnCount | `ColumnCount` | model->columnCount() | 计数 |
| RowCount | `RowCount` | model->rowCount() | 计数 |
| AllowUserToAddRows | `AllowUserToAddRows` | QTableView::setEditTriggers() | 测试 |
| AllowUserToDeleteRows | `AllowUserToDeleteRows` | QTableView::setEditTriggers() | 测试 |
| ReadOnly | `ReadOnly` | QTableView::setEditTriggers() | 测试 |
| MultiSelect | `MultiSelect` | QTableView::setSelectionMode() | 测试 |
| SelectionMode | `SelectionMode` | QTableView::setSelectionMode() | 测试 |
| ColumnHeadersHeightSizeMode | `ColumnHeadersHeightSizeMode` | verticalHeader()->hide() | 目测 |
| RowHeadersVisible | `RowHeadersVisible` | verticalHeader()->setVisible() | 目测 |
| ColumnHeadersVisible | `ColumnHeadersVisible` | horizontalHeader()->setVisible() | 目测 |
| RowHeadersDefaultCellStyle | `RowHeadersDefaultCellStyle` | QSS设置表头样式 | 取色器 |
| ColumnHeadersDefaultCellStyle | `ColumnHeadersDefaultCellStyle` | QSS设置表头样式 | 取色器 |
| AlternatingRowsDefaultCellStyle | `AlternatingRowsDefaultCellStyle` | QSS `alternate-background-color` | 目测 |
| GridColor | `GridColor` | QSS `gridline-color` | 取色器 |
| CellBorderStyle | `CellBorderStyle` | QSS `border` | 目测 |
| RowTemplate.Height | `RowTemplate.Height` | verticalHeader()->setDefaultSectionSize() | 像素测量 |
| AutoSizeColumnsMode | `AutoSizeColumnsMode` | QTableView::horizontalHeader()->setSectionResizeMode() | 测试 |
| Columns[i].Width | `Columns[i].Width` | setColumnWidth() | 像素测量 |
| Columns[i].HeaderText | `Columns[i].HeaderText` | model->setHeaderData() | 目测 |
| Columns[i].Visible | `Columns[i].Visible` | hideColumn() | 目测 |
| Columns[i].ReadOnly | `Columns[i].ReadOnly` | setItemDelegate() | 测试 |
| Columns[i].DefaultCellStyle | `Columns[i].DefaultCellStyle` | QSS delegate | 取色器 |

#### Chart (QChart)
| 属性 | WinForms | Qt | 验证 |
|-----|---------|----|-----|
| ChartType | `ChartType` | QLineChart/QBarChart等 | 目测 |
| Series[i].Color | `Series[i].Color` | QPen::setColor() | 取色器 |
| Series[i].LineWidth | `Series[i].BorderWidth` | QPen::setWidth() | 像素测量 |
| Series[i].PointStyle | `MarkerStyle` | QScatterSeries | 目测 |
| Legend.Visible | `Legend.Visible` | chart->legend()->setVisible() | 目测 |
| Legend.Position | `Legend.Position` | chart->legend()->setAlignment() | 目测 |
| Title.Text | `Title.Text` | chart->setTitle() | 目测 |
| Title.Font | `Title.Font` | QSS `font` | 对比 |
| AxisX.Title.Text | `AxisX.Title.Text` | axisX->setTitleText() | 目测 |
| AxisX.Title.Font | `AxisX.Title.Font` | QSS | 对比 |
| AxisX.LabelStyle.Font | `AxisX.LabelStyle.Font` | QSS | 对比 |
| AxisX.MinorGrid.Enabled | `AxisX.MinorGrid.Enabled` | axisX->setMinorGridLineVisible() | 目测 |
| AxisX.MinorGrid.LineColor | `AxisX.MinorGrid.LineColor` | QPen::setColor() | 取色器 |
| AxisX.MajorGrid.Enabled | `AxisX.MajorGrid.Enabled` | axisX->setGridLineVisible() | 目测 |
| AxisX.MajorGrid.LineColor | `AxisX.MajorGrid.LineColor` | QPen::setColor() | 取色器 |
| AxisY.Title.Text | `AxisY.Title.Text` | axisY->setTitleText() | 目测 |
| AxisY.Min/Max | `AxisY.Minimum/Maximum` | axisY->setRange() | 测试数据范围 |

---

## 📋 3. 布局级别检查清单

### 3.1 容器控件布局

| 容器类型 | WinForms属性 | Qt布局 | 验证方法 |
|---------|-------------|--------|---------|
| Panel | 无布局 | QVBoxLayout/QHBoxLayout | 像素级测量 |
| GroupBox | 无布局 | QVBoxLayout/QHBoxLayout | 像素级测量 |
| TabControl | TabPage布局 | QTabWidget | 测试Tab切换 |
| SplitContainer | SplitterDistance | QSplitter | 测试拖拽 |
| FlowLayoutPanel | FlowDirection | FlowLayout(自定义) | 测试换行 |
| TableLayoutPanel | RowStyles/ColumnStyles | QGridLayout + stretches | 像素级测量 |
| ToolStrip | GripStyle | QToolBar | 目测对比 |
| StatusStrip | Spring | QStatusBar | 测试拉伸 |
| MenuStrip | MdiWindowListItem | QMenuBar | 目测对比 |

### 3.2 布局间距规范

**必须记录所有间距值**:

| 间距类型 | WinForms值 | Qt对应 | 验证方法 |
|---------|-----------|--------|---------|
| 控件间距 | `Margin` (Left, Top, Right, Bottom) | layout->setMargins() | 像素级测量 |
| 子控件间距 | `Padding` | layout->setSpacing() | 像素级测量 |
| 控件内边距 | `Padding` | QSS `padding` | 像素级测量 |
| GroupBox标题高度 | 默认 | QSS `title-height` | 像素级测量 |
| TabControl标签高度 | 默认 | QSS tab-widget::tab-bar | 像素级测量 |
| Splitter宽度 | `SplitterWidth` | QSplitter::handleWidth() | 像素级测量 |
| ToolStrip按钮间距 | 默认 | QToolBar spacing | 像素级测量 |
| StatusStrip面板间距 | Spring | QStatusBar addWidget stretch | 目测对比 |

**记录模板**:
```markdown
### 容器: panelMain (主面板)

- 布局类型: Absolute (无布局)
- 位置: (200, 50)
- 大小: 1050, 680
- 内边距: Padding(5, 5, 5, 5)
- 背景色: RGB(255, 255, 255)
- 边框: FixedSingle (RGB(200, 200, 200))

### 子控件: tableData

- 相对位置: (10, 10)
- 相对大小: 1030, 660
- 外边距: Margin(0, 0, 0, 0)
```

### 3.3 Anchor和Dock映射

**WinForms Anchor → Qt**:

| Anchor值 | Qt实现 | 示例 |
|---------|--------|-----|
| None | 无布局,绝对定位 | `widget->move(x, y)` |
| Top | Top + TopMargin | `layout->setContentsMargins(0, topMargin, 0, 0)` |
| Bottom | Bottom + BottomMargin | layout + stretch + bottomMargin |
| Left | Left + LeftMargin | `layout->setContentsMargins(leftMargin, 0, 0, 0)` |
| Right | Right + RightMargin | layout + stretch + rightMargin |
| Top+Left | Top + Left | layout + topMargin + leftMargin |
| Top+Bottom | Top + Bottom | layout + stretch + topMargin + bottomMargin |
| Left+Right | Left + Right | layout + stretch + leftMargin + rightMargin |
| All | Top+Bottom+Left+Right | layout + stretch + margins |

**WinForms Dock → Qt**:

| Dock值 | Qt实现 | 示例 |
|--------|--------|-----|
| None | 无布局,绝对定位 | `widget->move(x, y)` |
| Top | QDockWidget + DockTop | `addDockWidget(Qt::TopDockWidgetArea, dock)` |
| Bottom | QDockWidget + DockBottom | `addDockWidget(Qt::BottomDockWidgetArea, dock)` |
| Left | QDockWidget + DockLeft | `addDockWidget(Qt::LeftDockWidgetArea, dock)` |
| Right | QDockWidget + DockRight | `addDockWidget(Qt::RightDockWidgetArea, dock)` |
| Fill | 中央Widget | `setCentralWidget(widget)` |

---

## 📋 4. 交互行为检查清单

### 4.1 鼠标事件

| 事件 | WinForms | Qt | 验证方法 |
|-----|---------|----|-----|
| 点击 | Click | clicked() | 测试点击 |
| 双击 | DoubleClick | mouseDoubleClickEvent() | 测试双击 |
| 右键点击 | MouseDown(Button=Right) | contextMenuEvent() | 测试右键 |
| 悬停 | MouseEnter | enterEvent() | 目测效果 |
| 离开 | MouseLeave | leaveEvent() | 目测效果 |
| 移动 | MouseMove | mouseMoveEvent() | 测试移动 |
| 按下 | MouseDown | mousePressEvent() | 测试按下 |
| 释放 | MouseUp | mouseReleaseEvent() | 测试释放 |
| 滚轮 | MouseWheel | wheelEvent() | 测试滚轮 |
| 拖拽开始 | DragStart | dragEnterEvent() | 测试拖拽 |
| 拖拽中 | DragOver | dragMoveEvent() | 测试拖拽 |
| 拖拽结束 | DragDrop | dropEvent() | 测试放置 |

### 4.2 键盘事件

| 事件 | WinForms | Qt | 验证方法 |
|-----|---------|----|-----|
| 按键按下 | KeyDown | keyPressEvent() | 测试按键 |
| 按键释放 | KeyUp | keyReleaseEvent() | 测试释放 |
| 字符输入 | KeyPress | keyPressEvent() | 测试输入 |
| 快捷键 | Shortcut | QShortcut | 测试快捷键 |

**常用快捷键清单**:
| 快捷键 | 功能 | 实现方式 |
|--------|------|---------|
| Ctrl+S | 保存 | QShortcut(QKeySequence::Save) |
| Ctrl+O | 打开 | QShortcut(QKeySequence::Open) |
| Ctrl+N | 新建 | QShortcut(QKeySequence::New) |
| Ctrl+C | 复制 | QShortcut(QKeySequence::Copy) |
| Ctrl+V | 粘贴 | QShortcut(QKeySequence::Paste) |
| Ctrl+X | 剪切 | QShortcut(QKeySequence::Cut) |
| Ctrl+Z | 撤销 | QShortcut(QKeySequence::Undo) |
| Ctrl+Y | 重做 | QShortcut(QKeySequence::Redo) |
| Ctrl+A | 全选 | QShortcut(QKeySequence::SelectAll) |
| Delete | 删除 | QShortcut(QKeySequence::Delete) |
| F1 | 帮助 | QShortcut(QKeySequence::HelpContents) |
| F5 | 刷新 | QShortcut(Qt::Key_F5) |

### 4.3 焦点行为

| 焦点属性 | WinForms | Qt | 验证方法 |
|---------|---------|----|-----|
| 焦点获取 | GotFocus | focusInEvent() | Tab键测试 |
| 焦点丢失 | LostFocus | focusOutEvent() | Tab键测试 |
| Tab停止 | TabStop | QWidget::setFocusPolicy() | Tab键测试 |
| Tab顺序 | TabIndex | QWidget::setTabOrder() | Tab键测试 |
| 焦点可见 | - | QSS `focus` 伪类 | 目测效果 |

**记录模板**:
```markdown
### 控件: txtSearch (搜索框)

- Tab停止: True
- Tab顺序: 2
- 焦点获取事件: txtSearch_GotFocus()
- 焦点丢失事件: txtSearch_LostFocus()
- 回车事件: txtSearch_KeyDown(Key=Enter)
```

### 4.4 拖拽行为

| 拖拽属性 | WinForms | Qt | 验证方法 |
|---------|---------|----|-----|
| 允许拖拽 | AllowDrop | setAcceptDrops(true) | 测试拖拽 |
| 拖拽效果 | DragDropEffects | setDropAction() | 目测光标 |
| 拖拽数据 | DataObject | QMimeData | 测试数据 |

---

## 📋 5. 主题和样式检查清单

### 5.1 颜色体系

**必须记录所有颜色值**:

| 颜色类型 | WinForms值 | Qt实现 | 验证方法 |
|---------|-----------|--------|---------|
| 系统背景色 | SystemColors.Window | QPalette::Window | 取色器 |
| 系统文本色 | SystemColors.WindowText | QPalette::WindowText | 取色器 |
| 控件背景色 | SystemColors.Control | QPalette::Button | 取色器 |
| 控件文本色 | SystemColors.ControlText | QPalette::ButtonText | 取色器 |
| 高亮色 | SystemColors.Highlight | QPalette::Highlight | 取色器 |
| 高亮文本色 | SystemColors.HighlightText | QPalette::HighlightedText | 取色器 |
| 禁用背景色 | SystemColors.ControlDark | QPalette::Window (disabled) | 取色器 |
| 禁用文本色 | SystemColors.GrayText | QPalette::WindowText (disabled) | 取色器 |
| 边框色 | SystemColors.ControlDark | QSS border | 取色器 |
| 链接色 | SystemColors.HotTrack | QSS color | 取色器 |

**记录模板**:
```markdown
### 全局颜色定义

- 主背景色: RGB(240, 240, 240)
- 次背景色: RGB(255, 255, 255)
- 主文本色: RGB(51, 51, 51)
- 次文本色: RGB(102, 102, 102)
- 强调色: RGB(0, 122, 204)
- 成功色: RGB(52, 199, 89)
- 警告色: RGB(255, 149, 0)
- 错误色: RGB(255, 59, 48)
- 边框色: RGB(200, 200, 200)
- 分隔线色: RGB(235, 235, 235)
```

### 5.2 字体体系

| 字体类型 | WinForms默认值 | Qt推荐值 | 验证方法 |
|---------|---------------|---------|---------|
| UI字体 | Segoe UI, 9pt | Microsoft YaHei, 9pt | 对比渲染 |
| 标题字体 | Segoe UI, 12pt, Bold | Microsoft YaHei, 12pt, Bold | 对比渲染 |
| 小字体 | Segoe UI, 8pt | Microsoft YaHei, 8pt | 对比渲染 |
| 代码字体 | Consolas, 9pt | Consolas, 9pt | 对比渲染 |
| 日志字体 | Consolas, 8pt | Consolas, 8pt | 对比渲染 |

### 5.3 控件样式规范

**按钮样式**:
```css
/* WinForms默认按钮 → Qt样式表 */
QPushButton {
    background-color: rgb(240, 240, 240);
    border: 1px solid rgb(173, 173, 173);
    border-radius: 0px;
    padding: 5px 20px;
    min-height: 25px;
    font-family: "Microsoft YaHei";
    font-size: 9pt;
}

QPushButton:hover {
    background-color: rgb(230, 230, 230);
}

QPushButton:pressed {
    background-color: rgb(220, 220, 220);
}

QPushButton:disabled {
    background-color: rgb(240, 240, 240);
    color: rgb(170, 170, 170);
    border: 1px solid rgb(200, 200, 200);
}
```

**文本框样式**:
```css
QLineEdit {
    border: 1px solid rgb(173, 173, 173);
    border-radius: 0px;
    padding: 3px 5px;
    background-color: white;
    font-family: "Microsoft YaHei";
    font-size: 9pt;
}

QLineEdit:focus {
    border: 2px solid rgb(0, 122, 204);
    background-color: white;
}
```

**表格样式**:
```css
QTableView {
    background-color: white;
    alternate-background-color: rgb(245, 245, 245);
    border: 1px solid rgb(173, 173, 173);
    gridline-color: rgb(235, 235, 235);
    selection-background-color: rgb(0, 122, 204);
    selection-color: white;
    font-family: "Microsoft YaHei";
    font-size: 9pt;
}

QTableView::item {
    padding: 3px;
}

QTableView::item:selected {
    background-color: rgb(0, 122, 204);
    color: white;
}

QHeaderView::section {
    background-color: rgb(240, 240, 240);
    border: 1px solid rgb(200, 200, 200);
    padding: 3px 5px;
    font-weight: bold;
}
```

### 5.4 高DPI支持

| DPI设置 | WinForms | Qt | 验证方法 |
|---------|---------|----|-----|
| DPI感知 | SetProcessDPIAware | AA_EnableHighDpiScaling | 150% DPI测试 |
| 字体缩放 | 自动缩放 | 自动缩放 | 对比不同DPI |
| 布局缩放 | AutoScaleMode | Layout自动 | 测试缩放 |

**Qt高DPI设置**:
```cpp
// main.cpp
QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
QApplication app(argc, argv);
```

---

## 📋 6. 可折叠/隐藏UI检查清单

### 6.1 面板折叠

| 组件 | WinForms | Qt | 验证方法 |
|-----|---------|----|-----|
| GroupBox折叠 | 自定义实现 | QGroupBox::setCheckable(true) | 测试折叠 |
| Panel折叠 | Visible=false | QWidget::setVisible() | 测试隐藏 |
| Accordion | 第三方控件 | QToolBox | 测试手风琴 |
| 折叠按钮 | 自定义按钮 | 自定义实现 | 测试展开/收起 |

**Qt折叠面板实现**:
```cpp
// 方案1: QGroupBox可折叠
groupBox->setCheckable(true);
groupBox->setChecked(false);  // 折叠状态
connect(groupBox, &QGroupBox::toggled, [this](bool checked) {
    contentWidget->setVisible(checked);
});

// 方案2: 自定义折叠按钮
void MainWindow::onCollapseClicked() {
    if (contentPanel->isVisible()) {
        contentPanel->hide();
        collapseBtn->setText("▶ 展开");
    } else {
        contentPanel->show();
        collapseBtn->setText("▼ 折叠");
    }
}
```

### 6.2 动态Tab页

| 功能 | WinForms | Qt | 验证方法 |
|-----|---------|----|-----|
| 添加Tab | TabPages.Add() | addTab() | 测试添加 |
| 删除Tab | TabPages.RemoveAt() | removeTab() | 测试删除 |
| 显示/隐藏Tab | TabPage.Visible | setTabVisible() | 测试显示 |
| 禁用Tab | TabPage.Enabled | setTabEnabled() | 测试禁用 |

**Qt动态Tab实现**:
```cpp
// 添加标签页
void MainWindow::addNewTab(const QString& title) {
    QWidget* page = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(page);
    // 添加内容
    int index = tabWidget->addTab(page, title);
    tabWidget->setCurrentIndex(index);
}

// 删除标签页
void MainWindow::removeCurrentTab() {
    int index = tabWidget->currentIndex();
    if (index > 0) {  // 保留第一个Tab
        tabWidget->removeTab(index);
    }
}

// 显示/隐藏标签页 (Qt 5.15+)
void MainWindow::setTabVisible(int index, bool visible) {
    tabWidget->setTabVisible(index, visible);
}
```

### 6.3 动态菜单

| 功能 | WinForms | Qt | 验证方法 |
|-----|---------|----|-----|
| 显示/隐藏 | Visible | setVisible() | 测试显示 |
| 启用/禁用 | Enabled | setEnabled() | 测试启用 |
| 选中状态 | Checked | setChecked() | 测试选中 |
| 动态添加 | Items.Add() | addAction() | 测试添加 |

**Qt动态菜单实现**:
```cpp
// 显示/隐藏菜单项
void MainWindow::toggleAdvancedMenu(bool show) {
    actionAdvancedSettings->setVisible(show);
    actionDebugTools->setVisible(show);
}

// 根据状态启用/禁用
void MainWindow::updateMenuStates() {
    actionSave->setEnabled(hasUnsavedChanges);
    actionUndo->setEnabled(canUndo);
    actionRedo->setEnabled(canRedo);
}

// 动态添加菜单项
void MainWindow::addRecentFile(const QString& filename) {
    QAction* action = new QAction(filename, this);
    connect(action, &QAction::triggered, [this, filename]() {
        openFile(filename);
    });
    menuRecentFiles->addAction(action);
}
```

### 6.4 工具栏状态

| 功能 | WinForms | Qt | 验证方法 |
|-----|---------|----|-----|
| 显示/隐藏 | Visible | setVisible() | 测试显示 |
| 启用/禁用 | Enabled | setEnabled() | 测试启用 |
| 选中状态 | Checked | setChecked() | 测试选中 |
| 图标切换 | Image | setIcon() | 目测对比 |

**Qt工具栏状态管理**:
```cpp
// 根据选择状态启用/禁用按钮
void MainWindow::onSelectionChanged() {
    bool hasSelection = tableView->selectionModel()->hasSelection();
    actionCopy->setEnabled(hasSelection);
    actionDelete->setEnabled(hasSelection);
    actionEdit->setEnabled(hasSelection && canEdit);
}

// 显示/隐藏高级按钮
void MainWindow::toggleAdvancedTools(bool show) {
    actionAdvanced->setVisible(show);
    toolBar->setToolButtonStyle(show ? Qt::ToolButtonTextBesideIcon : Qt::ToolButtonIconOnly);
}
```

---

## 📋 7. UI功能清单模板

### 7.1 完整记录模板

```markdown
# WinForms UI功能清单

## 项目信息
- 项目名称: [项目名称]
- 窗体数量: [数量]
- 控件总数: [数量]
- 记录日期: [日期]
- 记录人员: [姓名]

---

## 窗体清单

### 窗体1: MainForm

#### 窗体属性
- 标题: ""
- 大小: 
- 最小大小: 
- 最大大小: 
- 起始位置: 
- 背景色: 
- 边框样式: 
- 图标: 

#### 控件清单

##### 控件1: btnStart (Button)
- 位置: (, )
- 大小: , 
- 文本: ""
- 字体: [名称], [大小], [粗细]
- 文本颜色: RGB(, , )
- 背景色: RGB(, , )
- 边框: [样式]
- 圆角: [px]
- 内边距: [左, 上, 右, 下]
- Tab顺序: 
- 提示文本: ""
- 点击事件: 
- 快捷键: 

##### 控件2: txtSearch (TextBox)
- 位置: (, )
- 大小: , 
- 字体: 
- 占位符: ""
- 最大长度: 
- 只读: 
- 密码模式: 
- 回车事件: 

##### 控件3: tableData (DataGridView)
- 位置: (, )
- 大小: , 
- 列数: 
- 行数: 
- 行高: 
- 选择模式: 
- 多选: 
- 表头显示: 
- 行头显示: 
- 单元格边框: 
- 网格线颜色: RGB(, , )
- 交替行颜色: RGB(, , )
- 选中背景色: RGB(, , )
- 选中文本色: RGB(, , )

##### 列定义
- 列1: ColumnName
  - 宽度: 
  - 标题: ""
  - 只读: 
  - 对齐: 
  - 默认样式: 
- 列2: ...
```

---

## 📋 8. 验证工具和方法

### 8.1 像素级测量工具

| 工具 | 用途 | 使用方法 |
|------|------|---------|
| Screen Ruler | 测量像素距离 | 拖动标尺测量 |
| PixPick | 取色器 | 点击屏幕取色 |
| Snipaste | 截图标注 | F1截图标注 |
| Windows SDK Spy++ | 查看控件信息 | Spy++窗口分析 |
| Qt Designer | 布局预览 | 打开.ui文件查看 |

### 8.2 自动化验证脚本

**Python脚本示例: PyAutoGUI截图对比**
```python
import pyautogui
from PIL import Image, ImageChops

# 截取WinForms窗口
pyautogui.screenshot('winforms.png', region=(x, y, width, height))

# 截取Qt窗口
pyautogui.screenshot('qt.png', region=(x, y, width, height))

# 对比差异
img1 = Image.open('winforms.png')
img2 = Image.open('qt.png')
diff = ImageChops.difference(img1, img2)
diff.save('difference.png')

# 计算差异百分比
diff_pixels = sum(1 for c in diff.getdata() if c != (0, 0, 0, 0))
total_pixels = img1.width * img1.height
diff_percent = (diff_pixels / total_pixels) * 100
print(f"差异百分比: {diff_percent:.2f}%")
```

### 8.3 手动验证清单

**每个窗体的验证步骤**:
1. 打开WinForms版本
2. 打开Qt版本
3. 使用Screen Ruler测量每个控件的:
   - 位置
   - 大小
   - 间距
4. 使用PixPick测量每个控件的:
   - 背景色
   - 文本色
   - 边框色
5. 对比字体渲染:
   - 字体名称
   - 字体大小
   - 粗细
   - 斜体
6. 测试交互行为:
   - 点击
   - 双击
   - 悬停
   - 拖拽
   - Tab键切换
7. 测试可折叠/隐藏功能:
   - 折叠面板
   - 动态Tab
   - 菜单项
   - 工具栏
8. 截图对比,记录差异

---

## 📋 9. 常见UI差异与修复

### 9.1 常见差异

| 差异项 | WinForms | Qt | 修复方法 |
|--------|---------|----|---------|
| 按钮圆角 | 0px | 2-4px | `border-radius: 0px` |
| 表格行高 | 23px | 21px | `setDefaultSectionSize(23)` |
| 滚动条宽度 | 17px | 16px | `setStyleSheet("width: 17px")` |
| 组框标题对齐 | 左对齐 | 居中 | `setStyleSheet("text-align: left")` |
| 下拉箭头样式 | Windows原生 | Qt原生 | QSS自定义 |
| 复选框样式 | 方形 | 方形 | 无需修改 |
| 单选按钮样式 | 圆形 | 圆形 | 无需修改 |
| 进度条样式 | Windows进度条 | Qt进度条 | QSS自定义 |
| 标签图标 | 左侧文字 | 可配置 | `setToolButtonStyle()` |

### 9.2 修复代码模板

```cpp
// main.cpp - 全局样式设置
void setupGlobalStyles() {
    // 1. 禁用圆角
    qApp->setStyleSheet("* { border-radius: 0px; }");
    
    // 2. 设置默认字体
    QFont defaultFont("Microsoft YaHei", 9);
    qApp->setFont(defaultFont);
    
    // 3. 设置表格默认行高
    qApp->setStyleSheet(
        "QTableView { "
        "  font-family: \"Microsoft YaHei\"; "
        "  font-size: 9pt; "
        "}"
    );
    
    // 4. 禁用焦点虚线
    qApp->setStyleSheet(
        "QGroupBox:focus { border: none; } "
        "QLineEdit:focus { border: none; }"
    );
    
    // 5. 设置滚动条宽度
    qApp->setStyleSheet(
        "QScrollBar:vertical { width: 17px; } "
        "QScrollBar:horizontal { height: 17px; }"
    );
}
```

---

## 📋 总结

### 迁移前必须完成:

1. ✅ **记录所有窗体属性**
   - 大小、位置、背景色、边框等

2. ✅ **记录所有控件属性**
   - 位置、大小、字体、颜色、边框等

3. ✅ **记录所有布局信息**
   - 间距、对齐方式、Anchor/Dock等

4. ✅ **记录所有交互行为**
   - 鼠标事件、键盘事件、焦点行为等

5. ✅ **记录所有颜色和字体**
   - 系统颜色、自定义颜色、字体规格等

6. ✅ **记录所有可折叠/隐藏功能**
   - 折叠面板、动态Tab、菜单项、工具栏等

7. ✅ **进行像素级测量**
   - 使用Screen Ruler、PixPick等工具

8. ✅ **建立验证清单**
   - 每个UI元素的验证标准

### 迁移后必须验证:

1. ✅ **外观一致性**
   - 像素级对比所有控件

2. ✅ **布局一致性**
   - 响应式缩放行为

3. ✅ **交互一致性**
   - 所有事件响应

4. ✅ **可折叠/隐藏功能**
   - 新增功能的隐藏/收缩

5. ✅ **字体和颜色**
   - 渲染效果一致

**只有当所有验证项都通过时,才算实现UI 100%一致!**
