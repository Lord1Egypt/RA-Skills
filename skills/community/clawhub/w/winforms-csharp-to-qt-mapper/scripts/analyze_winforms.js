#!/usr/bin/env node

/**
 * WinForms项目分析工具
 * 分析WinForms项目结构，生成控件映射报告
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 命令行参数解析
const args = process.argv.slice(2);
const options = {
    project: null,
    output: 'winforms_analysis.json',
    verbose: false
};

// 解析参数
for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--project' || arg === '-p') {
        options.project = args[++i];
    } else if (arg === '--output' || arg === '-o') {
        options.output = args[++i];
    } else if (arg === '--verbose' || arg === '-v') {
        options.verbose = true;
    } else if (arg === '--help' || arg === '-h') {
        printHelp();
        process.exit(0);
    }
}

// 检查必要参数
if (!options.project) {
    console.error('错误: 必须指定项目路径');
    printHelp();
    process.exit(1);
}

// 检查项目路径是否存在
if (!fs.existsSync(options.project)) {
    console.error(`错误: 项目路径不存在: ${options.project}`);
    process.exit(1);
}

console.log('=== WinForms项目分析工具 ===');
console.log(`项目路径: ${options.project}`);
console.log(`输出文件: ${options.output}`);
console.log('');

// 主分析函数
async function analyzeWinFormsProject() {
    try {
        console.log('1. 扫描项目文件...');
        const files = scanProjectFiles(options.project);
        console.log(`   找到 ${files.length} 个文件`);

        console.log('2. 分析WinForms窗体文件...');
        const forms = analyzeForms(files);
        console.log(`   找到 ${forms.length} 个窗体`);

        console.log('3. 分析控件和事件...');
        const analysis = analyzeControlsAndEvents(forms);
        console.log(`   分析完成: ${analysis.controls} 个控件, ${analysis.events} 个事件`);

        console.log('4. 生成映射报告...');
        const report = generateReport(forms);
        
        // 保存报告
        fs.writeFileSync(options.output, JSON.stringify(report, null, 2));
        console.log(`   报告已保存到: ${options.output}`);

        // 显示摘要
        printSummary(report);

    } catch (error) {
        console.error('分析过程中出现错误:', error.message);
        if (options.verbose) {
            console.error(error.stack);
        }
        process.exit(1);
    }
}

// 扫描项目文件
function scanProjectFiles(projectPath) {
    const files = [];
    
    function scanDir(dir) {
        const items = fs.readdirSync(dir, { withFileTypes: true });
        
        for (const item of items) {
            const fullPath = path.join(dir, item.name);
            
            if (item.isDirectory()) {
                // 跳过一些目录
                if (!shouldSkipDirectory(item.name)) {
                    scanDir(fullPath);
                }
            } else if (item.isFile()) {
                // 只处理C#文件
                if (item.name.endsWith('.cs') || item.name.endsWith('.Designer.cs')) {
                    files.push({
                        path: fullPath,
                        name: item.name,
                        relativePath: path.relative(projectPath, fullPath)
                    });
                }
            }
        }
    }
    
    scanDir(projectPath);
    return files;
}

// 跳过不需要的目录
function shouldSkipDirectory(dirName) {
    const skipDirs = [
        'bin', 'obj', '.git', 'node_modules',
        'packages', 'Debug', 'Release',
        'x64', 'x86', 'Properties'
    ];
    return skipDirs.includes(dirName);
}

// 分析窗体文件
function analyzeForms(files) {
    const forms = [];
    
    for (const file of files) {
        // 查找窗体文件（包含partial class和继承自Form）
        const content = fs.readFileSync(file.path, 'utf8');
        
        if (isFormFile(content)) {
            const formInfo = extractFormInfo(file, content);
            if (formInfo) {
                forms.push(formInfo);
            }
        }
    }
    
    return forms;
}

// 判断是否为窗体文件
function isFormFile(content) {
    const patterns = [
        /partial\s+class\s+\w+\s*:\s*(Form|UserControl|Dialog)/,
        /public\s+class\s+\w+\s*:\s*(Form|UserControl|Dialog)/,
        /InitializeComponent\(\)/,
        /\b\.Designer\.cs$/i
    ];
    
    return patterns.some(pattern => pattern.test(content));
}

// 提取窗体信息
function extractFormInfo(file, content) {
    try {
        // 提取类名
        const classMatch = content.match(/class\s+(\w+)/);
        if (!classMatch) return null;
        
        const className = classMatch[1];
        
        // 提取基类
        const baseClassMatch = content.match(/class\s+\w+\s*:\s*(\w+)/);
        const baseClass = baseClassMatch ? baseClassMatch[1] : 'Form';
        
        // 查找Designer文件
        const designerFile = findDesignerFile(file, className);
        
        return {
            name: className,
            baseClass: baseClass,
            file: file.relativePath,
            designerFile: designerFile,
            controls: [],
            events: []
        };
    } catch (error) {
        if (options.verbose) {
            console.warn(`提取窗体信息失败: ${file.path}`, error.message);
        }
        return null;
    }
}

// 查找Designer文件
function findDesignerFile(file, className) {
    const baseName = file.name.replace(/\.(cs|Designer\.cs)$/, '');
    const possibleNames = [
        `${baseName}.Designer.cs`,
        `${className}.Designer.cs`
    ];
    
    const dir = path.dirname(file.path);
    for (const name of possibleNames) {
        const designerPath = path.join(dir, name);
        if (fs.existsSync(designerPath)) {
            return path.relative(options.project, designerPath);
        }
    }
    
    return null;
}

// 分析控件和事件
function analyzeControlsAndEvents(forms) {
    let totalControls = 0;
    let totalEvents = 0;
    
    for (const form of forms) {
        if (form.designerFile) {
            const designerPath = path.join(options.project, form.designerFile);
            try {
                const designerContent = fs.readFileSync(designerPath, 'utf8');
                const analysis = analyzeDesignerFile(designerContent);
                
                form.controls = analysis.controls;
                form.events = analysis.events;
                
                totalControls += analysis.controls.length;
                totalEvents += analysis.events.length;
                
                if (options.verbose) {
                    console.log(`   ${form.name}: ${analysis.controls.length} 控件, ${analysis.events.length} 事件`);
                }
            } catch (error) {
                if (options.verbose) {
                    console.warn(`分析Designer文件失败: ${form.designerFile}`, error.message);
                }
            }
        }
    }
    
    return {
        controls: totalControls,
        events: totalEvents
    };
}

// 分析Designer文件
function analyzeDesignerFile(content) {
    const controls = [];
    const events = [];
    
    // 提取控件定义（例如: private Button button1;）
    const controlRegex = /private\s+(\w+(?:\.\w+)*)\s+(\w+);/g;
    let match;
    
    while ((match = controlRegex.exec(content)) !== null) {
        const controlType = match[1];
        const controlName = match[2];
        
        controls.push({
            type: controlType,
            name: controlName,
            properties: {},
            events: []
        });
    }
    
    // 提取事件处理（例如: this.button1.Click += new System.EventHandler(this.button1_Click);）
    const eventRegex = /this\.(\w+)\.(\w+)\s*\+=\s*new\s+[^;]+\(this\.(\w+)\);/g;
    
    while ((match = eventRegex.exec(content)) !== null) {
        const controlName = match[1];
        const eventName = match[2];
        const handlerName = match[3];
        
        events.push({
            control: controlName,
            event: eventName,
            handler: handlerName
        });
        
        // 关联到对应控件
        const control = controls.find(c => c.name === controlName);
        if (control) {
            control.events.push({
                name: eventName,
                handler: handlerName
            });
        }
    }
    
    // 提取控件属性（简化版本）
    const propertyRegex = /this\.(\w+)\.(\w+)\s*=\s*([^;]+);/g;
    
    while ((match = propertyRegex.exec(content)) !== null) {
        const controlName = match[1];
        const propertyName = match[2];
        const propertyValue = match[3].trim();
        
        const control = controls.find(c => c.name === controlName);
        if (control) {
            control.properties[propertyName] = propertyValue;
        }
    }
    
    return { controls, events };
}

// 生成报告
function generateReport(forms) {
    const report = {
        metadata: {
            project: options.project,
            analysisDate: new Date().toISOString(),
            toolVersion: '1.0.0'
        },
        summary: {
            totalForms: forms.length,
            totalControls: forms.reduce((sum, form) => sum + form.controls.length, 0),
            totalEvents: forms.reduce((sum, form) => sum + form.events.length, 0)
        },
        forms: forms.map(form => ({
            name: form.name,
            baseClass: form.baseClass,
            file: form.file,
            designerFile: form.designerFile,
            controls: form.controls.map(control => ({
                type: control.type,
                name: control.name,
                properties: control.properties,
                events: control.events
            })),
            events: form.events
        })),
        recommendations: generateRecommendations(forms)
    };
    
    return report;
}

// 生成迁移建议
function generateRecommendations(forms) {
    const recommendations = {
        easyMigration: [],
        moderateMigration: [],
        complexMigration: [],
        customControls: [],
        thirdPartyControls: []
    };
    
    // 控件映射分类
    const controlCategories = {
        // 简单映射
        easy: ['Button', 'Label', 'TextBox', 'CheckBox', 'RadioButton', 'ComboBox', 'ListBox'],
        // 中等难度
        moderate: ['DataGridView', 'TreeView', 'ListView', 'TabControl', 'Panel', 'GroupBox'],
        // 复杂映射
        complex: ['ReportViewer', 'Chart', 'CrystalReportViewer', 'MapControl'],
        // 自定义控件
        custom: [/Custom/, /UserControl/, /^uc[A-Z]/, /^Custom[A-Z]/],
        // 第三方控件
        thirdParty: [/Telerik/, /DevExpress/, /Infragistics/, /ComponentOne/, /Syncfusion/]
    };
    
    for (const form of forms) {
        for (const control of form.controls) {
            const controlType = control.type.split('.').pop(); // 取短类型名
            
            // 检查第三方控件
            let isThirdParty = false;
            for (const pattern of controlCategories.thirdParty) {
                if (pattern.test(controlType)) {
                    recommendations.thirdPartyControls.push({
                        form: form.name,
                        control: control.name,
                        type: controlType
                    });
                    isThirdParty = true;
                    break;
                }
            }
            if (isThirdParty) continue;
            
            // 检查自定义控件
            let isCustom = false;
            for (const pattern of controlCategories.custom) {
                if (pattern.test(controlType)) {
                    recommendations.customControls.push({
                        form: form.name,
                        control: control.name,
                        type: controlType
                    });
                    isCustom = true;
                    break;
                }
            }
            if (isCustom) continue;
            
            // 分类标准控件
            if (controlCategories.easy.includes(controlType)) {
                recommendations.easyMigration.push({
                    form: form.name,
                    control: control.name,
                    type: controlType,
                    qtEquivalent: getQtEquivalent(controlType)
                });
            } else if (controlCategories.moderate.includes(controlType)) {
                recommendations.moderateMigration.push({
                    form: form.name,
                    control: control.name,
                    type: controlType,
                    qtEquivalent: getQtEquivalent(controlType),
                    notes: getMigrationNotes(controlType)
                });
            } else if (controlCategories.complex.includes(controlType)) {
                recommendations.complexMigration.push({
                    form: form.name,
                    control: control.name,
                    type: controlType,
                    notes: '需要特殊处理或第三方库'
                });
            } else {
                // 未知控件
                recommendations.complexMigration.push({
                    form: form.name,
                    control: control.name,
                    type: controlType,
                    notes: '未知控件类型，需要手动处理'
                });
            }
        }
    }
    
    return recommendations;
}

// 获取Qt对应控件
function getQtEquivalent(winformsControl) {
    const mapping = {
        'Button': 'QPushButton',
        'Label': 'QLabel',
        'TextBox': 'QLineEdit (单行) 或 QTextEdit (多行)',
        'CheckBox': 'QCheckBox',
        'RadioButton': 'QRadioButton',
        'ComboBox': 'QComboBox',
        'ListBox': 'QListWidget',
        'DataGridView': 'QTableView',
        'TreeView': 'QTreeWidget',
        'ListView': 'QListWidget (图标模式)',
        'TabControl': 'QTabWidget',
        'Panel': 'QWidget 或 QFrame',
        'GroupBox': 'QGroupBox',
        'Form': 'QMainWindow 或 QDialog',
        'UserControl': 'QWidget'
    };
    
    return mapping[winformsControl] || '需要自定义实现';
}

// 获取迁移说明
function getMigrationNotes(controlType) {
    const notes = {
        'DataGridView': '需要实现QAbstractItemModel模型',
        'TreeView': '需要设置QTreeWidgetItem结构',
        'ListView': '需要设置视图模式为图标或列表',
        'ReportViewer': '需要第三方报表库或重新实现',
        'Chart': '需要使用QChart或第三方图表库'
    };
    
    return notes[controlType] || '';
}

// 打印摘要
function printSummary(report) {
    console.log('');
    console.log('=== 分析摘要 ===');
    console.log(`窗体数量: ${report.summary.totalForms}`);
    console.log(`控件总数: ${report.summary.totalControls}`);
    console.log(`事件总数: ${report.summary.totalEvents}`);
    
    console.log('');
    console.log('迁移难度分类:');
    console.log(`  简单迁移: ${report.recommendations.easyMigration.length} 个控件`);
    console.log(`  中等难度: ${report.recommendations.moderateMigration.length} 个控件`);
    console.log(`  复杂迁移: ${report.recommendations.complexMigration.length} 个控件`);
    console.log(`  自定义控件: ${report.recommendations.customControls.length} 个`);
    console.log(`  第三方控件: ${report.recommendations.thirdPartyControls.length} 个`);
    
    if (report.recommendations.thirdPartyControls.length > 0) {
        console.log('');
        console.log('⚠ 发现第三方控件，需要寻找Qt对应版本或重新实现:');
        report.recommendations.thirdPartyControls.forEach(ctrl => {
            console.log(`  - ${ctrl.form}.${ctrl.control} (${ctrl.type})`);
        });
    }
}

// 打印帮助信息
function printHelp() {
    console.log(`
WinForms项目分析工具
用法: node analyze_winforms.js [选项]

选项:
  -p, --project <路径>    WinForms项目路径 (必需)
  -o, --output <文件>     输出文件路径 (默认: winforms_analysis.json)
  -v, --verbose          详细输出模式
  -h, --help            显示此帮助信息

示例:
  node analyze_winforms.js --project RC_DataAS/ --output analysis.json
  node analyze_winforms.js -p ./MyWinFormsApp -o report.json -v
`);
}

// 运行分析
analyzeWinFormsProject();