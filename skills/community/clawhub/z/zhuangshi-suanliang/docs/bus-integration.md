# 装饰算量 bus 联动

## lis-skill-bus 可选联动（试点，不强制）

- 状态过滤：项目名/楼栋/楼层一致时，本技能可与 `cad-file-reader` 及其它算量 skill 通过 lis-skill-bus 交换 `cad-contract/v1`；命中即复用，不再重复解图。
- 拉取（开工前，推荐）：`scripts/zhuangshi_statesync.sh pull --project 项目 [--building 楼栋] [--floor 楼层] [--out 落盘.json]`
  —— 命中且契约含本专业 section 字段（`rooms`、`room_schedules`、`practices`、`room_boundaries`、`measurements`、`views`）时返回 `hit=true usable=true`，可直接复用；未命中/缺字段/无 bus 一律返回 `hit=false`/`usable=false`，走本技能正常解析。
- 发布（算量落盘后，可选）：`scripts/zhuangshi_statesync.sh push --entry-file <本技能输出.json> --project 项目 [--building 楼栋] [--floor 楼层] [--specialty 装饰]`，自动包装成 `cad-contract/v1` 后入 bus。
- 对应接线脚本：`lis-skill-bus/integration/zhuangshi_pull_contract.sh` / `zhuangshi_publish_contract.sh`（薄壳，等价调用本技能 statesync）。
- 命中口径：`usable=true` 为本机状态里的「候选级命中」（`candidate_only=true`）；命中 section 内若有 `review_required`/P2/P3 项，statesync 只标 `review_flagged`，P0–P3 与复核项过滤仍在本技能算量核心按既有口径完成，不因 bus 命中而跳过滤。
- 命中开关（默认宽松）：默认仍为「至少一个 section 字段命中即 `usable=true`」的候选级命中；加 `--require-core` 后收紧为必选核心 section 至少一个命中且非空（装饰=`rooms` 房间 / `room_schedules` 做法表），缺核心时 `usable=false` 并把缺项写入 `review_flagged`。是否把默认改为收紧属业务口径，待用户/业务确认。
- bus 路径变更：仅需设置 `SKILLBUS_HOME` 指向新 bus 目录，本技能任何文件无需改动。
- 兼容/降级：客户端按如下优先级定位 `skillbus_client.py`，正式路径存在时不回退 dev 副本：
① `SKILLBUS_HOME`（bus 目录）或 `SKILLBUS_CLIENT`（直接指向 client 文件）显式指定
② `$HOME/.codex/mcp_servers/lis-skill-bus/skillbus_client.py`（正式安装落点）
③ `$HOME/.codex/skills/lis-skill-bus/skillbus_client.py` / `$HOME/.codex/skills/.skillbus/skillbus_client.py`
④ 常见本机开发副本（`tan/work` 等，最后才回退）。
命中 dev/临时副本时 stderr 会输出告警行「bus 命中来源：<路径>（临时副本/dev，非正式安装）」，正式路径输出「（正式安装）」；找不到 bus 时不报错，直接写 `$HOME/.codex/skills/.skillbus/state.json`（与 bus 同构，后续装 bus 可无缝读取）。 无 MCP/无 bus 不影响任何算量能力；本技能算法、口径、扣减、损耗、分账与台账逻辑不变。

- Windows 接线：GitHub 完整包 scripts/zhuangshi_statesync.cmd push/pull（GitHub/ClawHub 包含 .cmd，SkillHub 轻量包剔除 .cmd、Windows 改用同目录 .py 入口；macOS/Linux 用 `bash scripts/zhuangshi_statesync.sh` 等价调用）；等价 lis-skill-bus/integration/zhuangshi_publish_contract.sh / zhuangshi_pull_contract.sh。Windows 未实机跑通，仅静态校验通过（CRLF 行尾；无 /Users、/bin/sh、python3 硬编码；py 启动器 + %PYTHON%/%CODEX_PYTHON% 回退；默认路径用 %USERPROFILE%\.codex）。
