# 可折叠/隐藏UI组件实现指南

Qt实现可折叠和隐藏UI组件的完整指南,包括面板折叠、标签页管理、菜单控制、工具栏状态等,确保与WinForms行为100%一致。

---

## 📋 1. 面板折叠实现

### 1.1 QGroupBox可折叠(推荐)

**适用场景**: 标题栏可点击折叠的面板

**WinForms实现**:
```csharp
// 使用Panel + Button + Label组合实现
panelContent.Visible = false;
btnCollapse.Text = "▶ 展开";
```

**Qt实现**:

```cpp
// mainwindow.h
class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget* parent = nullptr);
    
private:
    QGroupBox* createCollapsibleGroupBox(const QString& title, QWidget* content);
    
    QGroupBox* m_groupBoxSettings;
    QWidget* m_contentSettings;
};

// mainwindow.cpp
MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
    // 创建可折叠面板
    m_groupBoxSettings = createCollapsibleGroupBox("高级设置", createSettingsContent());
    
    // 默认展开
    m_groupBoxSettings->setChecked(true);
    m_contentSettings->setVisible(true);
    
    // 添加到主布局
    QVBoxLayout* mainLayout = new QVBoxLayout(centralWidget());
    mainLayout->addWidget(m_groupBoxSettings);
}

QGroupBox* MainWindow::createCollapsibleGroupBox(const QString& title, QWidget* content) {
    QGroupBox* groupBox = new QGroupBox(title);
    groupBox->setCheckable(true);  // 启用可折叠
    groupBox->setChecked(true);    // 默认展开
    
    QVBoxLayout* layout = new QVBoxLayout(groupBox);
    layout->setContentsMargins(10, 10, 10, 10);
    layout->setSpacing(0);
    
    // 保存content指针
    m_contentSettings = content;
    content->setVisible(true);
    layout->addWidget(content);
    
    // 连接折叠信号
    connect(groupBox, &QGroupBox::toggled, this, [this](bool checked) {
        m_contentSettings->setVisible(checked);
        // 调整窗口大小
        resize(sizeHint());
    });
    
    return groupBox;
}

QWidget* MainWindow::createSettingsContent() {
    QWidget* widget = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(widget);
    
    // 添加内容
    QCheckBox* check1 = new QCheckBox("启用日志记录");
    QCheckBox* check2 = new QCheckBox("自动保存");
    QSpinBox* spinLog = new QSpinBox();
    spinLog->setRange(1, 365);
    spinLog->setSuffix(" 天");
    
    layout->addWidget(check1);
    layout->addWidget(check2);
    layout->addWidget(new QLabel("日志保留天数:"));
    layout->addWidget(spinLog);
    layout->addStretch();
    
    return widget;
}
```

**样式优化**:
```css
QGroupBox {
    font-weight: bold;
    border: 1px solid rgb(173, 173, 173);
    border-radius: 0px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
}

QGroupBox::indicator {
    width: 16px;
    height: 16px;
}

QGroupBox::indicator:checked {
    image: url(:/icons/expand.png);
}

QGroupBox::indicator:unchecked {
    image: url(:/icons/collapse.png);
}
```

---

### 1.2 自定义折叠按钮

**适用场景**: 需要完全控制折叠按钮样式和位置

**Qt实现**:

```cpp
// collapsiblepanel.h
class CollapsiblePanel : public QWidget {
    Q_OBJECT
public:
    explicit CollapsiblePanel(const QString& title, QWidget* parent = nullptr);
    void setContentWidget(QWidget* content);
    void setExpanded(bool expanded);
    bool isExpanded() const { return m_expanded; }
    
signals:
    void expandedChanged(bool expanded);
    
private slots:
    void onCollapseButtonClicked();
    
private:
    void updateCollapseButton();
    
    QPushButton* m_btnCollapse;
    QLabel* m_labelTitle;
    QWidget* m_contentWidget;
    QFrame* m_frameContent;
    bool m_expanded = true;
};

// collapsiblepanel.cpp
CollapsiblePanel::CollapsiblePanel(const QString& title, QWidget* parent)
    : QWidget(parent) {
    QVBoxLayout* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);
    
    // 标题栏
    QWidget* titleBar = new QWidget();
    QHBoxLayout* titleLayout = new QHBoxLayout(titleBar);
    titleLayout->setContentsMargins(10, 5, 10, 5);
    
    m_btnCollapse = new QPushButton();
    m_btnCollapse->setFixedSize(20, 20);
    m_btnCollapse->setFlat(true);
    m_btnCollapse->setCursor(Qt::PointingHandCursor);
    connect(m_btnCollapse, &QPushButton::clicked, this, &CollapsiblePanel::onCollapseButtonClicked);
    
    m_labelTitle = new QLabel(title);
    m_labelTitle->setStyleSheet("font-weight: bold;");
    
    titleLayout->addWidget(m_btnCollapse);
    titleLayout->addWidget(m_labelTitle);
    titleLayout->addStretch();
    
    // 内容框架
    m_frameContent = new QFrame();
    m_frameContent->setFrameStyle(QFrame::Panel | QFrame::Raised);
    QVBoxLayout* contentLayout = new QVBoxLayout(m_frameContent);
    contentLayout->setContentsMargins(10, 10, 10, 10);
    contentLayout->setSpacing(5);
    
    // 添加到主布局
    mainLayout->addWidget(titleBar);
    mainLayout->addWidget(m_frameContent);
    
    updateCollapseButton();
}

void CollapsiblePanel::setContentWidget(QWidget* content) {
    m_contentWidget = content;
    QVBoxLayout* layout = qobject_cast<QVBoxLayout*>(m_frameContent->layout());
    layout->addWidget(content);
}

void CollapsiblePanel::setExpanded(bool expanded) {
    if (m_expanded == expanded) {
        return;
    }
    
    m_expanded = expanded;
    m_frameContent->setVisible(expanded);
    updateCollapseButton();
    emit expandedChanged(expanded);
}

void CollapsiblePanel::onCollapseButtonClicked() {
    setExpanded(!m_expanded);
}

void CollapsiblePanel::updateCollapseButton() {
    if (m_expanded) {
        m_btnCollapse->setText("▼");
        m_btnCollapse->setToolTip("点击折叠");
    } else {
        m_btnCollapse->setText("▶");
        m_btnCollapse->setToolTip("点击展开");
    }
}
```

