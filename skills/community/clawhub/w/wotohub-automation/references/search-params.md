# 搜索参数参考

## 博客语言 `blogLangs`

完整语言列表见：`references/language-mapping.md` / `references/language-source.json`

常用映射示例：

| 用户输入 | dictCode | 英文名 |
|---|---|---|
| 英语 / English | en | English |
| 西班牙语 / Spanish | es | Spanish |
| 葡萄牙语 / Portuguese | pt | Portuguese |
| 越南语 / Vietnamese | vi | Vietnamese |
| 日语 / Japanese / jp | ja | Japanese |
| 韩语 / Korean / kr | ko | Korean |
| 德语 / German | de | German |
| 法语 / French | fr | French |
| 中文 / 简体中文 / 中文简体 / 简中 | zh-cn | Chinese (Simplified) |
| 繁体中文 / 中文繁体 / 繁中 | zh-tw | Chinese (Traditional) |
| 俄语 / Russian | ru | Russian |
| 阿拉伯语 / Arabic | ar | Arabic |
| 土耳其语 / Turkish | tr | Turkish |
| 菲律宾语 / Tagalog / Filipino | tl | Tagalog |

## 关键词参数

推荐主路径：使用 `advancedKeywordList`，不要把 `keywordList` 作为当前 skill 的主搜索字段。

```json
{
  "searchType": "KEYWORD",
  "advancedKeywordList": [
    {"value": "关键词", "exclude": false},
    {"value": "排除词", "exclude": true}
  ]
}
```

规则：
- 用户没有提关键词时，不填 `advancedKeywordList`
- 当前 skill 的关键词主路径统一使用 `advancedKeywordList`
- 分类主路径统一使用 `blogCateIds`
- `keywordList` / `keywordLogicalOperator` / `keywordRange` 不作为当前 skill 的默认主逻辑

## 观看量组合 `viewVolumeCombination`

```json
{"min": 2000, "type": "AVG", "excludeTop": false, "range": "D60"}
```

可选：
- `type`: `AVG` / `MEDIAN`
- `range`: `D60` / `D30` / `D15`

## 排序类型 `searchSort`

- `FANS_NUM` - 粉丝量
- `VIEW_AVG` - 平均观看量
- `INTERACTIVE_RATE` - 平均互动率
- `TOTAL_STAR` - 卧兔评分
- `SOLD_COUNT_30D` - 近30天销量
- `GMV_30D` - 近30天销售额
- `PROD_VIDEO_CNT_30D` - 带货视频数
