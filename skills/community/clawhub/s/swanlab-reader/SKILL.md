---
name: swanlab-reader
description: 读取 SwanLab 实验数据。当用户发来 SwanLab run URL 时使用。
credentials:
  - id: swanlab-key
    type: api-key
    description: SwanLab API Key（查询私有项目需要）
    env: SWANLAB_KEY | SWANLAB_API_KEY
    file: ~/.config/swanlab/key
    optional: true
env:
  - SWANLAB_KEY
  - SWANLAB_API_KEY
dependencies:
  - swanlab
  - numpy
---

# SwanLab Reader

## 安装

```bash
# 依赖：swanlab、numpy（uv run 自动处理）
uv run python skills/swanlab-reader/swanlab_reader.py set-key <your-key>
```

首次设置 API Key（只需一次）。key 保存在 `~/.config/swanlab/key`，或通过环境变量 `SWANLAB_KEY` / `SWANLAB_API_KEY` 传入。

## 命令

### `runs` — 项目概览
```bash
uv run python skills/swanlab-reader/swanlab_reader.py runs <username/project>
```

### `info` — 指标 + 配置
```bash
uv run python skills/swanlab-reader/swanlab_reader.py info <url>
```
末尾输出可直接复制粘贴的 `history` 命令。

### `history` — 历史序列
```bash
uv run python skills/swanlab-reader/swanlab_reader.py history <url> <key1> [key2] ...
uv run python skills/swanlab-reader/swanlab_reader.py history <url> <key> --plot   # 带 ASCII 图
```

### `plot` — 单独画图
```bash
uv run python skills/swanlab-reader/swanlab_reader.py plot <url> <key>
```

### `compare` — 多 run 对比
```bash
uv run python skills/swanlab-reader/swanlab_reader.py compare <url1> <url2> [url3 ...]
```
自动获取所有 run 的所有指标并列对比。

## 工作流

1. `runs <project>` 看项目下有哪些 run
2. `info <url>` 看指标列表 + 配置，复制末尾的 history 命令
3. `history <url> <keys>` 查具体指标历史
4. `compare <url1> <url2> ...` 多 run 并排对比
