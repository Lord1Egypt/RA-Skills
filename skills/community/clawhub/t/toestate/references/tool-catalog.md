# ToEstate 工具索引

2026-11-18 從 Bifrost MCP 讀回 55 個工具的輸入 schema。呼叫名稱為 `ToEstate-<工具>`。此表是用途與欄位索引，不是每項均已執行的證明。

「必填」指 JSON Schema required；地號或座標等擇一條件常另外寫在工具說明。實際型別、列舉、預設值和值域以當次 schema 及 description 為準。[任務實例](property-workflows.md) · [探測方式](mcporter-workflow.md)

## 名稱搜尋、物件、成交與租金

| 工具 | 用途（依公開工具說明摘錄） | 必填欄位 | 其他欄位 |
| --- | --- | --- | --- |
| `search` | 全站搜尋：輸入使用者說的任何東西——社區名、建案名、地址（可省略縣市）、行政區（「板橋」「台南東區」）、 | `query` | `limit` |
| `search_communities` | 用社區/建案名稱或地址關鍵字找社區，回傳 community_id 與摘要統計 | — | `county`, `limit`, `name`, `town` |
| `search_properties` | 用地址找棟（building）與戶（property） | `address` | `county`, `limit` |
| `get_community` | 取得社區：名稱、棟數、完工日、近 1/3 年單價與成交量、年增率、租金與租售比、各棟清單（最多 12 棟，另附總數）、附近社區與附近新建案、 | `community_id` | — |
| `get_building` | 取得單棟建築：屬性、統計（近 1/3 年中位單價、成交量）、戶別清單、最近交易 | `building_id` | — |
| `get_property` | 取得單一戶/樓層的資料與其歷次交易 | `property_id` | — |
| `search_transactions` | 搜尋實價登錄成交 | — | `address`, `building_id`, `building_type`, `community_id`, `county`, `date_from`, `date_to`, `include_special`, `limit`, `max_ping`, `max_price`, `min_ping`, `min_price`, `offset`, `town`, `txn_kind` |
| `search_listings` | 本站使用者刊登的待售／待租物件（kind: sale ／ rent），每筆附與同社區實價的比較 | — | `building_type`, `community_id`, `county`, `kind`, `limit`, `max_ping`, `max_price`, `min_ping`, `min_price`, `rooms`, `sort`, `town` |
| `analyze_property` | 「這間開價 X 合理嗎」：比較案例 → 參考單價區間 → 與開價比較（偏高/合理/偏低），附同棟成交、社區與行政區統計、周邊 POI 與環境風險 | `address` | `age_years`, `area_includes_parking`, `area_ping`, `asking_price`, `building_type`, `county`, `floor`, `has_parking`, `rooms` |
| `get_comparable_transactions` | 比較案例引擎：輸入標的（地址或座標、坪數、樓層、屋齡、房數、車位、型態），回傳依 comparable_score 排序的相似成交與各分項分數 | — | `address`, `age_years`, `area_ping`, `building_type`, `county`, `floor`, `has_parking`, `lat`, `limit`, `lng`, `radius_m`, `rooms`, `years` |
| `check_rent` | 租金行情查詢（租屋族問「這個租金貴不貴／附近租多少」用這個）：附近 3 公里內同型態、坪數相近（±35%）的一般租約最近 30 筆（近 24 個月）， | — | `address`, `area_ping`, `county`, `rent`, `rent_type`, `rooms`, `town` |
| `get_rent_statistics` | 各縣市（不給 county）或某縣市各行政區的租金統計：一般租約近一年（以資料完整月為終點）依型態分組（whole1～whole4 整層住家 1～4 房以上、 | — | `county` |

## 區域、市場、指數與交屋

| 工具 | 用途（依公開工具說明摘錄） | 必填欄位 | 其他欄位 |
| --- | --- | --- | --- |
| `get_area_statistics` | 行政區統計：近 1/3 年成交量與中位單價、年增率、租金 | `county` | `town` |
| `compare_areas` | 比較多個行政區（一次最多 12 個）：areas 例 ["桃園市中壢區","新竹縣竹北市"] 或 ["桃園市／中壢區"]（兩種寫法都可） | `areas` | `include_monthly`, `months` |
| `get_county_overview` | 全台各縣市近一年成交筆數、中位單價與年增率，以及各縣市統計重算時間（refreshed_at） | — | — |
| `get_market_pulse` | 市場脈動：全台加權中位單價與年變化、近一年成交量與年變化、資料完整月、行情模型誤差中位數 | — | — |
| `get_price_history` | 月度價格序列（中位/平均單價、成交量） | — | `building_id`, `community_id`, `county`, `months`, `town`, `txn_kind` |
| `get_price_index` | 房價指數（基期 2016-01=100）：中位數（median_index，月）、重複交易指數（repeat_sales_index，同一戶前後成交；granularity 標示月… | — | `community_id`, `county`, `months`, `town` |
| `get_index_overview` | 各縣市重複交易房價指數（同一戶前後兩次成交，2016-01=100）的月序列與一年變化、距歷史高點 | — | `months` |
| `get_index_towns` | 指定縣市內各行政區的重複交易季指數：最新值、一年／三年變化、最新一季配對數與是否初步值，及近 years 年的季序列 | `county` | `years` |
| `get_nowcast` | 近月成交量預估（申報延遲校正）：實價登錄申報有 1–3 個月延遲，最近幾個月筆數不全 | — | `county`, `months` |
| `get_demographics` | 鄉鎮市區人口基本面（戶政司月資料）：戶數、人口、出生死亡、遷入遷出、戶數年增、人口年增、12 個月淨遷入率 | `county` | `months`, `town` |
| `get_handover` | 交屋潮（預售屋交屋供給）：預售屋簽約時申報實價、交屋過戶時不再申報，所以內政部「建物買賣移轉棟數」＝中古買賣＋預售交屋 | `county` | `quarters_ahead`, `town` |

