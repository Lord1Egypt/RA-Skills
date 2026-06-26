# Session Guardian v2.0 升级日志

发布日期：2026-03-05

## 核心升级：从"保护单个session"到"保护整个军团协作网络"

### 新增功能

#### 1. 军团协作链路追踪 🔗
- 追踪 sessions_send 调用链路
- 可视化 King → 团长 → 成员 的协作过程
- 生成协作图和详细记录

**使用**：
```bash
bash scripts/collaboration-tracker.sh trace "任务名"
bash scripts/collaboration-tracker.sh graph "任务名"
```

#### 2. 智能备份策略 📦
- 区分固定Agent (main.jsonl) 和临时Subagent
- 固定Agent：5MB限制，保留90天
- 临时Subagent：1MB限制，保留7天
- 保护重要记忆，激进清理临时数据

**配置**：
```bash
FIXED_AGENT_SESSION_LIMIT_MB=5
SUBAGENT_SESSION_LIMIT_MB=1
FIXED_AGENT_KEEP_DAYS=90
SUBAGENT_KEEP_DAYS=7
```

#### 3. 知识库自动沉淀 📚
- 自动提取最佳实践（✅标记）
- 自动提取常见问题（❌标记）
- 生成结构化知识库

**使用**：
```bash
bash scripts/knowledge-extractor.sh extract dev-lead
bash scripts/knowledge-extractor.sh extract-all
```

#### 4. 协作健康度评分 📊
- 评估通信频率、Agent状态
- 量化协作质量（0-100分）
- 自动生成优化建议

**使用**：
```bash
bash scripts/collaboration-health.sh report
```

### 改进功能

#### health-check.sh
- ✅ 升级为v2.0智能策略
- ✅ 自动识别固定Agent和临时Subagent
- ✅ 差异化清理策略

### 新增文件

```
scripts/
├── collaboration-tracker.sh      # 协作链路追踪
├── knowledge-extractor.sh        # 知识提取
├── collaboration-health.sh       # 协作健康度评分
└── config.sh                     # 新增v2.0配置项

Assets/
├── SessionBackups/
│   └── collaboration/            # 协作链路记录
├── Knowledge/                    # 知识库（新增）
└── CollaborationReports/         # 协作报告（新增）
```

### 测试结果

✅ 智能备份策略：成功识别并清理临时Subagent（2MB）
✅ 知识提取：成功提取dev-lead的36KB最佳实践和17KB常见问题
✅ 协作健康度：成功生成健康报告
✅ 配置自动修复：成功修复3个agent的defaultModel配置

### 兼容性

- ✅ 完全向后兼容v1.0
- ✅ 所有v1.0功能正常运行
- ✅ 新功能可选启用

### 下一步

**阶段2（计划中）**：
- 智能总结升级（区分固定agent和协作）
- 每日总结体现军团协作过程

**阶段3（计划中）**：
- 完整文档和使用案例
- 性能优化和测试

---

版本：v2.0.0
创建者：King
状态：已完成阶段1核心功能
