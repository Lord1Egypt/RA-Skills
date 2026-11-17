# params.json 规范文档

每个 Skill 可以有一个 `params.json` 文件，定义该 Skill 接受的参数 schema。

## 查找优先级

skill-to-http 按以下顺序查找 params.json：

| 优先级 | 路径 | 说明 |
|--------|------|------|
| 1 | `{skill_dir}/params.json` | Skill 目录自身，由 Skill 作者维护 |
| 2 | `{data_dir}/params/{skill_name}/params.json` | data_dir，运行时自动生成或手动管理 |
| 3 | `~/.skill-to-http/params-template/{skill_name}/params.json` | 全局模板目录 |
| 4 | 自动生成 | 用 LLM 读取 SKILL.md 自动提取，失败则用兜底 schema |

优先级高的覆盖优先级低的。一旦在某级找到有效文件，后续级别不再查询。

## 字段说明

### 顶层字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | `"object"` | 是 | 固定值，必须是 `"object"` |
| `properties` | `object` | 是 | 参数定义，key 为参数名，value 为参数 schema |
| `required` | `string[]` | 否 | 必填参数名列表，`"message"` 必须包含在内 |
| `additionalProperties` | `boolean` | 否 | 是否允许额外字段，推荐设为 `false` |

### properties 内每个参数的字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | `string` | 是 | 参数类型：`string` `number` `boolean` `array` `object` |
| `description` | `string` | 是 | 参数说明 |
| `default` | any | 否 | 默认值 |
| `enum` | `any[]` | 否 | 枚举值限制 |
| `minimum` | `number` | 否 | 最小值（number 类型） |
| `maximum` | `number` | 否 | 最大值（number 类型） |
| `items` | `object` | 否 | 数组元素 schema（array 类型） |

## 完整示例

### 示例 1：只有 message 参数的简单 Skill

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "任务描述，告诉 Skill 需要完成什么工作"
    }
  },
  "required": ["message"],
  "additionalProperties": false
}
```

### 示例 2：带多个业务参数的 Skill

假设一个"发送 Hi 消息"的 Skill：

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "要发送的消息内容"
    },
    "target": {
      "type": "string",
      "description": "目标用户或群组名称"
    },
    "channel": {
      "type": "string",
      "description": "消息渠道",
      "enum": ["hi", "discord", "webchat"],
      "default": "hi"
    },
    "priority": {
      "type": "string",
      "description": "消息优先级",
      "enum": ["low", "normal", "high"],
      "default": "normal"
    },
    "retry_count": {
      "type": "number",
      "description": "发送失败重试次数",
      "default": 3,
      "minimum": 0,
      "maximum": 10
    },
    "silent": {
      "type": "boolean",
      "description": "是否静默发送（不触发通知）",
      "default": false
    }
  },
  "required": ["message", "target"],
  "additionalProperties": false
}
```

## 兜底 schema

当所有查找链都失败且 LLM 自动生成也失败时，使用以下最小兜底 schema：

```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "任务描述，告诉 Skill 需要完成什么工作"
    }
  },
  "required": ["message"],
  "additionalProperties": false
}
```

## 注意事项

1. `"message"` 是所有 Skill 的通用参数，**必须**作为 property 存在且包含在 `required` 中
2. `params.json` 应尽量精确地描述 Skill 接受的参数，以便 Swagger UI 自动生成可用的请求体示例
3. 对于 Skill 作者：建议在 Skill 根目录放置 `params.json`（优先级 1），便于版本控制和分发
4. 对于运维人员：可在 `data_dir` 或模板目录覆盖自动生成的 schema（优先级 2、3）