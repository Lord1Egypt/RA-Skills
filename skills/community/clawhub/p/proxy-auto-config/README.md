# 🔧 OpenClaw Proxy Auto-Config Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-green)](https://github.com/MaiiNor/openclaw-skill-proxy-auto-config)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**自动检测和配置系统代理设置，特别为 OpenClaw Gateway 优化**

## 📋 功能特性

### 🎯 核心功能
- **自动代理检测** - 智能检测系统代理配置
- **多协议支持** - SOCKS5、HTTP、HTTPS 代理
- **环境变量配置** - 自动设置系统环境变量
- **Gateway 集成** - 为 OpenClaw Gateway 优化配置
- **零依赖** - 纯 Python 实现，无需额外安装

### 🔍 检测能力
- ✅ 环境变量代理检测
- ✅ 本地端口扫描（常见代理端口）
- ✅ 进程检测（v2ray、Clash、SS/SSR 等）
- ✅ 网络配置检查
- ✅ 自动配置生成

## 🚀 快速开始

### 安装方法

#### 方法1：从 GitHub 安装（推荐）
```bash
openclaw skills install https://github.com/MaiiNor/openclaw-skill-proxy-auto-config
```

#### 方法2：从本地目录安装
```bash
# 克隆仓库
git clone https://github.com/MaiiNor/openclaw-skill-proxy-auto-config.git

# 安装技能
openclaw skills install ./openclaw-skill-proxy-auto-config
```

#### 方法3：手动安装
```bash
# 复制技能到 OpenClaw 技能目录
cp -r openclaw-skill-proxy-auto-config ~/.openclaw/workspace/skills/
```

### 基本使用

#### 1. 检测当前代理配置
```bash
# 运行代理检测
cd ~/.openclaw/workspace/skills/proxy-auto-config
python3 scripts/simple_proxy_check.py
```

#### 2. 自动配置代理
```bash
# 运行自动配置
python3 scripts/proxy_detector.py --configure

# 应用配置
source ~/.openclaw/proxy_config/configure_proxy.sh
```

#### 3. 配置 OpenClaw Gateway
```bash
# 设置 Gateway 代理
python3 scripts/gateway_proxy_setup.py
```

## 📁 文件结构

```
proxy-auto-config/
├── README.md                 # 本文档
├── SKILL.md                  # 技能定义文件
├── _meta.json               # 技能元数据
├── scripts/                 # 脚本目录
│   ├── simple_proxy_check.py    # 简化代理检测（零依赖）
│   ├── proxy_detector.py        # 完整代理检测器
│   ├── gateway_proxy_setup.py   # Gateway 代理设置
│   └── install_proxy_skill.py   # 安装脚本
└── venv/                    # Python 虚拟环境
```

## 🔧 详细使用指南

### 代理检测脚本

#### `simple_proxy_check.py` - 简化版本（推荐）
```bash
# 基本检测
python3 scripts/simple_proxy_check.py

# 详细输出
python3 scripts/simple_proxy_check.py --verbose

# 生成配置
python3 scripts/simple_proxy_check.py --configure
```

#### `proxy_detector.py` - 完整版本
```bash
# 完整检测
python3 scripts/proxy_detector.py

# 指定输出目录
python3 scripts/proxy_detector.py --output ~/.openclaw/proxy_config

# 自动配置
python3 scripts/proxy_detector.py --configure --auto
```

### 支持的代理类型

| 代理类型 | 默认端口 | 检测方法 |
|---------|---------|---------|
| **SOCKS5** | 10808, 1080 | 端口扫描 + 环境变量 |
| **HTTP/HTTPS** | 8080, 8888 | 环境变量检测 |
| **v2ray** | 10808 | 进程检测 |
| **Clash** | 7890, 7891 | 进程检测 |
| **SS/SSR** | 1080, 1081 | 进程检测 |

### 环境变量配置

技能会自动设置以下环境变量：

```bash
# HTTP 代理
export HTTP_PROXY="socks5://127.0.0.1:10808"
export http_proxy="socks5://127.0.0.1:10808"

# HTTPS 代理
export HTTPS_PROXY="socks5://127.0.0.1:10808"
export https_proxy="socks5://127.0.0.1:10808"

# 全局代理
export ALL_PROXY="socks5://127.0.0.1:10808"
export all_proxy="socks5://127.0.0.1:10808"
```

## ⚙️ 配置 OpenClaw Gateway

### 自动配置
```bash
# 运行 Gateway 代理设置
python3 scripts/gateway_proxy_setup.py

# 检查配置
cat ~/.openclaw/proxy_config/gateway_proxy.json
```

### 手动配置
1. 编辑 Gateway 配置文件：
```bash
nano ~/.openclaw/gateway/config.json
```

2. 添加代理配置：
```json
{
  "network": {
    "proxy": {
      "http": "socks5://127.0.0.1:10808",
      "https": "socks5://127.0.0.1:10808"
    }
  }
}
```

