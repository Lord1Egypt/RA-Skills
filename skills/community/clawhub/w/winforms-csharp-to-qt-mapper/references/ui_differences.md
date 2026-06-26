# WinForms与Qt UI差异对比详解

本文档详细对比WinForms和Qt在UI外观、行为、交互等方面的差异,并提供修复方法,确保实现100% UI一致性。

---

## 📊 1. 控件外观差异

### 1.1 Button (QPushButton vs Button)

| 属性 | WinForms默认值 | Qt默认值 | 差异 | 修复方法 |
|-----|---------------|---------|------|---------|
| 背景色 | RGB(240, 240, 240) | RGB(240, 240, 240) | 无 | - |
| 边框 | 1px solid RGB(173, 173, 173) | 1px solid RGB(173, 173, 173) | 无 | - |
| 圆角 | 0px | 2-4px | ⚠️ | `border-radius: 0px` |
| 文本对齐 | MiddleCenter | MiddleCenter | 无 | - |
| 内边距 | 5px | 根据字体计算 | ⚠️ | `padding: 5px 20px` |
| 悬停效果 | 背景色变亮 | 背景色变亮 | 无 | - |
| 按下效果 | 背景色变暗 | 背景色变暗 | 无 | - |
| 禁用状态 | 灰色 | 灰色 | 无 | - |

**Qt修复代码**:
```css
QPushButton {
    background-color: rgb(240, 240, 240);
    border: 1px solid rgb(173, 173, 173);
    border-radius: 0px;  /* 修复圆角 */
    padding: 5px 20px;   /* 修复内边距 */
    min-height: 25px;
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

---

### 1.2 TextBox (QLineEdit vs TextBox)

| 属性 | WinForms默认值 | Qt默认值 | 差异 | 修复方法 |
|-----|---------------|---------|------|---------|
| 背景色 | White | White | 无 | - |
| 边框 | Fixed3D (3D效果) | 平面边框 | ⚠️ | `border: 2px inset` |
| 内边距 | 3px | 0-1px | ⚠️ | `padding: 3px 5px` |
| 字体 | 9pt | 9pt | 无 | - |
| 焦点边框 | 无变化 | 2px蓝色 | ⚠️ | `focus { border: 2px solid ... }` |
| 禁用状态 | 灰色背景 | 灰色背景 | 无 | - |

**Qt修复代码**:
```css
QLineEdit {
    border: 2px inset rgb(173, 173, 173);
    border-radius: 0px;
    padding: 3px 5px;
    background-color: white;
    min-height: 20px;
}

QLineEdit:focus {
    border: 2px solid rgb(0, 122, 204);
    background-color: white;
}

QLineEdit:disabled {
    background-color: rgb(240, 240, 240);
    color: rgb(170, 170, 170);
    border: 1px solid rgb(200, 200, 200);
}

/* 占位符 */
QLineEdit[placeholderText=""] {
    color: rgb(170, 170, 170);
}
```

---

### 1.3 ComboBox (QComboBox vs ComboBox)

| 属性 | WinForms默认值 | Qt默认值 | 差异 | 修复方法 |
|-----|---------------|---------|------|---------|
| 背景色 | White | White | 无 | - |
| 边框 | Fixed3D | 平面边框 | ⚠️ | `border: 2px inset` |
| 下拉箭头 | Windows原生 | Qt原生 | ⚠️ | 自定义图片 |
| 下拉高度 | 106px (5项) | 动态 | ⚠️ | `setMaxVisibleItems(5)` |
| 下拉背景 | White | White | 无 | - |
| 悬停效果 | 无 | 背景色变化 | ⚠️ | 禁用hover |
| 禁用状态 | 灰色 | 灰色 | 无 | - |

**Qt修复代码**:
```css
QComboBox {
    border: 2px inset rgb(173, 173, 173);
    border-radius: 0px;
    padding: 3px 20px 3px 5px;  /* 右侧留箭头空间 */
    background-color: white;
    min-width: 100px;
}

QComboBox:hover {
    border: 2px inset rgb(173, 173, 173);  /* 禁用hover效果 */
}

QComboBox:drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: url(:/icons/combobox-arrow.png);  /* 自定义箭头 */
}

QComboBox QAbstractItemView {
    border: 1px solid rgb(173, 173, 173);
    background-color: white;
    selection-background-color: rgb(0, 122, 204);
    selection-color: white;
}
```

**Qt代码设置**:
```cpp
// 设置下拉最大项数
comboBox->setMaxVisibleItems(5);

