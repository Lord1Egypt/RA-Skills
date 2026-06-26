# 配置指南 — 图可丽视觉 API Skill

## 1. 注册账号

1. 访问 **https://www.tukeli.net**
2. 点击右上角「登录/注册」完成注册
3. 支持微信、手机号等方式注册

## 2. 获取 API Key

1. 登录后，点击右上角头像进入账户设置
2. 找到「API密钥」或「获取API密钥」入口
3. 复制生成的密钥（格式：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）

## 3. 配置密钥

在 skill 根目录创建 `.env` 文件：

```
TUKELI_API_KEY=你的API密钥
```

或通过环境变量导出：

```bash
export TUKELI_API_KEY="你的API密钥"
```

## 4. 安装依赖

```bash
cd tukeli-visual-api
pip install -r scripts/requirements.txt
```

唯一外部依赖为 **requests**（HTTP 客户端库）。

## 5. 测试连接

```bash
python scripts/tukeli.py --api matting --image /path/to/test.jpg
```

如果密钥配置正确，处理后的图片将保存到 `data/outputs/`。

## 6. 首次调用

```bash
# 通用抠图
python scripts/tukeli.py --api matting --image photo.jpg --output result.png

# 人脸变清晰
python scripts/tukeli.py --api face-clear --image blurry.jpg --output hd.png

# AI背景更换（先提交任务）
python scripts/tukeli.py --api ai-bg --submit \
  --image-url "https://example.com/transparent.png" \
  --text "美丽的海滩背景"

# AI背景更换（查询结果）
python scripts/tukeli.py --api ai-bg --query --task-id 12345
```

## 重要说明：API 域名

> ⚠️ 图可丽 API 的请求域名为 `https://picupapi.tukeli.net`，与官网域名 `www.tukeli.net` **不同**，请勿混淆。

| 用途 | 域名 |
|------|------|
| 官网/注册/充值 | `https://www.tukeli.net` |
| API 请求 | `https://picupapi.tukeli.net` |

## 故障排查

### 错误 1001（余额不足）
- 前往 https://www.tukeli.net 充值点数
- 查看价格列表：https://www.tukeli.net/apidoc-image-matting.html

### 错误 1002（API Key 无效）
- 检查 `.env` 文件中的密钥是否正确
- 确认密钥前后没有多余空格
- 重新从账户设置中复制密钥

### 错误 1003（不支持的图片格式）
- 抠图支持：PNG、JPG、JPEG、BMP、GIF
- 人脸变清晰支持：PNG、JPG、JPEG、BMP、WEBP

### 错误 1004（图片分辨率超限）
- 最大分辨率：4096×4096 像素
- 请先缩小图片再上传

### 错误 1005（文件大小超限）
- 抠图：最大 25 MB
- 人脸变清晰：最大 15 MB

### AI背景更换任务一直处于排队/处理中
- 服务器繁忙时任务会排队，请耐心等待
- 建议每隔 3~5 秒轮询一次查询接口
- 如果 `status=2`（处理失败），请重新提交任务

### 图片未保存
- 检查 `data/outputs/` 目录的写入权限
- 目录会自动创建，但在受限环境中可能失败

## 计费说明

| API | 计费规则 |
|-----|---------|
| 通用抠图 | 15M以下 1点/张，15M~25M 2点/张 |
| 人脸变清晰 | 2点/张 |
| AI背景更换（≤512×512）| 3点/次 |
| AI背景更换（≤1024×1024）| 6点/次 |
| AI背景更换（≤1920×1080）| 12点/次 |

## 安全说明

- API Key 不会出现在日志或输出中
- `.env` 文件已加入 `.gitignore`，请勿提交到版本控制
- 每日处理量限制可通过 `TUKELI_MAX_IMAGES_PER_DAY` 环境变量配置（默认：100）
