#!/usr/bin/env node

/**
 * Qt代码生成工具
 * 根据WinForms分析报告生成Qt代码
 */

const fs = require('fs');
const path = require('path');

// 命令行参数解析
const args = process.argv.slice(2);
const options = {
    mapping: null,
    output: './qt_output',
    projectName: 'QtMigratedApp',
    template: 'basic-qt-widgets',
    verbose: false
};

// 解析参数
for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--mapping' || arg === '-m') {
        options.mapping = args[++i];
    } else if (arg === '--output' || arg === '-o') {
        options.output = args[++i];
    } else if (arg === '--name' || arg === '-n') {
        options.projectName = args[++i];
    } else if (arg === '--template' || arg === '-t') {
        options.template = args[++i];
    } else if (arg === '--verbose' || arg === '-v') {
        options.verbose = true;
    } else if (arg === '--help' || arg === '-h') {
        printHelp();
        process.exit(0);
    }
}

// 检查必要参数
if (!options.mapping) {
    console.error('错误: 必须指定映射文件路径');
    printHelp();
    process.exit(1);
}

// 检查映射文件是否存在
if (!fs.existsSync(options.mapping)) {
    console.error(`错误: 映射文件不存在: ${options.mapping}`);
    process.exit(1);
}

console.log('=== Qt代码生成工具 ===');
console.log(`映射文件: ${options.mapping}`);
console.log(`输出目录: ${options.output}`);
console.log(`项目名称: ${options.projectName}`);
console.log(`模板类型: ${options.template}`);
console.log('');

// 主生成函数
async function generateQtCode() {
    try {
        // 1. 加载映射数据
        console.log('1. 加载映射数据...');
        const mappingData = JSON.parse(fs.readFileSync(options.mapping, 'utf8'));
        
        // 2. 创建输出目录
        console.log('2. 创建项目目录结构...');
        createProjectStructure();
        
        // 3. 生成CMakeLists.txt
        console.log('3. 生成构建配置...');
        generateCMakeLists(mappingData);
        
        // 4. 生成主程序文件
        console.log('4. 生成主程序文件...');
        generateMainFiles(mappingData);
        
        // 5. 生成窗体类文件
        console.log('5. 生成窗体类文件...');
        generateFormClasses(mappingData);
        
        // 6. 生成UI文件
        console.log('6. 生成UI文件...');
        generateUiFiles(mappingData);
        
        // 7. 生成资源文件
        console.log('7. 生成资源文件...');
        generateResourceFiles();
        
        // 8. 显示生成摘要
        console.log('8. 生成完成，显示摘要...');
        printGenerationSummary(mappingData);
        
        console.log('');
        console.log('✅ Qt项目生成完成！');
        console.log(`   项目位置: ${path.resolve(options.output)}`);
        console.log(`   构建命令: cd ${options.output} && mkdir build && cd build && cmake ..`);
        console.log(`   运行命令: ./${options.projectName}`);
        
    } catch (error) {
        console.error('生成过程中出现错误:', error.message);
        if (options.verbose) {
            console.error(error.stack);
        }
        process.exit(1);
    }
}

// 创建项目目录结构
function createProjectStructure() {
    const dirs = [
        '',
        'src',
        'include',
        'ui',
        'resources',
        'resources/icons',
        'resources/images',
        'docs',
        'tests'
    ];
    
    for (const dir of dirs) {
        const fullPath = path.join(options.output, dir);
        if (!fs.existsSync(fullPath)) {
            fs.mkdirSync(fullPath, { recursive: true });
            if (options.verbose) {
                console.log(`   创建目录: ${dir || '.'}`);
            }
        }
    }
}

