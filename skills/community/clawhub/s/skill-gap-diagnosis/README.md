# skill_gap_diagnosis — 業務缺口診斷

整合業績、競賽、榮譽、續保率、客戶增長、技能短板等多維數據，統一換算為保障保費口徑，計算缺口金額、需成交件數、緊急度/容易度標籤，按優先級排序，輸出多維度診斷結論。

## 文件結構

```
skill_gap_diagnosis/
├── SKILL.md              # 主文件：元數據、編排邏輯、輸入輸出契約
├── _meta.json            # 元數據
├── LICENSE.txt           # MIT 許可證
├── README.md             # 本文件
├── schema/
│   ├── input.json        # 輸入參數校驗 Schema
│   └── output.json       # 輸出結構校驗 Schema
├── scripts/
│   └── compute_gaps.py   # 缺口計算腳本
├── references/
│   └── diagnosis.md      # 診斷文案提示詞（含 Few-shot）
├── tests/
│   └── test_compute_gaps.py  # pytest 單元測試
└── assets/
    └── .gitkeep
```

## 快速使用

```python
from scripts.compute_gaps import compute_gaps

result = compute_gaps(
    performance_data={...},
    campaign_data={...},
    honor_data={...},
    renewal_data={...},
    customer_growth_data={...},
    skill_data={...}
)
```
