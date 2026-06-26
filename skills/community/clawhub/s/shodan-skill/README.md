# Shodan Skill for OpenClaw

<div align="center">

![Shodan](https://www.shodan.io/static/img/logo-6abcc86b.png)

An advanced, all-in-one Shodan wrapper skill for AI agents running on OpenClaw.

[English](#english) | [中文](#chinese)

</div>

---

<a name="english"></a>

## 🇬🇧 English

This skill provides a comprehensive interface to the Shodan API, enabling AI agents to perform advanced network reconnaissance, vulnerability scanning, and asset monitoring directly via natural language or structured commands.

### Features

- 🔎 **Advanced Search**: Full support for search filters (`vuln:`, `port:`, etc.) and facets (statistics).
- 📊 **Trends Analysis**: Generate statistics on global asset distribution (e.g., top countries using Nginx).
- 🔬 **Host Intelligence**: Deep inspection of IP addresses, including open ports, banners, and vulnerabilities.
- 📡 **Real-time Stream**: Tap into the Shodan Firehose for real-time data monitoring.
- 🛡️ **Network Alerts**: Manage network monitoring alerts to get notified of new exposures.
- 💣 **Exploit Search**: Search the Shodan Exploits database for CVEs and PoCs.
- 🌐 **DNS Toolkit**: Domain resolution and reverse lookups.
- 📚 **Built-in Docs**: Access Shodan filters and data dictionary directly from the CLI.

### Installation

#### Prerequisites

*   **OpenClaw**: Ensure you have OpenClaw installed and running.
*   **Python 3**: The skill relies on Python 3 environment.
*   **Shodan Library**: You need to install the official python library.

#### 1. Install Skill

Clone this repository into your OpenClaw skills directory (usually `~/.openclaw/skills/`):

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/liuweitao/shodan-skill.git ~/.openclaw/skills/shodan-skill
```

#### 2. Install Dependencies

Install the required Python library:

```bash
pip3 install shodan
```

#### 3. Configure API Key

You must configure your Shodan API Key before use. The skill reads the key from the standard Shodan CLI configuration or the `SHODAN_API_KEY` environment variable.

```bash
# Initialize Shodan with your API Key
shodan init YOUR_API_KEY
```

### Usage (for AI Agents)

Once installed, your AI agent (OpenClaw) will automatically detect the skill. You can ask it to:

*   "Search for vulnerable IIS servers in Japan."
*   "Count how many devices are running OpenSSH 7.4."
*   "Scan IP 1.2.3.4."
*   "Monitor my subnet 192.168.1.0/24 for unexpected ports."
*   "Find exploits for CVE-2019-0708."
*   "Stream realtime data for port 23."

---

<a name="chinese"></a>

## 🇨🇳 中文

这是一个专为 OpenClaw AI 智能体设计的高级 Shodan API 封装技能包。它允许 AI 直接调用 Shodan 的强大功能进行网络测绘、漏洞扫描和资产监控。

### 功能特点

- 🔎 **高级搜索**: 支持完整的搜索语法（`vuln:`, `port:` 等）和 Facets 统计分析。
- 📊 **趋势分析**: 生成全球资产分布的统计数据（例如：统计 Nginx 服务器的国家分布）。
- 🔬 **主机情报**: 深度查询 IP 地址详情，包括开放端口、Banner 信息和漏洞。
- 📡 **实时流**: 接入 Shodan Firehose 获取实时网络数据流。
- 🛡️ **网络监控**: 管理网络警报，监控 IP 暴露情况。
- 💣 **漏洞搜索**: 在 Shodan Exploits 数据库中搜索 CVE 和 PoC 代码。
- 🌐 **DNS 工具**: 域名解析和反查。
- 📚 **内置文档**: 内置 Shodan 搜索过滤器和数据字典速查。

### 安装指南

#### 前置要求

*   **OpenClaw**: 确保已安装并运行 OpenClaw。
*   **Python 3**: 本技能依赖 Python 3 环境。
*   **Shodan 库**: 需要安装官方 Python 库。

#### 1. 安装 Skill

将本项目克隆到 OpenClaw 的 skills 目录（通常是 `~/.openclaw/skills/`）：

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/liuweitao/shodan-skill.git ~/.openclaw/skills/shodan-skill
```

#### 2. 安装依赖

安装必要的 Python 库：

```bash
pip3 install shodan
```

#### 3. 配置 API Key

使用前必须配置 Shodan API Key。技能会自动读取系统标准的 Shodan 配置或 `SHODAN_API_KEY` 环境变量。

```bash
# 使用你的 API Key 初始化
shodan init YOUR_API_KEY
```

### 使用方法 (对 AI 说)

安装完成后，你的 AI 智能体 (OpenClaw) 会自动识别此技能。你可以直接用自然语言吩咐它：

*   “帮我搜索日本有哪些易受攻击的 IIS 服务器。”
*   “统计一下全球有多少台设备运行着 OpenSSH 7.4。”
*   “扫描一下 IP 1.2.3.4。”
*   “监控我的网段 192.168.1.0/24，有新端口开放时告诉我。”
*   “查找 CVE-2019-0708 的漏洞利用代码。”
*   “实时监听端口 23 的数据流。”

## Contributing / 贡献

欢迎提交 Pull Request！

## License

MIT
