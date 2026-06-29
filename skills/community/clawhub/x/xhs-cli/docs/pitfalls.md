# xiaohongshu-search 反爬坑笔记

## 大坑 (按踩坑频率)

### 1. IP 风控 300012 — 网络层就拦

**症状**: `ab open` 任何 xhs 页面 → 自动跳转到 `https://www.xiaohongshu.com/website-login/error?...&error_code=300012`

**根因**: xhs 风控把整段 IP (AS9808 移动 NAT / 部分商用 IP 段) 直接封了。这跟 cookie 无关,跟浏览器指纹无关,就是源 IP 被 ban。

**解决**:
- 换网络环境 (代理 / 4G / 换 IP)
- 不要再瞎试 cookie,浪费时间
- 注意: 有些 IP 段被 ban 是**动态**的,等几小时可能又通了

### 2. Cookie 失效 300011 — 账号异常

**症状**: API 返回 `{"code": 300011, "msg": "当前账号存在异常"}`

**根因**: `web_session` 短效 (6-12h),过期后服务端认为账号异常。

**解决**:
- 重导 cookie 到 `data/cookies-raw.txt`
- 跑 `python3 xhs-keepalive.py inject` 转 Netscape
- 跑 `check` 验证

### 3. X-s 签名复杂度 — 不能自己算

**症状**: 想直 curl API → 必须带 `X-s: XYS_...` 头

**根因**: `seccore_signv2` 函数用 `window.mnsv2` + `sha1` + `btoa` 拼装。这个 `mnsv2` 是混淆的 webpack 模块,在 xhs 官方页面加载时自动注入到 `window`。

**解决**: **不要自己算 X-s**,统一走 agent-browser 让官方 JS 帮我们算。

如果非要算 (CI 环境没浏览器),参考 `SKILL.md` 里的算法,但 `mnsv2` 内部用了混淆的字符串数组 + 字符处理,要 1:1 复刻非常麻烦。

### 4. agent-browser state save/load 的坑

**症状**: `state save` 出来 36 字节,`state load` 后页面还是被拦

**根因**: 
- `state save` 在 daemon 已运行时,daemon 状态优先,save 出来是 daemon 当前 state 的 subset
- 必须先 `close --all` 再 open with `--state`
- 36 字节的 state file 是 skeleton, 实际需要大几百 KB (含 user data dir / cookies / cache)

**解决**:
```bash
agent-browser close --all
agent-browser open "https://www.xiaohongshu.com/explore" --state $SKILL/data/state/xhs.state
```

### 5. agent-browser daemon 状态污染

**症状**: `ab eval` 一直返回 `about:blank`,但 `ab open` 看起来成功了

**根因**: daemon 内部 state 坏了,可能是 `eval` 里的 syntax error / 死循环 / 某个资源没释放

**解决**:
```bash
pkill -9 -f "Chrome|chromium|agent-browser"  # 强杀
agent-browser open "https://example.com"       # 测试是否恢复
# 恢复后:
agent-browser open "https://www.xiaohongshu.com/..."
```

## 小坑

### 6. `unread` cookie 的奇怪格式

这个 cookie 的值是 URL-encoded JSON,例如:
```
unread={%22ub%22:%226a31...%22,%22ue%22:%226a31...%22,%22uc%22:39}
```

不要尝试用 Python 解析,直接当字符串存就行。xhs 服务端会自己处理。

### 7. 多个 a1 / web_session 冲突

打开 xhs 页面后,服务端会**刷新**几个 cookie (`a1`, `webId`, `acw_tc`)。如果你的原始 cookies 还在,agent-browser 里就有两份:
- 原始: `a1=19ed3657b0bt...` (你的)
- 服务端新发: `a1=19ed4d196bbs...` (页面发的)

哪个生效取决于服务端的 cookie 选择逻辑。**结果不稳定**,所以重导 cookie 后应该立即用 agent-browser 做事,不要中间打开别的页面。

### 8. `web_session` 长度太短 ≠ 失效

我们之前看到 `web_session=040069b18d0f8a56c593f14d07384bfcbdc2d7` (32 字符),看起来比正常的短。但**这是有效的**。xhs 用的是 zstd / 自定义压缩的 session,不是 200+ 字符的 JWT 那种。

### 9. 搜索结果可能没有 "全部" Tab

搜索 AI 时,前 22 条左右有数据,后面就开始混合其他无关内容 (xhs 算法不精准)。要拿更精准的结果,加 `--sort hot` 或加更长的关键词。