3. 重启 Gateway：
```bash
openclaw gateway restart
```

## 🔄 自动化部署

### 定时检测（Cron 任务）
```bash
# 每小时检测一次代理
0 * * * * cd ~/.openclaw/workspace/skills/proxy-auto-config && python3 scripts/proxy_detector.py --configure --output ~/.openclaw/proxy_config >> ~/.openclaw/logs/proxy_check.log 2>&1
```

### 开机自启动
```bash
# 系统启动时配置 Gateway 代理
@reboot cd ~/.openclaw/workspace/skills/proxy-auto-config && python3 scripts/gateway_proxy_setup.py >> ~/.openclaw/logs/gateway_proxy_setup.log 2>&1
```

### 使用 systemd 服务
创建 `/etc/systemd/system/openclaw-proxy.service`：
```ini
[Unit]
Description=OpenClaw Proxy Auto-Config
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/$(whoami)/.openclaw/workspace/skills/proxy-auto-config/scripts/gateway_proxy_setup.py
User=$(whoami)
WorkingDirectory=/home/$(whoami)/.openclaw/workspace/skills/proxy-auto-config

[Install]
WantedBy=multi-user.target
```

## 🐛 故障排除

### 常见问题

#### 1. 代理检测失败
```bash
# 检查网络连接
ping 8.8.8.8

# 检查代理进程
ps aux | grep -E "v2ray|clash|ss-|xray"

# 检查端口监听
netstat -tlnp | grep :10808
```

#### 2. 环境变量未生效
```bash
# 重新加载配置
source ~/.openclaw/proxy_config/configure_proxy.sh

# 检查环境变量
env | grep -i proxy

# 测试代理连接
curl --socks5 127.0.0.1:10808 https://api.ipify.org
```

#### 3. Gateway 代理不工作
```bash
# 检查 Gateway 配置
openclaw gateway status

# 查看 Gateway 日志
tail -f ~/.openclaw/logs/gateway.log

# 测试 Gateway 网络
openclaw gateway test-network
```

### 调试模式
```bash
# 启用详细日志
python3 scripts/proxy_detector.py --verbose --debug

# 查看生成的配置
ls -la ~/.openclaw/proxy_config/
cat ~/.openclaw/proxy_config/configure_proxy.sh
```

## 🔒 安全注意事项

### ⚠️ 重要安全提示
1. **不要硬编码敏感信息** - 使用环境变量或配置文件
2. **验证代理来源** - 只使用可信的代理服务器
3. **定期更新** - 保持技能和代理工具最新
4. **监控日志** - 定期检查代理使用日志

### 安全配置示例
```python
# ❌ 错误：硬编码代理信息
proxy_url = "socks5://username:password@proxy.example.com:10808"

# ✅ 正确：使用环境变量
import os
proxy_url = os.getenv("PROXY_URL", "socks5://127.0.0.1:10808")
```

## 📊 性能优化

### 检测优化
```bash
# 快速检测模式（只检查常见端口）
python3 scripts/simple_proxy_check.py --fast

# 缓存检测结果
python3 scripts/proxy_detector.py --cache --ttl 300  # 缓存5分钟
```

### 资源使用
- **内存占用**: < 50MB
- **CPU 使用**: < 5% (检测时)
- **检测时间**: < 2秒 (快速模式)

## 🤝 贡献指南

### 报告问题
如果你发现任何问题，请：
1. 在 [GitHub Issues](https://github.com/MaiiNor/openclaw-skill-proxy-auto-config/issues) 报告
2. 提供详细的错误信息和重现步骤
3. 附上相关日志和配置

### 提交改进
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/MaiiNor/openclaw-skill-proxy-auto-config.git
cd openclaw-skill-proxy-auto-config

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- **OpenClaw 团队** - 提供了优秀的 AI 助手平台
- **v2ray 项目** - 优秀的代理工具
- **所有贡献者** - 感谢你们的反馈和改进建议

## 📞 支持与联系

### 获取帮助
- **GitHub Issues**: [报告问题](https://github.com/MaiiNor/openclaw-skill-proxy-auto-config/issues)
- **OpenClaw 社区**: [Discord](https://discord.com/invite/clawd)
- **文档**: [OpenClaw Docs](https://docs.openclaw.ai)

### 保持更新
```bash
# 关注仓库
git pull origin main

# 检查更新
openclaw skills update proxy-auto-config
```

## ⭐ 支持项目

如果这个技能对你有帮助，请：
1. 给仓库点个 ⭐ Star
2. 分享给其他 OpenClaw 用户
3. 提交改进建议
4. 报告遇到的问题

---

**最后更新**: 2026-03-29  
**版本**: 1.0.0  
**作者**: MaiiNor  
**状态**: ✅ 生产就绪

**Happy proxying!** 🚀