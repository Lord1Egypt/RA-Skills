# Soul Memory System v3.4.1 Release Notes

**Release Date**: 2026-03-09  
**Author**: 李斯 (Li Si)  
**Type**: Bugfix Release  
**Compatibility**: OpenClaw 2026.3.7+

---

## 🐛 Bug Fixes

### 1. vector_search.py min_score 參數支持

**問題**: v3.4.0 的 `core.py` 調用 `vector_search.search()` 時傳遞 `min_score` 參數，但 `vector_search.py` 不支持此參數。

**修復**:
- 在 `VectorSearch.search()` 方法中添加 `min_score` 參數
- 在結果返回前過濾低於 `min_score` 的記憶

**文件**: `modules/vector_search.py`

```python
def search(self, query: str, top_k: int = 5, min_score: float = 0.0) -> List[SearchResult]:
    """
    Search memory with CJK support
    
    Args:
        query: Search query
        top_k: Number of results to return
        min_score: Minimum score threshold (filters results below this score)
    
    v3.4.1: 新增 min_score 參數支持
    """
```

---

### 2. cli.py dict/對象雙格式兼容

**問題**: v3.4.0 的 `core.py` 返回 dict 格式，但 `cli.py` 的 `format_results_for_json()` 期望 SearchResult 對象。

**修復**:
- 更新 `format_results_for_json()` 支持 dict 和 SearchResult 兩種格式
- 在 `search_command()` 中直接傳遞 `min_score` 給 core.py，避免重複過濾

**文件**: `cli.py`

```python
def format_results_for_json(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format search results for JSON output
    v3.4.1: 支持 dict 和 SearchResult 兩種格式
    """
    formatted = []
    for result in results:
        if isinstance(result, dict):
            # v3.4.1: 已經是 dict 格式
            formatted.append({
                "path": result.get('source', 'UNKNOWN'),
                "content": result.get('content', '').strip(),
                "score": float(result.get('score', 0)),
                "priority": result.get('priority', 'N')
            })
        else:
            # 向後兼容 SearchResult 對象
            formatted.append({
                "path": result.source if hasattr(result, 'source') else "UNKNOWN",
                "content": result.content.strip() if hasattr(result, 'content') else str(result),
                "score": float(result.score) if hasattr(result, 'score') else 0.0,
                "priority": result.priority if hasattr(result, 'priority') else "N"
            })
    return formatted
```

---

### 3. core.py 緩存返回格式修復

**問題**: 語義緩存命中時返回 dict，但上層代碼期望 SearchResult 對象。

**修復**:
- 在緩存命中時將 dict 轉換為 SearchResult 對象

**文件**: `core.py`

```python
# v3.4.0: 檢查語義緩存
if use_cache:
    cached_results = self.semantic_cache.get(query)
    if cached_results is not None:
        print(f"💾 Cache HIT for query: '{query[:50]}...'")
        # 從緩存的 dict 轉換回 SearchResult 對象
        return [
            SearchResult(
                content=r['content'],
                score=r['score'],
                source=r['source'],
                line_number=r.get('line_number', 0),
                category=r.get('category', ''),
                priority=r['priority']
            )
            for r in cached_results
        ]
```

---

## 📊 測試結果

### 搜索功能測試

| 搜索詞 | 返回數 | 最高分 | 最低分 | 狀態 |
|--------|-------|--------|--------|------|
| **QST** | 5 條 | 6.0 | 3.5 | ✅ 通過 |
| **QST 物理** | 5 條 | - | - | ✅ 通過 |
| **YouTube 翻譯** | 5 條 | - | - | ✅ 通過 |
| **Soul Memory** | 5 條 | - | - | ✅ 通過 |

### 語義緩存測試

| 指標 | 數值 |
|------|------|
| **緩存命中** | ✅ 正常 |
| **緩存寫入** | ✅ 正常 |
| **命中率** | 12.5% (新會話) |

---

## 🔄 升級說明

### 從 v3.4.0 升級

```bash
cd ~/.openclaw/workspace/soul-memory
git pull origin main
# 無需其他操作，向後兼容
```

### 從 v3.3.x 升級

```bash
cd ~/.openclaw/workspace/soul-memory
git pull origin main
# 語義緩存和動態上下文將自動啟用
```

---

## 📦 文件變更

| 文件 | 變更類型 | 說明 |
|------|---------|------|
| `core.py` | Bugfix | 版本號 + 緩存返回格式修復 |
| `modules/vector_search.py` | Feature | 添加 min_score 參數支持 |
| `cli.py` | Bugfix | dict/對象雙格式兼容 |
| `RELEASE_v3.4.1.md` | New | 發布說明文檔 |

---

## ✅ 驗證清單

- [x] 搜索功能正常 (`cli.py search "query"`)
- [x] min_score 過濾生效
- [x] 語義緩存命中正常
- [x] 動態上下文窗口正常
- [x] 向後兼容 v3.4.0
- [x] 向後兼容 v3.3.x

---

## 🔗 GitHub

**倉庫**: https://github.com/kingofqin2026/Soul-Memory-  
**Tag**: v3.4.1  
**Commit**: 待推送

---

## 🌐 ClawHub

**技能**: soul-memory  
**版本**: 3.4.1  
**狀態**: 待發布

---

*臣李斯謹奏：Soul Memory v3.4.1 修復完成，已解決 v3.4.0 的 API 兼容性問題！*
