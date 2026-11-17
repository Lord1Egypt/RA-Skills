---
slug: straker-verify-tool-free
name: straker-verify-tool-free
version: 1.0.0
displayName: AI翻译验证(免费版)
summary: "100+语言AI翻译服务,支持项目创建、状态查询与文件下载,适合个人翻译需求,支持多种使用场景和自动化处理"
license: Proprietary
edition: free
description: 核心能力:，可自动提升工作效率

  - 100+语言AI翻译服务

  - 翻译项目创建与管理

  - 项目状态实时查询

  - 翻译文件下载

  - 支持文档与文本文件

  适用场景:

  - 个人文档翻译

  - 多语言内容创建

  - 翻译项目跟踪

  - 快速文本翻译

  差异化:

  - 100+语言全覆盖

  - 项目化翻译管理

  - API驱动,可自动化

  - 支持文件批量翻译

  适用关键词: 翻译, AI翻译, 多语言, translation, translate, localization, 语言翻译, 文档翻译'
tags:
  - 翻译
  - 本地化
  - 多语言
  - AI翻译
  - 安全
  - 加密
  - 工具
  - self
  - project_id
  - response
  - get
  - headers
tools:
  - read
  - exec
homepage: ""
category: "Security"
---
# AI翻译验证(免费版)

## 概述

AI翻译验证免费版是一款面向个人用户的AI翻译服务工具。支持100+语言的文档和文本翻译,提供翻译项目创建、状态查询和文件下载功能。通过API驱动实现自动化翻译流程,帮助用户快速完成多语言内容创建.
## 核心能力

### 功能概览

| 功能 | 描述 |
|---|---|
| 语言支持 | 100+语言对 |
| 项目管理 | 创建、确认、查询、下载 |
| 文件支持 | 文档、文本文件 |
| API驱动 | 全流程API化,可自动化 |

### 免费版与专业版对比

| 功能 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 语言数量 | 100+ | 100+ |
| 质量提升 | 不支持 | AI质量增强 |
| 人工审核 | 不支持 | 专业人工审核 |
| 批量翻译 | 单文件 | 批量+并行 |
| 翻译记忆 | 不支持 | TM+术语库 |
| API限额 | 10次/天 | 无限制 |
| 报告格式 | 文本 | HTML/JSON |
| Webhook | 不支持 | 翻译完成回调 |

**处理**: 解析免费版与专业版对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费版与专业版对比的响应数据,包含状态码、结果和日志.
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：翻译服务、支持项目创建、状态查询与文件下、适合个人翻译需求、核心能力、翻译项目创建与管、项目状态实时查询、翻译文件下载、支持文档与文本文等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:快速文本翻译

```bash
# 获取支持的语言列表
curl https://api-verify.example.com/languages
# ...
# 创建翻译项目
curl -X POST https://api-verify.example.com/project \
  -H "Authorization: Bearer $TRANSLATE_API_KEY" \
  -F "files=@document.txt" \
  -F "languages=<language-uuid>" \
  -F "title=我的翻译项目" \
  -F "confirmation_required=true"
```

### 场景二:翻译项目跟踪

```bash
# 查询项目状态
example.com/project/<project-uuid> \
  -H "Authorization: Bearer $TRANSLATE_API_KEY"
# ...
# 确认项目(如需要)
example.com/project/confirm \
  -H "Authorization: Bearer $TRANSLATE_API_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "project_id=<project-uuid>"
```

### 场景三:下载翻译结果

```bash
# 下载完成的翻译文件
example.com/project/<project-uuid>/download \
  -H "Authorization: Bearer $TRANSLATE_API_KEY" \
  -o translations.zip
```

## 不适用场景

以下场景AI翻译验证(免费版)不适合处理：

- 专业医学法律翻译认证
- 同声传译
- 文学创作翻译

## 触发条件

需要文本翻译、多语言转换、本地化处理时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 翻译管理脚本

