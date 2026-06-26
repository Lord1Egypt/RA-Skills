# SEVO P0 测试修复 - 产品需求

OpenClaw（主会话） / 2026-05-24

## 用户人群
SEVO 维护者，在审计指出 P0-3/4/5 修复后留下 4 个 broken test 时，需要快速修复测试以解锁发版。

## 痛点
P0-3/4/5 包元修复审计 CONDITIONAL PASS，4 个测试失败卡住 npm test 1270/1270 全绿门禁，发版被卡。

## 原始需求
修复 4 个 broken test 让 npm test 全绿。详细诊断和修复方案见 `/root/.openclaw/workspace/reports/sevo-p0-package-meta-audit-2026-05-24.md` §6。

## 用户体验流
1. 维护者跑测试看到 4 failed
2. 读审计报告 §6 拿到根因和修复方案
3. 编码 Agent 按方案修测试代码（不碰生产代码）
4. 重跑测试 1270/1270 全绿
5. 解锁发版

## 功能需求

### FR-1: 修复 cli-commands 测试参数名断言
将 `src/cli/__tests__/cli-commands.test.ts` 中 `advance command requires instance-id and has --dry-run` 用例的断言对齐 `cmd-advance.ts` 实际参数名 `pipeline-id`。

**AC-1.1**: 测试断言使用 `pipeline-id` 而非 `instance-id`，与生产代码 `command('advance <pipeline-id>')` 一致。
**AC-1.2**: 该用例独立通过。

### FR-2: 修复 clean-install-verification-stage 测试以适配 install step
将 `src/stages/__tests__/clean-install-verification-stage.test.ts` 中三个用例（passes / fails / timeout）的测试桩同步 P0-4 引入的 `installPackageIntoCleanRoot` 行为。

**AC-2.1 (passes 用例)**: `expect(calls).toHaveLength(4)`（不再是 3），并断言 `calls[0]?.args` 含 `npm install`。
**AC-2.2 (fails 用例)**: 测试桩匹配条件改为 `args.some(a => a.includes('exit 1'))`（适配 L2 包了 PATH= HOME= 的整体字符串）。
**AC-2.3 (timeout 用例)**: 测试桩首次调用（install）正常返回 `{ stdout: 'ok', stderr: '' }`，第二次调用（L1）才抛 timeout 错。

### FR-3: 全绿门禁
**AC-3.1**: 测试输出 `Test Files X passed (X) / Tests 1270 passed (1270)`。
**AC-3.2**: 不允许 `it.skip` 跳过。
**AC-3.3**: 不修改生产代码（`src/stages/clean-install-verification-stage.ts` 和 `src/cli/cmd-advance.ts` 内容不变）。
