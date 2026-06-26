# skills-of-algorithm-learning-platform-builder

---

# 🧠 skills-of-algorithm-learning-platform-builder

<div style="background-color:#f8f4eb; padding: 16px 20px; border-radius:12px; border: 1px solid #e8dfcf;">
<strong>algorithm-learning-platform-builder</strong> 是一套面向 AI 智能体的结构化技能规范，
让 AI 自动生成 <span style="color:#a98345;">可交互、可视化、可直接运行</span> 的算法教学网页，
帮助零基础小白直观理解机器学习、优化算法、统计聚类等原理，
告别抽象公式，用 <span style="color:#a98345;">可操作、可计算、可看图</span> 的方式学习算法。
</div>

---

## 📁 项目架构

```text
algorithm-learning-platform-builder/
├── SKILL.md                   # 🧩 技能总入口：AI 执行工作流与规则
├── agents/
│   └── openai.yaml            # 🤖 智能体配置：名称、图标、主题色
├── references/                # 📚 全套教学规范与模板
│   ├── page-architecture.md           # 🏛️ 页面结构规范
│   ├── explanation-patterns.md        # 📐 公式与步骤讲解规范
│   ├── interaction-patterns.md        # 🎛️ 交互控件设计规则
│   ├── algorithm-page-template.md     # 🧾 单算法页面模板
│   ├── comparison-page-template.md    # 📊 多算法对比模板
│   ├── writing-rules.md              # ✍️ 教学文案规范
│   ├── algorithm-family-maps.md      # 🌱 算法家族分类
│   ├── platform-upgrade-rules.md      # 🚀 平台升级规则
│   ├── request-routing-rules.md       # 🧭 请求路由规则
|   ├──request-routing-rules.md
│   └── output-quality-checklist.md    # ✅ 输出质量检查清单
└── assets/
    └── html-starter-template.html     # 🧪 可直接运行 HTML 模板
```

---

## 🎯 解决的痛点

- 📉 **算法公式太抽象**
  → 强制 **公式四步讲解 + 数值代入计算**
- 🧠 **新手看不懂推导**
  → 固定教学流：**直觉 → 公式 → 步骤 → 图表**
- 📝 **纯文字记不住**
  → 自动生成 **滑块、步进器、下拉切换** 交互
- 🔀 **多个算法易混淆**
  → 一键生成 **对比页 + 对比图表 + 场景建议**
- 🧱 **自建学习平台麻烦**
  → 提供 **模块化、可扩展** 架构，开箱即用

---

## ✨ 主要生成能力

### 1. 📘 单算法教学页面
完整讲解单个算法，包含：直觉、公式、分步计算、交互控制、可视化图表、结果总结。

### 2. 📊 多算法对比教学页面
同一任务下横向对比：公式、参数、流程、效果、优缺点，并给出使用建议。

### 3. 🧩 可复用算法学习平台
稳定外壳 + 可切换算法模块，支持无限扩展，形成通用交互式学习平台。


---------------
1.Topsis单算法页面教学
<img width="2013" height="990" alt="image" src="https://github.com/user-attachments/assets/69eca7ca-e43f-4e70-97b1-49aa25668fab" />
<img width="2190" height="1071" alt="image" src="https://github.com/user-attachments/assets/46f1ca15-5c6c-421a-acf1-6633ea4e3664" />
<img width="2091" height="1370" alt="image" src="https://github.com/user-attachments/assets/2773f0a0-c677-4a32-b8ad-71a5160e064c" />
<img width="2265" height="1377" alt="image" src="https://github.com/user-attachments/assets/2eb7e17a-7d16-4745-90b0-d2d9527ca8f7" />
-----------------
2.梯度树多算法对比教学
<img width="2177" height="1352" alt="image" src="https://github.com/user-attachments/assets/15b8b221-15a8-4444-8f23-52033470e78b" />
<img width="2277" height="1329" alt="image" src="https://github.com/user-attachments/assets/77a962e0-1bad-4014-a252-a5779053f08f" />
<img width="2328" height="1290" alt="image" src="https://github.com/user-attachments/assets/bc93eebf-86e6-4d3d-8c82-2d02a49594ed" />
<img width="2421" height="1410" alt="image" src="https://github.com/user-attachments/assets/579510f1-af48-4de9-87af-5e4952f3fe6a" />
------------------
样例结果下载
[sample.zip](https://github.com/user-attachments/files/26608090/sample.zip)