**使用示例**:
```cpp
// 在主窗口中使用
CollapsiblePanel* panel = new CollapsiblePanel("高级选项", this);
QWidget* content = new QWidget();
QVBoxLayout* layout = new QVBoxLayout(content);
layout->addWidget(new QCheckBox("选项1"));
layout->addWidget(new QCheckBox("选项2"));
panel->setContentWidget(content);

// 连接信号
connect(panel, &CollapsiblePanel::expandedChanged, [](bool expanded) {
    qDebug() << "面板状态:" << (expanded ? "展开" : "折叠");
});

// 控制折叠状态
panel->setExpanded(false);  // 折叠
panel->setExpanded(true);   // 展开
```

---

### 1.3 手风琴(Accordion)效果

**适用场景**: 多个面板,一次只能展开一个

**Qt实现**:

```cpp
// accordion.h
class Accordion : public QWidget {
    Q_OBJECT
public:
    explicit Accordion(QWidget* parent = nullptr);
    
    void addPanel(const QString& title, QWidget* content);
    void removePanel(int index);
    void setExpandedPanel(int index);
    int expandedPanelIndex() const { return m_expandedIndex; }
    
signals:
    void panelExpanded(int index);
    
private:
    void onPanelToggled(int index, bool expanded);
    
    QList<CollapsiblePanel*> m_panels;
    int m_expandedIndex = -1;
};

// accordion.cpp
Accordion::Accordion(QWidget* parent) : QWidget(parent) {
    QVBoxLayout* layout = new QVBoxLayout(this);
    layout->setContentsMargins(0, 0, 0, 0);
    layout->setSpacing(2);
}

void Accordion::addPanel(const QString& title, QWidget* content) {
    int index = m_panels.size();
    
    CollapsiblePanel* panel = new CollapsiblePanel(title, this);
    panel->setContentWidget(content);
    panel->setExpanded(false);
    
    // 连接信号
    connect(panel, &CollapsiblePanel::expandedChanged, [this, index](bool expanded) {
        onPanelToggled(index, expanded);
    });
    
    m_panels.append(panel);
    layout()->addWidget(panel);
    
    // 如果是第一个面板,自动展开
    if (m_panels.size() == 1) {
        setExpandedPanel(0);
    }
}

void Accordion::removePanel(int index) {
    if (index < 0 || index >= m_panels.size()) {
        return;
    }
    
    CollapsiblePanel* panel = m_panels.takeAt(index);
    layout()->removeWidget(panel);
    delete panel;
    
    // 调整展开索引
    if (m_expandedIndex == index) {
        m_expandedIndex = -1;
    } else if (m_expandedIndex > index) {
        m_expandedIndex--;
    }
}

void Accordion::setExpandedPanel(int index) {
    if (index < -1 || index >= m_panels.size()) {
        return;
    }
    
    // 折叠所有面板
    for (int i = 0; i < m_panels.size(); ++i) {
        m_panels[i]->setExpanded(false);
    }
    
    // 展开指定面板
    if (index >= 0) {
        m_panels[index]->setExpanded(true);
    }
    
    m_expandedIndex = index;
    emit panelExpanded(index);
}

void Accordion::onPanelToggled(int index, bool expanded) {
    if (expanded) {
        setExpandedPanel(index);
    }
}
```

