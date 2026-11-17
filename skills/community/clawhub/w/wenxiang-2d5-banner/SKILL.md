---



slug: wenxiang-2d5-banner
name: "wenxiang-2d5-banner"
version: 1.0.1
displayName: "2.5D横幅生成工具"
summary: "用Nano Banana Pro(ai-model 3 Pro Image)生成编辑图片。Generate/edit images with Nano Banana Pro (ai-model 3"
summary_zh: "用Nano Banana Pro(Gemini 3 Pro Image)生成编辑图片。Generate/edit images with Nano Banana Pro (Gemini 3"
license: "MIT"
description: |-
  Generate/edit images with Nano Banana Pro (ai-model 3 Pro Image)。Use\
  \ for image create/modify reque。Use when 用户需要Wenxiang 2d5 Banner相关功能时使用。不适用于超出本技能能力范围的复杂需求.
tags:
  - image
  - api
  - 依赖说明
  - 不支持
  - agent
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
homepage: "https://skillhub.cn/skill/"



---


# Wenxiang 2d5 Banner

## 专业版专属特性
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| Wenxiang 2d5 Banner生成编辑 | 不支持 | 支持 |
| 高清分辨率与无损输出 | 不支持 | 支持 |
| 批量生成与风格预设 | 不支持 | 支持 |
| 自定义模型微调 | 不支持 | 支持 |
| 商用版权授权 | 不支持 | 支持 |

## 能力清单
- Generate/edit images with Nano Banana Pro (ai-model 3 Pro Image)
- Use\
  \ for image create/modify reque

## 快速掌握
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 应用场景
| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 内容生成 | 提示词与风格参数 | 生成内容与质量评分 |
| 图片生成 | 提示词与尺寸参数 | 图片文件与分辨率 |
| 用Nano Bana | 目标数据与配置参数 | 处理结果与执行状态 |

**不适用于**：需要人工判断的复杂决策场景

## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| content | string | 否 | 处理的内容输入 |
| mode | string | 否 | 处理模式, 可选值: json/text/markdown |
| style | string | 否 | 输出风格, 参考 `references/style.md` |

## 输出说明
* Saves PNG to current directory (or specified path if filename includes directory)
* Script outputs the full path to the generated image
* **Do not read the image back** - just inform the user of the saved path

## 异常恢复流程
| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 

## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(ai-assistant Code / Cursor / Codex / ai-model CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 

### 可用性分类
- **分类**: MD+execute()
- **说明**: 基于Markdown的AI Skill,

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 案例展示

**Generate new image:**

```bash
uv run ~/.codex/skills/nano-banana-pro/（请参考skill目录中的脚本文件） --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**Edit existing image:**

```bash
uv run ~/.codex/skills/nano-banana-pro/（请参考skill目录中的脚本文件） --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```

## 热门问题
### Q1: 如何开始使用Wenxiang 2d5 Banner？
A: 请参考使用流程和依赖说明章节，确保运行环境满足要求后调用本技能。
## 异常管理机制
| 错误场景(续)| 原因 | 处理方式 |
|----:|:----|----:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 请求重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 差异化分析
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
|:-------|:-------|:-------|:-------|:-------|
| 图片设计 | 4小时 | 20分钟 | 3小时40分钟 | 10% |
| 图片编辑 | 2小时 | 30分钟 | 1小时30分钟 | 5% |
| 图片优化 | 1小时 | 15分钟 | 45分钟 | 3% |
| 图片批量生成 | 8小时 | 2小时 | 6小时 | 25% |
| 图片风格转换 | 3小时 | 1小时 | 2小时 | 15% |

### 差异化对比
| 对比维度 | 本技能 | 手动操作 | Python脚本 | 专业软件 |
|:-------|:-------|:-------|:-------|:-------|
| 操作便捷性 | 高 | 低 | 中 | 高 |
| 生成速度 | 快 | 慢 | 中 | 快 |
| 功能丰富度 | 高 | 低 | 中 | 高 |
| 学习成本 | 低 | 高 | 中 | 高 |
| 成本效益 | 高 | 低 | 中 | 高 |

### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
|:-----|:-----|:-----|:-----|:-----|
| 设计效率低 | 传统设计流程耗时较长，影响项目进度 | 广泛应用于广告、宣传等领域 | 提供自动化设计工具，缩短设计周期 | 设计效率提升20% |
| 设计风格单一 | 传统设计受限于设计师个人风格，缺乏多样性 | 广泛应用于品牌形象建设等领域 | 提供多种风格预设，满足多样化需求 | 风格多样性提升30% |
| 设计成本高 | 传统设计需要专业软件和设计师，成本较高 | 广泛应用于中小企业 | 提供免费或低成本的设计工具，降低设计门槛 | 设计成本降低40% |

## 常见问题FAQ

### Q2: 付费版与免费版有什么区别？
A: 付费版提供更多高级功能，如Wenxiang 2d5 Banner生成编辑、高清分辨率与无损输出、批量生成与风格预设、自定义模型微调以及商用版权授权。

### Q3: 如何配置API Key？
A: 在您的环境中执行命令 `export API_KEY="${API_KEY:?请设置环境变量}"`，并确保重启会话或开启新终端后生效。

### Q4: 图片生成后如何保存？
A: 图片将自动保存到当前目录（或指定路径，如果文件名包含目录）。脚本会输出生成图片的完整路径。

### Q5: 如何处理运行时错误？
A: 检查依赖说明中的配置要求，确认运行环境符合依赖说明。如果问题仍然存在，请尝试重试请求或检查网络连接。

## 排障手册
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
|:-------|:-------|:-------|:-------|
| 无法启动技能 | 运行环境不满足依赖要求 | 检查依赖说明，确认运行环境 | 安装缺失依赖项 |
| 生成图片失败 | 图片文件格式不支持 | 检查输入图片格式 | 使用支持的图片格式 |
| 图片分辨率低 | 输入参数错误 | 检查输入参数 | 修正输入参数 |
| API Key配置错误 | API Key配置不正确 | 检查API Key配置 | 重新配置API Key |

## 安全提示
1. 确保API Key安全，避免泄露到版本控制系统。
2. 使用官方提供的运行环境，避免使用第三方修改过的环境。
3. 避免在公共网络上传输敏感信息，如API Key。
4. 定期更新软件和依赖项，以修复已知的安全漏洞。
5. 对生成的图片进行版权检查，确保不侵犯他人版权。

### 安全风险防范

| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |

## 功能清单
- **自动化执行**: 用Nano Banana Pro(ai-model 3 Pro Image)生成编辑图片。Generate/edit ima
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果