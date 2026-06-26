# 云平台参考

当前 UnifiedQuantum 的云执行路径分两层：

1. CLI：`uniqc submit` / `uniqc result` / `uniqc task`
2. Python API：`submit_task` / `submit_batch` / `query_task` / `wait_for_result`

## 配置文件

默认配置路径：

```text
~/.uniqc/uniqc.yml
```

典型结构：

```yaml
default:
  originq:
    token: ""
    available_qubits: []
    available_topology: []
    task_group_size: 200
  quafu:
    token: ""
  ibm:
    token: ""
    proxy:
      http: ""
      https: ""
```

初始化：

```bash
uniqc config init
```

设置 token：

```bash
uniqc config set originq.token YOUR_ORIGINQ_TOKEN
uniqc config set quafu.token YOUR_QUAFU_TOKEN
uniqc config set ibm.token YOUR_IBM_TOKEN
```

## 配置 profile

可通过多 profile 管理不同环境：

```bash
uniqc config profile create dev
uniqc config profile use dev
uniqc config profile list
```

也可以临时覆盖：

```bash
export UNIQC_PROFILE=dev
```

## Python 任务 API

最常用的公共入口：

```python
from uniqc import (
    submit_task,
    submit_batch,
    query_task,
    wait_for_result,
    list_tasks,
    clear_completed_tasks,
)
```

### `submit_task`

```python
task_id = submit_task(
    circuit,
    backend="originq",
    shots=1000,
    metadata={"name": "demo"},
)
```

后端相关的常见 kwargs：

- OriginQ:
  - `backend_name="origin:wuyuan:d5"`
  - `circuit_optimize=...`
  - `measurement_amend=...`
- Quafu:
  - `chip_id="ScQ-P10"`
  - `auto_mapping=True`
- 通用 dummy 覆盖：
  - `dummy=True`

### `submit_batch`

```python
task_ids = submit_batch(
    [circuit_a, circuit_b],
    backend="quafu",
    shots=2000,
)
```

### `query_task`

```python
task_info = query_task(task_id)
print(task_info.status)
```

如果任务不在本地 cache 中，通常需要补 `backend=...`。

### `wait_for_result`

```python
result = wait_for_result(task_id, backend="originq", timeout=300)
```

返回值通常是一个归一化后的结果字典；dummy 路径下最常见的结构类似：

```python
{
    "counts": {"00": 500, "11": 500},
    "probabilities": {"00": 0.5, "11": 0.5},
    "shots": 1000,
    "platform": "dummy",
    "task_id": "...",
}
```

不同平台的原始数据会被归一化，但如果用户只关心最稳妥的兼容字段，优先读：

- `counts`
- `probabilities`

## dummy 模式

dummy 模式用于本地模拟，不消耗真实云平台额度。

启用方式有两类：

### 1. 单次任务

```python
task_id = submit_task(circuit, backend="originq", dummy=True)
```

### 2. 全局环境变量

```bash
export UNIQC_DUMMY=true
```

然后：

```python
task_id = submit_task(circuit, backend="originq")
```

注意：

- dummy 模式通常仍需要本地模拟依赖
- 它更适合开发 / 测试 / 文档示例，不等于“完全无依赖”

## 本地任务缓存

当前任务缓存使用 SQLite：

```text
~/.uniqc/cache/tasks.sqlite
```

相关接口：

```python
from uniqc import list_tasks, clear_completed_tasks, clear_cache
```

CLI 里对应：

```bash
uniqc task list
uniqc task show TASK_ID
uniqc task clear
```

## `TaskInfo`

缓存和查询结果常见字段：

- `task_id`
- `backend`
- `status`
- `result`
- `shots`
- `submit_time`
- `update_time`
- `metadata`

## 平台建议

### OriginQ

- 先确认 token 已配置
- Python API 更适合传 `backend_name`
- CLI 用 `--backend`

### Quafu

- 先确认 token 已配置
- Python API 可传 `chip_id`
- 当前 CLI 对 Quafu 的专有参数表达较少，必要时优先 Python

### IBM

- 先确认 token 已配置
- 代理设置写在 `ibm.proxy.http` / `ibm.proxy.https`

## 使用这些接口时不要默认

- 不要默认 dummy 模式“无条件可用”
- 不要默认 CLI 已经完整暴露了所有平台专有参数
- 不要默认任务结果永远只有一种字段布局；更稳妥的是优先读取常用字段
