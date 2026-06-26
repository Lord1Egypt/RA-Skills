# SkillPilot 重命名记录

**日期**: 2026-03-17  
**原因**: skillhub 已有 skill-router 名称冲突

---

## 重命名详情

### 旧名称
- **名称**: skill-router
- **问题**: 与 skillhub 现有技能重名

### 新名称
- **名称**: **SkillPilot**
- **含义**: Skill + Pilot = 技能领航员
- **寓意**: 引导选择最优技能路径

---

## 变更文件

| 文件 | 变更 |
|------|------|
| `skills/skill-router/` | → `skills/skill-pilot/` (目录重命名) |
| `SKILL.md` | 更新 name: skill-pilot, emoji: 🧭 |
| `__init__.py` | 更新函数名 create_pilot/get_pilot |
| `scripts/*.py` | 批量替换 SkillRouter → SkillPilot |
| `RELEASE.md` | 更新标题和技能信息 |

---

## 验证结果

✅ **测试通过**:
- 技能发现：33 个技能
- 目录结构：正常
- 导入测试：正常
- 功能测试：正常

---

## 发布检查

### 发布前准备
- [x] 目录重命名完成
- [x] SKILL.md 更新
- [x] 代码注释更新
- [x] 测试验证通过
- [x] RELEASE.md 更新

### 发布命令
```bash
cd ~/.openclaw/workspace
skillhub publish skills/skill-pilot
```

---

*重命名完成时间：2026-03-17 02:00 UTC*
