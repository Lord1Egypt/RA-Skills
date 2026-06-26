---
name: thinktank-skill-finder
description: ThinkTank Skill Finder. 面向智库研究场景的技能检索、推荐、比选与技能包安装。用户提到“找 skill”“推荐 skill”“安装 skill”“装一套研究技能”“给我配智库研究工具链”“有没有适合行业研究/学术研究/新闻监测/报告写作/画图/PDF/表格/PPT 的 skill”时使用。
---
# ThinkTank Skill Finder v1.0.9

面向智库研究场景的一站式 Skill 发现与安装工具。支持通过 ClawdHub 镜像进行检索与安装，便于中国网络环境使用；既可按需推荐和安装单个 Skill，也可直接安装智库研究核心包，以及学术研究、动态监测、分析建模等增强包。技能包安装默认使用 `restricted` 模式，不安装需要 API Key 或依赖中国以外网络的 skill；如需完整能力，可切换到 `standard` 模式。个别 skill 若中国镜像暂未收录，脚本会自动回退到 ClawdHub 官方源安装。

路径约定：本文所有路径都相对于本 skill 目录。执行前先定位 `skills/thinktank-skill-finder/`，下文用 `<skill_dir>` 表示。默认安装目标是用户目录下的 `.agents/skills/`；也就是安装到 `<user_home>/.agents/skills/<skill-name>/`，适合 Trae IDE 这类读取 `.agents/skills/` 的环境。

## 功能

当用户问：

- "有什么 skill 可以做智库研究？"
- "找一个能做行业研究的 skill"
- "有没有画图/报告相关 skill"
- "安装智库研究技能包"

## 使用方法

### 1. 搜索 Skills

```bash
clawdhub search "<英文检索词>"
```

### 2. 查看详情（含统计数据）

```bash
clawdhub inspect <skill-name>
```

或者直接 API 查询 stats：

```bash
curl "https://clawhub.ai/api/v1/skills/<skill-name>" | jq '.skill.stats'
```

### 3. 安装单个 Skill

```bash
clawdhub install <skill-name> --no-input --registry=https://cn.clawhub-mirror.com

# 如果中国镜像里没有这个 skill，再回退到官方源
clawdhub install <skill-name> --no-input
```

### 4. 安装智库研究技能包（按 skills.csv）

```bash
# 列出可用的技能包
cd <skill_dir> && python scripts/install_bundle.py --list

# 安装核心包（默认 restricted 模式）
cd <skill_dir> && python scripts/install_bundle.py thinktank-core

# 安装多个包（自动去重）
cd <skill_dir> && python scripts/install_bundle.py thinktank-core academic-research-plus

# 完整安装模式
cd <skill_dir> && python scripts/install_bundle.py thinktank-core --mode standard

# 如果要覆盖默认安装目录，可显式指定 clawdhub workdir/dir
cd <skill_dir> && python scripts/install_bundle.py thinktank-core --workdir "D:/demo/.agents" --dir skills
```

### 5. 验证安装

```bash
clawdhub --workdir ~/.agents --dir skills list
或者查看单个 Skill 详情：
clawdhub --workdir ~/.agents --dir skills inspect <skill-name>
```

## 工作流程

```text
场景 A：推荐单个技能
1. 理解用户需求
2. 理解意图并改写为英文检索词
3. 搜索 ClawdHub
4. 列出相关 Skills（含下载量/stars）
5. 推荐最合适的单个 Skill，并提供安装命令
6. 如有需要，补一句引导：如果你后面还会经常做这类任务，我也可以继续帮你配一组相关技能。
7. 用户想配一组相关技能时，转入场景 B；用户只要当前单个 Skill 时，执行安装命令并完成验证

场景 B：安装技能包
1. 识别“安装技能包/全套/bundle”等意图
2. 调用脚本查看可用的技能包
3. 向用户介绍各个 bundle 的用途和适用场景，并确认：是按默认的 restricted 模式安装，还是连同需要 API Key 或依赖中国以外网络的 skill 一起安装（standard 模式）
4. 如果用户指定了一个或多个 bundle，且接受默认模式，就执行“安装智库研究技能包”里的 restricted 命令
5. 如果用户指定了一个或多个 bundle，并明确要把需要 API Key 或依赖中国以外网络的 skill 也一起装上，就执行“安装智库研究技能包”里的 standard 命令
6. 安装完成后执行验证，并简要说明当前使用的是 restricted 还是 standard 模式
```

## 输出格式

搜索结果应包含：

- Skill 名称
- 简短描述（中文）
- 下载量
- Stars 数
- 是否已安装

## 示例

**用户**: "找一个能做行业研究的 skill"

**搜索**: `clawdhub search "market research"`

**推荐输出**:

```text
🔎 "行业研究" 结果：

1. market-research-agent
   描述：行业研究、竞品分析和市场规模拆解
   下载：5,433 | Stars: 17 | ❌ 未安装
   → 推荐安装

安装命令: clawdhub install market-research-agent --no-input --registry=https://cn.clawhub-mirror.com
安装后验证: clawdhub --workdir ~/.agents --dir skills inspect market-research-agent
```

---

*帮助用户发现需要的智库研究 Skills 🔎*
