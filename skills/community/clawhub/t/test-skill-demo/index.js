/**
 * Test Skill Demo - 测试技能示例
 * 
 * 这是一个完整的测试技能，展示 OpenClaw 技能的标准结构和功能。
 * 用于演示 ClawHub 发布流程和技能开发最佳实践。
 * 
 * @author agentsignals
 * @license MIT
 * @version 1.0.0
 */

/**
 * 技能主入口函数
 * @param {Object} context - 执行上下文
 * @param {Object} context.message - 触发消息
 * @param {Function} context.reply - 回复函数
 * @param {string} context.workspace - 工作区路径
 * @returns {Promise<Object>} 执行结果
 */
export async function run(context) {
  const { message, reply, workspace } = context;
  
  // 发送欢迎消息
  await reply("🐾 **Test Skill Demo 运行成功！**");
  await reply("");
  await reply("### 技能信息");
  await reply(`- 名称：test-skill-demo`);
  await reply(`- 版本：1.0.0`);
  await reply(`- 作者：agentsignals`);
  await reply("");
  await reply("### 执行环境");
  await reply(`- 时间：${new Date().toISOString()}`);
  await reply(`- 工作区：${workspace || 'N/A'}`);
  await reply(`- Node: ${process.version}`);
  await reply("");
  await reply("### 功能演示");
  await reply("✅ 消息回复功能正常");
  await reply("✅ 上下文信息获取正常");
  await reply("✅ 技能执行流程正常");
  await reply("");
  await reply("---");
  await reply("*这是一个测试技能，用于演示 ClawHub 发布流程。*");
  
  return { 
    status: "ok",
    timestamp: new Date().toISOString(),
    workspace: workspace || null
  };
}

/**
 * 技能元数据
 * 用于 ClawHub 注册和分类
 */
export const meta = {
  name: "test-skill-demo",
  description: "一个完整的测试技能示例，展示 ClawHub 技能的标准结构和最佳实践",
  version: "1.0.0",
  author: "agentsignals",
  license: "MIT",
  keywords: ["test", "demo", "example", "tutorial", "clawhub", "openclaw"],
  category: "utilities",
  repository: "https://clawhub.com/agentsignals/test-skill-demo",
  requirements: {
    node: ">=18.0.0",
    openclaw: ">=2026.1.0"
  },
  features: [
    "基础消息回复",
    "上下文信息展示",
    "模块化代码结构",
    "完整的元数据定义"
  ]
};

/**
 * 技能配置 Schema（可选）
 * 定义技能可配置的参数
 */
export const configSchema = {
  type: "object",
  properties: {
    greeting: {
      type: "string",
      default: "🐾",
      description: "自定义问候语前缀"
    },
    verbose: {
      type: "boolean",
      default: true,
      description: "是否输出详细信息"
    }
  }
};
