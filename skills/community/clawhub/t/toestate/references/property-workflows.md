# 房產查詢流程與資料口徑

下方 `te <tool> '<JSON>'` 是 [工作流程](mcporter-workflow.md) 定義的 Bash helper，會走現有 Bifrost 並解開回傳。以下皆為查詢；未逐條實測，已抽測項目見工作流程。示範地址只用行政區、路段或公開地標；`$community_id`、`$project_id`、`$lot_key`、`$land_key` 必須取自前一步回傳；不要杜撰或把不同類型 ID 互換。

## 1. 名稱、地址、行政區和生活圈

```bash
te search '{"query":"板橋","limit":5}' | jq '.items[] | {kind,title,sub,href,url}'
te search_communities '{"county":"新北市","town":"板橋區","limit":5}'
te search_properties '{"county":"新北市","address":"板橋區縣民大道二段","limit":3}'
# After identifying the exact community from the previous result:
te get_community "$(jq -cn --argjson id "$community_id" '{community_id:$id}')"
```

`search` 回傳 `kind/title/sub/href`；社區和建案可從已核對的 `/community/{id}`、`/project/{id}` 取 ID。社區數字不代表單棟或某戶；`get_building`、`get_property` 各用相應 ID。查不到某門牌，附近門牌只能當附近比較樣本。相對連結限補上 `https://toestate.tw`，不自己猜 slug。

## 2. 路段或社區的實價登錄

```bash
te search_transactions '{"county":"新北市","town":"永和區","address":"永和區竹林路","txn_kind":"sale","include_special":false,"limit":5}' \
  | jq '{count,limit,offset,summary,sources,items}'
```

`txn_kind`：`sale` 買賣、`presale` 預售、`rent` 租賃；`date_from/date_to` 用 YYYY-MM-DD，先依任務選時間區間。價格金額用元、坪數用坪；`area_ping` 排除車位、包含公設，`unit_price_ping` 為排除車位後元／坪。樣本少就列條件與筆數，不把前幾筆當全區。使用 `summary.basis` 交代統計口徑，分開看 `count`、`summary.n`、實回筆數；需要才用 `offset` 翻頁。特殊交易預設不納入，只有意圖明確才改 `include_special` 並標記。

## 3. 開價合理性與相似成交

```bash
# Set address only to the authorized subject and confirm the parking basis.
args=$(jq -cn --arg a "$address" \
  '{address:$a,asking_price:25000000,area_ping:35,area_includes_parking:true,has_parking:true}')
te analyze_property "$args" | jq '{offer,input_warnings,sources}'
te get_comparable_transactions '{"lat":25.0131,"lng":121.4648,"area_ping":30,"years":2,"radius_m":500,"limit":5}'
```

`asking_price` 是元（2500 萬＝25000000）；不要假定坪數或總價含車位。類型、屋齡、樓層、房數有證據才填。用 `offer.reference_total/range_total/basis`，原始 `estimate` 不另當整戶估價。列相似案例的時間、同棟與否、型態、坪數、關鍵差異與 `input_warnings`。有警告或無樣本就降低結論強度，不能替使用者決定出價。

## 4. 租屋租金與待售待租刊登

```bash
te check_rent '{"county":"臺北市","town":"大安區","rent_type":"whole","rooms":2,"area_ping":25,"rent":30000}' \
  | jq '{subject,stats,position,method,social,sources}'
te get_rent_statistics '{"county":"臺北市"}'
te search_listings '{"county":"臺北市","town":"大安區","kind":"rent","max_price":35000,"limit":5}'
```

`check_rent` 用 `whole` 搭配房數（4＝4 房以上），或 `studio/shared/room`；不要把 `get_rent_statistics` 的 `whole2` 統計分類當查詢列舉。租金元／月，坪數不含車位。引用服務實際回傳的 nearby／town／county 比較範圍（查看 `method`、`stats` 與相關欄位，不假定頂層一定有 `scope`）、樣本數和分位。樣本主要涵蓋應申報的仲介成交或包租業轉租，非所有私人出租；一般租約與包租代管另列。刊登是站內開價，不是成交、也不是全市場。

