---
name: wdp-work-mgr
description: 长时/批量脚本开发与任务跟踪：目标规划、TODO、逐任务验证标记、进度可见、断点续跑、并发受控、失败日志可见。生成的批处理脚本会嵌入可恢复机制（checkpoint 断点续跑、失败日志、并发限流、错误重试、信号处理）并读写工作目录文件。检测到「处理大量文件/长任务」时启用；发现已有 work/state.json 时先报进度再续跑。
---

# wdp-work-mgr：可恢复批处理与任务跟踪

## 何时触发
- 用户要批量处理大量文件/长任务/写批处理脚本，且明确是「要跑一批任务」
- 用户显式调用本 skill
- 会话启动时项目内已有 work/state.json → 先呈现进度，询问「续跑 or 重来」

## 何时不触发
- 只问单个文件/简单问题 → 不启动状态机、不写 work/
- 用户没有批处理/长任务意图
- 旧 state/checkpoint 仅当用户明确选择「续跑」时才读取

## 工作区（本 skill 唯一的写范围）
本 skill 只写当前项目内的 work/ 目录（plan.md / state.json / progress.md / logs/，字段与
schema 见 references/protocol.md 与 spec）；生成的批处理脚本只写 manifest 声明的输入/输出
目录，且输出路径由输入键确定性命名（temp+rename 原子写）。不触碰 work/ 之外的任何文件，
除非用户明确指定。

## 生命周期
1. 规划：把目标拆成任务，每个任务含验收标准（verify）；写 plan.md + state.json（全 pending）
2. 生成：对每个脚本任务，先写「8 维自审」小节（references/design-checklist.md），未过门不写脚本；
   优先嵌入 templates/wdp_checkpoint.py，参照 templates/batch_runner.py
3. 执行：smoke test（--limit 2-3 项）→ 全量跑 → verify 通过才标 done → 重渲染 progress.md
4. 恢复演练：首个批脚本生成后，先告知用户「将故意中断一次运行做断点演练」并取得同意；
   用小样本（--limit 2-3 项）演练，优先优雅中断（SIGTERM），需验证硬杀恢复时用合成数据；
   演练后报告只跑剩余项、计数吻合、无重复处理、输出无损
5. 续跑：见 references/protocol.md（读 state → 读 failures.log → verify done → 从断点续）

## 硬性规则
- 状态机：唯一进入 done 的路径是 verify 通过
- progress.md 每次状态变更时重生成；失败摘要必含计数、日志路径、最近失败
- checkpoint 必须带 seed；逻辑/输入变化时换 seed
- 并发仅脚本内层（run_batch 单写者）；外层任务串行
- 失败日志 failures.log 是唯一失败真相来源，任何失败必须可见可追溯

## 恢复协议
完整流程见 references/protocol.md。核心：续跑第一步读失败日志分类处理；
对 done 任务信任但验证；in_progress 批任务按 checkpoint 续跑。

## 交付物清单
每次本 skill 产出的脚本，都应满足 references/design-checklist.md 的 8 维；
模板与参考实现位于 templates/。
