---
name: validation-rule-management
description: 管理校验规则、规则组和校验场景的全流程操作。支持通过统一 CLI 工具快速执行 API 调用，自动处理参数解析、配置加载和错误提示。使用当用户需要进行校验规则管理、规则组维护、校验场景配置、启停操作或相关查询时，即使用户只说"帮我创建一条规则"或"查一下场景列表"也应触发。
---

# 校验规则管理

## 核心概念

```
校验场景 (ValidateScene)
  └─ 1:N 校验规则组 (ValidateRuleGroup)
           └─ 1:N 校验规则 (ValidateRule)
```

**状态**：`draft`（草稿）/ `enabled`（启用）/ `disabled`（禁用）

---

## 初始化（首次使用必做）

在使用任何命令前，**先检查 CLI 是否就绪**：

```bash
npx vr help 2>/dev/null || (cd <skill目录> && npm install)
```

如果 `npx vr help` 无输出或报错，说明还未初始化，执行：
```bash
cd /path/to/validation-rule-management
npm install
```

完成后即可在任意目录通过 `npx --prefix /path/to/validation-rule-management vr <action>` 调用，或直接在 skill 目录下用 `npx vr <action>`。

---

## 配置

**方式 1 — 环境变量**（推荐，适合脚本/CI）
```bash
export VALIDATE_BASE_URL=http://global-masterdata-http.default.yf-bw-test-2.test.51baiwang.com
export VALIDATE_TOKEN=your-token-here
```

**方式 2 — config.json**（放在项目根目录或 skill 目录）
```json
{
  "baseUrl": "http://global-masterdata-http.default.yf-bw-test-2.test.51baiwang.com",
  "token": "your-token-here"
}
```

---

## 命令速查

> 所有命令统一格式：`npx vr <action> [--key value ...]`
> 值含空格时 shell 自动处理，含 `=` 等特殊字符时用 `--json '{...}'`

### 规则组

```bash
npx vr create-rule-group  --groupName "基础信息校验组" --orderNum 1 [--description "描述"]
npx vr query-rule-groups  [--groupName "关键字"] [--pageNum 1] [--pageSize 10]
npx vr update-rule-group  --id 1 --groupName "新名称" --orderNum 2
npx vr delete-rule-group  --id 1
```

### 规则

```bash
npx vr create-rule  --groupId 1 --objectId Invoice --countryCode CN \
                    --ruleCode CN-SELLER-001 --ruleName "卖方名称必填" \
                    --ruleType required [--fieldKey sellerName] [--errorMessage "{field}不能为空"]

npx vr query-rules  [--groupId 1] [--status enabled] [--countryCode CN] [--pageSize 20]
npx vr enable-rule  --id 42 --status enabled|disabled
npx vr delete-rule  --id 42
```

### 场景

```bash
npx vr create-scene  --sceneCode CN_VAT_SPECIAL --sceneName "中国增值税专票场景" \
                     [--errorStrategy stop_on_error|continue_all]

npx vr query-scenes  [--sceneCode CN_VAT] [--status enabled] [--pageSize 10]
npx vr enable-scene  --id 10 --status enabled|disabled
npx vr delete-scene  --id 10
```

---

## 目录结构

```
validation-rule-management/
├── SKILL.md
├── package.json              # 定义 bin: { "vr": "./cli.js" }
├── cli.js                    # 入口：解析 action → 路由到对应命令模块
├── commands/                 # 按业务域划分的命令模块
│   ├── scenes.js             #   场景操作
│   ├── rule-groups.js        #   规则组操作
│   └── rules.js              #   规则操作
├── lib/                      # 基础设施
│   ├── api-client.js         #   HTTP 客户端 + 配置加载
│   ├── arg-parser.js         #   命令行参数解析
│   └── utils.js              #   公共工具函数
└── references/               # 参考文档（按需读取）
    ├── data-model.md         #   完整 DTO 定义 + API 端点汇总
    └── examples.md           #   典型使用示例
```

查阅字段定义或 API 路径时，读取 `references/data-model.md`。

---

## 常见问题

| 错误信息 | 原因 | 解决 |
|----------|------|------|
| `npx vr` 无响应 | 未执行 `npm install` | 在 skill 目录执行 `npm install` |
| 未找到配置 | 没有环境变量或 config.json | 设置环境变量或创建配置文件 |
| 缺少必填参数 | 参数不完整 | 运行 `npx vr help` 查看必填项 |
| 业务错误 | token 失效或权限不足 | 刷新 token，确认 appId 正确 |
