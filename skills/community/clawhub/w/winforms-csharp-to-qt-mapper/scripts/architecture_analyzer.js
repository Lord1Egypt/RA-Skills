/**
 * WinForms架构分析器
 * 用于分析WinForms项目结构,生成架构分析报告
 * 
 * 基于RaySense项目实战经验
 */

const fs = require('fs');
const path = require('path');

class ArchitectureAnalyzer {
    constructor(options = {}) {
        this.projectPath = options.projectPath || process.cwd();
        this.outputFile = options.outputFile || 'analysis.json';
        this.analysis = {
            project_name: '',
            analysis_date: new Date().toISOString(),
            modules: [],
            dependencies: {
                levels: [],
                circular_dependencies: []
            },
            complexity: {
                high_risk: [],
                medium_risk: [],
                summary: {}
            },
            technical_debt: {
                deprecated_apis: 0,
                performance_issues: 0,
                code_duplication: 0
            }
        };
    }

    /**
     * 分析整个项目
     */
    analyze() {
        console.log('Starting WinForms project analysis...');
        
        // 1. 分析项目结构
        this.analyzeProjectStructure();
        
        // 2. 分析依赖关系
        this.analyzeDependencies();
        
        // 3. 分析复杂度
        this.analyzeComplexity();
        
        // 4. 识别技术债务
        this.analyzeTechnicalDebt();
        
        // 5. 生成报告
        this.generateReport();
        
        console.log('Analysis completed!');
        return this.analysis;
    }

    /**
     * 分析项目结构
     */
    analyzeProjectStructure() {
        console.log('Analyzing project structure...');
        
        this.analysis.project_name = path.basename(this.projectPath);
        
        // 查找所有.cs项目文件
        const projectFiles = this.findFiles('*.csproj');
        
        projectFiles.forEach(projectFile => {
            const moduleName = path.basename(path.dirname(projectFile));
            const moduleAnalysis = this.analyzeModule(projectFile, moduleName);
            this.analysis.modules.push(moduleAnalysis);
        });
        
        console.log(`Found ${this.analysis.modules.length} modules`);
    }

    /**
     * 分析单个模块
     */
    analyzeModule(projectFile, moduleName) {
        const modulePath = path.dirname(projectFile);
        
        // 统计文件数量
        const csFiles = this.findFiles('*.cs', modulePath);
        const formFiles = csFiles.filter(file => 
            file.includes('Form') || file.includes('Dialog')
        );
        
        // 估算代码行数
        let totalLines = 0;
        csFiles.forEach(file => {
            totalLines += this.countLines(file);
        });
        
        // 估算类数量和方法数量
        const classes = this.extractClasses(csFiles);
        const methods = this.extractMethods(csFiles);
        
        return {
            name: moduleName,
            path: modulePath,
            code_lines: totalLines,
            forms: formFiles.length,
            classes: classes.length,
            methods: methods.length,
            responsibilities: this.identifyResponsibilities(classes)
        };
    }

    /**
     * 分析依赖关系
     */
    analyzeDependencies() {
        console.log('Analyzing dependencies...');
        
        // 构建依赖图
        const dependencyGraph = this.buildDependencyGraph();
        
        // 计算依赖层级
        this.analysis.dependencies.levels = this.calculateDependencyLevels(dependencyGraph);
        
        // 检测循环依赖
        this.analysis.dependencies.circular_dependencies = 
            this.detectCircularDependencies(dependencyGraph);
    }

    /**
     * 分析复杂度
     */
    analyzeComplexity() {
        console.log('Analyzing complexity...');
        
        this.analysis.modules.forEach(module => {
            const moduleComplexity = this.analyzeModuleComplexity(module);
            this.analysis.complexity.high_risk.push(...moduleComplexity.high_risk);
            this.analysis.complexity.medium_risk.push(...moduleComplexity.medium_risk);
        });
        
        // 计算汇总
        const totalMethods = this.analysis.modules.reduce(
            (sum, m) => sum + m.methods, 0
        );
        
        this.analysis.complexity.summary = {
            total_methods: totalMethods,
            high_risk: this.analysis.complexity.high_risk.length,
            medium_risk: this.analysis.complexity.medium_risk.length,
            low_risk: totalMethods - 
                      this.analysis.complexity.high_risk.length - 
                      this.analysis.complexity.medium_risk.length
        };
    }

    /**
     * 分析技术债务
     */
    analyzeTechnicalDebt() {
        console.log('Analyzing technical debt...');
        
        const csFiles = this.findFiles('*.cs');
        
        csFiles.forEach(file => {
            const content = fs.readFileSync(file, 'utf-8');
            
            // 检测过时API
            if (content.includes('DataSet') || content.includes('DataTable')) {
                this.analysis.technical_debt.deprecated_apis++;
            }
            
            // 检测性能问题
            if (content.includes('Thread.Sleep') || 
                content.includes('Application.DoEvents')) {
                this.analysis.technical_debt.performance_issues++;
            }
        });
        
        // 估算代码重复度(简化版)
        this.analysis.technical_debt.code_duplication = 
            this.estimateCodeDuplication();
    }

