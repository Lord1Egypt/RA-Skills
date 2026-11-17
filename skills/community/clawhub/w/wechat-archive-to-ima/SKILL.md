---
name: wechat-archive-to-ima
slug: wechat-archive-to-ima
displayName: 微信聊天记录图片文件归档到ima知识库
summary: 把微信PC端已落地的聊天附件按联系人归类、批量上传ima知识库或Obsidian；.dat加密图片一键解密，实测3898/3898成功。
description: >-
  把用户微信 PC 端已经落地到本地的聊天附件（图片、视频、文档）做系统化归档，
  按联系人归类，并同步上传到腾讯 ima 知识库（OpenAPI）或本地 Obsidian 库。
  适用场景：(1) 用户说"帮我整理微信里跟某人的所有资料/文件/图片"；
  (2) 用户说"把微信聊天里的合同、发票、会议纪要归档到知识库"；
  (3) 用户说"微信收到的文件太多找不到，帮我分类"；
  (4) 用户给了 ima 的 ClientID / APIKey，要求把本地资料批量入库；
  (5) 用户要对已归档的微信资料做摘要、合同条款提取、待办清单、客户画像分析；
  (6) 用户说"帮我把微信里所有人的附件都整理到电脑"；
  (7) 用户说"微信存下来的图片是 .dat 打不开，帮我解出来"（已支持：自动推导 code 并解密）。
  **不适用**：解密微信加密数据库（message_*.db / contact.db）、读取用户未在 PC 端打开过的消息、
  远程操作手机微信、抓内存密钥、导出聊天正文 —— 这些一律不做，
  遇到这类要求直接说明边界并给替代方案。
version: 1.0.0
author: 初五Agent
tags: [微信, ima, 附件归档, 图片解密, 知识库, wechat, ima-knowledge-base]
license: MIT
---


# 微信本地附件归档到 ima / Obsidian

## 核心原则（必须先读）

1. **只整理已经落地到本地磁盘的附件文件**。微信 PC 端把图片/文件下载到本地后是明文文件，
   可以直接读、复制、改名、分类。没有下载到本地的附件，本 skill 不做。
2. **不碰加密数据库**。`db_storage\message_*.db`、`contact.db` 是 SQLCipher 4 加密的，
   不破解、不 dump 内存密钥、不调用第三方解密工具。
3. **.dat 图片缓存已支持解密**。微信 4.x 把图片存成 V2 头的 .dat（单账号常见 3800+ 个），
   `scripts/wechat_dat_decrypt.py` 自动探测 .dat → 尾字节反推 xor → 枚举 wxid 候选
   → 推导 code（下界 0）→ 批量解密 → PIL 校验，实测 **3898/3898 成功、0 失败，
   PIL 3104/3104 全部可打开**（jpg 2689 / wxgf 794 / png 415）。
   `organize_attachments.py` 默认仍只列清单，加 `--decrypt` 才解密归档。
4. **手机端备份必须用户本人操作**。智能体碰不到用户手机。
5. **wxid/hash → 备注名映射需要用户配合一次**。本地按 hash 分目录，但映射在加密的 contact.db 里。
6. **ima API Key 等同账号权限**。任务结束提醒用户轮换 Key。

---

## 实测过的真实目录结构（微信 4.1.x Windows）

数据根目录（**注意：不在 Documents 下**）：
```
<用户主目录>\xwechat_files\<微信号>_<hash>\
```

账号下一级目录：
```
├── apm_record\      （APM 监控，忽略）
├── business\        （业务数据）
├── cache\           （缓存）
├── config\          （配置）
├── db_storage\      （加密数据库 ★ 不碰）
├── msg\              （★ 附件都在这）
│   ├── attach\<hash>\   ← 230 个联系人/群，每个目录是一个人的图片和文件
│   ├── file\YYYY-MM\    ← 文档按月分（通常为空，文档实际在 attach 下）
│   ├── video\YYYY-MM\   ← 视频按月分（同上）
│   └── migrate\       ← 3.x 迁移过来的孤儿文件
├── resource\
└── temp\
```

**实测样例**（2026-10-06 在本机跑出来的）：
- 账号目录 `<账号目录>`：账号总 2.1 GB，`msg\attach\` 3909 个文件
- `attach\` 下有 **230 个 hash 子目录**（即 230 个联系人/群）
- **明文文件散在 4 个源，不止 attach**（关键，别只跑 attach）：

| 源目录 | 文件数 | 主要内容 |
|---|---|---|
| `msg\attach\` | 3909 | .dat 3848（图片缓存，**可用 --decrypt 解出**）、pdf 14、pptx 7 |
| `msg\video\` | **299** | **jpg 208、mp4 91** |
| `msg\file\` | **72** | pdf 35、docx 13、pptx 11、xlsx 6 |
| `cache\` | 193 | jpg 33、.dat 50 |

  实跑归档结果：只跑 `attach\` 得到 **61 个**明文；跑全 4 源得到 **509 个**（attach 61 +
  video 261 + file 49 + cache 138），**8.3 倍**。另有 66 个重复文件进 `99-duplicates/`。
- 时间分布：主要集中在 2026-04 ~ 2026-09

---

## 完整工作链路

```
阶段 0：环境探测（智能体做，5 分钟）
   ↓
