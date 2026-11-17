# 示例资产

## sample_corpus.json

收录 26 首代表性歌曲翻译样本，按语言-流派分组：

### 覆盖语种
English, French, German, Japanese, Korean, Russian, Spanish, Spanish / English, Spanish/English

### 覆盖流派
Anime OP/ED, Electro / Hip-Hop, Folk, French Chanson, German Pop / Neue Deutsche Welle, Hip-Hop, J-Pop, K-Pop, Latin Pop, Latin Urban, Pop, Pop/Folk, Pop/Soul, Rock, Russian Pop, Vocaloid, World Pop

### 数据结构
每首歌包含：
- 元信息：曲名、艺人、流派、语种、年份
- 前30行原文与译文预览（便于快速参考翻译风格）
- 来源 URL

### 用途
- 模型遇到陌生歌曲翻译时，可参考相似流派的样本
- 用户要求"按 XX 风格翻译"时，可对照样本调整

### 完整语料
完整 44 首歌曲的歌词翻译请参考：
`/home/z/my-project/download/lyrics_collection/all_songs.json`
