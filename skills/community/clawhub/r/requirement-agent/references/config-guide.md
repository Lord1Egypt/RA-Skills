# 配置文件说明

## 概述

`config/rules.yaml` 控制 Requirement Agent 的行为，包括：

- 追问策略配置
- 自动执行规则
- 需要确认的规则

## 配置结构

### questioning（追问规则）

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| max_rounds | int | 5 | 最大追问轮数 |
| auto_skip_if_clear | bool | true | 需求明确时跳过追问 |
| trigger_keywords | string[] | 见下方 | 触发追问的关键词 |

默认触发关键词：
`大概`、`优化一下`、`类似`、`感觉`、`可能`、`差不多`、`改进`

### auto_execute（自动执行规则）

满足任一条件即自动执行，无需确认。

| 字段 | 类型 | 说明 |
|------|------|------|
| text_only | bool | 纯文本修改（注释、格式化） |
| single_file | bool | 单文件小改动 |
| safe_operations | string[] | 明确安全的操作关键词 |
| explicit_safe | bool | 用户明确说"直接改"时 |

### require_confirmation（确认规则）

满足任一条件即需要确认后再执行。

| 字段 | 类型 | 说明 |
|------|------|------|
| multi_file | bool | 多文件修改（2+ 文件） |
| delete | bool | 删除操作 |
| logic_change | bool | 逻辑变更 |
| dependency | bool | 添加依赖 |
| irreversible | bool | 不可逆操作 |
| migration | bool | 数据迁移 |
| keywords | string[] | 触发确认的关键词 |

## 修改建议

### 调整追问深度

如果觉得追问太多：

```yaml
questioning:
  max_rounds: 3    # 从 5 改为 3
```

### 放宽自动执行

如果希望更少确认：

```yaml
auto_execute:
  single_file: true      # 保持
  text_only: true         # 保持
  # 添加更多安全操作
  safe_operations:
    - "加注释"
    - "格式化"
    - "重命名"
    - "整理代码"
    - "添加 console.log"  # 新增
```

### 收紧确认规则

如果希望更谨慎：

```yaml
require_confirmation:
  multi_file: true
  delete: true
  logic_change: true
  dependency: true
  irreversible: true
  migration: true
  # 添加更多触发词
  keywords:
    - "删除"
    - "重写"
    - "替换"
    - "迁移"
    - "修改"              # 新增：所有修改都确认
    - "改动"
```

## 验证配置

修改配置后，可用以下方式验证 YAML 格式：

```bash
# 使用 python（需要 pyyaml）
python3 -c "import yaml; yaml.safe_load(open('config/rules.yaml'))"

# 或使用 yq 工具
yq eval '.' config/rules.yaml
```

无错误输出表示解析成功。