## 5. 行政區比較、時間序列與申報延遲

```bash
te get_market_pulse '{}' | jq '{cutoff,data_complete_month,refreshed_at,n_1y,median_ping_1y,sources}'
te get_area_statistics '{"county":"臺北市","town":"大安區"}'
te compare_areas '{"areas":["臺北市大安區","新北市板橋區"],"include_monthly":true,"months":12}'
te get_price_history '{"county":"新北市","town":"板橋區","months":24,"txn_kind":"sale"}'
te get_price_index '{"county":"新北市","town":"板橋區","months":24}'
te get_nowcast '{"county":"新北市","months":6}'
```

先選同期間、同類型再比較。盤點時 `compare_areas` 可傳最多 12 區，避免無需求的大範圍。區分中位價、重複交易指數、Hedonic 指數及其覆蓋、基期和月／季粒度；標為 preliminary 或樣本不足的期間不當成確定漲跌。`get_nowcast` 估成交量、區間與完成度，不是已成交筆數。資料完整月、統計截止、服務重算時間、最後一筆成交日分別標明。

## 6. 地圖成交、機能與環境圖層

```bash
te get_nearby_transactions '{"lat":25.0131,"lng":121.4648,"radius_m":500,"residential_only":true,"txn_kind":"sale","limit":5}'
te get_nearby_poi '{"lat":25.0131,"lng":121.4648,"radius_m":800,"limit":8}'
te get_transactions_in_area '{"min_lat":25.010,"min_lng":121.460,"max_lat":25.016,"max_lng":121.470,"months":12,"txn_kind":"sale","limit":20}'
```

半徑是公尺，依距離的案例不一定最相似。框選避免太大，官方工具說明建議約 3 公里見方以內以減少抽樣。查純土地用 `target:"land"`，勿和房地交易混算。POI 和淹水、液化、斷層屬圖層參考；資料無值不代表無風險，不能取代現勘或主管機關圖資。

## 7. 預算與購屋條件

```bash
te find_affordable_areas '{"county":"新北市","town":"板橋區","rooms":3,"budget":15000000}'
te search_by_conditions '{"county":"臺北市","max_total_price":30000000,"max_age_years":15,"near_poi_type":"mrt","near_poi_m":500,"limit":5}'
```

要用自備款與月付推預算，給 `down_payment/monthly_payment` 並核對 `ltv/rate/years`；`0.8` 是八成、`0.025` 是 2.5%，這些是假設，不是實際核貸。讀 `binding/share_ok/ping_at_budget`：這是過去樣本的相容率與參考坪數，非現有可買庫存。`screen_communities` 適合需要成交量、損失比、殖利率、學校距離等更細交集時使用。

## 8. 法拍、點交與公告

```bash
te get_foreclosures '{"county":"臺北市","status":"selling","kind":"house","deliverable":true,"exclude_share":true,"sort":"upcoming","limit":3}'
# Set lot_key from a matching live result.
te get_foreclosure_notice "$(jq -cn --arg k "$lot_key" '{lot_key:$k,full_text:false}')"
```

`status` 有 `selling/sold/lapsed/assumed`；`date_from/date_to` 是拍賣日，`rounds` 是如 `"1,2"` 的字串。價格一律用完整元金額。選中標的才用 `analyze_foreclosure` 比對同棟／附近成交；點交看 `delivery`、占用、租約、欠費、標的持分、防範註記與法院原文，必要才取 `full_text:true`。住宅點交不保證車位點交；`land_share` 是底價中的土地比重，不是產權持分。底價、拍定價、估算市價不同；折價、信心和同棟樣本數不是得標建議，公告有更新時以法院／執行機關最新文件為準。

