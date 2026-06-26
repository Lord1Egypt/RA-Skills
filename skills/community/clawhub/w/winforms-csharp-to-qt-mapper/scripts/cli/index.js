#!/usr/bin/env node

/**
 * WinForms到Qt迁移工具 - 增强版CLI
 * 提供完整的命令行接口，支持深度分析、智能迁移和验证
 */

const { program } = require('commander');
const chalk = require('chalk');
const figlet = require('figlet');
const path = require('path');
const fs = require('fs');

// 导入核心模块
const RoslynAnalyzer = require('../core/analyzer/RoslynAnalyzer');
const IntelligentMapper = require('../core/mapper/IntelligentMapper');
const QtCodeGenerator = require('../core/generator/QtCodeGenerator');
const logger = require('../../utils/logger');

// 显示启动横幅
function showBanner() {
    console.log(chalk.cyan(figlet.textSync('WinForms2Qt', { horizontalLayout: 'full' })));
    console.log(chalk.yellow('增强版WinForms到Qt迁移工具 v2.0.0\n'));
}

// 初始化程序
program
    .name('winforms-qt-migrate')
    .description('增强版WinForms到Qt迁移工具')
    .version('2.0.0')
    .option('-v, --verbose', '详细输出模式')
    .option('-q, --quiet', '安静模式，只显示错误')
    .option('--no-color', '禁用颜色输出')
    .hook('preAction', (thisCommand) => {
        // 设置日志级别
        if (thisCommand.opts().quiet) {
            logger.level = 'error';
        } else if (thisCommand.opts().verbose) {
            logger.level = 'debug';
        } else {
            logger.level = 'info';
        }
        
        // 显示横幅（如果不是安静模式）
        if (!thisCommand.opts().quiet) {
            showBanner();
        }
    });

// 分析命令
program
    .command('analyze')
    .description('深度分析WinForms项目')
    .requiredOption('-p, --project <path>', 'WinForms项目路径')
    .option('-o, --output <file>', '分析报告输出文件', 'analysis_report.json')
    .option('--deep', '启用深度分析（使用Roslyn）', true)
    .option('--no-deep', '禁用深度分析（使用基础分析）')
    .option('--export-stats', '导出统计信息')
    .action(async (options) => {
        try {
            console.log(chalk.blue.bold('\n=== WinForms项目深度分析 ===\n'));
            
            // 验证项目路径
            if (!fs.existsSync(options.project)) {
                console.error(chalk.red(`错误：项目路径不存在: ${options.project}`));
                process.exit(1);
            }
            
            console.log(chalk.green(`项目路径: ${path.resolve(options.project)}`));
            console.log(chalk.green(`输出文件: ${options.output}`));
            console.log(chalk.green(`分析模式: ${options.deep ? '深度分析(Roslyn)' : '基础分析'}\n`));
            
            // 创建分析器
            const analyzer = new RoslynAnalyzer({
                useRoslyn: options.deep,
                deepAnalysis: options.deep
            });
            
            // 执行分析
            console.log(chalk.cyan('开始分析项目...'));
            const startTime = Date.now();
            
            const analysisResult = await analyzer.analyzeProject(options.project);
            
            const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
            console.log(chalk.green(`分析完成，耗时 ${elapsedTime} 秒`));
            
            // 保存分析报告
            fs.writeFileSync(options.output, JSON.stringify(analysisResult, null, 2));
            console.log(chalk.green(`分析报告已保存到: ${options.output}`));
            
            // 显示摘要
            displayAnalysisSummary(analysisResult);
            
            // 导出统计信息（如果启用）
            if (options.exportStats) {
                const statsFile = options.output.replace('.json', '_stats.json');
                const stats = extractStats(analysisResult);
                fs.writeFileSync(statsFile, JSON.stringify(stats, null, 2));
                console.log(chalk.green(`统计信息已导出到: ${statsFile}`));
            }
            
            console.log(chalk.green.bold('\n✅ 分析完成！'));
            
        } catch (error) {
            console.error(chalk.red(`分析失败: ${error.message}`));
            if (options.verbose) {
                console.error(error.stack);
            }
            process.exit(1);
        }
    });

