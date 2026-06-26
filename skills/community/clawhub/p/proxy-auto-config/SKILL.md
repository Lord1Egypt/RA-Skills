---
name: proxy-auto-config
description: 自动检测和配置系统代理设置，特别为 OpenClaw Gateway 优化。使用场景包括：1) Gateway 启动时自动检测代理，2) 自动配置环境变量，3) 创建代理启动脚本，4) 定时检查代理状态，5) 支持 v2ray、Clash、SS/SSR 等常见代理工具。当系统使用代理网络环境时自动触发。
---

# 代理自动配置技能

## 概述

本技能自动检测系统中的代理配置，并为 OpenClaw Gateway 提供无缝的代理集成。支持自动检测 v2ray、Clash、SS/SSR 等常见代理工具，自动配置环境变量和 Gateway 设置，确保在网络受限环境下 OpenClaw 能正常工作。

## 核心功能

### 1. 代理自动检测
- **环境变量检测**: 自动读取 HTTP_PROXY、HTTPS_PROXY 等环境变量
- **进程检测**: 检测正在运行的 v2ray、Clash、SS/SSR 等代理进程
- **端口检测**: 扫描常见代理端口（1080-1090, 7890, 10808 等）
- **配置检测**: 读取代理工具的配置文件

### 2. Gateway 集成
- **自动配置**: Gateway 启动时自动应用代理设置
- **环境变量**: 设置 HTTP_PROXY、HTTPS_PROXY 等环境变量
- **插件配置**: 自动更新 Gateway 的 http-proxy 插件配置
- **启动脚本**: 创建带代理的 Gateway 启动脚本

### 3. 自动化管理
- **定时检查**: 每小时自动检查代理状态
- **启动钩子**: Gateway 启动前自动运行代理配置
- **故障恢复**: 代理失效时自动尝试其他配置
- **日志记录**: 详细的代理配置和运行日志

### 4. 多代理支持
- **v2ray/v2rayN**: 支持本地 SOCKS5 代理（端口 10808）
- **Clash**: 支持 HTTP/SOCKS 代理（端口 7890）
- **SS/SSR**: 支持 Shadowsocks 代理
- **系统代理**: 支持系统级别的代理设置

## 快速开始

### 1. 安装技能
```bash
cd ~/.openclaw/workspace/skills/proxy-auto-config
python3 scripts/install_proxy_skill.py
```

### 2. 检测代理
```bash
python3 scripts/proxy_detector.py --configure
```

### 3. 配置 Gateway
```bash
python3 scripts/gateway_proxy_setup.py
```

### 4. 使用代理启动 Gateway
```bash
# 使用包装脚本
openclaw-proxy start

# 或直接设置环境变量
HTTP_PROXY=socks5://127.0.0.1:10808 openclaw gateway start
```

## 工作流程

### 步骤 1: 代理检测
1. 扫描环境变量中的代理设置
2. 检测正在运行的代理进程
3. 检查监听端口的代理服务
4. 读取代理配置文件
5. 选择最佳的代理配置

### 步骤 2: 环境配置
1. 设置 HTTP_PROXY、HTTPS_PROXY 环境变量
2. 配置 Python requests 库的代理设置
3. 设置 Node.js/npm 的代理配置
4. 更新系统代理设置（如果支持）

### 步骤 3: Gateway 配置
1. 更新 Gateway 配置文件（gateway.json）
2. 配置 http-proxy 插件
3. 创建启动脚本
4. 设置 systemd 服务（如果可用）

### 步骤 4: 自动化部署
1. 创建定时检查任务
2. 设置 Gateway 启动钩子
3. 配置日志轮转
4. 启用故障监控

## 使用示例
### ⚠️ 注意：
- 代理端口 `10808` 是示例，请根据你的实际配置修改
- 使用 `~` 代替硬编码的家目录路径
- 所有路径都应该是相对路径或使用环境变量


### 示例 1: 手动检测和配置
```bash
# 检测当前代理
cd ~/.openclaw/workspace/skills/proxy-auto-config
python3 scripts/proxy_detector.py --verbose

# 配置环境
python3 scripts/proxy_detector.py --configure --output ~/.openclaw/proxy_config

# 应用配置
source ~/.openclaw/proxy_config/configure_proxy.sh
```

### 示例 2: Gateway 集成
```bash
# 配置 Gateway 代理
python3 scripts/gateway_proxy_setup.py --config-dir ~/.openclaw

# 查看 Gateway 配置
cat ~/.openclaw/gateway.json | jq '.plugins["http-proxy"]'

# 使用代理启动 Gateway
openclaw-proxy start
```

### 示例 3: 定时检查
```bash
# 查看定时任务
crontab -l | grep openclaw

# 查看检查日志
tail -f ~/.openclaw/logs/proxy_check.log

# 手动运行检查
python3 scripts/proxy_detector.py --configure
```

