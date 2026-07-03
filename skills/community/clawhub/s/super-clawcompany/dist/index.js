#!/usr/bin/env node
"use strict";
/**
 * ClawCompany - OpenClaw 虚拟团队协作系统
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.createProject = createProject;
exports.runPMAgent = runPMAgent;
exports.runDevAgent = runDevAgent;
exports.runReviewAgent = runReviewAgent;
const config_1 = require("./config");
const errors_1 = require("./errors");
const openclaw_1 = require("openclaw");
let logger;
/**
 * 创建项目（主入口）
 */
async function createProject(userRequest, projectPath, options) {
    // 1. 加载配置
    const config = (0, config_1.loadConfig)({ projectRoot: projectPath, ...options });
    const errors = (0, config_1.validateConfig)(config);
    if (errors.length > 0 && !config.dryRun) {
        throw new errors_1.ClawCompanyError('配置验证失败', 'CONFIG_ERROR', { errors });
    }
    // 2. 初始化日志
    logger = new config_1.Logger('ClawCompany', config.verbose ? config_1.LogLevel.DEBUG : config_1.LogLevel.INFO);
    logger.info('🦞 开始工作...');
    logger.debug('配置:', config);
    if (config.dryRun) {
        logger.warn('🔍 DRY RUN 模式 - 不会实际执行');
    }
    try {
        // 2. PM Agent 分析需求
        logger.step(1, 3, 'PM Agent 分析需求...');
        const tasks = await runPMAgent(userRequest, config);
        logger.success(`PM Agent 拆分了 ${tasks.length} 个任务`);
        // 3. 执行每个任务
        const allFiles = [];
        for (let i = 0; i < tasks.length; i++) {
            const task = tasks[i];
            logger.step(2, tasks.length + 2, `Dev Agent 实现 "${task.title}"...`);
            if (!config.dryRun) {
                const files = await runDevAgent(task, config.projectRoot, config);
                allFiles.push(...files);
                logger.success(`创建了 ${files.length} 个文件`);
            }
            else {
                logger.debug(`[DRY RUN] 跳过 Dev Agent`);
                allFiles.push(`dry-run-${task.id}.ts`);
            }
            // Review Agent 审查
            logger.step(3, tasks.length + 2, `Review Agent 审查...`);
            if (!config.dryRun) {
                const approved = await runReviewAgent(task, allFiles, config);
                if (approved) {
                    logger.success('审查通过');
                }
                else {
                    logger.warn('审查建议修改（暂跳过）');
                }
            }
            else {
                logger.debug(`[DRY RUN] 跳过 Review Agent`);
            }
        }
        // 4. 返回结果
        const result = {
            success: true,
            tasks,
            files: allFiles,
            summary: `🎉 项目完成！完成 ${tasks.length} 个任务，生成 ${allFiles.length} 个文件`
        };
        logger.info(result.summary);
        return result;
    }
    catch (error) {
        logger.error('项目执行失败', error);
        throw error;
    }
}
/**
 * PM Agent - 分析需求并拆分任务
 */
async function runPMAgent(userRequest, config) {
    return (0, errors_1.withErrorHandling)('PM Agent', async () => {
        if (config.dryRun) {
            return [
                {
                    id: 'dry-run-task-1',
                    title: '示例任务',
                    description: userRequest,
                    assignedTo: 'dev',
                    dependencies: []
                }
            ];
        }
        const session = await (0, openclaw_1.sessions_spawn)({
            runtime: 'subagent',
            task: `你是 PM Agent (产品经理)。

用户需求：${userRequest}

你的职责：
1. 分析用户需求
2. 拆分成 2-4 个可执行的子任务
3. 每个任务分配给 dev agent

返回 JSON 格式（只返回 JSON，不要其他内容）：
{
  "tasks": [
    {
      "id": "task-1",
      "title": "任务标题",
      "description": "任务详细描述",
      "assignedTo": "dev",
      "dependencies": []
    }
  ]
}`,
            thinking: config.pmAgentThinking || 'high',
            mode: 'run'
        });
        const history = await (0, openclaw_1.sessions_history)({ sessionKey: session.sessionKey });
        const lastMessage = history.messages[history.messages.length - 1];
        try {
            const result = JSON.parse(lastMessage.content);
            return result.tasks || [];
        }
        catch (parseError) {
            logger.error('PM Agent 返回格式错误，使用默认任务拆分');
            return [
                {
                    id: 'fallback-task-1',
                    title: '实现核心功能',
                    description: userRequest,
                    assignedTo: 'dev',
                    dependencies: []
                }
            ];
        }
    });
}
/**
 * Dev Agent - 实现任务
 */
