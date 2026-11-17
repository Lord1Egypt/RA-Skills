# 微信聊天记录批量导出 — 完整操作规程（SOP）

> 版本：v1.0 ｜ 沉淀日期：2026-10-06 ｜ 实战来源：某商住小区项目资料归档（客户名已匿名）
> 实战基准：**单次导出 1216 个文件 / 163.9MB**（79 文档 + 525 原图 + 504 缩略图 + 25 视频 + 封面），**验收缺口 = 0**

---

## 零、这次任务到底做了什么

**需求**：把微信联系人「某项目对接人（已匿名）」在 **2026-10-03 ~ 10-04** 两天内发的所有**文件、图片（必须原图）、视频**下载到本地，按项目归档，再导入腾讯 IMA 知识库。

**结果**：
- 文件 79 个（MD5 去重，含合同协议/收支财务/政府文件/委托书）
- 图片 525 张原图 + 504 张缩略图（原图全部全分辨率，不是 120px 预览图）
- 视频 25 个 mp4 + 封面
- 打包 `<项目名>-全部资料.zip` = 149MB / 1216 文件

**难点不在下载本身，在于：微信的设计让"批量获取原图"几乎不可能。**

---

## 一、环境要求

| 项 | 要求 | 说明 |
|---|---|---|
| 操作系统 | macOS（Intel / Apple Silicon 均可） | 路径与加密按 macOS 验证 |
| 微信 | 桌面版 4.x，**已登录且目标会话可打开** | 登录态在本地 `Containers/` |
| Python | 3.10+ | 本例 3.14 |
| Python 包 | `pyobjc-framework-Quartz`、`Pillow`、`pycryptodome` | Quartz 发合成事件、PIL 截图比对、Crypto 解密 |
| 外部工具 | `ffmpeg`（wxgf 转码）、`osascript`（AppleScript） | 无 ffmpeg 则视频无法转 jpg 封装 |
| 系统权限 | **辅助功能** + **屏幕录制**（系统设置 → 隐私与安全性 → 给终端/Python） | 缺任一：点击无效 / 截图全黑 |
| 供电 | `caffeinate -d -i -u -s` 或关闭自动锁屏 | 长任务被锁屏打断会丢状态 |
| 显示 | 禁用 App Exposé 遮挡、关闭多显示器干扰 | 遮挡窗口 = 点击落空 |

**Windows 版微信的存储路径与加密算法不同，本 SOP 未验证 Windows。**

---

## 二、微信本地数据结构（定位这三处）

```bash
BASE=~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<你的wxid>/

# 1) 图片：原始加密块（.dat）
$BASE/msg/attach/<会话hash>/<YYYY-MM>/Img/*.dat
   # _t.dat = 缩略图(120px)，非 _t.dat = 原图
   # 例外：部分 _t.dat 本身就是完整 JPEG（70KB+），可直接解出原图

# 2) 视频：已解密的 mp4
$BASE/msg/video/<YYYY-MM>/*.mp4  +  封面 *.jpg（含 xxx_thumb.jpg 变体）

# 3) 图片缓存：点开过完整图的解密块
$BASE/cache/<YYYY-MM>/Message/<会话hash>/Bubble/*.dat
```

**两条关键规则**：
1. **微信按「消息发生月份」分目录**，不是按文件落盘时间。目录 `2026-10` = 消息发于 10 月。
2. **会话 hash 不等于 wxid** —— 每个联系人/群有一个 hash 目录，需按目标联系人定位。

**三个定位参数**：
| 参数 | 怎么拿 | 本例值 |
|---|---|---|
| wxid | `ls $BASE上一级`，形如 `wxid_xxxxxxxx` | `wxid_abc123def456`（去掉 `_b3ac` 后缀） |
| 会话 hash | 在 `$BASE/msg/attach/` 下找有目标月份数据的目录 | `<会话hash>` |
| CODE | 解密用账号码，**按账号确定**，试解验证 | `1234567890` |

---

## 三、图片解密：V2 分段算法（最容易做错）

### 为什么难
微信 .dat **不是整文件 AES**。文件结构是：