// 设置下拉宽度
comboBox->view()->setMinimumWidth(comboBox->width());
```

---

### 1.4 DataGridView (QTableView vs DataGridView)

| 属性 | WinForms默认值 | Qt默认值 | 差异 | 修复方法 |
|-----|---------------|---------|------|---------|
| 行高 | 默认21px | 根据字体动态 | ⚠️ | `setDefaultSectionSize(21)` |
| 列头高度 | 默认21px | 根据字体动态 | ⚠️ | `setFixedHeight(21)` |
| 边框 | CellBorderStyle | 网格线 | ⚠️ | `gridline-color` |
| 网格线颜色 | RGB(200, 200, 200) | RGB(200, 200, 200) | 无 | - |
| 选中背景 | RGB(51, 153, 255) | RGB(51, 153, 255) | 无 | - |
| 交替行颜色 | 可选 | 无 | ⚠️ | `alternate-background-color` |
| 表头样式 | 3D边框 | 平面边框 | ⚠️ | QSS自定义 |
| 行头显示 | 可选 | 显示 | ⚠️ | `hide()` |
| 选择模式 | FullRowSelect | SingleSelection | ⚠️ | `setSelectionMode()` |

**Qt修复代码**:
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
    border: none;
}

QTableView::item:selected {
    background-color: rgb(0, 122, 204);
    color: white;
}

QTableView::item:hover {
    background-color: rgb(230, 240, 255);  /* 悬停效果 */
}

QHeaderView::section {
    background-color: rgb(240, 240, 240);
    border: 1px solid rgb(200, 200, 200);
    padding: 3px 5px;
    font-weight: bold;
    text-align: left;
}

QHeaderView::section:hover {
    background-color: rgb(230, 230, 230);  /* 表头悬停 */
}

QScrollBar:vertical {
    border: none;
    background: white;
    width: 17px;
}

QScrollBar::handle:vertical {
    background: rgb(200, 200, 200);
    min-height: 20px;
}
```

**Qt代码设置**:
```cpp
// 设置行高
tableView->verticalHeader()->setDefaultSectionSize(21);
tableView->verticalHeader()->setMinimumSectionSize(21);

// 设置列头高度
tableView->horizontalHeader()->setFixedHeight(21);

// 隐藏行头
tableView->verticalHeader()->hide();

// 设置选择模式(整行选择)
tableView->setSelectionBehavior(QAbstractItemView::SelectRows);
tableView->setSelectionMode(QAbstractItemView::SingleSelection);

// 设置列宽
tableView->setColumnWidth(0, 100);
tableView->horizontalHeader()->setStretchLastSection(true);
```

---

### 1.5 Chart (QChart vs Chart)

| 属性 | WinForms默认值 | Qt默认值 | 差异 | 修复方法 |
|-----|---------------|---------|------|---------|
| 图表类型 | Line, Bar等 | QLineChart等 | 对应 | 正确选择Chart类型 |
| 坐标轴颜色 | RGB(128, 128, 128) | RGB(128, 128, 128) | 无 | - |
| 坐标轴字体 | 8pt | 8pt | 无 | - |
| 图例位置 | Top, Bottom等 | Top, Bottom等 | 对应 | `setAlignment()` |
| 图例显示 | True | True | 无 | - |
| 标题字体 | 12pt Bold | 12pt Bold | 无 | - |
| 数据点样式 | Circle | Circle | 无 | - |
| 网格线 | 可选 | 可选 | 对应 | `setGridLineVisible()` |
| 动画 | 无 | 平滑动画 | ⚠️ | `setAnimationOptions(NoAnimation)` |

**Qt修复代码**:
```cpp
// 创建图表
QChart* chart = new QChart();

// 添加序列
QLineSeries* series = new QLineSeries();
series->setColor(QColor(0, 122, 204));
series->setPointsVisible(true);
series->setPointLabelsVisible(false);
chart->addSeries(series);

// 设置坐标轴
QValueAxis* axisX = new QValueAxis();
axisX->setTitleText("时间");
axisX->setLabelsFont(QFont("Microsoft YaHei", 8));
axisX->setGridLineVisible(true);
axisX->setGridLineColor(QColor(235, 235, 235));
axisX->setMinorGridLineVisible(false);
chart->addAxis(axisX, Qt::AlignBottom);
series->attachAxis(axisX);

QValueAxis* axisY = new QValueAxis();
axisY->setTitleText("数值");
axisY->setLabelsFont(QFont("Microsoft YaHei", 8));
axisY->setGridLineVisible(true);
axisY->setGridLineColor(QColor(235, 235, 235));
axisY->setMinorGridLineVisible(false);
chart->addAxis(axisY, Qt::AlignLeft);
series->attachAxis(axisY);

// 设置图例
chart->legend()->setVisible(true);
chart->legend()->setAlignment(Qt::AlignTop);

// 设置标题
chart->setTitle("数据趋势");
QFont titleFont("Microsoft YaHei", 12, QFont::Bold);
chart->setTitleFont(titleFont);

// 禁用动画(与WinForms一致)
chart->setAnimationOptions(QChart::NoAnimation);

// 设置图表视图
QChartView* chartView = new QChartView(chart);
chartView->setRenderHint(QPainter::Antialiasing);
chartView->setRubberBand(QChartView::RectangleRubberBand);
```