**使用示例**:
```cpp
// 创建手风琴
Accordion* accordion = new Accordion(this);

// 添加面板
QWidget* panel1Content = new QWidget();
new QVBoxLayout(panel1Content)->addWidget(new QLabel("面板1内容"));
accordion->addPanel("面板1", panel1Content);

QWidget* panel2Content = new QWidget();
new QVBoxLayout(panel2Content)->addWidget(new QLabel("面板2内容"));
accordion->addPanel("面板2", panel2Content);

QWidget* panel3Content = new QWidget();
new QVBoxLayout(panel3Content)->addWidget(new QLabel("面板3内容"));
accordion->addPanel("面板3", panel3Content);

// 设置默认展开的面板
accordion->setExpandedPanel(0);

// 监听面板变化
connect(accordion, &Accordion::panelExpanded, [](int index) {
    qDebug() << "展开面板:" << index;
});
```

---

## 📋 2. 标签页动态管理

### 2.1 动态添加/删除Tab页

**WinForms实现**:
```csharp
// 添加
TabPage newPage = new TabPage("新标签页");
tabControl.TabPages.Add(newPage);

// 删除
tabControl.TabPages.RemoveAt(index);

// 显示/隐藏 (没有直接方法)
tabPage.Hide();  // 不推荐,会导致标签页位置变化
```

**Qt实现**:

```cpp
// mainwindow.h
class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget* parent = nullptr);
    
private slots:
    void onAddTabClicked();
    void onCloseTabClicked(int index);
    void onTabChanged(int index);
    
private:
    QTabWidget* m_tabWidget;
    QPushButton* m_btnAddTab;
};

// mainwindow.cpp
MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
    m_tabWidget = new QTabWidget();
    m_tabWidget->setTabsClosable(true);  // 启用关闭按钮
    m_tabWidget->setMovable(true);       // 启用拖拽
    
    // 连接信号
    connect(m_tabWidget, &QTabWidget::tabCloseRequested, this, &MainWindow::onCloseTabClicked);
    connect(m_tabWidget, &QTabWidget::currentChanged, this, &MainWindow::onTabChanged);
    
    // 添加添加按钮
    m_btnAddTab = new QPushButton("+");
    m_btnAddTab->setFixedSize(20, 20);
    m_btnAddTab->setFlat(true);
    connect(m_btnAddTab, &QPushButton::clicked, this, &MainWindow::onAddTabClicked);
    
    // 将按钮添加到标签栏右侧
    m_tabWidget->setCornerWidget(m_btnAddTab, Qt::TopRightCorner);
    
    // 添加初始标签页
    addNewTab("主页面", createHomePageContent());
    
    setCentralWidget(m_tabWidget);
}

void MainWindow::addNewTab(const QString& title, QWidget* content) {
    int index = m_tabWidget->addTab(content, title);
    m_tabWidget->setCurrentIndex(index);
}

void MainWindow::onAddTabClicked() {
    static int tabCount = 1;
    QString title = QString("新标签页 %1").arg(++tabCount);
    
    QWidget* content = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(content);
    layout->addWidget(new QLabel(QString("这是 %1 的内容").arg(title)));
    
    addNewTab(title, content);
}

void MainWindow::onCloseTabClicked(int index) {
    // 保留第一个标签页
    if (index <= 0) {
        return;
    }
    
    // 确认关闭
    QWidget* tab = m_tabWidget->widget(index);
    QString title = m_tabWidget->tabText(index);
    
    QMessageBox::StandardButton reply = QMessageBox::question(
        this,
        "确认关闭",
        QString("确定要关闭标签页 \"%1\" 吗?").arg(title),
        QMessageBox::Yes | QMessageBox::No
    );
    
    if (reply == QMessageBox::Yes) {
        m_tabWidget->removeTab(index);
        delete tab;
    }
}

void MainWindow::onTabChanged(int index) {
    qDebug() << "当前标签页:" << index;
    // 可以在这里更新UI状态
}
```

---

### 2.2 显示/隐藏Tab页 (Qt 5.15+)

**Qt实现**:

```cpp
// Qt 5.15+ 支持直接隐藏标签页
void MainWindow::setTabVisible(int index, bool visible) {
    if (QVersionNumber::fromString(QT_VERSION_STR) >= QVersionNumber(5, 15, 0)) {
        m_tabWidget->setTabVisible(index, visible);
    } else {
        // Qt 5.15以下版本的替代方案
        if (visible) {
            // 重新添加
            QWidget* widget = m_hiddenTabs.take(index);
            QString title = m_hiddenTabTitles.take(index);
            m_tabWidget->insertTab(index, widget, title);
        } else {
            // 隐藏
            QWidget* widget = m_tabWidget->widget(index);
            QString title = m_tabWidget->tabText(index);
            m_hiddenTabs[index] = widget;
            m_hiddenTabTitles[index] = title;
            m_tabWidget->removeTab(index);
        }
    }
}
```

---

### 2.3 禁用Tab页

**Qt实现**:

