---
name: threatbook-skills
description: 集成微步在线威胁情报API，提供文件上传分析、文件信誉查询、多引擎检测、IP信誉查询和失陷检测能力；当用户需要分析可疑文件、查询文件威胁情报、检测IP安全状态或排查主机失陷风险时使用
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["THREATBOOK_API_KEY"]},"primaryEnv":"THREATBOOK_API_KEY"}}
dependency:
  python:
    - requests==2.28.0
---

# 微步在线威胁情报查询

## 任务目标
- 本 Skill 用于：集成微步在线（ThreatBook）的威胁情报API，提供全面的威胁情报查询能力
- 能力包含：文件上传分析、文件信誉报告、多引擎检测、IP信誉查询、失陷检测
- 触发条件：用户需要分析文件安全性、查询IP威胁情报、检测系统是否失陷

## 前置准备
- 依赖说明：脚本所需的依赖包及版本
  ```
  requests==2.28.0
  ```
- API凭证配置：需要微步在线API Key
  - 获取方式：访问 https://x.threatbook.cn 注册账号后，在个人中心获取API Key
  - 首次使用时会提示配置API Key

## 操作步骤

### 1. 文件上传分析
- **使用场景**：上传可疑文件进行威胁分析
- **执行方式**：调用 `scripts/file_upload.py`
- **参数说明**：
  - `file_path`：待分析的文件路径
- **示例**：
  ```bash
  python scripts/file_upload.py --file_path /path/to/suspicious.exe
  ```

### 2. 文件信誉报告
- **使用场景**：根据文件hash查询威胁情报
- **执行方式**：调用 `scripts/file_report.py`
- **参数说明**：
  - `hash_value`：文件的sha256/md5/sha1值
- **示例**：
  ```bash
  python scripts/file_report.py --hash_value 5d41402abc4b2a76b9719d911017c592
  ```

### 3. 多引擎检测报告
- **使用场景**：获取文件的多引擎反病毒扫描结果
- **执行方式**：调用 `scripts/file_multiengines.py`
- **参数说明**：
  - `hash_value`：文件的sha256/md5/sha1值
- **示例**：
  ```bash
  python scripts/file_multiengines.py --hash_value 5d41402abc4b2a76b9719d911017c592
  ```

### 4. IP信誉查询
- **使用场景**：查询IP地址的威胁情报信息
- **执行方式**：调用 `scripts/ip_reputation.py`
- **参数说明**：
  - `ip`：待查询的IP地址
- **示例**：
  ```bash
  python scripts/ip_reputation.py --ip 8.8.8.8
  ```

### 5. 失陷检测
- **使用场景**：检测域名或IP是否存在失陷风险
- **执行方式**：调用 `scripts/dns_compromise.py`
- **参数说明**：
  - `resource`：域名或IP地址
- **示例**：
  ```bash
  python scripts/dns_compromise.py --resource example.com
  ```

## 资源索引
- 文件上传分析：见 [scripts/file_upload.py](scripts/file_upload.py)
- 文件信誉报告：见 [scripts/file_report.py](scripts/file_report.py)
- 多引擎检测：见 [scripts/file_multiengines.py](scripts/file_multiengines.py)
- IP信誉查询：见 [scripts/ip_reputation.py](scripts/ip_reputation.py)
- 失陷检测：见 [scripts/dns_compromise.py](scripts/dns_compromise.py)

## 注意事项
- 所有API调用需要有效的API Key，首次使用请先配置凭证
- 文件上传功能仅支持小于特定大小的文件（具体限制请参考微步在线官方文档）
- API调用有频率限制，请勿短时间内频繁调用
- 返回结果中的威胁等级和情报信息仅供参考，请结合实际情况判断

## 使用示例

### 示例1：分析可疑文件
```bash
# 上传文件进行分析
python scripts/file_upload.py --file_path ./malware.exe

# 根据返回的hash查询详细报告
python scripts/file_report.py --hash_value <returned_hash>
```

### 示例2：查询IP威胁情报
```bash
# 查询单个IP
python scripts/ip_reputation.py --ip 192.168.1.1

# 批量查询可编写脚本循环调用
```

### 示例3：失陷检测排查
```bash
# 检测可疑域名
python scripts/dns_compromise.py --resource suspicious-domain.com

# 检测可疑IP
python scripts/dns_compromise.py --resource 10.0.0.1
```
