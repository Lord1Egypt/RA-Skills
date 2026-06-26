# YumFu 重命名完成 (2026-04-01 22:23)

## 改动记录

### 目录结构
- ✅ `~/clawd/skills/yummud/` → `~/clawd/skills/yumfu/`
- ✅ `~/clawd/memory/yummud/` → `~/clawd/memory/yumfu/`
- ✅ `~/clawd/memory/yummud-save.json` → `~/clawd/memory/yumfu-save.json`
- ✅ `~/.openclaw/media/outbound/yummud/` → `~/.openclaw/media/outbound/yumfu/`

### 文件内容
- ✅ SKILL.md - 所有 `yummud` → `yumfu`
- ✅ SKILL.md - 所有 `YumMUD` → `YumFu`
- ✅ SKILL.md - 所有 `/mud` → `/yumfu`
- ✅ README.md - 所有 `yummud` → `yumfu`
- ✅ README.md - 所有 `YumMUD` → `YumFu`
- ✅ game-data.md - 所有 `yummud` → `yumfu`
- ✅ game-data.md - 所有 `YumMUD` → `YumFu`

### 触发指令
- ✅ `/yumfu` (主指令)
- ✅ `/江湖` (中文别名)
- ❌ 移除 `/mud` 兼容

## 验证

```bash
# Skill 目录
ls ~/clawd/skills/yumfu/
# 输出: README.md  SKILL.md  game-data.md

# 存档
ls ~/clawd/memory/yumfu*
# 输出: 
#   yumfu-save.json
#   yumfu/saves/
#   yumfu/history/

# 图片输出
ls ~/.openclaw/media/outbound/yumfu/
# 输出: (空目录，等待游戏生成)
```

## 当前状态

**准备就绪！** ⚔️

玩家可以使用以下指令开始游戏：
- `/yumfu start` - 开始新游戏
- `/yumfu continue` - 继续游戏
- `/yumfu help` - 查看帮助
- `/江湖 开始` - 中文开始
