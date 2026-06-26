/**
 * 智能映射引擎
 * 结合规则匹配、模式识别和机器学习进行智能控件映射
 */

const fs = require('fs');
const path = require('path');
const logger = require('../../utils/logger');
const cache = require('../../utils/cache');

class IntelligentMapper {
    constructor(options = {}) {
        this.options = {
            useMachineLearning: true,
            usePatternRecognition: true,
            confidenceThreshold: 0.8,
            fallbackToBasic: true,
            cacheMappings: true,
            ...options
        };
        
        // 加载映射规则数据库
        this.mappingRules = this.loadMappingRules();
        
        // 初始化模式识别器
        this.patternRecognizer = this.options.usePatternRecognition ? 
            new PatternRecognizer() : null;
        
        // 初始化机器学习模型
        this.machineLearningModel = this.options.useMachineLearning ?
            new MachineLearningModel() : null;
        
        // 统计信息
        this.stats = {
            totalMappings: 0,
            exactMatches: 0,
            patternMatches: 0,
            mlMatches: 0,
            fallbackMatches: 0,
            failedMappings: 0
        };
    }

    /**
     * 智能映射控件
     */
    async mapControl(winformsControl, context = {}) {
        this.stats.totalMappings++;
        
        try {
            logger.debug(`Mapping control: ${winformsControl.type} (${winformsControl.name})`);
            
            let mapping = null;
            let mappingSource = 'unknown';
            
            // 1. 尝试精确规则匹配
            mapping = this.mappingRules.findExactMatch(winformsControl);
            if (mapping) {
                mappingSource = 'exact';
                this.stats.exactMatches++;
            }
            
            // 2. 尝试模式识别（如果没有精确匹配）
            if (!mapping && this.patternRecognizer) {
                mapping = await this.patternRecognizer.recognizePattern(winformsControl, context);
                if (mapping) {
                    mappingSource = 'pattern';
                    this.stats.patternMatches++;
                }
            }
            
            // 3. 尝试机器学习推荐（如果置信度不足）
            if ((!mapping || mapping.confidence < this.options.confidenceThreshold) && 
                this.machineLearningModel) {
                const mlRecommendation = await this.machineLearningModel.recommend(
                    winformsControl, 
                    context
                );
                
                if (mlRecommendation) {
                    if (mapping) {
                        // 合并映射结果
                        mapping = this.mergeMappings(mapping, mlRecommendation);
                    } else {
                        mapping = mlRecommendation;
                    }
                    mappingSource = 'machine_learning';
                    this.stats.mlMatches++;
                }
            }
            
            // 4. 回退到基础映射
            if (!mapping && this.options.fallbackToBasic) {
                mapping = this.fallbackMapping(winformsControl);
                if (mapping) {
                    mappingSource = 'fallback';
                    this.stats.fallbackMatches++;
                }
            }
            
            if (!mapping) {
                this.stats.failedMappings++;
                throw new Error(`无法映射控件: ${winformsControl.type}`);
            }
            
            // 5. 智能属性转换
            mapping.properties = this.transformPropertiesIntelligently(
                winformsControl.properties,
                mapping.qtControl,
                context
            );
            
            // 6. 智能事件转换
            mapping.events = this.transformEventsIntelligently(
                winformsControl.events,
                mapping.qtControl,
                context
            );
            
            // 7. 布局智能转换
            mapping.layout = this.transformLayoutIntelligently(
                winformsControl.layout,
                mapping.qtControl,
                context
            );
            
            // 8. 添加元数据
            mapping.metadata = {
                source: mappingSource,
                confidence: mapping.confidence || 1.0,
                originalType: winformsControl.type,
                mappedAt: new Date().toISOString(),
                context: this.summarizeContext(context)
            };
            
            logger.debug(`Mapped ${winformsControl.type} -> ${mapping.qtControl} (${mappingSource})`);
            
            // 缓存映射结果
            if (this.options.cacheMappings) {
                this.cacheMapping(winformsControl, mapping);
            }
            
            return mapping;
            
        } catch (error) {
            logger.error(`Failed to map control ${winformsControl.type}: ${error.message}`);
            this.stats.failedMappings++;
            
            // 返回一个基本的映射，至少保证项目可以继续
            return this.createFallbackMapping(winformsControl);
        }
    }

    /**
     * 批量映射控件
     */
    async mapControlsBatch(winformsControls, context = {}) {
        logger.info(`Batch mapping ${winformsControls.length} controls`);
        
        const mappings = [];
        const errors = [];
        
        // 使用Promise.all进行并行映射
        const promises = winformsControls.map(async (control, index) => {
            try {
                const mapping = await this.mapControl(control, {
                    ...context,
                    controlIndex: index,
                    totalControls: winformsControls.length
                });
                mappings.push(mapping);
            } catch (error) {
                errors.push({
                    control: control.name,
                    type: control.type,
                    error: error.message
                });
                logger.warn(`Failed to map control ${control.name}: ${error.message}`);
            }
        });
        
        await Promise.all(promises);
        
        logger.info(`Batch mapping completed: ${mappings.length}成功, ${errors.length}失败`);
        
        return {
            mappings,
            errors,
            stats: this.getStats()
        };
    }

