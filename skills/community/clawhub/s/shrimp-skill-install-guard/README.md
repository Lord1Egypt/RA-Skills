# Skill Install Guard｜技能安装守门员

> **一句话介绍**：在安装 OpenClaw skill 前后提供一套标准化安全流程：来源核验、全量文件审查、风险分级、安装放行/阻断、安装后验收。

## 这个 skill 能做什么

`skill-install-guard` 将“装 skill”变成可复盘的固定流程，避免凭感觉安装未知代码。

1. **来源核验**
   - 采集并展示关键来源信息（如作者、活跃度、更新时间、公开反馈等）
   - 缺失信息会显式标注，方便快速判断可信度

2. **全量文件审查（MANDATORY）**
   - 枚举目标 skill 文件并做审查覆盖统计
   - 区分文本与二进制文件，保留可解释的审查记录

3. **权限与风险评估**
   - 输出文件、网络、命令等权限需求
   - 给出风险等级与安装建议（放行/阻断）

4. **受控安装执行**
   - 仅在满足条件时执行安装命令
   - 对高风险或信息不充分场景保持保守策略

5. **安装后验收**
   - 校验目标目录是否落地
   - 校验 `SKILL.md` 等关键文件是否就绪

## 你会得到什么结果

- 一份结构化、可追溯的安装审查结果
- 清晰的风险等级与是否建议安装
- 明确的安装后验收结论（不是只看命令是否退出成功）

## 适合谁

- 经常安装第三方或陌生 skill 的个人用户
- 维护团队共享环境、需要统一安装标准的管理员
- 需要保留审计记录与复盘依据的安全敏感场景

## 核心价值

- **降低误装风险**：先核验再安装
- **统一流程标准**：每次安装都按同一质量门槛执行
- **结果可复盘**：从“看起来没问题”升级到“有证据可判断”

## 脚本入口

```bash
python3 scripts/skill-install-guard.py --slug <skill-slug> [options]
```

兼容包装器：

```bash
scripts/skill-install-guard.sh --slug <skill-slug> [options]
```

## 示例：本地非破坏性预检

```bash
python3 scripts/skill-install-guard.py \
  --slug some-skill \
  --source clawhub \
  --expected-dir skills/some-skill \
  --stop-before-install \
  --report-json tmp/skill-install-guard/some-skill-precheck.json
```

## 安装命令约束

`--install-cmd` 现在只接受**直接可执行命令**，不再通过 shell 解释执行。
这意味着应传入类似 `clawhub install some-skill` 的命令，而不要传 `cmd1 && cmd2`、管道、重定向等 shell 拼接写法。

## 示例：受控安装

```bash
python3 scripts/skill-install-guard.py \
  --slug some-skill \
  --source clawhub \
  --install-cmd 'clawhub install some-skill' \
  --expected-dir skills/some-skill \
  --report-json tmp/skill-install-guard/some-skill-install.json
```
