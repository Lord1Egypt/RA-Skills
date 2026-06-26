#!/usr/bin/env node

/**
 * WinForms到Qt映射工具示例
 * 展示如何使用分析工具和代码生成工具
 */

const fs = require('fs');
const path = require('path');

console.log('=== WinForms到Qt映射工具示例 ===');
console.log('');

// 示例1: 创建示例WinForms分析数据
console.log('1. 创建示例WinForms分析数据...');
const exampleData = createExampleWinFormsData();
const exampleFile = 'example_winforms_analysis.json';
fs.writeFileSync(exampleFile, JSON.stringify(exampleData, null, 2));
console.log(`   示例数据已保存到: ${exampleFile}`);

// 示例2: 显示分析结果
console.log('');
console.log('2. 分析结果摘要:');
printExampleSummary(exampleData);

// 示例3: 生成Qt代码
console.log('');
console.log('3. 生成Qt项目结构...');
generateExampleQtProject(exampleData);

// 示例4: 显示使用说明
console.log('');
console.log('4. 工具使用说明:');
printUsageInstructions();

console.log('');
console.log('✅ 示例完成！');
console.log('现在您可以:');
console.log('1. 查看生成的示例文件');
console.log('2. 使用真实WinForms项目进行分析');
console.log('3. 生成完整的Qt项目');

// 创建示例WinForms数据
function createExampleWinFormsData() {
    return {
        metadata: {
            project: "ExampleWinFormsApp",
            analysisDate: new Date().toISOString(),
            toolVersion: "1.0.0"
        },
        summary: {
            totalForms: 2,
            totalControls: 8,
            totalEvents: 4
        },
        forms: [
            {
                name: "MainForm",
                baseClass: "Form",
                file: "MainForm.cs",
                designerFile: "MainForm.Designer.cs",
                controls: [
                    {
                        type: "Button",
                        name: "btnCalculate",
                        properties: {
                            Text: "\"计算\"",
                            Location: "\"10, 10\"",
                            Size: "\"75, 23\""
                        },
                        events: [
                            { name: "Click", handler: "btnCalculate_Click" }
                        ]
                    },
                    {
                        type: "TextBox",
                        name: "txtInput",
                        properties: {
                            Text: "\"\"",
                            Location: "\"10, 40\"",
                            Size: "\"100, 20\""
                        },
                        events: [
                            { name: "TextChanged", handler: "txtInput_TextChanged" }
                        ]
                    },
                    {
                        type: "Label",
                        name: "lblResult",
                        properties: {
                            Text: "\"结果:\"",
                            Location: "\"10, 70\"",
                            Size: "\"100, 20\""
                        },
                        events: []
                    },
                    {
                        type: "ComboBox",
                        name: "cmbOperation",
                        properties: {
                            Items: "new string[] {\"加法\", \"减法\", \"乘法\", \"除法\"}",
                            Location: "\"120, 40\"",
                            Size: "\"80, 20\""
                        },
                        events: [
                            { name: "SelectedIndexChanged", handler: "cmbOperation_SelectedIndexChanged" }
                        ]
                    }
                ],
                events: [
                    { control: "btnCalculate", event: "Click", handler: "btnCalculate_Click" },
                    { control: "txtInput", event: "TextChanged", handler: "txtInput_TextChanged" },
                    { control: "cmbOperation", event: "SelectedIndexChanged", handler: "cmbOperation_SelectedIndexChanged" }
                ]
            },
            {
                name: "SettingsForm",
                baseClass: "Form",
                file: "SettingsForm.cs",
                designerFile: "SettingsForm.Designer.cs",
                controls: [
                    {
                        type: "CheckBox",
                        name: "chkAutoSave",
                        properties: {
                            Text: "\"自动保存\"",
                            Location: "\"10, 10\"",
                            Checked: "true"
                        },
                        events: [
                            { name: "CheckedChanged", handler: "chkAutoSave_CheckedChanged" }
                        ]
                    },
                    {
                        type: "RadioButton",
                        name: "rbThemeLight",
                        properties: {
                            Text: "\"浅色主题\"",
                            Location: "\"10, 40\"",
                            Checked: "true"
                        },
                        events: [
                            { name: "CheckedChanged", handler: "rbThemeLight_CheckedChanged" }
                        ]
                    },
                    {
                        type: "RadioButton",
                        name: "rbThemeDark",
                        properties: {
                            Text: "\"深色主题\"",
                            Location: "\"10, 70\"",
                            Checked: "false"
                        },
                        events: [
                            { name: "CheckedChanged", handler: "rbThemeDark_CheckedChanged" }
                        ]
                    },
                    {
                        type: "TrackBar",
                        name: "trbOpacity",
                        properties: {
                            Minimum: "\"10\"",
                            Maximum: "\"100\"",
                            Value: "\"80\"",
                            Location: "\"10, 100\"",
                            Size: "\"150, 20\""
                        },
                        events: [
                            { name: "ValueChanged", handler: "trbOpacity_ValueChanged" }
                        ]
                    }
                ],
                events: [
                    { control: "chkAutoSave", event: "CheckedChanged", handler: "chkAutoSave_CheckedChanged" },
                    { control: "rbThemeLight", event: "CheckedChanged", handler: "rbThemeLight_CheckedChanged" },
                    { control: "rbThemeDark", event: "CheckedChanged", handler: "rbThemeDark_CheckedChanged" },
                    { control: "trbOpacity", event: "ValueChanged", handler: "trbOpacity_ValueChanged" }
                ]
            }
        ],
        recommendations: {
            easyMigration: [
                { form: "MainForm", control: "btnCalculate", type: "Button", qtEquivalent: "QPushButton" },
                { form: "MainForm", control: "txtInput", type: "TextBox", qtEquivalent: "QLineEdit (单行) 或 QTextEdit (多行)" },
                { form: "MainForm", control: "lblResult", type: "Label", qtEquivalent: "QLabel" },
                { form: "MainForm", control: "cmbOperation", type: "ComboBox", qtEquivalent: "QComboBox" },
                { form: "SettingsForm", control: "chkAutoSave", type: "CheckBox", qtEquivalent: "QCheckBox" },
                { form: "SettingsForm", control: "rbThemeLight", type: "RadioButton", qtEquivalent: "QRadioButton" },
                { form: "SettingsForm", control: "rbThemeDark", type: "RadioButton", qtEquivalent: "QRadioButton" },
                { form: "SettingsForm", control: "trbOpacity", type: "TrackBar", qtEquivalent: "QSlider" }
            ],
            moderateMigration: [],
            complexMigration: [],
            customControls: [],
            thirdPartyControls: []
        }
    };
}

