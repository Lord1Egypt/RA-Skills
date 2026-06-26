# Scope Rules

## scoped_state_keys 设计原则

每个节点必须显式声明它需要访问的状态键。**未声明的键默认不可访问**。

## 规则

### 1. 最小权限
```json
// ✅ 正确：只声明需要的键
"scoped_state_keys": ["employee_info", "onboarding_ticket_id"]

// ❌ 错误：声明了不需要的键
"scoped_state_keys": ["employee_info", "salary_data", "performance_review", "everything"]
```

### 2. 输入输出对应
- 节点的 `input_mapping` 引用的键，必须在某个上游节点的 `scoped_state_keys` 中声明过
- 节点的 `output_mapping` 声明的键，应该在其 `scoped_state_keys` 中

### 3. 敏感字段
- 薪资、身份证、密码等敏感字段不能出现在 `scoped_state_keys` 中
- 如需使用，必须通过调用方预先脱敏或投影

### 4. 全局键
- 如果引用不带 `.` 前缀的键（如 `employee_info` 而非 `N1.employee_info`），视为全局键
- 全局键会在 validation_report 中标记为 warning
- 建议：尽量使用带节点前缀的显式引用

## 命名约定

| 前缀 | 含义 | 示例 |
|------|------|------|
| `N1.xxx` | 节点 N1 的输出 | `N1.employee_info` |
| `input.xxx` | 外部输入 | `input.file_path` |
| `global.xxx` | 全局状态 | `global.tenant_id` |
