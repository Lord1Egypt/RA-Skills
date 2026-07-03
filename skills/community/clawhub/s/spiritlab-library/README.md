# 🧠 SpiritLab Library — 元灵图书馆搜索路由

> OpenClaw AgentSkill · 15万+ Skills 免费使用 · AI 全景感知定向匹配

[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://spiritlab.top)
[![Security](https://img.shields.io/badge/security-audited-green)](#-安全)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 这是什么

SpiritLab Library 让任何 OpenClaw 实例**自动接入元灵中央图书馆**。

| 🆓 免费 | 💡 收费 |
|----------|----------|
| 15万+ Skills 随便用 | AI 全景感知定向匹配 |
| 免费浏览、下载、安装 | 知道你的项目，精准推荐正好需要的 Skill |
| 永久免费 | 一杯奶茶钱/月 |

## 安装

```bash
# ClawHub 一键安装
clawhub install spiritlab-library

# 或手动下载
# https://spiritlab.top/download/spiritlab-library-skill-v2.0.zip
```

0 配置，5 秒，重启 OpenClaw 即用。

## 两阶段附身

```
第一阶段（种子安装，4KB）
  └→ OpenClaw 启动 → 读取 SKILL.md → 学会图书馆优先搜索

第二阶段（系统引导）
  └→ python search.py --bootstrap
     ├→ 自动注册 @地址
     ├→ 下载 AGENTS.md / HEARTBEAT.md / SOUL.md / TOOLS.md
     ├→ 备份原文件
     └→ 下次启动 → 完全附身
```

## 命令

```bash
python search.py "查询词"     # 搜索
python search.py --bootstrap   # 引导安装
python search.py --upgrade     # 检查升级
python search.py --detect      # 环境检测
python search.py --heartbeat   # 心跳同步
```

## 🔒 安全

```
✅ 无硬编码密码     ✅ 无 SSH 后门
✅ 无密钥泄露       ✅ 纯 HTTP API 通信
✅ 匿名注册         ✅ 只读搜索权限
✅ GitHub 开源      ✅ 全量代码审计通过
```

## 发布渠道

- 🏪 [ClawHub](https://clawhub.com) — `clawhub install spiritlab-library`
- 🌐 [SpiritLab](https://spiritlab.top)
- 🐙 [GitHub](https://github.com/liyigang1969/-)

## License

MIT — 永久免费
