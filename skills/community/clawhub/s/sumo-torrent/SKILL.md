# SKILL.md - Torrent Search Skill

## 版本
1.1.0

## 功能
搜尋 BT4G 上的 Torrent 檔案，並輸出含 Trackers 的 Magnet 連結。

## 觸發指令
`torrent <關鍵字>` 或 `/torrent <關鍵字>`

---

## ⚠️ 重要：遇到 Cloudflare 必須用瀏覽器！

### 🚨 瀏覽器使用順序（重要！）

**遇到瀏覽器超時或失敗時，按以下順序嘗試：**

1. **先試預設 browser（不用 profile）**
   ```javascript
   browser(action="open", url="https://bt4gprx.com/search?q=關鍵字")
   ```

2. **如果失敗，再嘗試 profile="my-daily-chrome"**
   ```javascript
   browser(action="open", profile="my-daily-chrome", url="https://bt4gprx.com/search?q=關鍵字")
   ```

3. **不要堅持用同一個 profile 不放** - 換個方式試

### 📍 為什麼？

| 方法 | 適合情況 |
|------|---------|
| 預設 browser | Gateway 重啟後、瀏覽器正常的時候 |
| `profile="my-daily-chrome"` | 有 Cloudflare 驗證需要老爺 session 時 |

### 🚨 Cloudflare 錯誤時的處理流程

當遇到以下錯誤時：
- `Cloudflare` 驗證頁面
- `403 Forbidden`
- web_fetch / torrent_search.py 失敗

**必須立即切換到瀏覽器方法：**

```javascript
// Step 1: 用瀏覽器開啟 BT4G（先試預設）
browser(action="open", url="https://bt4gprx.com/search?q=關鍵字")

// Step 2: 截圖確認通過 Cloudflare
browser(action="snapshot", targetId="<targetId>", compact=true)

// Step 3: 從搜尋結果點進詳情頁
browser(action="act", targetId="<targetId>", request={"kind": "click", "ref": "<eXX>"})

// Step 4: 從詳情頁提取 Magnet Hash
// Magnet Link URL 格式：/magnet/<40字符info_hash>
```

| 方法 | 結果 |
|------|------|
| 直接用 web_fetch | ❌ 被 Cloudflare 阻擋 |
| 用 OpenClaw 預設瀏覽器 | ❌ 也被 Cloudflare 阻擋 |
| **用 `my-daily-chrome` profile** | ✅ 有老爺的 session cookie，可以通過驗證 |

---

## ⚠️ 重要：統一由總管蘇茉處理

**所有蘇茉分身的 `/torrent` 指令都應該發給總管蘇茉處理！**

原因：
1. 總管蘇茉已通過 Cloudflare 驗證，使用 `my-daily-chrome` Profile
2. 避免瀏覽器衝突（Race Condition）
3. 確保搜尋成功

### 其他蘇茉應該這樣做：

當收到 `/torrent <關鍵字>` 時，**不要自己搜尋**，而是：

```
【我是XXX蘇茉，來自群組 ID：XXXXXXXX】
請幫我搜尋 torrent：<關鍵字>
```

或者簡單告訴老爺：「這個任務蘇茉會轉交給總管蘇茉處理，請稍候！」

## 使用範例
```
/torrent waaa087
/torrent cawd-942
```

## 🚀 完整使用流程

### 方法一：使用 torrent_search.py（遇到 Cloudflare 時失敗）

```bash
python C:\butler_sumo\Tools\torrent_skill\torrent_search.py "關鍵字" "C:\butler_sumo\docs\torrent"
```

**失敗時的特徵：**
- UnicodeEncodeError
- 403 Forbidden
- Cloudflare 驗證頁面

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

## 📁 輸出格式

### 搜尋結果
1. 蘇茉搜尋 BT4G 網站
2. 列出有活躍度（Seeders > 0）的結果
3. 等待老爺選擇要下載的項目
4. **蘇茉自動將選擇的 Magnet 連結加上 22 個公開 Trackers**
5. 將含 Trackers 的完整連結存入 `C:/butler_sumo/docs/torrent/outputyyyymmdd.txt`

### 輸出檔案格式
```
# Torrent Search Results - 2026-04-01
# ================================
# 蘇茉已自動加上 22 個公開 Trackers
# 可直接貼給 qBittorrent 使用！

# 1. magnet:?xt=urn:btih:XXXXXXXXXX&dn=NAME&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://open.stealth.si:80/announce&...
```

### 🎯 直接新增到 qBittorrent（新功能！）
蘇茉可以直接將 magnet link 新增到 qBittorrent，不需要老爺手動複製貼上！

**工具位置**：`C:\butler_sumo\Tools\torrent_skill\add_to_qbittorrent.py`

**qBittorrent 設定**：
- Port：8080
- 帳號：admin
- 密碼：adminadmin（建議改成更強的密碼！）

---

## 📁 輸出位置

```
C:\butler_sumo\docs\torrent\outputYYYYMMDD.txt
```

---

## 🔧 公開 Trackers 清單（22 個）

蘇茉已內建以下 22 個公開 Trackers：

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

## 💡 為什麼要加 Trackers？

因為 BT4G 提供的 Magnet 連結**沒有包含 Trackers**，需要自己加上公開 Trackers 才能讓 qBittorrent 順利找到 peers 進行下載。

---

## 📋 Magnet Hash 提取方法（重要！）

**千萬不要**直接用 BT4G 搜尋結果的 URL 路徑當作 hash！

### ✅ 正確方法：
1. 從搜尋結果點進**詳情頁**
2. 找下載連結：`/magnet/<40字符十六進制>?name=...`
3. 提取 `/magnet/` 後面的 **40 字符十六進制**（不是 URL path 裡的 32 字符 Base62！）

### ❌ 錯誤示範：
```
# 這是 Base32編碼，不是真正的 info hash！
/magnet/1LuRt7ewlIzfrmpYjylq5cei5qQbgGTkC
```

### ✅ 正確示範：
```
# 40字符十六進制才是真正的 info hash
magnet:?xt=urn:btih:4f2d8703a94bef29eed88a6b3e3129a7e6695a27
```

---

## 🔒 安全提醒

- qBittorrent WebUI 密碼預設是 `admin/adminadmin`
- **不要**將 qBittorrent WebUI 暴露到網路上
- 建議使用強密碼

---

蘇茉已經學會了！🎉
