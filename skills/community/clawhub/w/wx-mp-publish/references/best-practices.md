# 微信公众号发布最佳实践

## 技术方案对比

| 方案 | JSON 解析 | HTML 转换 | 推荐 |
|------|----------|-----------|------|
| Python + markdown 库 | ❌ 编码问题，`Invalid \uXXXX escape` | ⚠️ nl2br 有问题 | 不推荐 |
| Node.js + marked | ✅ V8 原生，稳定 | ✅ gfm + 内联样式 | **推荐** |

### Python JSON 编码问题根源

微信 API 返回的 JSON 中含特殊字符（如 emoji、特殊 Unicode），Python 3 的 `json.loads()` 在某些 Linux 发行版（尤其中文环境）对 `\uXXXX` 转义序列处理不一致，导致静默解析失败，返回空 dict 或垃圾数据。

**现象**：Python 脚本显示"草稿列表"里有内容，但全是 `1970-01-01`、`(无标题)` 的垃圾数据——因为实际返回的 JSON 解析失败了。

**解法**：换 Node.js，V8 原生支持所有 Unicode，无此问题。

## Markdown → HTML 转换

### 工具：marked + 内联样式

```js
const { marked } = require('marked');
marked.setOptions({ breaks: false, gfm: true });

let html = marked.parse(markdownContent);
html = applyInlineStyles(html); // 内联 style 替换
```

### 内联样式说明

微信编辑器不支持外部 CSS，必须把所有样式内联。关键样式：

| 元素 | 样式 |
|------|------|
| h1 | 居中，24px，加粗，主题蓝 |
| h2 | 左侧下划线边框，主题蓝 |
| p | 15px，行高1.8 |
| blockquote | 左侧蓝色边框，灰色背景 |
| code_inline | 粉红背景，等宽字体 |
| code_block | 深灰背景，彩色代码 |
| img | max-width:100% |

### YAML Frontmatter 必须去除

```python
# Python
import re
content = re.sub(r'^---\n[\s\S]*?\n---\n', '', content, count=1, flags=re.DOTALL)

# Node.js
content = content.replace(/^---\n[\s\S]*?\n---\n/, '');
```

不去除会显示为正文乱码。

### 不要用 nl2br

`nl2br` 扩展把单个换行 `\n` 转成 `<br>`，但这是裸标签，微信编辑器无法识别段落边界，导致换行失效。

正确做法是 paragraph 自然闭合，不额外插入 `<br>`。

## 账号类型与权限

| 账号类型 | API 创建草稿 | API 直接发布 | 手动发布 |
|----------|-------------|-------------|---------|
| 服务号（已认证） | ✅ | ✅ | ✅ |
| 订阅号（已认证） | ✅ | ✅ | ✅ |
| 订阅号（审核中/个人） | ✅ | ❌ 48001 | ✅ |

## API 路径注意事项

微信 API 路径必须带 `/cgi-bin` 前缀：

```
错误：/draft/add?access_token=xxx
正确：/cgi-bin/draft/add?access_token=xxx
```

缺少前缀返回 404。

## 封面图要求

- **格式**：jpg / png
- **大小**：≤64KB
- **建议尺寸**：900×383 像素（2.35:1 宽屏）

已配置的封面图 media_id：
- Q版封面1-龙虾诞生（默认封面）：`A83aYO34D2tkzY601CqYd0X8h93oGFMds-XsUsKvziXKSpH8A-FiMvQ2yg_hkMAd`

## 常见错误速查

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 48001 | API 无发布权限 | 创建草稿后手动发布 |
| 45003 | 标题超长 | 缩短到 64 字符内 |
| 45004 | 摘要超长 | 缩短到 120 字符内 |
| 40001 | token 无效/过期 | 删除 `~/.config/wx-mp/.token_cache.json` 重新获取 |
| Invalid \uXXXX | Python JSON 解析失败 | 换 Node.js 方案 |
| 404 | API 路径缺少 /cgi-bin | 检查路径拼接 |
| Raw response length: 0 | httpReq port=443 未固定 | 微信 API 固定走 HTTPS 443 端口 |

## 发布前检查清单

- [ ] 标题 ≤64 字符
- [ ] 摘要 ≤120 字符（或留空）
- [ ] 封面图 ≤64KB
- [ ] 正文已去除 YAML frontmatter
- [ ] 草稿创建成功（media_id 非空）
- [ ] HTML 转换正确（h1/h2/p/blockquote 等标签正确）