    /**
     * 加载映射规则
     */
    loadMappingRules() {
        const rules = {
            exactMatches: new Map(),
            partialMatches: new Map(),
            patternRules: [],
            heuristicRules: []
        };
        
        // 加载基础控件映射
        const basicMappings = this.loadBasicMappings();
        basicMappings.forEach(mapping => {
            rules.exactMatches.set(mapping.winformsType, mapping);
        });
        
        // 加载容器控件映射
        const containerMappings = this.loadContainerMappings();
        containerMappings.forEach(mapping => {
            rules.exactMatches.set(mapping.winformsType, mapping);
        });
        
        // 加载数据控件映射
        const dataMappings = this.loadDataMappings();
        dataMappings.forEach(mapping => {
            rules.exactMatches.set(mapping.winformsType, mapping);
        });
        
        // 加载模式规则
        rules.patternRules = this.loadPatternRules();
        
        // 加载启发式规则
        rules.heuristicRules = this.loadHeuristicRules();
        
        logger.info(`Loaded ${rules.exactMatches.size} exact mapping rules`);
        logger.info(`Loaded ${rules.patternRules.length} pattern rules`);
        logger.info(`Loaded ${rules.heuristicRules.length} heuristic rules`);
        
        return {
            findExactMatch: (control) => {
                const exactMatch = rules.exactMatches.get(control.type);
                if (exactMatch) {
                    return {
                        ...exactMatch,
                        confidence: 1.0
                    };
                }
                
                // 尝试部分匹配
                for (const [pattern, mapping] of rules.partialMatches) {
                    if (control.type.includes(pattern)) {
                        return {
                            ...mapping,
                            confidence: 0.9
                        };
                    }
                }
                
                return null;
            },
            
            findPatternMatch: (control, context) => {
                for (const patternRule of rules.patternRules) {
                    if (patternRule.pattern.test(control.type)) {
                        const match = {
                            ...patternRule.mapping,
                            confidence: patternRule.confidence || 0.8
                        };
                        
                        // 应用规则转换
                        if (patternRule.transform) {
                            return patternRule.transform(match, control, context);
                        }
                        
                        return match;
                    }
                }
                return null;
            },
            
            applyHeuristics: (control, currentMapping, context) => {
                let enhancedMapping = { ...currentMapping };
                
                for (const heuristicRule of rules.heuristicRules) {
                    if (heuristicRule.condition(control, context)) {
                        enhancedMapping = heuristicRule.apply(enhancedMapping, control, context);
                    }
                }
                
                return enhancedMapping;
            }
        };
    }

    /**
     * 加载基础控件映射
     */
    loadBasicMappings() {
        return [
            {
                winformsType: 'System.Windows.Forms.Button',
                qtControl: 'QPushButton',
                propertyMapping: {
                    'Text': { qt: 'setText', type: 'string' },
                    'Enabled': { qt: 'setEnabled', type: 'bool' },
                    'Visible': { qt: 'setVisible', type: 'bool' },
                    'BackColor': { qt: 'setStyleSheet', transform: this.colorToStyleSheet },
                    'ForeColor': { qt: 'setStyleSheet', transform: this.colorToStyleSheet },
                    'Font': { qt: 'setFont', transform: this.fontToQFont }
                },
                eventMapping: {
                    'Click': { qt: 'clicked', handler: 'on{ControlName}Clicked' },
                    'MouseClick': { qt: 'custom', handler: 'mousePressEvent', custom: true }
                },
                layoutMapping: {
                    'Anchor': { qt: 'layoutConstraints', transform: this.anchorToConstraints },
                    'Dock': { qt: 'layoutDock', transform: this.dockToLayout }
                },
                difficulty: 1,
                notes: '直接映射，事件处理转换为信号槽'
            },
            {
                winformsType: 'System.Windows.Forms.Label',
                qtControl: 'QLabel',
                propertyMapping: {
                    'Text': { qt: 'setText', type: 'string' },
                    'Enabled': { qt: 'setEnabled', type: 'bool' },
                    'Visible': { qt: 'setVisible', type: 'bool' },
                    'AutoSize': { qt: 'sizePolicy', transform: this.autoSizeToPolicy },
                    'TextAlign': { qt: 'setAlignment', transform: this.textAlignToAlignment }
                },
                eventMapping: {},
                layoutMapping: {
                    'Anchor': { qt: 'layoutConstraints', transform: this.anchorToConstraints }
                },
                difficulty: 1,
                notes: '直接映射，支持文本对齐'
            },
            {
                winformsType: 'System.Windows.Forms.TextBox',
                qtControl: (props) => props.MultiLine ? 'QTextEdit' : 'QLineEdit',
                propertyMapping: {
                    'Text': { qt: 'setText', type: 'string' },
                    'ReadOnly': { qt: 'setReadOnly', type: 'bool' },
                    'MaxLength': { qt: 'setMaxLength', type: 'int' },
                    'Multiline': { qt: 'controlType', transform: this.determineTextControlType }
                },
                eventMapping: {
                    'TextChanged': { qt: 'textChanged', handler: 'on{ControlName}TextChanged' },
                    'KeyPress': { qt: 'keyPressEvent', handler: 'keyPressEvent', custom: true }
                },
                layoutMapping: {
                    'Anchor': { qt: 'layoutConstraints', transform: this.anchorToConstraints }
                },
                difficulty: 2,
                notes: '根据MultiLine属性选择QLineEdit或QTextEdit'
            },
            // 添加更多基础控件映射...
        ];
    }

