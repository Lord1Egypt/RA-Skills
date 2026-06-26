# HTML 生成防乱码规范

## 核心规则（必须遵守）

1. **绝对不用 Python f-string 直接写大段中文 HTML** — Python f-string 会把中文字符转成 `&#XXXXX;` 实体导致乱码
2. **正确方式：** 先写好 UTF-8 模板文件，再用 `str.replace()` 做精确替换
3. 写文件时指定 `encoding='utf-8'`
4. 不使用 Emoji（用 Unicode 符号替代）：`&#9650;` ▲、`&#9733;` ★、`&#9670;` ◆、`&#9654;` ►、`&#9660;` ▼

## 字体规范

```css
font-family: "PingFang SC","Microsoft YaHei","Helvetica Neue",Arial,sans-serif;
```

SVG `<text>` 元素必须内联 `font-family` 属性：
```xml
<text font-family="PingFang SC,Microsoft YaHei,Arial,sans-serif">文字</text>
```

## 列表布局规范

禁止 `::before` 伪元素做项目符号，改用 flex：

```html
<ul class="note-list">
  <li><span class="dot">&#9654;</span><span>内容文字</span></li>
</ul>

<style>
ul.note-list { list-style:none; padding:0; display:flex; flex-direction:column; gap:4px; }
ul.note-list li { display:flex; align-items:flex-start; gap:5px; }
</style>
```

## 图片嵌入（笔记封面）

图片用 base64 内嵌，flex 布局并排文字。注意：插入图片时必须关闭 flex 容器：

```html
<div class="note-box">
  <div style="display:flex;align-items:flex-start;">
    <img src="data:image/jpeg;base64,{b64}" style="width:78px;height:104px;object-fit:cover;border-radius:6px;flex-shrink:0;margin-right:10px;" alt="封面"/>
    <div style="flex:1;">
      <div class="note-ttl">素材标题</div>
      <ul class="note-list">...</ul>
    </div>        <!-- 关闭 flex:1 内层 -->
  </div>          <!-- 关闭 flex 外层 -->
</div>
```

**常见错误：** 忘记关闭 `</div></div>`，导致 TOP2 内容跑进 flex 容器里排版错乱。

## HTML 插入/替换方式

```python
# 正确：读取已有 UTF-8 文件，用 str.replace 做精确替换
with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('旧内容', '新内容', 1)  # 第3个参数限制替换次数，防止误替换

with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)
```
