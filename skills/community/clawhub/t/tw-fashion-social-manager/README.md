# Meta 社群數據抓取設定指南

本文件說明如何從零開始設定 Facebook、Instagram、Threads 的 API 存取權限，
讓 `scripts/fetch_insights.py` 可以自動抓取三平台的貼文數據。

---

## 概覽：需要設定的東西

| 平台 | 設定位置 | 產出 |
|------|---------|------|
| Facebook / Instagram | business.facebook.com | `META_ACCESS_TOKEN` |
| Facebook / Instagram App | developers.facebook.com | App（`META_PAGE_ID`、`META_IG_ACCOUNT_ID` 也在此確認）|
| Threads | developers.facebook.com（獨立 App）| `THREADS_CLIENT_ID`、`THREADS_CLIENT_SECRET`、`THREADS_ACCESS_TOKEN` |

---

## 一、Facebook / Instagram 設定（business.facebook.com）

### 1-1. 建立系統使用者

1. 前往 [business.facebook.com](https://business.facebook.com)
2. 左側選單 → **設定** → **使用者** → **系統使用者**
3. 點「新增」，角色選「**管理員**」

### 1-2. 為系統使用者指派資產

系統使用者建好後：

1. 點進系統使用者 → **新增資產**
2. 選擇「**粉絲專頁**」→ 勾選你的 FB 粉專 → 權限選「**完整控制**」
3. 再次「**新增資產**」→ 選「**應用程式**」→ 勾選你在 developers.facebook.com 建立的 App → 權限選「**開發者**」

### 1-3. 產生永久 Access Token

1. 點進系統使用者 → **產生新的 token**
2. 選擇你的 App
3. 勾選以下 **7 個權限**：

| 權限 | 用途 |
|------|------|
| `instagram_basic` | 讀取 IG 媒體清單 |
| `instagram_manage_insights` | 讀取 IG 貼文／Reels insights |
| `pages_read_engagement` | 讀取 FB 粉專貼文 insights |
| `pages_read_user_content` | 讀取粉專貼文內容 |
| `pages_show_list` | 取得 Page Access Token |
| `read_insights` | 讀取 FB 粉專層級 insights |
| `threads_business_basic` | 讀取 Threads 資料 |

4. 點「產生 token」，複製產生的 token → 存入 `.env` 的 `META_ACCESS_TOKEN`

> ⚠️ **重要**：每次更改權限後都必須重新產生 token，舊 token 不會自動繼承新權限。

---

## 二、Facebook / Instagram App 設定（developers.facebook.com）

這個 App 是用來提供 API 存取能力的，系統使用者 token 必須綁定一個 App 才能使用。

### 2-1. 建立 App

1. 前往 [developers.facebook.com](https://developers.facebook.com)
2. 右上角 → **我的應用程式** → **建立應用程式**
3. 類型選「**其他**」→ 用途選「**企業**」
4. 填入名稱後建立

### 2-2. 確認 App 為開發模式

右上角狀態切換確認是「**開發中（Development）**」。
開發模式下 App 擁有者 / 管理員 / 測試人員不需提交審核即可使用所有權限。

### 2-3. 取得 App ID 與 Secret（備用）

左側 → **設定** → **基本**：

- **應用程式編號** → `META_CLIENT_ID`（目前 script 不使用，可不設定）
- **應用程式密鑰** → `META_CLIENT_SECRET`（目前 script 不使用，可不設定）

> script 使用的是 Business 系統使用者產生的永久 token，不需要走 OAuth 換 token 流程，所以 `META_CLIENT_ID` / `META_CLIENT_SECRET` 可留空。

### 2-4. 取得 Page ID 與 IG Account ID

**PAGE_ID**：
- 前往你的 FB 粉專 → 關於 → 找「粉絲專頁 ID」
- 或在 [Graph API Explorer](https://developers.facebook.com/tools/explorer/) 執行 `GET /{page-name}?fields=id`

**IG_ACCOUNT_ID**：
- 可以直接填 IG 帳號的 username（如 `shop_real_live_authentic`），script 會自動解析成數字 ID
- 或填數字 ID 亦可

---

## 三、Threads 設定（developers.facebook.com，獨立 App）

Threads 有自己獨立的 API（`graph.threads.net`），需要建立一個分開的 App。

### 3-1. 建立 Threads App

1. 前往 [developers.facebook.com](https://developers.facebook.com) → **建立應用程式**
2. 類型選「**Threads**」
3. 建立後取得：
   - **Threads 應用程式編號** → `THREADS_CLIENT_ID`
   - **Threads 應用程式密鑰** → `THREADS_CLIENT_SECRET`

### 3-2. 設定 OAuth 重新導向 URI

1. 左側選單 → **Threads API** → **設定**
2. 在「**有效的 OAuth 重新導向 URI**」加入：`https://localhost/`
3. 儲存變更

> ⚠️ URI 必須完全一致，包含結尾斜線。

### 3-3. 加入測試人員（開發模式必要步驟）

App 在開發模式時，只有被加為測試人員的帳號才能授權：

1. 左側 → **角色** → **測試人員**
2. 加入你的 Facebook 帳號
3. 登入 Facebook 接受邀請

### 3-4. 取得 Threads Access Token（一次性 OAuth 流程）

**步驟 1**：瀏覽器打開以下網址（替換 `YOUR_CLIENT_ID`）：

```
https://threads.net/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=https://localhost/&scope=threads_basic,threads_manage_insights&response_type=code
```

**步驟 2**：用你的 Threads 帳號登入並授權

**步驟 3**：瀏覽器會跳到 `https://localhost/?code=XXXXXX`（頁面顯示無法連線是正常的），複製網址列的 `code` 值

**步驟 4**：用 code 換短效 token：

```bash
curl -X POST "https://graph.threads.net/oauth/access_token" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=https://localhost/" \
  -d "code=你的code"
```

**步驟 5**：用短效 token 換長效 token（有效期 60 天）：

```bash
curl "https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=YOUR_CLIENT_SECRET&access_token=短效token"
```

**步驟 6**：把拿到的長效 token 存入 `.env` 的 `THREADS_ACCESS_TOKEN`

> ⚠️ Threads token 有效期 **60 天**，到期前需重新執行步驟 1-6。
> 未來可考慮加入自動 refresh 機制（`th_refresh_token` grant type）。

---

## 四、.env 設定總覽

在 openclaw 專案根目錄的 `.env` 加入以下變數：

```env
# Facebook / Instagram（Business 系統使用者永久 token）
META_ACCESS_TOKEN=你的系統使用者token
META_PAGE_ID=你的FB粉專ID
META_IG_ACCOUNT_ID=你的IG帳號username或數字ID

# Threads（獨立 App）
THREADS_CLIENT_ID=你的Threads應用程式編號
THREADS_CLIENT_SECRET=你的Threads應用程式密鑰
THREADS_ACCESS_TOKEN=你的Threads長效token
```

---

## 五、執行 script

```bash
cd /path/to/openclaw
source .env
python3 ~/.openclaw/workspace/skills/tw-fashion-social-manager/scripts/fetch_insights.py
```

輸出報告位置：

```
~/.openclaw/workspace/socialMediaManager/reports/weekly_insights_YYYY-MM-DD.xlsx
```

---

## 六、常見錯誤

| 錯誤訊息 | 原因 | 解法 |
|---------|------|------|
| `This endpoint requires the 'pages_read_engagement' permission` | token 缺少權限，或權限新增後沒有重新產生 token | 在 business.facebook.com 確認權限後重新產生 token |
| `Tried accessing nonexisting field (threads)` | 使用了 FB Graph API 抓 Threads 資料（錯誤端點）| 確認 `THREADS_ACCESS_TOKEN` 已設定，script 會改用 `graph.threads.net` |
| `The user has not accepted the invite to test the app` | 測試人員未接受邀請 | 登入 Facebook 接受 App 測試人員邀請 |
| `redirect_uri` 不在白名單 | URI 不完全一致 | 確認 developers.facebook.com 的 URI 和授權網址一模一樣（含斜線）|
| `Session key invalid` | 嘗試 refresh 已是長效的 token | 正常現象，長效 token 不需 refresh，可忽略 |
