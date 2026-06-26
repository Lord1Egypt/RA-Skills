---
name: withme-youtube
description: "With me. YouTube 频道 Lofi 氛围视频制作全流程。小米（Content）全权调度，从选题到发布一条龙。含 AI 图片生成、Envato 音频下载、FFmpeg 合成、SEO 资料包、YouTube 上传排程、Shorts 切片。触发词：withme、lofi视频、氛围视频、YouTube发布、开始制作、V{N}。"
---

# With me. YouTube 视频制作工作流 v2.0

## 核心原则

**小米（Content）是制作总指挥。** Ken 只在关键节点审核，其余全自动。
Main 不参与具体制作，只在跨部门协调时介入。

## 项目路径

```
~/Projects/withme-youtube/
├── audio/v{N}/           ← 音频素材（音乐+环境音+氛围音）
├── images/originals/v{N}/ ← AI 生成原图
├── images/4k-upscaled/v{N}/ ← 4K 放大版
├── videos/v{N}/          ← 制作中间文件
├── licenses/v{N}/        ← Envato 授权证书
├── thumbnails/v{N}/      ← YouTube 封面
├── scripts/              ← FFmpeg 构建脚本
└── exports/              ← 最终导出
```

## Agent 分工

| 任务 | 负责 | 说明 |
|------|------|------|
| 选题/策划/全流程调度 | **小米（Content）** | 总指挥 |
| 场景 Prompt 优化 | @designer | 小米直接调度 |
| AI 图片生成 | @designer → exec | 小米派 designer，designer 直接 exec generate_image.py |
| 4K 放大 | @designer → exec | 使用放大工具 |
| Envato 音频搜索+下载 | @research → browser | 用 browser 工具访问 Envato（Ken 账号已登录） |
| FFmpeg 合成脚本 | 小米 | 复制模板 + 填参数 |
| FFmpeg 执行 | Ken / exec | 本地算力执行 |
| 封面制作 | @designer | 3 个备选 |
| 标题/描述/SEO | @seo | 品牌格式 + 30 标签 |
| 翻译 | @writing | 英文→繁中 |
| YouTube 上传 | exec youtube_upload.py | 脚本自动上传+排程 |
| Shorts 切片 | 小米 | 参考 youtube-shorts skill |

## 品牌标题体系

格式：`With me. | [Mood] — [Scene Description] [Emoji] [Duration] [Resolution]`

示例：`With me. | Rainy Night — Tropical Rainforest Ambience 🌧️ 2 Hours 4K`

---

## 制作流程（8 阶段）

### 阶段 1：选题 ⏱️ 即时

1. 读取 `HANDOFF-FROM-MAIN.md`（如有）获取主题
2. 从情绪×空间矩阵选择组合（见 `references/content-matrix.md`）
3. 向 Ken 确认：「即将开始制作 V{N}：{主题}，确认启动？」
4. Ken 回「好/确认/go」→ 进入阶段 2

### 阶段 2：AI 图片生成 ⏱️ ~10 分钟

1. 根据主题确定 5 个场景描述
2. 派 @designer 优化 prompt（构图、光影、色调、镜头参数）
3. **designer 直接执行生图：**
```bash
GEMINI_API_KEY="$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['models']['providers']['google']['apiKey'])")" \
uv run /Users/withme/.openclaw/shared/generate_image.py \
  --prompt "<prompt>" \
  --filename "~/Projects/withme-youtube/images/originals/v{N}/scene_{i}.png" \
  --resolution 2K
```
4. 生成完毕发给 Ken 预览
5. Ken 确认 / 要求修改 → 调整后重新生成

**⚠️ 不写 pending.json，不等 Main 巡检。**

### 阶段 3：4K 放大 ⏱️ ~15 分钟

1. 将 5 张图放大至 ≥3840×2160（支持 Ken Burns 裁切）
2. 存入 `~/Projects/withme-youtube/images/4k-upscaled/v{N}/`

### 阶段 4：音频准备 ⏱️ ~30 分钟（全自动）

> Envato 下载需 CDP + browser 配合，流程已验证可行。

1. 根据主题情绪确定搜索关键词（参考 `references/content-matrix.md`）
2. 用 `browser` 工具搜索 Envato Music，筛选 Claim Clear 曲目
3. **自动下载流程（每首重复）：**
```python
# Step 1: 用 CDP 设定下载路径（每个 page target 需单独设定）
import asyncio, json, websockets, urllib.request
targets = json.loads(urllib.request.urlopen("http://127.0.0.1:18800/json").read())
page_ws = [t["webSocketDebuggerUrl"] for t in targets if "envato" in t.get("url","")][0]
async with websockets.connect(page_ws) as ws:
    await ws.send(json.dumps({"id":1,"method":"Network.enable"}))
    await ws.recv()
    await ws.send(json.dumps({"id":2,"method":"Page.setDownloadBehavior",
        "params":{"behavior":"allow","downloadPath":"<目标目录>"}}))
    await ws.recv()
    # Step 2: JS 点击 Download 按钮
    await ws.send(json.dumps({"id":3,"method":"Runtime.evaluate",
        "params":{"expression":"document.querySelectorAll('button').forEach(b=>{if(b.textContent.trim()==='Download')b.click()})"}}))
    # Step 3: 等待下载完成（监听文件出现）
```
4. 下载清单：
   - **5-6 首主题音乐**（总循环 ~2 小时）
   - **1 个环境音循环**（雨声/海浪/壁炉/鸟鸣等）
   - **1 个氛围音循环**
