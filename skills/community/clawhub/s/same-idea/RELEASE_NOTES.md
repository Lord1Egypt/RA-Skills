# Release Notes

## v1.0.0 - Initial Release

### 首次发布 🎉

Same Idea Skill 是一个帮助你在阅读笔记中发现知识联系的 OpenClaw 技能。

### 核心功能

- **智能关键词提取** - 自动从输入文本中提取核心概念，支持中英文混合
- **多笔记库搜索** - 同时支持 Logseq 和 Obsidian vault
- **相关性评分排序** - 基于关键词匹配、引用标记、来源标记的智能排序
- **来源追溯** - 返回匹配结果时包含书籍、作者信息

### 包含内容

```
same-idea/
├── SKILL.md              # OpenClaw 技能定义
├── README.md             # 完整项目文档
├── CONTRIBUTING.md       # 贡献指南
├── LICENSE               # MIT 许可证
└── scripts/
    ├── find_similar.py   # 核心搜索脚本
    └── release.sh        # 发布辅助脚本
```

### 使用示例

输入一个想法：

```
"复利效应不仅适用于金钱，也适用于知识和关系"
```

获得共鸣发现：

```
## 共鸣发现

### 1. 知识复利
> "每天进步1%，一年后你会进步37倍"
**来源**: 《掌控习惯》 - 詹姆斯·克利尔
**共鸣点**: 强调微小积累的巨大效应，与你提到的知识复利概念一致
```

### 依赖项

- Python 3.6+
- ripgrep (可选，但推荐安装以获得更快的搜索速度)

### 安装

```bash
# 方法一：使用 clawhub
clawhub install same-idea

# 方法二：手动安装
git clone https://github.com/jianghaidong/same-idea-skill.git
cp -r same-idea-skill ~/.openclaw/workspace/skills/same-idea
```

### 已知限制

- 当前使用关键词匹配，未来可集成语义搜索
- 仅支持 Logseq 和 Obsidian，其他笔记软件欢迎贡献支持
- 搜索依赖笔记中的引用格式（如 `> ` 书名号等）

### 下一步计划

- [ ] 集成向量嵌入进行语义搜索
- [ ] 支持 Notion、Roam Research 等更多笔记软件
- [ ] 添加配置文件支持自定义 vault 路径
- [ ] 提供搜索结果的缓存机制

---

感谢使用 Same Idea Skill！如有问题或建议，欢迎在 [GitHub Issues](https://github.com/jianghaidong/same-idea-skill/issues) 中反馈。