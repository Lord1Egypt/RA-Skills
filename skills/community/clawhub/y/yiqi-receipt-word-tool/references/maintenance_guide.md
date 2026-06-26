# 付款截图 Word 排版工具 — 技术维护记录

> 最近更新：2026-05-04
> 工具文件：`scripts/receipt_word_tool.py`
> 原始开发会话：2026-04-28 / 2026-04-30

---

## 一、问题修复清单

| # | 问题描述 | 根因分析 | 修复方案 |
|---|---|---|---|
| 1 | **RuntimeError: main thread is not in main loop** 程序崩溃 | 后台 OCR 线程直接操作 GUI StringVar/Entry 等控件，tkinter 不允许非主线程修改控件状态 | 所有线程内 GUI 更新全部改用 `self.root.after(0, lambda: ...)` 调度到主线程执行 |
| 2 | **numpy.dtype size changed** 警告，easyocr 无法 import | Anaconda 自带 scikit-image 是按旧版 numpy 编译的，二进制不兼容 | `pip install --upgrade --force-reinstall scikit-image` 重新编译适配当前 numpy |
| 3 | **WinError 5 权限拒绝** scipy 卸载失败 | scipy DLL 被 Python 进程锁定 | PowerShell `Remove-Item -Force` 删除锁定文件夹后重试 |
| 4 | **GitHub/hf-mirror 下载 EasyOCR 模型失败**（WinError 10060 超时） | 国内网络无法访问 GitHub/HuggingFace，hf-mirror.com 重定向也被墙 | 改用 ModelScope（魔搭）国内镜像下载 |
| 5 | **CRYPT_E_REVOCATION_OFFLINE** curl 下载证书错误 | Windows SChannel 尝试连接微软证书吊销服务器（离线） | `curl --ssl-no-revoke -L` 绕过证书吊销检查 |
| 6 | **cv::findDecoder can't open/read file** OpenCV 读图失败 | OpenCV imread/imdecode 在 Windows 下不支持含中文/特殊字符的路径 | 改用 Pillow 读取图片 → 转 numpy 数组 → 传给 EasyOCR，彻底绕过 OpenCV |
| 7 | **金额识别全是 1** | OCR 把 `¥` 误识别为 `半`；兜底逻辑取所有金额的**最小值**（错误，付款截图应取最大值） | 正则增加 `半` 作为金额符号兼容；兜底改为取 max(candidates) |
| 8 | **44_18 识别为 0.66** | 支付宝立减 `-0.66` 被当成实付金额取走 | 改为取第一个负数（位置最前 = 账单开头实付） |
| 9 | **46_18/47_18 识别为负数**（如 `-6.00`） | 账单格式负数未取绝对值直接返回 | 返回 `abs(neg_positions[0][1])` 绝对值 |
| 10 | **43_18 误识别商品名的 24.15** | "商品名里有 `丫24.15`" 被正则误匹配为实付 | 改为在关键词后 200 字符内**贪心**匹配货币符号+金额，跳过商品名干扰 |
| 11 | **45_6 识别为 0.00** | `实付*0 确认收货后自动付款半4.12`，`*0` 干扰正则 | 贪心匹配：找关键词后最后一个 `[*￥¥半●]` + 数字，跳过 `*0` |
| 12 | **PyTorch pin_memory 警告刷屏** | 无 GPU 时 DataLoader 的 pin_memory 参数无效（正常但烦人） | `warnings.filterwarnings('ignore', message=".*pin_memory.*")` |
| 13 | **滴滴打车"半24.21"格式未识别** | 兜底正则使用 `\b` 边界，对"半"后紧跟数字的情况匹配失败 | 新增优先级3.5检测先用后付；优先级4改用显式货币符号匹配 `[￥¥半●]` + 普通金额回退 |
| 14 | **先用后付"确认收货后再付款"识别为¥0.00** | 先用后付订单确实无确认金额，OCR正确识别为0，但缺乏兜底 | 新增优先级3.5检测先用后付关键词，尝试提取订单金额作为参考值 |

---

## 本次会话修复详情

### 修复13：滴滴打车"半24.21"格式识别

**问题**：滴滴打车截图显示"半24.21"（半=¥符号），OCR正确识别但金额提取失败。

**修复前（优先级4兜底）**：
```python
all_amounts = re.findall(r'\b(\d{1,5}\.\d{1,2})\b', text)
candidates = [float(a) for a in all_amounts if 0.1 <= float(a) <= 9999]
```

