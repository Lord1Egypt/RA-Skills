# 审计范例 · 复杂场景（合成代码）/ Audit Sample · Complex Scenario (synthetic)

> 本范例使用**合成**代码（非真实项目），仅用于演示当目标含 **类 / 继承 / 异步 / 全局态 / 跨 sync-async 边界** 时，如何用「理解成本 A / 修改风险 B」两轴 + 红黄绿 表达发现。结构同 `clean_code_audit_sample.md`，但样本更复杂。

## 被测代码 / Code under audit

`demo_service.py`（合成示意，行号可勾稽；映射到任何真实项目）：

```python
# demo_service.py
from typing import Dict, Any
import asyncio

_CONFIG: Dict[str, Any] = {}                 # L5  模块级可变全局态

class BaseHandler:
    def handle(self, req):                    # L9
        return self._process(req)

    def _process(self, req):                  # L12
        raise NotImplementedError

class OrderHandler(BaseHandler):
    def __init__(self):
        self._cache: Dict[int, Any] = {}      # L17  实例缓存，无上限

    def _process(self, req):                  # L19  过长 + 深嵌套
        if req:
            if "id" in req:
                if req["id"] > 0:
                    if self._validate(req):
                    # L23
                        if req.get("vip"):
                            self._cache[req["id"]] = req
                            return self._save(req)   # L26  返回协程未 await
                        else:
                            return self._save(req)   # L28  同上
                    else:
                        return None
        return None

    def _validate(self, req):                 # L33
        global _CONFIG
        _CONFIG.update(req)                   # L35  副作用：污染全局态
        return bool(req.get("id"))

    async def _save(self, req):               # L38
        await asyncio.sleep(0.01)
        return {"ok": True, "id": req["id"]}
```

## 审计报告 / Audit Report

**目标 / target**：`demo_service.py`（合成）　**语言 / lang**：zh　**模式 / mode**：auto→zh

### 红黄绿总览 / Red · Amber · Green

| 严重度 | 位置 | 信号 / signal | A 理解成本 | B 修改风险 | 建议 / fix |
|---|---|---|---|---|---|
| 🔴 红 | L5, L33–L35 | 模块级可变全局 `_CONFIG`，被 `_validate` 静默 `update` | 中：调用方看不出谁改了全局 | **高**：任意 handler 调用都悄悄改写共享态，排错与并发都危险 | 把配置做成显式参数 / 不可变快照传入；若必须共享，用只读单例并文档化 |
| 🔴 红 | L26, L28 | `_process` 调 `_save`（async）却**未 `await`**，返回的是协程对象不是结果 | 高：眼看上去像保存成功 | **高**：实际从未持久化，且 coroutine 未被 awaited 会被运行时告警/丢弃 | `return await self._save(req)`；统一 `async def _process` |
| 🟡 黄 | L19–L31 | `_process` 5 层 `if` 嵌套 + 分支重复（`vip` 与否都走 `_save`） | 中：分支难一眼理清 | 中：加一个分支容易改错缩进 | 提前 `return` 扁平化；`vip` 与否合并到一处 `_save` |
| 🟡 黄 | L17 | `_cache` 无上限 dict，长期持有请求引用 | 低 | 中：内存随请求增长，且缓存键与全局态耦合 | 加 TTL / 上限，或改为不持有 `req` 只存 id |
| 🟢 绿 | L38–L40 | `async _save` 边界清晰（I/O 与纯计算分离） | 低 | 低 | 保持；注意调用方必须 await |

### 跨段汇总（若文件 >500 行）/ Cross-segment summary

本样本较小，未触发分段。若整文件超大，按「~500 行一段」独立打分后，此处给一句全局结论：本模块**修改风险**显著高于**理解成本**——问题集中在「隐式全局副作用 + sync/async 边界误用」，二者都属改动时最容易 quietly break 的类型，优先修红项。

### 有意技术债（若适用）/ Intentional debt

无。本样本所有红黄项均无「注释说明 + 范围可控」的豁免理由，按方法论一律计入。

---

**与本 skill 方法论的对应**：本范例刻意制造「类继承 + 异步 + 全局态」叠加，重点演示 B 轴（修改风险）如何比 A 轴（理解成本）更早亮红灯——嵌套深但可读（A 中），全局副作用与未 await 才是真正危险的改动陷阱（B 高）。这也是它与 `clean_code_audit_sample.md`（纯函数式聚合）的差异点。