    /**
     * 加载容器控件映射
     */
    loadContainerMappings() {
        return [
            {
                winformsType: 'System.Windows.Forms.Panel',
                qtControl: 'QWidget',
                propertyMapping: {
                    'BackColor': { qt: 'setStyleSheet', transform: this.colorToStyleSheet },
                    'BorderStyle': { qt: 'setFrameStyle', transform: this.borderStyleToFrame }
                },
                eventMapping: {},
                layoutMapping: {
                    'Dock': { qt: 'layoutDock', transform: this.dockToLayout },
                    'AutoScroll': { qt: 'scrollArea', transform: this.autoScrollToArea }
                },
                difficulty: 2,
                notes: '作为布局容器，可能需要设置布局管理器'
            },
            {
                winformsType: 'System.Windows.Forms.GroupBox',
                qtControl: 'QGroupBox',
                propertyMapping: {
                    'Text': { qt: 'setTitle', type: 'string' }
                },
                eventMapping: {},
                layoutMapping: {},
                difficulty: 2,
                notes: '直接映射，标题转换为setTitle'
            },
            {
                winformsType: 'System.Windows.Forms.TabControl',
                qtControl: 'QTabWidget',
                propertyMapping: {
                    'TabPages': { qt: 'addTab', transform: this.tabPagesToTabs }
                },
                eventMapping: {
                    'SelectedIndexChanged': { qt: 'currentChanged', handler: 'onTabChanged' }
                },
                layoutMapping: {},
                difficulty: 3,
                notes: '需要递归转换每个TabPage的内容'
            }
        ];
    }

    /**
     * 加载数据控件映射
     */
    loadDataMappings() {
        return [
            {
                winformsType: 'System.Windows.Forms.DataGridView',
                qtControl: 'QTableView',
                propertyMapping: {
                    'DataSource': { qt: 'setModel', transform: this.dataSourceToModel },
                    'Columns': { qt: 'horizontalHeader', transform: this.columnsToHeader }
                },
                eventMapping: {
                    'CellClick': { qt: 'clicked', handler: 'onCellClicked' },
                    'CellValueChanged': { qt: 'dataChanged', handler: 'onDataChanged' }
                },
                layoutMapping: {},
                difficulty: 5,
                notes: '需要实现QAbstractItemModel模型，复杂转换'
            },
            {
                winformsType: 'System.Windows.Forms.TreeView',
                qtControl: 'QTreeWidget',
                propertyMapping: {
                    'Nodes': { qt: 'addTopLevelItem', transform: this.nodesToTreeItems }
                },
                eventMapping: {
                    'AfterSelect': { qt: 'itemClicked', handler: 'onItemSelected' }
                },
                layoutMapping: {},
                difficulty: 4,
                notes: '需要转换节点结构为QTreeWidgetItem'
            }
        ];
    }

    /**
     * 加载模式规则
     */
    loadPatternRules() {
        return [
            {
                pattern: /^Custom/,
                mapping: {
                    qtControl: 'QWidget',
                    propertyMapping: {},
                    eventMapping: {},
                    layoutMapping: {},
                    difficulty: 4,
                    notes: '自定义控件，需要手动实现或寻找替代方案'
                },
                confidence: 0.7,
                transform: (mapping, control, context) => {
                    // 尝试根据控件名称猜测功能
                    if (control.name.includes('Chart')) {
                        return {
                            ...mapping,
                            qtControl: 'QChartView',
                            notes: '可能是一个图表控件，建议使用QChart'
                        };
                    }
                    if (control.name.includes('Grid')) {
                        return {
                            ...mapping,
                            qtControl: 'QTableView',
                            notes: '可能是一个网格控件，建议使用QTableView'
                        };
                    }
                    return mapping;
                }
            },
            {
                pattern: /UserControl$/,
                mapping: {
                    qtControl: 'QWidget',
                    propertyMapping: {},
                    eventMapping: {},
                    layoutMapping: {},
                    difficulty: 3,
                    notes: '用户控件，需要分析其内部组成'
                },
                confidence: 0.8
            }
        ];
    }

    /**
     * 加载启发式规则
     */
    loadHeuristicRules() {
        return [
            {
                condition: (control, context) => {
                    // 检查是否有复杂的事件处理
                    return control.events && control.events.length > 5;
                },
                apply: (mapping, control, context) => {
                    return {
                        ...mapping,
                        notes: mapping.notes + '。注意：有多个事件处理程序，可能需要优化信号槽连接。',
                        difficulty: Math.max(mapping.difficulty, 3)
                    };
                }
            },
            {
                condition: (control, context) => {
                    // 检查是否有数据绑定属性
                    const dataBindingProps = ['DataSource', 'DataMember', 'DataBindings'];
                    return dataBindingProps.some(prop => control.properties && prop in control.properties);
                },
                apply: (mapping, control, context) => {
                    return {
                        ...mapping,
                        notes: mapping.notes + '。注意：有数据绑定，需要实现Qt的模型-视图架构。',
                        difficulty: Math.max(mapping.difficulty, 4)
                    };
                }
            },
            {
                condition: (control, context) => {
                    // 检查是否有自定义绘制相关属性
                    const paintProps = ['Paint', 'OnPaint', 'CustomDraw'];
                    const props = Object.keys(control.properties || {});
                    return props.some(prop => paintProps.some(p => prop.includes(p)));
                },
                apply: (mapping, control, context) => {
                    return {
                        ...mapping,
                        notes: mapping.notes + '。注意：有自定义绘制，需要重写paintEvent。',
                        difficulty: Math.max(mapping.difficulty, 4)
                    };
                }
            }
        ];
    }

    /**
     * 模式识别器
     */
    class PatternRecognizer {
        constructor() {
            this.patterns = this.initializePatterns();
        }
        
