---
name: server-test-converter
description: 将服务器测试命令 txt 文件转换为 pytest 测试用例。每个 txt 文件对应生成一个独立的 pytest 文件，命令合并到一个函数中执行。包含通用框架 test_framework.py，适配各种测试环境。
trigger: 用户发送 txt 文件并要求转换为 pytest 测试用例，或提到服务器测试、网卡测试、命令转换
---

# 服务器测试用例转换器

将服务器/网卡测试命令文件转换为 pytest 测试用例。**每个 txt 文件生成一个对应的 pytest 文件**。

## 功能概述

- **输入**: 包含测试命令的 txt 文件（支持批量处理）
- **输出**: 每个 txt 文件对应一个 pytest 测试文件
- **执行方式**: 支持 send_r5 (R5卡) 和 send_host (主机Shell) 两种方式
- **通用框架**: 提供 test_framework.py，可适配各种测试环境

## 使用方法

### 1. 准备输入文件

将待转换的 txt 命令文件放到目录：
```
/home/admin/.openclaw/tytest/txt_contents/txt/*.txt
```

### 2. 运行转换脚本

```bash
python3 /home/admin/.openclaw/workspace/skills/server-test-converter/convert_commands.py
```

### 3. 获取输出

转换后的文件：
```
/home/admin/.openclaw/tytest/
├── test_framework.py    # 通用框架（需要配置）
├── test_xxx.py         # 生成的测试用例
└── txt_contents/       # 原始命令文件
```

## 通用框架说明

### test_framework.py

生成的测试代码依赖 `test_framework.py`，使用方式：

```python
from test_framework import send_r5, send_host, send_r5_wait, send_host_wait, tl_log, TARGET, TARGET_R5
```

### 配置步骤

1. **复制到测试服务器**: 将 `test_framework.py` 和 `test_xxx.py` 复制到测试服务器

2. **实现 send_a_cmd()**: 根据你的测试环境实现命令执行逻辑

```python
# 方式一: SSH
import paramiko
def send_a_cmd(cmd, target):
    ssh = paramiko.SSHClient()
    ssh.connect(hostname='192.168.1.100', username='admin', password='xxx')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read()

# 方式二: 调用已有框架
from your_framework import execute_cmd
def send_a_cmd(cmd, target):
    return execute_cmd(cmd, target)

# 方式三: 本地执行
import subprocess
def send_a_cmd(cmd, target):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout
```

3. **配置目标设备**: 修改 `TARGET` 和 `TARGET_R5` 的值

4. **运行测试**:
```bash
pip install pytest
pytest test_xxx.py -v
```

## 命令执行方式判断

| 命令类型 | 示例 | 执行方式 |
|---------|-----|---------|
| 内存操作 | `md`, `mw` | send_r5_wait |
| 调度器 | `txsch_test_*`, `dmif_txsch_*` | send_r5_wait |
| DFX诊断 | `dmif_eoc_*`, `*_show_dfx` | send_r5_wait |
| 网卡命令 | `ice_*`, `test_*`, `nicif_*` | send_r5_wait |
| 其他 | Shell 命令等 | send_host_wait |

## 输出格式

```python
#!/usr/bin/env python3
"""
自动生成的测试用例: xxx.txt
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_framework import send_r5, send_host, send_r5_wait, send_host_wait, tl_log, TARGET, TARGET_R5

class TestXxx:
    def test_all_commands(self, env):
        """执行所有命令"""
        commands = ['命令1', '命令2']
        for cmd in commands:
            send_r5_wait(TARGET_R5, cmd)
```

## 注意事项

1. **通用框架**: 不依赖特定测试框架，适配各种环境
2. **需要实现**: 用户需要实现 `send_a_cmd()` 函数
3. **配置目标**: 根据实际修改 `TARGET` 和 `TARGET_R5`
4. **自动去重**: 相同的命令只保留一条