阶段 1：用户手动把附件下载到本地（用户做，可能几小时）
   ↓
阶段 2：列联系人 hash 清单，用户指认备注名（智能体+用户，10 分钟）
   ↓
阶段 3：本地整理（智能体做，10~60 分钟）
   ↓
阶段 4：双轨入库（智能体做）
   ├─ 4A：Obsidian 本地库
   └─ 4B：ima 知识库（OpenAPI）
   ↓
阶段 5：分析与总结（按需）
```

---

## 阶段 0：环境探测

执行 `scripts/detect_wechat_paths.py`，会自动找出：
- 微信安装路径（注册表）
- 数据根目录（候选：`~/xwechat_files/`、`~/Documents/xwechat_files/`、`~/Documents/WeChat Files/`）
- 当前活跃账号（按最近修改时间排序）
- msg 下的联系人 hash 目录数、文件总数、总大小
- 按月份的附件分布

**不要凭猜写路径**。每个用户电脑路径不同，必须先跑脚本拿真值。

---

## 阶段 1：让附件真正落地到本地

**问题**：很多用户的 msg\attach\ 下文件不多，是因为微信默认只在用户点开图片/文件时才下载。

**两条路（选一条）**：

### 路径 A：开"自动下载"设置 + GUI 批量滚动
1. 让用户在电脑微信 → 设置 → 文件管理 → 打开**自动下载**（图片/视频/文件全开）
2. 智能体用桌面自动化（computer_use）逐个打开聊天窗口，滚动到顶/到底
3. 后台等几分钟，让附件下载完

**适合**：全量整理所有人的附件。但 230 个联系人逐个滚动要几小时。

### 路径 B：手机备份 + PC 端窗口触发
1. 用户在手机发起"备份到电脑"
2. 备份完后，电脑微信打开几个重要联系人窗口滚一遍
3. 附件落地后开始整理

**适合**：先挑几个重要联系人试水。

**注意**：用户如果想全量整理，推荐路径 A，但要做好"几小时跑批"的心理准备。

---

## 阶段 2：hash → 备注名映射（关键步骤）

`attach\<hash>\` 下每个 hash 目录就是一个联系人/群，但 hash 没有备注名。

**三种解决方案**：

1. **活跃度排行法（推荐）**：跑 `scripts/detect_wechat_paths.py --rank-contacts`，
   列出所有 hash 目录按文件数、最近修改时间排序，用户从 TOP 20/50 里指认常用的人。
2. **时间特征法**：用户说"我上周跟张三聊了很多"，脚本找最近一周有大量文件的 hash 目录，
   让用户确认。
3. **最笨但最稳**：用户列出想整理的几个联系人备注名，脚本把候选 hash 列出来，
   用户逐个指认。

**绝对不要尝试读 contact.db 去解密**。

---

## 阶段 3：本地整理

**必须扫全账号 4 个源**（只跑 `attach\` 会漏掉 8.3 倍明文文件）：

```bash
ACCOUNT="$HOME/xwechat_files/<账号目录>"
for SRC in "msg/attach" "msg/video" "msg/file" "cache"; do
  python scripts/organize_attachments.py \
    --src "$ACCOUNT/$SRC" \
    --dst "<输出目录>/$SRC" \
    --contact "$SRC"
done
```

参数说明（注意：参数名是 `--contact`，**不是** `--contact-hash`）：
- `--src` 传的是**该源目录**，脚本会用 `rglob` 递归遍历其下所有层级（含 `attach\<hash>\2026-09\Img\`）
- `--contact` 只写进日志/README，传源目录名即可；按联系人分组时传该 hash
- 默认**移动**文件，预览/试跑请加 `--copy`
- 要把 `.dat` 也解出来，追加 `--decrypt`（见下面"解密 .dat"）

### 解密 .dat（--decrypt 开关）

```bash
# 第一步：单独跑解密，拿到 code（写到 <输出目录>/secret_hit.json，只留在本机）
python scripts/wechat_dat_decrypt.py \
  --account "$ACCOUNT" \
  --out "<输出目录>/dat-decrypted"

# 第二步：归档时直接复用，二次使用秒出
python scripts/organize_attachments.py \
  --src "$ACCOUNT/msg/attach" \
  --dst "<输出目录>/msg/attach" \
  --contact "attach" --decrypt \
  --key-file "<输出目录>/dat-decrypted/secret_hit.json"
