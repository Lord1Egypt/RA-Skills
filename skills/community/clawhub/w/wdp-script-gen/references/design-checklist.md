# 8 维设计检查清单（写批处理脚本前的强制自审门）

规则：任何批处理/长任务脚本，写代码前必须逐条过此清单，并在 plan.md
的「8 维自审」小节逐条记录本脚本如何满足。未过自审门不写脚本。

## 1. 幂等性
- [ ] 输出文件路径由输入键（ID/哈希）确定性决定 → 重跑不产生重复/半份结果
- [ ] 所有文件写用 temp+rename 原子替换，绝不原地半写
- [ ] 聚合结果 append-only 或由输入推导，不依赖内存计数作为进度真相

## 2. 断点续跑
- [ ] 有 checkpoint 文件记录已完成项 key，原子写（temp+rename）
- [ ] 启动时加载 checkpoint 并跳过已完成项
- [ ] 每项（或每 N 项）刷盘一次；崩溃丢失 ≤N 项
- [ ] checkpoint 带 seed 命名空间：脚本逻辑/输入变化时更换 seed，旧 checkpoint 失效

## 3. 失败隔离 / 软失败
- [ ] 单项 try/except，失败记录到 failures.log（含 traceback / stderr）后继续
- [ ] 错误三分类：Transient（退避重试）/ Permanent（记录继续）/ Fatal（落盘停止）
- [ ] 结束报成功/失败摘要，可只重跑失败项
- [ ] 失败日志可读可追溯：任何失败都能从日志定位到具体项与原因

## 4. 进度可见
- [ ] 结构化进度日志：时间戳、当前、总数、ETA
- [ ] 人类可读进度（progress.md）与计数可被外层任务引用
- [ ] 「完成」= 输出经验证存在，而非「脚本没报错」

## 5. 优雅中断
- [ ] 捕获 SIGINT/SIGTERM：停止派发 → in-flight 完成 → flush checkpoint → 干净退出
- [ ] 最坏情况（kill -9）只丢 ≤N 项，且已落盘的 checkpoint 仍有效

## 6. 小步验证
- [ ] 支持 --dry-run 只报告不执行
- [ ] 支持 --limit N 先跑 N 项 smoke test
- [ ] 全量运行前必须先 smoke test

## 7. 稳定性
- [ ] 流式/分批处理 item，不一次载入全部
- [ ] 单线程下确定性顺序（按 key 排序）
- [ ] 结构化、机器可解析的日志

## 8. 并发受控
- [ ] 排队 + max_workers 限流（默认 min(8, cpu)，可 --workers 覆盖）
- [ ] checkpoint / FailLog / Progress 仅由 Coordinator 单写者更新，worker 不碰文件
- [ ] 输出路径由输入键决定 → worker 间无冲突