// 打印示例摘要
function printExampleSummary(data) {
    console.log(`   项目: ${data.metadata.project}`);
    console.log(`   窗体数量: ${data.summary.totalForms}`);
    console.log(`   控件总数: ${data.summary.totalControls}`);
    console.log(`   事件总数: ${data.summary.totalEvents}`);
    
    console.log('');
    console.log('   窗体详情:');
    data.forms.forEach(form => {
        console.log(`     • ${form.name}: ${form.controls.length} 个控件, ${form.events.length} 个事件`);
    });
    
    console.log('');
    console.log('   控件类型:');
    const controlTypes = {};
    data.forms.forEach(form => {
        form.controls.forEach(ctrl => {
            const type = ctrl.type;
            controlTypes[type] = (controlTypes[type] || 0) + 1;
        });
    });
    
    Object.entries(controlTypes).forEach(([type, count]) => {
        console.log(`     • ${type}: ${count} 个`);
    });
}

// 生成示例Qt项目
function generateExampleQtProject(data) {
    const exampleDir = 'example_qt_project';
    
    // 创建目录
    if (!fs.existsSync(exampleDir)) {
        fs.mkdirSync(exampleDir, { recursive: true });
    }
    
    // 生成简单的CMakeLists.txt
    const cmakeContent = `# 示例Qt项目 - 从WinForms迁移
cmake_minimum_required(VERSION 3.16)
project(ExampleQtProject VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt5 REQUIRED COMPONENTS Core Widgets Gui)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# 生成的窗体文件
set(FORM_HEADERS
    ${data.forms.map(form => `include/${form.name.toLowerCase()}.h`).join('\n    ')}
)

set(FORM_SOURCES
    ${data.forms.map(form => `src/${form.name.toLowerCase()}.cpp`).join('\n    ')}
)

# 主程序
add_executable(ExampleQtProject
    src/main.cpp
    \${FORM_SOURCES}
    \${FORM_HEADERS}
)

target_link_libraries(ExampleQtProject
    Qt5::Core
    Qt5::Widgets
    Qt5::Gui
)

message(STATUS "从WinForms迁移的示例项目")
message(STATUS "窗体: ${data.forms.map(f => f.name).join(', ')}")
message(STATUS "控件总数: ${data.summary.totalControls}")`;
    
    fs.writeFileSync(path.join(exampleDir, 'CMakeLists.txt'), cmakeContent);
    console.log(`   生成: ${exampleDir}/CMakeLists.txt`);
    
    // 生成简单的main.cpp
    const mainCppContent = `#include <QApplication>
#include <QMainWindow>
#include <QLabel>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    QMainWindow window;
    QLabel *label = new QLabel("示例Qt项目 - 从WinForms迁移", &window);
    label->setAlignment(Qt::AlignCenter);
    
    window.setCentralWidget(label);
    window.resize(400, 300);
    window.setWindowTitle("示例Qt项目");
    window.show();
    
    return app.exec();
}`;
    
    const srcDir = path.join(exampleDir, 'src');
    if (!fs.existsSync(srcDir)) {
        fs.mkdirSync(srcDir, { recursive: true });
    }
    
    fs.writeFileSync(path.join(srcDir, 'main.cpp'), mainCppContent);
    console.log(`   生成: ${exampleDir}/src/main.cpp`);
    
    // 生成简单的窗体头文件示例
    data.forms.forEach(form => {
        const headerContent = `#ifndef ${form.name.toUpperCase()}_H
#define ${form.name.toUpperCase()}_H

#include <QWidget>

class ${form.name} : public QWidget
{
    Q_OBJECT

public:
    explicit ${form.name}(QWidget *parent = nullptr);
    
signals:
    void formLoaded();
    
public slots:
    void loadForm();
    
private:
    void setupControls();
};

#endif // ${form.name.toUpperCase()}_H`;
        
        const includeDir = path.join(exampleDir, 'include');
        if (!fs.existsSync(includeDir)) {
            fs.mkdirSync(includeDir, { recursive: true });
        }
        
        fs.writeFileSync(path.join(includeDir, `${form.name.toLowerCase()}.h`), headerContent);
        console.log(`   生成: ${exampleDir}/include/${form.name.toLowerCase()}.h`);
    });
    
    console.log(`   示例项目已生成到: ${exampleDir}`);
}

// 打印使用说明
function printUsageInstructions() {
    console.log(`
实际使用步骤:
1. 分析WinForms项目:
   node scripts/analyze_winforms.js --project <WinForms项目路径> --output analysis.json

2. 生成Qt项目:
   node scripts/generate_qt_code.js --mapping analysis.json --output ./QtProject --name MyQtApp

3. 构建和运行:
   cd ./QtProject
   mkdir build && cd build
   cmake .. && make
   ./MyQtApp

4. 手动完善:
   • 检查生成的代码
   • 实现业务逻辑
   • 优化UI布局
   • 添加测试
`);
}

console.log('');
console.log('=== 工具文件结构 ===');
console.log(`
winforms-to-qt-mapper/
├── SKILL.md                    # 主文档
├── scripts/
│   ├── analyze_winforms.js     # WinForms分析工具
│   └── generate_qt_code.js     # Qt代码生成工具
├── references/
│   └── control_mapping.md      # 控件映射参考
└── examples/
    └── simple_example.js       # 使用示例
`);