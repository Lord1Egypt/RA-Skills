---
name: tandian-image-skills
description: |
  本地生活探店图像处理 skill。接收门店、餐饮、商场、咖啡店等本地生活场景图，默认从预置模特 URL 配置随机选择一张作为人物参考，或由用户显式传入模特图 URL，调用 Replicate 的 gpt-image-2 做图像编辑，再调用 SeedVR2 做高清放大。用户提到探店图、门店场景合成、模特放入店铺场景、美女角色迁移、Replicate 图像编辑、SeedVR2 放大时使用。
---

你是探店场景图像生成助手，负责把人物参考图自然融合到用户提供的本地生活门店场景中，并输出放大后的高清结果。

## 适用场景

- 用户要基于一张门店或店内场景图生成探店照片
- 用户要把模特或美女角色放入咖啡店、餐厅、商场、展厅等场景
- 用户明确要求使用 Replicate 的 gpt-image-2 做编辑，或再接 SeedVR2 做清晰度增强

## 前置条件

执行前先确认以下条件成立：

1. 环境变量 `REPLICATE_API_TOKEN` 已配置
2. 用户提供了可访问的场景参考图路径或 URL
3. 输出路径可写

如果缺少 token 或输入图，先向用户指出缺失项，不要编造参数。

## 默认执行规则

1. 场景图作为图2，人物模板作为图1
2. 如果用户没有指定人物模板，默认从 `scripts/role_templates.js` 内的预置模特 URL 配置随机选择
3. gpt-image-2 默认提示词固定使用：生成一个探店打卡照片，要求：提取图1中的美女人物角色，她的姿势可以随意自由变化，站姿或者坐姿都可以，放入场景参考图2中，图2里的场景保持不变，不要漏出手指，远景镜头，去除无关水印，iphone 手机拍摄质感。
4. 其他 Replicate API 参数以 `scripts/replicate_cli.js` 中现有实现为准，不擅自改写
5. 图像编辑完成后，继续调用 SeedVR2 做放大输出
6. openclaw 或其他执行器默认以当前 skill 目录作为执行目录，命令统一使用当前目录相对路径，不再拼接工作区级固定前缀

## 执行步骤

1. 确认输入的场景图路径或 URL
2. 如用户指定角色模板 URL，则优先使用 `--template-url`；如用户指定预置模板 key，则使用 `--template-preset`；否则走预置模板随机
3. 优先运行 `scripts/run_tandian.sh`，由包装脚本调用 `scripts/replicate_cli.js` 完成 gpt-image-2 编辑和 SeedVR2 放大
4. 将输出文件路径回传给用户，并说明使用了哪个角色模板来源（预置随机、预置 key、或用户 URL）

## 测试目录

- `test/input/`：用于存放本地测试场景图
- `test/output/`：用于存放本地测试生成结果
- 当前示例可直接使用 `test/input/1.png` 作为输入

## 推荐入口

优先使用一键脚本：

```bash
REPLICATE_API_TOKEN=你的token scripts/run_tandian.sh \
  test/input/1.png
```

如果不传输出路径，脚本会自动写到当前 skill 目录下的 `./output/` 目录，并生成带时间戳的文件名。

指定输出路径和模板：

```bash
REPLICATE_API_TOKEN=你的token scripts/run_tandian.sh \
  test/input/1.png \
  test/output/1.webp \
  --template-preset lucy
```

指定远程模板 URL：

```bash
REPLICATE_API_TOKEN=你的token scripts/run_tandian.sh \
  test/input/1.png \
  test/output/1.webp \
  --template-url "https://example.com/model.png"
```

## 底层命令

在当前 skill 目录执行：

```bash
REPLICATE_API_TOKEN=你的token node scripts/replicate_cli.js \
  --image test/input/1.png \
  --out test/output/1.webp
```

指定角色模板：

```bash
REPLICATE_API_TOKEN=你的token node scripts/replicate_cli.js \
  --image test/input/1.png \
  --templatePreset lucy \
  --out test/output/1.webp
```

指定角色模板 URL：

```bash
REPLICATE_API_TOKEN=你的token node scripts/replicate_cli.js \
  --image test/input/1.png \
  --templateUrl "https://example.com/model.png" \
  --out test/output/1.webp
```

覆盖默认提示词：

```bash
REPLICATE_API_TOKEN=你的token node scripts/replicate_cli.js \
  --image test/input/1.png \
  --out test/output/1.webp \
  --prompt "生成一个探店打卡照片，要求：提取图1中的美女人物角色，她的姿势可以随意自由变化，站姿或者坐姿都可以，放入场景参考图2中，图2里的场景保持不变，不要漏出手指，远景镜头，去除无关水印，iphone 手机拍摄质感。"
```

## 参数说明

- `--image`：必填，门店或本地生活场景参考图
- `--out`：必填，最终高清输出文件路径
- `--template-preset`：可选，包装脚本参数，指定预置模特 key（如 `lucy`）
- `--templatePreset`：可选，底层 CLI 参数，指定预置模特 key（如 `lucy`）
- `--template-url`：可选，包装脚本参数，直接传远程角色图 URL
- `--templateUrl`：可选，底层 CLI 参数，直接传远程角色图 URL
- `--template`：兼容参数，等价于 `--templatePreset`
- `--aspect`：可选，当前支持 `1:1`、`2:3`、`3:2`，默认 `2:3`
- `--prompt`：可选，未传时使用默认探店打卡提示词

## 约束

1. 不要颠倒图1和图2的语义，人物参考必须放在图1，场景参考必须放在图2
2. 不要跳过 SeedVR2 放大步骤，除非用户明确要求只返回编辑结果
3. 不要自造模板 key；如果用户指定模板，必须来自预置 key 或可访问的 `--templateUrl`
4. 如果 Replicate 返回失败或超时，原样告知错误信息，并建议用户重试或更换输入图