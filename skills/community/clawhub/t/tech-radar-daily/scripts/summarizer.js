/**
 * AI 摘要生成器
 * 使用规则引擎提取价值点，不依赖外部 AI 服务
 */

/**
 * 为项目生成摘要
 */
async function generateSummaries(projects) {
  const summarized = [];
  
  for (const project of projects) {
    try {
      const summary = await generateSummary(project);
      const score = scoreProject(project);
      summarized.push({
        ...project,
        summary,
        score
      });
    } catch (error) {
      console.error(`生成摘要失败 ${project.name}:`, error.message);
      const score = scoreProject(project);
      summarized.push({
        ...project,
        summary: project.description || '暂无摘要',
        score
      });
    }
  }
  
  // 按分数排序
  summarized.sort((a, b) => b.score - a.score);
  
  return summarized;
}

/**
 * 生成单个项目的摘要
 */
async function generateSummary(project) {
  // 暂时跳过 AI 摘要，直接返回价值点
  // TODO: 后续可以集成 Gemini CLI 或其他 AI 服务
  return extractValuePoint(project);
}

/**
 * 构建 AI 提示词
 */
function buildPrompt(project) {
  return `请用一句话（不超过 50 字）总结这个项目的核心价值：
项目名：${project.name}
描述：${project.description || '无'}
类型：${project.sourceType}
${project.stars ? `Star 数：${project.stars}` : ''}

要求：
1. 突出解决什么问题
2. 说明为什么值得关注
3. 不要重复项目名称`;
}

/**
 * 提取价值点（备用方案）
 */
function extractValuePoint(project) {
 const text = `${project.name || ''} ${project.description || ''}`.toLowerCase();

 if (project.sourceType === 'github') {

 // 语音
 if (text.includes('voice') || text.includes('speech') || text.includes('audio')) {
 return '语音 AI / 音频处理项目';
 }

 // 视觉
 if (
 text.includes('vision') ||
 text.includes('face') ||
 text.includes('image') ||
 text.includes('video') ||
 text.includes('deepfake')
 ) {
 return '计算机视觉 / 视频生成相关项目';
 }

 // AI Agent
 if (text.includes('agent')) {
 return 'AI Agent / 自动化研究框架';
 }

 // LLM
 if (text.includes('llm') || text.includes('gpt') || text.includes('language model')) {
 return '大模型应用或工具';
 }

 // 通用 AI
 if (text.includes('ai')) {
 return 'AI 相关开源项目';
 }

 if (text.includes('pdf')) {
 return 'PDF 生成或处理工具库';
 }

 if (text.includes('automation') || text.includes('bot')) {
 return '自动化工具或机器人框架';
 }

 if (text.includes('framework')) {
 return '开发框架类项目';
 }

 if (text.includes('api')) {
 return 'API 工具或服务框架';
 }

 return `开源项目，当前 ${project.stars || 0}⭐`;
 }

 if (project.sourceType === 'product') {
 return `${project.pricing || '商业产品'}，面向 ${project.targetUser || '开发者'} 用户`;
 }

 if (project.sourceType === 'tools') {
 if (project.deployable) {
 return '可自部署的实用工具';
 }
 return '解决特定问题的小工具';
 }

 return project.description || '值得关注的新项目';
}

/**
 * 项目重要度评分
 */
function scoreProject(project) {
 let score = 0;

 // Star 增长
 if (project.starsToday) {
 score += Math.sqrt(project.starsToday) * 10;
 }

 // 总 Star
 if (project.stars) {
 score += Math.log10(project.stars) * 10;
 }

 const text = `${project.name || ''} ${project.description || ''}`.toLowerCase();

 // AI 加分
 if (
 text.includes('ai') ||
 text.includes('llm') ||
 text.includes('agent') ||
 text.includes('gpt') ||
 text.includes('vision') ||
 text.includes('voice')
 ) {
 score += 20;
 }

 // 大厂项目加分
 if (
 text.includes('microsoft') ||
 text.includes('google') ||
 text.includes('meta') ||
 text.includes('openai')
 ) {
 score += 15;
 }

 return Math.round(score);
}

module.exports = {
  generateSummaries,
  scoreProject
};
