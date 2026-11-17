/**
 * QA QuickCheck - Skill 入口文件
 * 负责根据 manifest 中定义的 input 参数，调度执行对应的测试模式
 *
 * 注意：本 Skill 的核心逻辑由 AI Agent 通过读取 references/ 中的规则文件来执行，
 * 此入口文件仅作为 OpenClaw Skill 体系的结构性入口。
 */

module.exports = async function handler(input, context) {
  const { mode = "standard", project_path } = input;

  // 返回执行指引，实际执行由 AI Agent 根据 SKILL.md 和 references/ 完成
  return {
    mode,
    instructions: `请按 ${mode} 模式执行测试。AI Agent 将自动读取 references/00-调度器.md 并按照规则文件执行测试。`,
    references: {
      scheduler: "references/00-调度器.md",
      quick: ["references/00-A-缺陷定级与编号规则.md", "references/01-静态代码审计.md"],
      standard: [
        "references/00-A-缺陷定级与编号规则.md",
        "references/00-B-报告模板与追溯映射.md",
        "references/00-D-回归测试策略.md",
        "references/00-E-时间预算与超时处理.md",
        "references/00-F-测试数据管理策略.md",
        "references/01-静态代码审计.md",
        "references/02-动态功能测试.md",
        "references/02-0-测试设计方法论.md"
      ]
    },
    scripts: {
      "http-test-runner": "scripts/http-test-runner.js",
      "config-check": "scripts/security-headers-check.js",
      "data-factory": "scripts/data-factory.js"
    },
    project_path: project_path || process.cwd()
  };
};