---

## 📊 2. 布局差异

### 2.1 Anchor vs Layout

| Anchor设置 | Qt对应实现 | 差异 | 修复方法 |
|-----------|-----------|------|---------|
| Anchor=None | 绝对定位 `move()` | 完全相同 | 无需修复 |
| Anchor=Top | QVBoxLayout + TopMargin | 实现不同 | `layout->setContentsMargins(0, margin, 0, 0)` |
| Anchor=Bottom | QVBoxLayout + BottomMargin | 实现不同 | `layout->addStretch()` |
| Anchor=Left | QHBoxLayout + LeftMargin | 实现不同 | `layout->setContentsMargins(margin, 0, 0, 0)` |
| Anchor=Right | QHBoxLayout + RightMargin | 实现不同 | `layout->addStretch()` |
| Anchor=Top+Left | 两个方向的Margin | 实现不同 | `layout->setContentsMargins(left, top, 0, 0)` |
| Anchor=Top+Bottom | 上下固定中间伸缩 | 实现不同 | `layout->setStretch(1)` |
| Anchor=Left+Right | 左右固定中间伸缩 | 实现不同 | `layout->setStretch(1)` |
| Anchor=All | 四周固定中间伸缩 | 实现不同 | `layout->setStretch(1)`

**Qt代码实现**:
```cpp
// Anchor=Top
QWidget* topPanel = new QWidget();
QVBoxLayout* layout = new QVBoxLayout(topPanel);
layout->setContentsMargins(0, 10, 0, 0);  // 顶部10px margin

// Anchor=Bottom
QWidget* bottomPanel = new QWidget();
QVBoxLayout* layout = new QVBoxLayout(bottomPanel);
layout->setContentsMargins(0, 0, 0, 10);  // 底部10px margin
layout->addStretch();  // 底部对齐

// Anchor=Top+Bottom (上下固定,中间伸缩)
QWidget* middlePanel = new QWidget();
QVBoxLayout* layout = new QVBoxLayout(middlePanel);
layout->setContentsMargins(0, 10, 0, 10);
layout->addWidget(topWidget);
layout->addStretch();  // 中间可伸缩
layout->addWidget(bottomWidget);

// Anchor=Left
QWidget* leftPanel = new QWidget();
QHBoxLayout* layout = new QHBoxLayout(leftPanel);
layout->setContentsMargins(10, 0, 0, 0);

// Anchor=Right
QWidget* rightPanel = new QWidget();
QHBoxLayout* layout = new QHBoxLayout(rightPanel);
layout->setContentsMargins(0, 0, 10, 0);
layout->addStretch();  // 右侧对齐

// Anchor=Left+Right (左右固定,中间伸缩)
QWidget* centerPanel = new QWidget();
QHBoxLayout* layout = new QHBoxLayout(centerPanel);
layout->setContentsMargins(10, 0, 10, 0);
layout->addWidget(leftWidget);
layout->addStretch();  // 中间可伸缩
layout->addWidget(rightWidget);
```

---

### 2.2 Dock vs QDockWidget

| Dock设置 | Qt对应实现 | 差异 | 修复方法 |
|---------|-----------|------|---------|
| Dock=None | 绝对定位 | 完全相同 | - |
| Dock=Top | QDockWidget(Qt::TopDockWidgetArea) | 完全相同 | - |
| Dock=Bottom | QDockWidget(Qt::BottomDockWidgetArea) | 完全相同 | - |
| Dock=Left | QDockWidget(Qt::LeftDockWidgetArea) | 完全相同 | - |
| Dock=Right | QDockWidget(Qt::RightDockWidgetArea) | 完全相同 | - |
| Dock=Fill | setCentralWidget() | 完全相同 | - |

