# 流程钩子系统 — 使用说明

## 双档策略

| 档位 | 适用步骤 | 行为 |
|------|---------|------|
| **自动补齐** | init / backup / blueprint | 产物缺失时 Python 自动执行，LLM 不需要管 |
| **阻断指引** | config_check / write_tests / scenario / function_test / s4 / fix / bump / gen_report / write_conclusion | 前置缺失时 exit(1)，明确指引 LLM |

## 执行清单校验

config_check 步骤生成 `.execution-checklist.json`，后续每个步骤完成后校验清单：

| 校验点 | 步骤 | 校验内容 |
|--------|------|---------|
| **config_check** | 生成清单时 | 检查 flow-state 是否有活动会话，有则拒绝生成 |
| **write_tests** | 标记 done 时 | S1/S2/S3 各维度用例数 ≥1 |
| **scenario** | 标记 done 时 | timeline 中 scenario phase 的执行次数 ≥ 期望轮次 |
| **function_test** | 标记 done 时 | timeline 中 function_test phase 的执行次数 ≥ 期望轮次 |
| **s4** | 标记 done 时 | 噪声方案 ≥3 条 + trace 文件数 ≥ s4 期望轮次 |
| **gen_report** | 执行前 | 全部前置清单项均为 PASS 才放行 |
| **write_conclusion** | 执行前 | test-report.md 文件存在 |

## 配置锁定

执行清单生成时记下配置文件的 SHA256 哈希。后续每步校验都会比对哈希是否一致。配置被更新过则阻断，提示"配置已被篡改"。

## 查看流程状态

```
python scripts/hooks.py status <skill-dir>
```

## 可用步骤

```
init | backup | blueprint | config_check | write_tests | scenario |
function_test | s4 | fix | bump | gen_report | write_conclusion
```
