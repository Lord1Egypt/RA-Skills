---
name: wechat-chat-export-mac
slug: wechat-chat-export-mac
displayName: 微信聊天记录导出·原图视频批量
description: 当用户要把微信里某个联系人、某段时间的文件图片视频批量下载到本地时用。指定联系人+日期范围，自动定位会话、批量点开原图、V2三段解密转码、按项目归档并验收缺口为0；实战单次导出1216文件163.9MB。适用微信桌面版4.x，仅macOS。
summary: 微信聊天记录批量导出：文件+原图+视频，解密转码后按项目归档，验收缺口0。
version: 1.0.0
license: MIT
author: 初五Agent
category: office-efficiency
tags: [微信, 微信聊天记录, 导出, 聊天记录导出, 原图, 视频下载, 知识库归档, macOS, 自动化]
metadata:
  hermes:
    tags: [wechat, export, knowledge-base, macos, automation]
---

# 微信聊天记录批量导出（macOS 桌面版）

把指定联系人 + 日期范围内的**文件 / 图片原图 / 视频**批量下载到本地，解密转码后归档或导入知识库。

> 实战基准：单次导出 **1216 个文件 / 163.9MB**（79 文档 + 525 原图 + 504 缩略图 + 25 视频），缺口 0。

## When to Use

- 甲方/项目要归档某个微信联系人发来的合同、图纸、财务表
- 要把微信资料灌进 IMA / 飞书 / Notion 等知识库
- 微信自带「聊天记录迁移/备份」太慢、且不给散文件
- 取证、审计、离职交接需要原始文件

## 环境要求（缺一不可）

| 项 | 要求 |
|---|---|
| 系统 | macOS（Intel/Apple Silicon 均可），微信 **桌面版 4.x** |
| Python | 3.10+，装 `pyobjc-framework-Quartz`、`Pillow`、`pycryptodome` |
| 外部工具 | `ffmpeg`（转码 wxgf）、`osascript`（AppleScript） |
| 权限 | **辅助功能** + **屏幕录制**（系统设置 → 隐私与安全性），给 Python/终端 |
| 供电 | `caffeinate -d -i -u -s` 或关自动锁屏（长任务会被锁屏打断） |
| 微信状态 | **目标联系人会话已打开、窗口存在**；登录态在本地 |

Windows 版路径与加密不同，本 skill 仅验证 macOS。

## 一、数据路径（先定位这三处）

```bash
BASE=~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<你的wxid>/
# 1) 图片（原始加密块）
$BASE/msg/attach/<会话hash>/<YYYY-MM>/Img/*.dat
# 2) 视频
$BASE/msg/video/<YYYY-MM>/*.mp4  +  封面 *.jpg
# 3) 图片缓存（点开过的完整图）
$BASE/cache/<YYYY-MM>/Message/<会话hash>/Bubble/*.dat
```

**关键规则：微信按「消息月份」分目录**，不是按文件 mtime。目录名 `2026-10` = 消息发于 10 月。

定位参数（`scripts/wx_locate.py` 自动算出前两个）：
1. **账号目录 wxid** — `ls BASE 上一级`，形如 `wxid_xxxxxxxx_yyy`
2. **解密用 WXID** — **= 账号目录名去掉最后一段后缀**：`wxid_abc123def456_7f2a` → `wxid_abc123def456`（已实测：只有这个命中，带后缀或微信号 your_wechat_id 都解不开）
3. **会话 hash** — 按目标联系人在 `$BASE/msg/attach/` 下找有目标月份数据的目录
4. **CODE** — 10 位账号码，明文 grep 本机搜不到（在加密配置里），获取三途径见 `references/code-finding.md`

## 二、图片解密（V2 分段，最容易做错的一步）

```python
import hashlib, struct
from Crypto.Cipher import AES
from Crypto.Util import Padding

CODE = "<你的账号码>"        # 本例 1234567890，不同账号不同
WXID = "<你的wxid>"          # 不含 _xxx 后缀
KEY  = hashlib.md5((CODE + WXID).encode()).hexdigest()[:16].encode()
XOR  = int(CODE) & 0xFF
V2   = b'\x07\x08V2\x08\x07'
HEADER = 0x0F                # 15 字节头

def align(n):  return n - ~(~n % 16)   # 16 对齐

def decrypt(data):
    if len(data) < HEADER or data[:6] != V2:
        return None, None, "非V2头"
    aes_size, xor_size = struct.unpack_from('<LL', data, 6)   # 头后两个 uint32 LE
    a = align(aes_size)
    aes_c = data[HEADER:HEADER + a]          # ① AES 段
    off   = HEADER + a
    raw_end = len(data) - xor_size if xor_size > 0 else len(data)
    raw   = data[off:raw_end]                # ② 明文段（不加密，直接用）
    xord  = data[raw_end:]                   # ③ XOR 段
    dec = AES.new(KEY, AES.MODE_ECB).decrypt(aes_c)
    try: dec = Padding.unpad(dec, 16)
    except ValueError: pass
    out = dec + raw + bytes(b ^ XOR for b in xord)
    for m, f in {b'\xFF\xD8\xFF':'jpg', b'\x89PNG':'png', b'GIF8':'gif',
                 b'RIFF':'webp', b'wxgf':'hevc', b'II\x2A\x00':'tif', b'BM':'bmp'}.items():
        if out[:len(m)] == m: return out, f, None
    return None, None, "magic未知:" + out[:8].hex()
```

