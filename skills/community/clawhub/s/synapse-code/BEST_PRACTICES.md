# Synapse Skills 最佳实践

> **版本**: v1.1.0  
> **最后更新**: 2026-04-08  
> **适用对象**: 开发者、团队负责人、项目经理

---

## 📖 核心原则

### 1. 知识沉淀优先

**理念**: 开发不仅是写代码，更是知识积累的过程

```bash
# ❌ 只交付代码
/synapse-code run project "实现功能"  # 结束

# ✅ 沉淀知识
/synapse-code run project "实现功能"
/synapse-code log project            # 记录经验
/synapse-code query project --task-type feature  # 复用知识
```

---

### 2. 选择合适的模式

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| 修复小 bug | standalone | 快速交付，无需复杂流程 |
| 日常功能 | lite | 平衡效率和质量 |
| 大型模块 | full | 严格质量把控 |
| 复杂任务 | 并行模式 | 多 Agent 分工加速 |

---

### 3. 需求描述具体化

**模糊描述** (不推荐):
```bash
/synapse-code run project "做个功能"
```

**具体描述** (推荐):
```bash
/synapse-code run project "实现用户登录功能，使用 JWT 认证，支持邮箱和密码登录，需要后端 API 和前端页面"
```

**为什么**: 需求描述越具体，Agent 输出越准确

---

## 💻 代码开发最佳实践

### 1. 迭代式开发

```bash
# 第 1 轮：需求分析
/synapse-code run project "分析登录功能需求，输出需求文档"

# 第 2 轮：架构设计
/synapse-code run project "设计登录功能技术方案，包括 API 定义"

# 第 3 轮：代码实现
/synapse-code run project "实现登录功能代码，包括前后端"

# 第 4 轮：质量检查
/synapse-code run project "对登录功能进行测试和代码审查"
```

---

### 2. 使用 Git 管理

```bash
# 每次 Pipeline 前创建分支
git checkout -b feature/login

# Pipeline 完成后审查代码
git diff

# 确认无误后提交
git add .
git commit -m "feat: 实现用户登录功能"
```

---

### 3. 知识复用

```bash
# 查询历史类似功能
/synapse-code query project --contains "登录" --task-type feature

# 参考历史实现
cat .synapse/memory/feature/2024-01-15T10-30-00-login-feature.md

# 避免重复踩坑
/synapse-code query project --task-type bugfix --contains "认证"
```

---

## 📚 知识库建设最佳实践

### 1. 资料摄取频率

**推荐**: 每天/每周固定时间批量 ingest

```bash
# 周末批量摄取本周收藏的文章
for article in ~/clippings/2026-W15/*.md; do
    /synapse-wiki ingest ~/Wiki "$article"
done
```

---

### 2. 定期健康检查

```bash
# 每 ingest 10 次后运行 lint
/synapse-wiki lint ~/Wiki

# 修复发现的问题
# - 补充孤立页面的链接
# - 合并重复概念
# - 更新过时内容
```

---

### 3. 知识网络构建

**初期**: 大量摄取资料，建立基础
```bash
/synapse-wiki ingest ~/Wiki article1.md
/synapse-wiki ingest ~/Wiki article2.md
...
```

**中期**: 建立概念关联
```markdown
# 在 wiki/concepts/Prompt Engineering.md 中添加
## Related Concepts
- [[Few-Shot Learning]]
- [[Chain-of-Thought]]
- [[RAG]]
```

**后期**: 查询驱动完善
```bash
# 发现问题
/synapse-wiki query ~/Wiki "RAG 和 LLM Wiki 的区别"

# 补充缺失内容
# 创建新的概念页面或更新现有页面
```

---

## 🚀 Pipeline 使用最佳实践

### 1. 契约优先 (Contract-First)

**为什么**: ARCH 阶段生成的 OpenAPI/JSON Schema 是后续开发的唯一信任源

```bash
# ARCH 阶段输出
cat pipeline-workspace/ARCH/contracts/api.json

# DEV 阶段严格遵循契约
# 不随意修改接口定义
```

---

### 2. 真实验证

**为什么**: QA 阶段执行真实对抗测试，禁止模拟

```bash
# QA 阶段执行
- 边界测试 (boundary values)
- 安全测试 (security)
- 并发测试 (concurrency)
- 可靠性测试 (reliability)
```

---

