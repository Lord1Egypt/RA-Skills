# skill-rating-comparator

Skill 评分对比工具 - 自动对比同类型 Skill，生成多维度评分报告

## 功能

- 🔍 **自动发现** - 搜索 ClawHub 和 GitHub 上的同类 Skill
- 📊 **多维评分** - 6 大维度打分 (功能/代码/文档/评价/更新/安装)
- 📈 **对比报告** - 雷达图可视化 + 优劣势分析
- 💡 **推荐建议** - 基于评分给出选用建议

## 使用方法

### 基础用法

```
对比 skill-rating-comparator 和同类 Skill
评分对比 feishu-ai-coding-assistant
分析这个 Skill 的竞争力
```

### 高级用法

```
对比 skill-rating-comparator --platform=clawhub,github
评分 feishu-multi-agent-manager --dimensions=功能，代码，文档
生成 Skill 对比报告 --output=markdown
```

## 配置

在 OpenClaw 配置中添加：

```yaml
skills:
  skill-rating-comparator:
    platforms:
      - clawhub
      - github
    dimensions:
      - 功能完整性
      - 代码质量
      - 文档完善度
      - 用户评价
      - 更新频率
      - 安装便捷性
    weights:
      功能完整性：0.25
      代码质量：0.20
      文档完善度：0.15
      用户评价：0.15
      更新频率：0.15
      安装便捷性：0.10
```

## 输出示例

```
## 📊 Skill 评分对比报告

**目标 Skill:** skill-rating-comparator
**对比对象:** 5 个同类 Skill

### 综合评分
| Skill | 综合得分 | 排名 |
|-------|---------|------|
| skill-rating-comparator | 8.7 | 🥇 1 |
| skill-analyzer-pro | 7.9 | 🥈 2 |
| skill-compare-tool | 7.2 | 🥉 3 |

### 维度对比
- 功能完整性：⭐⭐⭐⭐⭐ (9/10)
- 代码质量：⭐⭐⭐⭐☆ (8/10)
- 文档完善度：⭐⭐⭐⭐⭐ (9/10)
- 用户评价：⭐⭐⭐⭐☆ (8/10)
- 更新频率：⭐⭐⭐⭐☆ (8/10)
- 安装便捷性：⭐⭐⭐⭐⭐ (9/10)

### 优势
✅ 功能最全面，支持多平台对比
✅ 文档详细，示例丰富
✅ 更新活跃，每周迭代

### 劣势
⚠️ 用户基数较小，评价数量有限
⚠️ 安装步骤稍复杂

### 推荐建议
如果你是...
- 个人开发者 → 推荐使用 skill-rating-comparator
- 团队使用 → 推荐使用 skill-analyzer-pro
- 需要快速部署 → 推荐使用 skill-compare-tool
```

## API

### 评分接口

```typescript
interface SkillRating {
  skillId: string;
  name: string;
  platform: 'clawhub' | 'github';
  scores: {
    functionality: number;      // 功能完整性
    codeQuality: number;        // 代码质量
    documentation: number;      // 文档完善度
    userReviews: number;        // 用户评价
    updateFrequency: number;    // 更新频率
    installation: number;       // 安装便捷性
  };
  totalScore: number;
  rank: number;
}
```

### 对比接口

```typescript
interface ComparisonReport {
  targetSkill: SkillRating;
  competitors: SkillRating[];
  summary: {
    strengths: string[];
    weaknesses: string[];
    recommendations: string[];
  };
  radarData: number[][];  // 雷达图数据
}
```

## 依赖

- @openclaw/sdk (运行时提供)
- node-fetch (HTTP 请求)
- cheerio (HTML 解析，可选)

## 开发说明

### 评分算法

每个维度 0-10 分，加权计算总分：

```
总分 = Σ(维度分 × 权重)

权重默认：
- 功能完整性：25%
- 代码质量：20%
- 文档完善度：15%
- 用户评价：15%
- 更新频率：15%
- 安装便捷性：10%
```

### 数据来源

1. **ClawHub API** - 下载量、评分、评论
2. **GitHub API** - Star、Fork、Issue、更新频率
3. **代码分析** - TypeScript 编译、代码规范
4. **文档分析** - README 完整度、示例数量

## 版本

- v1.0.0 - 初始版本，基础评分对比功能

## 作者

OpenClaw Skill 大师 ⚡

## 许可证

MIT
