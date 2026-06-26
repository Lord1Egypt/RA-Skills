const { exec } = require('child_process');
const path = require('path');

// Python 脚本路径（相对于技能目录）
const PYTHON_SCRIPT_PATH = 'C:\\Users\\Administrator.rjazz-2022BWPUD\\.openclaw\\workspace\\skills\\purchase_record\\scripts\\add_purchase.py';

/**
 * 执行 Python 脚本并返回结果
 */
function executePython(message) {
    return new Promise((resolve, reject) => {
        const pythonCmd = `python "${PYTHON_SCRIPT_PATH}" "${message.replace(/"/g, '\\"')}"`;
        
        exec(pythonCmd, (error, stdout, stderr) => {
            if (error) {
                console.error(`执行错误：${error.message}`);
                if (stderr) {
                    console.error(`Stderr: ${stderr}`);
                }
                
                // 解析错误信息中的提示
                const errorMsg = stderr || stdout;
                let reply;
                if (errorMsg.includes('格式不正确')) {
                    reply = '❌ **格式不正确**\n\n请使用：`采购 MMDD 物品名称 价格`\n例如：`采购 0312 螺丝 3 元`';
                } else {
                    reply = `❌ **执行失败**\n${errorMsg}`;
                }
                
                resolve(reply);
                return;
            }

            // 解析成功输出
            const output = stdout.toString();
            
            // 提取 Markdown 内容（如果有的话）
            let reply = output.trim();
            
            // 如果没有找到表格，提示创建
            if (!output.includes('✅')) {
                reply += '\n\n💡 **提示**: Excel 文件不存在或需要初始化，系统已自动创建。';
            }

            resolve(reply);
        });
    });
}

/**
 * 主命令处理器 - 支持异步处理
 */
module.exports = async function(command, context) {
    const lowerCmd = command.toLowerCase().trim();

    // 检测采购命令
    if (lowerCmd.startsWith('采购')) {
        try {
            const result = await executePython(lowerCmd);
            return { reply: result };
        } catch (error) {
            console.error('处理采购命令时出错:', error);
            return { 
                reply: '❌ **系统错误**\n抱歉，处理您的请求时出现了问题。请稍后重试。' 
            };
        }
    }

    // 帮助命令
    if (lowerCmd === 'purchase_record' || lowerCmd === 'help purchase_record') {
        return {
            reply: `📋 **采购记录管理**\n\n用法：`采购 <MMDD> <物品名称> <价格>`\n示例：`采购 0312 螺丝 3 元`\n\nExcel 路径：C:\\Users\\Administrator.rjazz-2022BWPUD\\Desktop\\purchase_record.xlsx`
        };
    }

    // 默认回复 - 返回 null 让系统继续处理其他命令
    return null;
};