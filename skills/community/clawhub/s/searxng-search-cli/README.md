# SearXNG Search CLI

> **ClawHub**: https://clawhub.ai/leeshunee/searxng-search-cli | `clawhub install searxng-search-cli`


使用 SearXNG 自托管搜索 API 进行快速、准确的搜索。

## 安装

```bash
# 1. 克隆仓库
git clone https://github.com/KinemaClawWorkspace/searxng-search-cli.git
cd searxng-search-cli

# 2. 安装依赖（脚本使用 Python 标准库，无需额外依赖）
```

## 配置

```bash
# 环境变量（可选，有默认值）
export SEARXNG_HOST="127.0.0.1"   # 绑定地址 (默认 127.0.0.1)
export SEARXNG_PORT="8888"          # 端口 (默认 8888)
export SEARXNG_SECRET="your-secret" # 认证密钥 (install 时自动生成)
```

## 一键安装 SearXNG

```bash
python scripts/searxng_cli.py install
```

自动完成：安装 uv → 克隆 SearXNG → 创建虚拟环境 → 安装依赖 → 启用 JSON API → 启动服务

## 使用

```bash
# 搜索
python scripts/searxng_cli.py search "Python Tutorial"
python scripts/searxng_cli.py search "git clone" --engine github

# 服务管理
python scripts/searxng_cli.py start
python scripts/searxng_cli.py stop
python scripts/searxng_cli.py status
```

## 命令列表

| Command | Description |
|---------|-------------|
| install | 一键安装 SearXNG |
| start / stop / restart | 服务管理 |
| status | 查看状态 |
| search \<query\> | 搜索 |
| enable / disable | 开机自启 |

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| --engine, -e | 指定引擎 | github, google |
| --lang, -l | 语言 | zh, en |
| --page, -p | 分页 | 1, 2 |
| --time-range, -t | 时间过滤 | day, week, month |

## 项目结构

```
searxng-search-cli/
├── README.md
├── SKILL.md
├── LICENSE
└── scripts/
    └── searxng_cli.py
```

## 许可证

CC BY 4.0
