---
name: python-venv-repair
description: 修复损坏的 Python venv 与缺标准库模块（_sqlite3）导致的服务启动失败。
author: peterliu-512
tags: [python, venv, troubleshooting, rhel, standard-library]
category: devops
---

# Python 虚拟环境故障修复

> 适用：systemd 服务反复 failed 但日志无内容、`ModuleNotFoundError: No module named '_xxx'`（标准库 C 扩展）、venv 换过基础解释器后行为异常。典型场景：量化交易/后台服务启动即崩。

## 诊断三件套（先确认根因再动手）

```bash
# 1. venv 的 python 软链指向
ls -la <venv>/bin/python3

# 2. pyvenv.cfg 与软链是否一致（不一致 = venv 被改坏过）
cat <venv>/pyvenv.cfg   # 看 home= 和 version=

# 3. 报错细节
<venv>/bin/python3 -c "import <module>"   # 复现 ModuleNotFoundError
```

**判断规则：**
- `pyvenv.cfg` 的 `home`/`version` 与 `python3` 软链指向**不一致** → venv 被换过基础解释器（实测实例：cfg 是 3.6.8，软链是编译版 3.11）
- 报错路径指向 `/usr/local/lib/python3.x/...` → 用的是**本地编译版 Python**（编译时可能缺模块）
- 同一错误 rpm 版 `/usr/bin/python3.x` 也可能报 → sys.path 被编译版污染（site 配置/PYTHONPATH）

## 缺标准库 C 扩展模块（_sqlite3）快速修复

不重编 Python，从 rpm 版复制 .so（ABI 版本必须一致）：

```bash
# 1. 确认 rpm 版有该模块（路径含 Python 小版本）
ls /usr/lib64/python3.11/lib-dynload/_sqlite3*.so

# 2. 确认编译版 lib-dynload 目录存在 + 系统有动态库依赖
ls /usr/local/lib/python3.11/lib-dynload/
ldconfig -p | grep sqlite    # 本例需要 libsqlite3.so.0

# 3. 复制（cpython-311 后缀必须匹配目标 Python 小版本）
sudo cp /usr/lib64/python3.11/lib-dynload/_sqlite3.cpython-311-x86_64-linux-gnu.so \
        /usr/local/lib/python3.11/lib-dynload/

# 4. 验证 + 重启服务
<venv>/bin/python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
sudo systemctl restart <service>
```

**注意：**
- 修复 `_sqlite3` 只是第一层，继续启动测试可能暴露后续依赖问题（逐层排查）
- 本类修复在 RHEL8 实测有效（复制后 sqlite 3.26.0 正常）；其他 RHEL 版本路径相同但版本号调整

## 备选方案（复制 .so 不可行时）

1. **重建 venv**（依赖要重装，耗时最长）：
   ```bash
   rm -rf <venv>
   /usr/bin/python3.11 -m venv <venv>   # 用 rpm 版，自带全套标准库
   <venv>/bin/pip install -r requirements.txt
   ```
2. **确认哪个 python 有完整标准库**：`/usr/bin/python3.6`（RHEL 8 默认）、`/usr/bin/python3.11`（rpm 包）通常都带 sqlite；本地编译版 `/usr/local/bin/python3.11` 常缺

## Pitfalls

- `pip install` 到默认 Python 不等于 venv 生效——始终用 `venv/bin/pip` 或 `venv/bin/python -m pip`
- systemd 服务 journal 被轮转后可能 "No entries"——先 `systemctl status` 看 Main PID 和退出码，再手动前台运行复现
- 系统同时存在 `/usr/bin/python3.11`（rpm）和 `/usr/local/bin/python3.11`（编译）时，`which python3.11` 可能指向编译版，误导诊断

## 验证命令

```bash
systemctl status <service> | grep -E "Active|Main PID"
<venv>/bin/python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
<venv>/bin/python3 main.py --mode paper   # 前台复现/确认启动
```