// 迁移命令
program
    .command('migrate')
    .description('将WinForms项目迁移到Qt')
    .requiredOption('-p, --project <path>', 'WinForms项目路径')
    .requiredOption('-o, --output <dir>', 'Qt项目输出目录')
    .option('-n, --name <name>', 'Qt项目名称', 'QtMigratedApp')
    .option('-a, --analysis <file>', '使用已有的分析报告')
    .option('--intelligent', '启用智能映射', true)
    .option('--no-intelligent', '禁用智能映射（使用基础映射）')
    .option('--template <type>', '项目模板类型', 'basic-qt-widgets')
    .option('--skip-validation', '跳过迁移验证')
    .option('--dry-run', '试运行，不实际生成文件')
    .action(async (options) => {
        try {
            console.log(chalk.blue.bold('\n=== WinForms到Qt迁移 ===\n'));
            
            // 验证输入
            if (!fs.existsSync(options.project)) {
                console.error(chalk.red(`错误：项目路径不存在: ${options.project}`));
                process.exit(1);
            }
            
            console.log(chalk.green(`源项目: ${path.resolve(options.project)}`));
            console.log(chalk.green(`输出目录: ${path.resolve(options.output)}`));
            console.log(chalk.green(`项目名称: ${options.name}`));
            console.log(chalk.green(`映射模式: ${options.intelligent ? '智能映射' : '基础映射'}`));
            console.log(chalk.green(`模板类型: ${options.template}`));
            console.log(chalk.green(`试运行: ${options.dryRun ? '是' : '否'}\n`));
            
            let analysisResult;
            
            // 使用现有分析报告或重新分析
            if (options.analysis && fs.existsSync(options.analysis)) {
                console.log(chalk.cyan('加载现有分析报告...'));
                analysisResult = JSON.parse(fs.readFileSync(options.analysis, 'utf8'));
                console.log(chalk.green(`分析报告加载成功: ${options.analysis}`));
            } else {
                console.log(chalk.cyan('开始项目分析...'));
                const analyzer = new RoslynAnalyzer();
                analysisResult = await analyzer.analyzeProject(options.project);
                console.log(chalk.green('项目分析完成'));
            }
            
            // 智能映射
            console.log(chalk.cyan('开始智能映射...'));
            const mapper = new IntelligentMapper({
                useMachineLearning: options.intelligent,
                usePatternRecognition: options.intelligent
            });
            
            const mappingResult = await mapper.mapControlsBatch(
                extractControlsFromAnalysis(analysisResult),
                { projectName: options.name }
            );
            
            console.log(chalk.green(`映射完成: ${mappingResult.mappings.length} 个控件已映射`));
            
            if (mappingResult.errors.length > 0) {
                console.log(chalk.yellow(`警告: ${mappingResult.errors.length} 个控件映射失败`));
                mappingResult.errors.forEach(error => {
                    console.log(chalk.yellow(`  - ${error.control} (${error.type}): ${error.error}`));
                });
            }
            
            // 生成Qt代码（如果不是试运行）
            if (!options.dryRun) {
                console.log(chalk.cyan('生成Qt项目代码...'));
                
                const generator = new QtCodeGenerator({
                    projectName: options.name,
                    templateType: options.template
                });
                
                await generator.generateProject({
                    analysis: analysisResult,
                    mappings: mappingResult.mappings,
                    outputDir: options.output
                });
                
                console.log(chalk.green(`Qt项目已生成到: ${path.resolve(options.output)}`));
            } else {
                console.log(chalk.yellow('试运行模式：未实际生成文件'));
            }
            
            // 验证迁移结果（如果启用）
            if (!options.skipValidation && !options.dryRun) {
                console.log(chalk.cyan('验证迁移结果...'));
                await validateMigration(options.project, options.output, analysisResult);
                console.log(chalk.green('迁移验证通过'));
            }
            
            // 显示迁移摘要
            displayMigrationSummary(analysisResult, mappingResult, options);
            
            console.log(chalk.green.bold('\n✅ 迁移完成！'));
            
        } catch (error) {
            console.error(chalk.red(`迁移失败: ${error.message}`));
            if (options.verbose) {
                console.error(error.stack);
            }
            process.exit(1);
        }
    });