## 預售、建商、條件與市場訊號

| 工具 | 用途（依公開工具說明摘錄） | 必填欄位 | 其他欄位 |
| --- | --- | --- | --- |
| `search_projects` | 新建案（預售備查建案）搜尋：建案名/建商、戶數、建照、預售成交筆數與中位單價、相對同區中古溢價（premium_vs_area）、交屋後中古 vs 預售（resale_vs_pre… | — | `county`, `limit`, `name`, `sort`, `town` |
| `get_project` | 建案頁：預售成交月序列、最近成交（txn_limit 筆，預設 15；transactions_total 為總筆數）、基地地號與現值、對應社區（交屋後）中古行情、附近 1.5 公… | `project_id` | `txn_limit` |
| `get_project_overview` | 新建案（預售）總覽：各行政區近 24 個月預售成交數、中位單價、相對同區中古的溢價 | — | `county` |
| `list_developers` | 建商彙總：推案數、戶數、預售成交、中位單價、相對區域中古溢價、交屋後中古 vs 預售、去化速度（戶/月） | — | `county`, `limit`, `name`, `sort` |
| `get_developer` | 單一建商：各縣市彙總 by_county、歷年預售成交與單價 yearly、交屋後表現 track、建案清單 projects（最多 20，精簡欄位） | `name` | — |
| `find_affordable_areas` | 自住／首購：「我的預算能在哪裡買到房子」 | — | `budget`, `building_type`, `county`, `down_payment`, `ltv`, `max_age`, `max_ping`, `min_ping`, `monthly_payment`, `parking`, `rate`, `rooms`, `town`, `years` |
| `search_by_conditions` | 社區條件搜尋 | — | `building_types`, `county`, `limit`, `max_age_years`, `max_ping`, `max_total_price`, `min_ping`, `min_total_price`, `min_txn_1y`, `near_poi_m`, `near_poi_type`, `price_hoh_max`, `sort`, `town`, `volume_hoh_min` |
| `screen_communities` | 社區篩選器（房地產版 Finviz） | — | `area_ping`, `building_types`, `county`, `limit`, `max_age_years`, `max_gap_vs_new`, `max_loss_share`, `max_mrt_m`, `max_ping`, `max_price_hoh`, `max_price_yoy`, `max_school_m`, `max_total_price`, `min_age_years`, `min_annual_return`, `min_ping`, `min_price_yoy`, `min_total_price`, `min_txn_1y`, `min_volume_hoh`, `min_volume_yoy`, `min_yield`, `sort`, `town`, `towns` |
| `get_deals` | 低估掃描：近 N 月成交單價低於同社區近一年中位 ≥10%（max_discount=-0.10）的案例，附可能原因（低樓層/頂樓/小坪/老屋/備註異常） | — | `community_id`, `county`, `exclude_reasons`, `limit`, `max_discount`, `months`, `sort`, `town` |
| `get_deal_summary` | 低估成交摘要：近 12 個月比同社區中位便宜的成交件數、中位折價、無明顯原因比例、各行政區分布 | — | `county` |
| `get_holding_analysis` | 社區持有分析：同一戶前後兩次成交 → 中位持有年、中位總報酬、年化報酬、賠售比例、兩年內轉手比例、近期轉手案例 | `community_id` | — |
| `get_investment_radar` | 投資機會雷達（行政區層）：近一年價格漲跌、成交量增減、租金殖利率、相對新案價差、供給比（兩年新案戶數/年成交量）、持有年化報酬， | — | `county`, `limit`, `sort` |
| `get_signal_backtest` | 指標領先性回測：投資機會雷達各科（殖利率、價格動能、一年量增、比新案便宜，以及已停用的近 3 月量能、價格平穩、供給少）與候選指標（指數動能、距高點回檔、一年漲幅原值、雷達總分）在… | — | `include_series`, `lag_q` |
| `get_valuation_methods` | 行情模型／指數方法說明與公開回測：各縣市 hedonic 模型的測試集 MdAPE、±10% 命中率、樣本數 | — | — |
| `get_remark_flags` | 實價登錄成交備註提到非自然死亡（凶宅）、海砂屋、輻射屋、火災的買賣與預售成交（「台中有哪些凶宅紀錄」） | — | `county`, `limit` |

