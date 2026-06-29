# 输出报告模板

> 本文件包含 universal-file-ops 的固定报告模板，动态加载。


每次流水线执行完毕，必须输出如下结构的报告。**这是固定模板，不允许增减字段或改变键名。** 只需把 `{{占位符}}` 替换为实际数据，所有字段必须存在（包括空数组和 skipped）。

### 模板 A — 仅执行了环境准备（未进入 B 或 C）

```json
{
  "report": "universal_file_ops_report",
  "phase": "A",
  "target": "{{无文件操作}}",
  "hook_trace": ["H-A01", "H-A02", "H-A03"],
  "environment": {
    "python_detected": "{{3.11.8 / 3.13.12 / not_found}}",
    "venv_created": {{true / false}},
    "packages_installed": ["{{pkg1}}", "{{pkg2}}"],
    "route": "{{B / C / unknown}}"
  },
  "steps": [
    {
      "step_id": "H-A01",
      "step_name": "detect_python",
      "status": "{{success / failed}}",
      "issues": []
    },
    {
      "step_id": "H-A02",
      "step_name": "setup_venv",
      "status": "{{success / failed}}",
      "issues": []
    },
    {
      "step_id": "H-A03",
      "step_name": "install_deps",
      "status": "{{success / failed}}",
      "issues": []
    }
  ],
  "overall": {
    "status": "{{failed / warning / passed}}",
    "error_count": 0,
    "warning_count": 0,
    "total_time_seconds": {{数字}}
  }
}
```

### 模板 B — 工具箱（文件 CRUD）

```json
{
  "report": "universal_file_ops_report",
  "phase": "B",
  "target": "{{目标文件绝对路径}}",
  "hook_trace": ["H-A01", "H-A02", "H-A03", "H-A11",
                  "H-B01", "H-B02", "H-B03", "H-B04"],
  "operation": "{{read / create / update / delete / copy / move / rename}}",
  "steps": [
    {
      "step_id": "H-A01",
      "step_name": "detect_python",
      "status": "{{success / failed}}",
      "issues": []
    },
    {
      "step_id": "H-A02",
      "step_name": "setup_venv",
      "status": "{{success / skipped}}",
      "issues": []
    },
    {
      "step_id": "H-A03",
      "step_name": "install_deps",
      "status": "{{success / skipped}}",
      "issues": []
    },
    {
      "step_id": "H-A11",
      "step_name": "semantic_route",
      "status": "success",
      "route": "B"
    },
    {
      "step_id": "H-B01",
      "step_name": "toolbox_read",
      "status": "{{success / failed}}",
      "size_bytes": {{数字}},
      "issues": []
    },
    {
      "step_id": "H-B02",
      "step_name": "toolbox_process",
      "status": "{{success / failed}}",
      "issues": []
    },
    {
      "step_id": "H-B03",
      "step_name": "toolbox_write",
      "status": "{{success / failed}}",
      "write_mode": "{{atomic_write}}",
      "backup_rollback_id": "{{rollback_id / null}}",
      "issues": []
    },
    {
      "step_id": "H-B04",
      "step_name": "toolbox_verify",
      "status": "{{success / failed}}",
      "verify_result": "{{内容一致 / 内容不一致}}",
      "issues": []
    }
  ],
  "overall": {
    "status": "{{passed / warning / failed}}",
    "error_count": 0,
    "warning_count": 0,
    "total_time_seconds": {{数字}}
  }
}
```

### 模板 C — 脚本流水线（创建/修改 Python 脚本）