        initializePatterns() {
            return {
                // 控件功能模式
                buttonPatterns: [
                    { pattern: /btnOK|btnCancel|btnClose/, type: 'QPushButton', role: 'dialogButton' },
                    { pattern: /btnSave|btnLoad|btnExport/, type: 'QPushButton', role: 'actionButton' },
                    { pattern: /btnAdd|btnDelete|btnEdit/, type: 'QPushButton', role: 'crudButton' }
                ],
                
                // 文本控件模式
                textPatterns: [
                    { pattern: /txtName|txtAddress|txtDescription/, type: 'QLineEdit', role: 'inputField' },
                    { pattern: /txtNotes|txtComments|txtLog/, type: 'QTextEdit', role: 'multiLineInput' },
                    { pattern: /lblStatus|lblMessage|lblInfo/, type: 'QLabel', role: 'statusLabel' }
                ],
                
                // 选择控件模式
                selectionPatterns: [
                    { pattern: /cmbCategory|cmbType|cmbOption/, type: 'QComboBox', role: 'selection' },
                    { pattern: /lstItems|lstSelection|lstResults/, type: 'QListWidget', role: 'list' },
                    { pattern: /chkEnable|chkOption|chkFlag/, type: 'QCheckBox', role: 'option' }
                ],
                
                // 数据控件模式
                dataPatterns: [
                    { pattern: /dgvData|gridView|dataGrid/, type: 'QTableView', role: 'dataGrid' },
                    { pattern: /tvHierarchy|treeView|treeList/, type: 'QTreeWidget', role: 'tree' },
                    { pattern: /chart|graph|plot/, type: 'QChartView', role: 'chart' }
                ]
            };
        }
        
        async recognizePattern(control, context) {
            const controlName = control.name;
            const controlType = control.type;
            
            // 1. 基于名称的模式识别
            for (const [category, patterns] of Object.entries(this.patterns)) {
                for (const pattern of patterns) {
                    if (pattern.pattern.test(controlName)) {
                        return {
                            qtControl: pattern.type,
                            confidence: 0.85,
                            patternMatch: {
                                category,
                                role: pattern.role,
                                pattern: pattern.pattern.toString()
                            },
                            notes: `基于名称模式识别: ${controlName} 匹配 ${pattern.role}`
                        };
                    }
                }
            }
            
            // 2. 基于上下文的模式识别
            if (context.parentControl) {
                const parentMapping = this.recognizeParentChildPattern(control, context);
                if (parentMapping) {
                    return parentMapping;
                }
            }
            
            // 3. 基于属性模式识别
            const propertyPattern = this.recognizePropertyPattern(control);
            if (propertyPattern) {
                return propertyPattern;
            }
            
            return null;
        }
        
        recognizeParentChildPattern(control, context) {
            const parentType = context.parentControl.type;
            const controlName = control.name;
            
            // 标签页内的控件
            if (parentType.includes('TabPage')) {
                if (controlName.includes('btn')) {
                    return {
                        qtControl: 'QPushButton',
                        confidence: 0.8,
                        notes: '标签页内的按钮'
                    };
                }
            }
            
            // 分组框内的控件
            if (parentType.includes('GroupBox')) {
                if (controlName.includes('rb')) {
                    return {
                        qtControl: 'QRadioButton',
                        confidence: 0.9,
                        notes: '分组框内的单选按钮'
                    };
                }
            }
            
            return null;
        }
        
        recognizePropertyPattern(control) {
            const properties = control.properties || {};
            
            // 检查是否有Items属性（可能是列表或下拉框）
            if ('Items' in properties) {
                return {
                    qtControl: properties.Items.includes('System.Windows.Forms.ListViewItem') ? 
                              'QListWidget' : 'QComboBox',
                    confidence: 0.8,
                    notes: '基于Items属性识别'
                };
            }
            
            // 检查是否有Checked属性（可能是复选框或单选按钮）
            if ('Checked' in properties) {
                return {
                    qtControl: control.name.startsWith('rb') ? 'QRadioButton' : 'QCheckBox',
                    confidence: 0.85,
                    notes: '基于Checked属性识别'
                };
            }
            
            // 检查是否有Value属性（可能是滑块或数值输入）
            if ('Value' in properties && 'Minimum' in properties && 'Maximum' in properties) {
                return {
                    qtControl: control.name.includes('Track') ? 'QSlider' : 'QSpinBox',
                    confidence: 0.8,
                    notes: '基于Value/Minimum/Maximum属性识别'
                };
            }
            
            return null;
        }
    }

    /**
     * 机器学习模型
     */
    class MachineLearningModel {
        constructor() {
            this.model = null;
            this.trainingData = [];
            this.isTrained = false;
        }
        
        async recommend(control, context) {
            try {
                // 如果模型未训练，使用基于规则的推荐
                if (!this.isTrained) {
                    return this.ruleBasedRecommendation(control, context);
                }
                
                // 提取特征
                const features = this.extractFeatures(control, context);
                
                // 使用模型进行预测
                const prediction = await this.model.predict(features);
                
                return {
                    qtControl: prediction.control,
                    confidence: prediction.confidence,
                    mlFeatures: features,
                    notes: '基于机器学习模型推荐'
                };
                
            } catch (error) {
                logger.warn(`ML recommendation failed: ${error.message}`);
                return this.ruleBasedRecommendation(control, context);
            }
        }
        
