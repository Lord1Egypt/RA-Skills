# 图文公众号发布流程

## 功能
将文案+配图一键发布到微信公众号草稿箱

## 核心特点
- **灵活性**：配图不限定类型，支持任意图片
- **多种生图方式**：MakeContents HTML渲染 / MiniMax生图 / 固定模板
- **完整流程**：文案→配图→上传微信→创建草稿→后台发布

---

## ⚠️ 关键易错点：图片必须先上传微信素材库

**文章内容里用的图片URL必须是微信素材库的URL（mmbiz.qpic.cn开头）**

**不能用：**
- MakeContents临时路径（/app/uploads/rendered/xxx）
- 外链图片URL
- 本地文件路径

**正确流程：**
1. 生成图片 → 下载到本地
2. 上传到微信素材库 → 获得mmbiz.qpic.cn的URL
3. 用微信返回的URL拼接到文章HTML里

**漏了这个步骤，图片在文章里会显示不出来！**

---

## 第一部分：文案准备

用户提供：
- 文章主题/标题
- 文章内容（可以是大纲或完整文案）
- 配图需求（几张、什么类型）

---

## 第二部分：配图生成

### 方式A：MakeContents封面图（固定接口）
适合：封面/缩略图
```bash
curl -s -X POST "http://localhost:3710/api/content/render" \
  -H "Content-Type: application/json" \
  -d '{"cover_word":"标签","cover_title":"标题","cover_description":"描述","cover_emoji":"🤖"}'
```

### 方式B：MakeContents HTML长图（灵活模板）
适合：详情页、工具展示、数据对比、步骤说明等任意图

**生成步骤：**
1. 写HTML内容（可自定义CSS样式）
2. 调用render-text接口转图片

```bash
# 1. 生成HTML文件
cat > /tmp/custom_image.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: #f5f5f7;
  padding: 40px 20px;
}
.title {
  font-size: 28px;
  font-weight: bold;
  color: #1a1a1a;
  text-align: center;
  margin-bottom: 20px;
}
/* 自定义内容样式 */
</style>
</head>
<body>
<div class="title">你的标题</div>
<!-- 自定义内容 -->
</body>
</html>
EOF

# 2. 转图片（width=750适合手机，height按需调整）
HTML=$(cat /tmp/custom_image.html | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
curl -s -X POST "http://localhost:3710/api/content/render-text" \
  -H "Content-Type: application/json" \
  -d "{\"html\":$HTML,\"width\":750,\"height\":1200}"
```

### 方式C：MiniMax图片生成
适合：需要AI创意生成的配图（产品图、场景图、插画等）

```bash
# 使用mmx CLI
mmx image generate --prompt "描述" --aspect-ratio 16:9 --output /tmp/gen_image.png
```

### 常用Twemoji Emoji（用于HTML模板中）
格式：`https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/{code}.png`

| Emoji | Code |
|-------|------|
| 🤖 | 1f916 |
| 🎨 | 1f3a8 |
| 📊 | 1f4ca |
| 🎙️ | 1f3a4 |
| 📡 | 1f4e2 |
| ✅ | 2705 |
| ❌ | 274c |
| ⚠️ | 26a0 |
| 💡 | 1f4a1 |
| 🚀 | 1f680 |
| ⭐ | 2b50 |
| 🔥 | 1f525 |

emoji转code方法：`python3 -c "print(hex(ord('🤖'))[2:])"` → `1f916`

---

## 第三部分：从容器下载图片

```bash
# 封面图
docker cp autocontents-makecontents-1:/app/uploads/rendered/{session_id}_cover.png /tmp/cover.png

# 长图
docker cp autocontents-makecontents-1:/app/uploads/rendered/{session_id}_text.png /tmp/detail.png

# 复制到workspace（可选）
cp /tmp/cover.png /home/success/.openclaw/workspace/
cp /tmp/detail.png /home/success/.openclaw/workspace/
```

---

## 第四部分：微信API上传

### 凭证
```bash
# 获取Access Token
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=YOUR_APPID&secret=YOUR_SECRET"
```
返回值中的access_token有效期2小时

### 上传图片到素材库（永久素材）
```bash
ACCESS_TOKEN="获取到的token"

# 封面图
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$ACCESS_TOKEN&type=image" \
  -F "media=@/tmp/cover.png"

# 详情图
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$ACCESS_TOKEN&type=image" \
  -F "media=@/tmp/detail.png"
```

返回格式：`{"media_id":"xxx","url":"http://mmbiz.qpic.cn/..."}`

### 上传缩略图（用于文章thumb_media_id）
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=$ACCESS_TOKEN&type=thumb" \
  -F "media=@/tmp/cover.png"
```
返回的media_id用于文章配置的thumb_media_id字段

---

## 第五部分：创建图文草稿

**⚠️ 文章内容中的图片URL必须用微信素材库的mmbiz.qpic.cn URL！**

```bash
cat > /tmp/article.json << 'EOF'
{
  "articles": [{
    "thumb_media_id": "上一步获取的thumb media_id",
    "title": "文章标题",
    "author": "",
    "digest": "文章摘要",
    "show_cover_pic": 1,
    "content": "HTML格式的文章内容，图片URL用微信素材库的URL",
    "content_source_url": ""
  }]
}
EOF

curl -s -X POST "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=$ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @/tmp/article.json
```

---

## 第六部分：发布

### API发布（服务号可用）
```bash
curl -s -X POST "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=$ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"media_id":"草稿media_id","pub_choose_type":1}'
```

### 手动发布（个人订阅号）
- 登录 mp.weixin.qq.com
- 内容与互动 → 草稿箱
- 找到文章 → 发布

---

## 常用模板参考

### 详情页长图模板
路径：`skills/auto-contents/references/templates/detail-page-gray.html`

### 工具栈图模板
路径：`skills/auto-contents/references/templates/tool-stack.html`

### 数据对比图模板（可直接用）
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:#f5f5f7;padding:30px 20px}
.title{font-size:22px;font-weight:bold;color:#1a1a1a;margin-bottom:20px;text-align:center}
.section{margin-bottom:24px}
.section-title{font-size:16px;font-weight:bold;margin-bottom:10px;padding-left:8px}
.green{border-left:4px solid #4CAF50}
.red{border-left:4px solid #f44336}
.items{display:flex;flex-direction:column;gap:8px}
.item{display:flex;gap:8px;font-size:14px;color:#333}
.check{color:#4CAF50}.cross{color:#f44336}
</style>
</head>
<body>
<div class="title">标题</div>
<div class="section green">
<div class="section-title">✅ 能做的</div>
<div class="items"><div class="item"><span class="check">✓</span>内容1</div></div>
</div>
<div class="section red">
<div class="section-title">❌ 不能做的</div>
<div class="items"><div class="item"><span class="cross">✗</span>内容1</div></div>
</div>
</body>
</html>
```

---

## 注意事项

### IP白名单
微信API需要IP在白名单内，当前IP：`14.218.121.191`

### 图片URL（重要！）
- 草稿中的图片URL必须用微信返回的永久素材URL（mmbiz.qpic.cn）
- 不能用MakeContents临时路径、外链、本地路径
- 每张要放进文章的图都必须先上传微信素材库

### 个人订阅号限制
- API创建草稿：✅
- API发布：❌（需手动发布）
- 上传素材：✅