```json
{
  "report": "universal_file_ops_report",
  "phase": "C",
  "target": "{{脚本文件绝对路径}}",
  "hook_trace": ["H-A01", "H-A02", "H-A03", "H-A11",
                  "H-C01", "H-C02", "H-C03", "H-C04",
                  "H-C05", "H-C06", "H-C07", "H-C08",
                  "H-C09", "H-C10"],
  "requirement_table": [
    {
      "id": "R-001",
      "function": "{{函数签名}}",
      "input": "{{输入示例}}",
      "expected": "{{预期输出}}",
      "status": "{{pending / implemented / passed / failed}}"
    }
  ],
  "steps": [
    {
      "step_id": "H-A01",
      "step_name": "detect_python",
      "status": "{{success / failed}}",
      "issues": []
    },
    {
      "step_id": "H-A02",
      "step_name": "setup_venv",
      "status": "{{success / skipped}}",
      "issues": []
    },
    {
      "step_id": "H-A03",
      "step_name": "install_deps",
      "status": "{{success / skipped}}",
      "issues": []
    },
    {
      "step_id": "H-A11",
      "step_name": "semantic_route",
      "status": "success",
      "route": "C"
    },
    {
      "step_id": "H-C01",
      "step_name": "preload_standards",
      "status": "{{loaded / failed}}",
      "reference": "references/py_standards.md",
      "issues": []
    },
    {
      "step_id": "H-C02",
      "step_name": "create_req_table",
      "status": "{{success / failed}}",
      "req_count": {{数字}},
      "issues": []
    },
    {
      "step_id": "H-C03",
      "step_name": "generate_code",
      "status": "{{success / failed}}",
      "issues": []
    },
    {
      "step_id": "H-C04",
      "step_name": "normalize",
      "status": "{{success / failed}}",
      "fix_count": {{数字}},
      "issues": []
    },
    {
      "step_id": "H-C05",
      "step_name": "review",
      "status": "{{success / warning / failed}}",
      "issues": [
        {
          "type": "{{syntax / missing-docstring / long-func / unused-import / naming / oo-suggest}}",
          "line": {{数字}},
          "severity": "{{error / warning / info}}",
          "message": "{{UFO-XXXX 格式的通俗中文描述}}"
        }
      ]
    },
    {
      "step_id": "H-C06",
      "step_name": "oo_ify",
      "status": "{{success / skipped / failed}}",
      "skip_reason": "{{file under 600 lines / temporary script / not applicable}}",
      "issues": []
    },
    {
      "step_id": "H-C07",
      "step_name": "gen_test",
      "status": "{{success / failed}}",
      "test_file": "{{测试文件绝对路径 / null}}",
      "test_count": {{数字}},
      "issues": []
    },
    {
      "step_id": "H-C08",
      "step_name": "sandbox_test",
      "status": "{{passed / failed}}",
      "tests_run": {{数字}},
      "passed_count": {{数字}},
      "failed_count": {{数字}},
      "error_count": {{数字}},
      "duration_seconds": {{数字}},
      "passed_tests": ["{{test_name_1}}"],
      "failed_tests": ["{{test_name_2}}"],
      "issues": []
    },
    {
      "step_id": "H-C09",
      "step_name": "fix_loop",
      "status": "{{passed / failed / skipped}}",
      "total_iterations": {{数字}},
      "issues": []
    },
    {
      "step_id": "H-C10",
      "step_name": "output_report",
      "status": "success",
      "issues": []
    }
  ],
  "fix_iterations": [
    {
      "iteration": 1,
      "status": "{{passed / failed}}",
      "hooks_executed": ["H-C09.1", "H-C09.2", "H-C09.3", "H-C09.4"],
      "analyzed_failure": "{{失败原因分析}}",
      "what_was_fixed": "{{具体修改了什么}}",
      "fix_detail": "{{text_crud.py update 修改了哪个文件的哪部分}}",
      "sandbox_result": {
        "passed": {{数字}},
        "failed": {{数字}},
        "errors": 0
      }
    }
  ],
  "overall": {
    "status": "{{passed / warning / failed}}",
    "error_count": {{数字}},
    "warning_count": {{数字}},
    "info_count": {{数字}},
    "fix_iterations": {{数字}},
    "total_time_seconds": {{数字}}
  }
}
```

### 字段填写规则

| 规则 | 说明 |
|------|------|
| **`status` 取值** | 仅允许：`success` / `warning` / `failed` / `skipped` / `passed` / `loaded` |
| **`issues` 数组** | 每个步骤必须存在，无问题时为 `[]`，不允许省略 |
| **`hook_trace`** | 实际执行的钩子列表，用来核对是否有跳过 |
| **`overall.status`** | `failed`（任意 `error` 或未通过的 sandbox）→ `warning`（仅有 `warning`）→ `passed`（全通过） |
| **`error_count`** | `issues` 中 `severity: "error"` 的数量 |
| **`warning_count`** | `issues` 中 `severity: "warning"` 的数量 |
| **`info_count`** | `issues` 中 `severity: "info"` 的数量 |
| **`fix_iterations`** | 无修复循环时写空数组 `[]`，不允许省略 |
| **`requirement_table`** | 无需求表时写空数组 `[]`，不允许省略 |
| **`issues[].message`** | **禁止直接暴露 Python 异常栈**，必须用 UFO-XXXX 格式 + 通俗中文描述 |
| **`total_time_seconds`** | 整个流水线的墙钟耗时，取整到小数点后 2 位 |

