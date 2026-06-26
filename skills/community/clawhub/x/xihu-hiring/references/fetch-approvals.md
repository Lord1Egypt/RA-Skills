# 获取飞书审批数据（lark-cli 方式）

本文档描述如何用 `lark-cli` 从飞书审批系统获取西湖数智招聘数据并组装为 `build_excel.py` 所需的 JSON payload。

## Step 1: 计算时间窗口

飞书审批 API 要求 `start_time` 和 `end_time` 为毫秒时间戳，且跨度不能超过 120 天。

```bash
END_TIME=$(($(date +%s) * 1000))
START_TIME=$(($END_TIME - 120 * 24 * 3600 * 1000))
```

## Step 2: 列出实例

```bash
lark-cli api GET "/open-apis/approval/v4/instances" \
  --params "{\"approval_code\":\"57E726C3-EA5E-4422-A2F3-ACED3A75F8D2\",\"start_time\":\"$START_TIME\",\"end_time\":\"$END_TIME\",\"page_size\":\"100\"}" \
  --as bot --page-all --format json
```

返回结构：
```json
{
  "code": 0,
  "data": {
    "instance_code_list": ["CODE1", "CODE2", ...],
    "has_more": false
  }
}
```

`--page-all` 自动处理分页。提取 `instance_code_list`。

## Step 3: 获取每个实例详情

```bash
lark-cli approval instances get \
  --params '{"instance_code":"<CODE>","locale":"zh-CN"}' \
  --as bot --format json
```

每个实例返回：
- `serial_number` — 审批编号
- `status` — APPROVED / REJECTED / PENDING / CANCELED / RECALL / DELETED
- `start_time` / `end_time` — 毫秒时间戳
- `open_id` — 提交人
- `form` — JSON 字符串，包含表单字段
- `task_list` — 审批任务列表（每个节点的审批人、状态、时间）

## Step 4: 组装 payload

将每个实例转换为一行：

```python
row = {
    "serial": inst["serial_number"],
    "status": translate(inst["status"]),  # APPROVED→通过, REJECTED→拒绝, PENDING→待审批...
    "submit_time": format_time(inst["start_time"]),
    "end_time": format_time(inst["end_time"]),
    "name": form["姓名"],
    "position": form["申请职位"],
    "phone": form["手机号"],
    "email": form["邮箱"],
    "school": form["毕业院校"],
    "prior_jobs": form["曾经任职"],
    "cv": "(CV附件-需在飞书内查看)",  # 不保留原始URL
    "node_resume_screen": node_status("简历筛查") or node_status("简历筛选"),
    "node_r1": node_status("一面"),
    "node_r2": node_status("二面"),
    "node_r3": node_status("终面"),   # 终面 = 三面/第三轮
    "node_handle": node_status("办理"),
    "tasks": [...]  # 用于 Sheet 2 的明细
}
```

**节点状态优先级**（同一节点有多条 task 时）：REJECTED > PENDING > APPROVED > 其他

**状态翻译表**：
| 英文 | 中文 |
|------|------|
| APPROVED | 通过 |
| REJECTED | 拒绝 |
| PENDING | 待审批 |
| CANCELED | 撤销 |
| RECALL | 撤回 |
| DONE | 完结 |
| TRANSFERRED | 转交 |
| DELETED | 删除 |

最终 payload 格式：
```json
{"rows": [row1, row2, ...]}
```

按 `submit_time` 降序排列。写入 `/tmp/hiring_payload.json`。

## 注意事项

- `form` 字段是 JSON 字符串，需要 `json.loads` 解析
- `form` 中每个 widget 有 `name` 和 `value`，`value` 可能是字符串、数组或对象
- CV 链接包含高熵 token，不要在对话中展示完整 URL
- 节点名 "终面" 对应报表中的 "三面"
- "简历筛查" 和 "简历筛选" 是同一节点的不同命名版本