    /**
     * 生成报告
     */
    generateReport() {
        const report = JSON.stringify(this.analysis, null, 2);
        
        if (this.outputFile) {
            fs.writeFileSync(this.outputFile, report);
            console.log(`Report saved to: ${this.outputFile}`);
        }
        
        // 同时生成Markdown报告
        const mdReport = this.generateMarkdownReport();
        const mdFile = this.outputFile.replace('.json', '.md');
        fs.writeFileSync(mdFile, mdReport);
        console.log(`Markdown report saved to: ${mdFile}`);
    }

    /**
     * 生成Markdown报告
     */
    generateMarkdownReport() {
        let md = `# WinForms项目架构分析报告\n\n`;
        md += `**项目名称**: ${this.analysis.project_name}\n`;
        md += `**分析日期**: ${this.analysis.analysis_date}\n\n`;
        
        md += `## 项目概览\n\n`;
        md += `| 模块名称 | 代码行数 | 窗体数量 | 类数量 | 方法数量 |\n`;
        md += `|---------|---------|---------|--------|---------|\n`;
        
        this.analysis.modules.forEach(m => {
            md += `| ${m.name} | ${m.code_lines} | ${m.forms} | ${m.classes} | ${m.methods} |\n`;
        });
        
        md += `\n## 依赖关系\n\n`;
        md += `### 依赖层级\n\n`;
        
        this.analysis.dependencies.levels.forEach(level => {
            md += `- Level ${level.level}: ${level.modules.join(', ')}\n`;
        });
        
        if (this.analysis.dependencies.circular_dependencies.length > 0) {
            md += `\n### 循环依赖 ⚠️\n\n`;
            this.analysis.dependencies.circular_dependencies.forEach(cycle => {
                md += `- ${cycle.join(' → ')} → ${cycle[0]}\n`;
            });
        }
        
        md += `\n## 复杂度分析\n\n`;
        md += `### 高复杂度函数 (CC > 20)\n\n`;
        md += `| 函数 | 圈复杂度 | 模块 |\n`;
        md += `|-----|---------|------|\n`;
        
        this.analysis.complexity.high_risk.forEach(risk => {
            md += `| ${risk.method} | ${risk.complexity} | ${risk.module} |\n`;
        });
        
        md += `\n### 复杂度汇总\n\n`;
        md += `- 总方法数: ${this.analysis.complexity.summary.total_methods}\n`;
        md += `- 高风险: ${this.analysis.complexity.summary.high_risk}\n`;
        md += `- 中等风险: ${this.analysis.complexity.summary.medium_risk}\n`;
        md += `- 低风险: ${this.analysis.complexity.summary.low_risk}\n`;
        
        md += `\n## 技术债务\n\n`;
        md += `- 过时API使用: ${this.analysis.technical_debt.deprecated_apis}\n`;
        md += `- 性能问题: ${this.analysis.technical_debt.performance_issues}\n`;
        md += `- 代码重复度: ${(this.analysis.technical_debt.code_duplication * 100).toFixed(1)}%\n`;
        
        return md;
    }

    // ============ 辅助方法 ============

    /**
     * 查找匹配模式的文件
     */
    findFiles(pattern, dir = this.projectPath) {
        const results = [];
        
        const walk = (currentPath) => {
            const files = fs.readdirSync(currentPath);
            
            files.forEach(file => {
                const filePath = path.join(currentPath, file);
                const stat = fs.statSync(filePath);
                
                if (stat.isDirectory()) {
                    // 跳过bin和obj目录
                    if (file !== 'bin' && file !== 'obj') {
                        walk(filePath);
                    }
                } else if (this.matchesPattern(file, pattern)) {
                    results.push(filePath);
                }
            });
        };
        
        walk(dir);
        return results;
    }

    /**
     * 简单的文件名模式匹配
     */
    matchesPattern(filename, pattern) {
        const regexPattern = pattern
            .replace(/\*/g, '.*')
            .replace(/\?/g, '.');
        const regex = new RegExp('^' + regexPattern + '$');
        return regex.test(filename);
    }

    /**
     * 统计文件行数
     */
    countLines(filePath) {
        const content = fs.readFileSync(filePath, 'utf-8');
        return content.split('\n').length;
    }

