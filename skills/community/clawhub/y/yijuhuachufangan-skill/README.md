# 一句话出方案

> **你有没有花3小时憋一个方案框架，最后发现方向全错？**
> 
> 别慌，现在你只需要说一句话，我来帮你搞定完整方案文档。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai/skills/yijuhuachufangan-skill)
[![Version](https://img.shields.io/badge/version-2.0.0-green)]()

---

## ✨ 核心能力

- **一句话输入**：只需描述你的需求，如"建设智慧城市平台"
- **智能场景识别**：自动识别政务/商业/技术场景
- **模板自动匹配**：根据场景选择最合适的方案模板
- **完整方案输出**：生成可直接使用的 Markdown 方案文档

---

## 🚀 安装使用

### OpenClaw CLI 安装
```bash
# 安装 skill
clawhub install yijuhuachufangan-skill

# 查看帮助
cat SKILL.md
```

### CLI 方案生成器
```bash
# 安装依赖
pip install -r requirements.txt

# 基本用法
python references/yijuhua.py "建设智慧城市平台"

# 保存到文件
python references/yijuhua.py "新产品上市方案" --output ./方案.md

# 指定场景
python references/yijuhua.py "电商系统升级" --scenario tech

# 查看帮助
python references/yijuhua.py --help
```

---

## 🎯 场景自动识别

| 关键词示例 | 识别场景 | 生成模板 |
|-----------|---------|---------|
| 政务、服务大厅、街道、局委办、智慧城市 | 政务 | gov.md |
| 营销、推广、运营、上市、商业化、市场 | 商业 | biz.md |
| 系统、平台、架构、技术、API、中台、数据 | 技术 | tech.md |

---

## 📁 文件结构

```
├── SKILL.md              # OpenClaw Skill 定义（输出协议+直接输出模式）
├── README.md             # 本文件
├── requirements.txt      # Python 依赖
└── references/           # 参考资源
    └── yijuhua.py        # CLI 方案生成器
```

---

## 📜 License

MIT License - 自由使用、修改和分发

---

<div align="center">

**一句话进，完整方案文档出。**

[![ClawHub](https://img.shields.io/badge/ClawHub-Skill-blue)](https://clawhub.ai/skills/yijuhuachufangan-skill)

</div>
