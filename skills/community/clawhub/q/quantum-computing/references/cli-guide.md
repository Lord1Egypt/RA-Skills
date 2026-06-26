# CLI 使用参考

UnifiedQuantum 当前的 CLI 入口是：

```bash
uniqc
```

等价 Python 入口：

```bash
python3 -m uniqc
```

## 命令总览

- `uniqc circuit`
- `uniqc simulate`
- `uniqc submit`
- `uniqc result`
- `uniqc task`
- `uniqc config`

## 一条稳妥的 Shell 工作流

如果输入来自 QASM，推荐先归一化：

```bash
uniqc circuit input.qasm --format originir -o normalized.ir
uniqc simulate normalized.ir
uniqc submit normalized.ir --platform dummy --wait
```

这样比直接把多种格式混进不同命令里更稳。

## `uniqc circuit`

格式转换和统计信息：

```bash
uniqc circuit INPUT_FILE [--format originir|qasm] [--output PATH] [--info]
```

示例：

```bash
uniqc circuit bell.ir --format qasm -o bell.qasm
uniqc circuit bell.qasm --format originir -o bell.ir
uniqc circuit bell.ir --info
```

## `uniqc simulate`

本地模拟：

```bash
uniqc simulate INPUT_FILE [--backend statevector] [--shots 1024] [--format table|json]
```

示例：

```bash
uniqc simulate bell.ir
uniqc simulate bell.ir --shots 4096 --format json
```

注意：

- 当前最安全的输入是 OriginIR
- 本地模拟通常需要安装 `unified-quantum[simulation]`
- 当前 CLI 的 `simulate` 路径最适合 `statevector`
- 密度矩阵工作流更建议走 Python API，并显式使用 `OriginIR_Simulator(backend_type="densitymatrix")`

## `uniqc submit`

提交云任务或 dummy 任务：

```bash
uniqc submit INPUT_FILES... --platform originq|quafu|ibm|dummy
```

当前可见选项：

```bash
--platform / -p
--backend / -b
--shots / -s
--name
--wait / -w
--timeout
--format / -f
```

示例：

```bash
uniqc submit bell.ir --platform originq --shots 1000
uniqc submit bell.ir --platform originq --backend origin:wuyuan:d5
uniqc submit bell.ir --platform dummy --wait
uniqc submit a.ir b.ir --platform quafu --shots 2000
```

关键区别：

- 当前 CLI 用的是 `--backend`，不是一些旧示例里常见的 `--chip-id`
- 对 OriginQ，`--backend` 常用于指定硬件名，例如 `origin:wuyuan:d5`
- 对 Quafu，底层 Python API 仍可传 `chip_id`，但当前 CLI 没有单独的 `--chip-id`

## `uniqc result`

查询任务结果：

```bash
uniqc result TASK_ID [--platform PLATFORM] [--wait] [--timeout 300] [--format table|json]
```

示例：

```bash
uniqc result abc123 --platform originq
uniqc result abc123 --wait --timeout 600
```

如果任务已经在本地 cache 里，通常可以少传一点参数；如果不在 cache 里，再补 `--platform`。

## `uniqc task`

本地任务缓存管理：

```bash
uniqc task list
uniqc task show TASK_ID
uniqc task clear
```

可用选项包括：

- `task list --status ... --platform ... --limit ... --format ...`
- `task clear --status ... --force`

## `uniqc config`

配置 `~/.uniqc/uniqc.yml`：

```bash
uniqc config init
uniqc config set originq.token YOUR_TOKEN
uniqc config get originq
uniqc config list
uniqc config validate
uniqc config profile list
uniqc config profile create dev
uniqc config profile use dev
```

## 配置 profile 与环境变量

- 默认 profile：`default`
- 当前激活 profile 可写进配置文件
- 临时覆盖可用：

```bash
export UNIQC_PROFILE=dev
```

## 常见误区

- 不要再把 CLI 讲成旧版的 `chip-id` 优先接口
- 不要假设裸环境一定能直接 `simulate`
- 不要默认系统里有 `python`；脚本示例优先写 `python3` 或 `uv run`
