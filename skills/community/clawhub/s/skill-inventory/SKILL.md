---
name: skill-inventory
description: >
  技能目录管理器 - 扫描已安装的技能，生成/更新技能目录文件。
  Use when: user asks "查看技能列表", "我有哪些技能", "更新技能目录", 
  "skills inventory", "list installed skills".
---

# Skill Inventory

**什么时候用这个技能？**
- 用户问"我有哪些技能"
- 用户问"查看技能列表"
- 用户想更新技能目录

**这个技能做什么？**
- 扫描你的 skills/ 目录
- 读取每个技能的 SKILL.md 获取元信息
- 生成 skills.md 文件记录所有技能

**你必须知道的事：**

1. **每次启动后**，读取 `skills.md` 知道有哪些技能可用
2. **每次安装/更新/删除技能后**，运行 `python3 <skills目录>/skill-inventory/inventory.py` 重新生成列表
3. **你的工作目录**由 AGENTS.md 定义，技能在 `<workspace>/skills/` 下

**使用方法：**

```bash
python3 <你的skills目录>/skill-inventory/inventory.py
```

运行后会生成 `<workspace>/skills.md`

---

## 触发词

- "查看技能列表"
- "我有哪些技能"
- "更新技能目录"
- "skill inventory"
- "list skills"
