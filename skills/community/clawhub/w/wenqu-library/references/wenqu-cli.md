# Wenqu CLI：搜索与下载增强

本技能只通过 `wenqu` 调用受管运行时；`wenqu-cli` 由本套件发布方（`gogoingai/wenqu-skills`）维护、与技能同源，不是第三方依赖。不要安装或调用第二套搜索/抓取 CLI、daemon 或 MCP。

## 环境与浏览器

首次使用前，向用户说明需要安装 `wenqu-cli` 并请求一次明确授权；获授权后，优先用 `pipx` 隔离安装锁定版本 `0.1.0`（已安装则跳过，不在每次任务中强制重装或升级）。安装后从 GitHub Releases（`gogoingai/wenqu-skills`）核对版本号与 SHA-256 校验值一致，再运行只读检查验证安装完整性：

```bash
pipx install 'wenqu-cli==0.1.0'
wenqu doctor --json
```

`wenqu doctor` 是只读检查，输出不含密钥；确认安装完整、运行环境就绪后再使用。若 `pipx` 不存在，才回退到当前 Python：

```bash
python3 -m pip install --user 'wenqu-cli==0.1.0'
export PATH="$(python3 -m site --user-base)/bin:$PATH"
wenqu doctor --json
```

`wenqu-cli` 仅暴露搜索（`wenqu library search`）与抓取（`wenqu library fetch`）两个受管子命令，作用域限定于本技能的素材收集，不执行越权或持久化操作。版本号随 wenqu-cli 发布同步更新；升级时由用户主动发起并重新核对校验值。

`wenqu-cli` 包含 Python 和 Crawl4AI 依赖。若 `wenqu doctor` 报告 Chromium 缺失，先运行下列预览；只有用户明确授权下载浏览器后，才执行不带 `--dry-run` 的命令：

```bash
wenqu setup library --dry-run --json
wenqu setup library
```

## 搜索

```bash
wenqu library search "<关键词>" --engines baidu,juejin,csdn --limit 9 --json
```

可选引擎是 `baidu`、`bing`、`linuxdo`、`csdn`、`duckduckgo`、`exa`、`brave`、`juejin` 与 `sogou`（也接受 `sougou` 和 `搜狗`）。`--limit` 是合并后的总上限；不要为了凑数默认全选。Startpage 已不属于 Wenqu CLI 的渠道。

每个结果都有 `engine` 与 `channel`。索引记录为 `wenqu-cli:{engine}`；若 `channel` 不是 `direct`，追加该值，例如 `wenqu-cli:csdn:delegate:duckduckgo` 或 `wenqu-cli:baidu:browser`。`partialFailures`、`skippedEngines` 与空结果都不能阻塞其余候选；Exa 没有 `EXA_API_KEY` 时会在请求前写入 `skippedEngines`。

百度、必应、Brave、搜狗直连失败或空结果时，CLI 默认使用 Crawl4AI 做一次浏览器回退。传 `--no-browser-fallback` 可关闭它。LinuxDo 与 CSDN 由公开搜索索引委托发现；掘金走公开接口。所有候选都必须在合并、去重与分级后再下载。

搜索只提供候选。公众号的搜狗结果也只能作为候选：先确认最终的原始 `mp.weixin.qq.com` URL，再下载；不能重放包装跳转链接、猜测标题匹配或绕过验证。

## 下载

```bash
# 单页
wenqu library fetch <url> --out {materials}/articles/<域名>/<slug>.md --json

# 限量同源抓取；N 必须在收集清单中明确
wenqu library fetch <url> --max-pages <N> --out {materials}/docs/<站点>.md --json

# 已确认的公开微信公众号文章
wenqu library fetch <mp.weixin.qq.com URL> \
  --out {materials}/articles/mp.weixin.qq.com/<slug>.md --json
```

微信公众号直达时，CLI 自动获取公众号正文并等待 `#js_content` 渲染完成。遇到验证、登录、付费墙、空正文或访问限制时，记录失败并改用 agent 原生下载或公开替代来源；不得反复请求或绕过访问控制。
