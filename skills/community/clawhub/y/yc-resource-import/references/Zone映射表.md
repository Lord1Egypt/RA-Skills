# 巴厘岛 Zone ID 官方映射表 V4.0

> 本表为 yc-resource-import 技能专用，用于自动匹配资源 Zone ID。

---

## Zone 区域划分

| Zone ID | 包含地区 | 说明 |
|---------|---------|------|
| Zone-S1 | 努沙杜瓦（Nusa Dua）、金巴兰（Jimbaran）、蒲希尼（Pulau Benoa）、港乐（Tanjung Benoa） | 南部高端度假区 |
| Zone-S2 | 库塔（Kuta）、水明漾（Seminyak）、长谷（Canggu）、萨努尔（Sanur）、雷贡（Legen）、纳闽巴来（Nusa Lambongan） | 西南海岸核心区 |
| Zone-C1 | 乌布（Ubud）、德格拉朗（Tegallalang）、嘉利维（Keliki）、扑满（Penestanan）、赛德村（Sayan） | 中部艺术文化区 |
| Zone-W1 | 贝都古（Bedugul）、汉达拉（Handara）、贾蒂卢维（Jatiluwih）、百度库（Bratan）、布萨基（Buaskan） | 西部山区/湖泊区 |
| Zone-E1 | 帕当拜（Padangbai）、阿曼（Amed）、图蓝本（Tulamben）、森杜尔（Sendang）、天使眼泪（Angel's Billabong） | 东部潜水区 |
| Zone-N1 | 京打马尼（Kintamani）、巴图尔（Batur）、罗威纳（Lovina）、塞库普（Singaraja）、姆德寺（Pura Madu） | 北部火山/海岸区 |
| Zone-OFF | 佩妮达（Nusa Penida）、蓝梦岛（Nusa Lembongan）、吉利群岛（Gili Islands）、蓝梦（Nusa Ceningan） | 离岛区域 |
| 未知 | 无法映射到以上区域 | 手动确认 |

---

## 自动匹配规则

1. **优先匹配合同中的区域描述**，如"位于努沙杜瓦" → Zone-S1
2. **GPS 坐标辅助判断**：
   - 南纬 8.6°~8.9° + 东经 115°~115.3° → Zone-S1/S2
   - 南纬 8.4°~8.6° + 东经 115.1°~115.5° → Zone-C1
   - 南纬 8.0°~8.4° + 东经 115°~115.4° → Zone-N1/W1
   - 佩妮达/蓝梦岛海域 → Zone-OFF
3. **地址关键词匹配**：
   - 努沙杜瓦/金巴兰/蒲希尼/港乐 → Zone-S1
   - 库塔/水明漾/长谷/萨努尔 → Zone-S2
   - 乌布/德格拉朗/嘉利维 → Zone-C1
   - 百度库/贝都古/汉达拉/贾蒂卢维 → Zone-W1
   - 阿曼/图蓝本/帕当拜 → Zone-E1
   - 京打马尼/巴图尔/罗威纳/塞库普 → Zone-N1
   - 佩妮达/蓝梦岛/吉利 → Zone-OFF
4. **无法匹配时填"未知"**，并在 notes 标注：`[Zone待确认]`

---

## 地区名称中英对照表

| 中文名 | 英文名 | Zone |
|--------|--------|------|
| 努沙杜瓦 | Nusa Dua | Zone-S1 |
| 金巴兰 | Jimbaran | Zone-S1 |
| 蒲希尼 | Pulau Benoa | Zone-S1 |
| 港乐 | Tanjung Benoa | Zone-S1 |
| 库塔 | Kuta | Zone-S2 |
| 水明漾 | Seminyak | Zone-S2 |
| 长谷 | Canggu | Zone-S2 |
| 萨努尔 | Sanur | Zone-S2 |
| 乌布 | Ubud | Zone-C1 |
| 德格拉朗 | Tegallalang | Zone-C1 |
| 嘉利维 | Keliki | Zone-C1 |
| 贝都古 | Bedugul | Zone-W1 |
| 百度库 | Lake Bratan | Zone-W1 |
| 汉达拉 | Handara | Zone-W1 |
| 贾蒂卢维 | Jatiluwih | Zone-W1 |
| 帕当拜 | Padangbai | Zone-E1 |
| 阿曼 | Amed | Zone-E1 |
| 图蓝本 | Tulamben | Zone-E1 |
| 京打马尼 | Kintamani | Zone-N1 |
| 巴图尔 | Mount Batur | Zone-N1 |
| 罗威纳 | Lovina | Zone-N1 |
| 塞库普 | Singaraja | Zone-N1 |
| 佩妮达 | Nusa Penida | Zone-OFF |
| 蓝梦岛 | Nusa Lembongan | Zone-OFF |
| 吉利群岛 | Gili Islands | Zone-OFF |

---

## Zone 产出说明

| 字段 | 说明 |
|------|------|
| Zone ID | 上述 Zone-S1/S2/C1/W1/E1/N1/OFF/未知 |
| region_en | 英文地区名（如 Ubud） |
| region_cn | 中文地区名（如 乌布） |
| gps_longitude | 经度（东经） |
| gps_latitude | 纬度（南纬） |

**注意**：Zone ID 用于内部系统分类，region_en/cn 用于展示，三个字段独立填写，不可混用。