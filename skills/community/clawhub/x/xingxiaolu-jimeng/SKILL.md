---
name: jimeng-ai
description: 即梦AI生图与视频生成工具。通过火山引擎API调用即梦AI，支持文生图、图片生成、视频生成。内置50+提示词模板覆盖电商、社交、商业设计、视频等场景。
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["python"]
---

# 即梦AI (Jimeng AI)

通过火山引擎 API 调用即梦AI，支持**文生图**、**图生视频**。

## 凭证

使用 `token-manager` 中保存的 `jimeng` 密钥：
- key: `jimeng`
- 内容: `AccessKeyId` + `SecretAccessKey`

## 快速使用

### 文生图（推荐）

```bash
# 生图并保存到文件
python skills/jimeng-ai/scripts/generate.py --prompt "描述" --output image.png

# 生图输出 MEDIA_URL（用于 OpenClaw 内联显示）
python skills/jimeng-ai/scripts/generate.py --prompt "描述"
```

### 查询任务

```bash
python skills/jimeng-ai/scripts/query.py <task_id> [req_key]
```

### 视频生成

```bash
python skills/jimeng-ai/scripts/video.py "描述" --duration 5
```

## 提示词模板库

内置50+即梦提示词模板，详见：

📋 **`references/prompts-templates.md`**

| 分类 | 模板数 | 场景 |
|------|--------|------|
| 🛒 电商促销海报 | 15个 | 双11/618/春节/520/3C数码/美妆/运动等 |
| 📱 社交媒体图文 | 10个 | 小红书/朋友圈/知识科普/美食/健身/职场 |
| 🎨 商业设计 | 8个 | Logo/IP形象/UI图标/VI系统 |
| 🎬 视频生成 | 10个 | Vlog/品牌广告/国潮/创意短片 |

### 万能公式

```
主体 + 动作/状态 + 场景环境 + 风格美学 + 光影氛围 + 镜头视角 + 画质参数
```

**示例：**
- ❌ "一只猫在沙发上。"
- ✅ "一只橘色的胖猫慵懒地躺在棕色的真皮沙发上，午后阳光从落地窗斜射进来，空气中有细小的灰尘颗粒在舞动，电影质感，浅景深，8K超高清。"

## 参数说明

### 文生图 (req_key: jimeng_t2i_v40)

| 参数 | 说明 |
|------|------|
| `--prompt, -p` | 图像描述（必填） |
| `--aspect` | 宽高比: `1:1`(默认), `3:4`, `4:3`, `16:9`, `9:16` |
| `--seed` | 随机种子，-1 表示随机 |
| `--output, -o` | 保存路径（不填则输出 MEDIA_URL） |

### 文生视频 (req_key: jimeng_i2v_first_v30_1080)

| 参数 | 说明 |
|------|------|
| `--prompt` | 视频描述（必填） |
| `--duration` | 时长(秒): 5-10（默认5） |
| `--seed` | 随机种子 |

## 输出格式

```
Task submitted: <task_id>
IMAGE_SAVED: /path/to/image.png    # --output 模式
MEDIA_URL: https://...             # 无 --output 模式
```

## 进阶技巧

1. **角色定位** — 提示词开头加"你是一位资深电商平面设计师"
2. **锁定元素** — 引号标出必出内容，如"标题为'盛夏狂欢节'"
3. **风格先行** — 越早写"风格"效果越好
4. **分阶段生成** — 先简短提示词验证构图，满意后再加细节
5. **参考图** — 支持参考图+提示词双保险

## 注意事项

1. 生图任务通常 5-10 秒完成，视频任务 30-60 秒
2. 免费账户每日有积分限制（约66次生图）
3. 轮询间隔建议 3-5 秒，避免频繁请求
4. 图片通过 `binary_data_base64` 返回，无需处理过期URL