// 生成CMakeLists.txt
function generateCMakeLists(mappingData) {
    const cmakeContent = `# ${options.projectName} - 从WinForms迁移的Qt项目
cmake_minimum_required(VERSION 3.10)
project(${options.projectName} VERSION 1.0.0 LANGUAGES CXX)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# MSVC编码支持（解决C4819警告）
if(MSVC)
    add_compile_options(/utf-8)
    add_compile_definitions(_CRT_SECURE_NO_WARNINGS)
endif()

# ========== 遵循 qt-cmake-build 规范 - 硬编码Qt路径 ==========
set(Qt5_DIR "D:/Qt/Qt5.12.10/5.12.10/msvc2017_64/lib/cmake/Qt5")
set(CMAKE_PREFIX_PATH "D:/Qt/Qt5.12.10/5.12.10/msvc2017_64")

# 查找Qt5组件
find_package(Qt5 REQUIRED COMPONENTS
    Core
    Widgets
    Gui
)

# 启用自动资源编译
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# 源代码文件
set(SOURCES
    src/main.cpp
    ${mappingData.forms.map(form => `src/${form.name.toLowerCase()}.cpp`).join('\n    ')}
)

# 头文件
set(HEADERS
    include/mainwindow.h
    ${mappingData.forms.map(form => `include/${form.name.toLowerCase()}.h`).join('\n    ')}
)

# UI文件
set(FORMS
    ${mappingData.forms.map(form => `ui/${form.name.toLowerCase()}.ui`).join('\n    ')}
)

# 资源文件
set(RESOURCES
    resources/resources.qrc
)

# 创建可执行文件
add_executable(${options.projectName}
    \${SOURCES}
    \${HEADERS}
    \${FORMS}
    \${RESOURCES}
)

# 链接Qt库
target_link_libraries(${options.projectName}
    Qt5::Core
    Qt5::Widgets
    Qt5::Gui
)

# 安装目标
install(TARGETS ${options.projectName} DESTINATION bin)

# 项目信息
message(STATUS "项目: \${PROJECT_NAME}")
message(STATUS "版本: \${PROJECT_VERSION}")
message(STATUS "源文件: \${SOURCES}")
message(STATUS "从WinForms迁移的窗体: ${mappingData.forms.length}个")

# 迁移统计
${generateMigrationStats(mappingData)}
`;

    const cmakePath = path.join(options.output, 'CMakeLists.txt');
    fs.writeFileSync(cmakePath, cmakeContent);
    console.log(`   生成: CMakeLists.txt`);
}

// 生成迁移统计
function generateMigrationStats(mappingData) {
    const totalControls = mappingData.summary.totalControls;
    const totalEvents = mappingData.summary.totalEvents;
    
    return `# 迁移统计
message(STATUS "总控件数: ${totalControls}")
message(STATUS "总事件数: ${totalEvents}")
message(STATUS "生成时间: "${new Date().toISOString()})`;
}

// 生成主程序文件
function generateMainFiles(mappingData) {
    // 生成main.cpp
    const mainCppContent = `#include "mainwindow.h"
#include <QApplication>
#include <QStyleFactory>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // 设置应用程序样式
    app.setStyle(QStyleFactory::create("Fusion"));
    
    // 设置应用程序信息
    app.setApplicationName("${options.projectName}");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("MigratedFromWinForms");
    
    // 创建主窗口
    MainWindow window;
    window.show();
    
    return app.exec();
}
`;

    const mainCppPath = path.join(options.output, 'src/main.cpp');
    fs.writeFileSync(mainCppPath, mainCppContent);
    console.log(`   生成: src/main.cpp`);
    
    // 生成mainwindow.h
    const mainWindowHContent = `#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTabWidget>

// 包含所有窗体头文件
${mappingData.forms.map(form => `#include "${form.name.toLowerCase()}.h"`).join('\n')}

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    void setupUi();
    void setupConnections();
    void setupMenuBar();
    void setupStatusBar();
    
private slots:
    void onAbout();
    void onExit();

private:
    // UI组件
    QTabWidget *tabWidget;
    
    // 窗体实例
    ${mappingData.forms.map(form => `${form.name} *${form.name.toLowerCase()}Form;`).join('\n    ')}
};

#endif // MAINWINDOW_H
`;

    const mainWindowHPath = path.join(options.output, 'include/mainwindow.h');
    fs.writeFileSync(mainWindowHPath, mainWindowHContent);
    console.log(`   生成: include/mainwindow.h`);
    
    // 生成mainwindow.cpp
    const mainWindowCppContent = `#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMenuBar>
#include <QStatusBar>
#include <QMessageBox>
#include <QAction>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setupUi();
    setupConnections();
    setupMenuBar();
    setupStatusBar();
    
    // 设置窗口标题
    setWindowTitle("${options.projectName} - 从WinForms迁移");
    
    // 设置窗口大小
    resize(1024, 768);
}

MainWindow::~MainWindow()
{
    // 清理资源
}

