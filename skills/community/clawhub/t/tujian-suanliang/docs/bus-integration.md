# 土建算量 bus 联动

## lis-skill-bus 可选联动（试点，不强制）

- 开工前先查共享状态：项目名/楼栋/楼层命中时直接复用 cad-file-reader 已发布的 `cad-contract/v1`，跳过重复解图。
- `run_qty` 一键接线：`scripts/run_qty.sh floor 图纸.dwg --floor-label "五层板配筋图" --with-geom -o 五层 --bus-pull --project 项目 [--building 楼栋] [--floor 楼层]`。命中且契约含可复用 `text_records + geometry_segments` 时，先把 cad 契约落到 `-o` 输出目录，建索引不再重复解图；未命中/无 bus/契约不可用一律走本机正常解析，不报错。`--bus-pull` 及其主键参数不会透传给算量核心。
- 独立拉取（调试/流程拆开用）：`scripts/qty_statesync.sh --project 项目 [--building 楼栋] [--floor 楼层] --out-dir 输出目录`，等价于 `lis-skill-bus/integration/qty_pull_contract.sh` 的自动落盘版。
- 核心门槛（土建默认已启用）：土建的必选核心为 `text_records + geometry_segments`（梁/板/柱/墙图元基础，缺任一即 `usable=false`，避免用空契约代真图），这是既有行为；新增 `--require-core` 仅为显式声明同一门槛，不改默认逻辑、可重复执行。是否对其它专业也默认开启 `--require-core` 属业务口径，待用户/业务确认。
- 兼容/降级：客户端按如下优先级定位 `skillbus_client.py`，正式路径存在时不回退 dev 副本：
① `SKILLBUS_HOME`（bus 目录）或 `SKILLBUS_CLIENT`（直接指向 client 文件）显式指定
② `$HOME/.codex/mcp_servers/lis-skill-bus/skillbus_client.py`（正式安装落点）
③ `$HOME/.codex/skills/lis-skill-bus/skillbus_client.py` / `$HOME/.codex/skills/.skillbus/skillbus_client.py`
④ 常见本机开发副本（`tan/work` 等，最后才回退）。
命中 dev/临时副本时 stderr 会输出告警行「bus 命中来源：<路径>（临时副本/dev，非正式安装）」，正式路径输出「（正式安装）」；找不到 bus 时不报错，直接写 `$HOME/.codex/skills/.skillbus/state.json`（与 bus 同构，后续装 bus 可无缝读取）。 bus 未安装时同样可用同一客户端读写本机状态文件（见 cad-file-reader 侧接线说明）。本技能自身口径、扣减、损耗、分账与台账逻辑不变。

- Windows 接线：GitHub 完整包 scripts/qty_statesync.cmd（SkillHub 版无 .cmd 时用 `bash scripts/qty_statesync.sh` 等价调用）；等价 lis-skill-bus/integration/qty_pull_contract.cmd。Windows 未实机跑通，仅静态校验通过（CRLF 行尾；无 /Users、/bin/sh、python3 硬编码；py 启动器 + %PYTHON%/%CODEX_PYTHON% 回退；默认路径用 %USERPROFILE%\.codex）。
