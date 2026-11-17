---
name: wechat-draft-publisher-cloud
description: 基于微信云托管 relay 的公众号草稿发布器：把现成的 markdown 文章 + 封面图推送到微信公众号草稿箱，本地无需 appid/secret、免 IP 白名单。触发：「推草稿」「发公众号草稿箱」「wechat draft publish」「send to wechat draft」。不触发：写文章、trending、邮件。默认 dry-run，加 --real 才真发；relay 地址与密钥通过环境变量或 config.json 注入（不硬编码）。
version: 1.0.0
homepage: https://github.com/shinchen6/wechat-draft-publisher-skill
metadata: {"openclaw":{"emoji":"📤"}}
---

# WeChat Draft Publisher (Cloud)

一个动作：`article.md + cover.png + 标题` → relay → 公众号草稿箱。

**默认 dry-run**（不真发，只本地转 HTML + 跑流程 + 写 mock media_id）。**真发必须显式加 `--real`**——防止自动化测试时误推到用户草稿箱。

## 何时用 / 不用

**用**：用户说"推草稿"、"发公众号草稿箱"，或上游流水线 Step 7 调用。
**不用**：写文章 / trending / 邮件 / 纯本机保存。

## relay 是什么

relay 是部署在 **微信云托管** 上的开源草稿代理服务端，利用官方「开放接口服务（云调用）」免鉴权调用公众号接口，本地脚本无需固定 IP、无需公众号 appid/secret。本 skill 是客户端，负责写稿、把 Markdown 转成微信图文 HTML、处理图片，再把内容交给 relay。

relay 只做三件事（纯代理，不解析 Markdown）：
- `POST /material`：接收图片 base64，上传到微信素材库，返回 `media_id` + `url`
- `POST /draft`：接收标题 + 已转好的 HTML + 封面 `thumb_media_id`，创建草稿
- `POST /draft-delete`：接收 `{"media_id": ...}`，删除草稿（需先在云调用「微信令牌」权限中加 `/cgi-bin/draft/delete`）

## Markdown -> HTML 在哪里做

**在本 skill 本地完成**（`scripts/md2wechat.py`，零依赖纯标准库实现）。relay 不碰 Markdown。
这样 relay 保持极简、零三方依赖；所有内容加工都在你本地可控。

## 配置注入（访问密钥 + 访问地址）

relay 跑在云托管，默认公网地址是平台生成的**默认域名**（谁都能访问），所以必须靠「访问密钥」保护。本 skill 按以下优先级解析 **访问地址(URL)** 与 **访问密钥(KEY)**：

1. **命令行**：`--cloud-url` / `--cloud-key`
2. **环境变量**（推荐）：
   - `WECHAT_DRAFT_RELAY_URL` / `WECHAT_DRAFT_RELAY_KEY`
   - 兼容旧名 `DRAFT_CLOUD_URL` / `DRAFT_API_KEY`
3. **config.json**（放在 `scripts/` 目录下，已被 `.gitignore` 忽略，不进仓库）：
   ```json
   { "relay_url": "https://<你的服务名>.<地域>.run.tcloudbase.com", "relay_key": "你的 RELAY_API_KEY" }
   ```
4. 脚本默认值（发布版留空，要求显式配置；私部署可在此填个人默认值）

**发布版不硬编码任何个人地址 / 密钥**——安装后由用户自己注入，符合开源安全要求。

## 输入

| 参数 | 必填 | 说明 |
|---|---|---|
| `article_path` `cover_path` | ✓ | markdown + PNG |
| `titles_md_path` \| `title_path` | 二选一 | 候选标题文件 / 已选标题文件 |
| `--real` | 选 | **加这个才真发**，否则 dry-run |
| `--cloud-url` `--cloud-key` | 选 | 覆盖注入的 relay 地址/密钥 |
| `covered_md_path` `covered_line` | 选 | 成功后追加去重 |
| `feishu_chat_id` | 选 | 真发成功后才发飞书（best-effort） |
| **正文插图** | 自动 | 脚本扫描 `article.md` 里的 `![](本地图)`，本地转 HTML 时把每张图经 relay `/material` 上传素材库换回 mmbiz 链接。**无需额外参数** |

## 输出（写 `$run_dir/publish_result.json`）

```json
{success, media_id, chosen_title, chosen_title_bytes, cloud_url, body_images, html_len, covered_appended, feishu_sent, error_code, error_msg, elapsed_sec}
```

## 用法