**修复后**：
```python
# 1. 标准金额（含货币符号的，如半24.21、¥12.34）
currency_amounts = re.findall(r'[￥¥半●][\s]*(\d+\.\d{1,2})', text)
# 2. 普通金额（数字前后有边界）
plain_amounts = re.findall(r'(?:^|[^\d￥¥半●])(\d{1,5}\.\d{1,2})(?=\s|$|[^\d￥¥半●])', text)
all_amounts = currency_amounts + plain_amounts
candidates = [float(a) for a in all_amounts if 0.01 <= float(a) <= 9999]
```

### 修复14：先用后付场景识别

**问题**：先用后付订单（确认收货后再付款）OCR结果为"确认收货后再付款"，金额为0。

**修复**：新增优先级3.5，检测先用后付关键词，尝试提取订单金额作为参考：
```python
if re.search(r'先用后付|确认收货后再付款|付款金额待确认', text):
    order_match = re.search(r'订单金额[：:]\s*[￥¥半]?\s*(\d+\.\d{1,2})', text)
    if order_match:
        v = float(order_match.group(1))
        if 0.01 <= v <= 9999:
            return v  # 返回订单金额供参考
    return 0.0  # 确实无确认金额
```

---

## 二、EasyOCR 模型离线下载（国内）

**ModelScope（魔搭）下载地址：**
```
检测模型：https://modelscope.cn/models/ms-agent/craft_mlt_25k/resolve/master/craft_mlt_25k.zip
中文识别模型：https://modelscope.cn/models/ms-agent/zh_sim_g2/resolve/master/zh_sim_g2.zip
```

**下载命令（Windows）：**
```bash
curl --ssl-no-revoke -L "URL" -o "目标路径"
```

**模型存放目录：** `C:\Users\11717\.EasyOCR\model\`

**最终验证：**
```python
import easyocr
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)
# 初始化成功即表示模型已正确加载
```

---

## 三、金额提取核心逻辑

```python
def _extract_amount_from_text(text: str) -> float:
    """
    策略优先级：
    1. 显式"实付/应付/合计/总计"关键词 → 贪心匹配货币符号+金额
    2. 订单金额 - 立减优惠（支付宝账单详情页）
    3. 负金额（账单格式，含中文 一 作为负号）→ 取绝对值
    4. 所有金额最大值兜底
    """
```

**关键正则：**
- 贪心匹配（绕过商品名干扰）：`r'[*￥¥半●][\s]*(\d+\.?\d*)'`
- 支付宝账单：`r"订单金额\s*[：:￥¥半]?\s*(\d+\.\d{1,2})"`
- 立减优惠：`r"(?:到店)?支付立减\s*[：:￥¥半-]?\s*(\d+\.\d{1,2})"`
- 负金额（含中文负号）：`r'[-一](\d+\.\d{1,2})'`

---

## 四、工具主要功能

| 功能 | 说明 |
|---|---|
| 选择/追加图片 | 支持拖入文件夹或追加单张 |
| OCR 批量识别 | 后台线程自动提取实付金额，支持手动修正 |
| 点击缩略图预览 | 点击弹出原图大图窗口（最大屏幕85%），ESC/关闭按钮关闭 |
| 生成 Word 文档 | 每页 6 张图（2列×3行），每 18 张插入蓝色小计，末尾红色总计 |

---

## 五、关键代码片段

**线程安全 GUI 更新（正确写法）：**
```python
def _ocr_single(self, idx: int):
    def task():
        self.root.after(0, lambda: self.ocr_status[idx].set('识别中…'))
        try:
            text, amount = extract_amount_from_image(self.image_paths[idx])
            self.root.after(0, lambda: self.amounts[idx].set(f'{amount:.2f}'))
        except Exception as e:
            self.root.after(0, lambda: self.ocr_status[idx].set(f'错误: {e}'))
    threading.Thread(target=task, daemon=True).start()
```

**Pillow 绕过 OpenCV 中文路径：**
```python
from PIL import Image
import numpy as np

with Image.open(image_path) as pil_img:
    img_array = np.array(pil_img.convert('RGB'))
results = reader.readtext(img_array, detail=0)
```

**缩略图点击放大：**
```python
thumb_label.bind('<Button-1>', lambda e, path=img_path: self._show_image_preview(path))

def _show_image_preview(self, img_path: str):
    preview_win = tk.Toplevel(self.root)
    preview_win.bind('<Escape>', lambda e: preview_win.destroy())
    # ... 加载原图、居中显示
```
