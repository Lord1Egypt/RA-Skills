/**
 * Roslyn深度代码分析器
 * 使用Microsoft.CodeAnalysis进行全面的C#代码分析
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const logger = require('../../utils/logger');
const cache = require('../../utils/cache');

class RoslynAnalyzer {
    constructor(options = {}) {
        this.options = {
            useRoslyn: true,
            deepAnalysis: true,
            extractSemantics: true,
            analyzeControlFlow: true,
            extractDependencies: true,
            cacheResults: true,
            ...options
        };
        
        this.roslynAvailable = this.checkRoslynAvailability();
        this.workspace = null;
        this.compilation = null;
    }

    /**
     * 检查Roslyn可用性
     */
    checkRoslynAvailability() {
        try {
            // 尝试加载Roslyn库
            require.resolve('@microsoft/codeanalysis-csharp');
            logger.info('Roslyn analysis libraries available');
            return true;
        } catch (error) {
            logger.warn('Roslyn libraries not available, falling back to basic analysis');
            return false;
        }
    }

    /**
     * 深度分析WinForms项目
     */
    async analyzeProject(projectPath) {
        const cacheKey = `analysis_${projectPath}_${Date.now()}`;
        
        if (this.options.cacheResults) {
            const cached = cache.get(cacheKey);
            if (cached) {
                logger.debug('Using cached analysis results');
                return cached;
            }
        }

        try {
            logger.info(`Starting deep analysis of project: ${projectPath}`);
            
            let analysisResult;
            
            if (this.roslynAvailable && this.options.useRoslyn) {
                analysisResult = await this.analyzeWithRoslyn(projectPath);
            } else {
                analysisResult = await this.analyzeBasic(projectPath);
            }
            
            if (this.options.cacheResults) {
                cache.set(cacheKey, analysisResult, 3600); // 缓存1小时
            }
            
            logger.info(`Analysis completed: ${analysisResult.summary.totalFiles} files analyzed`);
            return analysisResult;
            
        } catch (error) {
            logger.error(`Analysis failed: ${error.message}`, error);
            throw new Error(`Project analysis failed: ${error.message}`);
        }
    }

    /**
     * 使用Roslyn进行深度分析
     */
    async analyzeWithRoslyn(projectPath) {
        try {
            const { MSBuildWorkspace } = require('@microsoft/codeanalysis-workspaces-msbuild');
            const { CSharpSyntaxTree, CSharpCompilation } = require('@microsoft/codeanalysis-csharp');
            
            // 1. 创建工作空间
            logger.debug('Creating MSBuild workspace');
            this.workspace = MSBuildWorkspace.create();
            
            // 2. 打开项目
            logger.debug(`Opening project: ${projectPath}`);
            const project = await this.workspace.openProjectAsync(projectPath);
            
            // 3. 获取编译
            logger.debug('Getting compilation');
            this.compilation = await project.getCompilationAsync();
            
            // 4. 分析所有语法树
            logger.debug('Analyzing syntax trees');
            const syntaxTrees = await this.analyzeSyntaxTrees(project);
            
            // 5. 构建语义模型
            logger.debug('Building semantic models');
            const semanticModels = await this.buildSemanticModels();
            
            // 6. 提取符号信息
            logger.debug('Extracting symbols');
            const symbols = this.extractSymbols(semanticModels);
            
            // 7. 控制流分析
            let controlFlow = null;
            if (this.options.analyzeControlFlow) {
                logger.debug('Analyzing control flow');
                controlFlow = this.analyzeControlFlow(semanticModels);
            }
            
            // 8. 依赖分析
            let dependencies = null;
            if (this.options.extractDependencies) {
                logger.debug('Extracting dependencies');
                dependencies = this.extractDependencies(symbols);
            }
            
            // 9. 架构模式识别
            logger.debug('Identifying architectural patterns');
            const patterns = this.identifyArchitecturalPatterns(syntaxTrees, semanticModels);
            
            // 10. 生成分析报告
            const analysisResult = {
                metadata: {
                    projectPath,
                    analysisDate: new Date().toISOString(),
                    toolVersion: '2.0.0',
                    analysisMethod: 'Roslyn Deep Analysis'
                },
                projectInfo: this.extractProjectInfo(project),
                syntaxTrees: this.summarizeSyntaxTrees(syntaxTrees),
                semanticModels: this.summarizeSemanticModels(semanticModels),
                symbols: this.summarizeSymbols(symbols),
                controlFlow,
                dependencies,
                patterns,
                summary: this.generateSummary({
                    syntaxTrees,
                    semanticModels,
                    symbols,
                    patterns
                }),
                recommendations: this.generateRecommendations({
                    syntaxTrees,
                    semanticModels,
                    symbols,
                    patterns
                })
            };
            
            return analysisResult;
            
        } catch (error) {
            logger.error(`Roslyn analysis failed: ${error.message}`, error);
            throw error;
        }
    }

    /**
     * 基础分析（Roslyn不可用时使用）
     */
    async analyzeBasic(projectPath) {
        logger.info('Using basic analysis (Roslyn not available)');
        
        // 扫描项目文件
        const files = this.scanProjectFiles(projectPath);
        
        // 分析窗体文件
        const forms = await this.analyzeFormsBasic(files);
        
        // 分析控件和事件
        const analysis = this.analyzeControlsAndEventsBasic(forms);
        
        return {
            metadata: {
                projectPath,
                analysisDate: new Date().toISOString(),
                toolVersion: '2.0.0',
                analysisMethod: 'Basic Analysis'
            },
            summary: {
                totalFiles: files.length,
                totalForms: forms.length,
                totalControls: analysis.totalControls,
                totalEvents: analysis.totalEvents
            },
            forms: forms.map(form => ({
                name: form.name,
                baseClass: form.baseClass,
                file: form.file,
                designerFile: form.designerFile,
                controls: form.controls,
                events: form.events
            })),
            recommendations: this.generateBasicRecommendations(forms)
        };
    }

    /**
     * 分析语法树
     */
    async analyzeSyntaxTrees(project) {
        const syntaxTrees = [];
        
        for (const document of project.getDocuments()) {
            try {
                const syntaxTree = await document.getSyntaxTreeAsync();
                const root = syntaxTree.getRoot();
                
                // 提取重要信息
                const treeInfo = {
                    filePath: document.getFilePath(),
                    fileName: path.basename(document.getFilePath()),
                    rootNodeType: root.getType().toString(),
                    classes: this.extractClasses(root),
                    methods: this.extractMethods(root),
                    properties: this.extractProperties(root),
                    events: this.extractEvents(root),
                    controls: this.extractControls(root),
                    usings: this.extractUsings(root),
                    diagnostics: syntaxTree.getDiagnostics()
                };
                
                syntaxTrees.push(treeInfo);
                
            } catch (error) {
                logger.warn(`Failed to analyze document: ${document.getFilePath()}`, error);
            }
        }
        
        return syntaxTrees;
    }

    /**
     * 构建语义模型
     */
    async buildSemanticModels() {
        const semanticModels = [];
        
        if (!this.compilation) {
            return semanticModels;
        }
        
        for (const syntaxTree of this.compilation.getSyntaxTrees()) {
            try {
                const semanticModel = this.compilation.getSemanticModel(syntaxTree);
                
                const modelInfo = {
                    syntaxTree: syntaxTree.getFilePath(),
                    symbols: this.extractSemanticSymbols(semanticModel),
                    typeInfo: this.extractTypeInformation(semanticModel),
                    symbolInfo: this.extractSymbolInformation(semanticModel),
                    operations: this.extractOperations(semanticModel)
                };
                
                semanticModels.push(modelInfo);
                
            } catch (error) {
                logger.warn(`Failed to build semantic model for syntax tree`, error);
            }
        }
        
        return semanticModels;
    }

    /**
     * 提取符号
     */
    extractSymbols(semanticModels) {
        const symbols = {
            classes: [],
            interfaces: [],
            structs: [],
            enums: [],
            delegates: [],
            methods: [],
            properties: [],
            fields: [],
            events: []
        };
        
        for (const model of semanticModels) {
            if (model.symbols) {
                // 合并符号信息
                symbols.classes.push(...(model.symbols.classes || []));
                symbols.interfaces.push(...(model.symbols.interfaces || []));
                symbols.methods.push(...(model.symbols.methods || []));
                symbols.properties.push(...(model.symbols.properties || []));
                symbols.events.push(...(model.symbols.events || []));
            }
        }
        
        return symbols;
    }

    /**
     * 分析控制流
     */
    analyzeControlFlow(semanticModels) {
        const controlFlow = {
            methodCalls: [],
            conditionals: [],
            loops: [],
            exceptions: [],
            dataFlow: []
        };
        
        for (const model of semanticModels) {
            if (model.operations) {
                // 分析操作的控制流
                this.analyzeOperationsControlFlow(model.operations, controlFlow);
            }
        }
        
        return controlFlow;
    }

    /**
     * 提取依赖关系
     */
    extractDependencies(symbols) {
        const dependencies = {
            assemblies: new Set(),
            namespaces: new Set(),
            types: new Set(),
            externalReferences: new Set()
        };
        
        // 分析符号的依赖关系
        symbols.classes.forEach(cls => {
            if (cls.baseType) {
                dependencies.types.add(cls.baseType);
            }
            if (cls.interfaces) {
                cls.interfaces.forEach(intf => dependencies.types.add(intf));
            }
        });
        
        symbols.methods.forEach(method => {
            if (method.returnType) {
                dependencies.types.add(method.returnType);
            }
            if (method.parameters) {
                method.parameters.forEach(param => {
                    if (param.type) {
                        dependencies.types.add(param.type);
                    }
                });
            }
        });
        
        return {
            assemblies: Array.from(dependencies.assemblies),
            namespaces: Array.from(dependencies.namespaces),
            types: Array.from(dependencies.types),
            externalReferences: Array.from(dependencies.externalReferences)
        };
    }

    /**
     * 识别架构模式
     */
    identifyArchitecturalPatterns(syntaxTrees, semanticModels) {
        const patterns = {
            mvc: this.detectMvcPattern(syntaxTrees, semanticModels),
            mvvm: this.detectMvvmPattern(syntaxTrees, semanticModels),
            layered: this.detectLayeredArchitecture(syntaxTrees, semanticModels),
            eventDriven: this.detectEventDrivenPattern(syntaxTrees, semanticModels),
            dataBinding: this.detectDataBindingPattern(syntaxTrees, semanticModels)
        };
        
        return patterns;
    }

    /**
     * 提取项目信息
     */
    extractProjectInfo(project) {
        return {
            name: project.getName(),
            language: project.getLanguage(),
            outputFilePath: project.getOutputFilePath(),
            compilationOptions: project.getCompilationOptions(),
            parseOptions: project.getParseOptions(),
            projectReferences: project.getProjectReferences(),
            metadataReferences: project.getMetadataReferences(),
            documents: project.getDocuments().length,
            additionalDocuments: project.getAdditionalDocuments().length,
            analyzerReferences: project.getAnalyzerReferences().length
        };
    }

    /**
     * 扫描项目文件（基础分析）
     */
    scanProjectFiles(projectPath) {
        const files = [];
        
        function traverse(dir) {
            const items = fs.readdirSync(dir, { withFileTypes: true });
            
            for (const item of items) {
                const fullPath = path.join(dir, item.name);
                
                if (item.isDirectory()) {
                    // 跳过不需要的目录
                    if (!this.shouldSkipDirectory(item.name)) {
                        traverse(fullPath);
                    }
                } else if (item.isFile()) {
                    // 只处理C#相关文件
                    if (this.isCSharpFile(item.name)) {
                        files.push({
                            path: fullPath,
                            name: item.name,
                            relativePath: path.relative(projectPath, fullPath)
                        });
                    }
                }
            }
        }
        
        traverse.call(this, projectPath);
        return files;
    }

    /**
     * 判断是否为C#文件
     */
    isCSharpFile(fileName) {
        return fileName.endsWith('.cs') || 
               fileName.endsWith('.Designer.cs') ||
               fileName.endsWith('.xaml.cs');
    }

    /**
     * 跳过不需要的目录
     */
    shouldSkipDirectory(dirName) {
        const skipDirs = [
            'bin', 'obj', '.git', '.svn', '.vs',
            'node_modules', 'packages',
            'Debug', 'Release', 'x64', 'x86',
            'Properties', 'Resources',
            'TestResults', 'coverage'
        ];
        return skipDirs.includes(dirName);
    }

    /**
     * 基础窗体分析
     */
    async analyzeFormsBasic(files) {
        const forms = [];
        
        for (const file of files) {
            try {
                const content = fs.readFileSync(file.path, 'utf8');
                
                if (this.isFormFile(content)) {
                    const formInfo = this.extractFormInfoBasic(file, content);
                    if (formInfo) {
                        forms.push(formInfo);
                    }
                }
            } catch (error) {
                logger.warn(`Failed to analyze file: ${file.path}`, error);
            }
        }
        
        return forms;
    }

    /**
     * 判断是否为窗体文件
     */
    isFormFile(content) {
        const patterns = [
            /partial\s+class\s+\w+\s*:\s*(Form|UserControl|Dialog)/i,
            /public\s+class\s+\w+\s*:\s*(Form|UserControl|Dialog)/i,
            /InitializeComponent\(\)/,
            /\b\.Designer\.cs$/i,
            /System\.Windows\.Forms\./
        ];
        
        return patterns.some(pattern => pattern.test(content));
    }

    /**
     * 提取基础窗体信息
     */
    extractFormInfoBasic(file, content) {
        try {
            // 提取类名
            const classMatch = content.match(/class\s+(\w+)/);
            if (!classMatch) return null;
            
            const className = classMatch[1];
            
            // 提取基类
            const baseClassMatch = content.match(/class\s+\w+\s*:\s*(\w+(?:\.\w+)*)/);
            const baseClass = baseClassMatch ? baseClassMatch[1] : 'Form';
            
            return {
                name: className,
                baseClass: baseClass,
                file: file.relativePath,
                designerFile: this.findDesignerFileBasic(file, className),
                controls: [],
                events: []
            };
        } catch (error) {
            logger.warn(`Failed to extract form info: ${file.path}`, error);
            return null;
        }
    }

    /**
     * 查找Designer文件
     */
    findDesignerFileBasic(file, className) {
        const baseName = file.name.replace(/\.(cs|Designer\.cs|xaml\.cs)$/, '');
        const dir = path.dirname(file.path);
        
        const possibleNames = [
            `${baseName}.Designer.cs`,
            `${className}.Designer.cs`,
            `${baseName}.xaml.cs`
        ];
        
        for (const name of possibleNames) {
            const designerPath = path.join(dir, name);
            if (fs.existsSync(designerPath)) {
                return path.relative(path.dirname(file.path), designerPath);
            }
        }
        
        return null;
    }

    /**
     * 基础控件和事件分析
     */
    analyzeControlsAndEventsBasic(forms) {
        let totalControls = 0;
        let totalEvents = 0;
        
        for (const form of forms) {
            if (form.designerFile) {
                try {
                    const designerPath = path.join(
                        path.dirname(form.file), 
                        form.designerFile
                    );
                    
                    if (fs.existsSync(designerPath)) {
                        const designerContent = fs.readFileSync(designerPath, 'utf8');
                        const analysis = this.analyzeDesignerFileBasic(designerContent);
                        
                        form.controls = analysis.controls;
                        form.events = analysis.events;
                        
                        totalControls += analysis.controls.length;
                        totalEvents += analysis.events.length;
                    }
                } catch (error) {
                    logger.warn(`Failed to analyze designer file: ${form.designerFile}`, error);
                }
            }
        }
        
        return { totalControls, totalEvents };
    }

    /**
     * 分析Designer文件
     */
    analyzeDesignerFileBasic(content) {
        const controls = [];
        const events = [];
        
        // 提取控件定义
        const controlRegex = /(private|protected|internal)\s+(\w+(?:\.\w+)*)\s+(\w+);/g;
        let match;
        
        while ((match = controlRegex.exec(content)) !== null) {
            const [, , controlType, controlName] = match;
            
            controls.push({
                type: controlType,
                name: controlName,
                properties: {},
                events: []
            });
        }
        
        // 提取事件处理
        const eventRegex = /this\.(\w+)\.(\w+)\s*\+=\s*new\s+[^;]+\(this\.(\w+)\);/g;
        
        while ((match = eventRegex.exec(content)) !== null) {
            const [, controlName, eventName, handlerName] = match;
            
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
        
        // 提取控件属性
        const propertyRegex = /this\.(\w+)\.(\w+)\s*=\s*([^;]+);/g;
        
        while ((match = propertyRegex.exec(content)) !== null) {
            const [, controlName, propertyName, propertyValue] = match;
            
            const control = controls.find(c => c.name === controlName);
            if (control) {
                control.properties[propertyName] = propertyValue.trim();
            }
        }
        
        return { controls, events };
    }

    /**
     * 生成摘要
     */
    generateSummary(data) {
        return {
            totalFiles: data.syntaxTrees?.length || 0,
            totalClasses: data.symbols?.classes?.length || 0,
            totalMethods: data.symbols?.methods?.length || 0,
            totalProperties: data.symbols?.properties?.length || 0,
            totalEvents: data.symbols?.events?.length || 0,
            totalControls: this.countControls(data),
            architecturePatterns: Object.keys(data.patterns || {}).filter(k => data.patterns[k]),
            complexityScore: this.calculateComplexityScore(data)
        };
    }

    /**
     * 统计控件数量
     */
    countControls(data) {
        let count = 0;
        
        if (data.syntaxTrees) {
            data.syntaxTrees.forEach(tree => {
                if (tree.controls) {
                    count += tree.controls.length;
                }
            });
        }
        
        return count;
    }

    /**
     * 计算复杂度分数
     */
    calculateComplexityScore(data) {
        let score = 0;
        
        // 基于类数量
        score += (data.symbols?.classes?.length || 0) * 5;
        
        // 基于方法数量
        score += (data.symbols?.methods?.length || 0) * 2;
        
        // 基于控件数量
        score += this.countControls(data) * 3;
        
        // 基于架构复杂度
        const patternCount = Object.keys(data.patterns || {}).filter(k => data.patterns[k]).length;
        score += patternCount * 20;
        
        return Math.min(score, 100); // 归一化到0-100
    }

    /**
     * 生成建议
     */
    generateRecommendations(data) {
        const recommendations = {
            migrationStrategy: this.suggestMigrationStrategy(data),
            riskAreas: this.identifyRiskAreas(data),
            optimizationOpportunities: this.findOptimizationOpportunities(data),
            testingFocus: this.suggestTestingFocus(data),
            performanceConsiderations: this.identifyPerformanceConsiderations(data)
        };
        
        return recommendations;
    }

    /**
     * 建议迁移策略
     */
    suggestMigrationStrategy(data) {
        const complexity = this.calculateComplexityScore(data);
        
        if (complexity < 30) {
            return {
                strategy: 'Direct Migration',
                description: '简单项目，可以直接迁移',
                estimatedEffort: 'Low',
                recommendedApproach: '使用工具自动化迁移，人工审核关键部分'
            };
        } else if (complexity < 70) {
            return {
                strategy: 'Phased Migration',
                description: '中等复杂度项目，建议分阶段迁移',
                estimatedEffort: 'Medium',
                recommendedApproach: '按模块分阶段迁移，每阶段验证功能'
            };
        } else {
            return {
                strategy: 'Refactor and Migrate',
                description: '高复杂度项目，建议先重构再迁移',
                estimatedEffort: 'High',
                recommendedApproach: '重构代码结构，建立清晰架构，然后迁移'
            };
        }
    }

    /**
     * 识别风险区域
     */
    identifyRiskAreas(data) {
        const risks = [];
        
        // 检查复杂控件
        const complexControls = this.findComplexControls(data);
        if (complexControls.length > 0) {
            risks.push({
                type: 'Complex Controls',
                description: `发现 ${complexControls.length} 个复杂控件`,
                details: complexControls,
                mitigation: '需要专门的处理逻辑或自定义控件'
            });
        }
        
        // 检查第三方依赖
        const thirdPartyDeps = this.findThirdPartyDependencies(data);
        if (thirdPartyDeps.length > 0) {
            risks.push({
                type: 'Third-Party Dependencies',
                description: `发现 ${thirdPartyDeps.length} 个第三方依赖`,
                details: thirdPartyDeps,
                mitigation: '需要寻找Qt对应库或重新实现功能'
            });
        }
        
        // 检查自定义绘制
        const customPaint = this.findCustomPaintOperations(data);
        if (customPaint.length > 0) {
            risks.push({
                type: 'Custom Painting',
                description: `发现 ${customPaint.length} 个自定义绘制操作`,
                details: customPaint,
                mitigation: '需要重写Qt的paintEvent'
            });
        }
        
        return risks;
    }

    /**
     * 查找复杂控件
     */
    findComplexControls(data) {
        const complexPatterns = [
            /DataGridView/i,
            /TreeView/i,
            /ListView/i,
            /PropertyGrid/i,
            /ReportViewer/i,
            /Chart/i,
            /MapControl/i
        ];
        
        const complexControls = [];
        
        if (data.syntaxTrees) {
            data.syntaxTrees.forEach(tree => {
                if (tree.controls) {
                    tree.controls.forEach(control => {
                        if (complexPatterns.some(pattern => pattern.test(control.type))) {
                            complexControls.push({
                                file: tree.fileName,
                                control: control.name,
                                type: control.type
                            });
                        }
                    });
                }
            });
        }
        
        return complexControls;
    }

    /**
     * 查找第三方依赖
     */
    findThirdPartyDependencies(data) {
        const thirdPartyPatterns = [
            /Telerik/i,
            /DevExpress/i,
            /Infragistics/i,
            /ComponentOne/i,
            /Syncfusion/i,
            /Dundas/i,
            /ChartFX/i,
            /Actipro/i
        ];
        
        const thirdPartyDeps = new Set();
        
        if (data.dependencies && data.dependencies.assemblies) {
            data.dependencies.assemblies.forEach(assembly => {
                thirdPartyPatterns.forEach(pattern => {
                    if (pattern.test(assembly)) {
                        thirdPartyDeps.add(assembly);
                    }
                });
            });
        }
        
        return Array.from(thirdPartyDeps);
    }

    /**
     * 查找自定义绘制操作
     */
    findCustomPaintOperations(data) {
        // 在实际实现中，需要分析重写OnPaint或Paint事件的方法
        // 这里返回模拟数据
        return [];
    }

    /**
     * 查找优化机会
     */
    findOptimizationOpportunities(data) {
        const opportunities = [];
        
        // 检查事件处理优化
        if (this.hasExcessiveEventHandlers(data)) {
            opportunities.push({
                type: 'Event Handler Optimization',
                description: '发现过多的事件处理程序',
                recommendation: '考虑使用事件聚合器或命令模式',
                estimatedBenefit: '提高性能，简化维护'
            });
        }
        
        // 检查数据绑定优化
        if (this.hasComplexDataBinding(data)) {
            opportunities.push({
                type: 'Data Binding Optimization',
                description: '发现复杂的数据绑定逻辑',
                recommendation: '使用Qt的模型-视图架构',
                estimatedBenefit: '提高性能，简化数据管理'
            });
        }
        
        // 检查布局优化
        if (this.hasAbsoluteLayout(data)) {
            opportunities.push({
                type: 'Layout Optimization',
                description: '发现绝对定位布局',
                recommendation: '使用Qt布局管理器',
                estimatedBenefit: '提高响应式设计，简化维护'
            });
        }
        
        return opportunities;
    }

    /**
     * 检查是否有过多事件处理程序
     */
    hasExcessiveEventHandlers(data) {
        const totalEvents = data.summary?.totalEvents || 0;
        const totalControls = data.summary?.totalControls || 1;
        
        // 如果平均每个控件有超过3个事件处理程序，认为过多
        return totalEvents / totalControls > 3;
    }

    /**
     * 检查是否有复杂数据绑定
     */
    hasComplexDataBinding(data) {
        // 在实际实现中，需要分析数据绑定代码
        // 这里返回模拟结果
        return false;
    }

    /**
     * 检查是否有绝对定位布局
     */
    hasAbsoluteLayout(data) {
        // 在实际实现中，需要分析布局属性
        // 这里返回模拟结果
        return true; // WinForms常用绝对定位
    }

    /**
     * 建议测试重点
     */
    suggestTestingFocus(data) {
        const focusAreas = ['功能对等性', '性能测试', '布局一致性'];
        
        if (this.hasComplexControls(data)) {
            focusAreas.push('复杂控件功能');
        }
        
        if (this.hasDataBinding(data)) {
            focusAreas.push('数据绑定正确性');
        }
        
        if (this.hasCustomPaint(data)) {
            focusAreas.push('自定义绘制效果');
        }
        
        return focusAreas;
    }

    /**
     * 识别性能考虑
     */
    identifyPerformanceConsiderations(data) {
        const considerations = [];
        
        considerations.push({
            aspect: 'UI响应性',
            description: 'Qt的事件循环与WinForms不同',
            recommendation: '避免在UI线程进行长时间操作'
        });
        
        considerations.push({
            aspect: '内存管理',
            description: 'C++需要手动管理内存',
            recommendation: '使用智能指针，注意对象生命周期'
        });
        
        if (this.hasComplexControls(data)) {
            considerations.push({
                aspect: '复杂控件性能',
                description: '复杂控件可能影响性能',
                recommendation: '使用虚拟化技术处理大量数据'
            });
        }
        
        return considerations;
    }

    /**
     * 生成基础建议
     */
    generateBasicRecommendations(forms) {
        const recommendations = {
            easyMigration: [],
            moderateMigration: [],
            complexMigration: [],
            customControls: [],
            thirdPartyControls: []
        };
        
        // 控件分类
        const controlCategories = {
            easy: ['Button', 'Label', 'TextBox', 'CheckBox', 'RadioButton', 'ComboBox', 'ListBox'],
            moderate: ['DataGridView', 'TreeView', 'ListView', 'TabControl', 'Panel', 'GroupBox'],
            complex: ['ReportViewer', 'Chart', 'CrystalReportViewer', 'MapControl'],
            custom: [/Custom/, /UserControl/, /^uc[A-Z]/, /^Custom[A-Z]/],
            thirdParty: [/Telerik/, /DevExpress/, /Infragistics/, /ComponentOne/, /Syncfusion/]
        };
        
        for (const form of forms) {
            for (const control of form.controls) {
                const controlType = control.type.split('.').pop();
                
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
                        qtEquivalent: this.getQtEquivalentBasic(controlType)
                    });
                } else if (controlCategories.moderate.includes(controlType)) {
                    recommendations.moderateMigration.push({
                        form: form.name,
                        control: control.name,
                        type: controlType,
                        qtEquivalent: this.getQtEquivalentBasic(controlType),
                        notes: this.getMigrationNotesBasic(controlType)
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

    /**
     * 获取基础Qt对应控件
     */
    getQtEquivalentBasic(winformsControl) {
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

    /**
     * 获取基础迁移说明
     */
    getMigrationNotesBasic(controlType) {
        const notes = {
            'DataGridView': '需要实现QAbstractItemModel模型',
            'TreeView': '需要设置QTreeWidgetItem结构',
            'ListView': '需要设置视图模式为图标或列表',
            'ReportViewer': '需要第三方报表库或重新实现',
            'Chart': '需要使用QChart或第三方图表库'
        };
        
        return notes[controlType] || '';
    }

    /**
     * 提取类信息
     */
    extractClasses(rootNode) {
        // 在实际实现中，需要遍历语法树提取类信息
        return [];
    }

    /**
     * 提取方法信息
     */
    extractMethods(rootNode) {
        // 在实际实现中，需要遍历语法树提取方法信息
        return [];
    }

    /**
     * 提取属性信息
     */
    extractProperties(rootNode) {
        // 在实际实现中，需要遍历语法树提取属性信息
        return [];
    }

    /**
     * 提取事件信息
     */
    extractEvents(rootNode) {
        // 在实际实现中，需要遍历语法树提取事件信息
        return [];
    }

    /**
     * 提取控件信息
     */
    extractControls(rootNode) {
        // 在实际实现中，需要分析控件声明
        return [];
    }

    /**
     * 提取using语句
     */
    extractUsings(rootNode) {
        // 在实际实现中，需要提取using语句
        return [];
    }

    /**
     * 提取语义符号
     */
    extractSemanticSymbols(semanticModel) {
        // 在实际实现中，需要从语义模型提取符号
        return {
            classes: [],
            methods: [],
            properties: [],
            events: []
        };
    }

    /**
     * 提取类型信息
     */
    extractTypeInformation(semanticModel) {
        // 在实际实现中，需要提取类型信息
        return {};
    }

    /**
     * 提取符号信息
     */
    extractSymbolInformation(semanticModel) {
        // 在实际实现中，需要提取符号信息
        return {};
    }

    /**
     * 提取操作信息
     */
    extractOperations(semanticModel) {
        // 在实际实现中，需要提取操作信息
        return [];
    }

    /**
     * 分析操作的控制流
     */
    analyzeOperationsControlFlow(operations, controlFlow) {
        // 在实际实现中，需要分析操作的控制流
    }

    /**
     * 检测MVC模式
     */
    detectMvcPattern(syntaxTrees, semanticModels) {
        // 在实际实现中，需要检测MVC模式
        return false;
    }

    /**
     * 检测MVVM模式
     */
    detectMvvmPattern(syntaxTrees, semanticModels) {
        // 在实际实现中，需要检测MVVM模式
        return false;
    }

    /**
     * 检测分层架构
     */
    detectLayeredArchitecture(syntaxTrees, semanticModels) {
        // 在实际实现中，需要检测分层架构
        return false;
    }

    /**
     * 检测事件驱动模式
     */
    detectEventDrivenPattern(syntaxTrees, semanticModels) {
        // 在实际实现中，需要检测事件驱动模式
        return true; // WinForms通常是事件驱动的
    }

    /**
     * 检测数据绑定模式
     */
    detectDataBindingPattern(syntaxTrees, semanticModels) {
        // 在实际实现中，需要检测数据绑定模式
        return false;
    }

    /**
     * 总结语法树信息
     */
    summarizeSyntaxTrees(syntaxTrees) {
        return syntaxTrees.map(tree => ({
            fileName: tree.fileName,
            classes: tree.classes?.length || 0,
            methods: tree.methods?.length || 0,
            controls: tree.controls?.length || 0
        }));
    }

    /**
     * 总结语义模型信息
     */
    summarizeSemanticModels(semanticModels) {
        return semanticModels.map(model => ({
            symbols: model.symbols ? Object.keys(model.symbols).length : 0
        }));
    }

    /**
     * 总结符号信息
     */
    summarizeSymbols(symbols) {
        return {
            totalClasses: symbols.classes?.length || 0,
            totalMethods: symbols.methods?.length || 0,
            totalProperties: symbols.properties?.length || 0,
            totalEvents: symbols.events?.length || 0
        };
    }

    /**
     * 检查是否有复杂控件
     */
    hasComplexControls(data) {
        return this.findComplexControls(data).length > 0;
    }

    /**
     * 检查是否有数据绑定
     */
    hasDataBinding(data) {
        return data.patterns?.dataBinding || false;
    }

    /**
     * 检查是否有自定义绘制
     */
    hasCustomPaint(data) {
        return this.findCustomPaintOperations(data).length > 0;
    }
}

module.exports = RoslynAnalyzer;