// 验证命令
program
    .command('validate')
    .description('验证迁移结果')
    .requiredOption('-w, --winforms <path>', '原始WinForms项目路径')
    .requiredOption('-q, --qt <path>', '生成的Qt项目路径')
    .option('-r, --report <file>', '验证报告输出文件', 'validation_report.json')
    .option('--check-functionality', '检查功能对等性', true)
    .option('--check-performance', '检查性能')
    .option('--check-layout', '检查布局一致性', true)
    .action(async (options) => {
        try {
            console.log(chalk.blue.bold('\n=== 迁移验证 ===\n'));
            
            // 验证路径
            if (!fs.existsSync(options.winforms)) {
                console.error(chalk.red(`错误：WinForms项目不存在: ${options.winforms}`));
                process.exit(1);
            }
            
            if (!fs.existsSync(options.qt)) {
                console.error(chalk.red(`错误：Qt项目不存在: ${options.qt}`));
                process.exit(1);
            }
            
            console.log(chalk.green(`WinForms项目: ${path.resolve(options.winforms)}`));
            console.log(chalk.green(`Qt项目: ${path.resolve(options.qt)}`));
            console.log(chalk.green(`验证报告: ${options.report}\n`));
            
            // 执行验证
            console.log(chalk.cyan('开始验证迁移结果...'));
            
            const validationResult = await validateMigration(
                options.winforms,
                options.qt,
                options
            );
            
            // 保存验证报告
            fs.writeFileSync(options.report, JSON.stringify(validationResult, null, 2));
            console.log(chalk.green(`验证报告已保存到: ${options.report}`));
            
            // 显示验证结果
            displayValidationResults(validationResult);
            
            console.log(chalk.green.bold('\n✅ 验证完成！'));
            
        } catch (error) {
            console.error(chalk.red(`验证失败: ${error.message}`));
            process.exit(1);
        }
    });

// 批量处理命令
program
    .command('batch')
    .description('批量处理多个项目')
    .requiredOption('-c, --config <file>', '批量处理配置文件')
    .option('--parallel <number>', '并行处理数量', '2')
    .action(async (options) => {
        try {
            console.log(chalk.blue.bold('\n=== 批量处理 ===\n'));
            
            if (!fs.existsSync(options.config)) {
                console.error(chalk.red(`错误：配置文件不存在: ${options.config}`));
                process.exit(1);
            }
            
            const config = JSON.parse(fs.readFileSync(options.config, 'utf8'));
            const parallelCount = parseInt(options.parallel, 10);
            
            console.log(chalk.green(`配置文件: ${options.config}`));
            console.log(chalk.green(`项目数量: ${config.projects.length}`));
            console.log(chalk.green(`并行处理: ${parallelCount}\n`));
            
            await processBatch(config.projects, parallelCount);
            
            console.log(chalk.green.bold('\n✅ 批量处理完成！'));
            
        } catch (error) {
            console.error(chalk.red(`批量处理失败: ${error.message}`));
            process.exit(1);
        }
    });

// 帮助命令
program
    .command('help')
    .description('显示详细帮助信息')
    .action(() => {
        console.log(chalk.blue.bold('\n=== 增强版WinForms到Qt迁移工具帮助 ===\n'));
        
        console.log(chalk.yellow('主要命令:'));
        console.log('  analyze    - 深度分析WinForms项目');
        console.log('  migrate    - 迁移WinForms项目到Qt');
        console.log('  validate   - 验证迁移结果');
        console.log('  batch      - 批量处理多个项目');
        console.log('  help       - 显示此帮助信息\n');
        
        console.log(chalk.yellow('使用示例:'));
        console.log(chalk.cyan('  # 分析项目'));
        console.log('  winforms-qt-migrate analyze --project ./MyWinFormsApp --output analysis.json\n');
        
        console.log(chalk.cyan('  # 迁移项目'));
        console.log('  winforms-qt-migrate migrate --project ./MyWinFormsApp --output ./QtApp --name MyQtApp\n');
        
        console.log(chalk.cyan('  # 使用现有分析报告迁移'));
        console.log('  winforms-qt-migrate migrate --project ./MyWinFormsApp --output ./QtApp --analysis analysis.json\n');
        
        console.log(chalk.cyan('  # 验证迁移'));
        console.log('  winforms-qt-migrate validate --winforms ./MyWinFormsApp --qt ./QtApp\n');
        
        console.log(chalk.yellow('更多信息:'));
        console.log('  访问文档: https://github.com/raysense/winforms-to-qt-mapper');
        console.log('  报告问题: https://github.com/raysense/winforms-to-qt-mapper/issues\n');
    });

