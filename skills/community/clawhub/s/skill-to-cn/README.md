# skill-to-cn

将任意 Claude Code 技能翻译为中文版本。

## 用途

当用户要求"汉化技能"、"翻译技能"、"把XX技能翻译成中文"、"创建技能的中文版"时使用此技能。

## 安装

将此技能目录放置在 Claude Code 的 skills 目录下：

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/zhouchang1988/skill-to-cn.git ~/.claude/skills/skill-to-cn
```

## 使用方法

在 Claude Code 中请求汉化技能：

```
请汉化 pdf-editor 技能
```

或者指定完整路径：

```
请将 /path/to/skill 翻译成中文
```

## 工作流程

1. 确认源技能路径
2. 运行翻译脚本生成骨架文件
3. Claude 完成所有标记内容的翻译
4. 验证汉化结果

## 输出结构

汉化后的技能目录位于 `~/.claude/skills/<技能名>-cn/`：

```
~/.claude/skills/<技能名>-cn/
├── SKILL.md          # 已翻译
├── README-cn.md      # README.md 的中文翻译（如存在）
├── scripts/          # 注释已翻译
├── references/       # 已翻译（如存在）
├── assets/           # 原样复制（如存在）
└── <其他文件>        # 原样复制
```

## 许可证

MIT License