```bash
# 1) dry-run（默认，本地转 HTML + 校验，不发任何请求）
python scripts/publish_script.py --article X.md --cover Y.png --titles-md T.md

# 2) 真发（推荐先 1) 验证后再 2)）
python scripts/publish_script.py --real --article X.md --cover Y.png --titles-md T.md
```

**正文插图怎么写**：在 `article.md` 正常用 markdown 图片语法，脚本自动扫描、本地转 HTML、经 relay 上传。

```markdown
## 一段说明

![对比图](img/compare.png)

- 要点一
- 要点二
```

## 删除草稿

草稿箱会累积（每次 `--real` 都新增一篇、不覆盖）。清理旧草稿：

```bash
# 单个删除（默认 dry-run 只列出，--real 才真删）
python scripts/publish_script.py --delete <media_id> --real

# 批量删除（文件每行一个 media_id，# 开头为注释）
python scripts/publish_script.py --delete-batch ids.txt --real
```

底层走 relay `POST /draft-delete`，密钥/地址解析规则与发布一致（`--cloud-url`/`--cloud-key` > 环境变量 > config.json > 默认值）。**需先在云调用「微信令牌」权限中加 `/cgi-bin/draft/delete`** 并重建版本，否则报 `48001`。

- 本地图：`![](img/body1.png)` —— 脚本本地转 HTML 时经 relay `/material` 上传素材库后替换成 mmbiz 链接。
- `publish_result.json` 里 `body_images` 字段报告本次扫描到的本地插图数量，`html_len` 报告生成 HTML 长度，dry-run 即可验证。

## 流程（--real 时）

1. **校验**：`article` / `cover` / `titles_md|title_file` 文件存在；`run_dir` 自动 `makedirs`
2. **选标题**：titles.md 解析第 1 个 `1.` / `1、` / `1)` 候选；或直读 title.txt
3. **字节**：UTF-8 ≤64；超了**报错不截断**
4. **写 title.txt**：覆盖式写入，`run-dir/title.txt`
5. **本地转 HTML**：`md2wechat.convert(md, url_map)`（dry-run 也跑，验证转换不崩）
6. **上传插图**：每张图 base64 后 POST relay `/material` → 换回 mmbiz url，写入 url_map
7. **上传封面**：POST relay `/material` → 拿到 `thumb_media_id`
8. **建草稿**：标题 + HTML + `thumb_media_id` POST relay `/draft` → 返回 `media_id`
9. **写 publish_result.json**

## 错误码

| 码 / 现象 | 含义 | 修复 |
|---|---|---|
| `41001` missing access_token | 云调用网关未注入凭证 | relay 部署侧：开启「开放接口服务」开关并**重建版本** |
| `48001` / `85107` 接口未授权 | 云调用「微信令牌」权限缺 `/cgi-bin/material/add_material` + `/cgi-bin/draft/add` | 控制台补接口路径 |
| `40164` IP 不在白名单 | 非云托管部署、token 模式 | 把出口 IP 加公众号后台白名单（云托管免此步） |
| `invalid api key` | 缺 / 错 `X-API-Key` 头 | 检查注入的 relay 密钥 |
| `NETWORK`（本 skill 定义） | 域名不可达 / 超时 / 非 JSON / urllib 连接或 HTTP 错误 / **503 网关冷启动** | 503 自动 retry 1 次（8s 退避）；其它检查 relay 地址是否失效 |

**失败不删 article.md / cover.png，留人重试。**

## Pitfalls

1. **字节 ≠ 字符**：`len(s.encode('utf-8'))`，中文每字 3 字节
2. **超 64 字节不静默截断**：平台上限，截断会改语义
3. **默认 dry-run**：mock 返回 `MOCK_MEDIA_ID_dryrun`，**外部副作用全跳过**（不真发、不发飞书、不动 covered）。真发必须 `--real`
4. **零依赖发送 + 零依赖转换**：发送用标准库 `urllib` + `base64`（JSON 协议）；Markdown->HTML 用 `scripts/md2wechat.py`（纯标准库）。无需 `requests` / `curl` / `mistune`
5. **幂等**：covered_line 追加前先 grep；COVERED.md 不存在自动建文件头
6. **503 (nginx) 是网关层通用冷启动**：偶发（任何尺寸都可能）。内置 `do_publish_with_retry` 风格逻辑：识别 "503" + `err_code=NETWORK` 时 sleep(8) 后自动重试 1 次
7. **草稿箱会累积**：每次 `--real` 都新增 1 篇，**不会自动覆盖前一篇**
8. **云调用模式免 IP 白名单、免 appid/secret**：relay 部署在微信云托管并开启「开放接口服务」即可，本地脚本零凭证
