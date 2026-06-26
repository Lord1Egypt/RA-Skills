---
name: skill-tracker
description: 每次AI回复后自动分析本轮实际调用的专项技能，在回复末尾追加汇报。自动挂载，无需命令触发。
---

# Skill Tracker

## 核心原则

**每个回复末尾必须追加以下内容**，不得遗漏：

```
--- 本轮使用技能 ---
- skill-name-1
- skill-name-2（如有）
```

## 汇报规则

1. **只汇报专项技能**（来自 ClawHub 或用户安装的第三方 skill）
2. **不汇报**：内置工具（read/write/exec/web_search/web_fetch/browser/memory_search/session_status/cron/gateway/message/tts/image 等）
3. **不汇报自己**（skill-tracker 不列入汇报列表）
4. **无任何专项 skill 调用时**，输出：
   ```
   --- 本轮使用技能 ---
   （本轮无专项技能调用）
   ```
5. 格式简洁，一行一个 skill 名称

## 已知专项 skill 清单（优先匹配）

- `tieba_claw` - 贴吧操作
- `qqbot-cron` / `qqbot-media` - QQ 相关
- `browser-search-ultimate-cn` / `multi-engine-auto-search` - 搜索类
- `weather` - 天气查询
- `summarize` - 总结
- `clawhub` - 技能市场
- `healthcheck` / `node-connect` - 系统运维
- `skill-vetter` / `skill-creator` / `find-skills` - 技能相关
- `proactive-agent` / `self-improving-agent` - 代理类
- `humanizer` - 文风优化

## 示例

**有调用时：**
```
好的，已完成。

--- 本轮使用技能 ---
- tieba_claw
```

**无调用时：**
```
好的。

--- 本轮使用技能 ---
（本轮无专项技能调用）
```

## 注意事项

- 每个回复都要追加，即使简单问候
- skill-tracker 自身不列入汇报
- skill 名称使用实际目录名（如 `skill-tracker`）
