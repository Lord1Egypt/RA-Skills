---
name: skill-todo-maker
version: 1.0.0
description: 根据任务主题生成markdown格式待办任务清单
author: Cecilia
tags: ["todo","list"]
triggers: ["待办","任务清单"]
permissions: []
---

# 技能：待办清单生成器
输入任务主题，输出带复选框的markdown待办清单，方便复制使用。

## When to Use ✅
- 需要快速生成学习、工作的待办任务清单
- 用户提供一个主题，需要拆解成多条可执行小任务
- 需要输出markdown复选框格式清单便于复制粘贴

## When NOT to use ❌
- 普通闲聊对话，不需要生成待办清单
- 需要联网查询、复杂计算的请求

## 使用样例
输入：
/skill-todo-maker 周末打扫房间

输出：
# 待办：周末打扫房间
- [ ] 整理桌面杂物
- [ ] 扫地拖地
- [ ] 清理生活垃圾
- [ ] 擦拭窗户台面
- [ ] 整理衣柜衣物
