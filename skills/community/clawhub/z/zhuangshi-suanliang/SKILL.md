---
name: zhuangshi-suanliang
slug: zhuangshi-suanliang
displayName: 装饰算量 · 概算与物资计划
version: 0.9.36
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "装修表/做法表出装饰概算；不替代清单结算。触发词：装饰算量、装修、做法表。"
i18n:
  en: README.en.md
  zh: README.md
locale: zh-CN
locales: [zh-CN, en-US]
---

# 装饰算量 v0.9.36

## 识图契约红线（硬规则，禁止绕行）

- 算量技能**不得单独识别 DWG/DXF/PDF**：识图只能由 `cad-file-reader` 做一次，产出统一契约后各技能共享复用。
- **禁止自行 `import ezdwg/read_cad`、自带或重新下载 cad-file-reader 解图**；底座缺失如实标 `unavailable`，不得降级成「自己解图」。
- 算量入口默认只认 `cad-contract/v1` 契约；表格输入必须显式加 `--allow-manual`，结果强制 `final_quantity=false`、`formal_ledger_eligible=false`。图纸输入不设任何“开发直读”逃生开关，DWG/DXF/DWT 一律退出 `23`。
- `lis-skill-bus` 是契约与算量技能之间的唯一定接线。
- DWG 解码兜底（ezdwg 读不了的 ACAD 新变体/损坏卷）只能在底座内用 `ODAFileConverter` 在副本上转 DXF 复扫校验；本技能不得调用 CAD/看图 App/ODAFileConverter。
- 内存双档：默认 `CAD_MEM_LIMIT_MB=4096`；仅实测超 4GB 真实大图且串行跑时临时 8192，不改全局默认；mem_guard 只终止识图子进程。

## 入口闸门（固定退出码，禁止 fallback）

本技能吃**表格输入**（CSV/TSV/XLSX），不经 CAD 识图。表格链路不强制 `cad-file-reader`/`lis-skill-bus`；走 `--contract` 时才校验契约，图纸输入一律拒绝。

| 退出码 | 含义 | 处理 |
|---|---|---|
| `0` | 表格/契约入口可用 | 继续 |
| `20` | 缺 `cad-file-reader` 或版本 < 0.41.0 | `--check-deps` 提示；表格输入不受影响 |
| `21` | 缺 `lis-skill-bus` 或版本 < 0.1.11 | `--check-deps` 提示；表格输入不受影响 |
| `22` | `--contract` 契约无效（版本/结构/来源/哈希/单位） | 停止，回 `cad-file-reader` 重新生成 |
| `23` | `--input` 或 `--contract` 是 DWG/DXF/DWT | 停止，改走 `cad-file-reader` 契约 |
| `24` | `--contract` 证据不足，或只有手工来源却要求正式量 | 停止；`--allow-manual` 结果 `final_quantity=false` |

固定提示：`本技能不直接识图，请先安装并调用 cad-file-reader 生成 cad-contract.json，再经 lis-skill-bus 传入；不许 fallback 到内置解析。`

表格输入输出固定 `input_channel=table`，报告写明“表格输入，不经 CAD 识图”。

## 使用说明（按需读取）

快速概算/明细算量命令、输入校验、输出字段、防水与规范复核、CAD 测量候选交接、依赖闸门与联动细节已外移到 `references/on-demand.md`；本文保留红线、入口闸门、口径、边界与授权。
## 口径

- **概算量**：清单/商务口径，取基面量，不含损耗、搭接、附加层。
- **材料订货量**：基面量 × 单耗 ×（1 + 损耗率）；卷材另乘搭接系数；附加层单独计算。
- **块料**：按单片面积向上取整。
- **门窗洞口**：必须扣；洞口侧壁按项目口径单列。
- **单价**：内置综合单价只是示例参考；正式概算以合同清单、地方信息价、企业定额和市场询价为准。
- 输出不用于结算、对量、竣工计量或正式报价。

## 边界

1. 装饰造型、线条、异形吊顶、复杂幕墙、楼梯细部不自动展开，先列待确认项。
2. 材料消耗默认值只是参考，不能替代项目做法表、节点详图或企业定额。
3. 图纸文字粘连、天正实体、表格跨页时可能漏读，必须用待确认项复核。
4. CAD 测量候选只作识图证据，`final_quantity=false`；做法映射、洞口扣减、侧壁、损耗和材料台账必须在本技能内完成，真图回归仍是后续增强项。
5. 不自动把公司数据上传云端，不联网解析图纸。


## 运行时

`scripts/*.sh` 自动解析 Python、cad-file-reader 和依赖路径。排障与手工安装见 `docs/runtime.md`。

## 授权与保留

CC-BY-NC-SA-4.0，仅限非商业用途。商业使用（含承接造价/算量咨询业务）须另行取得作者书面授权；作者保留全部商业权利（商业使用、再发布、封装收费、授予第三方商业授权）。条款全文见 `LICENSE.md`。