void MainWindow::setupUi()
{
    // 创建中心部件
    QWidget *centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
    
    // 创建标签页控件
    tabWidget = new QTabWidget(centralWidget);
    
    // 创建窗体实例并添加到标签页
    ${mappingData.forms.map(form => `
    ${form.name.toLowerCase()}Form = new ${form.name}(this);
    tabWidget->addTab(${form.name.toLowerCase()}Form, "${form.name}");`).join('')}
    
    // 设置布局
    QVBoxLayout *layout = new QVBoxLayout(centralWidget);
    layout->addWidget(tabWidget);
    centralWidget->setLayout(layout);
}

void MainWindow::setupConnections()
{
    // 连接窗体信号
    ${mappingData.forms.map(form => `
    // ${form.name}信号连接
    // connect(${form.name.toLowerCase()}Form, &${form.name}::someSignal, this, &MainWindow::someSlot);`).join('')}
}

void MainWindow::setupMenuBar()
{
    // 文件菜单
    QMenu *fileMenu = menuBar()->addMenu("文件(&F)");
    
    QAction *exitAction = new QAction("退出(&X)", this);
    exitAction->setShortcut(QKeySequence::Quit);
    connect(exitAction, &QAction::triggered, this, &MainWindow::onExit);
    fileMenu->addAction(exitAction);
    
    // 帮助菜单
    QMenu *helpMenu = menuBar()->addMenu("帮助(&H)");
    
    QAction *aboutAction = new QAction("关于(&A)", this);
    connect(aboutAction, &QAction::triggered, this, &MainWindow::onAbout);
    helpMenu->addAction(aboutAction);
}

void MainWindow::setupStatusBar()
{
    statusBar()->showMessage("就绪 - 从WinForms迁移的Qt应用程序");
}

void MainWindow::onAbout()
{
    QMessageBox::about(this, "关于 ${options.projectName}",
        "<h3>${options.projectName}</h3>"
        "<p>版本: 1.0.0</p>"
        "<p>这是一个从WinForms迁移到Qt的应用程序。</p>"
        "<p>迁移统计:</p>"
        "<ul>"
        "<li>窗体数量: ${mappingData.forms.length}</li>"
        "<li>控件总数: ${mappingData.summary.totalControls}</li>"
        "<li>事件总数: ${mappingData.summary.totalEvents}</li>"
        "</ul>"
        "<p>生成时间: ${new Date().toLocaleString()}</p>");
}

void MainWindow::onExit()
{
    close();
}
`;

    const mainWindowCppPath = path.join(options.output, 'src/mainwindow.cpp');
    fs.writeFileSync(mainWindowCppPath, mainWindowCppContent);
    console.log(`   生成: src/mainwindow.cpp`);
}

// 生成窗体类文件
function generateFormClasses(mappingData) {
    for (const form of mappingData.forms) {
        generateFormHeader(form);
        generateFormSource(form);
    }
}

// 生成窗体头文件
function generateFormHeader(form) {
    const className = form.name;
    const lowerName = className.toLowerCase();
    
    const headerContent = `#ifndef ${className.toUpperCase()}_H
#define ${className.toUpperCase()}_H

#include <QWidget>

namespace Ui {
class ${className};
}

class ${className} : public QWidget
{
    Q_OBJECT

public:
    explicit ${className}(QWidget *parent = nullptr);
    ~${className}();

    // 公共方法
    void loadData();
    void saveData();
    void resetForm();

signals:
    void dataChanged();
    void formValidated(bool isValid);

public slots:
    void onFormLoad();
    void onFormSave();
    void validateForm();

private slots:
    ${form.events.map(event => `void ${event.handler}();`).join('\n    ')}

private:
    void setupUi();
    void setupConnections();
    void initializeControls();
    
    // 从WinForms属性初始化
    void initializeFromWinFormsProperties();

private:
    Ui::${className} *ui;
    
    // 控件成员变量
    ${form.controls.map(control => `QWidget *${control.name}; // WinForms类型: ${control.type}`).join('\n    ')}
    
    // 窗体状态
    bool m_isModified;
    bool m_isValid;
};

#endif // ${className.toUpperCase()}_H
`;

    const headerPath = path.join(options.output, `include/${lowerName}.h`);
    fs.writeFileSync(headerPath, headerContent);
    console.log(`   生成: include/${lowerName}.h`);
}

// 生成窗体源文件
function generateFormSource(form) {
    const className = form.name;
    const lowerName = className.toLowerCase();
    
    const sourceContent = `#include "${lowerName}.h"
#include "ui_${lowerName}.h"
#include <QMessageBox>
#include <QDebug>

