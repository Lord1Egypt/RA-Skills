/**
 * 响应解析器
 * 解析子 Agent 的返回结果
 */

/**
 * 解析子 Agent 响应
 * @param {Object} subagentResult - 子 Agent 运行结果
 * @param {string} visitorUid - 访客 UID
 */
function parseResponse(subagentResult, visitorUid) {
  console.log('[ResponseParser] ========== 解析响应 ==========');
  console.log(`[ResponseParser] 状态: ${subagentResult.status}`);
  
  // 处理超时
  if (subagentResult.status === 'timed_out') {
    console.log('[ResponseParser] ⚠️ 子 Agent 超时');
    return createFallbackResponse(visitorUid, '处理超时');
  }
  
  // 处理错误
  if (subagentResult.status === 'error' || subagentResult.error) {
    console.log(`[ResponseParser] ❌ 子 Agent 错误: ${subagentResult.error}`);
    return createFallbackResponse(visitorUid, `处理失败: ${subagentResult.error}`);
  }
  
  // 解析成功响应
  if (subagentResult.output) {
    try {
      console.log('[ResponseParser] 解析 JSON 输出...');
      const parsed = JSON.parse(subagentResult.output);
      
      // 验证必要字段
      if (!parsed.reply) {
        throw new Error('缺少 reply 字段');
      }
      
      console.log('[ResponseParser] ✅ 解析成功');
      
      return {
        reply: parsed.reply,
        to_uid: parsed.to_uid || visitorUid,
        intimacy_suggestion: parsed.intimacy_suggestion ?? null,
        need_owner_attention: parsed.need_owner_attention ?? false,
        attention_reason: parsed.attention_reason || '',
        tags_to_add: parsed.tags_to_add || [],
        tags_to_remove: parsed.tags_to_remove || []
      };
      
    } catch (error) {
      console.error(`[ResponseParser] ❌ 解析失败: ${error.message}`);
      console.log('[ResponseParser] 原始输出:', subagentResult.output?.substring(0, 200));
      return createFallbackResponse(visitorUid, '响应解析失败');
    }
  }
  
  // 无输出
  console.log('[ResponseParser] ⚠️ 无输出内容');
  return createFallbackResponse(visitorUid, '无响应内容');
}

/**
 * 创建降级响应
 */
function createFallbackResponse(visitorUid, reason) {
  return {
    reply: '抱歉，系统繁忙，已转接人工处理',
    to_uid: visitorUid,
    intimacy_suggestion: null,
    need_owner_attention: true,
    attention_reason: `子Agent${reason}`,
    tags_to_add: [],
    tags_to_remove: []
  };
}

module.exports = { parseResponse };