### 示例 4: 故障排除
```bash
# 测试代理连接
python3 scripts/proxy_detector.py --test --configure

# 查看详细日志
tail -f ~/.openclaw/logs/proxy_setup.log

# 重置配置
rm -rf ~/.openclaw/proxy_config/
python3 scripts/install_proxy_skill.py
```

## 脚本文件

### scripts/ 目录
包含所有可执行的 Python 脚本：

1. **proxy_detector.py** - 核心代理检测脚本
   - 自动检测系统代理配置
   - 支持多种代理工具（v2ray、Clash、SS/SSR）
   - 环境变量和配置文件管理
   - 代理连接测试和验证

2. **gateway_proxy_setup.py** - Gateway 代理设置脚本
   - 集成 OpenClaw Gateway 代理配置
   - 自动更新 gateway.json 配置文件
   - 创建启动脚本和 systemd 服务
   - 环境变量自动设置

3. **install_proxy_skill.py** - 安装和配置脚本
   - 检查系统依赖
   - 创建定时任务和启动钩子
   - 配置 systemd 集成
   - 生成使用指南

### 依赖要求
```bash
# 必需依赖
pip install psutil requests

# 可选依赖（用于高级功能）
pip install jq  # JSON 处理
```

## 配置文件结构

### 生成的配置文件
```
~/.openclaw/
├── gateway.json                    # Gateway 配置文件（自动更新）
├── proxy_config/                   # 代理配置目录
│   ├── proxy_config.json          # 代理检测结果
│   ├── configure_proxy.sh         # 代理配置脚本
│   └── gateway_proxy.json         # Gateway 代理配置
├── logs/                          # 日志目录
│   ├── proxy_setup.log           # 代理设置日志
│   ├── proxy_check.log           # 定时检查日志
│   └── gateway_proxy_setup.log   # Gateway 设置日志
└── gateway_proxy_hook.sh         # Gateway 启动钩子
```

### 系统集成文件
```
~/.local/bin/openclaw-proxy        # Gateway 代理包装脚本
~/.config/systemd/user/           # systemd 用户服务
   ├── openclaw-proxy-check.service
   └── openclaw-proxy-check.timer
```

## 在 OpenClaw 中使用

### 自动触发条件
当以下情况发生时自动触发代理配置：
1. **Gateway 启动时** - 自动检测和配置代理
2. **网络环境变化时** - 定时检查代理状态
3. **代理工具启动/停止时** - 自动更新配置
4. **用户手动请求时** - 通过命令触发重新配置

### 响应示例
```markdown
## 代理自动配置完成

✅ 检测到 v2rayN 代理
   - 类型: SOCKS5
   - 地址: socks5://127.0.0.1:10808
   - 进程: xray (PID: 3595)

⚙️ 配置已更新:
   - 环境变量: HTTP_PROXY, HTTPS_PROXY
   - Gateway 配置: http-proxy 插件
   - 启动脚本: ~/.local/bin/openclaw-proxy

🚀 使用代理启动 Gateway:
   ```bash
   openclaw-proxy start
   ```

📊 状态监控:
   - 下次检查: 1小时后
   - 日志文件: ~/.openclaw/logs/proxy_check.log
```

### 故障处理
当代理配置失败时：
1. **尝试备用代理** - 自动尝试其他检测到的代理
2. **回退直连模式** - 如果所有代理都不可用
3. **记录错误信息** - 详细的错误日志
4. **通知用户** - 提供修复建议

## 最佳实践

### 1. 代理工具配置
- 保持代理工具稳定运行
- 使用固定端口（如 10808）
- 启用代理工具的自启动
- 定期更新代理订阅

### 2. 技能维护
- 定期运行代理检测
- 监控代理连接状态
- 更新技能到最新版本
- 备份重要配置文件

### 3. 故障排除
- 检查代理工具是否正常运行
- 验证代理端口是否可访问
- 查看技能日志获取详细信息
- 手动测试代理连接

### 4. 性能优化
- 减少不必要的代理检测
- 缓存有效的代理配置
- 优化定时检查频率
- 使用轻量级检测方法

## 扩展和定制

### 添加新的代理支持
1. 在 `proxy_detector.py` 中添加新的检测逻辑
2. 更新代理端口和进程关键词
3. 添加对应的配置文件解析
4. 测试新的代理类型

### 自定义配置
1. 修改默认的代理端口列表
2. 调整检测优先级
3. 自定义日志格式和位置
4. 修改定时检查频率

### 集成其他工具
1. 添加对其他网络工具的支持
2. 集成到系统网络管理器
3. 添加 GUI 配置界面
4. 支持云代理服务

---

**技能状态**: ✅ 已完成并测试
**最后更新**: 2026-03-29
**适用环境**: Linux 系统，支持 systemd，使用 v2ray/Clash 等代理工具
