# 记录、同步与版本

CLI 输入示例（用户原话，不要将 AI 改写标成用户）：

```json
{
  "kind": "entry",
  "title": "今天的一点想法",
  "body": "用户实际说过的内容",
  "author": "user",
  "tags": [],
  "source": { "agent": "当前宿主", "conversation": "当前私人对话" },
  "refs": [],
  "fields": { "entryType": "thought" }
}
```

`kind` 支持 entry、summary、observation、plan、knowledge、review；transcript 仅由可信采集器生成。AI 撰写时 `author: ai`，自动保持草稿。观察需完整来源与证据字段，计划需通过原有验证规则并引用已确认方法。

观察使用 `fields.observation`，结构为 `{ "kind": "hypothesis", "content": "待验证解释", "sourceSessionId": "来源原话记录的UUID", "sourceRefs": ["来源记录ID"], "evidence": [], "counterEvidence": [], "confidence": 0.4 }`。kind 还可为 user_report、emotion、need、action、outcome、pattern、clinician_note；AI 解释不确定动机，hypothesis 置信度不超过 0.7。顶层 refs 同样保留来源 ID。

练习使用 `fields.plan`：`goal`、`exercise`、`frequency`、`metric`、`feedbackMethod`、`optOut` 均为非空文本；`stopConditions` 为非空字符串列表；`durationWeeks` 为 1–4；`sourceRefs` 至少包含一条已确认知识的记录 ID。一次一个目标，正文同时说明来源、退出方式与停止条件。不得改写为诊断或用药计划。

`write --input <文件>` 新建记录；`edit --id <ID> --revision <完整版本> --input <文件>` 修改正文、标题或标签。编辑 AI 内容重新进入草稿。原始对话不得由模型编辑后冒充原文。

`search --query <文本>` 默认最多 8 条短片段，显示来源与记忆资格；需要细节再 `read --id <ID>`。AI 草稿可明确读取以审核，但不进入正式记忆检索。

同步采用不可变内容版本、稳定逻辑 ID 和操作 ID。云库的“同步版本”用于完整快照；面向人的库保存可读原文和审核状态。长记录分片，不原地替换旧正文。可在 FlowUs 修改可读页面，下一次同步把修改保留为新版本。正文暂只支持文本块；未知或嵌套内容会报错，不丢掉不认识的部分。

查看库中旧版本时注意版本号与时间；新旧版本可能同时可见，实际记忆由程序按版本谱系筛选。不要自行删除“同步版本”里的中间片段。需要停止引用用 Excluded，需要删除用 Deleted 或私人命令；缺失页面或权限错误不是删除授权。

`sync` 返回 ok、pending、conflicts、jobs 与 lastSync。`ok: false` 表示还没有完成本次同步，不得报告成功。第一版完整扫描库，适合个人数据量；不是实时推送服务。

双端并发修改保留所有分支，`conflicts` 显示候选。本人可在终端用 `resolve --id <ID> --revision <所选版本>` 或在私人命令里先 `show <ID> <所选版本>` 再 `resolve`。裁决前不会作为记忆检索；存在删除分支时裁决也不会恢复正文。

本地 SQLite 的正文、标签、标题、来源、同步元数据、待处理任务均加密。检索在内存解密后进行，没有明文全文索引。备份数据库必须同时保留对应的秘密配置；云库可被其他安装实例拉取，各实例使用自己的本地密钥。

`export-consultation --from <ISO时间> --to <ISO时间> --records <明确选择的ID,...>` 生成便携 Markdown 咨询资料包，只包含时间范围内已确认、未删除、未停止引用的结构化记录。未确认草稿与全文不会自动进入导出；PDF 仍可使用原项目的可选渲染流程。