## 9. 地號、公告現值與使用分區

```bash
te list_land_sections '{"county":"新北市","town":"板橋區","limit":5}'
te search_lands '{"county":"新北市","town":"板橋區","limit":5}'
# Set land_key from a matching result; preserve its formatting.
land_args=$(jq -cn --arg k "$land_key" '{land_key:$k}')
te get_land "$land_args"
te get_zoning "$land_args"
```

土地按全筆／持分、分區、用途、面積與期間分組。公告現值非市價；`get_land_statistics`、`get_land_price_history` 的口徑不等於單宗地號。建蔽率、容積率及分區需主管機關證明。查建照使照另用 `get_building_permits`；工具目前只稱覆蓋新北市，外縣市沒有結果不能說沒核發。

## 10. 土地開發試算

```bash
te estimate_land_development "$(jq -cn --arg k "$land_key" \
  '{land_key:$k,product:"tower",price_ping:650000,profit:0.18,interest:0.04,bonus_pct:0}')"
```

此工具回推土地可負擔成本，不是土地估價。單價元／坪，利息和利潤用小數，`bonus_pct` 是百分比（例如 20 代表增加 20%）；容積或其他欄位以當次工具說明為準。解讀 `steps/warnings/sensitivity`；遇 `need:"area_ping"` 時需有可核對的基地坪數再重查。不要用工具預設或分區常見值裝成確定法定值。多地號合併先核對 `extra_keys` 及每筆分區和面積。

## 11. 預售建案、建商、交屋與人口

```bash
te search_projects '{"county":"新北市","town":"板橋區","limit":5}'
te get_project "$(jq -cn --argjson id "$project_id" '{project_id:$id,txn_limit:5}')"
te list_developers '{"county":"新北市","limit":5,"sort":"projects"}'
te get_handover '{"county":"新北市","town":"板橋區","quarters_ahead":4}'
te get_demographics '{"county":"新北市","town":"板橋區","months":12}'
```

建案備查、預售申報、完工、交屋與首次登記是不同事件。相對同區中古溢價先對齊期間和組成。交屋推估不是個別建案承諾；引用移轉和第一次登記的定義及推估假設。人口與戶數要分開，相關性不是房價因果；建商聚合名和專案應核對，不從統計推斷品質或履約結果。

## 12. 市場訊號、回測與備註風險

```bash
te get_deals '{"county":"臺北市","max_discount":-0.10,"limit":5}'
te get_investment_radar '{"county":"新北市","limit":5}'
te get_signal_backtest '{"include_series":false}'
te get_valuation_methods '{}'
te get_remark_flags '{"county":"新北市","limit":5}'
```

低於社區中位不代表低估：先看樓層、面積、屋況、車位和特殊交易。`get_holding_analysis` 的同戶重複成交是可配對子樣本，不代表所有屋主報酬；模型／指標回測不是未來保證，須報期間、樣本、誤差與限制。特殊備註是資料集文字中的線索；未標記不是沒有瑕疵，有標記也需核對原件，不任意指認住戶。

## 官網資料路標

[官方 llms.txt](https://toestate.tw/llms.txt) 索引了 [開價分析](https://toestate.tw/analyze)、[成交地圖](https://toestate.tw/map)、[價格指數](https://toestate.tw/price-index)、[法拍](https://toestate.tw/foreclosures)、[新建案](https://toestate.tw/projects)、[建商](https://toestate.tw/developers)、[土地行情](https://toestate.tw/land)、[生活圈](https://toestate.tw/zone) 與 [教學](https://toestate.tw/learn)。教學可解釋實登時差、坪數、車位、點交、租金涵蓋與預售流程；涉法律、稅率或貸款規定時另查主管機關當期原文。MCP 有 `sources` 就保存 attribution；網站只當補充或明示 fallback，不混成同一次 MCP 結果。