```cpp
// 禁用标签页
void MainWindow::setTabEnabled(int index, bool enabled) {
    m_tabWidget->setTabEnabled(index, enabled);
}

// 样式
m_tabWidget->setStyleSheet(R"(
    QTabBar::tab:disabled {
        color: rgb(170, 170, 170);
        background-color: rgb(230, 230, 230);
    }
)");
```

---

## 📋 3. 菜单动态控制

### 3.1 显示/隐藏菜单项

**WinForms实现**:
```csharp
menuItem.Visible = false;
menuItem.Visible = true;
```

**Qt实现**:

```cpp
// 创建菜单
QMenuBar* menuBar = menuBar();
QMenu* menuFile = menuBar->addMenu("文件(&F)");
QMenu* menuView = menuBar->addMenu("视图(&V)");
QMenu* menuTools = menuBar->addMenu("工具(&T)");
QMenu* menuHelp = menuBar->addMenu("帮助(&H)");

// 添加菜单项
QAction* actionNew = menuFile->addAction("新建(&N)");
actionNew->setShortcut(QKeySequence::New);
actionNew->setStatusTip("创建新文件");

QAction* actionOpen = menuFile->addAction("打开(&O)");
actionOpen->setShortcut(QKeySequence::Open);
actionOpen->setStatusTip("打开文件");

QAction* actionSave = menuFile->addAction("保存(&S)");
actionSave->setShortcut(QKeySequence::Save);
actionSave->setStatusTip("保存文件");

menuFile->addSeparator();

QAction* actionExit = menuFile->addAction("退出(&X)");
actionExit->setShortcut(QKeySequence::Quit);
actionExit->setStatusTip("退出程序");

// 高级菜单项(默认隐藏)
QAction* actionAdvanced = menuTools->addAction("高级设置(&A)");
actionAdvanced->setVisible(false);  // 默认隐藏

QAction* actionDebug = menuTools->addAction("调试工具(&D)");
actionDebug->setVisible(false);  // 默认隐藏

// 动态显示/隐藏
void MainWindow::toggleAdvancedMenu(bool show) {
    actionAdvanced->setVisible(show);
    actionDebug->setVisible(show);
}

// 根据状态显示
void MainWindow::updateMenuVisibility() {
    actionSave->setVisible(hasUnsavedChanges);
    actionAdvanced->isVisible(isAdminMode);
}
```

---

### 3.2 启用/禁用菜单项

**WinForms实现**:
```csharp
menuItem.Enabled = false;
menuItem.Enabled = true;
```

**Qt实现**:

```cpp
// 创建菜单项
QAction* actionCopy = editMenu->addAction("复制(&C)");
actionCopy->setShortcut(QKeySequence::Copy);

QAction* actionPaste = editMenu->addAction("粘贴(&V)");
actionPaste->setShortcut(QKeySequence::Paste);

QAction* actionUndo = editMenu->addAction("撤销(&Z)");
actionUndo->setShortcut(QKeySequence::Undo);

QAction* actionRedo = editMenu->addAction("重做(&Y)");
actionRedo->setShortcut(QKeySequence::Redo);

// 连接信号
connect(actionCopy, &QAction::triggered, this, &MainWindow::onCopy);
connect(actionPaste, &QAction::triggered, this, &MainWindow::onPaste);
connect(actionUndo, &QAction::triggered, this, &MainWindow::onUndo);
connect(actionRedo, &QAction::triggered, this, &MainWindow::onRedo);

// 根据状态启用/禁用
void MainWindow::updateMenuStates() {
    bool hasSelection = tableView->selectionModel()->hasSelection();
    bool canUndo = document->canUndo();
    bool canRedo = document->canRedo();
    bool canPaste = QApplication::clipboard()->text().isEmpty() == false;
    
    actionCopy->setEnabled(hasSelection);
    actionPaste->setEnabled(canPaste);
    actionUndo->setEnabled(canUndo);
    actionRedo->setEnabled(canRedo);
}

// 自动更新(使用信号槽)
void MainWindow::setupAutoUpdate() {
    // 选择变化时更新
    connect(tableView->selectionModel(), &QItemSelectionModel::selectionChanged,
            this, &MainWindow::updateMenuStates);
    
    // 文档状态变化时更新
    connect(document, &Document::undoStackChanged,
            this, &MainWindow::updateMenuStates);
}
```

---

### 3.3 可选中菜单项

**WinForms实现**:
```csharp
toolStripButton.Checked = true;
toolStripButton.CheckState = CheckState.Checked;
```

**Qt实现**:

