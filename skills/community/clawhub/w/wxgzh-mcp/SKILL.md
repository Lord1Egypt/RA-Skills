---
name: wxgzh-mcp
description: 微信公众号草稿创建与管理技能，支持图片上传、创建草稿、发布等操作。需配置 AppID、AppSecret、白名单 IP。
---

# wxgzh-mcp · 微信公众号草稿管理技能

## 功能列表

| 工具 | 说明 |
|------|------|
| `get_access_token` | 获取 Access Token |
| `upload_thumb` | 上传封面图 |
| `upload_image` | 上传正文图片 |
| `create_draft` | 创建草稿文章 |
| `list_drafts` | 获取草稿列表 |
| `delete_draft` | 删除草稿 |
| `publish_draft` | 发布草稿（需认证账号） |

## 文件结构

```
wxgzh-mcp/
├── SKILL.md              # 本说明文件
├── README.md             # 详细使用指南
├── config.json           # 配置文件（用户填写）
├── src/
│   ├── main.py           # 技能入口
│   ├── config.py         # 配置管理
│   ├── wechat_api.py     # 微信 API 封装
│   └── tools/
│       ├── token.py      # Token 工具
│       ├── media.py      # 媒体上传工具
│       └── draft.py       # 草稿管理工具
├── docker-compose.yml     # Docker 部署
└── requirements.txt       # Python 依赖
```

## 快速开始

### 第一步：配置白名单

本机 IP（用于 API 调用）需要加入微信公众号白名单。

**查询本机 IP：**
访问 https://api.ipify.org 或联系管理员获取。

**添加白名单：**
1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 设置与开发 → 基本配置
3. IP 白名单 → 添加 IP

### 第二步：填写配置

在 `config.json` 中填入你的公众号信息：

```json
{
  "app_id": "wx1234567890abcdef",
  "app_secret": "你的AppSecret",
  "proxy": null
}
```

### 第三步：安装依赖并测试

```bash
cd wxgzh-mcp
pip install -r requirements.txt

# 测试 Token 获取
python -c "from src.wechat_api import WeChatAPI; api = WeChatAPI(); print(api.get_access_token())"
```

### 第四步：创建草稿

```python
from src.wechat_api import WeChatAPI

api = WeChatAPI()

# 上传封面图（需先准备图片）
thumb_result = api.upload_thumb("封面图路径.jpg")
thumb_media_id = thumb_result["media_id"]

# 创建草稿
result = api.add_draft(
    title="文章标题",
    content="<p>正文内容 HTML</p>",
    author="作者名",
    thumb_media_id=thumb_media_id,
    digest="摘要"
)

draft_media_id = result["media_id"]
print(f"草稿创建成功: {draft_media_id}")
```

## 常见问题

### 错误 40164：IP 不在白名单
- 解决方案：参见第一步「配置白名单」

### 错误 45003：标题/作者超出限制
- 标题最多 64 字符
- 作者最多 8 字符

### 错误 48001：API 未授权
- 个人订阅号无法使用群发 API
- 草稿功能正常，可手动发布

## 注意事项

- Access Token 有效期 2 小时，模块自动缓存
- 图片格式支持 JPG、PNG，大小限制 2MB
- 封面图必须先上传获取 media_id 才能创建草稿