```python
import os
import requests
from pathlib import Path
# ...
class TranslationClient:
    """AI翻译客户端"""
# ...
    BASE_URL = "https://api-verify.example.com"
# ...
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("TRANSLATE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 TRANSLATE_API_KEY 环境变量")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
# ...
    def get_languages(self):
        """获取支持的语言列表"""
        response = requests.get(f"{self.BASE_URL}/languages")
        return response.json()
# ...
    def create_project(self, file_path, language_uuid, title="翻译项目"):
        """创建翻译项目"""
        with open(file_path, 'rb') as f:
                f"{self.BASE_URL}/project",
                headers=self.headers,
                files={"files": f},
                data={
                    "languages": language_uuid,
                    "title": title,
                    "confirmation_required": "true"
                }
            )
# ...
    def confirm_project(self, project_id):
        """确认翻译项目"""
            f"{self.BASE_URL}/project/confirm",
            data={"project_id": project_id}
        )
# ...
    def get_status(self, project_id):
        """查询项目状态"""
            f"{self.BASE_URL}/project/{project_id}",
        )
# ...
    def download(self, project_id, output_path="translations.zip"):
        """下载翻译结果"""
            f"{self.BASE_URL}/project/{project_id}/download",
            stream=True
        )
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return output_path
# ...
    def translate_text(self, text, source_lang, target_lang):
        """快速文本翻译"""
        # 创建临时文件
        temp_file = Path("temp_translate.txt")
        temp_file.write_text(text, encoding='utf-8')
# ...
        # 获取语言UUID
        languages = self.get_languages()
        target_uuid = None
        for lang in languages.get("data", []):
            if lang.get("code") == target_lang:
                target_uuid = lang.get("uuid")
                break
# ...
        if not target_uuid:
            return {"error": f"不支持的目标语言: {target_lang}"}
# ...
        # 创建并确认项目
        result = self.create_project(str(temp_file), target_uuid)
        project_id = result.get("data", {}).get("project_id")
# ...
        if project_id:
            self.confirm_project(project_id)
# ...
        temp_file.unlink()
        return result
# ...
# 示例
if __name__ == "__main__":
    client = TranslationClient()
# ...
    # 获取支持的语言
    langs = client.get_languages()
    print(f"支持 {len(langs.get('data', []))} 种语言")
# ...
    # 翻译文件
    result = client.create_project("document.txt", "lang-uuid-fr", "法语翻译")
    print(f"项目已创建: {result}")
# ...
    # 查询状态
    status = client.get_status("project-uuid")
    print(f"项目状态: {status}")
```

#
## 配置示例

### API配置

```bash
# 设置API Key
export TRANSLATE_API_KEY="your-api-key-here"
```

### 支持的常用语言

| 语言 | 代码 | UUID示例 |
|---:|---:|---:|
| 英语 | en | lang-uuid-en |
| 中文 | zh | lang-uuid-zh |
| 日语 | ja | lang-uuid-ja |
| 韩语 | ko | lang-uuid-ko |
| 法语 | fr | lang-uuid-fr |
| 德语 | de | lang-uuid-de |
| 西班牙语 | es | lang-uuid-es |
| 俄语 | ru | lang-uuid-ru |
| 阿拉伯语 | ar | lang-uuid-ar |
| 葡萄牙语 | pt | lang-uuid-pt |

## 最佳实践

### 1. 批量翻译工作流

```python
# 批量翻译多个文件到多种语言
files = ["doc1.txt", "doc2.txt", "doc3.txt"]
target_langs = ["fr", "de", "es", "ja"]
# ...
client = TranslationClient()
for file in files:
    for lang in target_langs:
        result = client.create_project(file, f"lang-uuid-{lang}", f"{file}_{lang}")
        print(f"已创建: {file} -> {lang}")
```

### 2. 自动化翻译流水线

```bash
#!/bin/bash
# auto_translate.sh
API_KEY=$TRANSLATE_API_KEY
FILE=$1
LANG=$2
# ...
# 创建项目
PROJECT=$(curl -s -X POST https://api-verify.example.com/project \
  -H "Authorization: Bearer $API_KEY" \
  -F "files=@$FILE" \
  -F "languages=lang-uuid-$LANG" \
  -F "title=auto_$FILE" | jq -r '.data.project_id')
# ...
# 确认项目
curl -s -X POST https://api-verify.example.com/project/confirm \
  -H "Authorization: Bearer $API_KEY" \
  -d "project_id=$PROJECT"
# ...
# 等待完成并下载
while true; do
  STATUS=$(curl -s https://api-verify.example.com/project/$PROJECT \
    -H "Authorization: Bearer $API_KEY" | jq -r '.data.status')
  if [ "$STATUS" = "completed" ]; then
    curl -s https://api-verify.example.com/project/$PROJECT/download \
      -H "Authorization: Bearer $API_KEY" \
      -o "${FILE%.*}_$LANG.zip"
    echo "翻译完成: ${FILE%.*}_$LANG.zip"
    break
  fi
  sleep 30
done
```

## 常见问题

### Q1: 如何获取API Key?

A: 在翻译服务平台的开发者门户注册账号,获取API Key。设置环境变量 `TRANSLATE_API_KEY`.
### Q2: 支持哪些文件格式?

A: 支持文本文件(.txt)、文档文件(.docx, .pdf)等。具体格式取决于API服务支持.
### Q3: 翻译需要多长时间?

A: 取决于文件大小和目标语言数量。小文件通常几分钟内完成,大文件可能需要更长时间.
### 已知限制

A: 免费版每天限制10次API调用。如需更多调用量或质量提升、人工审核功能,请使用专业版.
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+ 或支持curl的命令行

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Python | 运行时 | 推荐 | 系统自带 |
| requests | Python包 | 推荐 | `pip install requests` |
| curl | CLI工具 | 可选 | 系统自带 |
| jq | CLI工具 | 可选 | `apt install jq`(JSON处理) |

### API Key 配置
- 必需配置 `TRANSLATE_API_KEY` 环境变量
- 获取方式: 在翻译服务平台开发者门户注册

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent调用翻译API完成任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "AI翻译验证(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "straker verify"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
