# 图片上传

只在用户图片或点名生图的成品需要写入微排版素材库时阅读。素材库里的图不要上传。槽位、去背和 OSS 见 [assets.md](assets.md)。

脚本在本技能内：`$SKILL_DIR/scripts/upload_images.py`。`SKILL_DIR` 与鉴权见本技能 SKILL.md。

## 命令

```bash
python3 "$SKILL_DIR/scripts/upload_images.py" \
  --file "{taskDir}/images/{assetId}.png" \
  --out "{taskDir}/upload-result.json"
```

- `--file`、`--url`、`--dir` 都可重复。至少提供其中一项。
- 本地文件必须存在。`--dir` 默认只扫一层；用户明确要求递归时才加 `--recursive`。目录只收 `.png` `.jpg` `.jpeg` `.webp` `.gif` `.svg`。
- `--url` 只接受 `http://` 或 `https://`，拒绝 `data:`。作品流水线里先把地址下到 `images/`，再用 `--file`，见 [assets.md](assets.md)。
- `--dry-run` 只列出计划，不发请求。
- 脚本串行请求，超时 30 秒。429 自动重试一次。401、402、403 停止后续条目。
- 服务端按文件内容 SHA1 去重。相同图片再次上传返回已有记录，重试安全。

不要手写上传请求。

## 结果

退出码：`0` 全部成功；`1` 部分失败；`2` 参数错误或缺少 key。

成功时条目含 `source`、`mode`、`status`（`uploaded`）、`src`、`id`、`width`、`height`。作品流水线用其中的 `src`、`width`、`height`，见 [assets.md](assets.md)。

## 失败时暂停

有失败就停，等用户选择后再继续：

- 「重试」：对 `status=failed` 的条目再跑脚本。
- 「重试 N」：只重试第 N 项。
- 「继续」：保留已成功结果，失败槽位按 [assets.md](assets.md) 占位。

不要因此改去背或重新生图，除非用户改口。

## 接口

基础地址：`${WEIPAIBAN_API_BASE:-https://weipaiban.cn}`。请求带 `Authorization: Bearer $WEIPAIBAN_API_KEY`。`scripts/api_base.py` 的 `validate_api_base` 被上传、取素材和发布三个脚本共用。密钥只发到 `https://weipaiban.cn`（含子域）或本机 `localhost` / `127.0.0.1` / `::1`，其它地址直接失败。不要跳过证书校验。

| 用途     | 方法与路径                   | 请求                                 |
| -------- | ---------------------------- | ------------------------------------ |
| 本地文件 | `POST /api/v1/assets/upload` | `multipart/form-data`，字段名 `file` |
| 远程 URL | `POST /api/v1/assets/fetch`  | JSON `{"url":"https://..."}`         |

成功响应必须有 `data.src`，可直接作为上传结果里的 CDN 地址。新图片为 HTTP 201，重复内容为 HTTP 200。响应含 `error`，或缺少 `data.src`，都视为失败。

| 状态码    | 含义                   | 处理                                                                  |
| --------- | ---------------------- | --------------------------------------------------------------------- |
| 400       | 请求非法               | 检查文件或 URL 是否为可识别图片                                       |
| 401       | key 缺失、无效或过期   | 请用户到 <https://weipaiban.cn/settings/api-keys> 创建或复制密钥，并更新 `WEIPAIBAN_API_KEY` |
| 402       | 素材容量已满           | 清理素材或升级套餐（免费 50 / 专业月 1000 / 专业年 3000 / 大师 8000） |
| 403       | 未订阅且不是 developer | 与其它 `/api/v1` 相同                                                 |
| 413       | 文件过大               | 压缩或缩小后重试                                                      |
| 415       | 不支持的媒体类型       | 换成 png、jpg、jpeg、webp、gif 或 svg                                 |
| 429       | 限流                   | 等待后重试                                                            |
| 502       | 上游抓取失败           | 换可访问的 URL，或先下载再走 `--file`。不允许的地址也是这个结果       |