5. 下载后自动解压 ZIP → 存入 `~/Projects/withme-youtube/audio/v{N}/`
6. 发送曲目清单给 Ken 确认

**⚠️ 关键：必须用 `Page.setDownloadBehavior`（非 Browser 级），必须用 `browser` 工具（`web_fetch` 会被 Cloudflare 403）。**

### 阶段 5：FFmpeg 合成 ⏱️ ~5 分钟出脚本

1. 复制 `scripts/build-template.sh` → `scripts/build-v{N}.sh`
2. 填入实际路径（图片、音频、输出）
3. 设定参数：
   - 总时长 7200 秒（2 小时）
   - 5 场景各 1440 秒，Ken Burns 缓动
   - 场景间 3 秒交叉淡入淡出
   - 音量：音乐 -20dB / 环境音 -16dB / 氛围音 -22dB
   - 开头 10 秒淡入，结尾 30 秒淡出
   - 输出：4K H.264 CRF 18 + AAC 192k
4. 发给 Ken 审核后执行

### 阶段 6：封面 + 发布资料包 ⏱️ ~15 分钟（可与阶段 5 并行）

1. 派 @designer 制作 1280×720 封面（3 个备选）
2. 派 @seo 准备：
   - **标题** — 品牌格式
   - **英文描述** — 氛围叙事 + 时间戳 + 使用场景 + 频道介绍 + Envato credit block
   - **30 个标签** — 高流量/中竞争/长尾三层
3. 派 @writing 翻译繁中版
4. 整合为 `memory/youtube-publish-v{N}.md`
5. 发给 Ken 选封面 + 审核

### 阶段 7：上传排程 ⏱️ ~5 分钟

1. Ken 确认成品后，写入上传队列：
```json
// ~/.openclaw/shared/upload-queue.json
{
  "title": "With me. | ...",
  "file": "~/Projects/withme-youtube/exports/v{N}.mp4",
  "thumbnail": "~/Projects/withme-youtube/thumbnails/v{N}.jpg",
  "description": "...",
  "tags": ["..."],
  "publishAt": "下周五 10:00 GMT+8",
  "status": "pending"
}
```
2. 上传脚本：`~/.openclaw/shared/youtube_upload.py`
3. OAuth 凭证：`~/.openclaw/shared/youtube_client_secret.json`
4. Google 账号：`kylin1986@gmail.com`

### 阶段 8：Shorts 切片 ⏱️ ~10 分钟（上传后自动）

1. 从成品影片切出 5 支 Shorts（每支 30 秒，各场景一支）
2. 制作 Shorts 标题/描述（参考 youtube-shorts skill）
3. 排程：每周 3-5 条，穿插在工作日

---

## Ken 手动介入的节点（3 个）

| 节点 | 原因 |
|------|------|
| 阶段 1 确认主题 | 确保方向正确 |
| 阶段 5 审核 FFmpeg 参数 | 本地算力 + 美学微调 |
| 阶段 6 选封面 + 审核资料包 | 最终品质把关 |

## 全自动节点

- 图片生成 + 放大（@designer exec）
- Envato 音频搜索+下载（@research browser + CDP）
- SEO 资料包（@seo）
- 翻译（@writing）
- YouTube 上传排程（youtube_upload.py）
- Shorts 切片

---

## 状态追踪

每个阶段完成后更新 `memory/youtube-progress-v{N}.md`：
```markdown
# V{N} 制作进度 — {主题}
- [x] 阶段 1：主题确认 ✅ 2026-03-XX
- [x] 阶段 2：图片生成 ✅ 5/5 张
- [ ] 阶段 3：4K 放大
- [ ] 阶段 4：音频准备
- [ ] 阶段 5：FFmpeg 合成
- [ ] 阶段 6：封面+资料包
- [ ] 阶段 7：上传排程
- [ ] 阶段 8：Shorts 切片
```

---

## 发布设定

### 排程
- **每周五 10:00 台湾时间 (GMT+8)**
- 对应北美周四 18:00 PST

### YouTube Studio 设定
- 类别：音乐
- 语言：English
- Made for Kids：否
- 允许嵌入：是
- 通知订阅者：是
- 评论：开启 / 基本管理

### 音乐数量指南
- **最低 5-6 首**（单循环 ~15 分钟）
- 3 首循环感明显，影响留存
- 甜区：5-8 首

### 发布后检查
- [ ] 确认排程时间正确
- [ ] 繁中翻译填入 Translations
- [ ] 版权检测通过，有 claim 用 License PDF 争议
- [ ] Shorts 排程就位

---

## 一键触发

Ken 或 Main 发送：「开始制作 V{N}：{主题}」
小米自动执行阶段 1-8，仅在 3 个节点暂停等 Ken 确认。