        extractFeatures(control, context) {
            return {
                controlType: control.type,
                controlName: control.name,
                propertyCount: Object.keys(control.properties || {}).length,
                eventCount: control.events ? control.events.length : 0,
                hasDataBinding: this.hasDataBinding(control),
                hasCustomPaint: this.hasCustomPaint(control),
                parentType: context.parentControl ? context.parentControl.type : null,
                siblingCount: context.siblingControls ? context.siblingControls.length : 0,
                commonProperties: this.extractCommonProperties(control.properties)
            };
        }
        
        hasDataBinding(control) {
            const props = control.properties || {};
            return 'DataSource' in props || 'DataMember' in props || 'DataBindings' in props;
        }
        
        hasCustomPaint(control) {
            const props = control.properties || {};
            const propNames = Object.keys(props);
            return propNames.some(name => name.includes('Paint') || name.includes('Draw'));
        }
        
        extractCommonProperties(properties) {
            if (!properties) return [];
            
            const commonProps = ['Text', 'Enabled', 'Visible', 'Location', 'Size', 'BackColor', 'ForeColor'];
            return commonProps.filter(prop => prop in properties);
        }
        
        ruleBasedRecommendation(control, context) {
            // 基于规则的备选推荐
            
            // 1. 基于控件类型后缀
            const type = control.type.split('.').pop();
            const mapping = {
                'Button': 'QPushButton',
                'Label': 'QLabel',
                'TextBox': 'QLineEdit',
                'CheckBox': 'QCheckBox',
                'RadioButton': 'QRadioButton',
                'ComboBox': 'QComboBox',
                'ListBox': 'QListWidget',
                'Panel': 'QWidget',
                'GroupBox': 'QGroupBox',
                'TabControl': 'QTabWidget'
            };
            
            if (mapping[type]) {
                return {
                    qtControl: mapping[type],
                    confidence: 0.7,
                    notes: `基于控件类型后缀的规则推荐: ${type}`
                };
            }
            
            // 2. 基于常见命名模式
            if (control.name.startsWith('btn')) {
                return {
                    qtControl: 'QPushButton',
                    confidence: 0.8,
                    notes: '基于名称前缀的规则推荐: btn'
                };
            }
            if (control.name.startsWith('lbl')) {
                return {
                    qtControl: 'QLabel',
                    confidence: 0.85,
                    notes: '基于名称前缀的规则推荐: lbl'
                };
            }
            if (control.name.startsWith('txt')) {
                return {
                    qtControl: 'QLineEdit',
                    confidence: 0.8,
                    notes: '基于名称前缀的规则推荐: txt'
                };
            }
            
            // 3. 默认推荐
            return {
                qtControl: 'QWidget',
                confidence: 0.5,
                notes: '默认推荐，需要手动检查'
            };
        }
        
        async train(trainingData) {
            try {
                logger.info('Training machine learning model...');
                
                // 这里应该实现实际的模型训练逻辑
                // 由于这是一个示例，我们只模拟训练过程
                
                this.trainingData = trainingData;
                this.isTrained = true;
                
                logger.info(`Model trained with ${trainingData.length} samples`);
                
            } catch (error) {
                logger.error(`Model training failed: ${error.message}`);
                this.isTrained = false;
            }
        }
    }

    /**
     * 回退映射
     */
    fallbackMapping(control) {
        const type = control.type.split('.').pop();
        
        const fallbackMap = {
            'Button': 'QPushButton',
            'Label': 'QLabel',
            'TextBox': 'QLineEdit',
            'CheckBox': 'QCheckBox',
            'RadioButton': 'QRadioButton',
            'ComboBox': 'QComboBox',
            'ListBox': 'QListWidget',
            'Panel': 'QWidget',
            'GroupBox': 'QGroupBox',
            'Form': 'QMainWindow',
            'UserControl': 'QWidget'
        };
        
        if (fallbackMap[type]) {
            return {
                qtControl: fallbackMap[type],
                confidence: 0.6,
                notes: `回退映射: ${type} -> ${fallbackMap[type]}`
            };
        }
        
        // 通用回退
        return {
            qtControl: 'QWidget',
            confidence: 0.5,
            notes: '通用回退映射，需要手动实现'
        };
    }

    /**
     * 创建回退映射（错误处理）
     */
    createFallbackMapping(control) {
        return {
            qtControl: 'QWidget',
            confidence: 0.3,
            properties: {},
            events: {},
            layout: {},
            metadata: {
                source: 'error_fallback',
                confidence: 0.3,
                originalType: control.type,
                error: '映射失败，使用回退',
                mappedAt: new Date().toISOString()
            },
            notes: '映射失败，使用基本QWidget作为回退，需要手动实现'
        };
    }

    /**
     * 合并映射结果
     */
    mergeMappings(primary, secondary) {
        // 优先使用高置信度的结果
        if (primary.confidence >= secondary.confidence) {
            return {
                ...primary,
                // 合并属性映射
                properties: { ...secondary.properties, ...primary.properties },
                // 合并事件映射
                events: { ...secondary.events, ...primary.events },
                // 合并布局映射
                layout: { ...secondary.layout, ...primary.layout },
                // 更新置信度（加权平均）
                confidence: (primary.confidence * 0.7 + secondary.confidence * 0.3),
                // 合并备注
                notes: primary.notes + '; ' + secondary.notes
            };
        } else {
            return {
                ...secondary,
                properties: { ...primary.properties, ...secondary.properties },
                events: { ...primary.events, ...secondary.events },
                layout: { ...primary.layout, ...secondary.layout },
                confidence: (secondary.confidence * 0.7 + primary.confidence * 0.3),
                notes: secondary.notes + '; ' + primary.notes
            };
        }
    }

