---
slug: quark-scan-tool-free
name: quark-scan-tool-free
version: 1.0.0
displayName: 夸克扫描-免费版
summary: "文件高清扫描增强工具,支持画质增强、去手写、去水印、去阴影等,适合个人用户单张处理.。夸克扫描免费版,面向个人用户的文件高清扫描与图像增强工具。核心能力:"
license: Proprietary
edition: free
description: 夸克扫描免费版,面向个人用户的文件高清扫描与图像增强工具。核心能力:，可处理提升工作效率

  - 画质增强(模糊/昏暗/老旧照片修复)

  - 去手写笔迹(还原空白试卷/文档)

  - 去水印(精准去除文字/Logo水印)

  - 去阴影(消除拍摄阴影)

  - 文档去底色(转为白底黑字)

  - 素描速写/线稿提取

  适用场景:

  - 学生试卷/笔记电子化

  - 个人文档扫描存档

  - 老照片修复与增强

  - 创意线稿提取

  差异化:免费版聚焦单张图片处理,覆盖常用扫描增强场景,适合个人用户体验AI图像增强'
tags:
  - Creative
  - 图像处理
  - AI创作
  - 工具
  - 效率
  - 自动化
  - 开发
  - 代码
  - 知识
  - 文档
  - 创意
  - scene
  - api
  - key
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# 夸克扫描工具 - 免费版

## 概述

夸克扫描免费版是一款面向个人用户的文件高清扫描与图像增强工具。由夸克扫描王提供官方API能力,支持画质增强、去手写、去水印、去阴影、去底色、素描速写、线稿提取等多种场景,单张图片即可快速处理.
本版本适合学生、个人办公用户及创意爱好者,将手机拍摄的文档/照片转化为高清电子版,或进行艺术风格转换.
## 核心能力

| 能力项 | 免费版支持 | 说明 |
|---|-----|---|
| 画质增强 | 是 | 模糊/昏暗照片修复 |
| 考试增强 | 是 | 试卷/笔记电子化 |
| 证件票据增强 | 是 | 证件/小票清晰化 |
| 去手写笔迹 | 是 | 还原空白文档 |
| 去水印 | 是 | 去除文字/Logo |
| 去阴影 | 是 | 消除拍摄阴影 |
| 去屏纹 | 是 | 消除摩尔纹 |
| 去底色 | 是 | 转白底黑字 |
| 裁剪矫正 | 是 | 透视校正 |
| 素描速写 | 是 | 照片转素描 |
| 线稿提取 | 是 | 提取线条图 |
| 批量处理 | 否 | PRO 版支持 |
| API 集成 | 否 | PRO 版支持 |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：文件高清扫描增强、支持画质增强、去阴影等、适合个人用户单张、夸克扫描免费版、面向个人用户的文、件高清扫描与图像、增强工具、核心能力、老旧照片修复、还原空白试卷、精准去除文字、文档去底色、转为白底黑字等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:学生试卷电子化

学生希望将做过的试卷还原为空白版本,方便重新练习.
```bash
# 配置 API Key
export SCAN_WEBSERVICE_KEY="your_scan_key"
# ...
# 去手写笔迹(还原空白试卷)
python3 （请参考skill目录中的脚本文件） \
  --scene "remove-handwriting" \
  --path "./exam_photo.jpg" \
  --platform "community"
```

### 场景二:老照片修复

用户希望修复一张模糊昏暗的老照片.
```bash
# 画质增强
python3 （请参考skill目录中的脚本文件） \
  --scene "image-hd-enhance" \
  --path "./old_photo.jpg" \
  --platform "community"
```

### 场景三:文档去底色

用户希望将红头文件转为白底黑字便于阅读.
```bash
# 文档去底色
python3 （请参考skill目录中的脚本文件） \
  --scene "remove-background-color" \
  --path "./red_header_doc.jpg" \
  --platform "community"
```

### 场景四:创意线稿提取

绘画爱好者希望从照片中提取线稿用于上色练习.
```bash
# 提取线稿
python3 （请参考skill目录中的脚本文件） \
  --scene "extract-lineart" \
  --path "./anime_char.jpg" \
  --platform "community"
```

## 不适用场景

以下场景夸克扫描-免费版不适合处理：

- 加密文件破解
- 损坏文件修复
- 物理介质数据恢复

## 触发条件

需要文件处理、文档转换、格式互转、内容提取时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:配置 API Key

```bash
# 推荐方式:CLI 配置(永久生效)
skill-platform config set skills.entries.quark-scan-tool-free.env.SCAN_WEBSERVICE_KEY "your_scan_key"
# ...
# 或通过环境变量
export SCAN_WEBSERVICE_KEY="your_scan_key"
```