**Qt代码实现**:
```cpp
// 创建Dock Widget
QDockWidget* dockLeft = new QDockWidget("左侧面板", this);
dockLeft->setAllowedAreas(Qt::LeftDockWidgetArea | Qt::RightDockWidgetArea);
dockLeft->setFeatures(QDockWidget::DockWidgetMovable | QDockWidget::DockWidgetFloatable);

// 添加内容
QWidget* leftContent = new QWidget();
QVBoxLayout* layout = new QVBoxLayout(leftContent);
// ... 添加控件
dockLeft->setWidget(leftContent);

// 添加到主窗口
addDockWidget(Qt::LeftDockWidgetArea, dockLeft);

// 设置中央Widget
QWidget* centralWidget = new QWidget();
QVBoxLayout* centralLayout = new QVBoxLayout(centralWidget);
// ... 添加控件
setCentralWidget(centralWidget);

// Dock宽度固定
dockLeft->setMaximumWidth(200);
dockLeft->setMinimumWidth(150);
```

---

### 2.3 FlowLayoutPanel vs 自定义FlowLayout

| 属性 | WinForms | Qt | 差异 | 修复方法 |
|-----|---------|----|------|---------|
| 自动换行 | 是 | 否 | ⚠️ | 自定义FlowLayout |
| FlowDirection | LeftToRight | 无对应 | ⚠️ | 自定义 |
| 控件顺序 | 添加顺序 | 添加顺序 | 相同 | - |
| 间距 | Margin | layout spacing | 对应 | `setSpacing()` |

**Qt FlowLayout实现**:
```cpp
// flowlayout.h
class FlowLayout : public QLayout {
public:
    explicit FlowLayout(QWidget* parent, int margin = -1, int hSpacing = -1, int vSpacing = -1);
    explicit FlowLayout(int margin = -1, int hSpacing = -1, int vSpacing = -1);
    ~FlowLayout();

    void addItem(QLayoutItem* item) override;
    int horizontalSpacing() const;
    int verticalSpacing() const;
    Qt::Orientations expandingDirections() const override;
    bool hasHeightForWidth() const override;
    int heightForWidth(int) const override;
    int count() const override;
    QLayoutItem* itemAt(int index) const override;
    QLayoutItem* takeAt(int index) override;
    void setGeometry(const QRect& rect) override;
    QSize sizeHint() const override;

private:
    int doLayout(const QRect& rect, bool testOnly) const;
    int smartSpacing(QStyle::PixelMetric pm) const;

    QList<QLayoutItem*> itemList;
    int m_hSpace;
    int m_vSpace;
};

// flowlayout.cpp
FlowLayout::FlowLayout(QWidget* parent, int margin, int hSpacing, int vSpacing)
    : QLayout(parent), m_hSpace(hSpacing), m_vSpace(vSpacing) {
    setContentsMargins(margin, margin, margin, margin);
}

FlowLayout::FlowLayout(int margin, int hSpacing, int vSpacing)
    : m_hSpace(hSpacing), m_vSpace(vSpacing) {
    setContentsMargins(margin, margin, margin, margin);
}

FlowLayout::~FlowLayout() {
    QLayoutItem* item;
    while ((item = takeAt(0))) {
        delete item;
    }
}

void FlowLayout::addItem(QLayoutItem* item) {
    itemList.append(item);
}

int FlowLayout::horizontalSpacing() const {
    if (m_hSpace >= 0) {
        return m_hSpace;
    } else {
        return smartSpacing(QStyle::PM_LayoutHorizontalSpacing);
    }
}

int FlowLayout::verticalSpacing() const {
    if (m_vSpace >= 0) {
        return m_vSpace;
    } else {
        return smartSpacing(QStyle::PM_LayoutVerticalSpacing);
    }
}

int FlowLayout::count() const {
    return itemList.size();
}

QLayoutItem* FlowLayout::itemAt(int index) const {
    return itemList.value(index);
}

QLayoutItem* FlowLayout::takeAt(int index) {
    if (index >= 0 && index < itemList.size()) {
        return itemList.takeAt(index);
    } else {
        return 0;
    }
}

Qt::Orientations FlowLayout::expandingDirections() const {
    return Qt::Orientations();
}

bool FlowLayout::hasHeightForWidth() const {
    return true;
}

int FlowLayout::heightForWidth(int width) const {
    int height = doLayout(QRect(0, 0, width, 0), true);
    return height;
}

void FlowLayout::setGeometry(const QRect& rect) {
    QLayout::setGeometry(rect);
    doLayout(rect, false);
}

QSize FlowLayout::sizeHint() const {
    return minimumSize();
}

int FlowLayout::doLayout(const QRect& rect, bool testOnly) const {
    int left, top, right, bottom;
    getContentsMargins(&left, &top, &right, &bottom);
    QRect effectiveRect = rect.adjusted(+left, +top, -right, -bottom);
    int x = effectiveRect.x();
    int y = effectiveRect.y();
    int lineHeight = 0;

    for (QLayoutItem* item : itemList) {
        QWidget* wid = item->widget();
        int spaceX = horizontalSpacing();
        if (spaceX == -1) {
            spaceX = wid->style()->layoutSpacing(
                QSizePolicy::PushButton, QSizePolicy::PushButton, Qt::Horizontal);
        }
        int spaceY = verticalSpacing();
        if (spaceY == -1) {
            spaceY = wid->style()->layoutSpacing(
                QSizePolicy::PushButton, QSizePolicy::PushButton, Qt::Vertical);
        }

        int nextX = x + item->sizeHint().width() + spaceX;
        if (nextX - spaceX > effectiveRect.right() && lineHeight > 0) {
            x = effectiveRect.x();
            y = y + lineHeight + spaceY;
            nextX = x + item->sizeHint().width() + spaceX;
            lineHeight = 0;
        }

        if (!testOnly) {
            item->setGeometry(QRect(QPoint(x, y), item->sizeHint()));
        }

        x = nextX;
        lineHeight = qMax(lineHeight, item->sizeHint().height());
    }

    return y + lineHeight - rect.y() + bottom;
}

int FlowLayout::smartSpacing(QStyle::PixelMetric pm) const {
    QObject* parent = this->parent();
    if (!parent) {
        return -1;
    } else if (parent->isWidgetType()) {
        QWidget* pw = static_cast<QWidget*>(parent);
        return pw->style()->pixelMetric(pm, nullptr, pw);
    } else {
        return static_cast<QLayout*>(parent)->spacing();
    }
}
```