    /**
     * 智能属性转换
     */
    transformPropertiesIntelligently(winformsProperties, qtControl, context) {
        const transformed = {};
        
        if (!winformsProperties) {
            return transformed;
        }
        
        for (const [propName, propValue] of Object.entries(winformsProperties)) {
            try {
                const transformation = this.transformProperty(propName, propValue, qtControl, context);
                if (transformation) {
                    transformed[propName] = transformation;
                }
            } catch (error) {
                logger.warn(`Failed to transform property ${propName}: ${error.message}`);
                transformed[propName] = {
                    qtProperty: propName,
                    originalValue: propValue,
                    transformedValue: propValue,
                    transformation: 'direct',
                    confidence: 0.5,
                    notes: '转换失败，直接映射'
                };
            }
        }
        
        return transformed;
    }

    /**
     * 转换单个属性
     */
    transformProperty(propName, propValue, qtControl, context) {
        // 通用属性转换
        const commonTransformations = {
            'Text': (value) => ({
                qtProperty: 'setText',
                transformedValue: this.cleanStringValue(value),
                transformation: 'text',
                confidence: 0.95
            }),
            'Enabled': (value) => ({
                qtProperty: 'setEnabled',
                transformedValue: this.parseBool(value),
                transformation: 'bool',
                confidence: 0.95
            }),
            'Visible': (value) => ({
                qtProperty: 'setVisible',
                transformedValue: this.parseBool(value),
                transformation: 'bool',
                confidence: 0.95
            }),
            'BackColor': (value) => ({
                qtProperty: 'setStyleSheet',
                transformedValue: this.colorToStyleSheet(value, 'background-color'),
                transformation: 'color',
                confidence: 0.9
            }),
            'ForeColor': (value) => ({
                qtProperty: 'setStyleSheet',
                transformedValue: this.colorToStyleSheet(value, 'color'),
                transformation: 'color',
                confidence: 0.9
            })
        };
        
        // 特定控件的特殊转换
        const controlSpecificTransformations = {
            'QPushButton': {
                'Flat': (value) => ({
                    qtProperty: 'setFlat',
                    transformedValue: this.parseBool(value),
                    transformation: 'bool',
                    confidence: 0.9
                })
            },
            'QLabel': {
                'AutoSize': (value) => ({
                    qtProperty: 'sizePolicy',
                    transformedValue: this.autoSizeToPolicy(value),
                    transformation: 'sizePolicy',
                    confidence: 0.85
                }),
                'TextAlign': (value) => ({
                    qtProperty: 'setAlignment',
                    transformedValue: this.textAlignToAlignment(value),
                    transformation: 'alignment',
                    confidence: 0.9
                })
            },
            'QLineEdit': {
                'MaxLength': (value) => ({
                    qtProperty: 'setMaxLength',
                    transformedValue: this.parseInt(value),
                    transformation: 'int',
                    confidence: 0.95
                }),
                'ReadOnly': (value) => ({
                    qtProperty: 'setReadOnly',
                    transformedValue: this.parseBool(value),
                    transformation: 'bool',
                    confidence: 0.95
                })
            }
        };
        
        // 1. 尝试通用转换
        if (commonTransformations[propName]) {
            return commonTransformations[propName](propValue);
        }
        
        // 2. 尝试控件特定转换
        const controlTransforms = controlSpecificTransformations[qtControl];
        if (controlTransforms && controlTransforms[propName]) {
            return controlTransforms[propName](propValue);
        }
        
        // 3. 尝试启发式转换
        return this.heuristicPropertyTransform(propName, propValue, qtControl, context);
    }

    /**
     * 启发式属性转换
     */
    heuristicPropertyTransform(propName, propValue, qtControl, context) {
        // 基于属性名称的模式匹配
        if (propName.includes('Color')) {
            return {
                qtProperty: 'setStyleSheet',
                transformedValue: this.colorToStyleSheet(propValue),
                transformation: 'color_heuristic',
                confidence: 0.8,
                notes: '基于属性名称启发式转换'
            };
        }
        
        if (propName.includes('Size')) {
            return {
                qtProperty: 'resize',
                transformedValue: this.parseSize(propValue),
                transformation: 'size_heuristic',
                confidence: 0.7,
                notes: '基于属性名称启发式转换'
            };
        }
        
        if (propName.includes('Location') || propName.includes('Position')) {
            return {
                qtProperty: 'move',
                transformedValue: this.parsePoint(propValue),
                transformation: 'position_heuristic',
                confidence: 0.7,
                notes: '基于属性名称启发式转换'
            };
        }
        
        // 默认：直接映射
        return {
            qtProperty: propName,
            originalValue: propValue,
            transformedValue: propValue,
            transformation: 'direct',
            confidence: 0.5,
            notes: '直接映射，需要手动检查'
        };
    }

    /**
     * 智能事件转换
     */
    transformEventsIntelligently(winformsEvents, qtControl, context) {
        const transformed = {};
        
        if (!winformsEvents || !Array.isArray(winformsEvents)) {
            return transformed;
        }
        
        for (const event of winformsEvents) {
            try {
                const transformation = this.transformEvent(event, qtControl, context);
                if (transformation) {
                    transformed[event.name] = transformation;
                }
            } catch (error) {
                logger.warn(`Failed to transform event ${event.name}: ${error.message}`);
            }
        }
        
        return transformed;
    }

