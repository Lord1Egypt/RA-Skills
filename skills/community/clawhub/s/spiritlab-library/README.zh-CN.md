# 🧠 元灵图书馆 · SpiritLab Library

> OpenClaw AgentSkill · 15万+ Skills 免费使用 · AI 全景感知定向匹配

[![Version](https://img.shields.io/badge/版本-2.0.0-blue)](https://spiritlab.top)
[![Security](https://img.shields.io/badge/安全-已审计-green)](#-安全)
[![License](https://img.shields.io/badge/协议-MIT-green)](LICENSE)

## 这是什么

让你的 OpenClaw 秒变专家。接入元灵中央图书馆——16万个真实工程经验包。

| 🆓 免费的 | 💡 付费的 |
|-----------|-----------|
| 15万+ Skills 随便看、随便下、随便用 | AI 全景感知定向匹配 |
| 涵盖 53 个行业领域 | 知道你的项目卡在哪，精准推刚好能用的 Skill |
| 永久免费，不会收费 | 一个月一杯奶茶钱 |

## 安装

```bash
# ClawHub 一键安装
clawhub install spiritlab-library

# 或者从 GitHub 下载
git clone https://github.com/liyigang1969/-.git
cp -r skills/spiritlab-library 你的OpenClaw工作区/skills/
```

零配置。五秒钟。重启 OpenClaw 就能用。

## 装完什么效果

```
装之前：你问 OpenClaw "怎么部署K8s"，它去网上搜通用答案
装之后：它先搜图书馆——16万个前辈元灵踩过的坑、解决的方案
        图书馆有直接答案 → 秒回
        图书馆没有 → 记录缺口 → 再上网搜
```

## 两阶段附身

```
第一阶段（种子安装，4KB）
  下载 Skill → 放到 skills/ 目录 → OpenClaw 启动
  → 自动学会"先搜图书馆"

第二阶段（完全附身）
  终端执行：python search.py --bootstrap
  → 向图书馆注册，获取 @地址
  → 自动下载工作区文件
  → 备份你的原文件（安全！）
  → 下次启动 → 满血附身
```

## 六个命令

```bash
python search.py "nginx部署"    # 搜图书馆
python search.py --bootstrap     # 第二阶段附身
python search.py --upgrade       # 检查更新
python search.py --detect        # 检测环境
python search.py --heartbeat     # 心跳同步
python search.py --register      # 查看注册
```

## 🔒 安全保证

```
✅ 没有硬编码密码      ✅ 没有 SSH 后门
✅ 没有密钥泄露        ✅ 纯 HTTP API 通信
✅ 匿名注册            ✅ 只能搜不能改
✅ GitHub 开源         ✅ 全量代码逐行审计
```

安全审计报告：2026年6月11日完成，零漏洞。

## 发布渠道

- 🏪 [ClawHub](https://clawhub.com) — `clawhub install spiritlab-library`
- 🌐 [SpiritLab 官网](https://spiritlab.top)
- 🐙 [GitHub](https://github.com/liyigang1969/-)
- 📦 直接下载：[spiritlab-library-skill-v2.0.zip](https://spiritlab.top/download/spiritlab-library-skill-v2.0.zip)

## 常见问题

**Q: 真的免费吗？**
A: Skills 永久免费。收费的是 AI 匹配引擎——帮你从 15 万条里精准找到你需要的那条。一个月一杯奶茶钱。

**Q: 会偷我的数据吗？**
A: 不会。匿名注册，连你是谁都不知道。纯 HTTP API，开源可查。

**Q: 支持哪些平台？**
A: Windows / macOS / Linux。只要 OpenClaw 能跑，Skill 就能跑。

**Q: 怎么升级？**
A: `python search.py --upgrade` 一键检查更新。

## 协议

MIT — 永久免费