---

## 📊 3. 字体差异

### 3.1 默认字体对比

| 字体类型 | WinForms默认值 | Qt默认值 | 差异 | 修复方法 |
|---------|---------------|---------|------|---------|
| UI字体 | Segoe UI, 9pt | 根据系统 | ⚠️ | 显式设置字体 |
| 标题字体 | Segoe UI, 12pt, Bold | 根据系统 | ⚠️ | 显式设置字体 |
| 小字体 | Segoe UI, 8pt | 根据系统 | ⚠️ | 显式设置字体 |
| 代码字体 | Consolas, 9pt | Monospace | ⚠️ | 显式设置字体 |

**Qt全局字体设置**:
```cpp
// main.cpp
int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    
    // 设置全局字体(与WinForms Segoe UI对应)
    QFont defaultFont("Microsoft YaHei", 9);
    app.setFont(defaultFont);
    
    // 设置标题字体
    QFont titleFont("Microsoft YaHei", 12);
    titleFont.setBold(true);
    
    // 设置代码字体
    QFont codeFont("Consolas", 9);
    
    MainWindow window;
    window.show();
    return app.exec();
}
```

**Qt QSS字体设置**:
```css
/* 全局字体 */
* {
    font-family: "Microsoft YaHei";
    font-size: 9pt;
}

/* 标题字体 */
QLabel#title {
    font-family: "Microsoft YaHei";
    font-size: 12pt;
    font-weight: bold;
}

/* 代码字体 */
QTextEdit#code {
    font-family: "Consolas";
    font-size: 9pt;
}
```

---

### 3.2 字体渲染差异

| 渲染属性 | WinForms | Qt | 差异 | 修复方法 |
|---------|---------|----|------|---------|
| 抗锯齿 | ClearType | 根据系统 | ⚠️ | `QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps)` |
| 字体粗细 | Bold/Normal | Bold/Normal | 相同 | - |
| 斜体 | Italic | Italic | 相同 | - |
| 下划线 | Underline | Underline | 相同 | - |
| 删除线 | Strikeout | Strikeout | 相同 | - |
| 字符间距 | 无 | LetterSpacing | ⚠️ | `setLetterSpacing()` |
| 行间距 | 单行 | LineSpacing | ⚠️ | QSS `line-height` |

**Qt抗锯齿设置**:
```cpp
// main.cpp
QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
```

---

## 📊 4. 颜色差异

### 4.1 系统颜色对比

