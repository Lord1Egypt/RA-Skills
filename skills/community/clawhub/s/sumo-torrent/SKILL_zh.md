# SKILL_zh.md - Torrent 搜尋技能（中文說明）

## 功能
搜尋 BT4G 上的 Torrent 檔案，並輸出含 Trackers 的 Magnet 連結。

## 觸發指令
`torrent <關鍵字>` 或 `/torrent <關鍵字>`

---

## ⚠️ 重要：遇到 Cloudflare 必須用瀏覽器！

### 🚨 Cloudflare 錯誤時的處理流程

當遇到以下錯誤時：
- `Cloudflare` 驗證頁面
- `403 Forbidden`
- web_fetch / torrent_search.py 失敗

**必須立即切換到瀏覽器方法：**

```javascript
// Step 1: 用 profile="my-daily-chrome" 開啟 BT4G
browser(action="open", profile="my-daily-chrome", url="https://bt4gprx.com/search?q=關鍵字")

// Step 2: 截圖確認通過 Cloudflare
browser(action="snapshot", profile="my-daily-chrome", targetId="<targetId>", compact=true)

// Step 3: 從搜尋結果點進詳情頁
browser(action="act", profile="my-daily-chrome", targetId="<targetId>", request={"kind": "click", "ref": "<eXX>"})

// Step 4: 從詳情頁提取 Magnet Hash
```

### 📍 為什麼要用 profile="my-daily-chrome"？

| 方法 | 結果 |
|------|------|
| 直接用 web_fetch | ❌ 被 Cloudflare 阻擋 |
| 用 OpenClaw 預設瀏覽器 | ❌ 也被 Cloudflare 阻擋 |
| **用 `my-daily-chrome` profile** | ✅ 有老爺的 session cookie，可以通過驗證 |

---

## 🚀 完整使用流程

### 方法二：使用瀏覽器（✅ 推薦，100% 成功）

1. 老爺輸入 `/torrent <關鍵字>`
2. 蘇茉用 `profile="my-daily-chrome"` 開啟 BT4G
3. 蘇茉截圖確認 Cloudflare 通過
4. 蘇茉從搜尋結果找有 Seeders > 0 的項目
5. 老爺選擇要下載的項目
6. 蘇茉點進詳情頁提取 Magnet Hash
7. **蘇茉自動加上 22 個公開 Trackers**
8. **直接新增到 qBittorrent** 或存入 output 檔案

---

## 🔍 如何判斷結果是否可以下載？

| Seeders | 狀態 | 動作 |
|---------|------|------|
| **Seeders > 0** | ✅ 可下載 | 繼續流程 |
| **Seeders = 0** | ❌ 無人分享 | 告知老爺無法下載，建議其他關鍵字或等待 |

---

## 📁 輸出位置

```
C:\butler_sumo\docs\torrent\outputYYYYMMDD.txt
```

---

## 🔧 公開 Trackers 清單（22 個）

| # | Tracker URL |
|---|------------|
| 1 | udp://tracker.opentrackr.org:1337/announce |
| 2 | udp://open.stealth.si:80/announce |
| 3 | udp://wepzone.net:6969/announce |
| 4 | udp://tracker.torrent.eu.org:451/announce |
| 5 | udp://tracker.theoks.net:6969/announce |
| 6 | udp://tracker.srv00.com:6969/announce |
| 7 | udp://tracker.dler.org:6969/announce |
| 8 | udp://tracker.darkness.services:6969/announce |
| 9 | udp://tracker.corpscorp.online:80/announce |
| 10 | udp://tracker.bittor.pw:1337/announce |
| 11 | udp://tracker.004430.xyz:1337/announce |
| 12 | udp://t.overflow.biz:6969/announce |
| 13 | udp://leet-tracker.moe:1337/announce |
| 14 | udp://exodus.desync.com:6969/announce |
| 15 | udp://bittorrent-tracker.e-n-c-r-y-p-t.net:1337/announce |
| 16 | udp://6ahddutb1ucc3cp.ru:6969/announce |
| 17 | https://tracker.zhuqiy.com:443/announce |
| 18 | https://tracker.pmman.tech:443/announce |
| 19 | https://tracker.nekomi.cn:443/announce |
| 20 | https://tracker.moeblog.cn:443/announce |
| 21 | https://tracker.bt4g.com:443/announce |

---

## 📋 Magnet Hash 提取方法（重要！）

**千萬不要**直接用 BT4G 搜尋結果的 URL 路徑當作 hash！

### ✅ 正確方法：
1. 從搜尋結果點進**詳情頁**
2. 找下載連結： `/magnet/<40字符十六進制>?name=...`
3. 提取 `/magnet/` 後面的 **40 字符十六進制**

### ❌ 錯誤：
```
# 這是 Base32編碼，不是真正的 info hash！
/magnet/1LuRt7ewlIzfrmpYjylq5cei5qQbgGTkC
```

### ✅ 正確：
```
# 40字符十六進制才是真正的 info hash
magnet:?xt=urn:btih:4f2d8703a94bef29eed88a6b3e3129a7e6695a27
```

---

蘇茉已經學會了！🎉
