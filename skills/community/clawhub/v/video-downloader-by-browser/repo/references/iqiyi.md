# 爱奇艺（iqiyi.com / 奇巴布）流结构逆向笔记

> 实测日期：2026-09-14
> 实测样本：奇巴布分享页 `cartoon_share_detail.html?...&tv_id=<tv_id>`（短片段，1 分钟级）
> 成果：720P（1080×720）/ 51.1 秒 / 6.7 MB，H.264 + AAC，音画齐全
> 结论：**免费内容（payMark=0）无需登录，无头浏览器即可全自动搞定**，不必打扰用户开本地任务会话

---

## 1. 页面类型与入口

爱奇艺儿童版（奇巴布）分享页形如：

```
https://www.iqiyi.com/common/qibabu/cartoon_share_detail.html?pageType=longVideo&uid=<uid>&album_id=<id>&tv_id=<id>&gender=1
```

- 页面是 **Vue SPA 空壳**：`curl` 直接抓 HTML 只有 13 KB，标题恒为“奇巴布-爱奇艺儿童版”，拿不到任何视频信息。
- 不要试图从 HTML 正则提取源——没有。
- 突破口有两个：**基础信息接口**（拿 tvid/vid/playUrl）和**浏览器抓网络请求**（拿 m3u8）。

---

## 2. 基础信息接口（未风控，无需登录）

```
https://pcw-api.iqiyi.com/video/video/baseinfo/<tvid>
```

返回关键字段：

| 字段 | 含义 |
|---|---|
| `tvId` / `vid` | 正片标识，后续全靠它 |
| `name` | 视频标题（可能是带 #话题 的口语化标题） |
| `playUrl` | **标准播放页地址**（形如 `http://www.iqiyi.com/v_1eyb703oiw4.html`），后续用浏览器打开它 |
| `payMark` | `0` = 免费非 VIP；非 0 = 需要会员 |
| `issueTime` / `publishTime` | 毫秒时间戳 |

拿到 `playUrl` 后，后续一律用**标准播放页**做浏览器抓流，不要再用分享页（分享页播放器行为不同）。

---

## 3. yt-dlp 与官方接口现状（2026-09 实测，全部失效）

| 手段 | 结果 |
|---|---|
| `yt-dlp <分享页>` | `ERROR: [iqiyi] Can't find any video`（`temp_id: download video page`） |
| `yt-dlp <playUrl>` | 同上，**yt-dlp 的爱奇艺解析器已坏** |
| `cache.video.iqiyi.com/vms?...` | `{"code":"A000001","msg":"Rule Block."}`（风控拦截） |
| `pcw-api.iqiyi.com/player/video/playurl` | `Not Found` |
| `mesh.if.iqiyi.com/player/lw/lwplay/accelerator`（不带 `.js`） | `404` |

**结论：别在纯 HTTP 层硬啃，直接上浏览器抓网络请求。** 这是爱奇艺和优酷最大的区别——优酷还能靠 seek 采集 URL，爱奇艺的取流接口全被风控。

---

## 4. 浏览器抓流（核心可行路径）

用 playwright（**headless 即可**，无需有头、无需登录）打开 `playUrl`：

监听 `response`，关注这些关键词：`m3u8`、`dash`、`tvg_video_stream`、`lwplay/accelerator`、`playervideoinfo`。

### 会遇到的几个接口，作用各不相同

| 接口 | 作用 | 注意 |
|---|---|---|
| `mesh.if.iqiyi.com/player/pcw/video/playervideoinfo?id=<tvid>` | 标题、`vipType`、`cid` | 看 `vipType` 判断是否会员内容 |
| `www.iqiyi.com/prelw/player/lw/lwplay/accelerator.js?...` | 播放器配置，含 `videoDuration`、`isVIP` | **可用来提前知道总时长，便于校验成品** |
| `mesh.if.iqiyi.com/tvg/tvg_video_stream?...` | **推荐位列表，不是正片！** | 里面的 `play_url` 是 `qips://tvid=...` 的其他推荐视频，**别误当正片下载** |
| `https://meta-cdn.video.iqiyi.com/<date>/xx/xx/<hash>.m3u8?qdv=3&...&qd_tvid=<tvid>&qd_sc=...` | **正片 m3u8** | 目标 |

### 触发播放的写法

```js
const v = document.querySelector('video');
if (v) { v.muted = true; v.playbackRate = 8; v.play().catch(()=>{}); }
```

- `playbackRate = 8` 能显著加快加载，几十秒的视频几秒就请求完。
- 有前贴广告时，尝试点击“跳过”类按钮；但短视频常无广告。
- m3u8 **未加密**（无 `EXT-X-KEY`）。

---

## 5. 分片规律（与优酷完全不同，务必注意）

