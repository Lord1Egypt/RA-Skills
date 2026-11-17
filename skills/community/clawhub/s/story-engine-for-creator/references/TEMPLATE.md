# STORY-ENGINE 通用模板

本目录是故事引擎的**通用模板形态**：引擎本体只保留语言无关逻辑，语言相关的词表、正则、阈值全部外置到 `adapters/`。客户交付时按模板复制，只改适配层与词表档案，不改引擎。

适用：长篇虚构文本的一致性审计（因果链、人物、时空、伏笔、文风）。

---

## 1. 目录

| 路径 | 作用 | 定制时是否改动 |
|---|---|---|
| `Story Engine for Creator.py` | 引擎本体：五步因果算子、四类呈现审计、伏笔台账、哈希链、责任闭环 | **不改** |
| `adapters/zh.py` | 中文参考适配器：45 个常量块 + 6 个方法 | 换语言时新建 `adapters/<lang>.py` |
| `adapters/spec.md` | 适配器协议（六方法契约、常量包规则、部署约束） | 读，不改 |
| `extraction/rule_extractor.py` | 规则抽取器：章 → 事件节点（角色/地点/时间/状态），词表驱动 | **不改** |
| `extraction/schema.py` | `EventNode` 等数据结构 | 不改 |
| `extraction/lexicons/example.json` | 词表档案骨架 | 复制为新档案并替换内容 |
| `logic_validators.py` | 事件级逻辑校验：时空矛盾、生死状态矛盾、时间线回退、伏笔断裂 | 不改 |
| `branch_simulator.py` | 剧情多分支推演 + 审计形状校验 | 不改 |
| `branch_variants.example.json` | 分支推演配置示例 | 按项目改 |

部署约束：引擎文件必须与 `adapters/` 同级。单独复制引擎文件到别处会直接 `ImportError`，这是设计选择——避免两套适配行为并存。

---

## 2. 最小调用

引擎文件名含空格，不能用普通 `import`，用 `importlib`：

```python
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("story_engine", ROOT / "Story Engine for Creator.py")
eng = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eng)

state = eng.GlobalState()
engine = eng.UltimateCausalNovelEngine("书名", state)

report = engine.audit_text(
    text=Path("chapter01.txt").read_text(encoding="utf-8"),
    include_causal=True,      # 关掉可省一次五步算子，约省 30%
    diff_only=False,          # True = 增量审计，只查本次文本，不重算全局态
)
print(report["all_passed"], report["audit_hash"])
print(report["logical"], report["presentation"])
```

传角色档案可显著降低误报（别称密集文本尤其需要）：

```python
characters = {
    "规范名": {
        "aliases": ["别称1", "别称2"],
        "knowledge": ["已知信息"],
        "forbidden_knowledge": ["不该知道的事"],
        "register_hints": ["语域特征"],
    }
}
report = engine.audit_text(text=txt, characters=characters, include_causal=True)
```

**逐章调用，不要整本一次性传入。** 全量语料实测（四大名著 461 章、306 万字、Python 3.13）：整段一次性 41.0s，逐章流式 12.4s，差 3.3 倍，且整段方式的单位成本随规模上升（1 章 183k 字/秒 → 461 章 74k 字/秒）。

---

## 3. 定制三层

### 3.1 语言适配器（换语种）

```bash
cp adapters/zh.py adapters/<lang>.py
```

1. 替换常量（词表、正则、阈值、风格族预设）。
2. 实现六方法：`split_sentences` / `tokenize` / `extract_names` / `era_forbidden` / `style_features` / `length_unit`。
3. 校准 `_THRESHOLDS`——**不可直接沿用中文值**。
4. 改 `_ADAPTER_LANG`，或调用处显式传入。
5. 提供该语言回归基线：≥20 个样本，含古今、题材对比。

细节见 `adapters/spec.md`。已知边界：当前只有中文实现，英文/日文适配器**无语料、无验收**；协议就绪不等于能力就绪。

### 3.2 词表档案（换作品/客户）

```bash
cp extraction/lexicons/example.json extraction/lexicons/<client>.json
```

改 `characters`（必填，规范名 → 别称列表）、`places`、`time_markers`、`death_markers`、`legal_context_markers`，然后：

```python
from extraction import rule_extractor as rx
lex = rx.load_lexicon("client")
nodes = rx.extract_corpus("./corpus/client", lex=lex)
report = logic_validators.run_all(eng, nodes)
```

`characters` 为空会直接报错，不静默降级——这是刻意设计：宁可失败，也不让启发式兜底产出伪角色名。

### 3.3 阈值校准（换题材）

客户语料跑一遍，统计各审计项的命中分布，再调整适配器里的阈值。验收标准：校准前后**确定性字段零变化**（排除 `audit_hash` / `audit_prev_hash`），而不是对比哈希——哈希载荷含 uuid 派生字段，同一文本重复审计会得到不同值（`adapters/spec.md` §6.4 已记录该缺陷）。

---

## 4. 交付验收清单

| 项 | 判据 |
|---|---|
| 全量审计时长 | 按章流式跑完客户全书，记录总时长与每章 p95 |
| 最坏输入 | 100 万字无标点单行 ≤ 20s；5 万行重复文本 ≤ 10s（Python 3.13 实测基线） |
| 畸形输入 | 空串 / 纯空白 / emoji 与控制字符 / 5 万级嵌套引号 均不抛异常 |
| 确定性 | 同一文本串行、多线程、多进程审计，`audit_hash` 必须只有 1 个值 |
| 定制回归 | 校准前后确定性字段逐项比对，差异数 = 0 |

---

## 5. 已知边界

1. **语义层不在模板内**。认知越界、谶语应验、伏笔回收需要角色知识模型与情节图谱，字面匹配做不到。不配置就不产出此类结论。
2. **风格族判定在现代中文上失效**：现代文本会被判为古典族（古典字密度无判别力，实测现代文档 23.4‰ > 古典 20.65‰）。协议化只是把该逻辑外置，未修复。
3. **哈希链非确定性**：报告含 `uuid.uuid4/uuid1` 派生的 `node_id` / `nonce` / `audit_timestamp`。要做存证，须先把这些字段移出哈希载荷或改为内容派生。
4. **跨语言未验证**：只有中文参考实现。
