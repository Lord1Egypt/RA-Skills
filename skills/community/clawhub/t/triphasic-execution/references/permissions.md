# 权限权重说明（R-16）

> 由 `permission_checker.py` 扫描生成（2026-05-24），扫描 8 个文件、3219 行。

## 扫描结果摘要

| 项目 | 值 |
|------|-----|
| 风险等级 | **MEDIUM** |
| 权限权重 | **50.00%** |
| 扫描文件数 | 8 |
| 扫描行数 | 3219 |
| 问题总数 | 28 |

## 权限统计

| 权限类型 | 次数 | 权重 |
|---------|------|------|
| `sensitive_access` | 0 | 40% |
| `critical_write` | 0 | 30% |
| `network_access` | 1 | 20% |
| `file_delete` | 6 | 10% |
| `subprocess_call` | 21 | — |

## 高权限操作清单

### subprocess_call（21 处，HIGH）

| 文件 | 行号 | 匹配模式 | 授权方式 |
|------|-------|----------|----------|
| `scripts/cron_helper.py` | 17, 43 | `subprocess` | `immediate` |
| `scripts/exec_wrapper.py` | 32, 167, 180, 187, 195 | `subprocess` | `immediate` |
| `scripts/install.py` | 85, 88, 126, 214 | `subprocess` / `exec(` | `immediate` |
| `scripts/lessons_register.py` | 18, 60, 83 | `subprocess` | `immediate` |
| `scripts/problem_daemon.py` | 27, 160, 413, 416, 417, 439 | `subprocess` / `Popen` | `immediate` |

### file_delete（6 处，HIGH）

| 文件 | 行号 | 匹配模式 | 授权方式 |
|------|-------|----------|----------|
| `scripts/install.py` | 76, 189 | `shutil.rmtree` | `immediate` |
| `scripts/task_progress.py` | 439, 443, 496, 501 | `os.remove` | `immediate` |

### network_access（1 处，MEDIUM）

| 文件 | 行号 | 匹配模式 | 授权方式 |
|------|-------|----------|----------|
| `scripts/settings.py` | 25 | `urllib` | `unified` |

## 授权方式说明

| 方式 | 适用场景 | 说明 |
|------|----------|------|
| `unified` | 中风险操作（network_access） | 批量统一授权，首次确认后可复用 |
| `immediate` | 高风险操作（subprocess_call、file_delete） | 每次执行前需用户确认 |
| `silent` | 低风险操作 | 无需授权，静默执行 |

## 风险结论

- **风险等级：MEDIUM**（权重 50%）
- **建议**：高权限操作（subprocess、文件删除）已标注 `immediate` 授权方式，符合规范；网络访问（`settings.py`）使用 `unified` 授权，符合规范。
- **R-15 检查**：所有高权限操作前均应有授权检查逻辑。