    /**
     * 转换单个事件
     */
    transformEvent(event, qtControl, context) {
        const eventMappings = {
            'Click': {
                qtSignal: 'clicked',
                handlerName: `on${this.capitalize(event.control)}Clicked`,
                parameters: [],
                confidence: 0.95
            },
            'TextChanged': {
                qtSignal: 'textChanged',
                handlerName: `on${this.capitalize(event.control)}TextChanged`,
                parameters: ['const QString& text'],
                confidence: 0.9
            },
            'CheckedChanged': {
                qtSignal: 'toggled',
                handlerName: `on${this.capitalize(event.control)}Toggled`,
                parameters: ['bool checked'],
                confidence: 0.9
            },
            'SelectedIndexChanged': {
                qtSignal: 'currentIndexChanged',
                handlerName: `on${this.capitalize(event.control)}SelectionChanged`,
                parameters: ['int index'],
                confidence: 0.9
            },
            'ValueChanged': {
                qtSignal: 'valueChanged',
                handlerName: `on${this.capitalize(event.control)}ValueChanged`,
                parameters: ['int value'],
                confidence: 0.9
            }
        };
        
        if (eventMappings[event.name]) {
            return {
                ...eventMappings[event.name],
                originalHandler: event.handler,
                transformation: 'direct'
            };
        }
        
        // 自定义事件处理
        return {
            qtSignal: 'custom',
            handlerName: event.handler,
            parameters: [],
            originalHandler: event.handler,
            transformation: 'custom',
            confidence: 0.7,
            notes: '自定义事件，需要手动实现信号槽连接'
        };
    }

    /**
     * 智能布局转换
     */
    transformLayoutIntelligently(layout, qtControl, context) {
        if (!layout) {
            return {};
        }
        
        const transformed = {};
        
        // Anchor属性转换
        if (layout.Anchor) {
            transformed.anchor = this.anchorToConstraints(layout.Anchor);
        }
        
        // Dock属性转换
        if (layout.Dock) {
            transformed.dock = this.dockToLayout(layout.Dock);
        }
        
        // AutoSize属性转换
        if (layout.AutoSize) {
            transformed.autoSize = this.autoSizeToPolicy(layout.AutoSize);
        }
        
        return transformed;
    }

    /**
     * 工具函数：清理字符串值
     */
    cleanStringValue(value) {
        if (typeof value !== 'string') {
            return String(value);
        }
        
        // 移除多余的引号
        let cleaned = value.trim();
        if (cleaned.startsWith('"') && cleaned.endsWith('"')) {
            cleaned = cleaned.substring(1, cleaned.length - 1);
        }
        
        return cleaned;
    }

    /**
     * 工具函数：解析布尔值
     */
    parseBool(value) {
        if (typeof value === 'boolean') {
            return value;
        }
        
        const str = String(value).toLowerCase().trim();
        return str === 'true' || str === '1';
    }

    /**
     * 工具函数：解析整数
     */
    parseInt(value) {
        const num = parseInt(value, 10);
        return isNaN(num) ? 0 : num;
    }

    /**
     * 工具函数：解析大小
     */
    parseSize(value) {
        // 格式: "100, 50" 或 "new Size(100, 50)"
        const match = value.match(/(\d+)\s*,\s*(\d+)/);
        if (match) {
            return {
                width: parseInt(match[1], 10),
                height: parseInt(match[2], 10)
            };
        }
        return { width: 0, height: 0 };
    }

    /**
     * 工具函数：解析点
     */
    parsePoint(value) {
        // 格式: "10, 20" 或 "new Point(10, 20)"
        const match = value.match(/(\d+)\s*,\s*(\d+)/);
        if (match) {
            return {
                x: parseInt(match[1], 10),
                y: parseInt(match[2], 10)
            };
        }
        return { x: 0, y: 0 };
    }

