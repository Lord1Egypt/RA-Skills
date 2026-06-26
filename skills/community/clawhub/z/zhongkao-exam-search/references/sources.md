# 中考真题来源详细参考

## 来源1: 中考网 (zhongkao.com) — ⭐ 最可靠

### 网站结构
- 主站: https://www.zhongkao.com
- 移动版: https://m.zhongkao.com
- 地方站: https://{城市拼音}.zhongkao.com (如 cs.zhongkao.com = 长沙)

### 下载版页面
- **URL模式**: `m.zhongkao.com/e/{YYYYMMDD}/{随机ID}.shtml`
- **特征**: 页面底部有"下载完整版"按钮，指向 files.eduuu.com
- **搜索关键词**: `{城市} {科目} 真题 下载版 {年份}`

### 下载链接
- **URL模式**: `https://files.eduuu.com/ohr/{年}/{月}/{日}/{时间戳}_{hash}.{rar|zip}`
- **示例**: `https://files.eduuu.com/ohr/2021/06/22/174543_60d1b147d1e67.rar`
- **格式**: ZIP 或 RAR，内含 PDF/DOCX/PNG

### 图片版页面
- 当没有下载版时，中考网会提供图片版
- **URL模式**: 同下载版，但页面底部无"下载完整版"按钮
- **图片URL模式**: `https://files.eduuu.com/img/{年}/{月}/{日}/{文件名}.jpg`
- **分页**: 页面底部有 1 2 3 4... 分页链接

### 已知限制
- 2024年起部分省份（如湖南）全省统一命题，中考网可能只提供图片版而非下载版
- 地方站更新可能滞后
- 搜索功能需要中文编码

### 已验证的下载记录
| 年份 | 城市 | 科目 | 下载URL | 文件大小 | 格式 |
|------|------|------|---------|----------|------|
| 2021 | 长沙 | 英语 | files.eduuu.com/ohr/2021/06/22/174543_60d1b147d1e67.rar | 6.3MB | RAR→DOCX |
| 2022 | 长沙 | 英语 | files.eduuu.com/ohr/2022/06/29/... | 6.8MB | ZIP→PDF |
| 2023 | 长沙 | 英语 | files.eduuu.com/ohr/2023/07/02/153948_64a129c49cd43.zip | 2.3MB | ZIP→PNG×8 |
| 2024 | 长沙 | 英语 | 仅有图片版，无下载版ZIP | — | 图片版 |

---

## 来源2: 中学英语网 (trjlseng.com) — 英语专用

### 网站结构
- 主站: https://trjlseng.com
- 中考真题列表: https://trjlseng.com/zkst/
- 分页: https://trjlseng.com/zkst/list_{page}.html

### 下载链接
- **URL模式**: `https://trjlseng.com/uploads/ueditor/file/{日期}/{文件名}.zip`
- **示例**: `https://trjlseng.com/uploads/ueditor/file/20250703/1751534361398983.zip`
- **格式**: ZIP，内含 DOCX

### 已知限制
- 仅收录英语科目
- 可能需要注册登录才能下载（部分页面可直接下载）
- 更新可能滞后于中考时间

### 已验证的下载记录
| 年份 | 城市 | 科目 | 下载URL | 文件大小 | 格式 |
|------|------|------|---------|----------|------|
| 2025 | 长沙 | 英语 | trjlseng.com/uploads/ueditor/file/20250703/1751534361398983.zip | 1.2MB | ZIP→DOCX(含答案) |

---

## 来源3: 第一试卷网 (shijuan1.com) — 免费下载

### 网站结构
- 主站: https://www.shijuan1.com
- 中考英语分类: https://www.shijuan1.com/a/sjyyzk/
- 分页: https://www.shijuan1.com/a/sjyyzk/list_{分类ID}_{page}.html

### 下载链接
- **URL模式**: `https://www.shijuan1.com/uploads/soft/{分类}/{科目编码}/中考/{文件名}.rar`
- **格式**: RAR，内含 PDF/DOCX

### 科目分类编码
| 科目 | 编码 | 分类页URL |
|------|------|-----------|
| 语文 | sjywzk | /a/sjywzk/ |
| 数学 | sjshxzk | /a/sjshxzk/ |
| 英语 | sjyyzk | /a/sjyyzk/ |
| 物理 | sjwlzk | /a/sjwlzk/ |
| 化学 | sjhxzk | /a/sjhxzk/ |
| 历史 | sjlszk | /a/sjlszk/ |
| 道法 | sjzzzk | /a/sjzzzk/ |
| 生物 | sjswwk | /a/sjswwk/ |
| 地理 | sjdlzk | /a/sjdlzk/ |

### 已知限制
- 按省份拼音排序分页，需逐页查找
- 搜索功能可能返回404
- 更新可能滞后

---

## 来源4: 中学学科网 (zxzyw.cn)

### 特点
- 覆盖面较广，各科都有
- 部分资源免费，部分需积分
- URL模式: `https://www.zxzyw.cn/{科目分类}/{文件ID}.html`

---

## 来源5: 无忧考网 (51test.net)

### 特点
- 有Word版和PDF版
- Word版通常需要VIP
- 页面URL模式: `https://www.51test.net/show/{ID}.html`
- 可获取页面文本内容（非VIP也能看部分）

---

## 社交媒体来源

### 小红书
- 搜索关键词: `{城市}{年份}中考{科目}真题 PDF` 或 `{城市}{年份}中考{科目}真题 网盘`
- 可能有夸克/百度/阿里云盘链接
- 使用小红书Skill的 `search.sh` 搜索

### 微信公众号
- 搜索: `{城市}中考{科目}真题 含答案`
- 常有百度网盘分享，但链接可能过期
- 使用 wechat-article-search Skill 搜索

### 知乎
- 搜索: `{年份}全国中考真题汇总`
- 可能有合集网盘链接

---

## 付费来源（最后备选）

| 网站 | URL | 资源质量 | 价格 |
|------|-----|----------|------|
| 学科网 | zxxk.com | 最全 | VIP 30元/月起 |
| 21世纪教育网 | 21cnjy.com | 较全 | VIP 20元/月起 |
| 百度文库 | wenku.baidu.com | 一般 | VIP 15元/月 |
| 道客巴巴 | doc88.com | 一般 | 需积分 |
| 原创力文档 | book118.com | 较好 | 需积分 |
