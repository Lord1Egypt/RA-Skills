# 太极架构 v2.1

多 Agent 协作框架，支持集中式、分布式、元混合三种运行模式。

## 核心特性

- 🔹 **三种模式**：集中式（4个永久Agent）、分布式（对等Worker并行）、元混合（每阶段一组Worker）
- 🔹 **基于 Redis 的消息总线**：支持权限检查和独立订阅
- 🔹 **可插拔 Skill 系统**：通过 YAML 注册，支持子进程调用，白名单隔离
- 🔹 **状态持久化**：SQLite 存储任务和 Worker 状态
- 🔹 **完全可移植**：无硬编码路径，环境变量驱动

## 环境要求

- Python 3.9+
- Redis（消息总线）
- Linux / macOS（Windows 建议用 WSL）

## 快速开始

```bash
# 1. 安装
./install.sh

# 2. 启动 Redis（新终端）
redis-server

# 3. 运行测试
./start.sh --mode centralized --request "分析日志文件 app.log"
```

## 运行模式

| 模式 | 命令 | 适用场景 |
|------|------|---------|
| 集中式 | `--mode centralized` | 线性依赖任务（默认） |
| 分布式 | `--mode distributed --workers 5` | 数据并行任务 |
| 元混合 | `--mode hybrid`（开发中） | 多阶段复杂任务 |

## 配置文件

| 文件 | 作用 |
|------|------|
| `config.yaml` | 主配置（Redis地址、Worker池大小等） |
| `configs/communication.yaml` | 消息权限矩阵 |
| `configs/modes/*.yaml` | 各模式详细参数 |
| `configs/skills/manifest.yaml` | 可用 Skill 列表 |

## 项目结构

```
taichi-framework/
├── orchestrator.py          # 主入口
├── config.yaml               # 主配置
├── core/
│   ├── agents/              # 4个永久Agent（集中式）
│   ├── worker/
│   │   ├── worker.py        # Worker（集中式）
│   │   └── distributed/     # 分布式Worker
│   ├── communication/       # Redis总线 + 权限
│   ├── skills/              # Skill注册与执行
│   └── utils/               # 日志、状态、特征提取
├── configs/
│   ├── modes/               # 模式配置
│   └── skills/              # Skill清单
├── workspace/                # 运行时（日志、数据库）
└── tests/                   # 测试脚本
```

## 三种模式详解

### 集中式（Centralized）
```
用户 → Planner → Drafter → Validator → Dispatcher → Worker池 → 结果
```
- 4个永久 Agent，决策集中
- 适合任务步骤线性、依赖明确

### 分布式（Distributed）
```
用户 → [Worker-1, Worker-2, ..., Worker-N] → 合并结果
```
- 无中心协调，Worker 对等协作
- 通过一致性哈希分片并行处理
- 适合数据并行（如批量计算、分片扫描）

### 元混合（Meta-Hybrid）（开发中）
```
用户 → Planner组 → Drafter组 → Validator组 → Dispatcher组 → 执行Worker
```
- 每阶段由一组 Worker 以分布式方式完成
- 兼具集中式的流程控制和分布式的并行能力

## 测试

```bash
# 集中式
python tests/test_basic.py

# 分布式
python tests/test_distributed.py
```

## 调试

```bash
# 详细日志
TAICHI_DEBUG=1 ./start.sh --mode centralized --request "test"

# 查看日志
tail -f workspace/logs/taichi.log
```

## 添加新 Skill

编辑 `configs/skills/manifest.yaml`：

```yaml
skills:
  - name: "my_skill"
    description: "自定义Skill"
    executor:
      type: "subprocess"
      command: "python3 /path/to/script.py {{arg1}}"
      allowed_commands: ["python3"]
```

## 卸载

```bash
./uninstall.sh
```

## 许可证

MIT
