# Image Sources Specification

> 图片来源规范：免费图库 API、选图规则与裁切指南。

---

## 三大免费图库

### 1. Pexels

| 项目 | 说明 |
|------|------|
| **网址** | https://www.pexels.com/api/ |
| **特点** | 支持中文搜索；通用/热门场景覆盖好 |
| **API** | `GET https://api.pexels.com/v1/search?query={keyword}&per_page=5` |
| **认证** | 需要 API Key（免费层：200 次/小时） |
| **备用** | 浏览 https://www.pexels.com/search/{keyword}/ |
| **版权** | 免费商用，无需署名（但建议署名） |

**API 调用示例：**

```bash
curl -H "Authorization: YOUR_API_KEY" \
  "https://api.pexels.com/v1/search?query=workspace&per_page=5"
```

**响应关键字段：**

```json
{
  "photos": [
    {
      "id": 12345,
      "width": 4000,
      "height": 6000,
      "src": {
        "original": "https://images.pexels.com/…",
        "large2x": "https://images.pexels.com/…?w=1600",
        "large": "https://images.pexels.com/…?w=940"
      },
      "alt": "workspace with laptop and coffee"
    }
  ]
}
```

---

### 2. Unsplash

| 项目 | 说明 |
|------|------|
| **网址** | https://unsplash.com/developers |
| **特点** | 摄影质量最高，尤其擅长人物/生活方式/空间 |
| **API** | `GET https://api.unsplash.com/search/photos?query={keyword}&per_page=5` |
| **认证** | 需要 API Key（免费层：50 次/小时） |
| **备用** | 浏览 https://unsplash.com/s/photos/{keyword} |
| **版权** | 免费商用，Unsplash License |

**API 调用示例：**

```bash
curl -H "Authorization: Client-ID YOUR_ACCESS_KEY" \
  "https://api.unsplash.com/search/photos?query=minimal+interior&per_page=5"
```

**响应关键字段：**

```json
{
  "results": [
    {
      "id": "abc123",
      "width": 5472,
      "height": 3648,
      "urls": {
        "raw": "https://images.unsplash.com/…",
        "full": "https://images.unsplash.com/…?w=2160",
        "regular": "https://images.unsplash.com/…?w=1080"
      },
      "alt_description": "minimal interior design",
      "user": { "name": "Photographer Name" }
    }
  ]
}
```

---

### 3. Wallhaven

| 项目 | 说明 |
|------|------|
| **网址** | https://wallhaven.cc/help/api |
| **特点** | 游戏、摄影、壁纸类内容丰富 |
| **API** | `GET https://wallhaven.cc/api/v1/search?q={keyword}&categories=111&purity=100` |
| **认证** | 免费，基础搜索无需 API Key |
| **备用** | 浏览 https://wallhaven.cc/search?q={keyword} |
| **版权** | 混合版权，商用优先选择 Pexels/Unsplash |

**API 调用示例：**

```bash
curl "https://wallhaven.cc/api/v1/search?q=nature&categories=111&purity=100&sorting=relevance"
```

**响应关键字段：**

```json
{
  "data": [
    {
      "id": "abc123",
      "width": 3840,
      "height": 2160,
      "path": "https://w.wallhaven.cc/full/abc123.jpg",
      "url": "https://wallhaven.cc/w/abc123",
      "category": "nature",
      "purity": "sfw"
    }
  ]
}
```

**参数说明：**

| 参数 | 值 | 说明 |
|------|---|------|
| `categories` | `111` | 三个数字分别代表 General/Anime/People，1=启用 |
| `purity` | `100` | 三个数字分别代表 SFW/Sketchy/NSFW，1=启用 |
| `sorting` | `relevance`, `random`, `date_added`, `views`, `favorites`, `toplist` | 排序方式 |

---

## 图片选择规则（Image Selection Rules）

### 优先级排序

```
1. 用户提供的图片（最真实，最无"AI 感"）
2. 免费图库搜索（匹配页面视觉角色，非泛泛装饰）
3. AI 生成图片（仅在确实增加价值时使用，通常 1-2 页）
```

### 选图原则

- **匹配视觉角色**：图片应服务于页面的视觉叙事，而非泛泛装饰
- **风格一致**：同一组卡片内图片风格应统一（色调、构图、氛围）
- **避免"AI 感"**：优先真实摄影，生成图片应自然、不夸张
- **生成图片限制**：不嵌入标题、页码、Logo 或虚假 UI 标签

### 尺寸与比例

| 规则 | 要求 |
|------|------|
| **比例匹配** | 图片比例必须匹配布局槽位（3:4 竖版、16:9 横版等） |
| **最小宽度** | 1600px（适配高 DPI 显示器） |
| **推荐宽度** | 2000-4000px |
| **格式** | 优先 JPEG（照片）、PNG（UI/截图） |

