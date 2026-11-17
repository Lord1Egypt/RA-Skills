# 优酷（youku.com）流媒体结构 —— 实战逆向笔记

> 2026-09 实测于 `https://v.youku.com/v_show/id_<vid>.html`（01:16:39 / 1080P）

## 一、分片结构（最关键）

优酷长视频**不是**一个 m3u8 索引 + N 个小 ts，而是：

```
全片被切成 N 个“大分片”，每个分片 ≈ 140 秒，是一个独立且完整的 MP4 文件
每个分片有自己的 URL（含独立 vkey 令牌）
```

**分片数推算**：`N = ceil(总时长 / 140)`。本例 4599s → `ceil(4599/140) = 33` 个分片。

## 二、URL 结构

```
https://vali01.cp31.ott.cibntv.net/{vid前缀}/{fid}.mp4.ts?...&ts_start=..&ts_end=..&ts_seg_no=..
                                              ↑
                                    03000C2 X {HH} 649EAA3B903EE8...
                                            ↑ ↑↑
                       前7位 03000C2 固定；第8位 X 随视频/流变化(0/1/7..，勿写死)
                       HH = 分片号，十六进制 2 位（00~20 = 0~32），源播放顺序的权威编号
```

**⚠️ 巨坑 1：分片号是十六进制，不是十进制。**
早期脚本用 `f'{k:02d}'`（十进制）去匹配，导致 `0a`~`20` 共 6 个分片永远匹配不上，反复重试都失败。
正确做法：`idx = filename[8:10]` 然后 `int(idx, 16)`。

**⚠️ 巨坑 2：前缀只固定前 7 位 `03000C2`，第 8 位会变。**
实测同批两个视频的文件名前缀分别是 `03000C20..` 和 `03000C27..`，本笔记最早逆向的是 `03000C21..`。
第 8 位与视频/清晰度/CDN 编码有关，**不能 `startswith('03000C21')` 写死**，否则换视频整片采不到（0 分片）。
正确匹配：`re.match(r'^03000C2[0-9a-fA-F]([0-9a-fA-F]{2})', fn)`，第 8 位通配、段号取捕获组。

**🔑 段号即顺序（合并顺序的权威依据）**：`HH` 是优酷 CDN 生成的源段号，
采集用它作 key、合并按它升序。合并前再核对“每个分片 key == URL 内嵌 HH”，
全一致即顺序正确——比人眼看长片或抽帧比画面都可靠（切镜会让画面差异法误报）。

## 三、时间窗口参数

请求带三个参数：

| 参数 | 含义 |
|---|---|
| `ts_start` / `ts_end` | 10 秒窗口，例如 `99.9` ~ `109.9` |
| `ts_seg_no` | 全局窗口序号 |

规律：**`ts_seg_no = 分片号 × 14 + 窗口号`**（每个分片 140s ÷ 10s = 14 个窗口）

### ⭐ 关键技巧：去掉窗口参数可取回整个分片

把 `ts_start` / `ts_end` / `ts_seg_no` 三个参数**全部删掉**再请求，CDN 会返回**整个分片的完整 MP4**（约 70-85 MB），无需自己拼 14 个窗口。

```python
import re
def strip_window(u):
    u = re.sub(r'&?ts_start=[0-9.]+', '', u)
    u = re.sub(r'&?ts_end=[0-9.]+', '', u)
    u = re.sub(r'&?ts_seg_no=\d+', '', u)
    return u.replace('?&', '?').replace('&&', '&')
```

**注意**：`ts_start` 超过分片末尾（如 >140s）会返回 **HTTP 400**。这不是 bug，恰恰证明每个文件只含 140s 内容。

## 四、seek 引出 URL

播放器 seek 到 `分片号 × 140 + 偏移` 时，浏览器就会请求对应分片的 URL。
偏移取 5 / 30 / 60 / 95 / 120 秒轮换（个别分片某些点不触发请求）。

**⚠️ 必须禁用浏览器缓存**，否则重复 seek 到同一位置会命中缓存、不发网络请求、监听不到 URL：

```javascript
const cdp = await ctx.newCDPSession(page);
await cdp.send('Network.enable');
await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
```

## 五、画质

