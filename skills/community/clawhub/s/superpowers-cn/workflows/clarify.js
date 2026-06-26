/**
 * 超能力 CN - 澄清阶段
 * 
 * 当接到任务时，主动理解需求的本质
 */

/**
 * 澄清问题清单
 */
export const clarifyQuestions = [
  "你想解决什么问题？",
  "最终效果是什么样的？",
  "有什么限制或要求？",
  "有没有参考示例？",
  "希望什么时候完成？"
];

/**
 * 分析需求本质
 * @param {string} userRequest - 用户的原始需求
 * @returns {object} 解析后的需求理解
 */
export function analyzeRequest(userRequest) {
  return {
    original: userRequest,
    understood: '',
    goal: '',
    constraints: [],
    scope: [],
    risks: []
  };
}

/**
 * 生成澄清问题
 * @param {string} request - 需求描述
 */
export function generateClarifyQuestions(request) {
  return `
## 🎯 需求澄清

在开始之前，我想确认几个问题：

${clarifyQuestions.map((q, i) => `${i + 1}. ${q}`).join('\n')}

请告诉我你的具体需求，我们先对齐再做。
  `.trim();
}