---

## 主体感知裁切（Subject-Aware Cropping）

始终根据照片主体位置设置 `object-position` 内联样式：

| 主体位置 | object-position | 典型场景 |
|---------|-----------------|---------|
| 主体偏上 | `center 25-35%` | 天空、建筑顶部、头部特写 |
| 主体居中 | `center 50%`（默认） | 居中构图、正面肖像 |
| 主体偏中下 | `center 55-65%` | 半身像、桌面物品 |
| 主体偏下/前景 | `center 70-80%` | 地面物品、低角度拍摄 |

**使用示例：**

```html
<!-- 人物半身照，主体偏中下 -->
<img src="…" style="object-fit:cover;object-position:center 60%">

<!-- 建筑照片，主体偏上 -->
<img src="…" style="object-fit:cover;object-position:center 30%">

<!-- 居中构图，默认 -->
<img src="…" style="object-fit:cover;object-position:center 50%">
```

### 裁切决策流程

```
1. 观察照片主体位置
   ↓
2. 选择对应的 object-position 范围
   ↓
3. 微调百分比确保主体完整可见
   ↓
4. 在目标比例下验证裁切效果
```

### 注意事项

- `object-fit:cover` 会裁切图片以填满容器，必须配合正确的 `object-position`
- `object-fit:contain` 保持完整但可能留白，适用于 UI 截图
- 人像裁切时避免切到面部关键区域（眼睛、嘴巴）
- 产品图裁切时确保产品主体完整可见

---

## Unsplash 直链下载（无需 API Key）

当 AI 生图 API 返回相同占位图时，使用 Unsplash 直链作为备选方案。

### 直链格式

```
https://images.unsplash.com/photo-{id}?w={width}&h={height}&fit=crop&auto=format&q={quality}
```

### 参数说明

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `w` | 1080 | 宽度（像素） |
| `h` | 1440 | 高度（像素，3:4比例） |
| `fit` | crop | 裁切模式 |
| `q` | 85 | JPEG质量（80-90） |

### 常用主题图片 ID

| 主题 | Photo ID | 描述 |
|------|----------|------|
| 深蓝科技抽象 | `1620712943543-bcc4688e7485` | 电路板/数据可视化风格 |
| 暗夜星空 | `1534796636912-3b95b3ab5986` | 深蓝星空/宇宙 |
| 极简办公 | `1497366216548-37526070297c` | 现代办公空间 |
| 城市天际线 | `1477959858617-67f85cf4f1df` | 城市夜景 |
| 自然纹理 | `1506905925346-21bda4d32df4` | 山脉/自然 |

### 下载方法

```javascript
// Node.js 下载（推荐，支持重定向跟踪）
const https = require('https');
const fs = require('fs');

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const follow = (u, redirects = 0) => {
      if (redirects > 10) return reject(new Error('Too many redirects'));
      https.get(u, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return follow(res.headers.location, redirects + 1);
        }
        const file = fs.createWriteStream(dest);
        res.pipe(file);
        file.on('finish', () => { file.close(); resolve(fs.statSync(dest).size); });
      }).on('error', reject);
    };
    follow(url);
  });
}
```

```bash
# curl 下载（需用 curl.exe 而非 PowerShell 的 curl 别名）
curl.exe -s -L -o "assets/cover.jpg" "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1080&h=1440&fit=crop&auto=format&q=85"
```

---

## AI 生图验证规则

### 问题：AI 生图 API 可能返回相同占位图

`trae-api-cn.mchost.guru` 的 `text_to_image` API 无论 prompt 如何不同，可能返回完全相同的占位图。两个不同的 CDN URL 不代表图片内容不同。

### 验证方法

```javascript
const fs = require('fs');
const b1 = fs.readFileSync('assets/cover.jpg');
const b2 = fs.readFileSync('assets/finale.jpg');

// 必须验证：两张图文件内容不同
if (b1.equals(b2)) {
  console.error('ERROR: cover.jpg and finale.jpg are identical!');
  console.error('AI image API returned same placeholder. Switch to Unsplash.');
  // 换用 Unsplash 直链下载
}
```

### 铁律

1. **下载多张图片后必须验证唯一性**：`buf1.equals(buf2) === false`
2. **如果两张图完全相同，立即换用 Unsplash**：不要反复重试 AI 生图 API
3. **禁止假设 URL 不同 = 内容不同**：CDN URL 的签名和路径不同不代表图片内容不同
4. **验证时机**：在 Step 3 Compose 组装 HTML 之前，确保所有图片文件已验证有效
