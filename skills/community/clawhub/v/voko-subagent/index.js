/**
 * VOKO Subagent Skill - 主入口
 * 
 * 运行在 OpenClaw Gateway 内部，负责：
 * 1. 接收来自 voko im-service 的 CLI 调用
 * 2. 创建真正的子 Agent 处理访客消息
 * 3. 返回处理结果
 */

const { handleVisitorMessage } = require('./src/handler');
const { parseArgs } = require('./src/args-parser');

/**
 * Skill 主入口
 * 支持两种调用方式：
 * 1. CLI: openclaw skill run voko-subagent --visitor-uid=xxx --db-path=xxx
 * 2. Gateway: 通过 tool.sessions_spawn 调用
 */
async function main() {
  console.log('[VOKO-Subagent] ========== Skill 启动 ==========');
  
  try {
    // 解析参数
    const args = parseArgs();
    console.log('[VOKO-Subagent] 参数:', JSON.stringify(args, null, 2));
    
    // 处理访客消息
    const result = await handleVisitorMessage(args);
    
    console.log('[VOKO-Subagent] ✅ 处理完成');
    console.log('[VOKO-Subagent] ========== Skill 结束 ==========');
    
    // 输出结果（JSON 格式，方便调用方解析）
    console.log('\n===RESULT===');
    console.log(JSON.stringify(result, null, 2));
    console.log('===END===');
    
    return result;
  } catch (error) {
    console.error('[VOKO-Subagent] ❌ 处理失败:', error.message);
    console.error('[VOKO-Subagent] 堆栈:', error.stack);
    
    const errorResult = {
      success: false,
      error: error.message,
      reply: '系统繁忙，请稍后再试',
      need_owner_attention: true,
      attention_reason: `子Agent处理失败: ${error.message}`
    };
    
    console.log('\n===RESULT===');
    console.log(JSON.stringify(errorResult, null, 2));
    console.log('===END===');
    
    return errorResult;
  }
}

// 运行主函数
main();
