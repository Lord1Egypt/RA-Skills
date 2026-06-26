# 夸克网盘技能

纯 Python 实现的夸克网盘操作技能，支持扫码登录、文件管理、批量上传、分享、转存等功能。

## 功能

- ✅ 扫码登录（获取 Cookie）
- ✅ 查看用户信息和容量
- ✅ 列出文件/目录
- ✅ 搜索文件
- ✅ 上传文件
- ✅ 下载文件
- ✅ 删除文件/文件夹
- ✅ 清空目录
- ✅ 创建文件夹
- ✅ 分享文件（可设密码/有效期）
- ✅ 查看分享列表
- ✅ 取消分享
- ✅ 转存他人分享
- ✅ **批量上传目录** ⭐ 新增

## 快速开始

### 1. 安装依赖

```bash
pip install httpx
```

### 2. 登录

```bash
python3 scripts/quark_cli.py login
```

扫描二维码完成登录，Cookie 自动保存。

### 3. 常用命令

```bash
# 列出根目录文件
python3 scripts/quark_cli.py list

# 上传文件
python3 scripts/quark_cli.py upload /本地文件 /远程路径

# 批量上传目录 ⭐ 新增
python3 scripts/quark_cli.py batch-upload /本地目录 --remote-dir /远程目录

# 分享文件（带密码，30天有效）
python3 scripts/quark_cli.py share /文档/report.pdf --expire 30d --passcode 1234

# 转存他人分享
python3 scripts/quark_cli.py share-save "https://pan.quark.cn/s/xxxxx" --to /我的资源
```

## 命令列表

| 命令 | 说明 | 示例 |
|------|------|------|
| `login` | 扫码登录 | `login --timeout 300` |
| `user` | 查看用户信息 | `user` |
| `list` | 列出文件 | `list /文档` |
| `search` | 搜索文件 | `search "关键词"` |
| `upload` | 上传文件 | `upload /本地 /远程` |
| `download` | 下载文件 | `download /远程 /本地` |
| `delete` | 删除文件 | `delete /路径 -y` |
| `clear` | 清空目录 | `clear /目录 -y` |
| `mkdir` | 创建文件夹 | `mkdir "文件夹名" --parent /父目录` |
| `share` | 分享文件 | `share /文件 --expire 7d --passcode 1234` |
| `share-list` | 查看分享 | `share-list` |
| `share-cancel` | 取消分享 | `share-cancel <分享ID>` |
| `share-save` | 转存资源 | `share-save "链接" --to /目录` |
| `batch-upload` | 批量上传 | `batch-upload /本地目录 --remote-dir /远程目录` ⭐ |

## 批量上传功能

### 基本用法

```bash
# 上传整个目录
python3 scripts/quark_cli.py batch-upload /path/to/dir --remote-dir /远程目录

# 使用默认远程目录（/备份/日期）
python3 scripts/quark_cli.py batch-upload /path/to/dir
```

### 高级选项

```bash
# 跳过特定文件模式
python3 scripts/quark_cli.py batch-upload /dir --skip "__pycache__,.pyc,node_modules"

# 限制上传文件大小（MB）
python3 scripts/quark_cli.py batch-upload /dir --max-size 5

# 组合使用
python3 scripts/quark_cli.py batch-upload ~/.hermes --remote-dir /Hermes备份 --skip "cache,output" --max-size 20
```

### 批量上传特性

- ✅ 自动创建远程目录结构
- ✅ 支持秒传（相同文件自动跳过）
- ✅ 进度显示和统计
- ✅ 可配置跳过模式和文件大小限制
- ✅ 自动处理同名文件（夸克会自动加后缀）

## 分享功能

### 创建分享

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

## Cookie 配置

### 方式1：扫码登录（推荐）

```bash
python3 scripts/quark_cli.py login
```

### 方式2：环境变量

```bash
export QUARK_COOKIE="your_cookie_string"
```

### 方式3：配置文件

```bash
python3 scripts/quark_cli.py config --cookie "your_cookie_string"
```

## 上传坑点

### 1. 文件夹创建参数
使用 `file_name` 而非 `dir_name`：
```python
{"pdir_fid": parent_fid, "file_name": folder_name, "dir_init_lock": False}
```

### 2. callback 编码
callback 是 dict，需要 json.dumps 后再 base64：
```python
callback_b64 = base64.b64encode(json.dumps(callback).encode()).decode()
```

### 3. Cookie 鉴权
通过 `cookies.set()` 设置到域名，不能仅放在 headers 中：
```python
client.cookies.set(name, value, domain=".quark.cn")
```

### 4. 公共查询参数
所有请求需附加 `?pr=ucpro&fr=pc&uc_param_str=`

### 5. 重复文件处理
夸克对同名文件自动加 `(1)` 后缀，不会覆盖。

## 技术实现

- **API 域名**: `https://drive-pc.quark.cn`
- **认证方式**: Cookie（`__pus`）
- **上传方式**: 分片上传（支持秒传和断点续传）
- **分享协议**: 支持密码/有效期设置
- **依赖**: httpx

## License

MIT
