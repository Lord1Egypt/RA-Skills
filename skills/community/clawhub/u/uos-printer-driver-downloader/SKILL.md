---
name: printer-downloader
description: 从统信 UOS 驱动中心搜索并下载打印机驱动程序
---

# UOS 打印机驱动下载

从统信 UOS 官方驱动中心搜索打印机驱动并下载 `.deb` 安装包。提供两种使用方式：分离式（先搜索后下载）和一体化（搜索下载一步完成）。

## 触发条件

用户请求包含以下意图时调用此技能：
- 搜索或下载 UOS/统信系统的打印机驱动
- 查找特定型号的打印机驱动
- 离线预下载打印机驱动

## 脚本说明

| 脚本 | 用途 | 交互 |
|------|------|------|
| `list_printers.py` | 搜索驱动并保存到 `driver_list.json` | 搜索关键词可交互输入 |
| `download_driver.py` | 从 `driver_list.json` 选择并下载 | 完全非交互 |
| `download_printer.py` | 搜索并下载一步完成 | 完全非交互 |

共享模块 `driver_utils.py` 提供公共搜索、下载、显示函数。

## 调用方式

### 分离式（适合对比选择）

```bash
# 步骤一：搜索驱动
cd scripts && python3 list_printers.py "LJ2405"

# 步骤二：下载驱动
python3 download_driver.py                                    # 自动选第一个 amd64
python3 download_driver.py --arch arm64                       # 自动选 arm64
python3 download_driver.py --index 2 --output ~/Desktop       # 手动指定序号和目录
```

| 参数 | 说明 |
|------|------|
| `--index N` | 指定下载序号（1-based），不传则按架构自动选择 |
| `--arch <架构>` | 优先匹配架构（默认 `amd64`），如 `arm64`、`all` |
| `--output <目录>` | 下载目录（默认 `~/Desktop`） |

### 一体化（适合快速下载）

```bash
cd scripts && python3 download_printer.py "<打印机型号>" [下载目录] [--arch <架构>]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| 打印机型号 | 是 | 搜索关键词，如 `"联想 LJ2405"` |
| 下载目录 | 否 | 下载目录（默认当前目录） |
| `--arch <架构>` | 否 | 优先匹配架构（默认 `amd64`） |

### 选择逻辑

一体化脚本和分离式下载脚本（未指定 `--index` 时）采用相同的多选策略：

1. **all 架构**：始终全部下载（通用驱动包）
2. **指定架构**：下载所有匹配 `--arch` 的驱动
3. 不够 3 个则有多少下多少

指定 `--index` 时仅下载所选序号的单个驱动。

## 输出

- **控制台**：表格显示搜索结果（序号、架构、型号、版本、包名）
- **下载文件**：保存到 `<输出目录>/printer_driver_YYYYMMDD/<型号>/` 下，文件名 `{包名}_{版本}_{架构}.deb`
  ```
  ~/Desktop/printer_driver_20260605/
  ├── HP_LaserJet_Pro_MFP_M125nw/
  │   └── hplip_1.0.5_amd64.deb
  └── Canon_LBP2900/
      └── cndrvcups_2.0.0_amd64.deb
  ```
- **搜索缓存**（分离式）：`driver_list.json` 保存在当前目录

## 错误处理

| 错误 | 处理 |
|------|------|
| 参数不足 | 提示正确用法 |
| 搜索无结果 | 提示未找到，建议更换关键词 |
| `driver_list.json` 不存在 | 提示先运行 `list_printers.py` |
| 网络请求失败 | 提示检查网络连接 |
| 序号超出范围 | 提示可选范围 |

## 依赖

```bash
pip install requests
```
