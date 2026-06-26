# 常见问题与易错点

## 错误 1：直接调用内部接口

错误：

```bash
curl https://api.xianchou.com/run
```

正确：

```bash
xianchou generate image --prompt "..." --poll
```

CLI 只能调用 `/api/cli/*`。

## 错误 2：使用 Web 登录 token 作为 CLI 凭据

错误：

```bash
xianchou auth login --key <WEB_LOGIN_TOKEN>
```

正确：

```bash
# 在 Web 头像菜单中打开 Access Key，创建并复制完整 key
xianchou auth login --key <ACCESS_KEY> --project-id <PROJECT_ID>
```

CLI 使用用户创建的 Access Key，不使用浏览器 localStorage 中的登录 token。

## 错误 3：硬编码模型 ID

错误：

```bash
xianchou generate image --prompt "..." --model-id guessed-model
```

正确：

```bash
xianchou models image --project-id <PROJECT_ID>
```

从返回结果中读取 `provider_id` 和 `model_id`。

## 错误 4：忘记 `--write`

`xianchou markdown images` 默认 dry-run，不会修改 Markdown。

正确：

```bash
xianchou markdown images ./article.md --count 3 --write
```

## 错误 5：混淆本地路径和 URL 前缀

`--assets-dir` 是图片保存位置，`--public-url-prefix` 是写入 Markdown 的链接前缀。

```bash
xianchou markdown images ./article.md \
  --assets-dir ./public/images \
  --public-url-prefix /images \
  --write
```

## 错误 6：重复插入图片

不要手动删除 `<!-- xianchou:image ... -->` 标记。CLI 用该标记识别已有图片块并更新，删除后可能重复插入。

## 错误 7：误以为默认会生成封面

`xianchou markdown images` 默认只生成正文图片，不会更新 frontmatter。

正确：

```bash
xianchou markdown images ./article.md --cover --write
```
