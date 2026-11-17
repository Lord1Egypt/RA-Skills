---
name: campus-info
description: 清华校内信息查询。查看校内通知（分类）+ 水木搜索（馆藏图书检索）。当用户需要"校内通知、重要公告、放假安排、搜书、找图书馆藏书、水木搜索"时使用。
metadata:
  openclaw:
    requires:
      env:
        - CAS_PASSWORD
    os:
      - windows
      - macos
      - linux
---

# 信息查询

校内通知查询（info 门户）+ 水木搜索（馆藏检索）。

## 如果你是 AI，请阅读以下内容

### 铁律

- **铁律 1：AI 运行所有脚本**。禁止让用户敲命令。
- **铁律 2：脚本面向 AI**。stdout 输出 JSON，进度写 `runtime/logs/campus.log`，不写 stderr。
- **铁律 3：验证码两阶段**。登录触发 2FA 时返回 pending，AI 问用户拿码后 `login.py --submit-code`。
- **铁律 4：全程无头 + 即用即退**。base-cas 一律 headless 运行。浏览器用完即关，保留 session cookie 文件 + profile 指纹；仅 2FA 登录流程内保持打开。

### 使用

```
info.py notices [--category 重要公告] [--limit N]  # 通知列表（需登录）
info.py read --xxid <id>                           # 通知详情全文（需登录）
info.py search --query <词> [--limit N]            # 水木搜索（馆藏检索，公开）
```

输出 JSON：`notices`（xxid/标题/链接）、`read`（全文文本）、`search`（书名/作者/类型/年份）。

### 工作流

```
用户: 最近有什么校内通知 / 放假安排
AI:
  1. info.py notices → 通知列表
  2. 要详情 → info.py read --xxid
  3. 汇总（如放假调课安排）

用户: 帮我搜一本书 / 图书馆有没有 XX
AI:
  1. info.py search --query <词> → 馆藏结果
  2. 汇报书名/作者
```

### 通知分类

重要公告 / 办公通知 / 综合信息 / 教务通知 / 科研通知 / 招标招租

### 技术链路

- **通知登录**：base-cas info（webvpn → CAS，信任浏览器免 2FA）。info 是**整页 CAS**（非 iframe）。
- **通知列表**：`/f/info/xxfb_fg/xnzx/template/more?lmid=<分类id>` → 解析 `xxid` 链接
- **通知详情**：`/f/info/xxfb_fg/xnzx/template/detail?xxid=<id>` → body 全文
- **水木搜索**（公开，无需登录）：Primo explore `tsinghua-primo.hosted.exlibrisgroup.com.cn`，检索 API `/primo_library/libweb/webservices/rest/primo-explore/v1/pnxs`
  - **注意**：pnxs 手动 fetch 403（参数不全），需**真实浏览器导航**（填检索框+回车）捕获响应解析
  - 响应 `docs[].pnx.display`（title/creator/type/creationdate）
- 分类 lmid：重要公告=LM_XJ_ZYGG_UNION / 办公通知=LM_XJ_BGTZ / 综合信息=LM_XJ_ZHXX

> 注意：info 直连（info.tsinghua.edu.cn）会被重定向到 CAS（本机/机房 IP），必须走 base-cas info 登录。水木搜索（Primo）公开可检索。

### 边界

- 通知查询需登录；水木搜索公开。
- 详情返回纯文本（附件/图片未处理）。

---

## 如果你是用户，请阅读以下内容

对 AI 说：
- **"最近有什么通知"** / "放假安排" — 校内通知
- **"看一下那条通知"** — 通知详情