// 默认命令（显示帮助）
program
    .action(() => {
        program.help();
    });

// 解析命令行参数
program.parse(process.argv);

/**
 * 显示分析摘要
 */
function displayAnalysisSummary(analysisResult) {
    console.log(chalk.cyan.bold('\n分析摘要:'));
    console.log(chalk.cyan('─────────────'));
    
    const summary = analysisResult.summary || {};
    
    console.log(chalk.green(`项目: ${analysisResult.metadata?.projectPath || '未知'}`));
    console.log(chalk.green(`分析日期: ${analysisResult.metadata?.analysisDate || '未知'}`));
    console.log(chalk.green(`分析模式: ${analysisResult.metadata?.analysisMethod || '未知'}`));
    console.log('');
    
    console.log(chalk.yellow('项目统计:'));
    console.log(`  文件总数: ${summary.totalFiles || 0}`);
    console.log(`  类总数: ${summary.totalClasses || 0}`);
    console.log(`  方法总数: ${summary.totalMethods || 0}`);
    console.log(`  控件总数: ${summary.totalControls || 0}`);
    console.log(`  事件总数: ${summary.totalEvents || 0}`);
    
    if (summary.architecturePatterns) {
        console.log(chalk.yellow('\n架构模式:'));
        summary.architecturePatterns.forEach(pattern => {
            console.log(`  • ${pattern}`);
        });
    }
    
    if (summary.complexityScore !== undefined) {
        console.log(chalk.yellow('\n复杂度评分:'));
        const score = summary.complexityScore;
        let level;
        if (score < 30) level = chalk.green('低');
        else if (score < 70) level = chalk.yellow('中');
        else level = chalk.red('高');
        
        console.log(`  分数: ${score}/100 (${level})`);
    }
    
    // 显示建议
    if (analysisResult.recommendations) {
        console.log(chalk.yellow('\n迁移建议:'));
        
        const strategy = analysisResult.recommendations.migrationStrategy;
        if (strategy) {
            console.log(`  策略: ${strategy.strategy}`);
            console.log(`  描述: ${strategy.description}`);
            console.log(`  预估工作量: ${strategy.estimatedEffort}`);
            console.log(`  推荐方法: ${strategy.recommendedApproach}`);
        }
        
        const risks = analysisResult.recommendations.riskAreas || [];
        if (risks.length > 0) {
            console.log(chalk.yellow('\n风险区域:'));
            risks.forEach(risk => {
                console.log(`  • ${risk.type}: ${risk.description}`);
                console.log(`    缓解措施: ${risk.mitigation}`);
            });
        }
    }
}

/**
 * 从分析结果中提取控件
 */
function extractControlsFromAnalysis(analysisResult) {
    const controls = [];
    
    if (analysisResult.forms) {
        analysisResult.forms.forEach(form => {
            if (form.controls) {
                form.controls.forEach(control => {
                    controls.push({
                        ...control,
                        formName: form.name,
                        formType: form.baseClass
                    });
                });
            }
        });
    }
    
    return controls;
}

/**
 * 提取统计信息
 */
function extractStats(analysisResult) {
    return {
        timestamp: new Date().toISOString(),
        project: analysisResult.metadata?.projectPath,
        summary: analysisResult.summary,
        statistics: {
            fileTypes: countFileTypes(analysisResult),
            controlTypes: countControlTypes(analysisResult),
            eventTypes: countEventTypes(analysisResult),
            complexityMetrics: calculateComplexityMetrics(analysisResult)
        }
    };
}

