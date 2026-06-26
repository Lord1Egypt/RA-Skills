# 数据格式说明

## JSON 数据文件

路径：`today_combined_spaded.json`

每条资讯为 6 字段数组：

| 索引 | 字段 | 说明 | 示例 |
|------|------|------|------|
| 0 | key | 唯一标识（英文） | `bigme_inkphone` |
| 1 | cat_id | 板块 ID（1-5） | `1` |
| 2 | title | 标题 | `Bigme 大我官宣全球首款彩色墨水屏+OLED双屏手机...` |
| 3 | src | 来源名称 | `IT之家`、`快科技` |
| 4 | url | 文章链接 | `https://www.ithome.com/0/935/476.htm` |
| 5 | text | 正文摘要（完整） | 完整段落文字... |

## 板块分类

| cat_id | 板块名称 |
|--------|---------|
| 1 | 📱 手机/硬件 |
| 2 | 🤖 AI/大模型 |
| 3 | 🚗 汽车 |
| 4 | 🏢 科技大厂 |
| 5 | 💻 系统/App |

## 空格处理规则

CJK（中文/日文/韩文）与 ASCII（英文/数字）之间必须加空格：

```python
def add_space(s):
    s = re.sub(r'([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])([A-Za-z0-9])', r'\1 \2', s)
    s = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', r'\1 \2', s)
    return s
```

示例：
- `+OLED` → `+ OLED`
- `288Hz 高刷` → `288Hz 高刷`
- `3799 元` → `3799 元`

## 图片目录

路径：`news_imgs_today/`

命名：`{key}.jpg` 或 `{key}.png`

图片以 base64 编码内嵌到 HTML img 标签：
```html
<img class="card-img" src="data:image/jpeg;base64,...">
```