CDN 文件名末段含画质索引，档位越高文件越大，**去掉窗口参数后拿到的就是当前播放器选定画质的分片**：

- 未登录：约 480P
- 登录：720P
- 会员：1080P（`03000C2 X HH 649EAA` 这类前缀；X 随流变化不代表画质，画质以播放器选定档位为准）

**流程上必须先让用户在浏览器里切好最高画质，再采集 URL。**

## 六、观看密码弹窗（✅ 已验证可全自动）

部分视频作者设了观看密码。弹窗一出现，`<video>` 元素会从 DOM 移除，所有采集失效。

- 输入框选择器：`#kui_layer_password-layer_passwordInput`（即 `PW_INPUT`）
- 确定按钮：文本恰为“确定”、`children.length===0`、`offsetParent` 可见的元素

**一条命令搞定**（browser_ctl.mjs 的 `pwauto` 已内置）：

```bash
echo "pwauto <密码>" > <工作目录>/cmd.txt
# 等 15~20s，status.txt 出现 {"t":..,"w":1920} 且 t 增长 = 成功
```

### 正确解法（三步，缺一不可）

```javascript
// 1. 真实点击聚焦 + 清空
const inp = await page.$('#kui_layer_password-layer_passwordInput');
await inp.click({ clickCount: 3 });
await page.keyboard.press('Backspace');
// 2. 逐字符键盘输入 —— 关键！
await page.keyboard.type('0980', { delay: 90 });
// 3. 真实鼠标点“确定”（Enter 键无效，该弹窗没绑回车提交）
const c = await page.evaluate(() => {
  const b = [...document.querySelectorAll('*')]
    .find(e => e.textContent.trim()==='确定' && e.children.length===0 && e.offsetParent);
  const r = b.getBoundingClientRect();
  return { x: r.x + r.width/2, y: r.y + r.height/2 };
});
await page.mouse.move(c.x, c.y);
await page.mouse.down(); await new Promise(r=>setTimeout(r,120)); await page.mouse.up();
```

### 为什么必须这样（踩坑记录）

| 做法 | 结果 | 原因 |
|---|---|---|
| 原生 setter `inp.value=x` + input 事件（`pwfill`） | 回读 value 正确，但提交**空密码**→“密码错误” | 只改 DOM 属性，Vue v-model 响应式数据不同步 |
| `page.fill()` | 可能不触发 Vue 的键盘监听 | 受控组件依赖完整 key 事件序列 |
| **`page.keyboard.type()` 逐字符** ✅ | Vue 正确同步 | 派发完整 `keydown→keypress→input→keyup` |
| `keyboard.press('Enter')` | 弹窗没反应 | 优酷密码框**不绑定回车提交** |
| JS `dispatchEvent(MouseEvent)` 点确定 | 可能不生效 | 前端事件拦截 |
| **`page.mouse` 真实坐标点击** ✅ | 弹窗消失、视频播放 | 浏览器级真实输入，无法被 JS 拦截 |

成功判据：`status.txt` 从 `novideo` 变为 `{"t":N,"dur":4599,"w":1920,...}` 且 `t` 持续增长。
失败降级：`pwauto` 失败时先 `pwinfo` 导出弹窗 HTML 核对选择器；再不行就把窗口交给用户手动点（值已填好）。

## 七、令牌时效

URL 里的 vkey/令牌会过期（实测 1.5 小时前的 URL 部分仍可用，但不保证）。
**采集完立即下载**，不要隔夜。若下载中报 403/400，重新 seek 采集该分片即可。

## 八、性能

- CDN **单连接限速**（约 1-9 MB/s）
- **并发 Range 请求可线性提速**：单文件 6 路并行实测 ~55 MB/s
- 推荐：单分片 6 路 Range + 3 个分片并行。本例 2.45 GB / 33 分片 → **175 秒**下完

## 九、合并

每个分片都是一个带完整 moov 的 MP4，直接 concat demuxer 无损合并：

```bash
ffmpeg -f concat -safe 0 -i list.txt -c copy -movflags +faststart out.mp4
```

本例 33 片段（32×140s + 末尾 122.5s）→ 合并后 4599.0s，与页面显示 01:16:39 完全一致。
分片间有约 3.5s 的重叠误差，concat 会自动处理，接缝解码零错误。
