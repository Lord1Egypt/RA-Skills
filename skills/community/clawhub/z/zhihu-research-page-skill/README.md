# 一句话生成知乎高质量回答网页（可自由剪裁）

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-v22-blue)](SKILL.md)

> 通过大规模联网搜索自动创建知乎风格的深度知识网页，样式高度还原 zhihu.com。默认生成含 10 个回答的多答主模拟回答页面，含 ≥10 万有效中文字和 ≥500 次真实搜索引用。支持手动裁剪为任意比例版本，多次执行自动创建带版本号的独立文件夹。

---

## 快速开始

```
# npx安装
npx skills add https://github.com/timeRATE-966/zhihu-research-page-skill
```

## 用例

```
/zhihu-research-page 执行2%版本
主题：什么是 Harness Engineering？
```

```
/zhihu-research-page 执行100%的v2版本
主题：国际象棋怎么学？代数记谱法、西西里、西班牙主流开局这些是什么？
```

```
/zhihu-research-page 执行200%的v2版本
主题：各种调式的流行歌曲都有什么特点，它们各有什么代表作？
```

> ⚠️ **重要**：100% 版本约需 100 分钟且 token 消耗巨大，强烈建议先生成 2% 版本检验效果。

## 核心特性

| 特性                     | 说明                                                                |
| ------------------------ | ------------------------------------------------------------------- |
| **大规模搜索驱动** | 默认 ≥500 次真实 WebSearch，所有事实附可点击来源链接               |
| **知乎风格还原**   | CSS 高度还原 zhihu.com 设计，含顶栏/侧栏/问题头/答主块/操作条       |
| **10 个回答多答主**    | 每个回答独立答主身份与头像，模拟真实知乎多视角回答                      |
| **自由剪裁**       | 支持任意 N% 版本（1% ~ 500%），等比缩减字数/搜索/回答数             |
| **版本管理**       | 多次执行自动创建`v{N}_{pct}pct/` 独立文件夹，主题保持一致         |
| **教程模式**       | 自动识别学习/教程类主题，提炼答主背景，写作目标面向"跟着做就能上手" |
| **自动自查**       | 组装阶段自动检测`<code>` 标签、CSS 颜色泄漏、字数达标等 5 项      |

## 剪裁比例参考

| 比例 | 搜索次数 | 总字数    | 回答数 | 耗时      | 适用         |
| ---- | -------- | --------- | ------ | --------- | ------------ |
| 2%   | ≥10     | ≥2,000   | 3      | ~2 分钟   | 极速检验效果 |
| 5%   | ≥25     | ≥5,000   | 3      | ~5 分钟   | 快速验证     |
| 30%  | ≥150    | ≥30,000  | 3      | ~30 分钟  | 中速草稿     |
| 100% | ≥500    | ≥100,000 | 10     | ~100 分钟 | 完整版       |
| 200% | ≥1,000  | ≥200,000 | 20     | ~200 分钟 | 深度加量     |

## 安装

### npx安装

```
npx skills add https://github.com/timeRATE-966/zhihu-research-page-skill
```

### 手动安装

克隆后手动放置于各Agent的skill目录，这里以Claude Code为例。

```bash
git clone https://github.com/timeRATE-966/zhihu-research-page-skill.git
cp -r zhihu-research-page-skill ~/.claude/skills/zhihu-research-page
```


## 文件结构

```
zhihu-research-page/
├── SKILL.md                          # 核心 Skill 定义
├── README.md                         # 本文件
├── LICENSE                           # MIT
├── CHANGELOG.md                      # 版本更新日志
├── TROUBLESHOOTING.md                # 15 类高频异常及处理
├── .claude-plugin/
│   └── marketplace.json              # Claude Code 插件市场元数据
├── templates/
│   ├── writing_agent_prompt.md       # 回答撰写代理 Prompt
│   ├── search_agent_prompt.md        # 搜索代理 Prompt
│   └── author_block.html             # 统一答主块模板
├── scripts/
│   ├── assemble.py                   # 拼接与自查脚本
│   ├── scan_html.py                  # HTML <code> 标签预扫描
│   ├── wordcount_check.py            # 独立字数核验
│   └── inline_images.py              # 单文件打包（图片 base64 内嵌）
├── examples/
│   ├── basic.md                      # 基础用法示例
│   └── advanced.md                   # 进阶用法示例
├── tests/
│   └── test.md                       # 自检清单
└── references/
    └── css-template.css              # 知乎风格 CSS 模板
```

## 触发词

生成知乎风网页、知识专题页、深度研究网页、产品百科页、知乎风研究报告、学习路径、教程页面、怎么做、入门指南

## License

MIT
