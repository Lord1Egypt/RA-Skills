# Contributing

## 调试 xhs 抓取的常见入口

1. **先跑 `xhs-keepalive.py check`** — 90% 的问题在这里暴露
2. **agent-browser eval 看 console** — 抓 search_result 后 `document.querySelectorAll('section.note-item').length` 看是否有数据
3. **看 cookie 状态** — `agent-browser cookies get` 检查 web_session / a1 还在不在
4. **看 X-s 是不是被刷** — `eval` 算一次 `__sign(url, body)` 看返回的 base64

## 加新命令

参照 `xhs-fetch.py` 里 `cmd_search` / `cmd_note` / `cmd_user` 的模板：
- `ensure_cookies_loaded()` 必备
- `ab_open()` + `time.sleep(3)` 让页面渲染完
- `ab_eval()` 抓 DOM（agent-browser eval 是 JS 表达式,不能用 return,用 IIFE）
- 错误处理:检查 `300012` / `安全限制` / `Security Verification` 滑块 → 早返回

## ⚠️ captcha 检测设计模式(必读)

xhs 有 2 套独立的拦截,退出码要区分:

| 触发 | 退出码 | 父脚本动作 |
|---|---|---|
| **300012 IP 风控** | 2 | 重试前 sleep 60s |
| **Security Verification 滑块**(`user/profile/...` 路径独立) | 3 | 重试前 sleep 60s(3 次),提示用户**等 30+ 分钟**或**人过滑块 + 重导 cookie** |
| **300011 账号异常** | 1 | 不重试,提示重导 cookie |
| **其他** | 1 | 不重试,报错 |

**新加的 `cmd_*` 函数**如果会打开 `user/profile/...` 路径,**必须**检测 `Security Verification` / `website-login/captcha` / `verifyType=124` 并 return 3。否则 harvest 父脚本无法做 60s backoff,会一直 captcha 不退。

具体代码参考 `xhs-fetch.py` `cmd_user` L523-528。

## 限速铁律(必读)

`ab_open` 每次都是新网络请求,连续 7-8 次不 sleep 必中 300012。`ab_eval` 不打网络(只查已渲染 DOM),连续多个 eval 安全。

新加的脚本/函数**必须**:
- `ab_open` 之后 sleep ≥ 3s(默认 4s)
- `ab_eval` 之后如果要再 `ab_open`(切页),sleep ≥ 2s
- 多个 `ab_open` 连续调用 → 必中 300012,不要这么做

## 提交前 checklist

- [ ] `python3 xhs-keepalive.py check` 退出码 0
- [ ] `python3 xhs-fetch.py paths` 输出符合预期
- [ ] `python3 xhs-fetch.py search "测试" --limit 5` 拿得到 5 条数据
- [ ] 跑过 `--out /tmp/test.json` 看 JSON 结构合理
- [ ] 没在源码里 hardcode cookie 字符串
- [ ] `data/cookies.txt` 还是 chmod 600
- [ ] 新加的 `cmd_*` 有 captcha 检测 + 正确的 sleep 间隔

## 路径硬性约束

- 所有运行时数据放 `$SKILL/data/`
- 落盘文件用 `Path(__file__).parent / 'data' / ...` 模式,不用 `/tmp/xhs/...`
- 老的 `/tmp/xiaohongshu/` 路径只在 `paths.py` 里兼容,其它脚本不要再 hardcode
- 优先用 `from paths import ...` 而不是直接拼路径