async function runDevAgent(task, projectPath, config) {
    return (0, errors_1.withErrorHandling)('Dev Agent', async () => {
        if (config.dryRun) {
            return [`dry-run-${task.id}.ts`];
        }
        const session = await (0, openclaw_1.sessions_spawn)({
            runtime: config.devAgentRuntime || 'acp',
            agentId: config.devAgentRuntime === 'acp' ? 'opencode' : undefined,
            task: `你是 Dev Agent (开发者)。

任务：${task.title}
描述：${task.description}
项目路径：${projectPath}

你的职责：
1. 理解任务需求
2. 创建必要的代码文件
3. 确保代码可运行

请实现这个任务，创建相应的文件。`,
            mode: 'run',
            cwd: projectPath
        });
        const history = await (0, openclaw_1.sessions_history)({ sessionKey: session.sessionKey });
        const lastMessage = history.messages[history.messages.length - 1];
        // 解析生成的文件（简化版）
        // TODO: 从 OpenCode 的输出中提取文件列表
        return [`src/${task.title.replace(/\s+/g, '-')}.ts`];
    });
}
/**
 * Review Agent - 审查代码
 */
async function runReviewAgent(task, files, config) {
    return (0, errors_1.withErrorHandling)('Review Agent', async () => {
        if (config.dryRun) {
            return true;
        }
        const session = await (0, openclaw_1.sessions_spawn)({
            runtime: 'subagent',
            task: `你是 Review Agent (代码审查)。

任务：${task.title}
生成的文件：${files.join(', ')}

你的职责：
1. 检查代码质量
2. 安全性审查
3. 决定是否批准

返回 JSON 格式：
{
  "approved": true/false,
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2"]
}`,
            thinking: config.reviewAgentThinking || 'high',
            mode: 'run'
        });
        const history = await (0, openclaw_1.sessions_history)({ sessionKey: session.sessionKey });
        const lastMessage = history.messages[history.messages.length - 1];
        try {
            const result = JSON.parse(lastMessage.content);
            return result.approved !== false;
        }
        catch {
            return true; // 默认批准
        }
    });
}
// CLI 入口
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
        console.log(`
🦞 ClawCompany - AI 虚拟团队协作系统

用法：
  clawcompany <需求描述> [选项]

选项：
  --path <目录>      项目路径（默认：当前目录）
  --verbose          详细日志
  --dry-run          模拟运行（不实际执行）

示例：
  clawcompany "创建一个登录页面"
  clawcompany "实现计算器" --path ~/my-project
  clawcompany "Todo应用" --verbose --dry-run

环境变量：
  GLM_API_KEY        GLM API Key（必需）
  PROJECT_ROOT       默认项目路径
  VERBOSE            详细模式
  DRY_RUN            模拟运行
    `);
        process.exit(0);
    }
    // 解析参数
    const userRequest = [];
    let projectPath = process.cwd();
    let verbose = false;
    let dryRun = false;
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--path' && args[i + 1]) {
            projectPath = args[i + 1];
            i++;
        }
        else if (args[i] === '--verbose') {
            verbose = true;
        }
        else if (args[i] === '--dry-run') {
            dryRun = true;
        }
        else if (!args[i].startsWith('--')) {
            userRequest.push(args[i]);
        }
    }
    const requestText = userRequest.join(' ');
    createProject(requestText, projectPath, { verbose, dryRun })
        .then(result => {
        console.log('\n' + JSON.stringify(result, null, 2));
        process.exit(0);
    })
        .catch(error => {
        console.error('\n❌ 错误:', error.message);
        if (verbose && error.details) {
            console.error('详情:', error.details);
        }
        process.exit(1);
    });
}