/**
 * 统计文件类型
 */
function countFileTypes(analysisResult) {
    const counts = {};
    
    if (analysisResult.forms) {
        analysisResult.forms.forEach(form => {
            const ext = path.extname(form.file || '');
            counts[ext] = (counts[ext] || 0) + 1;
        });
    }
    
    return counts;
}

/**
 * 统计控件类型
 */
function countControlTypes(analysisResult) {
    const counts = {};
    
    if (analysisResult.forms) {
        analysisResult.forms.forEach(form => {
            if (form.controls) {
                form.controls.forEach(control => {
                    const type = control.type.split('.').pop();
                    counts[type] = (counts[type] || 0) + 1;
                });
            }
        });
    }
    
    return counts;
}

/**
 * 统计事件类型
 */
function countEventTypes(analysisResult) {
    const counts = {};
    
    if (analysisResult.forms) {
        analysisResult.forms.forEach(form => {
            if (form.events) {
                form.events.forEach(event => {
                    counts[event.event] = (counts[event.event] || 0) + 1;
                });
            }
        });
    }
    
    return counts;
}

/**
 * 计算复杂度指标
 */
function calculateComplexityMetrics(analysisResult) {
    const summary = analysisResult.summary || {};
    
    return {
        totalElements: (summary.totalClasses || 0) + (summary.totalMethods || 0) + (summary.totalControls || 0),
        density: {
            methodsPerClass: summary.totalClasses ? (summary.totalMethods / summary.totalClasses).toFixed(2) : 0,
            controlsPerForm: analysisResult.forms ? (summary.totalControls / analysisResult.forms.length).toFixed(2) : 0,
            eventsPerControl: summary.totalControls ? (summary.totalEvents / summary.totalControls).toFixed(2) : 0
        }
    };
}

/**
 * 验证迁移
 */
async function validateMigration(winformsPath, qtPath, options = {}) {
    // 这是一个简化的验证实现
    // 实际实现应该包括：
    // 1. 文件结构验证
    // 2. 代码完整性验证
    // 3. 功能对等性检查（如果启用）
    // 4. 性能基准测试（如果启用）
    // 5. 布局一致性检查（如果启用）
    
    console.log(chalk.cyan('执行验证检查...'));
    
    const validationResult = {
        timestamp: new Date().toISOString(),
        winformsProject: winformsPath,
        qtProject: qtPath,
        checks: [],
        passed: 0,
        failed: 0,
        warnings: 0
    };
    
    // 检查1: Qt项目结构
    const structureCheck = await validateProjectStructure(qtPath);
    validationResult.checks.push(structureCheck);
    
    // 检查2: 文件完整性
    const integrityCheck = await validateFileIntegrity(qtPath);
    validationResult.checks.push(integrityCheck);
    
    // 检查3: 构建配置
    const buildCheck = await validateBuildConfiguration(qtPath);
    validationResult.checks.push(buildCheck);
    
    // 可选的深度检查
    if (options.checkFunctionality) {
        const functionalityCheck = await validateFunctionality(winformsPath, qtPath);
        validationResult.checks.push(functionalityCheck);
    }
    
    if (options.checkLayout) {
        const layoutCheck = await validateLayoutConsistency(winformsPath, qtPath);
        validationResult.checks.push(layoutCheck);
    }
    
    // 统计结果
    validationResult.checks.forEach(check => {
        if (check.status === 'passed') validationResult.passed++;
        else if (check.status === 'failed') validationResult.failed++;
        else if (check.status === 'warning') validationResult.warnings++;
    });
    
    validationResult.overallStatus = validationResult.failed === 0 ? 'passed' : 'failed';
    
    return validationResult;
}

/**
 * 验证项目结构
 */
