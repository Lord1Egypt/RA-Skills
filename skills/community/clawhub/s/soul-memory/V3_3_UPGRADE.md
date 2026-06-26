# Soul Memory v3.3 升級文檔

## 什麼是 v3.3？

Soul Memory v3.3 是一次重大升級，核心改進包括：

| 模組 | 改進 | v3.2.4 → v3.3 |
|------|------|---------------|
| **關鍵詞映射** | 分層字典 + 權重化 | 單層 → 三層分級 |
| **去重機制** | 語意相似度 + MD5 | MD5 → 雙層機制 |
| **標籤系統** | 多標籤搜索索引 | 無 → 多標籤支持 |
| **用戶定制** | 通用 Schema | 硬編碼 → 可擴展 |

---

## 核心改進

### 1. 分層關鍵詞字典（通用 Schema）

```python
KEYWORD_MAPPING = {
    'Theory': {
        'primary': [
            ('framework', 10, ['framework', 'theory', 'core']),
            ('schema', 9, ['schema', 'structure', 'pattern']),
            ('model', 8, ['model', 'simulation', 'computation']),
        ],
        'secondary': [
            ('document', 7, ['document', 'export', 'format']),
            ('version', 6, ['version', 'iteration', 'update']),
        ],
        'tertiary': [
            ('analysis', 3, ['analysis', 'discussion', 'review']),
        ]
    }
}
```

**特點**：
- 三層分級（primary > secondary > tertiary）
- 權重系統（10 到 3）
- 多標籤支持

**優勢**：
- 無需硬編碼用戶特定字眼
- 用戶可動態添加 `USER_KEYWORDS`
- 通用術語適應不同場景

### 2. 語意相似度去重（雙層機制）

```
第一層：MD5 完全匹配（快速）
  ↓ (如果不匹配)
第二層：語意相似度檢查 (difflib, threshold=0.85)
  ↓
判定是否重複
```

**效果**：
- 完全相同：📦 跳過（MD5 相同）
- 語意相似：🔄 跳過（相似度 > 85%）
- 唯一內容：✅ 保存

### 3. 多標籤索引系統

```python
# 記憶標籤格式
**標籤**: framework(10), deployment(7), website(9)
## [C] 14:30 - Heartbeat 自動提取
已部署 framework 到 website...

---

# 標籤搜索
tag_idx.search(['framework', 'website'], operator='AND')
```

**搜尋方式**：
- AND: 必須包含所有標籤
- OR: 包含任一標籤即可
- 按分數排序（權重 × 優先級）

---

## 使用方式

### 基本使用（使用默認配置）

```bash
# 運行 Heartbeat
python3 /root/.openclaw/workspace/soul-memory/heartbeat-trigger_v3_3.py
```

### 自定義關鍵詞

```python
from keyword_mapping_v3_3 import classify_content, USER_KEYWORDS

# 添加用戶特定關鍵詞
USER_KEYWORDS['MyDomain'] = {
    'primary': [
        ('my_framework', 10, ['my_framework', 'my_theory']),
        ('my_project', 8, ['my_project', 'my_repo']),
    ]
}

# 使用
tags = classify_content(content, custom_mapping=USER_KEYWORDS)
```

### 標籤搜索

```python
from tag_index_v3_3 import TagIndex

# 加載索引
tag_idx = TagIndex('/path/to/tag_index.json')

# 搜索
results = tag_idx.search(['framework', 'deployment'], operator='AND')
for r in results:
    print(f"{r['file']}:{r['line']} [{r['priority']}]")
```

---

## 設備路徑

| 文件用途 | 路徑 |
|----------|------|
| **Heartbeat 主程序** | `/root/.openclaw/workspace/soul-memory/heartbeat-trigger_v3_3.py` |
| **關鍵詞映射** | `/root/.openclaw/workspace/soul-memory/keyword_mapping_v3_3.py` |
| **語意去重** | `/root/.openclaw/workspace/soul-memory/semantic_dedup_v3_3.py` |
| **標籤索引** | `/root/.openclaw/workspace/soul-memory/tag_index_v3_3.py` |
| **去重記錄** | `/root/.openclaw/workspace/soul-memory/data/dedup.json` |
| **標籤索引** | `/root/.openclaw/workspace/soul-memory/data/tag_index.json` |

---

## 關鍵詞字典示例

