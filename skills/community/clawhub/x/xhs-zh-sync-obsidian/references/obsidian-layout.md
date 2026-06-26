# Obsidian 目录与分类

导出目标：

```text
<obsidian.vault>/<obsidian.base_dir>/<platform>/<level1>/<level2>/<title-id>.md
```

示例：

```text
~/obsidian/互联网笔记/小红书/科技-AI/AI工具与工作流/OpenClaw 工作流-abc123.md
~/obsidian/互联网笔记/知乎/阅读-知识/长文与观点/一篇回答-123456.md
```

每篇笔记包含 YAML frontmatter：

```yaml
title: "..."
source: "小红书"
source_id: "..."
source_url: "..."
category_level1: "..."
category_level2: "..."
author: "..."
generated_at: "..."
tags:
  - "小红书"
  - "小红书/科技-AI"
  - "小红书/科技-AI/AI工具与工作流"
```

分类规则文件默认是：

```text
~/.config/social-favorites-to-obsidian/classify_rules.yaml
```

规则格式：

```yaml
rules:
  - level1: "科技-AI"
    level2: "AI工具与工作流"
    keywords: ["OpenClaw", "智能体", "Obsidian"]
```

第一条命中的规则生效。没有命中时进入 `其他/待整理`。