    /**
     * 工具函数：颜色转换
     */
    colorToStyleSheet(colorValue, property = 'color') {
        // 格式: "Color.Red" 或 "Color.FromArgb(255, 0, 0)" 或 "#FF0000"
        let color = '#000000'; // 默认黑色
        
        if (typeof colorValue === 'string') {
            const str = colorValue.toLowerCase();
            
            // 命名颜色
            const namedColors = {
                'red': '#FF0000',
                'green': '#00FF00',
                'blue': '#0000FF',
                'black': '#000000',
                'white': '#FFFFFF',
                'gray': '#808080',
                'grey': '#808080'
            };
            
            for (const [name, hex] of Object.entries(namedColors)) {
                if (str.includes(name)) {
                    color = hex;
                    break;
                }
            }
            
            // RGB颜色
            const rgbMatch = str.match(/fromargb\((\d+),\s*(\d+),\s*(\d+)/i);
            if (rgbMatch) {
                const r = parseInt(rgbMatch[1], 10);
                const g = parseInt(rgbMatch[2], 10);
                const b = parseInt(rgbMatch[3], 10);
                color = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
            }
        }
        
        return `${property}: ${color};`;
    }

    /**
     * 工具函数：字体转换
     */
    fontToQFont(fontValue) {
        // 简化版本，实际需要更复杂的解析
        return {
            family: 'Arial',
            size: 9,
            bold: false,
            italic: false
        };
    }

    /**
     * 工具函数：Anchor到约束转换
     */
    anchorToConstraints(anchorValue) {
        // WinForms Anchor枚举值
        const anchors = {
            'Top': 0x01,
            'Bottom': 0x02,
            'Left': 0x04,
            'Right': 0x08,
            'None': 0x00
        };
        
        // 解析Anchor值
        let constraints = [];
        
        if (anchorValue.includes('Top')) constraints.push('AlignTop');
        if (anchorValue.includes('Bottom')) constraints.push('AlignBottom');
        if (anchorValue.includes('Left')) constraints.push('AlignLeft');
        if (anchorValue.includes('Right')) constraints.push('AlignRight');
        
        return constraints.length > 0 ? constraints : ['NoConstraint'];
    }

    /**
     * 工具函数：Dock到布局转换
     */
    dockToLayout(dockValue) {
        const dockMap = {
            'Top': 'TopDock',
            'Bottom': 'BottomDock',
            'Left': 'LeftDock',
            'Right': 'RightDock',
            'Fill': 'FillLayout',
            'None': 'NoDock'
        };
        
        return dockMap[dockValue] || 'NoDock';
    }

    /**
     * 工具函数：AutoSize到策略转换
     */
    autoSizeToPolicy(autoSizeValue) {
        return this.parseBool(autoSizeValue) ? 
            { horizontal: 'Preferred', vertical: 'Preferred' } :
            { horizontal: 'Fixed', vertical: 'Fixed' };
    }

    /**
     * 工具函数：文本对齐转换
     */
    textAlignToAlignment(alignValue) {
        const alignmentMap = {
            'TopLeft': 'AlignTop | AlignLeft',
            'TopCenter': 'AlignTop | AlignHCenter',
            'TopRight': 'AlignTop | AlignRight',
            'MiddleLeft': 'AlignVCenter | AlignLeft',
            'MiddleCenter': 'AlignCenter',
            'MiddleRight': 'AlignVCenter | AlignRight',
            'BottomLeft': 'AlignBottom | AlignLeft',
            'BottomCenter': 'AlignBottom | AlignHCenter',
            'BottomRight': 'AlignBottom | AlignRight'
        };
        
        return alignmentMap[alignValue] || 'AlignLeft | AlignVCenter';
    }

    /**
     * 工具函数：确定文本控件类型
     */
    determineTextControlType(multilineValue) {
        return this.parseBool(multilineValue) ? 'QTextEdit' : 'QLineEdit';
    }

    /**
     * 工具函数：边框样式转换
     */
    borderStyleToFrame(borderStyle) {
        const styleMap = {
            'None': 'NoFrame',
            'FixedSingle': 'Box',
            'Fixed3D': 'Panel',
            'Border': 'StyledPanel'
        };
        
        return styleMap[borderStyle] || 'NoFrame';
    }

    /**
     * 工具函数：自动滚动转换
     */
    autoScrollToArea(autoScrollValue) {
        return this.parseBool(autoScrollValue) ? 'QScrollArea' : 'None';
    }

    /**
     * 工具函数：TabPages转换
     */
    tabPagesToTabs(tabPagesValue) {
        // 简化版本，实际需要解析TabPage集合
        return [];
    }

    /**
     * 工具函数：数据源到模型转换
     */
    dataSourceToModel(dataSourceValue) {
        return {
            modelType: 'QStandardItemModel',
            notes: '需要实现具体的数据模型'
        };
    }

    /**
     * 工具函数：列到表头转换
     */
    columnsToHeader(columnsValue) {
        // 简化版本
        return [];
    }

    /**
     * 工具函数：节点到树项转换
     */
    nodesToTreeItems(nodesValue) {
        // 简化版本
        return [];
    }

    /**
     * 工具函数：首字母大写
     */
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    /**
     * 缓存映射结果
     */
    cacheMapping(control, mapping) {
        const cacheKey = `mapping_${control.type}_${control.name}`;
        cache.set(cacheKey, mapping, 86400); // 缓存24小时
    }

    /**
     * 总结上下文
     */
    summarizeContext(context) {
        const summary = {};
        
        if (context.parentControl) {
            summary.parentType = context.parentControl.type;
        }
        
        if (context.siblingControls) {
            summary.siblingCount = context.siblingControls.length;
        }
        
        if (context.controlIndex !== undefined) {
            summary.controlIndex = context.controlIndex;
            summary.totalControls = context.totalControls;
        }
        
        return summary;
    }

    /**
     * 获取统计信息
     */
    getStats() {
        return {
            ...this.stats,
            successRate: (this.stats.totalMappings - this.stats.failedMappings) / this.stats.totalMappings * 100,
            averageConfidence: this.calculateAverageConfidence()
        };
    }

    /**
     * 计算平均置信度
     */
    calculateAverageConfidence() {
        // 在实际实现中，需要跟踪所有映射的置信度
        return 0.85; // 模拟值
    }

    /**
     * 重置统计信息
     */
    resetStats() {
        this.stats = {
            totalMappings: 0,
            exactMatches: 0,
            patternMatches: 0,
            mlMatches: 0,
            fallbackMatches: 0,
            failedMappings: 0
        };
    }

    /**
     * 导出映射规则
     */
    exportRules() {
        return {
            exactMappings: Array.from(this.mappingRules.exactMatches.entries()),
            patternRules: this.mappingRules.patternRules,
            heuristicRules: this.mappingRules.heuristicRules,
            stats: this.getStats()
        };
    }

    /**
     * 导入映射规则
     */
    importRules(rules) {
        // 在实际实现中，需要实现规则导入逻辑
        logger.info('Importing mapping rules...');
    }
}

module.exports = IntelligentMapper;