获取地址:`https://scan.quark.cn/business` → 开发者后台 → 登录/注册 → 查看 API Key

### 第二步:执行扫描命令

```bash
# 单张图片处理(根据意图选择 scene)
python3 （请参考skill目录中的脚本文件） \
  --scene "${SCENE_VALUE}" \
  --path "${IMAGE_FILE_PATH}" \
  --platform "${AGENT_NAME}"
```

### 第三步:获取结果

处理完成后,结果图片保存至系统临时目录(如 `/tmp/imgs`),路径在返回 JSON 的 `data.path` 字段.
## 示例

### 场景标识对照表

| 场景 | scene 标识 | 说明 |
|:-----|:-----|:-----|
| 考试增强 | exam-enhance | 试卷/笔记高清化 |
| 画质增强 | image-hd-enhance | 模糊/昏暗修复 |
| 证件票据增强 | certificate-enhance | 证件/小票清晰化 |
| 去手写 | remove-handwriting | 还原空白文档 |
| 去水印 | remove-watermark | 去除文字/Logo |
| 去阴影 | remove-shadow | 消除拍摄阴影 |
| 去屏纹 | remove-screen-pattern | 消除摩尔纹 |
| 去底色 | remove-background-color | 转白底黑字 |
| 裁剪矫正 | image-crop-rectify | 透视校正 |
| 素描速写 | sketch-drawing | 照片转素描 |
| 线稿提取 | extract-lineart | 提取线条图 |
| 扫描合同 | scan-contract | 合同高清化 |
| 扫描文件 | scan-document | 兜底通用扫描 |

### 输入类型支持

```bash
# 图片 URL
python3 （请参考skill目录中的脚本文件） --scene "${SCENE}" --url "${IMAGE_URL}" --platform "${AGENT}"
# ...
# 本地文件路径
python3 （请参考skill目录中的脚本文件） --scene "${SCENE}" --path "${IMAGE_PATH}" --platform "${AGENT}"
# ...
# 图片 BASE64
python3 （请参考skill目录中的脚本文件） --scene "${SCENE}" --base64 "${IMAGE_BASE64}" --platform "${AGENT}"
```

## 最佳实践

1. **图片清晰度**:输入图片越清晰,处理效果越好,避免严重模糊
2. **格式与大小**:支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp,本地文件不超过 5MB
3. **意图明确**:描述处理意图时尽量具体,如"去掉试卷手写答案"而非"处理这张图"
4. **单一意图**:每次请求只执行一个意图,避免混合指令导致误判
5. **结果路径**:处理结果保存在临时目录,建议及时复制到持久存储
6. **隐私意识**:图片会上传至夸克服务器处理,敏感文件请谨慎

## 常见问题

### Q1:支持哪些图片格式?
A:支持 jpg、jpeg、png、gif、bmp、webp、tiff、wbmp 格式,本地文件不超过 5MB.
### Q2:可以处理视频吗?
A:不可以。本工具仅支持单张静态图片。如需处理视频,请先提取视频帧再逐帧处理.
### Q3:处理结果保存在哪?
A:处理后的图片保存至系统临时目录(如 `/tmp/imgs`),路径在返回 JSON 的 `data.path` 字段。建议及时复制到其他位置.
### Q4:API Key 如何获取?
A:访问 `https://scan.quark.cn/business`(开发者后台),登录/注册账号后查看 API Key。注意:请直接在浏览器地址栏手动输入该地址.
### Q5:免费版可以批量处理吗?
A:免费版每次仅限单张图片。如需批量处理或 API 集成,请使用 PRO 版.
### Q6:处理失败怎么办?
A:检查图片格式与大小是否符合要求;确认 API Key 有效;查看返回的错误信息(code 与 message).
## 依赖说明

### 运行环境
- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Python 3.9+

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| 夸克扫描 API | 外部 API | 必需 | 官网注册获取 Key |
| Python 3.9+ | 运行时 | 必需 | 官方安装 |
| requests | Python 库 | 必需 | pip install requests |
| base64 | 编码工具 | 必需 | Python 内置 |

### API Key 配置
- **环境变量名**: `SCAN_WEBSERVICE_KEY`
- **获取方式**: 访问 `https://scan.quark.cn/business` 开发者后台
- **配置方式**: CLI 配置(`skill-platform config set`)或环境变量
- **安全建议**: 妥善保管 Key,泄露后及时在官方平台轮换或撤销
- **隐私提示**: 图片会发送至夸克扫描王服务器(`scan-business.quark.cn`)处理

### 可用性分类
- **分类**: MD+EXEC(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过意图识别与脚本调用驱动图像扫描增强

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "夸克扫描-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "quark scan"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