| 颜色类型 | WinForms | Qt | 差异 | 修复方法 |
|---------|---------|----|------|---------|
| 窗口背景 | SystemColors.Window | QPalette::Window | ⚠️ | RGB(240, 240, 240) |
| 窗口文本 | SystemColors.WindowText | QPalette::WindowText | ⚠️ | RGB(0, 0, 0) |
| 控件背景 | SystemColors.Control | QPalette::Button | ⚠️ | RGB(240, 240, 240) |
| 控件文本 | SystemColors.ControlText | QPalette::ButtonText | ⚠️ | RGB(0, 0, 0) |
| 高亮色 | SystemColors.Highlight | QPalette::Highlight | ⚠️ | RGB(0, 122, 204) |
| 高亮文本 | SystemColors.HighlightText | QPalette::HighlightedText | ⚠️ | RGB(255, 255, 255) |
| 禁用文本 | SystemColors.GrayText | QPalette::WindowText(disabled) | ⚠️ | RGB(109, 109, 109) |
| 边框色 | SystemColors.ControlDark | 无对应 | ⚠️ | RGB(173, 173, 173) |
| 链接色 | SystemColors.HotTrack | 无对应 | ⚠️ | RGB(0, 102, 204) |

**Qt QSS颜色设置**:
```css
/* 全局颜色定义 */
:root {
    --window-bg: rgb(240, 240, 240);
    --window-text: rgb(0, 0, 0);
    --control-bg: rgb(240, 240, 240);
    --control-text: rgb(0, 0, 0);
    --highlight-bg: rgb(0, 122, 204);
    --highlight-text: rgb(255, 255, 255);
    --disabled-text: rgb(109, 109, 109);
    --border-color: rgb(173, 173, 173);
    --link-color: rgb(0, 102, 204);
}

/* 应用颜色 */
QWidget {
    background-color: var(--window-bg);
    color: var(--window-text);
}

QPushButton {
    background-color: var(--control-bg);
    color: var(--control-text);
    border: 1px solid var(--border-color);
}

QPushButton:hover {
    background-color: rgb(230, 230, 230);
}

QPushButton:pressed {
    background-color: rgb(220, 220, 220);
}

QPushButton:disabled {
    color: var(--disabled-text);
}

QLabel#link {
    color: var(--link-color);
    text-decoration: underline;
}
```

---

## 📊 5. 交互差异

### 5.1 鼠标事件

| 事件 | WinForms | Qt | 差异 | 修复方法 |
|-----|---------|----|------|---------|
| Click | Click | clicked() | 相同 | - |
| DoubleClick | DoubleClick | mouseDoubleClickEvent() | ⚠️ | Qt也会触发两次Click |
| MouseEnter | MouseEnter | enterEvent() | 相同 | - |
| MouseLeave | MouseLeave | leaveEvent() | 相同 | - |
| MouseDown | MouseDown | mousePressEvent() | 相同 | - |
| MouseUp | MouseUp | mouseReleaseEvent() | 相同 | - |
| MouseMove | MouseMove | mouseMoveEvent() | ⚠️ | Qt需要`setMouseTracking(true)` |
| MouseHover | MouseHover | 无对应 | ⚠️ | 需要自己实现 |

**Qt鼠标事件实现**:
```cpp
// 启用鼠标跟踪(连续鼠标移动事件)
widget->setMouseTracking(true);

// 重写鼠标事件
void MyWidget::mousePressEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        // 左键按下
    }
    QWidget::mousePressEvent(event);
}

void MyWidget::mouseDoubleClickEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        // 双击处理
    }
    QWidget::mouseDoubleClickEvent(event);
}

void MyWidget::enterEvent(QEvent* event) {
    // 鼠标进入
    QWidget::enterEvent(event);
}

void MyWidget::leaveEvent(QEvent* event) {
    // 鼠标离开
    QWidget::leaveEvent(event);
}
```

---

### 5.2 键盘事件

| 事件 | WinForms | Qt | 差异 | 修复方法 |
|-----|---------|----|------|---------|
| KeyDown | KeyDown | keyPressEvent() | 相同 | - |
| KeyUp | KeyUp | keyReleaseEvent() | 相同 | - |
| KeyPress | KeyPress | keyPressEvent() | 相同 | - |
| PreviewKeyDown | PreviewKeyDown | 无对应 | ⚠️ | 事件过滤器 |
| 快捷键 | ProcessCmdKey | QShortcut | 对应 | QShortcut |

**Qt键盘事件实现**:
```cpp
// 快捷键
QShortcut* shortcutSave = new QShortcut(QKeySequence::Save, this);
connect(shortcutSave, &QShortcut::activated, this, &MainWindow::onSave);

// 重写键盘事件
void MyWidget::keyPressEvent(QKeyEvent* event) {
    switch (event->key()) {
        case Qt::Key_Return:
            // 回车键
            break;
        case Qt::Key_Escape:
            // ESC键
            break;
        case Qt::Key_Delete:
            // 删除键
            break;
    }
    QWidget::keyPressEvent(event);
}

// 事件过滤器(PreviewKeyDown)
bool MyWidget::eventFilter(QObject* obj, QEvent* event) {
    if (event->type() == QEvent::KeyPress) {
        QKeyEvent* keyEvent = static_cast<QKeyEvent*>(event);
        if (keyEvent->key() == Qt::Key_Enter) {
            // 预处理回车键
            return true;  // 事件已处理
        }
    }
    return QObject::eventFilter(obj, event);
}

// 安装事件过滤器
lineEdit->installEventFilter(this);
```