${className}::${className}(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::${className})
    , m_isModified(false)
    , m_isValid(true)
{
    ui->setupUi(this);
    setupUi();
    setupConnections();
    initializeControls();
    initializeFromWinFormsProperties();
    
    // 初始化窗体状态
    resetForm();
}

${className}::~${className}()
{
    delete ui;
}

void ${className}::setupUi()
{
    // 从UI文件加载的界面已经由ui->setupUi(this)设置
    // 这里可以添加额外的UI设置
    
    // 设置窗体属性
    setWindowTitle("${className}");
    
    // 根据WinForms属性设置大小
    // 注意: WinForms使用像素，Qt使用逻辑像素，可能需要调整
}

void ${className}::setupConnections()
{
    // 连接信号和槽
    ${form.events.map(event => `
    // ${event.control}.${event.event} -> ${event.handler}
    connect(${event.control}, &${getQtSignalForEvent(event.event)}, this, &${className}::${event.handler});`).join('')}
    
    // 连接数据变化信号
    // connect(someControl, &QLineEdit::textChanged, this, [this]() { m_isModified = true; });
}

void ${className}::initializeControls()
{
    // 初始化控件
    ${form.controls.map(control => `
    // ${control.name} - ${control.type}
    // 根据WinForms属性初始化`).join('')}
}

