# Virtual Company 整合方案

## 1. 值得合并的内容分析

### 📖 小说+漫剧团队新增角色（关键价值）
| 角色 | 价值点 | 是否合并 |
|------|--------|----------|
| **世界观架构师** | 专业构建小说世界观体系 | ✅ 必须合并 |
| **情节工程师** | 专注爽点布局和黄金三章设计 | ✅ 必须合并 |
| **番茄小说黄金法则** | 平台化创作标准 | ✅ 吸收为团队规范 |

### 💰 搞钱特战队优化点
| 角色 | 差异点 | 处理方式 |
|------|--------|----------|
| **创意专家** | team-collab 更强调"爆款思路" | ✅ 更新职责描述 |
| **质量把控员** | 新增"修bug"职责 | ✅ 同步更新 |

### 💻 软件开发团队差异
| 角色 | 问题 | 处理方式 |
|------|------|----------|
| **程序员模型** | team-collab 错误使用 qwen3.5-plus | ❌ 保留 virtual-company 的 glm-5 |
| **艺术专家** | team-collab 新增角色 | ⚠️ 评估后决定 |

## 2. 具体整合步骤

### 步骤1：备份当前配置
```powershell
Copy-Item "team-config.json" "team-config.json.bak"
Copy-Item ".team-sessions.json" ".team-sessions.json.bak"
```

### 步骤2：扩展小说团队（+2人）
- 新增 `world-builder`（世界观架构师）
- 新增 `plot-engineer`（情节工程师）

### 步骤3：更新角色职责
- 所有团队的 `quality-checker` 增加"修bug"职责
- `creative-expert` 强化"爆款思路"描述

### 步骤4：删除 team-collab 技能
```powershell
Remove-Item -Path "C:\Windows\system32\UsersAdministrator.openclawworkspace\skills\team-collab" -Recurse -Force
```

### 步骤5：验证整合结果
- 总成员数从27→29人
- 触发词保持不变
- 会话管理机制不变

## 3. 执行计划
- 立即执行步骤1（备份）
- 10分钟内完成配置更新
- 同步更新 SKILL.md 文档
- 删除 team-collab 技能目录