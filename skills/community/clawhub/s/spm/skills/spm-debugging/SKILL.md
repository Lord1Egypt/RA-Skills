---
name: spm-debugging
version: 1.0.0
description: 调试规范 — Agent 最常见的错误是瞎试。本技能强制根因分析+单变量实验。SPM Phase 4 异常时自动引用。
---

# SPM Debugging — 调试规范

## 自动检测

SPM Phase 4 检测到测试失败/回归/Eval Delta 异常 → 自动引用本技能。也可独立使用。

## 独立使用

不走 SPM 也可以直接说："按 spm-debugging 规范调试这个错误。"

---

## Agent 调试 5 大反模式

| # | 反模式 | 症状 | 为什么坏 |
|---|--------|------|---------|
| 1 | **瞎试** | "我改成 X 试试...不行...再试试 Y..." | 不知道哪个改动修了 bug，可能引入新问题 |
| 2 | **改症状不改根因** | "这个 undefined error 我加个 `?? {}` 就行" | 补丁越叠越多，真正的问题始终在 |
| 3 | **同时改 3 处** | 改了 A、B、C 三个文件一起跑 | 不知道哪个生效了，也不知道谁引入了新 bug |
| 4 | **不写复现测试** | 直接看代码猜，不跑测试确认 | 修完无法证明修好了，回归也检测不到 |
| 5 | **跳过根因直接查 StackOverflow** | "这个报错我搜一下...copy/paste 解决方案" | 解决方案不是针对你的场景的，可能完全不适用 |

---

## 4 阶段调试法

SPM `systematic-debugging.md` 工作流 + 本技能具体执行规则：

### Phase 1: 错误捕获

```
1. 复制完整的堆栈跟踪（不要截断）
2. 标注：哪个文件、哪一行、什么错误类型
3. 确认：你能稳定复现这个错误吗？
```

```bash
# 先跑测试，确认它真的失败
npm test path/to/failing.test.ts 2>&1 | tee /tmp/debug.log
```

### Phase 2: 只改一样

```
✅ 单变量实验：一次只改一个东西
✅ 每次改动后跑测试确认
✅ 记录每次实验的结果

❌ 同时改 3 个文件
❌ "我觉得可能是 X 也可能是 Y，一起改了"
```

### Phase 3: 假设验证

```
1. 形成一个明确假设："我认为根本原因是因为 <X>"
2. 设计最小验证："修改 <Y> 应该消除/改变错误"
3. 执行 → 确认 → 记录
4. 假设错了？形成新假设。不堆叠修复。
```

### Phase 4: 修复 + 防止回归

```
1. 基于验证过的假设，写最小修复
2. 写复现测试 (RED) → 确认它在修复前失败
3. 应用修复 → 确认测试变 GREEN
4. 跑全量测试 → 无回归
5. Commit: fix(scope): root cause — what happened and why
```

---

## 常见调试命令

```bash
# ✅ 查看最近改动
git diff HEAD~1 --name-only
git log --oneline -5

# ✅ 二分法定位 (找到引入bug的commit)
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-sha>
# 在每个 step 跑测试 → git bisect good/bad
git bisect reset  # 结束后清理

# ✅ 隔离测试
npm test -- -t "test name pattern"  # 只跑匹配的测试

# ✅ 增加调试日志 (修完就删！)
console.log('DEBUG:', { variable, type: typeof variable })
```

---

## 死循环对策

如果修了 3 次还没好 → STOP。这是架构问题，不是 bug：

```
1. 停止修改代码
2. 重新读错误：是不是误解了错误含义？
3. 检查环境：Node 版本？依赖版本？环境变量？
4. 检查假设：你确定"正确的行为"真的是正确的吗？
5. 升级到 strong model 做根因分析
6. 如果还是不行 → 请求人工介入
```

**铁律：3 次修复失败 = 停止自主修复，不准继续试。**
