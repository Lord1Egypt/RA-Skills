# Release Hygiene

用于清理旧包、判断何时生成 zip、避免把滞后包当作当前交付。

## 原则

- 源码继续优化期间，不保留过期 `weekend-pick-one-*.zip` 作为可安装版本。
- 用户明确要求打包时再运行 `scripts/package_release.py`。
- `scripts/run_forward_tests.py` 只算静态夹具检查，不能单独证明真实 Agent 行为。
- 打包前必须准备独立 Agent 输出目录和 72 小时内的真实浏览器证据文件，再运行：

```bash
python3 scripts/run_release_gates.py \
  --agent-output-dir /path/to/agent-outputs \
  --live-evidence /path/to/live-browser-evidence.json
```
- 若源码已变更而旧 zip 仍在 `dist`，先移动到 `/private/tmp/...` 备份目录。
- `latest.zip` 只允许指向刚刚验证过的源码状态。

## 清理范围

只清理本 Skill 相关文件：

- `dist/weekend-pick-one-*.zip`
- `dist/weekend-pick-one-*.manifest.json`

不得清理其他 Skill 的包，除非用户明确点名。

## 报告格式

```markdown
清理：
- 移走旧 weekend 包：N 个
- 备份位置：...

验证：
- 静态夹具：通过数 / 总数
- 结构校验：通过
- 独立 Agent：通过数 / 总数
- 真实浏览器：来源类型 / 核验时间

状态：
- 未打包 / 已打包
```