## 地圖、土地與建管

| 工具 | 用途（依公開工具說明摘錄） | 必填欄位 | 其他欄位 |
| --- | --- | --- | --- |
| `get_nearby_transactions` | 找座標附近的成交，依距離排序 | `lat`, `lng` | `limit`, `radius_m`, `residential_only`, `target`, `txn_kind`, `years` |
| `get_transactions_in_area` | 地圖框選：經緯度範圍內近 months 個月的成交點（單價、總價、日期、社區） | `min_lat`, `min_lng`, `max_lat`, `max_lng` | `building_type`, `limit`, `max_age_years`, `max_price`, `min_price`, `months`, `target`, `txn_kind` |
| `get_nearby_poi` | 附近 POI（mrt/tra/hsr/school/hospital/park/…）與該點的環境風險（液化/淹水/斷層敏感區） | `lat`, `lng` | `limit`, `poi_types`, `radius_m` |
| `search_lands` | 找地號：依縣市/區/段名（可只給前綴）/地號，回傳 land_key、面積、分區、最新成交與公告現值 | — | `county`, `land_no`, `limit`, `section`, `town` |
| `get_land` | 地號頁：面積、分區/建蔽容積、歷年公告現值、歷次交易（標示全筆/持分）、成交倍數、同段鄰號近 5 年成交、上方建物與社區 | — | `county`, `land_key`, `land_no`, `section`, `town` |
| `list_land_sections` | 地段排行：各段（段小段）近一年土地成交筆數、單價、漲跌、公告現值倍數 | `county` | `limit`, `sort`, `town`, `zoning_category` |
| `get_land_section` | 地段：給 section_key 回傳整段統計、段內地號清單（前 limit 個，依近期成交排序）、近期土地成交；只給 county(+town) 則列出該區各地段排行（sort:… | — | `county`, `limit`, `section_key`, `sort`, `town` |
| `get_land_rankings` | 地段榜：sort = n_1y 熱門 ／ yoy 漲最多 ／ yoy_asc 跌最多 ／ multiple 現值倍數最高 ／ price 單價最高 | — | `county`, `limit`, `min_n`, `sort`, `zoning_category` |
| `get_land_statistics` | 土地行情統計：行政區 × 分區類別（住/商/工/農/公設/非都市…）的近 1/3 年成交量、中位元/坪、年增率、公告現值倍數；附各縣市總覽 | — | `county`, `town`, `zoning_category` |
| `get_land_price_history` | 土地成交單價月序列（全筆移轉、非特殊交易），可依都市計畫使用分區類別（住宅區、商業區、工業區、農業區…）過濾 | `county` | `months`, `town`, `zoning_category` |
| `get_zoning` | 座標或地號 → 都市計畫使用分區、建蔽率、容積率（參考值） | — | `land_key`, `lat`, `lng` |
| `estimate_land_development` | 土地開發試算（回推土地可負擔成本，非土地估價）：V = S ÷ (1+R) ÷ (1+i) − (C+M)；S 總銷、R 利潤率、i 資本利息綜合利率、C 營建費用、M 規劃設計與… | `land_key` | `area_ping`, `basement_levels`, `bonus_pct`, `build_cost_ping`, `extra_keys`, `far_pct`, `indirect`, `interest`, `margin`, `parking_price`, `price_ping`, `product`, `profit`, `sale_ratio` |
| `get_building_permits` | 建照/使照查詢（起造人、戶數、樓層、構造、面積） | — | `address`, `building_id`, `county`, `land_key` |

## 法拍與點交

| 工具 | 用途（依公開工具說明摘錄） | 必填欄位 | 其他欄位 |
| --- | --- | --- | --- |
| `get_foreclosures` | 法拍標的（全台地方法院＋行政執行署） | — | `comparable_only`, `county`, `date_from`, `date_to`, `deliverable`, `exclude_share`, `featured`, `hide_suspect`, `kind`, `limit`, `max_ping`, `max_price`, `min_market_confidence`, `min_ping`, `min_price`, `offset`, `q`, `rounds`, `sort`, `status`, `town` |
| `get_foreclosure_stats` | 法拍統計（可限縣市）：目前待拍件數與各拍次底價相對市價、拍定價相對市價、點交與否的價差、各縣市件數與中位折價 | — | `county` |
| `get_foreclosure_notice` | 單一法拍標的的法院拍賣公告：本標別的「點交情形／使用情形／備註」原文、解析後的點交明細（delivery），以及公告 PDF 連結 | `lot_key` | `full_text` |
| `analyze_foreclosure` | 一次取得分析單一法拍標的所需的全部資料：標的（法院、案號、拍次、底價、坪數換算、點交碼、公告解析的點交明細與現況摘要、保證金、投標時間）、 | `lot_key` | `full_text` |
