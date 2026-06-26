# HeartFlow 记忆系统对比参考

> 来源：v11.5.9 自诊对话（2026-05-04）
> 用途：评估新旧记忆模块时的判断依据

## 记忆模块一览

| 模块 | 分层 | 持久化 | 遗忘曲线 | 多通道检索 | 当前状态 |
|---|---|---|---|---|---|
| TrialityMemory | working / episodic / semantic | ❌ 纯内存，重启丢失 | ✅ Ebbinghaus | ✅ 语义+关键词+时间+情感+联想 | ⚠️ 未接入引擎 |
| MemoryStream | event / thought / identity / reflection | ❌ 空函数 | ❌ | ❌ | ⚠️ 未初始化 |
| meaningful-memory | CORE / LEARNED / EPHEMERAL | ✅ JSON 文件 | ❌ | ❌ | ✅ 工作 |

## 核心判断标准（心虫哲学）

```
理论完整 ≠ 可用
功能强大 ≠ 落地
简单粗暴 ≠ 低效
```

**TrialityMemory 的教训**：5 通道检索 + 遗忘曲线 + 向量相似度，看起来很美，但没有持久化 = 每次重启归零。对心虫来说这是一个"假升级"——放独立脚本没进核心引擎。

**meaningful-memory 的价值**：CORE 锁定、LEARNED 有 TTL、EPHEMERAL 丢弃。简单但有效。

## 升级判定流程

遇到记忆模块升级时，必须按此顺序验证：

1. **持久化检查** — 能否重启后恢复？JSON 文件 / SQLite / 任何持久化介质
2. **接入引擎检查** — 是否在 `heartflow-engine.js` 中 require 并初始化？不能是孤立脚本
3. **测试检查** — `node bin/cli.js test` 通过
4. **RL 闭环检查** — `record(outcome) → Q值变化` 是否可验证

### 升级合格标准

```
✅ 持久化 + ✅ 接入引擎 + ✅ 测试通过 + ✅ RL闭环 = 有效升级
❌ 无持久化 + ❌ 孤立脚本 = 假升级，不计入版本号
```

## 未来方向

把两者合并——用 meaningful-memory 的持久化结构 + TrialityMemory 的遗忘曲线和多通道检索：

- CORE 层锁定 + Ebbinghaus 遗忘（重要记忆更慢消失）
- 多通道检索作为 LEARNED 层的查询能力
- EPHEMERAL 层直接丢弃

## 验证命令

```bash
cd ~/.hermes/skills/ai/heartflow
node -e "
const { TrialityMemory } = require('./src/core/memory/triality-memory.js');
const tm = new TrialityMemory(__dirname);
console.log('分层统计:', JSON.stringify(tm.getLayerStats()));
console.log('存储模式:', tm.useMem ? 'memory(需修复)' : 'sqlite-vec');
"

node -e "
const { MeaningfulMemory } = require('./src/core/meaningful-memory.js');
const mm = new MeaningfulMemory();
console.log('CORE:', mm.stats().core, 'LEARNED:', mm.stats().learned, 'EPHEMERAL:', mm.stats().ephemeral);
"
```