```
[15字节头][AES段(16对齐)][明文段][XOR段]
          ^-- 0x07 0x08 'V2' 0x08 0x07 + <uint32 aes_size> + <uint32 xor_size>
```

### 正确实现

```python
import hashlib, struct
from Crypto.Cipher import AES
from Crypto.Util import Padding

CODE = "<你的账号码>"       # 本例 1234567890
WXID = "<你的wxid>"         # 不含 _b3ac 后缀
KEY  = hashlib.md5((CODE + WXID).encode()).hexdigest()[:16].encode()
XOR  = int(CODE) & 0xFF
V2   = b'\x07\x08V2\x08\x07'
HEADER = 0x0F               # 15 字节

def align(n):  return n - ~(~n % 16)   # 16 字节对齐

def decrypt(data):
    if len(data) < HEADER or data[:6] != V2:
        return None, None, "非V2头"
    aes_size, xor_size = struct.unpack_from('<LL', data, 6)  # 头后两个 uint32 小端
    a = align(aes_size)
    aes_c = data[HEADER:HEADER + a]              # ① AES 段
    off   = HEADER + a
    raw_end = len(data) - xor_size if xor_size > 0 else len(data)
    raw   = data[off:raw_end]                    # ② 明文段（不加密！直接拼）
    xord  = data[raw_end:]                       # ③ XOR 段
    dec = AES.new(KEY, AES.MODE_ECB).decrypt(aes_c)
    try: dec = Padding.unpad(dec, 16)
    except ValueError: pass                      # 对齐填充可能报错，忽略
    out = dec + raw + bytes(b ^ XOR for b in xord)
    # 按 magic 识别真实格式
    MAGIC = {b'\xFF\xD8\xFF':'jpg', b'\x89PNG':'png', b'GIF8':'gif',
             b'RIFF':'webp', b'wxgf':'hevc', b'II\x2A\x00':'tif', b'BM':'bmp'}
    for m, f in MAGIC.items():
        if out[:len(m)] == m: return out, f, None
    return None, None, "magic未知:" + out[:8].hex()
```

### 三条铁律
1. ❌ **不能对整个文件做 AES** —— 必须按 15 字节头分三段处理，整文件解密 100% 失败
2. ❌ **不能按 `_t.dat` 就丢弃** —— 早期部分 `_t.dat` 就是完整 JPEG，可直接解出原图
3. ✅ **用 magic bytes 判格式**，`wxgf` 是微信裸 HEVC 封装

### 参数校验法
拿任意一个 .dat 试解：
- 解出 `FF D8` / `89 PNG` / `wxgf` → **CODE 与 WXID 正确**
- 报「非V2头」→ 文件损坏或头格式变了
- 报「magic未知」→ **CODE 或 WXID 不对**（最常见）

---

## 四、wxgf → jpg 转码

```bash
ffmpeg -y -f hevc -i in.wxgf -frames:v 1 out.jpg
```
⚠️ **必须加 `-f hevc`**，否则报 `moov atom not found`（wxgf 不是标准容器）。

---

## 五、⭐ 核心机制：微信"不点开就不下载原图"

### 问题本质
- 本地只存 **120px 缩略图**（`*_t.dat`）
- 原图必须**点开才从服务器拉取**
- 微信自己的"聊天记录导出"不给散文件、不给原图

### 唯一验证有效的批量触发路径

```
打开查看器(点聊天流图片) → RAISE 查看器窗口 → 方向键翻页 → 文件落盘
```

**方向键 code**：
| 键 | code | 效果 |
|---|---|---|
| 左 | 123 | 翻更早（**视频唯一有效方向**） |
| 右 | 124 | 翻更晚（图片有效；视频无效） |

```python
def key(code):   # 合成方向键
    for d in (True, False):
        CGEventPost(kCGHIDEventTap, CGEventCreateKeyboardEvent(None, code, d))
        time.sleep(0.03)
```

