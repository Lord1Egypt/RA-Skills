# xiaohongshu-search

小红书内容抓取 skill。统一走 agent-browser 路径，让 xhs 官方 JS 帮我们算 X-s 签名 + 渲染 DOM。

> **⚠️ 强登录态 skill** — 没有 cookie 什么数据都拿不到。首次使用需要用户手动导 cookie 到 `data/cookies-raw.txt`。

## 5 个核心命令

```bash
# 1. 主题收割 (80% 场景): 搜→按点赞排序→逐个抓详情+评论→落盘→REPORT.md
python3 xhs-harvest.py hot "AI" --limit 10 --comments 10

# 2. 按用户名收割 (从显示名到全量作品,推荐路径)
python3 xhs-harvest.py user --from-name "小Lin说" --notes 50 --limit 20

# 3. 用户名 → user_id 解析 (只需 user_id,不收割)
python3 xhs-fetch.py user-search "小Lin说"

# 4. 已知 note_id 批量抓
python3 xhs-harvest.py ids id1 id2 id3 --tokens "t1,t2,t3"

# 5. 精细控制:单笔记 / 单用户
python3 xhs-fetch.py note "69a97fd1..." --comments 30
python3 xhs-fetch.py user "5abf9024..." --notes 20
```

**`xhs-harvest.py`** 编排工作流(增量+断点+限速+报告全包),**`xhs-fetch.py`** 原子操作(细粒度控制)。

## 快速开始

```bash
# 0. 用户在浏览器登录 xiaohongshu.com
# 1. 手动导 cookie: F12 → Application → Cookies → 复制 www.xiaohongshu.com 全部
echo "a1=xxx; web_session=xxx; id_token=xxx; ..." > data/cookies-raw.txt
chmod 600 data/cookies-raw.txt

# 2. 转 Netscape + 验证
python3 xhs-keepalive.py inject   # 转 Netscape 格式
python3 xhs-keepalive.py check     # 验证登录态 (exit 0=有效, 1=cookie, 2=IP)

# 3. 跑收割
python3 xhs-harvest.py hot "AI" --limit 10
```

## 核心优势

- **统一走 agent-browser**:不用反爬、不用算 X-s、不用对抗 fingerprint
- **skill 自包含**:git clone 即用,数据全在 `data/` 下
- **老路径兼容**:老的 `/tmp/xiaohongshu/` 自动识别
- **env 覆盖**:`XHS_DATA_DIR` / `XHS_COOKIE_FILE` 给 docker / CI 用
- **限速+重试内置**:harvest 默认 4s sleep + 60s backoff,captcha 自动重试 3 次

## cookie 生命周期

| 字段 | 有效期 | 失效后 |
|---|---|---|
| `web_session` | **6-12h** | 重新导 (300011 账号异常) |
| `acw_tc` / `websectiga` / `sec_poison_id` | 数小时 | 重新导 (风控指纹过期) |
| `a1` / `id_token` | 数天~数周 | 重新登录小红书拿 |
| `webId` / `gid` | 数天 | 重新导 |

**体感**:每天换 1-2 次 cookie 比较稳。看到 `300011` 就提示用户重新导。

## ⚠️ 按用户名收割的 captcha 陷阱

`xiaohongshu.com/user/profile/<id>` 这条路径**有独立的人机验证**(verifyType=124,不是 300012 IP 风控)。**短时间内访问 2 次必触发**。

**✅ 正确做法**:用 `xhs-harvest.py user --from-name "name"`,user 主页只访问 1 次。

**❌ 错误做法**(会 captcha):
```bash
xhs-fetch.py user-search "name" --verify   # 第 1 次
xhs-harvest.py user 5abf...               # 第 2 次 → 触发
```

触发后**衰减需 30+ 分钟**。详细决策规则见 [SKILL.md](./SKILL.md)。

## 与 douyin-search / zhihu-search 的差异

| 维度 | douyin | zhihu | **xhs** |
|---|---|---|---|
| 抓取路径 | HTTP API (无 X-s) | HTTP API (cookie) | **agent-browser only** (X-s 强) |
| 必填 cookie | `ttwid` | `z_c0` | `a1` + `web_session` + `id_token` |
| cookie 短效期 | 30 天 | 1-2 周 | **6-12 小时** |
| IP 风控 | 中 | 弱 | **强** (移动 NAT 段基本被封) |
| 写操作 | 暂未 | 暂未 | 暂未 |

## 详细文档

- [SKILL.md](./SKILL.md) — 给 LLM agent 用的完整文档(精简到 100 行)
- [docs/pitfalls.md](./docs/pitfalls.md) — 反爬坑 / 调试笔记
- [CHANGELOG.md](./CHANGELOG.md) — 版本历史
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 贡献指南

## License

MIT