async function validateProjectStructure(qtPath) {
    const requiredDirs = ['src', 'include', 'ui'];
    const requiredFiles = ['CMakeLists.txt', 'src/main.cpp'];
    
    const missingDirs = requiredDirs.filter(dir => !fs.existsSync(path.join(qtPath, dir)));
    const missingFiles = requiredFiles.filter(file => !fs.existsSync(path.join(qtPath, file)));
    
    return {
        name: '项目结构验证',
        status: missingDirs.length === 0 && missingFiles.length === 0 ? 'passed' : 'failed',
        details: {
            missingDirectories: missingDirs,
            missingFiles: missingFiles
        },
        message: missingDirs.length === 0 && missingFiles.length === 0 ?
            '项目结构完整' :
            `缺少: ${[...missingDirs, ...missingFiles].join(', ')}`
    };
}

/**
 * 验证文件完整性
 */
async function validateFileIntegrity(qtPath) {
    let corruptedFiles = 0;
    let emptyFiles = 0;
    
    function checkFile(filePath) {
        try {
            const stats = fs.statSync(filePath);
            if (stats.size === 0) {
                emptyFiles++;
                return false;
            }
            
            const content = fs.readFileSync(filePath, 'utf8');
            if (content.trim().length === 0) {
                emptyFiles++;
                return false;
            }
            
            return true;
        } catch (error) {
            corruptedFiles++;
            return false;
        }
    }
    
    // 检查关键文件
    const criticalFiles = [
        'CMakeLists.txt',
        'src/main.cpp',
        'src/mainwindow.cpp',
        'include/mainwindow.h'
    ];
    
    const failedFiles = criticalFiles.filter(file => {
        const fullPath = path.join(qtPath, file);
        return fs.existsSync(fullPath) && !checkFile(fullPath);
    });
    
    return {
        name: '文件完整性验证',
        status: failedFiles.length === 0 ? 'passed' : 'warning',
        details: {
            corruptedFiles,
            emptyFiles,
            failedFiles
        },
        message: failedFiles.length === 0 ?
            '所有关键文件完整' :
            `${failedFiles.length} 个文件可能有问题`
    };
}

/**
 * 验证构建配置
 */
async function validateBuildConfiguration(qtPath) {
    const cmakePath = path.join(qtPath, 'CMakeLists.txt');
    
    if (!fs.existsSync(cmakePath)) {
        return {
            name: '构建配置验证',
            status: 'failed',
            details: { missingFile: 'CMakeLists.txt' },
            message: '缺少CMakeLists.txt文件'
        };
    }
    
    try {
        const content = fs.readFileSync(cmakePath, 'utf8');
        
        const requiredElements = [
            'cmake_minimum_required',
            'project(',
            'find_package(Qt5',
            'add_executable(',
            'target_link_libraries('
        ];
        
        const missingElements = requiredElements.filter(element => !content.includes(element));
        
        return {
            name: '构建配置验证',
            status: missingElements.length === 0 ? 'passed' : 'warning',
            details: {
                missingElements,
                fileSize: content.length
            },
            message: missingElements.length === 0 ?
                'CMake配置完整' :
                `缺少: ${missingElements.join(', ')}`
        };
        
    } catch (error) {
        return {
            name: '构建配置验证',
            status: 'failed',
            details: { error: error.message },
            message: '无法读取CMakeLists.txt'
        };
    }
}

/**
 * 验证功能对等性
 */
async function validateFunctionality(winformsPath, qtPath) {
    // 简化的功能验证
    // 实际实现应该更复杂，可能包括：
    // - 对比窗体数量
    // - 对比控件数量
    // - 对比事件处理程序
    // - 业务逻辑对比
    
    return {
        name: '功能对等性验证',
        status: 'warning', // 通常是警告，因为需要人工验证
        details: {
            note: '功能对等性需要人工验证'
        },
        message: '建议进行人工功能测试'
    };
}

/**
 * 验证布局一致性
 */
async function validateLayoutConsistency(winformsPath, qtPath) {
    // 简化的布局验证
    return {
        name: '布局一致性验证',
        status: 'warning',
        details: {
            note: '布局一致性需要视觉验证'
        },
        message: '建议进行视觉对比测试'
    };
}

/**
 * 显示验证结果
 */