---

## 📊 6. 滚动条差异

| 属性 | WinForms | Qt | 差异 | 修复方法 |
|-----|---------|----|------|---------|
| 滚动条宽度 | 17px | 16px (Win) / 15px (Mac) | ⚠️ | `setStyleSheet("width: 17px")` |
| 滚动条样式 | Windows原生 | Qt原生 | ⚠️ | QSS自定义 |
| 滚动步长 | SystemInformation.VerticalScrollBarWidth | 40px | ⚠️ | `setPageStep()` |
| 滚动速度 | 3行 | 3行 | 相同 | - |
| 滚动箭头 | Windows原生 | Qt原生 | ⚠️ | QSS自定义 |

**Qt滚动条QSS**:
```css
/* 垂直滚动条 */
QScrollBar:vertical {
    border: none;
    background: white;
    width: 17px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:vertical {
    background: rgb(200, 200, 200);
    min-height: 20px;
}

QScrollBar::add-line:vertical {
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    height: 0px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

/* 水平滚动条 */
QScrollBar:horizontal {
    border: none;
    background: white;
    height: 17px;
    margin: 0px 0px 0px 0px;
}

QScrollBar::handle:horizontal {
    background: rgb(200, 200, 200);
    min-width: 20px;
}

QScrollBar::add-line:horizontal {
    width: 0px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    width: 0px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
```

**Qt滚动条代码设置**:
```cpp
// 设置滚动步长
scrollArea->verticalScrollBar()->setSingleStep(20);   // 单步滚动20px
scrollArea->verticalScrollBar()->setPageStep(100);   // 页面滚动100px

// 滚动到指定位置
scrollArea->verticalScrollBar()->setValue(0);

// 获取滚动位置
int position = scrollArea->verticalScrollBar()->value();
```

---

## 📊 7. 高DPI支持差异

| DPI设置 | WinForms | Qt | 差异 | 修复方法 |
|---------|---------|----|------|---------|
| DPI感知 | SetProcessDPIAware | AA_EnableHighDpiScaling | 对应 | 设置属性 |
| 字体缩放 | 自动缩放 | 自动缩放 | 相同 | - |
| 布局缩放 | AutoScaleMode | Layout自动 | 相同 | - |
| 图片缩放 | 自动 | 需要 | ⚠️ | `AA_UseHighDpiPixmaps` |

**Qt高DPI设置**:
```cpp
// main.cpp
// 设置高DPI支持(必须在QApplication构造前)
QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
QApplication::setAttribute(Qt::AA_DisableWindowContextHelpButton);

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    
    // 设置DPI缩放比例(可选)
    qputenv("QT_AUTO_SCREEN_SCALE_FACTOR", "1");
    qputenv("QT_SCALE_FACTOR", "1.5");  // 150% DPI
    
    MainWindow window;
    window.show();
    return app.exec();
}
```

---

## 📊 8. 常见差异修复清单

### 必须修复的差异:

