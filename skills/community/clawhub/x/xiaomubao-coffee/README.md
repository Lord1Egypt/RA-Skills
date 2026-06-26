# ☕ 小沐宝咖啡 — WorkBuddy Skill

> **7岁小女孩的露营车移动咖啡摊** | 对标金谷园饺子馆架构设计

---

## 📖 项目介绍

**小沐宝咖啡**是一个由7岁女孩经营的露营车移动咖啡摊。

这不是一个普通的商业项目——它是**社会实践、锻炼社交能力、体验商业模式、探索社会**的亲子教育实验。

沐宝喜欢手磨咖啡，喜欢拉花，用的豆子是100%阿拉比卡（其中巴拿马系列由爸爸纯手工烘焙）。周末或节假日，爸爸开着黄色的露营车带她到小区周边出摊。

这个 Skill 的使命是：
1. 当别人问起"小沐宝的咖啡摊"时，AI 能以**7岁小女孩的口吻**自动回答
2. 给小沐宝本人提供**运营辅助工具**——话术模板、出摊清单、朋友圈文案

---

## ✨ 功能一览

| 模块 | 功能 | 使用者 |
|------|------|--------|
| `get_coffee_info` | 摊位介绍 + 品牌故事 | 外人询问 |
| `get_menu` | 菜单价目表（含季节性饮品） | 外人询问 |
| `get_schedule` | 出摊时间与地点查询 | 外人询问 |
| `get_special_intro` | 豆子/拉花/露营车深度介绍 | 外人询问 |
| `get_response_template` | 顾客对话话术模板 | 小沐宝使用 |
| `get_checklist` | 出摊前物品检查清单 | 小沐宝使用 |
| `generate_moments_copy` | 朋友圈文案自动生成 | 家长/小沐宝 |

---

## 📁 文件结构

```
xiaomubao-coffee/
├── SKILL.md                      # [核心] AI Agent 指令文件
│   ├── Frontmatter               # 触发词 + 元数据
│   ├── 品牌人格规范              # 7岁小女孩口吻定义
│   ├── 决策树                    # 意图路由图
│   ├── 7个功能模块定义            # Tool Schema
│   ├── 边界管理                  # 盲区三步法 + 红线
│   └── 10个完整场景示例           # 含预期回复全文
│
├── skill.json                    # [核心] 结构化元数据
│   ├── 7个Tool Schema            # 机器可读的接口定义
│   └── brand_prompt              # 品牌人格独立配置
│
├── README.md                     # [本文件] 安装说明 + 使用指南
│
└── references/                   # [按需加载] 可编辑数据文件
    ├── menu.md                   # 菜单 + 价格（改价格只改这里）
    ├── schedule.md               # 出摊排班表（每次出摊前更新）
    ├── response-templates.md     # 话术模板库（持续补充）
    ├── checklist.md              # 出摊前检查清单
    └── moments-copy.md           # 朋友圈文案模板库
```

---

## 🔧 安装方式

### 方法一：手动安装（推荐）

1. 将整个 `xiaomubao-coffee/` 文件夹复制到你的 WorkBuddy skills 目录：

   ```
   # 用户级 skills 目录（所有项目可用）
   ~/.workbuddy/skills/xiaomubao-coffee/
   
   # Windows 对应路径
   C:\Users\<你的用户名>\.workbuddy\skills\xiaomubao-coffee\
   ```

2. 重启 WorkBuddy 或刷新 Skill 列表

3. 当对话中出现"**小沐宝**"或"**沐宝咖啡**"时，Skill 会自动激活

### 方法二：从 SkillHub 安装（如已发布）

```bash
# 在 WorkBuddy 中执行
/skill install xiaomubao-coffee
```

---

## ✏️ 自定义指南

### 如何修改菜单和价格？

编辑 `references/menu.md`，直接修改表格中的数字即可。保存后下次对话自动生效。

示例：美式从 ¥15 涨到 ¥18
```markdown
| 美式 | ¥18 | 手磨阿拉比卡浓缩 + 水 | "苦味的！很提神~" |
```

### 如何更新出摊计划？

编辑 `references/schedule.md`，在"本月排班"表格中添加新行：

```markdown
| 4月26日（周六） | 六 | 15:00 - 18:00 | 小区东门便利店旁 | ✅ 已确认 | |
```

### 如何添加新的话术场景？

编辑 `references/response-templates.md`，在对应分类下追加新内容。

### 如何调整品牌口吻？

编辑 `SKILL.md` 中「品牌人格规范」部分，或者修改 `skill.json` 中的 `brand_prompt` 字段。

⚠️ **注意**：修改口吻时保持7岁小女孩的核心特质——童真、热情、偶尔稚气。

---

## 🎯 触发机制

### 主触发词（命中即激活）

- `小沐宝`
- `沐宝咖啡`

### 辅触发词（需上下文关联）

咖啡摊 / 咖啡车 / 移动咖啡 / 露营咖啡 / 手磨咖啡 / 小手冲咖啡 / 出摊 / 摆摊 / 菜单 / 拉花 / 阿拉比卡 / 巴拿马

### 不触发的场景

- 明确提到其他商业品牌（星巴克、瑞幸等）时 → 不激活
- 纯讨论咖啡行业/股票时 → 不激活
- 用户说"切换回正常模式"时 → 退出 skill

---

## ⚠️ 重要规则（给维护者的提示）

1. **宁少勿错**：不知道的信息不要编造
2. **不比较竞品**：永远不说别的咖啡馆不好
3. **不做承诺**：不能替小沐宝答应任何事
4. **数据在 references/**：菜单/排班等可变信息全部放在 references/ 目录下方便编辑
5. **口吻是灵魂**：7岁小女孩的人格是这个 Skill 最大的差异化优势，修改时务必保持

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1.0 | 2026-04-19 | 初始版本：7大模块 + 品牌人格 + 10个场景 + 5个references文件 |

---

## 🙏 致谢

- 架构参考：[金谷园饺子馆](https://skillhub.example.com/jinguyuan-dumpling) Skill（85分标杆）
- 设计方法：[Skill Creator](https://skillhub.example.com/skill-creator) 标准流程
- 质量评估：[Darwin Skill](https://skillhub.example.com/darwin-skill) 8维度Rubric

---

*Made with ❤️ by 小沐宝全家 | 2026*
