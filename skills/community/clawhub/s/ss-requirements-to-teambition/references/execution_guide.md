# HK 需求采集 — AI 执行指南

## 数据文件

路径：`scripts/hk_需求/data/hk_需求_YYYY-MM-DD.json`

```json
{
  "sessions": [
    {
      "session_id": "jgdxgrv",
      "customer_name": "HelpKnow.ai 服务群",
      "ss_project_id": "27828",
      "messages": [
        {
          "sender_type": 1,    // 1=客户, 2=客服
          "sender": "xxx",     // sys_user_id（客服时用）
          "text": "客户消息内容",
          "send_time": 1748054400000  // 毫秒时间戳
        }
      ]
    }
  ]
}
```

---

## 客服姓名映射

路径：`scripts/hk_需求/agent_names.json`

```json
{
  "uid_to_real": {
    "187751": "游鸿凯",
    "975520": "张梦非",
    ...
  }
}
```

接待客服真实姓名从 `uid_to_real` 查 `sender`（sys_user_id）。

---

## TB 任务创建

**调用**：`teambition-mcp__createTaskV3`

### 标准 note 格式（参考 TB#789-296）

```
## 涉及客户
[客户名称] | SS项目ID: [ss_project_id]

## 客户业务场景
[客户背景、当前使用情况]

## 需求详情
1. **问题一标题**：问题描述。客户原话。客服处理结果。
2. **问题二标题**：问题描述。客户原话。客服处理结果。

## 会话信息
- SS会话ID: [session_id]
- 接待客服: [真实姓名]
- 时间: [YYYY-MM-DD]
- 标签: [标签名]
```

### 示例

```json
{
  "projectId": "6959d07f4991ad9a71ca2afa",
  "scenariofieldconfigId": "6959d080d242a000e6f0de59",
  "stageId": "69fed981a6333372a4b12b72",
  "content": "[27828] 新建AI员工时找不到首次创建时的4种角色预设人设模板",
  "note": "## 涉及客户\nHelpKnow.ai 服务群 项目ID:27828 | SS项目ID: 568206,624697\n\n## 客户业务场景\n客户在HelpKnow服务群中咨询AI员工功能。客户首次创建AI员工时有4种角色模板（含预设提示词），但第二次创建时找不到这些预设模板，导致需要手动编写完整人设，体验不佳。\n\n## 需求详情\n1. **预设角色模板消失**：客户反馈\"我刚刚创建第一个AI员工的时候，好像有4种角色可以选，里面自带了提示词。现在找不到了\"。客服确认第一个是旧版AI机器人（旧版回复AI员工），新版AI员工没有预设角色模板。\n2. **旧版机器人用途**：客户询问旧版机器人是否还有用。客服建议使用新版AI员工回复，旧版已不推荐使用。\n3. **人设需要手动编写**：客户表示新创建的AI员工人设要自己写，\"我又懒得写\"。客服建议编辑之前的AI员工复制人设内容。客户反馈之前没有创建成功，所以没有可复制的内容。客服建议在旧版机器人的设置中查看是否有人设内容。\n\n## 会话信息\n- SS会话ID: jgdxgrv\n- 接待客服: 游鸿凯\n- 时间: 2026-05-23\n- 标签: HelpKnow需求",
  "customfields": [
    {
      "customfieldName": "需求orBUG",
      "value": [{"id": "69df253e95d7ece67f2d6e95", "title": "需求"}]
    },
    {
      "cfId": "69df25e800b8437a49b4840e",
      "value": [{"title": "jgdxgrv"}]
    },
    {
      "cfId": "6a1422a4f4593ff6edd1ee63",
      "value": [{"title": "HelpKnow.ai 服务群 项目ID:27828"}]
    },
    {
      "cfId": "69e055b3f2ad64465068810e",
      "value": [{"title": "27828"}]
    }
  ]
}
```

**字段填写规范**：
- `需求orBUG`：单选，用 `customfieldName` + `value.id`
- 文本字段（会话ID/客户名称/项目ID）：用 `cfId` + `value.title`

---

## TB 追加备注

**调用**：`teambition-mcp__updateTaskNoteV3`

追加格式（接在原 note 内容后）：
```
——更新 [时间]（session: [session_id]，客服：[接待客服真实姓名]）——
[本次新增的需求详情]

---
[原有 note 完整保留]
```

**操作**：先 `queryTaskV3` 读出原 note，再拼接，最后 `updateTaskNoteV3` 整体写入。

---

## 搜索未完成任务

**调用**：`teambition-mcp__searchProjectTasksV3`

```
projectId: 6959d07f4991ad9a71ca2afa
q: stageId = "69fed981a6333372a4b12b72"
pageSize: 100
```

返回后内存过滤 `isDone = false`。

---

## 读取任务备注

**调用**：`teambition-mcp__queryTaskV3`

```
shortIds: "789-296"
```

返回的 `result[0].note` 即为当前备注内容。

---

## 执行流程

```
1. 读取 scripts/hk_需求/data/analysis_context.json
2. 对每个会话：
   a. 完整读取客户消息，分析是否有实质需求
   b. 搜索 TB 未完成任务（按 stageId 拉，内存过滤 isDone）
   c. 按 customer_name 过滤已有任务
   d. 各 demand 逐一判断：
      - 同一件事 → queryTaskV3 读 note → 拼接 → updateTaskNoteV3
      - 疑似相关 → createTaskV3（备注标注疑似与哪个任务相关）
      - 新需求   → createTaskV3（按标准 note 格式）
3. 输出执行汇总（创建 X 个，追加 Y 个）
```