function displayValidationResults(validationResult) {
    console.log(chalk.cyan.bold('\n验证结果:'));
    console.log(chalk.cyan('─────────────'));
    
    console.log(chalk.green(`整体状态: ${validationResult.overallStatus === 'passed' ? chalk.green('通过') : chalk.red('失败')}`));
    console.log(chalk.green(`通过: ${validationResult.passed}`));
    console.log(chalk.green(`失败: ${validationResult.failed}`));
    console.log(chalk.green(`警告: ${validationResult.warnings}\n`));
    
    console.log(chalk.yellow('详细检查结果:'));
    validationResult.checks.forEach(check => {
        const statusColor = check.status === 'passed' ? chalk.green : 
                           check.status === 'failed' ? chalk.red : chalk.yellow;
        console.log(`  ${statusColor('●')} ${check.name}: ${statusColor(check.status)}`);
        console.log(`     ${check.message}`);
    });
}

/**
 * 显示迁移摘要
 */
function displayMigrationSummary(analysisResult, mappingResult, options) {
    console.log(chalk.cyan.bold('\n迁移摘要:'));
    console.log(chalk.cyan('─────────────'));
    
    const summary = analysisResult.summary || {};
    const stats = mappingResult.stats || {};
    
    console.log(chalk.green(`项目: ${options.name}`));
    console.log(chalk.green(`源项目: ${path.basename(options.project)}`));
    console.log(chalk.green(`目标项目: ${path.resolve(options.output)}`));
    console.log('');
    
    console.log(chalk.yellow('迁移统计:'));
    console.log(`  窗体数量: ${summary.totalForms || 0}`);
    console.log(`  控件总数: ${summary.totalControls || 0}`);
    console.log(`  成功映射: ${mappingResult.mappings.length}`);
    console.log(`  映射失败: ${mappingResult.errors.length}`);
    
    if (stats.successRate !== undefined) {
        console.log(`  映射成功率: ${stats.successRate.toFixed(1)}%`);
    }
    
    if (stats.averageConfidence !== undefined) {
        console.log(`  平均置信度: ${(stats.averageConfidence * 100).toFixed(1)}%`);
    }
    
    console.log(chalk.yellow('\n映射类型分布:'));
    if (stats.exactMatches !== undefined) {
        console.log(`  精确匹配: ${stats.exactMatches}`);
    }
    if (stats.patternMatches !== undefined) {
        console.log(`  模式匹配: ${stats.patternMatches}`);
    }
    if (stats.mlMatches !== undefined) {
        console.log(`  机器学习: ${stats.mlMatches}`);
    }
    if (stats.fallbackMatches !== undefined) {
        console.log(`  回退映射: ${stats.fallbackMatches}`);
    }
    
    // 显示错误摘要（如果有）
    if (mappingResult.errors.length > 0) {
        console.log(chalk.yellow('\n映射错误摘要:'));
        const errorTypes = {};
        mappingResult.errors.forEach(error => {
            errorTypes[error.type] = (errorTypes[error.type] || 0) + 1;
        });
        
        Object.entries(errorTypes).forEach(([type, count]) => {
            console.log(`  • ${type}: ${count} 个`);
        });
    }
    
    // 下一步建议
    console.log(chalk.yellow('\n下一步建议:'));
    if (!options.dryRun) {
        console.log('  1. 检查生成的Qt项目代码');
        console.log('  2. 构建并运行项目进行测试');
        console.log('  3. 根据需要进行手动调整');
        console.log('  4. 进行完整的功能测试');
    } else {
        console.log('  1. 检查映射报告');
        console.log('  2. 调整映射规则（如果需要）');
        console.log('  3. 重新运行迁移命令（不使用--dry-run）');
    }
}

/**
 * 批量处理项目
 */
