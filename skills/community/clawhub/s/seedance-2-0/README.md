# Seedance 2.0 Skill for OpenClaw

字节跳动 Seedance 2.0 AI视频生成技能，为 OpenClaw 提供开箱即用的视频生成能力，同时包含完整的申请开通指南。

## 功能特性

- 📋 **完整申请指南** - 引导用户通过邀请链接申请Seedance 2.0白名额
- 🎨 **提示词模板** - 内置常见场景提示词模板（宣传、活动、vlog等）
- ⚙️ **可配置参数** - 支持模型选择、时长、分辨率、比例等配置
- 📥 **自动下载** - 生成完成后自动下载视频文件到本地

## 安装依赖

```bash
cd /root/.openclaw/workspace/skills/seedance2.0
bun install
```

## 配置

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 `ARK_API_KEY`：
```
ARK_API_KEY=your-actual-api-key-here
```

## 使用

### 查看申请指南

```bash
bun run seedance2.0.ts --guide
```

这会输出完整的申请开通流程和邀请链接。

### 直接生成视频

```bash
# 使用自定义提示词
bun run seedance2.0.ts --prompt "麓湖社区丰富多彩的社群活动，邻里互动温馨热闹" --output output.mp4

# 使用模板 + 自定义提示词
bun run seedance2.0.ts --template promo --prompt "春季促销活动，限时5折优惠" --output promo.mp4

# 自定义参数
bun run seedance2.0.ts --prompt "产品演示" --model pro --duration 10 --ratio 16:9 --resolution 1080p --output video.mp4
```

## 可用模板

| 模板名 | 用途 |
|--------|------|
| promo | 产品宣传促销 |
| event | 活动预告 |
| vlog | 日常生活vlog |
| education | 知识科普 |
| marketing | 营销短视频 |

## 可用模型

| 模型名 | 模型ID | 说明 |
|--------|--------|------|
| pro | doubao-seedance-2-0-260128 | Seedance 2.0 Pro 最新版 |
| fast | doubao-seedance-1-0-fast | 快速版，生成更快 |
| lite | doubao-seedance-1-0-lite | 轻量版 |

## 完整参数说明

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|------|
| `--guide` | 输出申请开通指南 | 否 | - |
| `--prompt "text"` | 生成提示词 | 是* | - |
| `--template name` | 使用内置提示词模板 | 否* | - |
| `--model pro/fast/lite` | 选择模型 | 否 | `pro` |
| `--duration N` | 视频时长（秒），支持 5/10/16 | 否 | `5` |
| `--ratio 9:16/16:9/1:1` | 视频宽高比 | 否 | `9:16` |
| `--no-audio` | 关闭音频生成 | 否 | 默认开启 |
| `--watermark` | 开启水印 | 否 | 默认关闭 |
| `--ref-image URL` | 添加参考图片（可多次使用） | 否 | - |
| `--ref-video URL` | 添加参考视频（可多次使用） | 否 | - |
| `--ref-audio URL` | 添加参考音频（可多次使用） | 否 | - |
| `--output file.mp4` | 输出文件路径 | 否 | 自动生成 |

\* `--prompt` 和 `--template` 必须至少提供一个

## 申请开通

如果你还没有开通 Seedance 2.0 白名额，可以通过以下方式申请：

### 邀请链接
https://partner.volcengine.com/partners/auth/confirm?inviteToken=Z804VS6L0OUHUALB0UA450PEUPSJ4TYN4LA4JPO6F652OBSUUKI94FYKM5FL5YC2&partnerType=101&partnerName=%E6%99%BA%E7%BB%B4%E7%95%8C%EF%BC%88%E6%88%90%E9%83%BD%EF%BC%89%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&InvitationSource=1&ActivityCode=Seedance2.0

### 手机扫码
二维码文件存放在 `qrcode.png`，手机扫码直接绑定申请。

详细说明查看 [SKILL.md](./SKILL.md)