## 调试命令

```bash
# 1. 看 IP / 城市
curl -s "https://ipinfo.io/json" | python3 -m json.tool | head -10

# 2. 看 agent-browser 当前 cookies
agent-browser cookies get

# 3. 算 X-s
agent-browser eval "(() => { const sha1 = /* 同步实现 */; ... })()"

# 4. 看 xhs 页面的 webpack 模块
agent-browser eval "Object.keys(window).filter(k => k.startsWith('webpack'))"

# 5. 看 mnsv2 是不是可用
agent-browser eval "typeof window.mnsv2"
```

## 经验法则

1. **看到 300012 → 换网络** (90% 概率是 IP 问题,不是 cookie)
2. **看到 300011 → 重导 cookie** (90% 概率是 web_session 失效)
3. **agent-browser 卡死 → `close --all && pkill -9`** 是万能解
4. **不要 hardcode cookie** — 永远走 `data/cookies.txt`
5. **搜索时加 sleep** — xhs 检测短时间高频请求,30 个请求后 sleep 10s

## 新坑 (1.1.0,按踩坑频率)

### 10. user/profile 路径有独立 captcha(verifyType=124)

**症状**: `ab open` `https://www.xiaohongshu.com/user/profile/<id>` → 重定向到 `https://www.xiaohongshu.com/website-login/captcha?...&verifyType=124`,页面 title 是 "Security Verification"。

**根因**: xhs 给 `user/profile/...` 这条路径**单独**套了一层人机验证,**跟 300012 IP 风控独立**。别的页面(explore / search / note)都没事,只看别人主页会中。

**特征**:
- 不会因为换网络/IP 退(是 session 级状态)
- 衰减需 30+ 分钟,不像 300012 几分钟就好
- 该账号 + 该 IP 组合的 session 被标记后,即使单次访问也会弹

**解决**:
- **避免多次访问 user 主页** — `xhs-harvest.py user --from-name` 路径会全流程只访问 1 次
- **避免** `user-search --verify` + `harvest user` 的两步走组合(必中)
- 触发后: 等 30+ 分钟衰减 / 浏览器人过滑块 + 重导 cookies

**检测代码**(`xhs-fetch.py` `cmd_user`):
```python
if 'Security Verification' in r.stdout or 'website-login/captcha' in r.stdout:
    err("触发滑块验证 (verifyType=124)")
    return 3  # 区别于 300012 的返回码 2
```

### 11. ab_open 密集触发 300012(高频踩坑)

**症状**: 连续 `ab open` 7-8 次不 sleep → 后面几次都中 300012。

**根因**: xhs 检测"短时间高频请求",即使单次操作正常,密集打模式会触发 IP 风控升级。

**场景**:
- 调试时手贱连开 7-8 个不同页面看状态
- agent 写自动化脚本时调 ab 太密集

**解决**:
- **能交给 `xhs-fetch.py` / `xhs-harvest.py` 的事,绝不要用 `ab` 手动打** — 脚本里 sleep + 60s backoff 都包好了
- 调试时先 `xhs-keepalive.py check` 看状态
- 需要手动 ab 时每步 sleep 4s+

**注意**: `ab_eval` 不打网络(只查已渲染 DOM),连续多个 eval 安全。只有 `ab_open` 触发风控。

### 12. user-search --verify + harvest user = 必中 captcha

**症状**: 跑完 `xhs-fetch.py user-search "name" --verify`(成功,拿到 user_id),接着跑 `xhs-harvest.py user <id>` → 立即 captcha。

**根因**:
- `user-search --verify` 访问 user 主页 1 次(确认 name 匹配)
- `harvest user` Phase 1 又访问 user 主页 1 次(拿 note 列表)
- 总共 2 次访问 `user/profile/...` 路径 → 触发 verifyType=124 captcha

**解决**:
- **不要 verify**:search 返回的 author 名跟关键词前缀匹配 + DOM 中 `avatar-container` class 过滤就够稳,不必再开 user 主页确认
- **用 `--from-name`**: `xhs-harvest.py user --from-name "name"` 内部把 verify + Phase 1 合成单次 ab_eval,user 主页只访问 1 次

**检测代码**(`xhs-harvest.py` `cmd_user` Phase 1):
```python
if r.returncode == 3:  # captcha
    if attempt >= 3: return 1
    print("  ⚠️  captcha 触发,sleep 60s 后重试")
    time.sleep(60)
    continue
```