```cpp
// 创建可选中菜单项
QAction* actionShowToolbar = menuView->addAction("显示工具栏(&T)");
actionShowToolbar->setCheckable(true);
actionShowToolbar->setChecked(true);

QAction* actionShowStatusBar = menuView->addAction("显示状态栏(&S)");
actionShowStatusBar->setCheckable(true);
actionShowStatusBar->setChecked(true);

QAction* actionShowGrid = menuView->addAction("显示网格(&G)");
actionShowGrid->setCheckable(true);
actionShowGrid->setChecked(false);

// 连接信号
connect(actionShowToolbar, &QAction::toggled, [this](bool checked) {
    toolBar->setVisible(checked);
});

connect(actionShowStatusBar, &QAction::toggled, [this](bool checked) {
    statusBar()->setVisible(checked);
});

connect(actionShowGrid, &QAction::toggled, [this](bool checked) {
    showGrid = checked;
    update();  // 重新绘制
});

// 独占选择(单选)
QAction* actionViewDetails = menuView->addAction("详细信息");
actionViewDetails->setCheckable(true);
actionViewDetails->setChecked(true);

QAction* actionViewList = menuView->addAction("列表");
actionViewList->setCheckable(true);

QAction* actionViewIcons = menuView->addAction("图标");
actionViewIcons->setCheckable(true);

// 创建动作组(确保互斥)
QActionGroup* viewGroup = new QActionGroup(this);
viewGroup->setExclusive(true);
viewGroup->addAction(actionViewDetails);
viewGroup->addAction(actionViewList);
viewGroup->addAction(actionViewIcons);

// 连接信号
connect(actionViewDetails, &QAction::triggered, [this]() { setViewMode(ViewMode::Details); });
connect(actionViewList, &QAction::triggered, [this]() { setViewMode(ViewMode::List); });
connect(actionViewIcons, &QAction::triggered, [this]() { setViewMode(ViewMode::Icons); });
```

---

### 3.4 动态添加菜单项

**WinForms实现**:
```csharp
ToolStripMenuItem recentItem = new ToolStripMenuItem(filename);
recentItem.Click += RecentItem_Click;
menuRecent.DropDownItems.Add(recentItem);
```

**Qt实现**:

```cpp
// mainwindow.h
class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget* parent = nullptr);
    
    void addRecentFile(const QString& filename);
    void clearRecentFiles();
    
private slots:
    void onRecentFileTriggered();
    
private:
    QMenu* m_menuRecent;
    QList<QAction*> m_recentFileActions;
    static const int MAX_RECENT_FILES = 10;
};

// mainwindow.cpp
MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
    // 创建菜单
    QMenu* menuFile = menuBar()->addMenu("文件(&F)");
    
    // 最近文件菜单
    m_menuRecent = menuFile->addMenu("最近文件(&R)");
    m_menuRecent->setEnabled(false);  // 没有最近文件时禁用
    
    // 添加清除菜单项
    QAction* actionClearRecent = m_menuRecent->addAction("清除最近文件(&C)");
    connect(actionClearRecent, &QAction::triggered, this, &MainWindow::clearRecentFiles);
    m_menuRecent->addSeparator();
}

void MainWindow::addRecentFile(const QString& filename) {
    // 检查是否已存在
    for (QAction* action : m_recentFileActions) {
        if (action->data().toString() == filename) {
            // 移动到第一个位置
            m_menuRecent->removeAction(action);
            m_menuRecent->insertAction(m_menuRecent->actions().first(), action);
            return;
        }
    }
    
    // 创建新动作
    QAction* action = new QAction(filename, this);
    action->setData(filename);
    connect(action, &QAction::triggered, this, &MainWindow::onRecentFileTriggered);
    
    // 插入到第一个位置(在清除按钮之后)
    QAction* insertBefore = m_menuRecent->actions().at(1);
    m_menuRecent->insertAction(insertBefore, action);
    m_recentFileActions.prepend(action);
    
    // 限制最大数量
    while (m_recentFileActions.size() > MAX_RECENT_FILES) {
        QAction* last = m_recentFileActions.takeLast();
        m_menuRecent->removeAction(last);
        delete last;
    }
    
    // 启用菜单
    m_menuRecent->setEnabled(true);
}

void MainWindow::clearRecentFiles() {
    for (QAction* action : m_recentFileActions) {
        m_menuRecent->removeAction(action);
        delete action;
    }
    m_recentFileActions.clear();
    m_menuRecent->setEnabled(false);
}

void MainWindow::onRecentFileTriggered() {
    QAction* action = qobject_cast<QAction*>(sender());
    if (action) {
        QString filename = action->data().toString();
        openFile(filename);
    }
}
```

---

## 📋 4. 工具栏状态管理

### 4.1 显示/隐藏工具栏按钮

**WinForms实现**:
```csharp
toolStripButton.Visible = false;
toolStripButton.Visible = true;
```

**Qt实现**:

