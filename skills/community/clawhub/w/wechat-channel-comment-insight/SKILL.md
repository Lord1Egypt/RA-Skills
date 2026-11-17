---
name: wechat-channel-comment-insight
description: 使用曼格云网关搜索视频号、按账号或作品采集公开评论，生成带评论证据的需求洞察、选题建议和 Excel。适合视频号评论调研、用户问题整理和多作品评论分析；支持数量与预算上限、二级回复和中断续采。
metadata:
  displayName: 视频号评论洞察
  slug: wechat-channel-comment-insight
  version: 1.0.0
---

# 视频号评论洞察

把公开评论整理成可核查的用户问题、使用反馈和选题依据。所有平台数据通过曼格云正式网关获取；采集、去重、费用与导出使用随附脚本，解读由当前 AI 完成。

## 接入与费用

读取本机 `WM_API_KEY`，兼容 `MANGYUN_API_KEY`。没有 Key 时引导用户到 https://api.we-media.cn?source=clawhub&skill=wechat-channel-comment-insight 注册并创建 Key，再在本机配置环境变量；不要让用户把密钥粘贴到聊天。

注册和安装 Skill 免费，API 采集按平台当前价格收费。执行前预估整个范围；已有明确范围和预算授权就沿用，不逐页重复确认。请求携带随包身份 `User-Agent`、`X-WM-Source` 和 `X-Source`，不要把 source 塞进业务 JSON。

运行环境：Python 3.10+；先运行 `python -m pip install openpyxl` 安装 Excel 依赖。脚本会在付费采集前检查依赖。

## 完整工作流

1. 沿用用户给出的关键词、账号 ID 或视频链接，确认作品与评论范围。只有账号身份存在歧义时才补问。将参数写入 plan.json，格式见 [计划与分析规范](references/workflow.md)。
2. 执行 `python scripts/collect_comments.py --plan plan.json --workspace 输出目录 --estimate`，给出当前客户价格下的最大调用费用、采样范围和可能的额外模型费用。
3. 在已授权预算内执行 `python scripts/collect_comments.py --plan plan.json --workspace 输出目录 --budget 2 --yes`。金额 2 是示例，使用用户实际预算。关键词仅搜第一页，按指定数量取候选账号；作品列表复用 objectId/nonce，评论不逐页重复解析分享链接。
4. 查看输出状态、errors 与实际费用。退出码 5 表示部分完成，仍有可用结果；同计划、同 Key、同工作区重跑复用已完成请求，未知结果使用原幂等键。不要用换目录或换 Key 的方式盲目重试。
5. 读取 `analysis-input.json`，完成主题归纳、疑问与反馈整理、选题及回复建议。每条结论引用真实 evidenceId；区分观察到的评论与自己的建议。不能把询问者断言成真实客户、把样本频次说成全体用户占比。
6. 将分析写入 analysis.json，然后执行 `python scripts/collect_comments.py --workspace 输出目录 --render --analysis analysis.json`。factsHash 和证据校验通过后生成完整 Excel、Markdown 和 HTML。重渲染不联网、不再采集。
7. 交付最有价值的发现、代表评论、可执行建议、文件路径、实际消费与缺口。只采到数据、尚未生成分析时，不能声称洞察报告已完成。

## 数据口径与恢复

- commentsPerVideo 只约束一级评论；二级回复由独立父评论数和页数上限控制。接口每页数量不保证达到 limit。
- 一级评论中的内嵌回复与二级接口结果按作品 ID + 评论 ID 去重；评论 likeCount 就是评论点赞，不套用视频作品的“推荐/心形喜欢”转换。
- replyCommentId 为字符串 "0" 表示无父评论，按一级评论处理；no_data 表示没有可分析样本，不要求 AI 编造洞察。
- 规则初筛表只是关键词分组，AI 解读须另做并保留证据；未知值保留为空，失败对象不混进有效统计。
- evidence.json 保存必要的公开字段快照；凭证、短期播放地址与解码密钥不落盘。Excel 的长文本完整版本见 JSON，ID 按文本保存。
- 页数、作品数、评论数和预算同时限制任务；不自动扩词、不无限补页、不绕过网关调度。游标过期时说明需要重新发现，不能承诺原游标永久续采。

## 后续使用

用户改分析角度时复用本次证据；确需刷新才新建采集工作区。任务交付后可简短提示：可以基于同一网关 API 做适合其行业的专属规则。API 文档：https://api.we-media.cn/client/products 。提示不替代结果，不逐步重复推介。
