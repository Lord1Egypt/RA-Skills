---
name: wechat-article-assistant
description: 微信公众号文章同步与详情抓取助手。支持公众号后台登录、搜索与添加公众号、同步文章列表、抓取单篇或单账号文章详情、下载文章图片、配置代理、导出最近文章汇总和 Markdown 报告。用于“查最近文章”“抓文章详情”“下载公众号文章图片”“同步指定公众号文章”“按账号导出汇总”等场景。
---

# WeChat Article Assistant

使用这个 skill 时，按这里写的流程执行，不要跳过上游步骤，也不要自己用别的方法替代。

## 核心约定

1. **先读这个 skill，再执行操作**
   - 涉及公众号列表、文章详情、图片下载、汇总导出、代理配置时，先按这里的命令走。

2. **公众号文章详情优先使用 skill 自带命令**
   - 单篇文章详情：`article-detail`
   - 单账号批量抓详情：`fetch-account-details`
   - 不要自己手写抓取逻辑替代 skill。

3. **没拿到图片，就视为流程异常**
   - 对公众号文章详情抓取，必须确认图片已经下载成功。
   - 如果详情抓到了但图片没拿到，先排查代理/抓取问题，不要继续后续处理。

4. **详情抓取遇到环境异常页时，优先检查代理**
   - 公众号文章详情抓取常见失败原因是微信返回环境异常校验页。
   - 先 `proxy-show`，必要时 `proxy-set`，再重试。

---

## 一、这个 skill 处理什么

当前主要处理这些事：

1. 登录微信公众号后台并保存登录态
2. 搜索 / 添加 / 删除公众号
3. 配置公众号同步策略
4. 配置公众号主题分类
5. 同步文章列表
6. 抓取文章详情和图片
7. 导出最近文章汇总 / 单账号汇总

---

## 二、统一入口

```bash
python scripts/wechat_article_assistant.py --help
```

---

## 三、常用查询命令

### 1）查看公众号列表

```bash
python scripts/wechat_article_assistant.py list-accounts --json
```

### 2）查看最近文章

```bash
python scripts/wechat_article_assistant.py recent-articles \
  --hours 48 \
  --limit 20 \
  --json
```

适合：
- “查最近 24 小时 / 48 小时文章”
- “最近同步到了哪些文章”

### 3）查看某个公众号的文章列表

```bash
python scripts/wechat_article_assistant.py list-account-articles \
  --nickname "集虚空间" \
  --count 20 \
  --json
```

也可以用 `--fakeid` 指定账号。

可选参数：
- `--begin`
- `--count`
- `--keyword`
- `--remote`
- `--save`

适合：
- “查某个公众号最近发了什么”
- “按关键词筛某个公众号的文章”

---

## 四、文章详情抓取（重点）

这是最容易漏写、但最关键的部分。

### 方式 A：抓取单篇文章详情

当你已经有文章链接，或者已经知道 `aid` 时，用 `article-detail`。

```bash
python scripts/wechat_article_assistant.py article-detail \
  --link "https://mp.weixin.qq.com/s/xxxx" \
  --download-images true \
  --save true \
  --json
```

或者：

```bash
python scripts/wechat_article_assistant.py article-detail \
  --aid "2247484413_1" \
  --download-images true \
  --save true \
  --json
```

### `article-detail` 关键参数

- `--aid`
- `--link`
- `--download-images`
- `--include-html`
- `--force-refresh`
- `--save`
- `--json`

### 方式 B：抓取某个公众号最近几篇文章详情

当你已经知道公众号，但还没逐篇抓详情，用 `fetch-account-details`。

```bash
python scripts/wechat_article_assistant.py fetch-account-details \
  --nickname "集虚空间" \
  --limit 5 \
  --download-images true \
  --save true \
  --json
```

或者：

```bash
python scripts/wechat_article_assistant.py fetch-account-details \
  --fakeid "Mzk3NTM3NTQ0MA==" \
  --limit 5 \
  --download-images true \
  --save true \
  --json
```

### `fetch-account-details` 关键参数

- `--fakeid`
- `--nickname`
- `--limit`
- `--download-images`
- `--include-html`
- `--force-refresh`
- `--save`
- `--export-markdown`
- `--include-report-markdown`
- `--report-title`
- `--json`

### 什么时候用哪个

- **有单篇链接 / 单篇 aid** → `article-detail`
- **要批量抓某个公众号最近几篇详情** → `fetch-account-details`

### 关于图片下载

推荐至少加：

```bash
--download-images true --save true
```

判断标准：
- 详情抓取成功 + 图片下载成功 → 才算拿到完整素材
- 只有正文，没有图片 → 不算完成

---

## 五、代理配置（重点）

### 查看代理配置

```bash
python scripts/wechat_article_assistant.py proxy-show --json
```

### 设置代理

```bash
python scripts/wechat_article_assistant.py proxy-set \
  --url "http://127.0.0.1:7890" \
  --enabled true \
  --apply-article-fetch true \
  --apply-sync true \
  --json
```

