# System Info Skill

快速查询系统信息的 OpenClaw Skill。

## 功能

- 查询操作系统信息
- 查询 CPU 信息
- 查询内存使用情况
- 查询磁盘使用情况
- 支持 JSON 和表格输出
- 跨平台支持(Windows/Linux/macOS)

## 安装

```bash
npx clawhub install system-info
```

## 使用

### 查询所有信息

```bash
python scripts/system_info.py
```

### 查询特定信息

```bash
python scripts/system_info.py --cpu
python scripts/system_info.py --memory
python scripts/system_info.py --disk
python scripts/system_info.py --os
```

### JSON 输出

```bash
python scripts/system_info.py --format json
```

## 要求

- Python 3.6+
- 无需额外依赖(仅使用标准库)

## 示例

```
=== 系统信息 ===

操作系统: Windows 10
CPU: Intel Core i7-9700K
CPU 核心数: 8
内存总量: 16.0 GB
内存使用: 8.5 GB (53%)
磁盘总量: 512.0 GB
磁盘使用: 256.0 GB (50%)
```

## 许可

MIT