**关键发现（都是踩出来的）**：
1. **单击图片只开查看器、不触发下载** ← 最容易误判成"点了没反应"而放弃
2. 查看器序列翻到底后文件数零增长 → 必须**关闭 → 换位置 → 重开**再翻
3. **视频只有左方向(123)有效** —— 查看器是从底部的图打开的，视频都在更早位置；曾用右方向翻 520 页，mp4 零增长
4. 翻页间隔：**图片 ≥0.42s，视频 ≥0.9s**（视频单个 1.9~4.9MB，太快翻过去没下完）
5. 检测到文件数增长后**再等 8 秒**确认下完整，避免拿到半截文件

### 滚动（单位写错就完全无效）

```python
# ✅ 有效：pixel 单位
CGEventPost(kCGHIDEventTap, CGEventCreateScrollWheelEvent(
    None, kCGScrollEventUnitPixel, 1, px))   # 负=更早，正=回最新

# ❌ 无效：line 单位对微信 0% 像素变化（实测截图完全相同）
```

**回底公式**（每轮开始必做，否则滚过头）：
```python
key(121)  # Cmd+↓（配合 mod 55）
# + 正向滚动兜底（px > 0）
```

### 关闭查看器（ESC 无效）

```applescript
-- ❌ key code 53 (ESC) —— 微信查看器不响应
-- ✅ 走菜单
tell application "System Events" to tell process "WeChat"
  click menu item "关闭" of menu "文件" of menu bar 1
end tell
```

---

## 六、七步执行 SOP

| # | 步骤 | 具体动作 | 验收标准 |
|---|---|---|---|
| **1** | **清场** | 关掉：`.doc` 预览窗、聊天记录窗、查看器、权限弹窗、System Settings | 微信只剩主窗口 |
| **2** | **定位** | 拿到 wxid、会话 hash、CODE、目标月份目录 | 三个路径可 `ls` |
| **3** | **试解** | 取 1 个 .dat 解密 | 出 `FFD8`/`PNG`/`wxgf` magic |
| **4** | **回底** | 切到目标会话 → `Cmd+↓` → 滚到底（日期=最新） | 标题栏=目标联系人 |
| **5** | **批量下载** | 循环：盲点开查看器 → 方向键翻页 → 关闭 → 滚一层 | full/dat 与 mp4 数持续增长 |
| **6** | **解密+转码** | V2 分段解密 → `ffmpeg -f hevc` → jpg/png | 失败数 = 0 |
| **7** | **验收** | stem 集合比对（见第八节） | **缺口 = 0** |

### 盲点坐标（本例）
微信窗口 `(63,112) 900×700`，消息区 `x303-963, y152-760`：
- 图片消息中心 `x ∈ {420, 460, 500, 540}`
- `y = 200, 270, 340, ... 620`（**步长 70**）

⚠️ **步长改成 48 会全点空** —— 必须对准图片行中心（图片行高约 70）。

### 停止条件（三选一）
1. **9 月目录增长 = 越界** → 点开 9 月的图会存进 `2026-09/`，监控该目录，一旦增长立即停
2. **连续 3 轮目标月份 full+mp4 零增长** → 停
3. **已滚到聊天顶部**（日期分隔线=最早）→ 停

---

## 七、踩过的 9 个坑（按发现顺序）

| # | 坑 | 现象 | 根因与解法 |
|---|---|---|---|
| 1 | **查看器遮挡** | 点击全落空、0 增长 | 查看器 z-index 高于主窗口 → 先关它，或先 RAISE 主窗口 |
| 2 | **line 滚动无效** | 截图 0% 像素变化 | 微信不响应 line 单位 → 改 `kCGScrollEventUnitPixel` |
| 3 | **ESC 关不掉查看器** | 按了没反应 | 微信查看器不监听 ESC → 走菜单「文件→关闭」 |
| 4 | **整文件 AES 解密失败** | 报「非V2头」/magic 未知 | 微信是**三段式**（AES段+明文段+XOR段）→ 按 15 字节头分段 |
| 5 | **滚过头** | `opened=False` 连续多轮 | 没先回底 → 每轮开始 `Cmd+↓` + 正向滚动兜底 |
| 6 | **盲点步长错** | 打不开查看器 | y 步长 48 会点到行间隙 → 用 70 对准图片行中心 |
| 7 | **第二个 Enter** | 文件没选上，反而把输入框文字**发送**出去 | macOS 文件对话框只按 **1 次** Enter（"前往"），之后**用鼠标点「打开」** |
| 8 | **遮挡窗口** | 系统设置/权限弹窗/doc 预览盖住聊天区 | 跑批前统一清场（SOP 第 1 步） |
| 9 | **vision 坐标尺度混乱** | 三次报不同基准（2560×1600 / 2880×1800 / 1920×1080） | **截图后先 `Image.open().size` 拿真实尺寸**，再用「裁剪图内坐标 ÷ 放大倍数 + 裁剪偏移」换算 |

