# wxgzh-mcp

微信公众号草稿管理 MCP 服务，支持通过自然语言或代码创建、发布公众号文章。

## 功能特性

- ✅ 获取 Access Token（自动缓存）
- ✅ 上传封面图获取 media_id
- ✅ 上传正文图片
- ✅ 创建草稿文章
- ✅ 查看草稿列表
- ✅ 删除草稿
- ✅ 发布草稿（需认证账号）

## 环境要求

- Python 3.11+
- 微信公众号账号（订阅号/服务号）

## 部署步骤

### 1. 配置白名单

**查询本机公网 IP：**
```bash
curl https://api.ipify.org
```

将返回的 IP 地址添加到微信公众号白名单：
1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入 **设置与开发 → 基本配置**
3. 点击 **IP白名单** → **修改**
4. 添加你的公网 IP
5. 保存

### 2. 获取公众号凭证

登录微信公众平台，进入 **设置与开发 → 基本配置**：

| 字段 | 获取位置 |
|------|---------|
| AppID | 基本配置页面 |
| AppSecret | 基本配置页面（需点击查看） |
| 公众号 ID | 设置 → 公众号信息 → 原始 ID |

### 3. 填写配置文件

复制并编辑 `config.json`：

```bash
cp config.json.example config.json
```

填入你的信息：

```json
{
  "app_id": "wx1234567890abcdef",
  "app_secret": "你的AppSecret",
  "proxy": null
}
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 测试连接

```bash
python -c "
from src.wechat_api import WeChatAPI
api = WeChatAPI()
token = api.get_access_token()
print(f'Token 获取成功: {token[:20]}...')
"
```

## 使用示例

### 创建草稿

```python
from src.wechat_api import WeChatAPI

api = WeChatAPI()

# 上传封面图
thumb = api.upload_thumb("cover.jpg")
print(f"封面 media_id: {thumb['media_id']}")

# 创建草稿
draft = api.add_draft(
    title="文章标题",
    content="<p>正文内容，支持 HTML 格式</p>",
    author="作者",
    thumb_media_id=thumb["media_id"],
    digest="摘要说明"
)
print(f"草稿 media_id: {draft['media_id']}")
```

### 查看草稿列表

```python
from src.wechat_api import WeChatAPI

api = WeChatAPI()
drafts = api.get_draft_list(offset=0, count=10)
print(f"共有 {drafts['total']} 篇草稿")

for draft in drafts["item"]:
    media_id = draft["media_id"]
    update_time = draft["update_time"]
    print(f"草稿ID: {media_id}, 更新时间: {update_time}")
```

### 删除草稿

```python
from src.wechat_api import WeChatAPI

api = WeChatAPI()
api.delete_draft("草稿media_id")
print("删除成功")
```

## API 参考

### WeChatAPI 类

```python
class WeChatAPI:
    def __init__(self, app_id=None, app_secret=None, proxy=None)
    def get_access_token(self, force_refresh=False) -> str
    def upload_image(self, image_path: str) -> dict
    def upload_thumb(self, thumb_path: str) -> str  # 返回 media_id
    def add_draft(self, title, content, author=None, thumb_media_id=None, digest=None) -> dict
    def get_draft_list(self, offset=0, count=20) -> list
    def get_draft_count(self) -> int
    def delete_draft(self, media_id) -> dict
    def publish_draft(self, media_id) -> dict  # 需认证账号
```

## 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 40001 | AppSecret 错误 | 检查 config.json 中的 AppSecret |
| 40164 | IP 不在白名单 | 添加本机 IP 到白名单 |
| 45003 | 标题/作者超长 | 减少字符数 |
| 48001 | API 未授权 | 个人订阅号不支持群发 API |

## 发布文章流程

1. 使用 `upload_thumb` 上传封面图，获取 `media_id`
2. 使用 `create_draft` 创建草稿
3. 登录微信公众平台 → 草稿箱 → 编辑 → 群发

## 认证与限制

| 账号类型 | 草稿创建 | 自动发布 |
|---------|---------|---------|
| 个人订阅号 | ✅ | ❌ 需手动群发 |
| 企业订阅号（认证） | ✅ | ✅ |
| 服务号 | ✅ | ✅ |

## 技术栈

- Python 3.11+
- requests（HTTP 客户端）
- json5（配置文件解析）

## License

MIT
