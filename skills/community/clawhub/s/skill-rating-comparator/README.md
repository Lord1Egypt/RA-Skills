# Skill 评分对比工具 ⚡

> 自动对比同类型 Skill，生成多维度评分报告，帮你做出最佳选择

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.ai/skills/skill-rating-comparator)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.8+-orange.svg)](https://openclaw.ai)

---

## 🎯 功能亮点

- 🔍 **自动发现** - 搜索 ClawHub 和 GitHub 上的同类 Skill
- 📊 **多维评分** - 6 大维度打分 (功能/代码/文档/评价/更新/安装)
- 📈 **对比报告** - 雷达图可视化 + 优劣势分析
- 💡 **推荐建议** - 基于评分给出选用建议

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install skill-rating-comparator
```

### 使用

在飞书或 OpenClaw 对话中发送：

```
对比 skill-rating-comparator
评分 feishu-ai-coding-assistant
分析 feishu-multi-agent-manager 的竞争力
```

---

## 📊 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 功能完整性 | 25% | 核心功能、高级功能、配置选项、API 完整性 |
| 代码质量 | 20% | TypeScript 使用、类型定义、代码规范、测试覆盖 |
| 文档完善度 | 15% | README 完整度、示例代码、API 文档、FAQ |
| 用户评价 | 15% | 评分、评论、Star/Fork 比例 |
| 更新频率 | 15% | 最后更新时间、发布频率 |
| 安装便捷性 | 10% | 安装步骤复杂度、依赖数量 |

---

## 📋 输出示例

### 综合评分表格

| 排名 | Skill | 平台 | 综合得分 | 功能 | 代码 | 文档 | 评价 | 更新 | 安装 |
|------|-------|------|---------|------|------|------|------|------|------|
| 🥇 1 | skill-rating-comparator | clawhub | **8.7** | 9 | 8 | 9 | 8 | 8 | 9 |
| 🥈 2 | skill-analyzer-pro | clawhub | **7.9** | 8 | 8 | 7 | 8 | 7 | 9 |
| 🥉 3 | skill-compare-tool | clawhub | **7.2** | 7 | 7 | 8 | 7 | 6 | 9 |

### 维度详情

- 功能完整性：⭐⭐⭐⭐⭐ (9/10)
- 代码质量：⭐⭐⭐⭐☆ (8/10)
- 文档完善度：⭐⭐⭐⭐⭐ (9/10)
- 用户评价：⭐⭐⭐⭐☆ (8/10)
- 更新频率：⭐⭐⭐⭐☆ (8/10)
- 安装便捷性：⭐⭐⭐⭐⭐ (9/10)

### 优劣势分析

**✅ 优势**
- 功能完整性领先 (9 vs 平均 7.3)
- 文档完善度领先 (9 vs 平均 7.0)
- 安装便捷性领先 (9 vs 平均 8.3)

**⚠️ 劣势**
- 用户评价待提升 (8 vs 平均 8.5)

**💡 推荐建议**
- 综合评分第一，推荐作为首选
- 安装便捷，适合快速部署场景
- 文档完善，适合新手使用

---

## ⚙️ 配置

在 OpenClaw 配置中自定义权重：

```yaml
skills:
  skill-rating-comparator:
    weights:
      functionality: 0.30      # 功能完整性 (默认 0.25)
      codeQuality: 0.25        # 代码质量 (默认 0.20)
      documentation: 0.15      # 文档完善度 (默认 0.15)
      userReviews: 0.10        # 用户评价 (默认 0.15)
      updateFrequency: 0.10    # 更新频率 (默认 0.15)
      installation: 0.10       # 安装便捷性 (默认 0.10)
```

---

## 🔧 开发

### 环境要求

- Node.js >= 18.0.0
- OpenClaw >= 2026.3.8

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/rfdiosuao/openclaw-skills.git
cd openclaw-skills/skill-rating-comparator

# 安装依赖
npm install

# 编译
npm run build

# 测试
npm test

# 开发模式
npm run dev
```

### 项目结构

```
skill-rating-comparator/
├── src/
│   ├── index.ts          # 主入口
│   └── types.d.ts        # 类型定义
├── tests/
│   └── index.test.ts     # 单元测试
├── SKILL.md              # ClawHub 技能说明
├── README.md             # 完整文档
├── package.json          # NPM 配置
├── tsconfig.json         # TypeScript 配置
└── .gitignore
```

---

## 📖 API

### SkillRatingComparator 类

```typescript
import { SkillRatingComparator } from './index';

const comparator = new SkillRatingComparator({
  weights: {
    functionality: 0.30,
    codeQuality: 0.25,
    // ... 其他权重
  }
});

// 生成对比报告
const report = await comparator.generateReport('skill-name');

// 格式化为 Markdown
const markdown = comparator.formatReportMarkdown(report);
```

### 返回类型

```typescript
interface ComparisonReport {
  targetSkill: SkillRating;
  competitors: SkillRating[];
  summary: {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  radarData: {
    labels: string[];
    datasets: number[][];
  };
}
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 更新日志

### v1.0.0 (2026-03-23)

- ✨ 初始版本发布
- 🔍 支持 ClawHub 和 GitHub 搜索
- 📊 6 维度评分系统
- 📈 Markdown 报告生成
- 💡 智能推荐建议

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

**OpenClaw Skill 大师 ⚡**

- GitHub: [@rfdiosuao](https://github.com/rfdiosuao)
- ClawHub: [OpenClaw Skill Master](https://clawhub.ai/users/skill-master)

---

## 🙏 致谢

感谢所有贡献者和用户！

---

<div align="center">

**如果觉得有用，请给个 Star ⭐**

[GitHub](https://github.com/rfdiosuao/openclaw-skills) | [ClawHub](https://clawhub.ai/skills/skill-rating-comparator)

</div>
