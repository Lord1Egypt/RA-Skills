# 星火软件商店 Skill

## 概述

星火软件商店 Skill 支持在 Linux 系统上搜索、安装和卸载应用程序。支持两个应用商店：

- **星火应用商店 (Spark Store)** - 适用于 Debian 系发行版 (deepin, Ubuntu, Debian, UOS 等)
- **星火 APM (AmberPM)** - 适用于所有 Linux 发行版 (Arch, Fedora, 银河麒麟等)

## 触发条件

当用户提出以下请求时触发：

- 搜索应用 / 查找软件
- 安装应用 / 安装软件
- 卸载应用 / 卸载软件
- 更新应用 / 更新软件
- 提到 "星火应用商店" 或 "APM"
- 提到 "aptss" 或 "apm" 命令

## 系统检测

首先检测当前系统是否为 Debian 系：

```python
from scripts.detect_os import is_debian_based, get_system_name

is_debian = is_debian_based()
system_name = get_system_name()
```

Debian 系包括：debian, ubuntu, deepin, linuxmint, pop, elementary, kali, UOS, 统信等。

## 搜索流程

### Debian 系系统

同时搜索两个商店，合并结果：

1. 调用 `spark_store_api.search(keyword)` - 搜索 Spark Store
2. 调用 `spark_apm_api.search(keyword)` - 搜索 APM
3. 合并结果，按相关性排序
4. 展示搜索结果

### 非 Debian 系系统

仅搜索 APM：

1. 调用 `apm_api.search(keyword)` - 搜索 APM
2. 展示搜索结果

## 搜索 API

### Spark Store API

- 分类列表：`https://d.spark-app.store/store/categories.json`
- 应用列表：`https://d.spark-app.store/store/{category}/applist.json`

### APM API

- 分类列表：`https://d.spark-app.store/amd64-apm/categories.json`
- 应用列表：`https://d.spark-app.store/amd64-apm/{category}/applist.json`

## 安装/卸载流程

### Debian 系系统

使用 aptss 命令：

```bash
# 安装
sudo aptss install <package_name>

# 卸载
sudo aptss remove <package_name>

# 更新
sudo aptss upgrade
```

### 非 Debian 系系统

使用 apm 命令：

```bash
# 安装
sudo apm install <package_name>

# 卸载
sudo apm remove <package_name>

# 更新
sudo apm update
```

## 命令检查

在执行安装/卸载操作前，检查命令是否可用：

```python
# 检查 aptss
from scripts.spark_store_api import check_command_available as spark_check
spark_check()  # 返回 True/False

# 检查 apm
from scripts.spark_apm_api import check_command_available as apm_check
apm_check()  # 返回 True/False
```

## 错误处理

- **网络错误**：提示用户检查网络连接
- **命令不存在**：提示用户安装对应的工具
- **安装/卸载失败**：展示错误信息和建议

## 使用示例

### 搜索应用

用户输入："搜索微信"

```
系统检测：Debian 系
搜索 Spark Store...
搜索 APM...
合并结果：
1. 微信（wine）- com.qq.weixin.spark - 版本 3.9.10deepin1.1
2. 企业微信（wine）- com.qq.weixin.work.deepin - 版本 5.0.0.6008~spark2
...
```

### 安装应用

用户输入："安装微信"

```
检测到 Debian 系系统
请选择安装源：
1. 星火应用商店 (aptss)
2. APM (apm)
```

用户选择后执行安装命令。

### 卸载应用

用户输入："卸载微信"

```
包名：com.qq.weixin.spark
确认卸载？ [Y/n]
执行卸载...
```

## 文件结构

```
spark-store-skill/
├── SKILL.md                    # 本文件
├── README.md                    # 使用说明
└── scripts/
    ├── __init__.py
    ├── detect_os.py             # 系统检测
    ├── spark_store_api.py       # Spark Store API
    └── spark_apm_api.py         # APM API
```

## 依赖

- Python 3
- curl
- aptss (Debian 系)
- apm (所有系统)

## 注意事项

1. 搜索结果可能较多，建议分页展示
2. 安装/卸载需要 root 权限
3. 部分应用可能需要重启才能生效