```

- `wechat_dat_decrypt.py` 参数：`--account <账号目录>`、`--out <输出目录>`、
  `[--wxid 候选]`、`[--code 已知code]`、`[--timeout 秒]`；已知 code 时跳过暴力推导
- `organize_attachments.py --decrypt` 可用 `--code` / `--key-file` / `--wxid` 直接给密钥，
  一个都不给就自动推导（默认超时 300s，`--decrypt-timeout` 可调）
- 源目录**只读**，解密产物只写 `--out` / `--dst`

它会：
- **不加 `--decrypt`（原行为）**：跳过 `.dat`，记录到 `00-index/dat_files.csv`
- **加 `--decrypt`**：解出 `.dat` 后按 `YYYY-MM/类型/` 正常归档（jpg/png 进 `02-images/`，
  wxgf 动图进 `05-misc/`），解密失败的才留在 `dat_files.csv` 并标注原因
- 把明文文件（pdf/docx/xlsx/pptx/jpg/mp4）按 `YYYY-MM/类型/` 分子目录
- 重命名为 `YYYYMMDD-<原文件名>`
- SHA256 去重，重复文件移入 `99-duplicates/`
- 生成 `index.csv` 和 `README.md`

输出目录结构：
```
<输出目录>/
├── 00-index/
│   ├── README.md
│   ├── index.csv
│   ├── dat_files.csv          ← 未解密/解密失败的 .dat 清单（加 --decrypt 后通常为空）
│   └── secret_hit.json        ← --decrypt 命中的 code（本机复用，不要外发）
├── 01-documents/    (.docx .pdf .xlsx .pptx)
├── 02-images/       (.jpg .png)
├── 03-videos/       (.mp4 .mov)
├── 05-misc/
└── 99-duplicates/
```

---

## 阶段 4A：入 Obsidian（可选）

如果用户指定了 Obsidian 库路径：
- 把输出目录整个复制到 `<Obsidian库>/豆包工作成果/03-知识沉淀/微信归档/<备注名>/`
- 生成 `index.md`，frontmatter 写好来源、联系人、时间范围、文件数、标签
- 附件用相对路径 `![[文件名]]` 引用

---

## 阶段 4B：入腾讯 ima 知识库

**用户必须提供 4 个参数**（缺一不可）：
- `client_id`：从 https://ima.qq.com/agent-interface 生成
- `api_key`：同上
- `knowledge_base_id`：ima 网页进入目标库，URL 中复制
- `folder_id`：目标文件夹 ID（可选）

跑 `scripts/ima_upload.py`：
- 单文件 ≤ 50 MB
- PDF ≤ 1000 页
- QPS 限流：每秒 1 个，失败重试 3 次
- 失败清单写入 `upload_failed.csv`

详细 API 参数见 `references/ima_api.md`。

---

## 阶段 5：分析与总结（按需）

| 分析类型 | 输入 | 输出 |
|---|---|---|
| 合同关键条款提取 | 01-documents/*.docx/pdf | 甲乙方、金额、期限、违约条款表 |
| 发票/收据清单 | 01-documents 里的发票类 | 开票方、金额、日期、税额表 |
| 会议纪要要点 | 文档 | 决议、待办、责任人 |
| 客户画像 | 整个归档目录 | 职业、关注点 |
| 往来款流水 | 发票 + 转账截图 | 按时间排的流水表 |

**注意**：聊天文字本 skill 不导出。要文字记录，用户自己用 WeChatMsg 跑一遍（开源免费），
导出 HTML/Word 后给智能体整理。

---

## 边界与免责（第一次回复用户时必须说清楚）

| 事项 | 可行度 | 说明 |
|---|---|---|
| 自动定位本地附件目录 | 100% | 脚本直接遍历 |
| 整理明文附件（pdf/docx/jpg/mp4） | 100% | 明文文件 |
| 入 Obsidian | 100% | 本地写文件 |
| 入 ima | 90% | 需 API Key |
| hash → 备注名映射 | 60% | 通常要用户指认一次 |
| 解密 .dat 图片 | 100% | **已支持**：自动推导 code 并解密，实测 3898/3898、PIL 100% |
| 提取聊天文字 | 30% | 依赖用户手动导出或 WeChatMsg |
| 读加密 message.db | 0% | **做不到，不承诺**：聊天正文当前解不开 |
| 远程操作手机 | 0% | 做不到 |
| 找回云端过期附件 | 0% | 救不回 |

---

## 参考文件索引

- 路径对照、版本差异、实测结构：`references/wechat_paths.md`
- ima OpenAPI 完整参数、错误码、调用示例：`references/ima_api.md`
- 可行性反推论证全过程：`references/feasibility.md`
- .dat V2 格式、code 推导原理、两个关键坑与真实边界：`references/dat_decryption.md`

**只有需要时才读对应 reference**，不要一次全加载到上下文。