```cpp
// 创建工具栏
QToolBar* toolBar = addToolBar("主工具栏");
toolBar->setMovable(true);     // 可移动
toolBar->setFloatable(true);   // 可浮动
toolBar->setAllowedAreas(Qt::TopToolBarArea | Qt::BottomToolBarArea);

// 添加工具栏按钮
QAction* actionNew = toolBar->addAction(QIcon(":/icons/new.png"), "新建");
actionNew->setShortcut(QKeySequence::New);

QAction* actionOpen = toolBar->addAction(QIcon(":/icons/open.png"), "打开");
actionOpen->setShortcut(QKeySequence::Open);

QAction* actionSave = toolBar->addAction(QIcon(":/icons/save.png"), "保存");
actionSave->setShortcut(QKeySequence::Save);

toolBar->addSeparator();

// 高级按钮(默认隐藏)
QAction* actionAdvanced = toolBar->addAction(QIcon(":/icons/advanced.png"), "高级");
actionAdvanced->setVisible(false);  // 默认隐藏

// 动态显示/隐藏
void MainWindow::toggleAdvancedTools(bool show) {
    actionAdvanced->setVisible(show);
    
    // 更新工具栏样式
    if (show) {
        toolBar->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
    } else {
        toolBar->setToolButtonStyle(Qt::ToolButtonIconOnly);
    }
}
```

---

### 4.2 启用/禁用工具栏按钮

**WinForms实现**:
```csharp
toolStripButton.Enabled = false;
toolStripButton.Enabled = true;
```

**Qt实现**:

```cpp
// 创建工具栏
QToolBar* toolBar = addToolBar("编辑工具栏");

QAction* actionCut = toolBar->addAction(QIcon(":/icons/cut.png"), "剪切");
actionCut->setShortcut(QKeySequence::Cut);

QAction* actionCopy = toolBar->addAction(QIcon(":/icons/copy.png"), "复制");
actionCopy->setShortcut(QKeySequence::Copy);

QAction* actionPaste = toolBar->addAction(QIcon(":/icons/paste.png"), "粘贴");
actionPaste->setShortcut(QKeySequence::Paste);

toolBar->addSeparator();

QAction* actionUndo = toolBar->addAction(QIcon(":/icons/undo.png"), "撤销");
actionUndo->setShortcut(QKeySequence::Undo);

QAction* actionRedo = toolBar->addAction(QIcon(":/icons/redo.png"), "重做");
actionRedo->setShortcut(QKeySequence::Redo);

// 根据状态启用/禁用
void MainWindow::updateToolbarStates() {
    bool hasSelection = tableView->selectionModel()->hasSelection();
    bool canUndo = document->canUndo();
    bool canRedo = document->canRedo();
    bool canPaste = QApplication::clipboard()->text().isEmpty() == false;
    
    actionCut->setEnabled(hasSelection);
    actionCopy->setEnabled(hasSelection);
    actionPaste->setEnabled(canPaste);
    actionUndo->setEnabled(canUndo);
    actionRedo->setEnabled(canRedo);
}

// 自动更新
void MainWindow::setupAutoUpdate() {
    connect(tableView->selectionModel(), &QItemSelectionModel::selectionChanged,
            this, &MainWindow::updateToolbarStates);
    connect(document, &Document::undoStackChanged,
            this, &MainWindow::updateToolbarStates);
    connect(QApplication::clipboard(), &QClipboard::dataChanged,
            this, &MainWindow::updateToolbarStates);
}
```

---

### 4.3 可选中工具栏按钮

**WinForms实现**:
```csharp
toolStripButton.CheckOnClick = true;
toolStripButton.Checked = true;
```

**Qt实现**:

```cpp
// 创建可选中按钮
QAction* actionBold = toolBar->addAction(QIcon(":/icons/bold.png"), "加粗");
actionBold->setCheckable(true);
actionBold->setShortcut(QKeySequence::Bold);

QAction* actionItalic = toolBar->addAction(QIcon(":/icons/italic.png"), "斜体");
actionItalic->setCheckable(true);
actionItalic->setShortcut(QKeySequence::Italic);

QAction* actionUnderline = toolBar->addAction(QIcon(":/icons/underline.png"), "下划线");
actionUnderline->setCheckable(true);
actionUnderline->setShortcut(QKeySequence::Underline);

// 连接信号
connect(actionBold, &QAction::toggled, [this](bool checked) {
    textEdit->setFontWeight(checked ? QFont::Bold : QFont::Normal);
});

connect(actionItalic, &QAction::toggled, [this](bool checked) {
    textEdit->setFontItalic(checked);
});

connect(actionUnderline, &QAction::toggled, [this](bool checked) {
    textEdit->setFontUnderline(checked);
});

// 同步状态(当光标位置变化时更新)
void MainWindow::updateToolbarFromSelection() {
    QTextCursor cursor = textEdit->textCursor();
    QTextCharFormat format = cursor.charFormat();
    
    actionBold->setChecked(format.fontWeight() == QFont::Bold);
    actionItalic->setChecked(format.fontItalic());
    actionUnderline->setChecked(format.fontUnderline());
}

connect(textEdit, &QTextEdit::cursorPositionChanged,
        this, &MainWindow::updateToolbarFromSelection);
```

---

### 4.4 工具栏样式切换

**Qt实现**:

