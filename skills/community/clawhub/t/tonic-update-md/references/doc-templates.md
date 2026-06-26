# doc-templates.md — Ready-to-use doc templates

## PROJECT-OVERVIEW.md

```markdown
# PROJECT-OVERVIEW.md — 項目總覽

> 每 session 必讀（精簡版）。詳細內容按需讀取對應文件。

---

## 📌 項目基本資料

- **項目名：** <name>
- **域名：** <url>
- **定位：** <one-line description>
- **VM / Hosting：** <host info>
- **狀態：** <emoji + version>

---

## 🛠️ 功能 / 模組

| # | 功能 | 狀態 | 備注 |
|---|------|------|------|
| 1 | <feature> | ⏳ | |

---

## 🏗️ 技術架構

- **Frontend：** <stack>
- **Backend：** <stack>
- **Database：** <db info>
- **Hosting：** <hosting info>

---

## 📁 文檔地圖

| 文件 | 內容 |
|------|------|
| `PROJECT-OVERVIEW.md` | 本文件 — 精簡總覽（每 session 必讀） |
| `PROJECT-DEPLOY.md` | 部署、Docker、Nginx、SSL |
| `PROJECT-APPS.md` | 功能詳細規格 |
| `PROJECT-DB.md` | 數據庫 schema |
| `PROJECT-HISTORY.md` | 版本日誌 |

---

## 🔄 文檔更新規則

| 改動類型 | 需要更新 |
|----------|----------|
| 新功能 / 改功能 | `OVERVIEW`（狀態）+ `APPS` |
| 新版本發布 | `HISTORY` + `OVERVIEW`（版本號）|
| 部署/基礎設施改動 | `DEPLOY` |
| DB schema 改動 | `DB` |

**規則：Deploy 成功 → 立即更新文檔。唔好等，唔好忘。**
```

---

## PROJECT-HISTORY.md

```markdown
# PROJECT-HISTORY.md — 版本日誌

---

## v0.1.0 — YYYY-MM-DD

### 類別（基礎設施 / 功能 / 修復）
- ✅ <item>
- 🔄 <item>
- ⏳ <item>

---

_格式：版本號 — 日期 — 摘要_
_狀態：✅ 完成 | 🔄 進行中 | ⏳ 待開始 | ❌ 取消_
```

---

## PROJECT-DEPLOY.md

```markdown
# PROJECT-DEPLOY.md — 部署指南

---

## 🚀 伺服器資料

- **IP：** <ip>
- **User：** <user>
- **Project Dir：** <path>
- **SSH：** `ssh -i <key> user@ip`

---

## 🐳 Docker

### 啟動
\`\`\`bash
docker build -t <image> .
docker run -d --name <container> --network <net> -p <port>:<port> --env-file .env <image>
\`\`\`

### 更新
\`\`\`bash
git pull && docker build -t <image> .
docker stop <container> && docker rm <container>
docker run -d --name <container> --network <net> -p <port>:<port> --env-file .env <image>
\`\`\`

---

## 🌐 Nginx

Config: `<path>/nginx/conf.d/<project>.conf`

### Reload（不重啟其他服務）
\`\`\`bash
docker exec <nginx-container> nginx -s reload
\`\`\`

---

## 🔒 SSL

- **域名：** <domain>
- **到期：** <date>
- **Auto-renew：** <method>

---

## ✅ 部署 Checklist

- [ ] Build 成功
- [ ] Container 起動正常
- [ ] Nginx config test 通過
- [ ] Nginx reload
- [ ] 網站可訪問
- [ ] 更新 OVERVIEW 版本號
- [ ] 更新 HISTORY
```

---

## PROJECT-DB.md

```markdown
# PROJECT-DB.md — 數據庫設計

---

## 連接資料

- **Host：** <host>
- **Port：** <port>
- **Database：** <db_name>
- **User：** <user>

---

## Schema

### table_name
\`\`\`sql
CREATE TABLE table_name (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  field      VARCHAR(100) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
\`\`\`

---

## 更新規則

- 新增 table / column → 更新本文件
- Migration → 記錄喺 HISTORY
- 永不直接 ALTER PROD，先測試
```
