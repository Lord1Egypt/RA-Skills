---
name: quark-drive
description: |
  夸克网盘操作技能 - 支持扫码登录、文件列表、上传、下载、分享（可设密码/有效期）、转存、删除等操作。
  当用户提到夸克网盘、quark、网盘文件管理、上传下载、分享链接、转存资源时使用此技能。
metadata:
  openclaw:
    emoji: ☁️
    requires:
      bins: ['python3']
      env:
        - QUARK_COOKIE
---

# 夸克网盘操作技能

通过 Python 脚本操作夸克网盘，支持扫码登录、文件管理、分享、转存等功能。

## ⚠️ 使用前必读

1. **首次使用必须先登录**：运行 `python3 scripts/quark_cli.py login` 获取 Cookie
2. **Cookie 有效期**：约 7 天，过期后需重新登录
3. **文件大小限制**：单文件最大 40GB（超级会员）
4. **并发限制**：避免同时进行多个上传/下载任务
5. **COS 上传限制**：`pds.quark.cn` 是阿里云内网地址，外部无法直接解析。实际上传域名是 `{bucket}.pds.quark.cn`（如 `ul-sz.pds.quark.cn`），该子域名可正常解析。分片上传流程：pre→hash→PUT parts→commit（含 callback）
6. **QQ Bot 图片发送**：MEDIA: 语法不支持 qqbot。需直接调用 QQ Bot API：1) 获取 access_token；2) 上传图片到 `/v2/users/{chat_id}/files`（file_type=1, file_data=base64）；3) 发送消息（msg_type=7, media.file_info）

## 功能路由表

| 用户需求 | 命令 | 说明 |
|---------|------|------|
| "登录夸克网盘" | `python3 scripts/quark_cli.py login` | 扫码登录获取 Cookie |
| "列出文件" | `python3 scripts/quark_cli.py list [路径]` | 列出目录内容 |
| "搜索文件" | `python3 scripts/quark_cli.py search <关键词>` | 搜索文件 |
| "上传文件" | `python3 scripts/quark_cli.py upload <本地路径> <网盘路径>` | 上传文件 |
| "下载文件" | `python3 scripts/quark_cli.py download <网盘路径> <本地路径>` | 下载文件 |
| "删除文件" | `python3 scripts/quark_cli.py delete <路径>` | 删除文件/文件夹 |
| "清空文件" | `python3 scripts/quark_cli.py clear [路径]` | 清空指定目录 |
| "创建文件夹" | `python3 scripts/quark_cli.py mkdir <名称> [父目录]` | 创建文件夹 |
| "查看用户信息" | `python3 scripts/quark_cli.py user` | 显示用户信息和容量 |
| "分享文件" | `python3 scripts/quark_cli.py share <路径> --expire 7d --passcode 1234` | 创建分享链接（可设密码） |
| "查看我的分享" | `python3 scripts/quark_cli.py share-list` | 列出所有分享 |
| "取消分享" | `python3 scripts/quark_cli.py share-cancel <分享ID或链接>` | 取消分享 |
| "转存资源" | `python3 scripts/quark_cli.py share-save <分享链接> --to /目标目录` | 转存他人分享到我的网盘 |
| "批量上传目录" | `python3 scripts/quark_cli.py batch-upload <本地目录> --remote-dir /远程目录` | 批量上传整个目录 |

## 分享功能详解

### 创建分享（带密码）
```bash
# 无密码分享，7天有效
python3 scripts/quark_cli.py share /文档/report.pdf --expire 7d

# 带密码分享，30天有效
python3 scripts/quark_cli.py share /文档/report.pdf --expire 30d --passcode 1234

# 永久分享
python3 scripts/quark_cli.py share /文档/report.pdf --expire permanent
```

### 转存他人分享
```bash
# 基本转存
python3 scripts/quark_cli.py share-save "https://pan.quark.cn/s/xxxxx"

# 带密码转存
python3 scripts/quark_cli.py share-save "https://pan.quark.cn/s/xxxxx 提取码: 1234"

# 指定保存目录
python3 scripts/quark_cli.py share-save "https://pan.quark.cn/s/xxxxx" --to /我的资源
```

## 批量上传功能

### 基本用法
```bash
# 上传整个目录到夸克网盘
python3 scripts/quark_cli.py batch-upload /path/to/local/dir --remote-dir /远程目录

# 使用默认远程目录（/备份/日期）
python3 scripts/quark_cli.py batch-upload /path/to/local/dir
```

### 高级选项
```bash
# 跳过特定文件模式
python3 scripts/quark_cli.py batch-upload /path/to/dir --skip "__pycache__,.pyc,node_modules"

# 限制上传文件大小（MB）
python3 scripts/quark_cli.py batch-upload /path/to/dir --max-size 5

# 组合使用
python3 scripts/quark_cli.py batch-upload ~/.hermes --remote-dir /Hermes备份 --skip "cache,output,__pycache__" --max-size 20
```

### 批量上传特性
- ✅ 自动创建远程目录结构
- ✅ 支持秒传（相同文件自动跳过）
- ✅ 进度显示和统计
- ✅ 可配置跳过模式和文件大小限制
- ✅ 自动处理同名文件（夸克会自动加后缀）

## Cookie 配置

### 方式1：环境变量（推荐）
```bash
export QUARK_COOKIE="your_cookie_string_here"
```

### 方式2：配置文件
```bash
python3 scripts/quark_cli.py config --cookie "your_cookie_string_here"
```

### 方式3：扫码登录（推荐）
```bash
python3 scripts/quark_cli.py login
```

## 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 401 | 未授权 | 重新登录 |
| 403 | 禁止访问 | 检查文件权限 |
| 404 | 文件不存在 | 检查路径 |
| 413 | 文件过大 | 分片上传或压缩 |
| 500 | 服务器错误 | 稍后重试 |
| 14001 | 参数错误 | 检查文件夹参数名（应为file_name） |

## 上传坑点与解决方案

### 坑点1：文件夹创建参数错误
**问题**: 使用 `dir_name` 而非 `file_name` 会导致 400 错误
```python
# ✅ 正确
{"pdir_fid": parent_fid, "file_name": folder_name, "dir_init_lock": False, "dir_path": ""}

# ❌ 错误
{"pdir_fid": parent_fid, "dir_name": folder_name, ...}
```

### 坑点2：callback 编码错误
**问题**: callback 是 dict，需要 json.dumps 后再 base64
```python
# ✅ 正确
callback_b64 = base64.b64encode(json.dumps(callback).encode()).decode()

# ❌ 错误
callback_b64 = base64.b64encode(callback.encode()).decode()
```

### 坑点3：Cookie 鉴权问题
**问题**: GET 正常但 POST 返回 401
```python
# ✅ 正确：通过 cookies.set() 设置到域名
client = httpx.Client(headers={"User-Agent": "..."})
for part in cookie.split(";"):
    name, value = part.strip().split("=", 1)
    client.cookies.set(name.strip(), value.strip(), domain=".quark.cn")

# ❌ 错误
headers = {"Cookie": cookie_string, ...}
client = httpx.Client(headers=headers)
```

### 坑点4：POST 请求必须带公共查询参数
```python
# ✅ 所有请求URL需附加
params={"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
```

### 坑点5：重复文件处理
夸克网盘对同名文件自动加 `(1)`、`(2)` 后缀，不会覆盖。重跑上传前需清理。

## 技术实现

- **API 基础 URL**: `https://drive-pc.quark.cn`
- **认证方式**: Cookie（`__pus`）
- **上传方式**: 分片上传（支持断点续传）
- **下载方式**: 直链下载
- **分享协议**: 支持密码/有效期设置
