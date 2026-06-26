# Operations Reference

## 目录

1. 常用命令配方
2. 代理 / 网关配置
3. 排查清单
4. Windows Python 别名问题
5. OpenClaw 定时任务建议
6. Sync Debug 输出怎么看

## 1. 常用命令配方

### 登录

```bash
python scripts/wechat_article_assistant.py login-start \
  --channel feishu \
  --target user:YOUR_OPEN_ID \
  --account default \
  --wait true \
  --json
```

### 添加公众号

```bash
python scripts/wechat_article_assistant.py add-account-by-keyword "成都发布" --json
```

### 拉文章列表

```bash
python scripts/wechat_article_assistant.py list-account-articles \
  --fakeid "MzA4MTg1NzYyNQ==" \
  --remote true \
  --count 10 \
  --json
```

### 抓文章详情

```bash
python scripts/wechat_article_assistant.py article-detail \
  --link "https://mp.weixin.qq.com/s/xxxxxxxx" \
  --json
```

### 同步全部公众号

```bash
python scripts/wechat_article_assistant.py sync-all --interval-seconds 180 --json
```

## 2. 代理 / 网关配置

### 推荐地址形态

```text
https://your-gateway.example.com
```

运行时会自动拼成：

```text
https://your-gateway.example.com/?url=https://mp.weixin.qq.com/...
```

### 设置单个网关

```bash
python scripts/wechat_article_assistant.py proxy-set \
  --url "https://proxy-01.example.com" \
  --apply-article-fetch true \
  --apply-sync true \
  --enabled true \
  --json
```

### 设置多个网关

```bash
python scripts/wechat_article_assistant.py proxy-set \
  --url "https://proxy-01.example.com" \
  --urls "https://proxy-02.example.com" \
  --urls "https://proxy-03.example.com" \
  --apply-article-fetch true \
  --apply-sync true \
  --enabled true \
  --json
```

### 查看当前代理配置

```bash
python scripts/wechat_article_assistant.py proxy-show --json
```

### 快速测试网关可用性

```text
https://your-gateway.example.com/?url=https://www.baidu.com/
```

**注意：**

- sync 和 article 都按 gateway 风格理解
- 不要把 gateway 地址当成标准 HTTP/HTTPS CONNECT 代理
- `Tunnel connection failed: 400 Bad Request` 往往说明代码走到了标准代理分支，或地址本身不是 CONNECT 代理

## 3. 排查清单

默认先跑：

```bash
python scripts/wechat_article_assistant.py env-check --json
python scripts/wechat_article_assistant.py doctor --json
python scripts/wechat_article_assistant.py login-info --validate true --json
python scripts/wechat_article_assistant.py proxy-show --json
```

必要时补充：

```bash
python -m pip show beautifulsoup4 requests markdownify
python -m pip install -r requirements.txt
bash scripts/run_sync_all.sh --help
ls -la scripts/
ls -la requirements.txt
```

### 重点检查项

1. `python` / `python3` 是否真可用
2. 关键依赖是否已安装
3. 关键脚本是否存在
4. `openclaw` 命令是否可用
5. 数据目录 / 二维码目录 / 数据库是否存在
6. 是否已有登录态
7. 代理是否启用、是否开对了 `apply_article_fetch` / `apply_sync`

### 常见判断

- **依赖缺失**：先补依赖，再重试业务命令
- **路径错误**：先核对 skill 目录、媒体目录、cron 路径
- **invalid session**：先怀疑登录态过期
- **网关返回 HTML / 非 JSON**：先怀疑网关被拦截或返回错误页

## 4. Windows Python 别名问题

如果用户在 Windows 上输入 `python` / `python3` 会跳微软商店：

1. 打开“应用执行别名”（App execution aliases）
2. 找到：
   - `python.exe`
   - `python3.exe`
3. 关闭这两个开关

然后再检查：

- 如果能正常执行，说明已修复
- 如果提示找不到命令，说明机器上还没正确安装 Python 或没配 PATH

## 5. OpenClaw 定时任务建议

如果用户要每天固定时间自动同步全部公众号：

- 优先使用 `scripts/run_sync_all.sh`
- 再配合 `openclaw cron add`
- 推荐参数：
  - `--session isolated`
  - `--announce`
  - `--tz "Asia/Shanghai"`
  - 要求精确整点时再加 `--exact`

适用场景：

- 每天固定时间同步全部公众号
- 长期后台运行
- 需要自动把同步结果回传当前聊天

## 6. Sync Debug 输出怎么看

sync 失败时，如果返回里有 `data.request_debug`，优先看：

- `operation`
- `mode`：`gateway` / `direct`
- `request_url`
- `curl`
- `proxy_url`
- `note`

### 常见解释

- `mode=gateway`
  - 说明请求按 `/?url=...` 形式走了网关
- `mode=direct`
  - 说明请求是本地 requests 直连 / 直出
- 日志里先出现 `gateway response failed ... invalid session`
  - 说明网关已经打到微信接口了，只是业务侧返回 session 失效
- 日志里出现 `Tunnel connection failed: 400 Bad Request`
  - 说明后续掉回了标准代理分支，且当前地址并不是可用的 CONNECT 代理
