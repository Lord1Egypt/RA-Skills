---
name: tdx-ua-patcher
description: 通达信 TcefWnd.dll User-Agent 修改工具。用于查找通达信安装目录、检测版本信息、修改浏览器组件的 UA 标识。当用户需要修改通达信 UA、伪装成移动端浏览器、或绕过某些网站对通达信内置浏览器的限制时使用此 skill。
---

# 通达信 UA 修改工具

## 功能概述

此 skill 用于修改通达信交易软件内置浏览器组件 (TcefWnd.dll) 的 User-Agent 字符串，使其伪装成移动设备浏览器。

## 使用场景

- 通达信内置浏览器被某些网站识别并限制访问
- 需要以移动端 UA 访问网页
- 绕过网站对特定浏览器版本的检测

## 使用方法

### 1. 列出所有通达信安装

```powershell
python scripts/patch_ua.py --list
```

此命令会：
- 扫描常见安装路径 (C:\new_tdx, D:\tdx, E:\tongdaxin 等)
- 显示每个安装的版本信息
- 显示当前的 UA 字符串

### 2. 预览修改（不实际修改）

```powershell
python scripts/patch_ua.py --dry-run
```

### 3. 执行修改

自动查找并修改：
```powershell
python scripts/patch_ua.py
```

指定特定路径修改：
```powershell
python scripts/patch_ua.py --path "E:\tongdaxin\chrome\TcefWnd.dll"
```

使用自定义 UA：
```powershell
python scripts/patch_ua.py --ua "Dalvik/2.1.0 (Linux; U; Android 13; SM-G991B)"
```

## 工作流程

当用户要求修改通达信 UA 时：

1. **查找安装**
   - 运行 `python scripts/patch_ua.py --list`
   - 显示所有找到的通达信安装位置
   - 显示版本信息和当前 UA

2. **确认修改**
   - 询问用户要修改哪个安装（如果有多个）
   - 确认新的 UA 字符串（默认使用 Android UA）

3. **执行修改**
   - 自动创建 `.backup` 备份文件
   - 修改 UA 字符串，保持长度不变（填充空格）
   - 验证修改结果

4. **恢复备份**
   如果需要恢复：
   ```powershell
   Copy-Item "TcefWnd.dll.backup" "TcefWnd.dll" -Force
   ```

## 技术细节

### 修改原理

- UA 字符串存储在 DLL 的只读数据段
- 通过查找 "Mozilla/5.0 (Windows NT" 特征码定位
- 新 UA 必须与原始 UA 长度一致，避免破坏文件偏移
- 不足长度用空格填充

### 支持版本

- 通达信 Chrome 81 版本（较新版本）
- 其他 Chrome 内核版本（自动检测）

### 安全注意事项

1. **自动备份**：修改前自动创建 `.backup` 文件
2. **长度保持**：新 UA 自动填充至原始长度，防止偏移错误
3. **进程检查**：修改前需确保通达信未运行（tdxcef.exe、TdxW.exe）

## 默认 Android UA

```
Dalvik/2.1.0 (Linux; U; Android 11; Redmi 9 Build/RP1A.208720.011)
```

## 脚本位置

- 主脚本：`scripts/patch_ua.py`