**三条铁律**：
1. ❌ **不能对整个文件做 AES** —— 必须按 15 字节头分三段，整文件解密 100% 失败
2. ❌ 不能按文件名 `_t.dat` 判断就丢弃 —— 部分 `_t.dat` 本身就是完整 JPEG（70KB+），能直接解出原图
3. ✅ 解密结果按 **magic bytes** 判格式，`wxgf` 是微信裸 HEVC 封装

**CODE/WXID 校验法**：用 `scripts/wx_probe.py` 拿一个真实 dat 试解，解出 `FF D8`/`89 PNG`/`wxgf` 即参数正确；报「magic未知」说明 CODE 或 WXID 不对。

## 快速开始：随包脚本（全部本机实测）

| 脚本 | 作用 | 实测结果 |
|---|---|---|
| `scripts/wx_locate.py` | 定位 wxid/会话hash/月份，**自动算解密用WXID** | ✅ 识别出 106 个会话，目标 hash 自动排到第一 |
| `scripts/wx_probe.py` | 验证 CODE+WXID 对不对 | ✅ full→wxgf、_t→jpg 双命中 |
| `scripts/wx_download.py` | GUI 批量下载（动态窗口测量+盲点网格） | ✅ 编译+单元测试，坐标=实战值 |
| `scripts/wx_decrypt.py` | 批量解密 + wxgf→jpg 转码 | ✅ 4/4 零失败 |
| `scripts/wx_verify.py` | 验收（stem 比对，缺口=0） | ✅ 真实交付目录缺口 0 |

```bash
python3 scripts/wx_locate.py                          # 1 定位（拿到 WXID+hash）
python3 scripts/wx_probe.py --code <CODE> --wxid <WXID> --dat <任一.dat>   # 2 验参
python3 scripts/wx_download.py --hash <hash> --month 2026-10 --wxid <账号目录>   # 3 GUI下载
python3 scripts/wx_decrypt.py --code <CODE> --wxid <WXID> --src <Img目录> --dst ./out  # 4 解密转码
python3 scripts/wx_verify.py --src <Img目录> --dst ./out    # 5 验收缺口=0
```

CODE 获取三途径见 `references/code-finding.md`；完整操作手册见 `references/sop.md`。

## 三、wxgf 转 jpg

```bash
ffmpeg -y -f hevc -i in.wxgf -frames:v 1 out.jpg   # 不加 -f 会报 moov atom not found
```

## 四、⭐ 核心难点：微信「不点开就不下载原图」

本地只存 120px 缩略图（`*_t.dat`），原图必须**点开才从服务器拉**。这是整个任务最耗时的根因。

### 唯一验证有效的批量触发路径

```
打开查看器(点聊天流图片) → RAISE 查看器窗口 → 方向键翻页 → 文件落盘
```

```python
# 方向键 code：右=124（更晚），左=123（更早）
def key(code):
    for d in (True, False):
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, code, d))
        time.sleep(0.03)
```

- **单击图片只开查看器、不下载** ← 最容易误判成「点了没反应」
- 查看器序列翻到底后零增长 → 必须**关闭 → 换位置 → 重开**再翻
- **视频只有左方向(123)有效**：查看器是从底部的图打开的，视频都在更早位置；右方向翻 520 页 mp4 零增长
- 图片翻页间隔 ≥0.42s，**视频 ≥0.9s**（单个 1.9~4.9MB，太快翻过去没下完）
- 检测到文件数增长后再等 8s 确认下完整

### 滚动（写错就完全无效）

```python
# ✅ 有效：pixel 单位
CGEventPost(kCGHIDEventTap, CGEventCreateScrollWheelEvent(
    None, kCGScrollEventUnitPixel, 1, px))     # 负=更早，正=回最新
# ❌ 无效：line 单位对微信 0% 像素变化
```

每轮必须**先回底部**再加深：`Cmd+↓`(keycode 121 + mod 55) + 正向滚动兜底，否则滚过头到聊天顶部 → 盲点全 `opened=False`。

### 关闭查看器（ESC 无效）

```applescript
-- ❌ key code 53 (ESC) 微信查看器不响应
-- ✅ 走菜单
tell application "System Events" to tell process "WeChat"
  click menu item "关闭" of menu "文件" of menu bar 1
end tell
```