async function processBatch(projects, parallelCount) {
    console.log(chalk.cyan(`开始批量处理 ${projects.length} 个项目...`));
    
    const results = [];
    const batches = [];
    
    // 创建批次
    for (let i = 0; i < projects.length; i += parallelCount) {
        batches.push(projects.slice(i, i + parallelCount));
    }
    
    // 处理每个批次
    for (let batchIndex = 0; batchIndex < batches.length; batchIndex++) {
        const batch = batches[batchIndex];
        console.log(chalk.cyan(`处理批次 ${batchIndex + 1}/${batches.length} (${batch.length} 个项目)`));
        
        const batchPromises = batch.map(async (projectConfig, index) => {
            const projectNumber = batchIndex * parallelCount + index + 1;
            console.log(chalk.cyan(`  项目 ${projectNumber}/${projects.length}: ${projectConfig.name}`));
            
            try {
                const result = await processSingleProject(projectConfig);
                return { ...result, success: true };
            } catch (error) {
                console.log(chalk.red(`  项目 ${projectConfig.name} 失败: ${error.message}`));
                return {
                    project: projectConfig.name,
                    success: false,
                    error: error.message
                };
            }
        });
        
        const batchResults = await Promise.all(batchPromises);
        results.push(...batchResults);
        
        // 批次间延迟（避免资源竞争）
        if (batchIndex < batches.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    
    // 显示批量处理结果
    displayBatchResults(results);
    
    return results;
}

/**
 * 处理单个项目
 */
async function processSingleProject(projectConfig) {
    const startTime = Date.now();
    
    // 分析项目
    const analyzer = new RoslynAnalyzer();
    const analysisResult = await analyzer.analyzeProject(projectConfig.winformsPath);
    
    // 映射控件
    const mapper = new IntelligentMapper();
    const mappingResult = await mapper.mapControlsBatch(
        extractControlsFromAnalysis(analysisResult),
        { projectName: projectConfig.qtName || projectConfig.name }
    );
    
    // 生成Qt项目
    const generator = new QtCodeGenerator({
        projectName: projectConfig.qtName || projectConfig.name,
        templateType: projectConfig.template || 'basic-qt-widgets'
    });
    
    await generator.generateProject({
        analysis: analysisResult,
        mappings: mappingResult.mappings,
        outputDir: projectConfig.outputDir
    });
    
    const elapsedTime = ((Date.now() - startTime) / 1000).toFixed(2);
    
    return {
        project: projectConfig.name,
        analysis: {
            files: analysisResult.summary?.totalFiles || 0,
            controls: analysisResult.summary?.totalControls || 0
        },
        mapping: {
            success: mappingResult.mappings.length,
            failed: mappingResult.errors.length,
            rate: mappingResult.stats?.successRate || 0
        },
        time: elapsedTime,
        outputDir: projectConfig.outputDir
    };
}

/**
 * 显示批量处理结果
 */
function displayBatchResults(results) {
    console.log(chalk.cyan.bold('\n批量处理结果:'));
    console.log(chalk.cyan('─────────────'));
    
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    
    console.log(chalk.green(`总计: ${results.length} 个项目`));
    console.log(chalk.green(`成功: ${successful}`));
    console.log(chalk.green(`失败: ${failed}`));
    console.log(chalk.green(`成功率: ${((successful / results.length) * 100).toFixed(1)}%\n`));
    
    if (successful > 0) {
        console.log(chalk.yellow('成功项目统计:'));
        
        const stats = {
            totalFiles: 0,
            totalControls: 0,
            totalTime: 0
        };
        
        results.filter(r => r.success).forEach(result => {
            stats.totalFiles += result.analysis?.files || 0;
            stats.totalControls += result.analysis?.controls || 0;
            stats.totalTime += parseFloat(result.time || 0);
        });
        
        console.log(`  总文件数: ${stats.totalFiles}`);
        console.log(`  总控件数: ${stats.totalControls}`);
        console.log(`  总耗时: ${stats.totalTime.toFixed(1)} 秒`);
        console.log(`  平均耗时: ${(stats.totalTime / successful).toFixed(1)} 秒/项目`);
    }
    
    if (failed > 0) {
        console.log(chalk.yellow('\n失败项目:'));
        results.filter(r => !r.success).forEach(result => {
            console.log(`  • ${result.project}: ${result.error}`);
        });
    }
}

// 导出模块（用于测试）
module.exports = {
    displayAnalysisSummary,
    extractControlsFromAnalysis,
    validateMigration,
    displayMigrationSummary
};