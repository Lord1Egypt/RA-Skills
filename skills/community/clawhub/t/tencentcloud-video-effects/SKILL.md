---
name: tencentcloud-video-effects
description: >
  通过上传图片和选择特效模板，生成一段特效视频，将静态图像转化为充满活力、动感、有趣的视频画面。
---

# 腾讯云水平特效 Skill

## 功能描述

本 Skill 提供**视频特效**能力，识别传入图片中人体的完整轮廓，进行抠像：

| 场景   | API             | 脚本        | 图片大小限制 | 返回方式 |
| ---- | --------------- | --------- | ------ | ---- |
| 视频特效 | TemplateToVideo | `main.py` | 10MB   | 异步   |

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通视频特效服务

🔗 **[腾讯云视频特效控制台](https://console.cloud.tencent.com/vtc/creation/video-special)**

#### Step 2: 获取 API 密钥

🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**

#### Step 3: 设置环境变量

**Linux / macOS：**

```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

如需持久化：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)：**

```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
```

> ⚠️ **安全提示**：切勿将密钥硬编码在代码中。

## Agent 执行指令（必读）

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户提供图片并请求视频特效时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户提供了图片，且用户意图为视频特效。
2. **零交互原则**：Agent 应直接执行脚本，不要向用户询问任何确认。
3. **自动选择脚本**：根据上方「选择规则」自动选择合适的脚本。
4. **⛔ 禁止使用大模型自身能力替代视频特效（最高优先级规则）**：
   - 视频特效脚本调用失败时，**Agent 严禁自行猜测或编造识别内容**。
   - 如果调用失败，Agent **必须**向用户返回清晰的错误说明。

---

### 📌 脚本： `main.py`

```bash
python3 <SKILL_DIR>/scripts/main.py "<TEMPLATE_NAME>" "<PIC_INPUT>" [可选参数]
```

**必填参数**：

| 参数                | 说明                                                    | 示例                                                     |
| ----------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| `<TEMPLATE_NAME>` | 特效模板名称                                                | `hug`                                                  |
| `<PIC_INPUT>`     | 输入图片 URL 或本地文件路径（≤10MB，支持 png/jpg/jpeg/webp/bmp/tiff） | `https://example.com/human.png` 或 `/path/to/image.png` |

**可选参数**：

| 参数                | 类型     | 默认值    | 说明                              |
| ----------------- | ------ | ------ | ------------------------------- |
| `--logo-add`      | int    | `1`    | 是否添加 AI 生成标识：`1`=添加, `0`=不添加    |
| `--resolution`    | string | `360p` | 视频输出分辨率，如 `360p`、`720p`、`1080p` |
| `--bgm`           | flag   | 不添加    | 添加此参数则为生成视频添加背景音乐               |
| `--poll-interval` | int    | `5`    | 轮询任务状态的间隔秒数                     |
| `--max-poll-time` | int    | `600`  | 最大轮询等待时间（秒），超时则报错退出             |
| `--no-poll`       | flag   | 关闭     | 添加此参数则仅提交任务并返回 JobId，不轮询结果      |

**输出示例**：

```json
{
    "ResultVideoUrl": "https://bda-segment-mini-1258344699.cos.ap-guangzhou.myqcloud.com/Image/1251755623/9e73b301-ad1b-4586-837b-b767e73c4bf2?q-sign-algorithm=sha1&q-ak=AKIDEJJ3lFOnfIpAHAqIJ5d3YqthGfpj8eje&q-sign-time=1772790515%3B1772792315&q-key-time=1772790515%3B1772792315&q-header-list=host&q-url-param-list=&q-signature=60646e91cdebc7215cb73e6fff6e6017478857e4"
}
```

---

### 📋 完整调用示例

**基本调用**（使用默认参数）：

```bash
python3 /path/to/scripts/main.py hug "https://example.com/human.png"
```

**指定分辨率和背景音乐**：

```bash
python3 /path/to/scripts/main.py hug "https://example.com/human.png" --resolution 720p --bgm
```

**去除 AI 标识 + 高分辨率**：

```bash
python3 /path/to/scripts/main.py hug /path/to/local/image.jpg --logo-add 0 --resolution 1080p
```

**仅提交任务，不等待结果**：

```bash
python3 /path/to/scripts/main.py hug "https://example.com/human.png" --no-poll
```

**自定义轮询策略**：

```bash
python3 /path/to/scripts/main.py hug "https://example.com/human.png" --poll-interval 10 --max-poll-time 300
```

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 向用户询问"是否要执行视频特效"——应直接执行
- 手动安装依赖——脚本内部自动处理
- 忘记读取输出结果并返回给用户
- 视频特效服务调用失败时，自行编造识别内容

## API 参考文档

详细的引擎类型、参数说明、错误码等信息请参阅 `references/` 目录下的文档：

- [提交视频特效API](references/SubmitTemplateToVideoJob.md)（[原始文档](https://cloud.tencent.com/document/product/1616/119001)）
- [查询视频特效API](references/DescribeTemplateToVideoJob.md)（[原始文档](https://cloud.tencent.com/document/product/1616/119002)）

## 核心脚本

- `scripts/main.py` — 视频特效脚本

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK，`main.py` 使用）

安装依赖（可选 - 脚本会自动安装）：

```bash
pip install tencentcloud-sdk-python requests
```
