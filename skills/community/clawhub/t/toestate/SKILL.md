---
name: toestate
description: "查台灣實價登錄、特定社區或建案房價、開價與附近成交比較、租金、行政區趨勢、法拍點交、地號與使用分區、交屋供給或自住預算時使用。也適用於使用者直接指定 ToEstate。"
metadata:
  openclaw:
    emoji: "🏠"
    requires:
      bins:
        - mcporter
        - jq
  related-skills:
    mcporter: Discover and call a configured ToEstate-capable Bifrost MCP server.
---

# ToEstate — 台灣不動產資料查詢

以 ToEstate 查公開房產資料。這是第三方整合技能，非 ToEstate 官方套件；需先在自己的環境配置可使用 ToEstate 的 Bifrost。預設路徑是 **mcporter → Bifrost → ToEstate**；不需要獨立的 `toestate` 連線或編輯器匯入。

## 核心流程

1. **定範圍。** 先辨別是買賣、預售、租賃、刊登、法拍或土地。保留縣市、行政區、時間窗與建物類型；沒有明確條件就不要偷補。對外只送最少查詢條件，不送姓名、帳密、私人筆記或未經授權的第三人住址。能用行政區或路段回答時不送完整門牌。
2. **確認能力。** 依 [mcporter 工作流程](references/mcporter-workflow.md) 核對配置中的 Bifrost 有所需的 `ToEstate-<tool>`。Bifrost 的清單、實際呼叫、回傳資料是三層驗證。不要為了補工具重新開啟自動匯入、重建直連或修改 Gateway。
3. **先消歧義再查明細。** 名稱或地標不確定用 `search`；專門的 `search_communities`、`search_projects`、`search_properties` 各自定位。到第二步才用結果給的 ID／key 查詳情；同名核對縣市、區、地址與類別。相近地址不是精確門牌，不可代替；沒有實登紀錄也不能推論沒有成交。
4. **驗證回傳。** 看 exit code、MCP `isError` 和解開後的業務錯誤、樣本數、範圍、警告。從小 `limit` 開始，先判讀再追加。不要把查詢失敗、查無樣本、資料未覆蓋和欄位未回傳混為一談。
5. **回報口徑。** 附 `sources`、查詢範圍、期間與筆數；有 `cutoff`、`data_complete_month`、`refreshed_at` 時分開說明。沒有截止日就標未提供；最近成交日和查詢日都不等於資料截止日。關鍵結論附可回查的頁面或公告，保留原來源署名。

## 工具怎麼選

| 意圖 | 先用 | 要補什麼再查 |
| --- | --- | --- |
| 找社區、建案、路段 | `search`；已知類型走專用搜尋 | `get_community`／`get_project`／`get_building`／`get_property` |
| 逐筆成交、開價比較 | `search_transactions`；指定地址和開價用 `analyze_property` | `get_comparable_transactions` 或同棟、社區成交 |
| 租金、待售／待租 | `check_rent`／`get_rent_statistics`；刊登用 `search_listings` | `search_transactions(txn_kind=rent)` 看逐筆申報 |
| 行政區、趨勢、近期量 | `get_area_statistics`／`compare_areas`；全台 `get_market_pulse` | `get_price_history`／`get_price_index`／`get_nowcast` |
| 地圖、機能或環境 | `get_nearby_transactions`／`get_transactions_in_area` | `get_nearby_poi`；土地另看 `get_zoning` |
| 法拍 | `get_foreclosures` | 用 `lot_key` 查 `get_foreclosure_notice`／`analyze_foreclosure` |
| 土地、地段、開發 | `search_lands`／`list_land_sections` | `get_land`／`get_zoning`；假設完整才試算開發 |
| 首購預算、建商、交屋、人口 | `find_affordable_areas`／`search_projects`／`list_developers` | `get_developer`／`get_handover`／`get_demographics` |

## 快速查詢

```bash
mcporter call bifrost.ToEstate-get_area_statistics \
  --args '{"county":"臺北市","town":"大安區"}' \
  --no-oauth --timeout 12000 --output json
```

依工作流程處理外層 `result` 可能是 JSON 字串的情形；不要把指令 exit 0 當成有行情數字。

## 判讀重點

- 實登申報有約 1–3 個月落差；每日更新不代表今天成交都入庫。統計預設排除部分特殊交易。不要把初步期或預估當完整月份，也別混用指數與元／坪。[官方資料說明](https://toestate.tw/llms.txt)
- 交易工具的 `area_ping` 含公設、排除車位，並非室內坪；`unit_price_ping` 是扣車位後元／坪；總價、坪數與每坪價格要按各欄位口徑單獨解讀，不可直接用含車位總價除以扣車位坪數。[資料口徑與任務範例](references/property-workflows.md)
- `analyze_property` 用 `offer.reference_total`、`offer.range_total`、`offer.basis` 和 `input_warnings`，以相似成交的統計比較表達，不能當成估價報告或出價指示。法拍點交、地籍分區、租稅、貸款和產權，關鍵決策以該管機關文件或合格專業意見為準。
- Bifrost 回傳的 55 個工具為 2026-11-18 盤點快照；不是 55 個都成功跑過。查詢的 schema、回傳欄位與當下可用性以現場為準。斷線時可改查公開頁面並說明方法，不回填推測數字。

## 詳細參考

- [mcporter 工作流程](references/mcporter-workflow.md)：能力探測、JSON 解包、錯誤處理與實測紀錄。
- [房產查詢工作流程](references/property-workflows.md)：12 種查詢情境、參數範例、資料來源與踩雷點。
- [完整工具索引](references/tool-catalog.md)：55 個已公開工具的用途與輸入欄位。參數預設、列舉及版本以當次工具說明為準。
- [ToEstate 官方 MCP 教學](https://toestate.tw/mcp-guide) 與 [官方 llms.txt](https://toestate.tw/llms.txt)。
