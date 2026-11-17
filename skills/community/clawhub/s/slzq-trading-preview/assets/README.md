# assets

| 文件 | 内容 | 用途 |
|------|------|------|
| `kefu-qrcode.png` | 企业微信客服二维码，编码内容为 `https://work.weixin.qq.com/ca/cawcde585f7474b3f7` | 用户需要**开户**或需要人工协助时出示 |
| `kefu-qrcode.base64.txt` | 同一张二维码的 **base64 data URI**（`data:image/png;base64,…`，单行 1162 字符） | 宿主不能发送本地文件、但能渲染内联图片时用它 |

## kefu-qrcode.png

- 尺寸 490×490，容错等级 **H**（最高），四周留白 4 模块，普通手机摄像头正常距离即可识别。
- 图片内容 = 上述链接本身，扫码后进入三立智期企业微信客服会话。
- **展示方式**（按宿主能力从上往下挑第一个可行的）：
  1. 能发本地文件 → 直接把 `assets/kefu-qrcode.png` 发给用户；
  2. 不能发文件但能渲染内联图片（Markdown / HTML）→ 用 `assets/kefu-qrcode.base64.txt` 里的 data URI，例如 `![三立智期客服](data:image/png;base64,…)`；
  3. 只能发纯文本 → 把链接原样给出。
  三种方式都要说明"扫码或点击均可联系三立智期客服办理开户"。

## kefu-qrcode.base64.txt

- 内容是**完整的 data URI**（含 `data:image/png;base64,` 前缀），整个文件就一行，读出来去掉行尾换行即可直接用。
- 与 `kefu-qrcode.png` 是同一张图：base64 解码后与原文件逐字节一致（md5 `020b5871aa6ccaed5cd7221cec06a695`），解码还原后扫码得到的仍是 `https://work.weixin.qq.com/ca/cawcde585f7474b3f7`。
- **不要手工重排或折行**，也不要只截一段——base64 断了图就废了。
- 换二维码时两个文件必须一起更新，命令：`python3 -c "import base64,pathlib;p=pathlib.Path('assets');p.joinpath('kefu-qrcode.base64.txt').write_text('data:image/png;base64,'+base64.b64encode(p.joinpath('kefu-qrcode.png').read_bytes()).decode()+chr(10))"`

### 何时出示

- 用户还没有三立智期期货账户，问「怎么开户」；
- 用户要开通**实盘**权限，但尚未完成开户（实盘登录的前置条件）；
- 用户遇到本 skill 无法处理的账户类问题（密钥吊销、账号异常、资金问题等）。

模拟盘不需要开户——领到密钥时服务端已自动开通模拟盘账户，**不要**在模拟盘场景抛这个二维码。

### 重新生成

链接变更时按同样参数重新生成，并回读校验内容一致：

```bash
python3 - <<'PY'
import segno, cv2
URL = "https://work.weixin.qq.com/ca/cawcde585f7474b3f7"
OUT = "assets/kefu-qrcode.png"
segno.make(URL, error='h').save(OUT, scale=10, border=4, dark="#000000", light="#FFFFFF")
decoded, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(OUT))
assert decoded == URL, decoded
print("OK", decoded)
PY
```