| 序号 | 差异项 | WinForms值 | Qt默认值 | 修复方法 |
|-----|--------|-----------|---------|---------|
| 1 | 按钮圆角 | 0px | 2-4px | `border-radius: 0px` |
| 2 | 表格行高 | 21px | 21px (动态) | `setDefaultSectionSize(21)` |
| 3 | 表格列头高度 | 21px | 21px (动态) | `setFixedHeight(21)` |
| 4 | 滚动条宽度 | 17px | 16px | `setStyleSheet("width: 17px")` |
| 5 | 组框标题对齐 | 左对齐 | 居中 | `setStyleSheet("text-align: left")` |
| 6 | 文本框内边距 | 3px | 0-1px | `padding: 3px 5px` |
| 7 | 下拉箭头样式 | Windows原生 | Qt原生 | 自定义图片 |
| 8 | 下拉高度 | 106px (5项) | 动态 | `setMaxVisibleItems(5)` |
| 9 | 链接颜色 | RGB(0, 102, 204) | 蓝色 | `color: rgb(0, 102, 204)` |
| 10 | 高亮颜色 | RGB(51, 153, 255) | 蓝色 | `selection-background-color: rgb(0, 122, 204)` |
| 11 | 禁用文本色 | RGB(109, 109, 109) | 灰色 | `color: rgb(109, 109, 109)` |
| 12 | 边框颜色 | RGB(173, 173, 173) | 灰色 | `border: 1px solid rgb(173, 173, 173)` |
| 13 | 字体 | Segoe UI, 9pt | 系统默认 | `QFont("Microsoft YaHei", 9)` |
| 14 | 标题字体 | Segoe UI, 12pt, Bold | 系统默认 | `QFont("Microsoft YaHei", 12, QFont::Bold)` |
| 15 | 窗口背景 | RGB(240, 240, 240) | 白色 | `background-color: rgb(240, 240, 240)` |
| 16 | 控件背景 | RGB(240, 240, 240) | 灰色 | `background-color: rgb(240, 240, 240)` |
| 17 | 网格线颜色 | RGB(235, 235, 235) | 灰色 | `gridline-color: rgb(235, 235, 235)` |
| 18 | 交替行颜色 | RGB(245, 245, 245) | 无 | `alternate-background-color: rgb(245, 245, 245)` |
| 19 | 鼠标跟踪 | 自动 | 禁用 | `setMouseTracking(true)` |
| 20 | 双击事件 | 单独事件 | 触发两次Click | 区分处理 |

---

## 📊 9. 完整修复代码模板

### main.cpp - 全局设置

```cpp
#include <QApplication>
#include "MainWindow.h"

int main(int argc, char* argv[]) {
    // 高DPI支持
    QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
    
    // 禁用上下文帮助按钮
    QApplication::setAttribute(Qt::AA_DisableWindowContextHelpButton);
    
    QApplication app(argc, argv);
    
    // 设置全局字体
    QFont defaultFont("Microsoft YaHei", 9);
    app.setFont(defaultFont);
    
    // 设置全局样式
    app.setStyleSheet(R"(
        /* 全局样式 */
        * {
            font-family: "Microsoft YaHei";
            font-size: 9pt;
            border-radius: 0px;  /* 禁用圆角 */
        }
        
        QWidget {
            background-color: rgb(240, 240, 240);
            color: rgb(0, 0, 0);
        }
        
        QPushButton {
            background-color: rgb(240, 240, 240);
            border: 1px solid rgb(173, 173, 173);
            padding: 5px 20px;
            min-height: 25px;
        }
        
        QPushButton:hover {
            background-color: rgb(230, 230, 230);
        }
        
        QPushButton:pressed {
            background-color: rgb(220, 220, 220);
        }
        
        QPushButton:disabled {
            color: rgb(109, 109, 109);
        }
        
        QLineEdit {
            border: 2px inset rgb(173, 173, 173);
            padding: 3px 5px;
            background-color: white;
            min-height: 20px;
        }
        
        QLineEdit:focus {
            border: 2px solid rgb(0, 122, 204);
        }
        
        QTableView {
            background-color: white;
            alternate-background-color: rgb(245, 245, 245);
            border: 1px solid rgb(173, 173, 173);
            gridline-color: rgb(235, 235, 235);
            selection-background-color: rgb(0, 122, 204);
            selection-color: white;
        }
        
        QTableView::item {
            padding: 3px;
        }
        
        QHeaderView::section {
            background-color: rgb(240, 240, 240);
            border: 1px solid rgb(200, 200, 200);
            padding: 3px 5px;
            font-weight: bold;
        }
        
        QScrollBar:vertical {
            width: 17px;
        }
        
        QScrollBar:horizontal {
            height: 17px;
        }
    )");
    
    MainWindow window;
    window.show();
    return app.exec();
}
```

---

## 📊 总结

### 关键差异总结

1. **控件外观**: 圆角、内边距、边框样式需要修复
2. **布局系统**: Anchor需要转换为Layout,需要自定义FlowLayout
3. **字体设置**: 需要显式设置字体,否则使用系统默认
4. **颜色体系**: 需要手动设置颜色,不能依赖系统调色板
5. **交互行为**: 鼠标跟踪、双击事件需要特殊处理
6. **滚动条**: 宽度、样式需要QSS自定义
7. **高DPI**: 需要启用高DPI支持属性

### 验证方法

1. **像素级测量**: 使用Screen Ruler测量所有控件的尺寸和间距
2. **颜色对比**: 使用PixPick对比所有控件的背景色、文本色、边框色
3. **字体对比**: 目测对比字体渲染效果
4. **交互测试**: 测试所有鼠标和键盘事件
5. **缩放测试**: 测试不同DPI下的显示效果

### 只有修复所有差异,才能实现100% UI一致!
