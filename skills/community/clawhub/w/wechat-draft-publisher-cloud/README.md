# wechat-draft-publisher-cloud（skill）

把 **markdown 文章 + 封面图** 推到 **公众号草稿箱** 的客户端 skill。需配合部署在微信云托管的草稿代理服务端（利用官方「开放接口服务」免鉴权调用公众号接口），访问地址与密钥通过环境变量或 `config.json` 注入，本 skill 不硬编码。

本 skill 是**单独一个项目发布**，便于上架到 skill 官方仓库、独立安装。

## 配套项目（relay 服务端）

本 skill 只是客户端；真正调用公众号接口的是部署在微信云托管的 relay 服务端：[shinchen6/wechat-draft-relay](https://github.com/shinchen6/wechat-draft-relay)。自行部署后，把它的访问地址与密钥注入本 skill 即可（见下方「配置」）。

> **零三方依赖**：`scripts/publish_script.py` 只用 Python 标准库（`urllib` + `base64` + `json`）发请求；Markdown -> 微信图文 HTML 的转换也用标准库在本地完成（`scripts/md2wechat.py`）。只要环境有 Python 3.8+ 即可直接跑，无需 `pip install` 任何东西。

## 安装

方式一（从 skill 官方仓库）：在客户端执行安装 `wechat-draft-publisher-cloud` 即可。

方式二（手动）：把本目录复制到技能目录，例如：

```bash
# WorkBuddy
cp -r wechat-draft-publisher-cloud ~/.workbuddy/skills/wechat-draft-publisher-cloud

# 或放到你的私有 skills 目录
cp -r wechat-draft-publisher-cloud <你的 skills 根>/wechat-draft-publisher-cloud
```

## 配置（注入访问地址 + 访问密钥）

relay 跑在云托管，默认公网地址是平台生成的**默认域名**（任何人可访问），因此必须靠「访问密钥」保护。本 skill 按优先级解析 **URL** 与 **KEY**：

1. **命令行** `--cloud-url` / `--cloud-key`
2. **环境变量**（推荐）：
   - `WECHAT_DRAFT_RELAY_URL` / `WECHAT_DRAFT_RELAY_KEY`
   - 兼容旧名 `DRAFT_CLOUD_URL` / `DRAFT_API_KEY`
3. **config.json**（放在 `scripts/` 目录，已被 `.gitignore` 忽略）：
   ```json
   { "relay_url": "https://<服务名>.<地域>.run.tcloudbase.com", "relay_key": "你的 RELAY_API_KEY" }
   ```

复制 `scripts/config.example.json` 为 `scripts/config.json` 填入即可。发布版**不硬编码**任何个人地址/密钥。

> relay 地址在哪看：微信云托管控制台 → 你的服务 → 服务详情 → **默认公网访问地址**。
> relay 密钥：部署 relay 时设置的 `RELAY_API_KEY` 环境变量。

## 使用

```bash
# dry-run（默认，只本地转 HTML + 校验，不真发）
python scripts/publish_script.py --article X.md --cover Y.png --titles-md T.md

# 真发
python scripts/publish_script.py --real --article X.md --cover Y.png --titles-md T.md
```

正文插图：在 `article.md` 写 `![](img/body1.png)`，脚本本地转 HTML 时自动经 relay 上传素材库替换。

## 删除草稿

草稿箱会累积（每次 `--real` 都新增一篇、不覆盖）。清理旧草稿：

```bash
# 单个删除（默认 dry-run 只列出，--real 才真删）
python scripts/publish_script.py --delete <media_id> --real

# 批量删除（文件每行一个 media_id，# 开头为注释）
python scripts/publish_script.py --delete-batch ids.txt --real
```

底层走 relay `POST /draft-delete`，需先在云调用「微信令牌」权限加 `/cgi-bin/draft/delete` 并重建版本。

## 流程（--real 时）

1. 本地读 `article.md`，`md2wechat` 把 Markdown 转成微信图文 HTML（图片引用先留占位）
2. 每张正文插图 base64 后 POST relay `/material` → 换回 mmbiz 链接，回填进 HTML
3. 封面 POST relay `/material` → 拿到 `thumb_media_id`
4. 标题 + HTML + `thumb_media_id` POST relay `/draft` → 创建草稿

详见 [SKILL.md](SKILL.md)。
