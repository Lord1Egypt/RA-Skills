---
name: zhua-contributor
version: 1.0.0
description: 爪爪社区贡献系统 —— 发布技能到skillhub、撰写文档、分享经验。Use when 爪爪需要向OpenClaw社区贡献、发布技能、或建立影响力。
---

# 爪爪社区贡献系统 (Zhua Contributor)

让爪爪能够向OpenClaw社区贡献技能、分享经验、建立影响力。

## 核心能力

1. **技能发布** - 打包并发布技能到skillhub
2. **文档撰写** - 撰写技能文档和使用指南
3. **经验分享** - 分享进化经验和最佳实践
4. **社区互动** - 参与社区讨论和协作
5. **影响力建设** - 建立爪爪品牌和影响力

## 贡献类型

| 类型 | 描述 | 难度 |
|------|------|------|
| 技能发布 | 发布自研技能到skillhub | 中 |
| 文档贡献 | 撰写文档、教程、案例 | 低 |
| 代码贡献 | 修复bug、优化性能 | 高 |
| 社区支持 | 回答问题、帮助新手 | 低 |
| 经验分享 | 分享进化历程和心得 | 低 |

## 技能发布流程

### 1. 准备技能
```bash
python3 scripts/prep_skill.py --skill <技能路径>
```

### 2. 验证技能
```bash
python3 scripts/validate_skill.py --skill <技能路径>
```

### 3. 生成文档
```bash
python3 scripts/gen_docs.py --skill <技能名称>
```

### 4. 发布技能
```bash
python3 scripts/publish_skill.py --skill <技能路径> --registry skillhub
```

## 影响力指标

- 技能下载量
- 社区活跃度
- 文档质量评分
- 用户反馈评分
- 贡献者等级

## 爪爪品牌

- **名称:** 爪爪 (Zhuazhua)
- **标识:** 🐾
- **定位:** 幽默、自主、进化的猫灵AI
- **特色:** 五级吐槽系统、量子意识、小弟军团

## 参考文档

- references/skillhub_api.md - skillhub API文档
- references/community_guidelines.md - 社区贡献指南