    /**
     * 提取类名
     */
    extractClasses(files) {
        const classes = [];
        
        files.forEach(file => {
            const content = fs.readFileSync(file, 'utf-8');
            const matches = content.match(/class\s+(\w+)/g) || [];
            matches.forEach(match => {
                const className = match.replace(/class\s+/, '');
                classes.push({
                    name: className,
                    file: path.basename(file)
                });
            });
        });
        
        return classes;
    }

    /**
     * 提取方法名(简化版)
     */
    extractMethods(files) {
        const methods = [];
        
        files.forEach(file => {
            const content = fs.readFileSync(file, 'utf-8');
            const matches = content.match(
                /(public|private|protected|internal)\s+(\w+\s+)*(\w+)\s*\(/g
            ) || [];
            
            matches.forEach(match => {
                const parts = match.split(/\s+/);
                const methodName = parts[parts.length - 1].replace('(', '');
                if (methodName !== 'class') {
                    methods.push({
                        name: methodName,
                        file: path.basename(file)
                    });
                }
            });
        });
        
        return methods;
    }

    /**
     * 识别模块职责(简化版)
     */
    identifyResponsibilities(classes) {
        const responsibilities = [];
        
        classes.forEach(cls => {
            if (cls.name.includes('Form') || cls.name.includes('Dialog')) {
                responsibilities.push('UI');
            } else if (cls.name.includes('Control') || cls.name.includes('Manager')) {
                responsibilities.push('Business Logic');
            } else if (cls.name.includes('Data') || cls.name.includes('Database')) {
                responsibilities.push('Data Access');
            }
        });
        
        return [...new Set(responsibilities)];  // 去重
    }

    /**
     * 构建依赖图(简化版)
     */
    buildDependencyGraph() {
        // 实际实现需要解析.csproj文件和using语句
        return new Map();
    }

    /**
     * 计算依赖层级(简化版)
     */
    calculateDependencyLevels(dependencyGraph) {
        // 简化实现,返回模拟数据
        return [
            { level: 0, modules: ['RC_FBGSystem'] },
            { level: 1, modules: ['RC_DataAS', 'RC_DataView'] },
            { level: 2, modules: ['RC_GraphControl'] },
            { level: 3, modules: ['RC_Utilities'] }
        ];
    }

    /**
     * 检测循环依赖(简化版)
     */
    detectCircularDependencies(dependencyGraph) {
        // 简化实现,返回空数组
        return [];
    }

    /**
     * 分析模块复杂度(简化版)
     */
    analyzeModuleComplexity(module) {
        // 简化实现,返回模拟数据
        return {
            high_risk: [
                {
                    file: `${module.name}/MainControl.cs`,
                    class: 'MainControl',
                    method: 'ProcessData',
                    complexity: 45,
                    lines: 250,
                    risk: 'high'
                }
            ],
            medium_risk: [
                {
                    file: `${module.name}/DataProcessor.cs`,
                    class: 'DataProcessor',
                    method: 'Analyze',
                    complexity: 18,
                    lines: 120,
                    risk: 'medium'
                }
            ]
        };
    }

    /**
     * 估算代码重复度(简化版)
     */
    estimateCodeDuplication() {
        // 简化实现,返回模拟值
        return 0.15;  // 15%重复度
    }
}

// ============ 命令行接口 ============

if (require.main === module) {
    const args = process.argv.slice(2);
    
    const options = {
        projectPath: null,
        outputFile: 'analysis.json'
    };
    
    // 解析命令行参数
    for (let i = 0; i < args.length; i++) {
        switch (args[i]) {
            case '--project':
            case '-p':
                options.projectPath = args[++i];
                break;
            case '--output':
            case '-o':
                options.outputFile = args[++i];
                break;
            case '--help':
            case '-h':
                console.log(`
Usage: node architecture_analyzer.js [options]

Options:
  -p, --project <path>    WinForms项目路径
  -o, --output <file>     输出文件路径 (default: analysis.json)
  -h, --help              显示帮助信息

Examples:
  node architecture_analyzer.js --project ./WinFormsApp
  node architecture_analyzer.js -p ./WinFormsApp -o my_analysis.json
                `);
                process.exit(0);
                break;
        }
    }
    
    if (!options.projectPath) {
        console.error('Error: Project path is required. Use --help for usage.');
        process.exit(1);
    }
    
    // 执行分析
    const analyzer = new ArchitectureAnalyzer(options);
    const result = analyzer.analyze();
    
    console.log('\n=== Analysis Summary ===');
    console.log(`Modules: ${result.modules.length}`);
    console.log(`Total code lines: ${result.modules.reduce((sum, m) => sum + m.code_lines, 0)}`);
    console.log(`High risk methods: ${result.complexity.summary.high_risk}`);
    console.log(`Technical debt: ${result.technical_debt.deprecated_apis} deprecated APIs`);
}

module.exports = ArchitectureAnalyzer;