```cpp
// 切换工具栏按钮样式
void MainWindow::setToolbarButtonStyle(Qt::ToolButtonStyle style) {
    toolBar->setToolButtonStyle(style);
}

// 示例使用
void MainWindow::onToolbarStyleChanged(QAction* action) {
    if (action == actionStyleIcons) {
        setToolbarButtonStyle(Qt::ToolButtonIconOnly);
    } else if (action == actionStyleText) {
        setToolbarButtonStyle(Qt::ToolButtonTextOnly);
    } else if (action == actionStyleBeside) {
        setToolbarButtonStyle(Qt::ToolButtonTextBesideIcon);
    } else if (action == actionStyleUnder) {
        setToolbarButtonStyle(Qt::ToolButtonTextUnderIcon);
    }
}
```

---

## 📋 5. 状态栏动态内容

### 5.1 动态更新状态栏

**WinForms实现**:
```csharp
statusStrip.Items[0].Text = "就绪";
statusStrip.Items[1].Text = "共 100 条记录";
```

**Qt实现**:

```cpp
// 创建状态栏
QStatusBar* statusBar = statusBar();

// 添加标签
QLabel* labelStatus = new QLabel("就绪");
statusBar->addWidget(labelStatus);  // 左侧

statusBar->addPermanentWidget(new QLabel(" | "));  // 永久分隔符

QLabel* labelRecordCount = new QLabel("共 0 条记录");
statusBar->addPermanentWidget(labelRecordCount);  // 右侧

statusBar->addPermanentWidget(new QLabel(" | "));

QLabel* labelPosition = new QLabel("行 1, 列 1");
statusBar->addPermanentWidget(labelPosition);

// 动态更新
void MainWindow::updateStatus(const QString& message) {
    labelStatus->setText(message);
    
    // 3秒后恢复默认状态
    QTimer::singleShot(3000, [this]() {
        labelStatus->setText("就绪");
    });
}

void MainWindow::updateRecordCount(int count) {
    labelRecordCount->setText(QString("共 %1 条记录").arg(count));
}

void MainWindow::updateCursorPosition(int row, int column) {
    labelPosition->setText(QString("行 %1, 列 %2").arg(row + 1).arg(column + 1));
}
```

---

## 📋 6. 完整示例: 带可折叠界面的主窗口

