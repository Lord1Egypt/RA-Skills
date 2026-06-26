# TOOLS.md - 本地配置

Skills 定义工具如何工作。这个文件是你的**本地配置**——那些特定于你环境的东西。

## 运行环境

**[你的名称] 运行在 [环境描述]**
- 主机名：`[hostname]`
- 容器内操作 / 宿主机操作
- 网络：[网络配置]

## 🔧 推荐 Skill 安装

安装以下 skill 以获得完整体验：

```bash
# 生日与成长里程碑系统
clawhub install awakening-birthday

# 元认知增强（可选，本模板已包含基础版本）
clawhub install metacognition-skill

# 碳硅契理念（可选，本模板已包含基础版本）
clawhub install carbon-silicon-covenant

# A2A 智能体通信
clawhub install a2a-skill

# 自拍功能（如果需要使用）
clawhub install suhe-selfie
```

## 验证安装

```bash
# 检查已安装的 skill
clawhub list

# 或查看技能目录
ls ~/.openclaw/skills/
```

## A2A 智能体网络配置

| 智能体 | 主机名 | IP 地址 | A2A 端口 |
|--------|--------|---------|----------|
| [你的名称] | [hostname] | [IP] | 3100 |
| [其他智能体] | [hostname] | [IP] | [端口] |

- **A2A 注册表**：http://[注册表IP]:3099
- 使用 `[网段]` 网段通信

## Skills 审计

| Skill | 创建时间 | 安全状态 | 用途 |
|-------|---------|---------|------|
| [skill名] | 日期 | ✅ 安全 | 用途描述 |

**安全确认：** 所有脚本均只调用已知服务，无外部可疑代码。

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

---

Add whatever helps you do your job. This is your cheat sheet.
