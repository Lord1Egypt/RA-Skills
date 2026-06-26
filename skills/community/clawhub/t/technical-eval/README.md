# Technical Evaluation Skill

## 版本信息
- **版本号**: v1.0.0
- **发布日期**: 2026-03-20
- **状态**: 活跃

## 核心功能
专业的技术选型评估工作流，从需求定义到实施路径的完整决策支持。

## 主要特性
- 八步技术评估工作流（需求定义 → 全景扫描 → 趋势雷达 → 深度评估 → PoC验证 → 风险控制 → 选型决策 → 报告生成）
- 量化强化原则（强制量化、半量化、定性标注）
- 行业专业化模板（AI Infra、SaaS、AI Agent、消费品、AI软件）
- Tavily API 域名白名单配置（统一配置路径：~/.openclaw/.env）

## 配置要求
- Tavily API Key: 配置在 ~/.openclaw/.env 文件中
- 数据源域名白名单：已内置专业数据源配置

## 输出格式
- evaluation-report.md: 完整选型决策报告
- presentation.html: 可视化演示文稿（乔布斯风格）
- data/: 原始数据和分析结果
- sources.md: 数据源和参考文献

## 兼容性
- 向后兼容所有 technical-eval 使用场景
- 与 ppt-generator 技能集成
- 支持 business-strategy-analysis 技能协作