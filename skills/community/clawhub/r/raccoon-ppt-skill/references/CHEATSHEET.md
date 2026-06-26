# PPT OpenAPI 速查

## 认证

```text
Authorization: Bearer $RACCOON_API_TOKEN
```

基础地址：

```text
$RACCOON_API_HOST/api/open/office/v2
```

## 核心接口

| 功能 | 方法 | 路径 |
| --- | --- | --- |
| 创建 PPT 任务 | POST | `/ppt_jobs` |
| 查询任务状态 | GET | `/ppt_jobs/{job_id}` |
| 回复补充问题 | POST | `/ppt_jobs/{job_id}/reply` |

## 最小请求体

创建任务：

```json
{
  "prompt": "帮我生成一份介绍 Transformer 发展历程的培训 PPT",
  "role": "研究人员",
  "scene": "培训教学",
  "audience": "大众群体"
}
```

回复追问：

```json
{
  "answer": "重点介绍自注意力机制、BERT 和 GPT 的演进关系"
}
```

## 对外状态

| 状态 | 含义 | skill 动作 |
| --- | --- | --- |
| `queued` | 已创建，等待执行 | 继续轮询 |
| `running` | 后台处理中 | 继续轮询 |
| `waiting_user_input` | 需要用户补充信息 | 停止轮询并提问 |
| `succeeded` | 已完成 | 返回 `download_url` |
| `failed` | 已失败 | 展示 `error_message` |
| `canceled` | 已取消 | 通知用户重试 |

## download_url 使用说明

当任务状态为 `succeeded` 时，响应中的 `download_url` 是预签名的 S3 下载地址。

**重要提示：**
- `download_url` 是标准 JSON 字符串，可能包含 `\u0026` 等转义字符
- Python 的 `json.loads()` 会自动将 `\u0026` 转换为 `&`
- 解析后的 `download_url` 可直接用于下载，无需手动替换或编码
- 直接使用：`requests.get(download_url)` 或在浏览器中打开

**错误做法：**
- ❌ 手动将 `\u0026` 替换为 `&`
- ❌ 对整个 URL 再次进行 URL 编码
- ❌ 修改 URL 中的任何参数

## 当前推荐枚举

`role`：

- `企业管理者（CEO/总监/经理）`
- `学生`
- `研究人员`
- `销售`
- `市场`
- `营销`
- `产品经理`
- `项目经理`
- `教师`
- `培训师`
- `财务`
- `会计`
- `行政`
- `人力资源`

`scene`：

- `工作汇报`
- `市场调研`
- `培训教学`
- `学术演讲`
- `商业提案`
- `活动策划`

`audience`：

- `公司内部（上级/同事/下属）`
- `外部客户`
- `投资人`
- `学生`
- `大众群体`
- `专业人士`

Skill 侧使用建议：

- 优先把用户语义映射到上述稳定分类。
- 若没有合适匹配项，继续通过前置对话收敛到最接近的稳定分类。
- 如需保留额外语义，可把补充说明吸收到 `prompt`，但不要发明新的分类值。

## 错误处理口径

- 参数类错误：提示用户补全或改写需求。
- 业务类错误：如 `600020` 未完成任务数达到上限，提示稍后再试；如 `600021` 当前状态不允许 `reply`，提示先查看最新状态。
- 运行类错误：向用户展示 `error_message`。
- `waiting_user_input`：不是错误，是正常业务态。
