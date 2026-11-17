# 重试策略（`_with_retry` 契约）

> 本文件是 SKILL.md 中多次提到的 `_with_retry` 的**唯一定义源**。
> 所有"外部调用"（skillhub 搜索、推送等）统一遵守以下契约，确保行为一致、不整轮崩。
> 改这里的参数 = 改全局重试行为，请勿在 SKILL.md 正文重复定义。

## 契约参数
- **最大重试次数**：2 次（不含首次，共 3 次尝试）
- **退避序列**：2s、5s（每次重试前等待；与 `usage_diag.py` 的 `proxy_reachable(retry=2, backoff=(2,5))` 保持一致）
- **最终失败处理**：标记该项为"部分失败 / 跳过"，写入报告并标注，但**绝不**抛异常终止整轮检查。

## 两类外部调用的落地方式

### A. Shell 命令（如 skillhub 搜索）
直接用脚本封装，确定性最高：
```bash
python scripts/retry_helper.py --max-retries 2 --backoff 2,5 -- skillhub search "<关键词>"
```
- 退出码 `0` = 成功；`2` = 重试耗尽（调用方 mark-and-skip）；`3` = 本脚本参数错误。
- stdout 逐字透传，便于解析；进度信息走 stderr，不污染 stdout。

### B. 工具调用（如推送 SendMessage / 企微 bot）
工具调用无法用 shell 包装，按以下伪代码**自律重试**（语义与 A 完全一致）：
```
attempts = 3
for i in range(attempts):
    if i > 0:
        sleep([2, 5][(i - 1) % 2])
    result = 调用推送工具(摘要)
    if 成功(result):
        break
else:
    # 仅落文件 + 报告横幅，不整轮崩（详见 SKILL.md「推送」段自愈逻辑）
    标记 push_status="failed"，记录 push_failed_at / push_fail_reason
```

## 为什么这么设计（讲 why，不堆 must）
- 弱网 / 限流是常态，外部调用失败**不应污染本地检查**（本地项才是高频价值）。
- 统一退避避免对远端造成重试风暴，也对齐诊断脚本的代理重试口径。
- 标记跳过而非中止，保证"本地检查照常、网络项下轮自动补齐"的弱网友好体验。
