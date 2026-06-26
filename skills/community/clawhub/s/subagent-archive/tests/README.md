# Tests / 跨平台测试

This directory contains cross-platform test scripts for `archive-sessions.ps1`.

## Test Scripts

### `test-syntax.ps1`

PowerShell 5.1 语法解析测试。验证脚本无语法错误。

**用法**：
```powershell
powershell -ExecutionPolicy Bypass -File test-syntax.ps1
```

**预期输出**：
```
PS 5.1 语法解析: 0 错误
```

### `test-pwsh7-syntax.ps1`

PowerShell 7+ 语法解析测试。验证脚本在跨平台 pwsh 下也无语法错误。

**用法**：
```powershell
pwsh -ExecutionPolicy Bypass -File test-pwsh7-syntax.ps1
```

**预期输出**：
```
pwsh 7 语法解析: 0 错误
```

### `test-dry-run.ps1`

完整的 dry-run 测试。用户需要：
1. 准备一个测试 agent（有 sessions.json 即可）
2. 准备一个测试 workspace（有 MEMORY.md 即可）
3. 跑这个脚本

**用法**：
```powershell
$env:TEST_AGENT = "myagent"
$env:TEST_WORKSPACE = "/path/to/workspace-myworkspace"
pwsh -ExecutionPolicy Bypass -File test-dry-run.ps1
```

**预期输出**：
- 脚本以 exit code 0 结束
- 看到 `[OK] 日志已追加: ...`
- 看到 `v3.2 执行汇总`

### `test-multi-workspace-error.ps1`

测试多 workspace 错误处理。需要：
- 至少 2 个 workspace-* 目录带 `MEMORY.md`

**用法**：
```powershell
pwsh -ExecutionPolicy Bypass -File test-multi-workspace-error.ps1
```

**预期输出**：
```
[ERR] 检测到多个 workspace:
[ERR]   - ...
[ERR]   - ...
[ERR] 请用 -WorkspaceDir <path> 显式指定其中一个。
```

Exit code: 2

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Test PowerShell 5.1 syntax
  shell: pwsh
  run: ./tests/test-syntax.ps1

- name: Test pwsh 7 syntax
  shell: pwsh
  run: ./tests/test-pwsh7-syntax.ps1
```

## Test Status

| Test | Win PS 5.1 | Win pwsh 7 | macOS pwsh 7 | Linux pwsh 7 |
|------|-----------|-----------|--------------|--------------|
| `test-syntax.ps1` | ✅ Tested | ⏳ TODO | ⏳ TODO | ⏳ TODO |
| `test-pwsh7-syntax.ps1` | N/A | ⏳ TODO | ⏳ TODO | ⏳ TODO |
| `test-dry-run.ps1` | ✅ Tested | ⏳ TODO | ⏳ TODO | ⏳ TODO |
| `test-multi-workspace-error.ps1` | ✅ Tested | ⏳ TODO | ⏳ TODO | ⏳ TODO |

> 当前开发环境只有 Windows + PowerShell 5.1。pwsh 7 测试需要社区贡献。
