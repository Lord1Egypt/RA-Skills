/**
 * OpenClaw Hook Handler - Self-Learning Skill
 * 
 * 在会话开始时自动检查待处理的学习记录，并提醒 Agent 处理。
 */

const fs = require('fs');
const path = require('path');

/**
 * Hook: 会话开始时执行
 * 检查 .learnings/ 目录下的待处理高优先级条目
 */
async function onSessionStart(context) {
    const workspace = process.env.WORKSPACE || './workspace';
    const learningsDir = path.join(workspace, '.learnings');
    const learningsFile = path.join(learningsDir, 'LEARNINGS.md');
    
    // 检查文件是否存在
    if (!fs.existsSync(learningsFile)) {
        return {
            action: 'continue',
            message: ''
        };
    }
    
    // 读取学习记录
    const content = fs.readFileSync(learningsFile, 'utf-8');
    
    // 查找待处理的高优先级条目
    const highPriorityPattern = /\*\*Priority\*\*:\s*(high|critical).*?\*\*Status\*\*:\s*pending/gs;
    const matches = content.matchAll(highPriorityPattern);
    
    const pendingItems = [];
    for (const match of matches) {
        pendingItems.push(match[0]);
    }
    
    if (pendingItems.length === 0) {
        return {
            action: 'continue',
            message: ''
        };
    }
    
    // 构建提醒消息
    let reminder = `\n\n🔍 **待处理的高优先级学习记录 (${pendingItems.length} 条)**\n\n`;
    reminder += `请检查 \`.learnings/LEARNINGS.md\` 中的待处理条目，并决定是否需要:\n`;
    reminder += `1. 立即处理 (如果影响当前任务)\n`;
    reminder += `2. 提升到项目文件 (如果广泛适用)\n`;
    reminder += `3. 标记为解决或延后\n\n`;
    
    // 显示前 3 条
    const preview = pendingItems.slice(0, 3).map((item, i) => {
        const idMatch = item.match(/\[(\w+-\d+-\w+)\]/);
        const categoryMatch = item.match(/\]\s*(\w+)/);
        return `${i + 1}. [${idMatch ? idMatch[1] : '???'}] ${categoryMatch ? categoryMatch[1] : 'unknown'}`;
    }).join('\n');
    
    reminder += preview;
    
    if (pendingItems.length > 3) {
        reminder += `\n... 还有 ${pendingItems.length - 3} 条，请查看完整文件`;
    }
    
    reminder += `\n\n---\n\n`;
    
    return {
        action: 'inject',
        message: reminder,
        position: 'after_system'
    };
}

/**
 * Hook: 用户提交 prompt 后执行
 * 检查是否有需要记录的学习内容
 */
async function onPromptSubmit(context) {
    const prompt = context.prompt || '';
    
    // 检测用户纠正的信号
    const correctionSignals = [
        '不对', '错了', '不是这样', '应该是', '你搞错了',
        'actually', 'no,', 'wrong,', 'incorrect,', 'should be'
    ];
    
    const hasCorrection = correctionSignals.some(signal => 
        prompt.toLowerCase().includes(signal)
    );
    
    if (hasCorrection) {
        return {
            action: 'suggest',
            message: '\n\n💡 检测到用户纠正，是否需要记录到 `.learnings/LEARNINGS.md`？\n'
        };
    }
    
    return {
        action: 'continue',
        message: ''
    };
}

module.exports = {
    onSessionStart,
    onPromptSubmit
};