---

## 八、验收方法（必须用 stem 比对）

### ❌ 错误方法：感知哈希
缩略图 120px vs 原图 1080px，resize 到 16×16 后**哈希对不上**，会误报 **75~104 张缺口**（全是假的）。

### ✅ 正确方法：stem 文件名集合比对

```python
import os
dat = os.listdir(IMG_DIR)
full_stems  = {f[:-4] for f in dat if not f.endswith('_t.dat')}
thumb_stems = {f[:-6] for f in dat if f.endswith('_t.dat')}   # 去 _t.dat

# 需要补的 = 只有缩略图、没有原图的
need = thumb_stems - full_stems
# 交付目录的 stem 集合
delivered = {os.path.splitext(f)[0] for f in os.listdir(DEST)}

print("缺口:", len(need - delivered))   # 目标 = 0
```

### 视频验收
`msg/video/<月>/` 封面含 `xxx.jpg` 和 `xxx_thumb.jpg` **两个变体**：
- `xxx_thumb.jpg` **不是独立视频**，否则会虚报缺口（本例曾虚报"缺 10 个"）
- 正确：`mp4` 文件名去扩展名后的集合比对 → 实际 25 个独立视频，缺口 = 0

---

## 九、交付形态与知识库导入

### 目录结构
```text
<项目名>/
  1-文件/            # MD5 去重后的文档（79 个 / 68.3MB）
  2-图片/原图/        # 全分辨率 jpg/png（525 张 / 36.1MB）← 知识库用这个
  2-图片/缩略图/      # 504 个 / 1.9MB
  3-视频/             # 25 mp4 + 封面（101 文件 / 57.7MB）
  _进度台账.md        # 跨会话恢复用（记已消费 y 坐标、时间窗、方法）
```

### 打包
```bash
cd <父目录> && zip -r <项目名>-全部资料.zip <项目名>/   # 149MB / 1216 文件，约 8 秒
```

### 导入 AI 知识库（IMA / 飞书）
1. **先发长文本指令**（项目名、文件构成、归档要求）→ AI 建立归档意图
2. **再传文件**（拖拽 zip 或点上传按钮）
3. ⚠️ 传大文件时：文件对话框**只按 1 次 Enter**，之后用鼠标点「打开」

---

## 十、安全与合规红线

1. **仅导出你有权访问的会话** —— 个人隐私数据需授权
2. **解密参数（CODE/WXID/KEY）是本机账号密钥** —— 不要写进公开仓库，放环境变量或 `~/.config/` 下的私密文件
3. **微信版本升级后路径/加密可能变化** —— 上线前先跑「第三步 试解」验证
4. **不用于窃取他人聊天记录** —— 本 SOP 面向"自己的账号、导自己的数据"

---

## 十一、可复用性评估

| 维度 | 结论 |
|---|---|
| **技术可复用** | ✅ 算法/机制与账号无关，只需换 wxid、会话 hash、CODE 三个参数 |
| **平台限定** | ⚠️ 仅 macOS 验证；Windows 路径+加密不同，需另做适配 |
| **版本敏感** | ⚠️ 微信升级可能改路径或加密 → 每次跑前"试解"步骤必须执行 |
| **自动化程度** | 7 步中 1~4 可全自动，5 是 GUI 自动化核心，6~7 可全自动 |
| **耗时量级** | 本例 2 天聊天记录 ≈ 1216 文件，GUI 下载阶段占 80% 时间 |
| **适配场景** | 项目归档、法律取证、离职交接、知识库灌库、审计 |
