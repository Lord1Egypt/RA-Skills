# WeChat Article Generator Skill

自动生成微信公众号文章并上传到草稿箱。

## 设计规范

### 色彩规范
- **小标题**: 绿色 `#07c160`，带左边框
- **正文**: 黑色 `#333`
- **重点词**: 加粗 `<strong>`，不使用额外颜色
- **禁用**: emoji、花里胡哨的背景色、多种颜色混用

### 排版规范
- 简洁专业，避免过度设计
- 列表使用 `·` 或数字，不使用 emoji
- 引用居中斜体，不使用彩色背景
- 标签统一绿色圆角

## 使用方法

```bash
# 生成文章并上传
./wechat-article.sh <input.md> <title> [author] [thumb_media_id]

# 示例
./wechat-article.sh article.md "文章标题" "超哥" --upload
```

## 支持的 Markdown 语法

```markdown
# 一级标题 → 绿色小标题带边框
## 二级标题 → 加粗小标题
### 三级标题 → 普通加粗

- 列表项 → · 列表项
* 列表项 → · 列表项
1. 列表项 → 1. 列表项

> 引用 → 居中斜体引用框

**强调** → <strong>强调</strong>（黑色加粗）
*斜体* → <em>斜体</em>

普通段落 → 黑色正文
```

## 配置

在 `config.json` 中配置：

```json
{
  "appid": "your_appid",
  "appsecret": "your_appsecret",
  "default_author": "超哥",
  "style": {
    "primary_color": "#07c160",
    "text_color": "#333"
  },
  "formatting_rules": {
    "use_emoji": false,
    "max_colors": 2
  }
}
```

## 文件结构

```
skills/wechat-article/
├── SKILL.md              # 本文件
├── wechat-article.sh     # 主脚本
├── template.html         # 文章模板（简洁版）
├── config.json           # 配置文件
└── lib/
    └── wechat-api.sh     # 微信API封装
```

## 依赖

- curl
- jq
- sed/awk

## 版本

v1.1.0 - 更新为简洁专业风格，移除emoji，统一色彩
