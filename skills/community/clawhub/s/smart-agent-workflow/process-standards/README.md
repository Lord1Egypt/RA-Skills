# 团队规范索引 README

> 所有团队成员必读
> 最后更新：2026-03-28
> 这是你的导航地图，找不到规范时先看这里

---

## 🚀 新成员必读（按顺序）

**第一天：**
1. 本文件（README.md）— 了解规范体系
2. TEAM_PROTOCOL.md — 团队协作协议
3. 你的 SOUL.md — 了解自己的角色

**第二天：**
4. WBS_RULES_v2.0.md — 任务拆分规范
5. TASK_REPORTING_v2.0.md — 汇报规则
6. SECURITY_CHECK.md — 安全检查

**第三天：**
7. CONTEXT_MANAGEMENT_v2.0.md — Context 控制
8. 项目专属规范（如 Tiqmo）

---

## 📋 核心规范（所有人必须遵守）

### 1. 任务执行

| 文档 | 路径 | 用途 | 优先级 |
|------|------|------|--------|
| WBS 拆分规范 | `core/WBS_RULES_v3.0.md` | 任务拆分、P0/P1分级 | ⭐⭐⭐ |
| 任务汇报规范 | `core/TASK_REPORTING_v3.0.md` | 汇报时机、格式（简化版） | ⭐⭐⭐ |
| 安全检查规范 | `core/SECURITY_CHECK.md` | 操作前安全检查 | ⭐⭐⭐ |

### 2. 协作通信

| 文档 | 路径 | 用途 | 优先级 |
|------|------|------|--------|
| 团队协议 | `core/TEAM_PROTOCOL.md` | 通信协议、Task Brief | ⭐⭐⭐ |
| Context 管理 | `core/CONTEXT_MANAGEMENT_v2.0.md` | Token 控制、优化 | ⭐⭐ |

### 3. 项目专属

| 文档 | 路径 | 用途 | 优先级 |
|------|------|------|--------|
| Tiqmo 流程 | `projects/tiqmo/FLOW.md` | Tiqmo 项目流程 | ⭐⭐ |
| Coco English 流程 | `projects/coco-english/FLOW.md` | Coco English 项目流程 | ⭐⭐ |

---

## 📝 模板文件（直接复制使用）

| 模板 | 路径 | 用途 |
|------|------|------|
| Task Brief 模板 | `templates/task_brief_template.md` | 跨 agent 传递任务 |
| 汇报模板 | `templates/report_template.md` | 任务汇报 |
| WBS 拆分模板 | `templates/wbs_template.md` | 任务拆分方案 |
| 安全检查模板 | `templates/security_check_template.md` | 操作前安全检查 |

---

## 🗂️ 文档结构

```
workspace-shared/
├── README.md（本文件，索引）
├── core/（核心规范，所有人必须遵守）
│   ├── WBS_RULES_v2.0.md
│   ├── CONTEXT_MANAGEMENT_v2.0.md
│   ├── TASK_REPORTING_v2.0.md
│   ├── SECURITY_CHECK.md
│   └── TEAM_PROTOCOL.md
├── projects/（项目专属规范）
│   ├── tiqmo/
│   │   ├── FLOW.md
│   │   └── SKILL.md
│   └── coco-english/
│       └── FLOW.md
├── templates/（模板文件）
│   ├── task_brief_template.md
│   ├── report_template.md
│   ├── wbs_template.md
│   └── security_check_template.md
├── tasks/（任务追踪）
│   └── TQ-YYYYMMDD-XXX.md
├── logs/（日志）
│   └── security_log.md
└── archive/（已废弃文档）
```

---

## 🔍 快速查找

### 我想知道...

**如何拆分任务？**
→ `core/WBS_RULES_v2.0.md`

**如何汇报进度？**
→ `core/TASK_REPORTING_v2.0.md`

**如何检查安全？**
→ `core/SECURITY_CHECK.md`

**如何传递任务？**
→ `core/TEAM_PROTOCOL.md` + `templates/task_brief_template.md`

**如何控制 Context？**
→ `core/CONTEXT_MANAGEMENT_v2.0.md`

**Tiqmo 项目怎么做？**
→ `projects/tiqmo/FLOW.md`

---

## 📊 文档版本管理

### 版本号规则

- **v1.0** - 初始版本
- **v1.1** - 小修改（修复错误、补充说明）
- **v2.0** - 大改动（新增机制、重构流程）

### 文档更新流程

1. **修改文档**
   - 更新内容
   - 更新版本号
   - 更新"最后更新"日期
   - 在底部"版本历史"记录变更

2. **通知团队**
   - 在团队群发通知
   - 说明变更内容
   - 标注影响范围

3. **废弃旧版本**
   - 旧版本移到 `archive/`
   - 在索引中标注"已废弃"

---

## 🎯 使用场景速查

### 场景1：收到新任务

```
1. 读取 WBS_RULES_v2.0.md
2. 判断是否需要拆分
3. 输出拆分方案（使用 wbs_template.md）
4. 执行前检查安全（使用 SECURITY_CHECK.md）
5. 每批次完成后汇报（使用 TASK_REPORTING_v2.0.md）
```

### 场景2：需要传递任务给其他 agent

```
1. 读取 TEAM_PROTOCOL.md
2. 使用 task_brief_template.md 创建 Task Brief
3. 通过 sessions_send 发送
```

### 场景3：Context 使用率过高

```
1. 读取 CONTEXT_MANAGEMENT_v2.0.md
2. 评估是否需要创建 Task Brief
3. 如果需要，使用 task_brief_template.md
4. 提示用户开新对话
```

### 场景4：遇到问题卡住

```
1. 读取 TASK_REPORTING_v2.0.md
2. 使用"问题上报"模板
3. 立即上报组长
```

---

## 📈 规范执行检查清单

### 每次任务前

```markdown
- [ ] 是否读取了相关规范？
- [ ] 是否需要拆分任务？
- [ ] 是否输出了拆分方案？
- [ ] 是否执行了安全检查？
```

### 每次任务中

```markdown
- [ ] 是否在每个断点汇报？
- [ ] 是否监控 Context 使用率？
- [ ] 是否遇到问题立即上报？
```

### 每次任务后

```markdown
- [ ] 是否输出了最终汇报？
- [ ] 是否使用了标准格式？
- [ ] 是否包含关键数据？
- [ ] 是否说明了下一步？
```

---

## 🆘 常见问题

### Q1: 找不到某个规范怎么办？

**A:** 先看本文件（README.md），如果还是找不到，问组长。

### Q2: 规范太多，记不住怎么办？

**A:** 不需要全记住，用到时查。重点记住：
- WBS 拆分规范
- 任务汇报规范
- 安全检查规范

### Q3: 规范和实际情况不符怎么办？

**A:** 
1. 先按规范执行
2. 记录问题
3. 向组长反馈
4. 讨论后更新规范

### Q4: 新项目需要新规范吗？

**A:** 
1. 核心规范（core/）适用所有项目
2. 项目专属规范放在 projects/[项目名]/
3. 使用 PROJECT_FLOW_TEMPLATE.md 创建

---

## 📞 联系方式

**规范相关问题：** 找组长（zuzhang）
**技术问题：** 找 Ethon（default）
**测试问题：** 找 Lily（bot2）
**需求问题：** 找产品（chanpin）

---

**版本历史：**
- v1.0 (2026-03-28) - 初始版本，建立索引体系
