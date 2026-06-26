<p align="center">
  <img alt="以史为鉴.skill" src="https://img.shields.io/badge/%E4%BB%A5%E5%8F%B2%E4%B8%BA%E9%89%B4.skill-Decision%20Sandbox-000000?style=for-the-badge">
</p>

<h1 align="center">以史为鉴.skill</h1>

<p align="center">
  <strong>把中国历史案例，变成现实决策的结构化分析与沙盘推演工具。</strong><br>
  <strong>Chinese History Decision Skill for Claude Code &amp; OpenClaw</strong><br>
  现实里的难题，往往不是缺一个建议，而是看不清自己身在什么局。<br>
  团队内耗、改革推不动、盟友不稳、资源不如对手、该换人还是再等等，<strong>以史为鉴.skill</strong> 会让 agent 先识局、再鉴史、最后推演可选路径的收益、风险和失败点。
</p>

<p align="center">
  <code>LearnFromHistory-skill</code> · <code>yi-shi-wei-jian</code>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-16a34a">
  <img alt="Runtime" src="https://img.shields.io/badge/Runtime-Claude%20Code%20%7C%20OpenClaw-111827">
  <img alt="Skill Slug" src="https://img.shields.io/badge/Slug-yi--shi--wei--jian-7c3aed">
</p>

`LearnFromHistory-skill` 是一个面向 Claude Code 和 OpenClaw 的 Agent Skill。

它不做历史百科式讲解，而是把现实问题拆成三步：

- 识局：先判断你现在处在什么局
- 鉴史：再找 2-4 个结构相似的历史案例
- 推演：最后给出多条路径，并逐条做沙盘推演

如果你想做的不是“聊历史”，而是“借历史帮助决策”，这个仓库就是为这个场景设计的。

## Why This Skill

大多数“历史类比”工具的问题，不是不会举例，而是停在举例。

这个 skill 的目标是把历史案例真正转成可用的决策分析，固定输出：

- `【局面判断】`
- `【历史参照】`
- `【关键变量】`
- `【可选路径】`
- `【沙盘推演】`
- `【借鉴原则】`
- `【边界提醒】`

其中 `【沙盘推演】` 是核心差异点。它不会只给一句建议，而是把每条路径拆成：

- 适用条件
- 短期收益
- 短期风险
- 中期演化
- 最容易失败点

## What You Get

当前仓库已经包含：

- 40 条结构化中国历史案例
- 可持续扩充的用户案例库 `data/user_cases.json`
- 面向分类、检索、比较、推演和安全边界的 prompts
- 可本地运行的 Python CLI
- 发布检查、安装检查和自动化测试

项目身份如下：

| Item | Value |
| --- | --- |
| GitHub repository | `LearnFromHistory-skill` |
| Skill name | `以史为鉴` |
| Skill slug | `yi-shi-wei-jian` |
| Entry file | `SKILL.md` |
| Runtime | Python 3.10+ |
| License | MIT |

## A Quick Example

用户输入：

```text
我接手一个派系很重的团队，资源不多，但必须在两个月内推动新制度上线。我现在该先稳内部，还是直接推进改革？
```

skill 不会只回答“先稳后推”这种空话，而会输出类似这样的结构：

```text
【局面判断】
主局面：改革推进
次局面：内部冲突、以弱对强

【历史参照】
1. 秦孝公任用商鞅变法
2. 王安石变法
3. 吴起相楚变法受挫

【关键变量】
- 执行链条
- 利益补偿
- 时间窗口
- 合法性

【可选路径】
1. 先整执行链
2. 试点推进
3. 强授权直推
```

## Install In One Minute

### OpenClaw

ClawHub 安装：

```bash
clawhub install yi-shi-wei-jian
```

或者直接跟你的龙虾说：

```text
安装以史为鉴 skill
```

手动安装：

```bash
git clone https://github.com/GreatXiaoRY/LearnFromHistory-skill.git skills/yi-shi-wei-jian
```

### Claude Code

项目级安装：

```bash
git clone https://github.com/GreatXiaoRY/LearnFromHistory-skill.git .claude/skills/yi-shi-wei-jian
```

全局安装：

```bash
git clone https://github.com/GreatXiaoRY/LearnFromHistory-skill.git ~/.claude/skills/yi-shi-wei-jian
```

安装完成后重启会话，让宿主重新加载 `SKILL.md`。

## Natural Language Usage

分析现实问题：

```text
请用以史为鉴分析：我必须联合一个不完全信任的合作方，对抗更强的对手，但我担心项目一推进，对方就会翻脸。
```

新增案例入库：

```text
把“赵武灵王胡服骑射”这个案例加入案例库，后续检索也要能用。核心局面是改革推进和以弱对强，关键决策是主动改制，来源请记《史记·赵世家》。
```

安装后，宿主 agent 可以先补齐缺失字段，再把整理后的结构化案例写入本地库，供以后继续检索使用。

## Add New Cases

这个项目不把案例库写死在最初的 40 条里。

基础案例位于：

- `data/historical_cases.json`

用户新增案例位于：

- `data/user_cases.json`

查看新增案例模板：

```powershell
python src/main.py --print-case-template
```

从文件写入新案例：

```powershell
python scripts/add_case.py --case-file path\to\new_case.json
```

直接通过标准输入写入：

```powershell
@'
{ ... 单条案例 JSON ... }
'@ | python scripts/add_case.py --stdin
```

`--stdin` 这一条很重要，因为它让 Claude Code / OpenClaw 这类宿主可以把自然语言整理后的结构化结果直接写入案例库，而不要求用户手工编辑 JSON 文件。

## Local CLI

分析问题：

```powershell
python src/main.py --question "我接手一个派系很重的团队，资源不多，但必须在两个月内推动新制度上线，我该怎么布局？"
```

打印案例模板：

```powershell
python src/main.py --print-case-template
```

直接新增案例：

```powershell
python src/main.py --add-case-json "{...单条案例 JSON...}"
```

## Development

环境准备：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

本地验证：

```powershell
python scripts/validate_cases.py
python scripts/verify_install.py
python scripts/check_release.py
python -m unittest discover -s tests
```

`.github/workflows/ci.yml` 会在 GitHub Actions 中执行同样的检查。

## Project Structure

```text
LearnFromHistory-skill/
├─ SKILL.md
├─ README.md
├─ skill.json
├─ manifest.json
├─ data/
│  ├─ historical_cases.json
│  ├─ user_cases.json
│  └─ cases.schema.json
├─ prompts/
├─ examples/
├─ scripts/
├─ src/
└─ tests/
```

## Notes

- 仓库名是 `LearnFromHistory-skill`
- 技能安装目录必须是 `yi-shi-wei-jian`
- 仓库只使用本地数据和相对路径，不依赖外部 API
- `user_cases.json` 会随着用户新增案例持续扩充
- 项目结构已经按 Claude Code / OpenClaw / ClawHub 分发场景整理

## License

本仓库采用 [MIT License](LICENSE)。
