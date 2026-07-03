# 环境变量配置说明

配置文件：`scripts/skill.env`，每行格式 `KEY=VALUE`，无需引号。

---

## MPTEXT_API_KEY（mptext API 密钥）

### 获取地址
```
https://down.mptext.top/dashboard/api
```
注册后可在 API 页面生成密钥，有效期 4 天（会话级）。

> ⚠️ 注意：本副本使用 down.mptext.top 作为 API 域名。原始版使用 wechat.faiz-world.com。

### 配置方式
```
MPTEXT_API_KEY=你的密钥
```

### 用途
mptext API 的所有接口均需此 key：
- `search_account` — 搜索公众号
- `get_articles` — 获取文章列表
- `download_article` — 下载文章正文
- `get_author_info` — 查询公众号主体信息

---

## Cookie（微信公众平台 Cookie）

> Cookie 方案为备用方案，大部分场景用 mptext API 即可覆盖。

### 获取方式（推荐：Cookie-Editor 插件）

1. 安装浏览器插件 **Cookie-Editor**（Chrome/Edge 扩展商店有）
2. 登录微信公众平台 `https://mp.weixin.qq.com/`
3. 点击 Cookie-Editor 插件图标 → **Export** → 导出为 JSON
4. 将 JSON 内容发给 agent，说明写入 `scripts/skill.env`

> agent 会将 JSON 转为 `cookie=***` 格式写入配置文件。

### 配置方式

```
cookie=你的cookie值
token=你的token值
```

### 用途
- 公众号文章列表（原生 API）
- 按 biz 查询公众号信息
- 获取文章互动数据（阅读/点赞/评论）

### Cookie 失效表现
- token 获取返回 ret≠0
- 搜索返回空列表
- 修复：重新登录微信公众平台，重新获取 Cookie