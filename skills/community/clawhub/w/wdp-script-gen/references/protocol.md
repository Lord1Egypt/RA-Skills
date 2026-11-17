# wdp-work-mgr 恢复协议

## work/ 工作区约定
- work/plan.md     目标、假设、任务清单（每任务含验收标准）
- work/state.json  机器可读单一事实来源（schema 见 spec §5.2），AI 原子写
- work/progress.md 由 state 渲染的进度视图，每次状态变更时重生成
- work/logs/       脚本运行日志 + failures.log（唯一失败真相来源，JSON-lines）

## 任务状态机
pending → in_progress → done（唯一进入 done 的路径 = verify 通过）
                     └→ failed（诊断修复后只重跑该任务）
verify 失败或输出缺失 → 打回 pending

## 首次启动（无 work/state.json）
1. 规划：目标 → 拆任务 → 写 plan.md + state.json（全 pending）
2. 逐任务：脚本过 8 维自审门 → smoke test（2-3 项）→ 全量跑 → verify → 标 done
3. 首个批处理脚本生成后做「恢复演练」（见下）

## 续跑（存在 work/state.json）
1. 读 state → 呈现进度摘要
2. 读失败日志：work/logs/failures.log 按 category 分类——
   - 重试后仍失败的项 → AI 诊断修复，或对其 --retry-failures
   - 无法修复的项 → 记录在任务 note，不阻塞整体
3. 信任但验证：对每个 done 任务重查 verify 条件，输出缺失 → 打回 pending
4. in_progress 批任务：读其 checkpoint，done+failed==total 则标 done，否则从断点续
5. 从第一个未完成任务继续

## 恢复演练（resume drill，强制）
首个批处理脚本生成后：先向用户说明「将故意中断一次运行做断点演练」，取得同意后用小样本
（--limit 2-3 项）演练——优先用优雅中断（SIGTERM）验证收尾；需验证硬杀恢复时，用合成数据
而非用户真实数据。演练后报告：只跑剩余项、计数吻合、无重复处理、输出无损
（硬杀允许 ≤max_workers 项重复工作但输出不损坏）。
这是证明断点真生效的强制动作，不是赌它生效。

## 触发条件
- 检测到批处理 / 大量文件 / 长任务意图时主动启用
- 会话启动时发现项目内已有 work/state.json → 先报进度，询问「续跑 or 重来」

## 失败日志可见性
- failures.log 行字段：ts, item_key, category, retries, error_type, error_msg, traceback, stderr_tail
- progress.md 必须渲染失败摘要：计数 + 日志路径 + 最近若干条（item/错误/时间）
- 「完成」= 验证输出通过；失败数来自 failures.log 而非内存