### 关键差异：所有分片指向同一个 ts 文件

m3u8 里的每个分片 URL 都是**同一个 `.ts` 文件**，靠查询参数切字节区间：

```
https://data.video.iqiyi.com/videos/v1ts/20240902/c4/8b/<hash>.ts?start=0&end=348928&contentlength=348928&sd=0
https://data.video.iqiyi.com/videos/v1ts/20240902/c4/8b/<hash>.ts?start=348928&end=702744&contentlength=353816&sd=2680
```

- 分片区间**首尾相接**（上一片 `end` == 下一片 `start`），因此 **总字节 = 最后一片的 `end`**。
- `sd` 参数是该分片对应的毫秒时间偏移，可用于定位，下载用不上。

### ⚠️ `data.video.iqiyi.com` 直接请求会 405

对该域名发请求（哪怕带 UA / Referer / Origin / cookie / Range 全都试过）一律返回：

```
HTTP/1.1 405 Method Not Allowed   (响应体 17 字节 JSON)
```

推测是对非授信 IP / 地域做了限制（实测出口 IP 在境外）。**浏览器能正常下，是因为它拿到的是带签名的 CDN 地址**：

```
https://gdctyunct.inter.71edge.com/videos/v1ts/20240902/c4/8b/<hash>.ts?key=<签名>&dis_k=...&dis_t=...&dis_dz=CT-ShangHai&dis_st=...&qdv=3&src=iqiyi.com&...
https://n1cloudcdnct.inter.71edge.com/videos/v1ts/...（备用 CDN 域名）
```

**只有这种带 `key` 签名的 URL 才能下到数据（HTTP 200）。**

---

## 6. 正确下载姿势（三步）

### A. 拿带签名的真实 CDN URL

浏览器播放时监听 `.ts` 响应，取 `response.url`——它已经包含 `key` 等签名参数。

### B. 整文件一次下载（推荐）

实测**签名不绑定具体字节区间**，所以可以把 `start` / `end` / `contentlength` 直接改成整文件范围：

```
start=0&end=<总字节-1>&contentlength=<总字节>
```

```bash
curl -A "<桌面版 UA>" -e "https://www.iqiyi.com/" "<替换后的 URL>" -o full.ts
```

一次拿到完整流（实测 7,617,759 字节 / 7.3 MB，HTTP 200）。

> 若哪天签名改为绑定区间、整文件请求失败，回退方案：用同一个签名 URL 按 m3u8 的 22 个区间分别替换 `start`/`end` 逐片下载，再 `cat` 拼接（区间首尾相接，拼起来即完整流）。

### C. 转封装

```bash
ffmpeg -y -i full.ts -c copy -movflags +faststart out.mp4
```

爱奇艺的 ts 是标准 MPEG-TS，`-c copy` 无损、秒级完成。

---

## 7. ⚠️ 最大的坑：别用“浏览器边播边抓分片 body”来拼

第一版思路是：让浏览器播放，监听每个 `.ts` 响应，用 `response.body()` 抓字节再排序拼接。

**实测失败**：

- 播放器按自己的缓冲策略请求字节块（例如 `start=348160` 一次取 **6.4 MB**），与 m3u8 定义的 22 个分片区间**完全不一致**；
- 抓了 11/22 块就结束，区间**有重叠也有缺漏**；
- 直接拼出来必然**花屏、时长错乱**。

**正确做法**：回到 m3u8 定义的连续区间（或干脆整文件下载），不要相信播放器的取块边界。

---

## 8. 校验清单

- [ ] 成品时长 ≈ m3u8 的 `EXTINF` 总和（实测 51.107 s vs 51.0 s，吻合）
- [ ] 有音轨（`ffprobe` 应看到 `aac`），短视频也可能无音轨，需实际确认
- [ ] 分辨率与 `playervideoinfo` / 播放器声明一致
- [ ] 交用户播放验收

---

## 9. 何时需要人工介入

| 情况 | 处理 |
|---|---|
| `payMark=0`、`vipType=[]` | **免费内容，无头浏览器全自动**，不用打扰用户 |
| 播放页弹登录 / VIP 购买 | 走手动介入协议；按项目首选项，**建议用户在“本地任务”模式下新建会话** |
| 出现滑动验证 / 短信验证码 | 立即停止自动化，交给用户 |

---

## 10. 一键脚本

已封装为 `scripts/iqiyi_grab.py`，输入视频页 URL 直接出 mp4：

```bash
python scripts/iqiyi_grab.py "https://www.iqiyi.com/common/qibabu/cartoon_share_detail.html?...&tv_id=<tv_id>" out.mp4
```

脚本内部按本文 2 → 4 → 6 → 8 的顺序自动执行，含时长校验。
