# 验收协议规范

本文档定义 SDD 工作流的标准化验收流程，确保主 agent 和 autonomous agent 之间的状态同步。

---

## 验收阶段定义

**触发时机**：Phase 7 (Implement) 完成后

**目标**：验证代码可运行性并输出标准化结果

---

## 验收流程

### 1. 执行验收检查

```bash
# 1. 语法检查
python3 -m py_compile app/*.py app/*/*.py

# 2. 测试验证
pytest tests/ -v

# 3. 服务启动
PYTHONPATH=. timeout 5 uvicorn app.main:app --port 8765 || true
```

### 2. 更新 progress.json

**必须**在验收完成后立即更新：

```json
{
  "projectName": "example-project",
  "currentPhase": "acceptance",
  "status": "completed",
  "startTime": "2026-03-13T09:00:00+08:00",
  "endTime": "2026-03-13T10:30:00+08:00",
  "completedTasks": [
    "constitution",
    "specify",
    "clarify",
    "plan",
    "tasks",
    "analyze",
    "implement",
    "acceptance"
  ],
  "acceptanceResults": {
    "syntaxCheck": "passed",
    "testResults": "18 passed, 2 warnings",
    "serviceStartup": "verified",
    "filesGenerated": 18
  }
}
```

### 3. 输出标准化信号

**必须**在终端输出明确的验收结果：

```
ACCEPTANCE_RESULT: PASS
```

或

```
ACCEPTANCE_RESULT: FAIL
```

**PASS 标准**：
- ✅ 语法检查通过
- ✅ 至少 1 个测试通过
- ✅ 服务能启动（即使无响应也视为通过）

**FAIL 场景**：
- ❌ 语法检查失败
- ❌ 0 个测试通过
- ❌ 服务启动失败（import 错误等）

---

## 状态同步规范

### 主 agent → autonomous agent

主 agent 启动 autonomous agent 时传递：

```json
{
  "projectPath": "/path/to/project",
  "sessionName": "dev-session",
  "currentPhase": "constitution"
}
```

### autonomous agent → 主 agent

Autonomous agent 通过以下方式同步状态：

1. **progress.json 更新**（必须）
   - 每个 phase 完成时更新
   - 验收完成时最终更新

2. **终端输出信号**（必须）
   - `ACCEPTANCE_RESULT: PASS|FAIL`

3. **错误通知**（按需）
   - 遇到无法自动修复的错误时通知主 agent

---

## 验收检查详细规范

### 语法检查

```bash
find . -name "*.py" -not -path "./.venv/*" -not -path "./__pycache__/*" | \
  xargs python3 -m py_compile
```

**通过标准**：所有文件编译成功，无 SyntaxError

### 测试验证

```bash
pytest tests/ -v --tb=short
```

**通过标准**：
- 至少 1 个测试通过
- 允许 warnings（如 deprecation warnings）

**最佳实践**：
- 核心功能测试**应该**全部通过
- 集成测试**可以**部分跳过（如依赖外部服务）

### 服务启动

```bash
PYTHONPATH=. timeout 5 uvicorn app.main:app --port 8765 &
UVICORN_PID=$!
sleep 3
curl -s http://localhost:8765/ || echo "Service started"
kill $UVICORN_PID 2>/dev/null
```

**通过标准**：
- uvicorn 进程能启动
- 无 import 错误
- 能响应 HTTP 请求（即使 404 也视为通过）

---

## 错误处理流程

### 可自动修复的错误

| 错误类型 | 自动修复方式 |
|---------|-------------|
| ModuleNotFoundError | `pip install <package>` |
| SyntaxError | 通知 autonomous agent 修复 |
| TestFailure | 通知 autonomous agent 修复 |

### 需人工介入的错误

| 错误类型 | 处理方式 |
|---------|---------|
| 依赖冲突 | 通知主 agent → 人工决策 |
| 外部服务不可用 | 通知主 agent → 人工决策 |
| 业务逻辑错误 | 通知主 agent → 人工决策 |

---

## 进度更新规范

### 更新时机

| Phase | 更新字段 |
|-------|---------|
| constitution | `currentPhase`, `completedTasks` |
| specify | `currentPhase`, `completedTasks` |
| clarify | `currentPhase`, `completedTasks` |
| plan | `currentPhase`, `completedTasks` |
| tasks | `currentPhase`, `completedTasks` |
| analyze | `currentPhase`, `completedTasks` |
| implement | `currentPhase`, `completedTasks` |
| acceptance | `currentPhase`, `status`, `endTime`, `acceptanceResults` |

### 状态字段说明

- `currentPhase`: 当前执行阶段
- `status`: `pending` | `in_progress` | `completed` | `failed`
- `completedTasks`: 已完成的阶段列表
- `acceptanceResults`: 验收检查结果（仅在 acceptance 阶段）

---

## 示例：完整验收流程

```bash
# 1. 进入项目目录
cd /path/to/project

# 2. 激活虚拟环境
source .venv/bin/activate

# 3. 语法检查
echo "=== Syntax Check ==="
find . -name "*.py" -not -path "./.venv/*" -not -path "./__pycache__/*" | \
  xargs python3 -m py_compile && echo "✅ Syntax check passed"

# 4. 测试验证
echo "=== Test Verification ==="
pytest tests/ -v --tb=short
TEST_RESULT=$?

# 5. 服务启动
echo "=== Service Startup ==="
PYTHONPATH=. timeout 5 uvicorn app.main:app --port 8765 &
UVICORN_PID=$!
sleep 3
curl -s http://localhost:8765/ > /dev/null && echo "✅ Service started"
kill $UVICORN_PID 2>/dev/null

# 6. 更新 progress.json
cat > .task-context/progress.json <<EOF
{
  "projectName": "example",
  "currentPhase": "acceptance",
  "status": "completed",
  "endTime": "$(date -Iseconds)",
  "acceptanceResults": {
    "syntaxCheck": "passed",
    "testResults": "$(pytest tests/ -v | tail -1)",
    "serviceStartup": "verified"
  }
}
EOF

# 7. 输出标准化信号
if [ $TEST_RESULT -eq 0 ]; then
  echo "ACCEPTANCE_RESULT: PASS"
else
  echo "ACCEPTANCE_RESULT: FAIL"
fi
```

---

## 常见问题

### Q: 测试有 warnings 但全部通过，算 PASS 还是 FAIL？

**A**: 算 **PASS**。Warnings（如 deprecation warnings）不影响功能，但**应该**在后续迭代中修复。

### Q: 服务启动后立即崩溃，算 PASS 还是 FAIL？

**A**:
- 如果崩溃原因是 import 错误 → **FAIL**
- 如果崩溃原因是业务逻辑错误（如数据库连接失败）→ **PASS**（服务本身可运行）

### Q: 多少个测试通过算"足够"？

**A**: 至少 1 个核心功能测试通过。理想情况下，所有单元测试**应该**通过。

### Q: progress.json 必须手动更新吗？

**A**: 是的。Autonomous agent **必须**在每个阶段完成后更新 progress.json，这是主 agent 监控进度的唯一可靠方式。

---

**最后更新**: 2026-03-13
**版本**: v1.0