### `proxy-set` 关键参数

- `--url`
- `--enabled`
- `--apply-article-fetch`
- `--apply-sync`
- `--urls`
- `--json`

### 什么时候必须先看代理

如果抓详情时出现类似错误：

```text
微信返回环境异常校验页，请配置代理后重试文章详情抓取
```

就先：
1. `proxy-show`
2. 需要时 `proxy-set`
3. 再重新执行 `article-detail` / `fetch-account-details`

---

## 六、同步与配置

### 1）设置同步策略和主题

```bash
python scripts/wechat_article_assistant.py set-account-config \
  --fakeid "FAKEID" \
  --processing-mode sync_and_detail \
  --categories "学习主题" \
  --auto-export-markdown true \
  --json
```

### 2）同步单个公众号

```bash
python scripts/wechat_article_assistant.py sync --fakeid "FAKEID" --json
```

### 3）同步全部公众号

```bash
python scripts/wechat_article_assistant.py sync-all \
  --interval-seconds 180 \
  --channel feishu \
  --target user:ou_xxx \
  --account support \
  --json
```

### `sync-all` 通知参数

`sync-all` 当前已经支持：

- `--channel`
- `--target`
- `--account`

这三个参数用于同步过程中的进度通知。

### `sync-all` 当前通知行为

如果同时传入了 `channel/target/account`，同步过程中会通过 `openclaw message send` 发送通知。

#### 1）每完成一个公众号，同步一次进度

示例文案：

```text
xxx公众号完成，进度1/4。状态：成功；新增文章 3 篇。
```

如果该公众号同步失败，则会发送：

```text
xxx公众号完成，进度1/4。状态：失败；原因：具体错误。
```

#### 2）如果检测到登录过期，停止后续同步

`sync-all` 在开始前会先验证登录状态。

如果一开始就发现登录已过期：
- 不执行后续公众号同步
- 立即通过 `channel/target/account` 发送过期提醒
- 直接返回失败

如果在同步某个公众号过程中发现登录已过期：
- 发送登录过期提醒
- 停止后续公众号同步
- 不再继续剩余账号

当前登录过期提醒文案类似：

```text
xxx公众号同步失败，进度1/4。检测到公众号登录已过期，已停止后续同步，请重新扫码登录公众号后台。
```

### 当前同步模式说明

每个公众号可设置：

- `processing_mode=sync_only`
  - 只同步文章列表，不自动抓详情
- `processing_mode=sync_and_detail`
  - 同步文章列表后，自动抓取新增文章详情

还可以设置：
- `auto_export_markdown=true`

---

## 七、导出汇总

### 导出最近文章总汇总

```bash
python scripts/wechat_article_assistant.py export-recent-report \
  --hours 24 \
  --save true \
  --include-markdown false \
  --only-markdown-accounts true \
  --json
```

### 导出单公众号汇总

```bash
python scripts/wechat_article_assistant.py export-account-report \
  --fakeid "FAKEID" \
  --save true \
  --include-markdown false \
  --json
```

### 汇总规则

- 只汇总 `auto_export_markdown=true` 的公众号
- 默认按最近 24 小时统计
- 优先按主题分类分组
- 同主题下再按公众号分组
- 最后按发布时间排序

---

## 八、文件输出规则

为了避免中文和特殊字符出现在文件名里：

- 合并总汇总：`YYYYMMDD-HHMMSS_combined-report.md`
- 单公众号汇总：`YYYYMMDD-HHMMSS_account-report_<fakeid>.md`
- 单篇文章详情：`article_<aid>.md`

---

## 九、推荐工作流

### 场景 A：查最近 48 小时文章

```bash
python scripts/wechat_article_assistant.py recent-articles \
  --hours 48 \
  --limit 20 \
  --json
```

### 场景 B：用户指定一篇公众号文章，要拿完整详情和图片

```bash
python scripts/wechat_article_assistant.py article-detail \
  --link "https://mp.weixin.qq.com/s/xxxx" \
  --download-images true \
  --save true \
  --json
```

如果失败且提示环境异常：

```bash
python scripts/wechat_article_assistant.py proxy-show --json
python scripts/wechat_article_assistant.py proxy-set \
  --url "http://127.0.0.1:7890" \
  --enabled true \
  --apply-article-fetch true \
  --apply-sync true \
  --json
```

然后再重试 `article-detail`。

### 场景 C：用户指定公众号，要抓最近几篇详情和图片

```bash
python scripts/wechat_article_assistant.py fetch-account-details \
  --nickname "集虚空间" \
  --limit 5 \
  --download-images true \
  --save true \
  --json
```

## 十、登录与排障

### 检查登录状态

```bash
python scripts/wechat_article_assistant.py login-info --validate true --json
```

### 环境检查

```bash
python scripts/wechat_article_assistant.py env-check --json
python scripts/wechat_article_assistant.py doctor --json
```

---

## 参考资料

需要更细说明时再读：
- `references/operations.md`
- `references/interface-reference.md`
- `references/sqlite-schema.md`
- `references/account-classification.md`