### Theory 類（理論框架）

| 層級 | 關鍵詞 | 權重 | 標籤 |
|------|--------|------|------|
| Primary | `framework` | 10 | framework, theory, core |
| Primary | `schema` | 9 | schema, structure, pattern |
| Secondary | `document` | 7 | document, export, format |
| Tertiary | `analysis` | 3 | analysis, discussion, review |

### System 類（系統配置）

| 層級 | 關鍵詞 | 權重 | 標籤 |
|------|--------|------|------|
| Primary | `api_key` | 10 | api_key, secret, token |
| Primary | `config_file` | 9 | config_file, setting, parameter |
| Secondary | `repository` | 7 | repository, git, version_control |
| Secondary | `web_server` | 6 | web_server, apache, nginx |

### Deployment 類（部署和網站）

| 層級 | 關鍵詞 | 權重 | 標籤 |
|------|--------|------|------|
| Primary | `deployment_target` | 10 | deploy, publish, release |
| Primary | `website_url` | 9 | website, domain, host |
| Secondary | `static_file` | 7 | html, css, js, static |

---

## 升級步驟

### 步驟 1：備份現有數據

```bash
cp /root/.openclaw/workspace/soul-memory/dedup_hashes.json \
   /root/.openclaw/workspace/soul-memory/dedup_hashes.json.backup
```

### 步驟 2：測試新功能

```bash
# 測試關鍵詞映射
python3 /root/.openclaw/workspace/soul-memory/keyword_mapping_v3_3.py

# 測試語意去重
python3 /root/.openclaw/workspace/soul-memory/semantic_dedup_v3_3.py

# 測試標籤索引
python3 /root/.openclaw/workspace/soul-memory/tag_index_v3_3.py
```

### 步驟 3：運行 Heartbeat v3.3

```bash
python3 /root/.openclaw/workspace/soul-memory/heartbeat-trigger_v3_3.py
```

### 步驟 4：驗證結果

```bash
# 檢查新記憶
cat /root/.openclaw/workspace/soul-memory/data/tag_index.json

# 檢查去重記錄
cat /root/.openclaw/workspace/soul-memory/data/dedup.json
```

---

## 注意事項

### 1. 通用 vs 特定

v3.3 使用通用術語，不包含用戶特定字眼：

| v3.2.4（特定） | v3.3（通用） |
|----------------|---------------|
| `QST` | `framework` |
| `qsttheory.com` | `website_url` |
| `Qst-memory` | `repository` |
| `秦王` | `user`（用戶自定義） |

如需特定字眼，通過 `USER_KEYWORDS` 添加。

### 2. 模擬數據目錄

第一次運行會自動創建：
```
/root/.openclaw/workspace/soul-memory/data/
├── dedup.json          # 去重記錄
└── tag_index.json      # 標籤索引
```

### 3. 性能優化

- MD5 去重：O(1) 快速
- 語意去重：O(n×m)（n: 已保存數量, m: 內容長度）
- 標籤搜索：O(k)（k: 標籤數量）

---

## 故障排除

### 問題：無法加載標籤索引

```bash
# 檢查文件是否存在
ls -la /root/.openclaw/workspace/soul-memory/data/

# 腳次運行會自動創建，如權限問題則手動創建
mkdir -p /root/.openclaw/workspace/soul-memory/data/
chmod 755 /root/.openclaw/workspace/soul-memory/data/
```

### 問題：關鍵詞識別不准

```python
# 添加自定義關鍵詞
from keyword_mapping_v3_3 import USER_KEYWORDS

USER_KEYWORDS['MyCategory'] = {
    'primary': [
        ('my_keyword', 10, ['my_tag1', 'my_tag2']),
    ]
}
```

---

## 版本歷史

| 版本 | 日期 | 改進 |
|------|------|------|
| v3.2.2 | 2026-02-19 | MD5 哈希去重 |
| v3.2.4 | 2026-02-26 | 寬鬆識別模式 |
| **v3.3** | **2026-02-26** | **分層關鍵詞 + 語意去重 + 多標籤** |

---

## 下一步

- [ ] 用戶自定義關鍵詞文檔
- [ ] 標籤可視化界面
- [ ] 自動優化權重
- [ ] 分類推薦系統

---

**作者**: Soul Memory System Team
**日期**: 2026-02-26
**版本**: 3.3.0
