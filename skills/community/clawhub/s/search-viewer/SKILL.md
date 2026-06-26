# 🕵️ Search Viewer Skill

> 信息收集与空间测绘工具

## 简介

Search Viewer 是一个聚合多个空间测绘平台的信息收集工具，帮助渗透测试人员进行 reconnaissance（侦察）阶段的信息收集。

## 支持平台

| 平台 | 说明 | 用途 |
|------|------|------|
| **Fofa** | 网络空间搜索引擎 | 资产发现 |
| **Hunter** | 鹰图 | 企业资产查询 |
| **Shodan** | 物联网搜索引擎 | 设备发现 |
| **360 Quake** | 360空间测绘 | 资产发现 |
| **Zoomeye** | 钟馗之眼 | 网络空间探测 |

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/adminlove520/Search_Viewer.git
cd Search_Viewer
```

### 2. 安装依赖

```bash
pip install pyside2 requests
```

### 3. 运行

```bash
python Search_Viewer.py
```

## 使用方法

### 配置 API Key

首次使用需要配置各平台的 API Key：
- Fofa: 需要注册获取 FOFA_TOKEN
- Hunter: 需要积分
- Shodan: 需要 API Key
- 360 Quake: 需要 API Key
- Zoomeye: 需要登录获取 Token

### 搜索语法

#### Fofa 语法

```bash
# 搜索 title="nginx" 的网站
title="nginx"

# 搜索 banner="nginx" 
banner="nginx"

# 搜索端口 80 的主机
port=80

# 组合查询
domain="example.com" && port=443
```

#### Shodan 语法

```bash
# 搜索 nginx
nginx

# 搜索特定国家
country:CN

# 搜索特定端口
port:22

# 组合
nginx country:CN
```

#### Hunter 语法

```bash
# 搜索域名
domain="example.com"

# 搜索 ip
ip="1.1.1.1"
```

## 职业应用

### 渗透测试工程师

| 阶段 | 使用平台 | 目的 |
|------|----------|------|
| 信息收集 | Fofa/Zoomeye | 发现目标资产 |
| 子域名枚举 | Hunter/Shodan | 扩大攻击面 |
| 端口扫描 | Quake | 发现开放服务 |
| 指纹识别 | 全平台 | 识别技术栈 |

### 安全研究员

| 用途 | 说明 |
|------|------|
| 漏洞发现 | 通过空间测绘发现暴露资产 |
| 趋势分析 | 分析特定技术的全球分布 |
| 应急响应 | 快速定位受影响资产 |

## 典型查询示例

### 查找目标的资产

```bash
# Fofa: 查找目标域名相关的所有资产
domain="目标域名"

# Hunter: 企业资产查询
company="目标公司"
```

### 查找特定技术

```bash
# Fofa: 查找暴露的数据库
app="mysql" && port=3306

# Shodan: 查找暴露的 Redis
redis untagged
```

### 查找弱口令服务

```bash
# Shodan: 查找 SSH
port:22 has_ssh:true

# Fofa: 查找 FTP
ftp anon=Yes
```

## 注意事项

1. **合规使用**: 只对自己有授权的目标进行测试
2. **API 限制**: 各平台有查询限制，合理使用
3. **隐私保护**: 不要收集和存储敏感个人信息
4. **法律风险**: 遵守当地法律法规

## 相关资源

- 官方仓库: https://github.com/adminlove520/Search_Viewer
- Fofa: https://fofa.info
- Hunter: https://hunter.qianxin.com
- Shodan: https://www.shodan.io
- Zoomeye: https://www.zoomeye.org

## 更新日志

- 2026-03-12: 初始版本
