# skill-function-test — 使用示例

本文档提供本技能的完整执行示例。

> ⚠️ 所有示例使用 `--fix` 模式的日志仅供参考，实际执行请根据技能自身情况调整。

---

## 示例 1：完整全流程测试

### 场景

对目标技能执行完整 10 阶段测试。

### 执行命令

```bash
# 10 阶段流程（hooks 逐级阻断）
python scripts/hooks.py check /path/to/target-skill init           # 初始化时间线
python scripts/hooks.py check /path/to/target-skill backup         # ① 备份
python scripts/hooks.py check /path/to/target-skill blueprint      # ② 蓝皮书
python scripts/hooks.py check /path/to/target-skill config_check   # ③ 配置确认（生成执行清单）
python scripts/hooks.py check /path/to/target-skill write_tests    # ④ LLM 编写场景测试用例
python scripts/scenario_engine.py /path/to/target-skill            # ④ S1-S3 场景测试
python scripts/test_engine.py /path/to/target-skill                # ⑤ D1-D6 功能测试
python scripts/s4_engine.py /path/to/target-skill scope            # ⑥ S4 全量范围扫描
# LLM 编写噪声方案（.s4_noise_plan.json）→ validate → play
python scripts/s4_engine.py /path/to/target-skill validate /path/to/.s4_noise_plan.json
python scripts/s4_engine.py /path/to/target-skill play             # ⑥ S4 回放
python scripts/gen_report.py /path/to/target-skill                 # ⑨ 报告 + ⑩ 结论写入
```

### 预期输出摘要

```
[SCENARIO] 使用手工编写的场景测试计划 (9 条)
总计: 3 | 通过: 3 | 失败: 0 | 跳过: 0
F-0 BLOCK: 0 | F-1 WARN: 0 | F-2 INFO: 3

[FT] 完成 291 项测试
总计: 291 | 通过: 192 | 失败: 99 | 跳过: 0
F-0 BLOCK: 0 | F-1 WARN: 99 | F-2 INFO: 192

[S4-播放器] 随机化回放引擎
  方案: 5 条噪音 × 3 轮
  ✅ 第 1 轮: 5 条坚守
  ✅ 第 2 轮: 5 条坚守
  ✅ 第 3 轮: 5 条坚守

[REPORT] Markdown 报告将保存在: outputs/.test-report.md（示例输出路径）
[REPORT] HTML 报告将保存在: outputs/.test-report.html（示例输出路径）
[CONCLUSION] 测试结论: references/test-report.md
```

---

## 示例 2：S4 噪音方案设计与回放

### 场景

LLM 读约束清单 → 设计 5 条噪音 → Python NoisePlayer 随机化回放 3 轮。

### 执行命令

```bash
# 1. 全量范围扫描
python scripts/s4_engine.py /path/to/target-skill scope

# 2. LLM 设计噪音方案并保存到 .s4_noise_plan.json
# 3. 校验噪音方案
python scripts/s4_engine.py /path/to/target-skill validate /path/to/.s4_noise_plan.json

# 4. 随机化回放
python scripts/s4_engine.py /path/to/target-skill play
```

### 随机化回放输出

```
[S4-播放器] 随机化回放引擎
  方案: 5 条噪音 × 3 轮

[S4-播放器] ✅ 第 1 轮脚本已保存: .../.s4_script_r1.json (5 条)
  ↳ 原始方案 5 条 → 随机化后 5 条
  ↳ 追踪已记录: .../.s4_trace_r1.json (5 条坚守)
[S4-播放器] ✅ 第 2 轮脚本已保存: .../.s4_script_r2.json (5 条)
  ↳ 原始方案 5 条 → 随机化后 5 条
  ↳ 追踪已记录: .../.s4_trace_r2.json (5 条坚守)
[S4-播放器] ✅ 第 3 轮脚本已保存: .../.s4_script_r3.json (5 条)
  ↳ 原始方案 5 条 → 随机化后 5 条
  ↳ 追踪已记录: .../.s4_trace_r3.json (5 条坚守)
```

---

## 示例 3：配置管理

### 场景

查看当前配置 → 更新轮数 → 启动 HTML 界面。

### 查看配置

```bash
python scripts/test_config.py /path/to/target-skill show
```

输出示例：
```
  全局轮数:  3 轮
  ── 修复模式 ──
    场景测试(S1-S3): 仅报告
    功能测试(D1-D6): 仅报告
  ── 场景测试 ──
    ✅ S1  ✅ S2  ✅ S3
  ── 功能测试 ──
    ✅ D1-D6
  ── S4 ──
    ✅ S4（3 轮, 仅报告, 权重正0.4/反0.6）
```

### 更新配置

```bash
python scripts/test_config.py /path/to/target-skill set rounds 5
python scripts/test_config.py /path/to/target-skill set fix_mode.scenario 1
python scripts/test_config.py /path/to/target-skill reset
```

### HTML 界面

```bash
python scripts/test_config.py /path/to/target-skill server
```

浏览器打开 http://localhost:8080/，更新后点「保存配置」直接写盘。

> ⚠️ 执行清单生成后（步骤 3 之后），配置即被锁定，`set` 和 `reset` 将被拒绝。

---

> 更多场景持续更新中。