## 五、执行 SOP（七步）

| # | 步骤 | 产出/验收 |
|---|---|---|
| 1 | **清场**：关 `.doc` 预览窗、聊天记录窗、查看器、权限弹窗、System Settings | 微信只剩主窗口 |
| 2 | **定位**：wxid、会话 hash、CODE、目标月份目录 | 三个路径可读 |
| 3 | **试解**：取 1 个 dat 解密验证 magic | 出 `FFD8`/`PNG`/`wxgf` |
| 4 | **回底**：切到目标会话 → Cmd+↓ → 滚到底（日期=最新） | 标题栏=目标联系人 |
| 5 | **批量下载**：循环「盲点开查看器 → 方向键翻页 → 关闭 → 滚一层」 | full/dat 数持续增长 |
| 6 | **解密+转码**：V2 分段解密 → ffmpeg -f hevc → jpg/png | 0 失败 |
| 7 | **验收**：stem 集合比对（见下） | 缺口 = 0 |

**盲点坐标**（本例窗口 `(63,112) 900×700`，消息区 `x303-963, y152-760`）：
图片消息中心 `x ∈ {420,460,500,540}`，`y = 200,270,...,620`（步长 70）。**步长改成 48 会全点空** —— 必须对准图片行中心。

### 停止条件
- 点开 9 月的图会存进 `2026-09/` → **监控该目录，一旦增长=越界，立即停**
- 连续 3 轮目标月份 full+mp4 零增长 → 停
- 已滚到聊天顶部（日期分隔线=最早）→ 停

## 六、验收（必须用 stem 比对）

```python
full_stems  = {f[:-4]   for f in dat if not f.endswith('_t.dat')}
thumb_stems = {f[:-6]   for f in dat if f.endswith('_t.dat')}   # 去 _t.dat
need = thumb_stems - {能直接从 _t 解出的那些}
delivered = {os.path.splitext(f)[0] for f in os.listdir(DEST)}
print("缺口:", len(need - delivered))      # 目标 = 0
```

**❌ 不要用感知哈希验收**：缩略图 120px vs 原图 1080px，resize 到 16×16 后哈希对不上，会误报 75~104 张缺口（假的）。

视频同理：`msg/video/<月>/` 封面含 `xxx.jpg` 和 `xxx_thumb.jpg` 两个变体，**`_thumb` 不是独立视频**，否则会虚报缺口。

## 七、坑清单（按踩坑顺序）

| 坑 | 现象 | 解法 |
|---|---|---|
| 查看器遮挡 | 点击全落空、0 增长 | 查看器 z-index 高于主窗口，先关它/先 RAISE |
| line 滚动无效 | 截图 0% 像素变化 | 改 `kCGScrollEventUnitPixel` |
| ESC 关不掉查看器 | 按了没反应 | 走菜单「文件→关闭」 |
| 整文件 AES | 报「非V2头」/magic 未知 | 按 15 字节头分三段 |
| 滚过头 | `opened=False` 连续多轮 | 每轮先 Cmd+↓ 回底 |
| 盲点步长错 | 打不开查看器 | y 步长用 70 对准图片行 |
| 第二个 Enter | 文件没选上，反而把输入框文字**发送**出去 | 文件对话框只按 1 次 Enter，之后用鼠标点「打开」 |
| 遮挡窗口 | 系统设置/权限弹窗/doc 预览盖住聊天区 | 跑批前统一清场（见 SOP 第 1 步） |
| vision 坐标尺度 | 三次报不同基准(2560/2880/1920) | **截图后先 `Image.open().size` 拿真实尺寸**，再用「裁剪图内坐标 ÷ 放大倍数 + 裁剪偏移」换算 |

## 八、交付形态

```text
<项目名>/
  1-文件/          # MD5 去重后的文档
  2-图片/原图/      # 全分辨率 jpg/png（知识库用这个）
  2-图片/缩略图/
  3-视频/           # mp4 + 封面
  _进度台账.md      # 跨会话恢复用
```

导入知识库：打包 `zip -r` 或在 IMA/飞书知识库点上传；**长文本指令先发、文件随后**，让 AI 先建立归档意图。

## 安全与合规
- 仅导出**你有权访问**的会话；个人隐私数据需授权
- 解密参数属本机账号密钥，**不要写进公开仓库**（放环境变量或 `~/.config/` 下的私密文件）
- 微信版本升级后路径/加密可能变化，上线前先跑「试解」步骤验证

---

## 关于作者

本技能由「九品锦锂e」制作。

- 微信：ly5419495
- 公众号：初五Agent（微信搜一搜，复盘和方法都写在那儿）
- 技能货架：https://skillpay.alipay.com/public/jiupinjinlie

> 使用中遇到问题、想要定制版本（Windows 适配、其他 IM 的同类导出）或需要配套支持，可通过上面任一方式联系，备注「SkillHub」优先通过。
