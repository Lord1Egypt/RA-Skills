# Team Collab 角色配置

你可以自定义角色和每个角色使用的模型。

---

## 快速配置

在项目目录创建 `team-collab.json` 或者在对话中直接指定。

### 示例配置

```json
{
  "roles": {
    "product_manager": {
      "name": "产品经理",
      "model": "bailian/qwen-plus",
      "enabled": true
    },
    "developer": {
      "name": "程序员",
      "model": "bailian/glm-5",
      "enabled": true
    },
    "designer": {
      "name": "设计师",
      "model": "bailian/qwen3.5-plus",
      "enabled": true
    },
    "legal_advisor": {
      "name": "法律顾问",
      "model": "bailian/qwen-max",
      "enabled": false
    }
  }
}
```

---

## 对话中指定

### 自定义模型

```
"用团队协作模式，程序员用 qwen-max"
"设计师换成 glm-5"
```

### 添加自定义角色

```
"加一个财务顾问角色，用 qwen-max"
"添加翻译专家，模型用 deepseek-coder"
```

### 禁用角色

```
"不需要法律顾问"
"跳过艺术专家"
```

---

## 可用模型列表

| 模型 | 特点 | 适合角色 |
|------|------|----------|
| `bailian/glm-5` | 代码强、中文好 | 程序员、审查员 |
| `bailian/qwen-plus` | 综合能力强 | 产品经理、市场分析 |
| `bailian/qwen-max` | 推理强、质量高 | 法律顾问、审查员 |
| `bailian/qwen3.5-plus` | 创意、设计 | 设计师、艺术专家 |
| `deepseek-coder` | 代码专用 | 程序员、测试 |
| `bailian/qwen-qwq` | 深度思考 | 复杂分析 |

---

## 自定义角色模板

创建新角色：

```
角色ID: my_custom_role
角色名称: 数据分析师
推荐模型: bailian/qwen-plus
职责: 数据分析、报表生成、洞察提取
```

在对话中说：
```
"添加自定义角色：数据分析师，模型用 qwen-plus，负责数据分析"
```

---

## 配置文件位置

- **全局配置**: `~/.openclaw/team-collab.json`
- **项目配置**: `./team-collab.json`
- **默认配置**: `skills/team-collab/config/default.json`

项目配置优先于全局配置。

---

## 预设模式

### 最小团队（2人）
```
产品经理 + 程序员
```

### 核心团队（5人）
```
产品经理 + 程序员 + 设计师 + 测试 + 审查员
```

### 全员团队（8人）
```
核心团队 + 法律顾问 + 艺术专家 + 市场分析
```

### 商业团队（6人）
```
产品经理 + 市场分析 + 程序员 + 设计师 + 法律顾问 + 审查员
```

### 创业团队（7人）
```
产品经理 + 市场分析 + 程序员 + 设计师 + 测试 + 法律顾问 + 审查员
```