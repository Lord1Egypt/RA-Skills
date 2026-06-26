# EasyOCR 离线模型下载（国内）

> 如果工具首次启动下载太慢，或网络不通，直接用这里的方法手动下载。

## 下载地址（ModelScope 魔搭）

EasyOCR 有两个必需模型：

| 模型 | 用途 | 下载地址 |
|---|---|---|
| `craft_mlt_25k.pth` | 检测模型 | https://modelscope.cn/models/ms-agent/craft_mlt_25k/resolve/master/craft_mlt_25k.zip |
| `zh_sim_g2.pth` | 中文识别模型 | https://modelscope.cn/models/ms-agent/zh_sim_g2/resolve/master/zh_sim_g2.zip |

## Windows 下载命令

```bash
# 检测模型
curl --ssl-no-revoke -L "https://modelscope.cn/models/ms-agent/craft_mlt_25k/resolve/master/craft_mlt_25k.zip" -o "C:\Users\11717\.EasyOCR\model\craft_mlt_25k.pth"

# 中文识别模型
curl --ssl-no-revoke -L "https://modelscope.cn/models/ms-agent/zh_sim_g2/resolve/master/zh_sim_g2.zip" -o "C:\Users\11717\.EasyOCR\model\zh_sim_g2.pth"
```

> **注意**：`--ssl-no-revoke` 参数必须加，Windows SChannel 会尝试连接微软证书吊销服务器（可能离线），不加会导致 `CRYPT_E_REVOCATION_OFFLINE` 错误。

## 模型存放目录

```
C:\Users\<用户名>\.EasyOCR\model\
```

确认目录存在：
```bash
mkdir -p "C:\Users\11717\.EasyOCR\model"
```

## 验证是否成功

运行以下 Python 代码，若无报错即成功：

```python
import easyocr
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False, verbose=False)
print("EasyOCR 初始化成功")
```

## 已知网络问题

| 问题 | 解决方案 |
|---|---|
| GitHub 下载超时 | 用 ModelScope |
| HuggingFace 访问被墙 | 用 ModelScope |
| hf-mirror.com 重定向到 xethub 被墙 | 用 ModelScope |
| curl 证书错误 `CRYPT_E_REVOCATION_OFFLINE` | 加 `--ssl-no-revoke` |