void ${className}::initializeFromWinFormsProperties()
{
    // 根据WinForms Designer中的属性初始化控件
    ${form.controls.filter(ctrl => Object.keys(ctrl.properties).length > 0).map(control => `
    // ${control.name} 属性:
    ${Object.entries(control.properties).map(([key, value]) => `    // ${key} = ${value}`).join('\n')}`).join('\n')}
}

void ${className}::loadData()
{
    // 加载数据逻辑
    qDebug() << "Loading data for ${className}";
    m_isModified = false;
    emit dataChanged();
}

void ${className}::saveData()
{
    // 保存数据逻辑
    qDebug() << "Saving data for ${className}";
    m_isModified = false;
    
    QMessageBox::information(this, "保存", "${className} 数据已保存");
}

void ${className}::resetForm()
{
    // 重置窗体到初始状态
    qDebug() << "Resetting ${className} form";
    m_isModified = false;
    m_isValid = true;
    
    // 重置所有控件
    ${form.controls.map(control => `// ${control.name}->reset();`).join('\n    ')}
}

void ${className}::onFormLoad()
{
    loadData();
}

void ${className}::onFormSave()
{
    saveData();
}

void ${className}::validateForm()
{
    // 表单验证逻辑
    m_isValid = true;
    
    // 验证各个控件
    ${form.controls.map(control => `// validateControl(${control.name});`).join('\n    ')}
    
    emit formValidated(m_isValid);
}

// 事件处理函数
${form.events.map(event => `
void ${className}::${event.handler}()
{
    // ${event.control} 的 ${event.event} 事件处理
    qDebug() << "${event.handler}: ${event.control}.${event.event}";
    
    // TODO: 实现事件处理逻辑
    // 从WinForms迁移时需要检查事件处理代码
}`).join('\n')}
`;

    const sourcePath = path.join(options.output, `src/${lowerName}.cpp`);
    fs.writeFileSync(sourcePath, sourceContent);
    console.log(`   生成: src/${lowerName}.cpp`);
}

// 获取Qt信号对应的事件
function getQtSignalForEvent(winformsEvent) {
    const mapping = {
        'Click': 'clicked',
        'TextChanged': 'textChanged',
        'CheckedChanged': 'toggled',
        'SelectedIndexChanged': 'currentIndexChanged',
        'ValueChanged': 'valueChanged',
        'SelectionChanged': 'selectionChanged'
    };
    
    return mapping[winformsEvent] || 'triggered';
}

// 生成UI文件
function generateUiFiles(mappingData) {
    for (const form of mappingData.forms) {
        generateUiFile(form);
    }
}

// 生成单个UI文件
function generateUiFile(form) {
    const className = form.name;
    const lowerName = className.toLowerCase();
    
    const uiContent = `<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>${className}</class>
 <widget class="QWidget" name="${className}">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>${className}</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QLabel" name="titleLabel">
     <property name="text">
      <string>${className} - 从WinForms迁移</string>
     </property>
     <property name="alignment">
      <set>Qt::AlignCenter</set>
     </property>
     <property name="styleSheet">
      <string notr="true">font-size: 16px; font-weight: bold;</string>
     </property>
    </widget>
   </item>
   <item>
    <spacer name="verticalSpacer">
     <property name="orientation">
      <enum>Qt::Vertical</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>20</width>
       <height>40</height>
      </size>
     </property>
    </spacer>
   </item>
   <item>
    <widget class="QGroupBox" name="controlsGroupBox">
     <property name="title">
      <string>控件区域</string>
     </property>
     <layout class="QGridLayout" name="gridLayout">
      <!-- 这里将根据WinForms控件自动生成 -->
      <property name="leftMargin">
       <number>10</number>
      </property>
      <property name="topMargin">
       <number>10</number>
      </property>
      <property name="rightMargin">
       <number>10</number>
      </property>
      <property name="bottomMargin">
       <number>10</number>
      </property>
     </layout>
    </widget>
   </item>
   <item>
    <widget class="QGroupBox" name="actionsGroupBox">
     <property name="title">
      <string>操作</string>
     </property>
     <layout class="QHBoxLayout" name="horizontalLayout">
      <item>
       <widget class="QPushButton" name="loadButton">
        <property name="text">
         <string>加载(&L)</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="saveButton">
        <property name="text">
         <string>保存(&S)</string>
        </property>
       </widget>
      </item>
      <item>
       <widget class="QPushButton" name="resetButton">
        <property name="text">
         <string>重置(&R)</string>
        </property>
       </widget>
      </item>
      <item>
       <spacer name="horizontalSpacer">
        <property name="orientation">
         <enum>Qt::Horizontal</enum>
        </property>
        <property name="sizeHint" stdset="0">
         <size>
          <width>40</width>
          <height>20</height>
         </size>
        </property>
       </spacer>
      </item>
      <item>
       <widget class="QPushButton" name="closeButton">
        <property name="text">
         <string>关闭(&C)</string>
        </property>
       </widget>
      </item>
     </layout>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
 <!-- 控件映射注释 -->
 <!-- 
 从WinForms迁移的控件:
 ${form.controls.map(ctrl => ` ${ctrl.name}: ${ctrl.type} -> ${getQtControlType(ctrl.type)}`).join('\n ')}
 -->
</ui>`;

    const uiPath = path.join(options.output, `ui/${lowerName}.ui`);
    fs.writeFileSync(uiPath, uiContent);
    console.log(`   生成: ui/${lowerName}.ui`);
}

// 获取Qt控件类型
function getQtControlType(winformsType) {
    const typeMap = {
        'Button': 'QPushButton',
        'Label': 'QLabel',
        'TextBox': 'QLineEdit',
        'CheckBox': 'QCheckBox',
        'RadioButton': 'QRadioButton',
        'ComboBox': 'QComboBox',
        'ListBox': 'QListWidget',
        'DataGridView': 'QTableView',
        'TreeView': 'QTreeWidget',
        'TabControl': 'QTabWidget',
        'Panel': 'QFrame',
        'GroupBox': 'QGroupBox',
        'ProgressBar': 'QProgressBar',
        'TrackBar': 'QSlider',
        'NumericUpDown': 'QSpinBox',
        'DateTimePicker': 'QDateTimeEdit',
        'PictureBox': 'QLabel'
    };
    
    const shortType = winformsType.split('.').pop();
    return typeMap[shortType] || 'QWidget';
}

// 生成资源文件
function generateResourceFiles() {
    // 生成resources.qrc
    const qrcContent = `<!DOCTYPE RCC>
<RCC version="1.0">
<qresource>
    <file>icons/app_icon.png</file>
    <file>images/logo.png</file>
</qresource>
</RCC>`;

    const qrcPath = path.join(options.output, 'resources/resources.qrc');
    fs.writeFileSync(qrcPath, qrcContent);
    console.log(`   生成: resources/resources.qrc`);
    
    // 生成README.md
    const readmeContent = `# ${options.projectName}

从WinForms迁移的Qt应用程序。

## 项目结构

\`\`\`
${options.projectName}/
├── CMakeLists.txt          # 构建配置
├── src/                    # 源代码
│   ├── main.cpp           # 主程序入口
│   ├── mainwindow.cpp     # 主窗口实现
│   └── [form].cpp         # 各个窗体实现
├── include/               # 头文件
│   ├── mainwindow.h
│   └── [form].h
├── ui/                    # UI文件
│   └── [form].ui
├── resources/             # 资源文件
│   └── resources.qrc
└── build/                 # 构建目录（运行后生成）
\`\`\`

## 构建说明

### 前提条件
- CMake 3.16+
- Qt5 (Core, Widgets, Gui)
- C++17编译器

### 构建步骤
\`\`\`bash
# 创建构建目录
mkdir build && cd build

# 配置项目
cmake ..

# 编译
make -j4

# 运行
./${options.projectName}
\`\`\`

## 迁移信息

此项目是从WinForms应用程序迁移而来。迁移工具使用了自定义的WinForms到Qt映射工具。

### 迁移特点
1. 保持原有窗体结构
2. 转换事件处理为信号槽机制
3. 使用Qt布局管理器替代WinForms布局
4. 保持业务逻辑不变

### 注意事项
1. 某些WinForms控件在Qt中没有直接对应，可能需要调整
2. 事件处理逻辑可能需要手动优化
3. 布局可能需要重新设计以适应Qt的布局系统

## 开发指南

### 添加新功能
1. 在对应窗体类的头文件中声明新方法
2. 在源文件中实现方法
3. 在UI文件中添加必要的控件
4. 连接信号和槽

### 修改现有功能
1. 查看对应窗体的事件处理函数
2. 根据业务需求修改实现
3. 确保信号槽连接正确

## 许可证

此项目遵循MIT许可证。

## 支持

如有问题，请参考：
- Qt官方文档: https://doc.qt.io/
- 迁移工具文档: docs/migration_guide.md
`;

    const readmePath = path.join(options.output, 'README.md');
    fs.writeFileSync(readmePath, readmeContent);
    console.log(`   生成: README.md`);
}

// 打印生成摘要
function printGenerationSummary(mappingData) {
    console.log('');
    console.log('=== 生成摘要 ===');
    console.log(`项目名称: ${options.projectName}`);
    console.log(`输出目录: ${path.resolve(options.output)}`);
    console.log(`生成文件:`);
    console.log(`  • CMakeLists.txt - 构建配置`);
    console.log(`  • src/main.cpp - 主程序入口`);
    console.log(`  • src/mainwindow.cpp - 主窗口实现`);
    console.log(`  • include/mainwindow.h - 主窗口头文件`);
    console.log(`  • ${mappingData.forms.length} 个窗体类文件`);
    console.log(`  • ${mappingData.forms.length} 个UI文件`);
    console.log(`  • resources/resources.qrc - 资源文件`);
    console.log(`  • README.md - 项目说明`);
    
    console.log('');
    console.log('迁移统计:');
    console.log(`  窗体数量: ${mappingData.forms.length}`);
    console.log(`  控件总数: ${mappingData.summary.totalControls}`);
    console.log(`  事件总数: ${mappingData.summary.totalEvents}`);
    
    if (mappingData.recommendations) {
        console.log('');
        console.log('迁移建议:');
        console.log(`  简单迁移控件: ${mappingData.recommendations.easyMigration.length}`);
        console.log(`  中等难度控件: ${mappingData.recommendations.moderateMigration.length}`);
        console.log(`  复杂迁移控件: ${mappingData.recommendations.complexMigration.length}`);
        
        if (mappingData.recommendations.thirdPartyControls.length > 0) {
            console.log('');
            console.log('⚠ 需要特别注意的第三方控件:');
            mappingData.recommendations.thirdPartyControls.forEach(ctrl => {
                console.log(`  • ${ctrl.control} (${ctrl.type})`);
            });
        }
    }
}

// 打印帮助信息
function printHelp() {
    console.log(`
Qt代码生成工具
用法: node generate_qt_code.js [选项]

选项:
  -m, --mapping <文件>    WinForms分析报告文件 (必需)
  -o, --output <目录>     输出目录 (默认: ./qt_output)
  -n, --name <名称>       项目名称 (默认: QtMigratedApp)
  -t, --template <模板>   模板类型 (默认: basic-qt-widgets)
  -v, --verbose          详细输出模式
  -h, --help            显示此帮助信息

示例:
  node generate_qt_code.js --mapping winforms_analysis.json --output ./QtProject
  node generate_qt_code.js -m analysis.json -n MyApp -o ./output -v

支持的模板:
  • basic-qt-widgets: 基础Qt Widgets应用程序
  • qt-quick: Qt Quick应用程序 (未来支持)
  • modern-ui: 现代UI风格应用程序 (未来支持)
`);
}

// 运行生成
generateQtCode();