# 火山引擎API参考PDF关键页面提取摘要

## 提取页面概述

本次提取了火山引擎API参考PDF的28个关键页面，涵盖以下三个主要部分：

1. **第7页** - SDK安装及升级
2. **第10-15页** - 对话(Chat) API详细内容
3. **第450-470页** - 错误码完整列表和SDK使用说明

## 详细页面内容摘要

### 1. Base URL及鉴权（第11-13页）

#### 关键信息：
- **Base URL**：
  - 数据面 API：`https://ark.cn-beijing.volces.com/api/v3`
  - 管控面 API：`https://ark.cn-beijing.volcengineapi.com/`
  - Coding Plan用户需要使用特定的Base URL

#### 鉴权方式：
1. **API Key签名鉴权**（简单方便）：
   - 在HTTP请求header中添加 `Authorization: Bearer $ARK_API_KEY`
   - 适用于数据面API

2. **Access Key签名鉴权**（传统云上资源权限管控）：
   - 支持精细化的权限管理
   - 通过HMAC-SHA256签名
   - 签名相关字段：
     - Service：`ark`
     - Region：`cn-beijing`

3. **管控面API鉴权**：
   - 管理API Key、推理接入点等接口
   - 使用Access Key签名

### 2. 对话(Chat) API详细内容（第14-15页）

#### API端点：
- `POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`

#### 主要功能：
- 发送包含文本、图片、视频等模态的消息列表
- 模型生成对话中的下一条消息

#### 关键请求参数：
1. **model** (string, 必选)：
   - 调用的模型ID（Model ID）
   - 多个应用及精细管理场景推荐使用Endpoint ID

2. **messages** (object[], 必选)：
   - 消息列表，支持不同类型的消息
   - 消息类型包括：
     - 系统消息（system）：模型需遵循的指令
     - 用户消息（user）
     - 助手消息（assistant）

#### 消息结构：
- **role** (string, 必选)：发送消息的角色（system/user/assistant）
- **content** (string/object[], 必选)：消息内容
  - 纯文本内容
  - 多模态内容对象数组

### 3. 错误码完整列表（第460-470页）

#### 错误码分类：

##### 400 Bad Request 错误：
1. **敏感内容检测错误**：
   - `SensitiveContent.Detected.SevereViolation`：输入文本可能包含严重违规信息
   - `SensitiveContent.Detected.Violence`：输入文本可能包含激进行为相关信息
   - `InputTextSensitiveContentDetected`：输入文本可能包含敏感信息
   - `InputImageSensitiveContentDetected`：输入图像可能包含敏感信息
   - `InputVideoSensitiveContentDetected`：输入视频可能包含敏感信息
   - `InputAudioSensitiveContentDetected`：输入音频可能包含敏感信息
   - `OutputTextSensitiveContentDetected`：生成的文字可能包含敏感信息
   - `OutputImageSensitiveContentDetected`：生成的图像可能包含敏感信息
   - `OutputVideoSensitiveContentDetected`：生成的视频可能包含敏感信息
   - `OutputAudioSensitiveContentDetected`：生成的音频可能包含敏感信息
   - `InputTextSensitiveContentDetected.PolicyViolation`：输入文本可能违反平台规定
   - `InputImageSensitiveContentDetected.PolicyViolation`：输入图片可能违反平台规定
   - `InputVideoSensitiveContentDetected.PolicyViolation`：输入视频可能违反平台规定
   - `InputAudioSensitiveContentDetected.PolicyViolation`：输入音频可能违反平台规定
   - `InputImageSensitiveContentDetected.PrivacyInformation`：输入图片可能包含真人
   - `InputVideoSensitiveContentDetected.PrivacyInformation`：输入视频可能包含真人

2. **风险识别错误**：
   - `InputTextRiskDetection`：火山引擎风险识别产品检测到输入文本可能包含敏感信息
   - `InputImageRiskDetection`：火山引擎风险识别产品检测到输入图片可能包含敏感信息

##### 429 Too Many Requests 错误：
1. **速率限制错误**：
   - `ModelAccountRpmRateLimitExceeded`：请求已超过账户模型RPM(Requests Per Minute)限制
   - `ModelAccountTpmRateLimitExceeded`：请求已超过账户模型TPM(Tokens Per Minute)限制
   - `ModelAccountIpmRateLimitExceeded`：请求已超过账户模型IPM(Images Per Minute)限制
   - `APIAccountRpmRateLimitExceeded`：当前账号该接口的RPM限制已超出

2. **配额错误**：
   - `QuotaExceeded`：当前账号免费试用额度已消耗完毕
   - `QuotaExceeded`：当前账号处于排队中状态的任务数已超过限制

##### 其他常见错误：
- `InvalidRequest`：请求参数无效
- `MissingParameter`：缺少必要参数
- `ResourceNotFound`：请求的资源不存在
- `AccessDenied`：访问被拒绝
- `InternalError`：服务端内部错误

### 4. SDK使用说明（第7、10页）

#### Python SDK：
- **前提条件**：Python版本不低于3.7
- **安装方式**：
  - 使用pip：`pip install 'volcengine-python-sdk[ark]'`
  - 使用UV：`uv pip install volcengine-python-sdk[ark]`
  - 源码安装：`python setup.py install --user`

#### Java SDK：
- 通过Gradle安装
- 在`build.gradle`文件中添加依赖

#### Go SDK：
- 通过go get安装

## 关键发现

### 1. 双轨鉴权体系
火山引擎API采用双轨鉴权体系：
- **API Key鉴权**：简单便捷，适合快速开发和测试
- **Access Key鉴权**：支持精细化权限管理，适合企业级应用

### 2. 接口分类明确
- **数据面API**：面向业务数据传输和实时交互
- **管控面API**：用于系统资源管理和配置控制

### 3. 错误码体系完善
错误码按照HTTP状态码分类，涵盖：
- 客户端错误（400系列）
- 权限错误（403系列）
- 资源错误（404系列）
- 服务端错误（500系列）

### 4. 多模态支持
Chat API支持文本、图片、视频、音频等多种模态的输入输出。

## 使用建议

1. **开发环境**：推荐使用Python SDK，安装简便，文档完善
2. **鉴权选择**：个人开发可使用API Key，企业应用建议使用Access Key+IAM权限管理
3. **错误处理**：实现完整的错误处理逻辑，特别是敏感内容检测相关错误
4. **性能优化**：注意请求频率限制和并发限制，实现适当的重试机制

## 文件列表

提取的文件保存在`extracted_pages/`目录下：

### Base URL及鉴权部分：
- `page_007.txt` - SDK安装及升级
- `page_010.txt` - Java/Golang SDK安装
- `page_011.txt` - Base URL及鉴权概念
- `page_012.txt` - Access Key签名鉴权示例
- `page_013.txt` - Access Key签名方法

### 对话(Chat) API部分：
- `page_014.txt` - 对话(Chat) API概述及请求参数
- `page_015.txt` - 对话(Chat) API消息参数详细说明

### 错误码列表部分（第450-470页）：
- `page_450.txt` - 查询推理用量API
- `page_451.txt` - 查询推理用量参数说明
- `page_452-470.txt` - 完整的错误码列表，包括：
  - 敏感内容检测错误（400系列）
  - 速率限制错误（429系列）
  - 配额错误（429系列）
  - 其他常见错误

共提取28个页面文件，涵盖了火山引擎API的关键参考信息。

---
*提取时间：2026-04-15*
*PDF版本：火山引擎API参考文档*