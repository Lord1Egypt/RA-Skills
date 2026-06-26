# Basic Usage

## Simple Text to Card

Convert a short Markdown text into a single XHS card image.

### Input

```json
{
  "markdown": "## 今日好物推荐\n\n**无线降噪耳机** 🎧\n\n- 主动降噪，隔绝噪音\n- 30小时续航\n- 佩戴舒适，轻若无物\n\n> 戴上它，世界都安静了 ✨",
  "theme": "sakura",
  "bg_style": "none"
}
```

### Output

Single card image (1125x1500px) with sakura pink theme, no AI background.

## With Auto Title Extraction

Omit the `title` field and let the LLM extract one from content.

### Input

```json
{
  "markdown": "最近发现了一个超好用的学习方法！费曼学习法真的太强了，简单来说就是：学完一个知识点后，试着用最简单的语言教给别人。如果你能讲清楚，说明你真的懂了。\n\n具体步骤：\n1. 选择一个概念\n2. 用简单语言解释\n3. 找出卡住的地方\n4. 回去重新学习\n\n坚持一个月，学习效率提升了50%！"
}
```

The LLM will:
1. Extract a title like "费曼学习法，效率翻倍"
2. Format the body with headings, bold text, and lists
3. Render with the default white theme and AI art background

## With Custom Author

```json
{
  "markdown": "## 周末早午餐食谱\n\n**法式吐司** 🍞\n\n- 全麦面包 2片\n- 鸡蛋 1个\n- 牛奶 50ml\n- 肉桂粉少许\n\n中火煎至两面金黄，撒上糖粉，配上新鲜水果 🍓",
  "title": "周末早午餐",
  "author": "美食小厨",
  "theme": "mint"
}
```