```cpp
// mainwindow.h
class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    MainWindow(QWidget* parent = nullptr);
    
private:
    void setupMenuBar();
    void setupToolBar();
    void setupStatusBar();
    void setupCentralWidget();
    
    QWidget* createLeftPanel();
    QWidget* createCentralPanel();
    QWidget* createRightPanel();
    
    // 菜单动作
    QMenu* m_menuFile;
    QMenu* m_menuView;
    QMenu* m_menuTools;
    
    // 工具栏
    QToolBar* m_toolBar;
    QAction* m_actionToggleLeftPanel;
    QAction* m_actionToggleRightPanel;
    
    // 中央控件
    QSplitter* m_splitterMain;
    QSplitter* m_splitterLeft;
    CollapsiblePanel* m_panelLeft;
    CollapsiblePanel* m_panelRight;
    
    // 状态栏
    QLabel* m_labelStatus;
    QLabel* m_labelRecordCount;
};

// mainwindow.cpp
MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {
    setWindowTitle("可折叠界面示例");
    resize(1200, 800);
    
    setupMenuBar();
    setupToolBar();
    setupStatusBar();
    setupCentralWidget();
    
    // 默认展开所有面板
    m_panelLeft->setExpanded(true);
    m_panelRight->setExpanded(true);
}

void MainWindow::setupMenuBar() {
    // 视图菜单
    m_menuView = menuBar()->addMenu("视图(&V)");
    
    // 显示/隐藏左面板
    m_actionToggleLeftPanel = m_menuView->addAction("左侧面板(&L)");
    m_actionToggleLeftPanel->setCheckable(true);
    m_actionToggleLeftPanel->setChecked(true);
    connect(m_actionToggleLeftPanel, &QAction::toggled, [this](bool checked) {
        m_panelLeft->setVisible(checked);
    });
    
    // 显示/隐藏右面板
    m_actionToggleRightPanel = m_menuView->addAction("右侧面板(&R)");
    m_actionToggleRightPanel->setCheckable(true);
    m_actionToggleRightPanel->setChecked(true);
    connect(m_actionToggleRightPanel, &QAction::toggled, [this](bool checked) {
        m_panelRight->setVisible(checked);
    });
    
    // 工具菜单
    m_menuTools = menuBar()->addMenu("工具(&T)");
    
    QAction* actionCollapseAll = m_menuTools->addAction("折叠所有(&A)");
    connect(actionCollapseAll, &QAction::triggered, [this]() {
        m_panelLeft->setExpanded(false);
        m_panelRight->setExpanded(false);
    });
    
    QAction* actionExpandAll = m_menuTools->addAction("展开所有(&E)");
    connect(actionExpandAll, &QAction::triggered, [this]() {
        m_panelLeft->setExpanded(true);
        m_panelRight->setExpanded(true);
    });
}

void MainWindow::setupToolBar() {
    m_toolBar = addToolBar("工具栏");
    
    QAction* actionToggleLeft = m_toolBar->addAction("左面板");
    actionToggleLeft->setCheckable(true);
    actionToggleLeft->setChecked(true);
    connect(actionToggleLeft, &QAction::toggled, m_actionToggleLeftPanel, &QAction::setChecked);
    
    QAction* actionToggleRight = m_toolBar->addAction("右面板");
    actionToggleRight->setCheckable(true);
    actionToggleRight->setChecked(true);
    connect(actionToggleRight, &QAction::toggled, m_actionToggleRightPanel, &QAction::setChecked);
}

void MainWindow::setupStatusBar() {
    m_labelStatus = new QLabel("就绪");
    statusBar()->addWidget(m_labelStatus);
    
    m_labelRecordCount = new QLabel("共 0 条记录");
    statusBar()->addPermanentWidget(m_labelRecordCount);
}

void MainWindow::setupCentralWidget() {
    // 主分割器
    m_splitterMain = new QSplitter(Qt::Horizontal);
    
    // 左侧分割器
    m_splitterLeft = new QSplitter(Qt::Vertical);
    
    // 左侧面板
    m_panelLeft = new CollapsiblePanel("导航", this);
    m_panelLeft->setContentWidget(createLeftPanel());
    m_splitterLeft->addWidget(m_panelLeft);
    
    // 中央面板
    m_splitterLeft->addWidget(createCentralPanel());
    m_splitterLeft->setStretchFactor(1, 1);
    
    // 右侧面板
    m_panelRight = new CollapsiblePanel("属性", this);
    m_panelRight->setContentWidget(createRightPanel());
    
    // 添加到主分割器
    m_splitterMain->addWidget(m_splitterLeft);
    m_splitterMain->addWidget(m_panelRight);
    m_splitterMain->setStretchFactor(0, 1);
    
    setCentralWidget(m_splitterMain);
}

QWidget* MainWindow::createLeftPanel() {
    QWidget* widget = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(widget);
    
    QTreeWidget* tree = new QTreeWidget();
    tree->setHeaderHidden(true);
    
    QTreeWidgetItem* root = new QTreeWidgetItem(tree, QStringList() << "根节点");
    QTreeWidgetItem* child1 = new QTreeWidgetItem(root, QStringList() << "子节点1");
    QTreeWidgetItem* child2 = new QTreeWidgetItem(root, QStringList() << "子节点2");
    
    layout->addWidget(tree);
    
    return widget;
}

QWidget* MainWindow::createCentralPanel() {
    QWidget* widget = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(widget);
    
    QTableView* table = new QTableView();
    layout->addWidget(table);
    
    return widget;
}

QWidget* MainWindow::createRightPanel() {
    QWidget* widget = new QWidget();
    QVBoxLayout* layout = new QVBoxLayout(widget);
    
    QFormLayout* formLayout = new QFormLayout();
    
    QLineEdit* lineEdit1 = new QLineEdit();
    QLineEdit* lineEdit2 = new QLineEdit();
    QComboBox* comboBox = new QComboBox();
    comboBox->addItems({"选项1", "选项2", "选项3"});
    
    formLayout->addRow("属性1:", lineEdit1);
    formLayout->addRow("属性2:", lineEdit2);
    formLayout->addRow("属性3:", comboBox);
    
    layout->addLayout(formLayout);
    
    return widget;
}
```

---

## 📋 总结

### 实现要点

1. **面板折叠**: 使用QGroupBox::setCheckable()或自定义CollapsiblePanel
2. **手风琴**: 使用Accordion类,一次只展开一个面板
3. **标签页管理**: 动态addTab/removeTab,Qt 5.15+支持setTabVisible()
4. **菜单动态控制**: setVisible()/setEnabled()/setCheckable()
5. **工具栏状态**: 与菜单项共享QAction,自动同步状态
6. **状态栏**: addWidget(左侧)/addPermanentWidget(右侧)

### 与WinForms对比

| 功能 | WinForms | Qt | 实现难度 |
|-----|---------|----|---------|
| 面板折叠 | 自定义实现 | QGroupBox可折叠 | 简单 |
| 手风琴 | 自定义实现 | 自定义Accordion | 中等 |
| 标签页管理 | TabPages | addTab/removeTab | 简单 |
| Tab隐藏 | 无 | setTabVisible (Qt 5.15+) | 简单 |
| 菜单动态 | Visible/Enabled | setVisible/enabled | 简单 |
| 工具栏状态 | 与菜单同步 | 共享QAction | 简单 |

### 关键技巧

1. **使用QAction**: 菜单和工具栏共享同一个QAction,自动同步状态
2. **信号槽连接**: 使用lambda表达式简化代码
3. **样式优化**: 使用QSS统一控制外观
4. **状态同步**: 使用信号槽机制自动更新UI状态