### 3. 原子化原则

**约束**: 每个生成函数 ≤ 50 行

```python
# ✅ 推荐
def validate_user_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

# ❌ 不推荐 - 超过 50 行
def process_user_registration(data):
    # 100 行代码...
```

---

## 🔄 团队协作最佳实践

### 1. 统一项目结构

```
project/
├── .knowledge/          # Synapse 知识库
│   ├── CLAUDE.md
│   ├── log.md
│   └── index.md
├── .synapse/            # 记忆存储
│   └── memory/
│       ├── feature/
│       ├── bugfix/
│       └── refactor/
└── src/                 # 源代码
```

---

### 2. 代码审查流程

```bash
# 1. Pipeline 完成后查看摘要
cat /tmp/pipeline_summary.json

# 2. 审查生成的代码
git diff HEAD~1

# 3. 运行测试
python3 -m pytest tests/

# 4. 确认质量报告
cat pipeline-workspace/QA/qa_report.md
```

---

### 3. 知识共享

```bash
# 导出项目记忆
/synapse-code query project --json > knowledge-export.json

# 分享给团队
# 团队可以导入或查询历史记录
```

---

## 📊 效率提升技巧

### 1. 使用快捷键

```bash
# 定义 alias (添加到 ~/.zshrc)
alias sc-run='/synapse-code run'
alias sc-status='/synapse-code status'
alias sc-query='/synapse-code query'
alias sw-ingest='/synapse-wiki ingest'
alias sw-query='/synapse-wiki query'
```

---

### 2. 批量处理

```bash
# 批量运行 Pipeline
projects=("project-a" "project-b" "project-c")
for p in "${projects[@]}"; do
    /synapse-code run "$p" "需求描述"
done
```

---

### 3. 会话管理

```bash
# 保存当前会话状态
/synapse-code log project

# 下次会话恢复上下文
/synapse-code query project --recent-logs --limit 5
```

---

## 🔒 安全最佳实践

### 1. 敏感信息管理

```bash
# ❌ 不要提交
echo "API_KEY=secret123" >> config.json
git add config.json

# ✅ 正确做法
echo "API_KEY=<占位符>" >> config.template.json
echo "API_KEY=secret123" >> .env.local
echo ".env.local" >> .gitignore
```

---

### 2. 代码审查要点

```markdown
## 审查清单
- [ ] 是否有硬编码的密钥
- [ ] 是否有 SQL 注入风险
- [ ] 是否有 XSS 漏洞
- [ ] 是否有命令注入风险
- [ ] 是否有文件上传漏洞
```

---

### 3. 依赖管理

```bash
# 锁定依赖版本
{
  "dependencies": {
    "gitnexus": "1.5.3"  // 精确版本
  }
}

# 定期更新依赖
npm audit
npm update
```

---

## 📈 持续改进

### 1. 回顾会议

```markdown
## 每次 Pipeline 后回顾
- 什么做得好？
- 遇到什么问题？
- 下次如何改进？
```

---

### 2. 知识更新

```bash
# 定期查看 ROADMAP.md
cat ROADMAP.md

# 贡献改进建议
# https://github.com/ankechenlab-node/synapse-code/issues
```

---

### 3. 性能基准

```bash
# 记录 Pipeline 运行时间
time /synapse-code run project "需求"

# 建立基准
# - standalone: < 5 分钟
# - lite: < 15 分钟
# - full: < 60 分钟
```

---

## 📋 检查清单

### 项目启动前
- [ ] 确认项目是 git 仓库
- [ ] 运行 `/synapse-code init`
- [ ] 确认 config.json 配置正确
- [ ] 选择合适的 Pipeline 模式

### Pipeline 完成后
- [ ] 审查生成的代码
- [ ] 查看质量报告
- [ ] 运行测试验证
- [ ] 运行 auto-log 记录知识

### 知识库维护
- [ ] 定期 ingest 新资料
- [ ] 每 10 次 ingest 后运行 lint
- [ ] 补充概念关联
- [ ] 更新过时内容

---

## 📚 相关文档

- [AGENT_GUIDE.md](AGENT_GUIDE.md) - Agent 使用指南
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排查
- [TESTING.md](TESTING.md) - 测试指南
- [ROADMAP.md](ROADMAP.md) - 开发路线图

---

*最佳实践会持续更新，欢迎贡献你的经验*
