---
name: 七牛云对象存储操作
description: 使用七牛云 Kodo 与 qshell 执行对象存储操作，包含下载 qshell、配置账号、查询 bucket、上传文件、下载文件。适用于用户提到七牛云、七牛 Kodo、qshell、对象存储上传下载、AK/SK、bucket、key、文件中转、把文件上传到七牛或从七牛下载到本地的场景。
---

# 七牛云对象存储操作

用于通过 **qshell** 操作七牛云对象存储（Kodo）。

## 何时使用

当用户要你：

- 下载并使用 `qshell`
- 配置七牛 AK / SK
- 向 bucket 上传文件
- 从 bucket 下载文件
- 创建新的 bucket
- 删除 bucket 中对象
- 查询 bucket 中对象是否存在
- 用七牛做临时文件中转

## 核心结论

### 1. 优先使用 qshell，不要优先手搓管理 API

虽然可以直接调 Kodo API，但下载对象内容时，实际链路比较绕。对于真实工作，`qshell` 更稳。

### 2. qshell 下载地址必须严格保留完整请求参数

实测可用的 Linux amd64 下载地址：

```text
https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-amd64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell
```

注意：

- 必须保留 `ref=developer.qiniu.com`
- 必须保留 `s_path=%2Fkodo%2F1302%2Fqshell`
- `s_path` 的 `/` 必须保留为 URL 编码后的 `%2F`
- 不要擅自去掉参数，不要手动改写编码

### 3. 下载 qshell 时建议带 Referer

实测直接裸 `curl` 可能拿到 `403 Forbidden`，以下方式可用：

```bash
curl -L \
  -H "Referer: https://developer.qiniu.com/kodo/1302/qshell" \
  -H "User-Agent: Mozilla/5.0" \
  "https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-amd64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell" \
  -o qshell.tar.gz
```

## 推荐工作流

1. 下载 qshell
2. 解压并赋予执行权限
3. 用 `qshell account` 配置 AK / SK
4. 用 `qshell user cu` 切换到目标账号
5. 如需创建空间，用 `mkbucket`
6. 上传中小文件优先用 `fput`，大文件优先用 `rput`
7. 删除对象用 `delete`
8. 下载单文件优先用 `get`；如需批量或按 key 列表下载，用 `qdownload2 + --key-file`
9. 下载到本地后，如需要避免冲突，手动加时间戳重命名

## 下载并准备 qshell

### Linux amd64

```bash
curl -L \
  -H "Referer: https://developer.qiniu.com/kodo/1302/qshell" \
  -H "User-Agent: Mozilla/5.0" \
  "https://kodo-toolbox-new.qiniu.com/qshell-v2.18.0-linux-amd64.tar.gz?ref=developer.qiniu.com&s_path=%2Fkodo%2F1302%2Fqshell" \
  -o qshell-v2.18.0-linux-amd64.tar.gz

tar -xzf qshell-v2.18.0-linux-amd64.tar.gz
chmod +x qshell
./qshell -v
```

如果用户已经把压缩包放到本地，例如：

```text
/home/xa/qshell-v2.18.0-linux-amd64.tar
```

则直接：

```bash
tar -xf /home/xa/qshell-v2.18.0-linux-amd64.tar -C ./tmp/bin
chmod +x ./tmp/bin/qshell
./tmp/bin/qshell -v
```

## 账号配置

优先要求：**AK / SK 配置在 `~/.openclaw/openclaw.json` 中**，不要在 skill 文件、脚本或最终回复里硬编码。

建议使用如下结构：

```json
{
  "skills": {
    "entries": {
      "qiniu-kodo-qshell": {
        "enabled": true,
        "env": {
          "QINIU_ACCESS_KEY": "your-ak",
          "QINIU_SECRET_KEY": "your-sk"
        }
      }
    }
  }
}
```

运行时从环境变量读取：

- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`

只有在用户明确要求临时测试、且当前环境没有配置可读时，才临时通过命令参数传入。完成任务后，不要在回复中回显密钥。

若必须手动配置 qshell，可使用：

```bash
./qshell account <AK> <SK> <account_name>
./qshell user cu <account_name>
```

注意：

- `account_name` 不能和本地已存在名称冲突，否则会报已存在
- 若需要避免冲突，使用时间戳或随机后缀

例如：

```bash
ACC="tempacct_$(date +%s)"
./qshell account "$AK" "$SK" "$ACC"
./qshell user cu "$ACC"
```

## 常用命令

### 1. 查询对象信息

```bash
./qshell stat <bucket> <key>
```

### 2. 创建空间（bucket）

`mkbucket` 用来创建新的空间。

```bash
./qshell mkbucket <bucket> [--region <region>] [--private]
```

参数：

- `<bucket>`：空间名，必填
- `--region`：区域，常见值：`z0`（华东）、`z1`（华北）、`z2`（华南）、`na0`（北美）、`as0`（东南亚）
- `--private`：创建私有空间；不带时默认创建公有空间

示例：

```bash
./qshell mkbucket my-bucket --region z1 --private
```

建议：

- 若用户没有明确指定区域，按文档默认 `z0`
- 创建前先确认 bucket 名未被占用
- 若用户强调私有下载链路或受控访问，优先创建私有空间

### 3. 上传文件

#### 3.1 `fput`：中小文件上传

`fput` 以 `multipart/form-data` 方式上传，适合中小文件。文档明确建议：**一般文件大小超过 100MB 时，优先改用分片上传**。

```bash
./qshell fput <bucket> <key> <local_file>
```

示例：

```bash
./qshell fput c2ol-fqx test.txt ./hello.txt
```

常用可选参数：

- `--overwrite`：覆盖已有对象
- `--mimetype <type>`：指定 MimeType
- `--file-type <n>`：指定存储类型
- `--accelerate`：启用上传加速

#### 3.2 `rput`：大文件/分片上传

`rput` 适合大文件，默认走分片上传 API V2，更稳。

```bash
./qshell rput <bucket> <key> <local_file>
```

示例：

```bash
./qshell rput c2ol-fqx big/video.mp4 ./video.mp4
```

常用可选参数：

- `--overwrite`：覆盖已有对象
- `--mimetype <type>`：指定 MimeType
- `--file-type <n>`：指定存储类型
- `--resumable-api-v2=false`：改用 V1 分片接口
- `--resumable-api-v2-part-size <bytes>`：设置 V2 分片大小
- `--accelerate`：启用上传加速

选择建议：

- 小文件、普通文档：优先 `fput`
- 大文件、视频、弱网环境：优先 `rput`
- 用户没有特别说明，但文件明显较大时，不要硬用 `fput`

### 4. 删除单个对象

`delete` 用来从空间中删除一个文件。

```bash
./qshell delete <bucket> <key>
```

示例：

```bash
./qshell delete c2ol-fqx old.txt
```

注意：

- 这是不可逆操作
- 删除前最好先和用户确认 key 是否正确
- 如果是批量删除需求，不要循环单条乱删，优先考虑 qshell 的批量能力

### 5. 下载文件

#### 5.1 `get`：单文件下载优先选项

官方文档里，`get` 就是下载指定文件的直接命令。

```bash
./qshell get <bucket> <key> [-o <outfile>]
```

示例：

```bash
./qshell get qiniutest test.txt
./qshell get qiniutest test.txt -o /tmp/test.txt
```

说明：

- `-o/--outfile`：指定本地保存路径
- `--domain`：指定下载域名；不指定时，qshell 会按自身优先级选 bucket 绑定域名或源站域名
- `--check-size` / `--check-hash`：下载后校验一致性
- `--enable-slice`：大文件时启用切片下载

建议：

- 下载单个明确 key：优先 `get`
- 需要按列表下载、目录式下载、批量下载：再用 `qdownload2`

#### 5.2 `qdownload2`：批量/按 key 列表下载

`qdownload2` **没有** `--key` 参数。下载单文件时，如必须使用它，也要通过 `--key-file` 提供 key 列表。

先创建一个只包含目标 key 的文件：

```bash
printf "comstudy.ino\n" > keys.txt
```

然后下载：

```bash
./qshell qdownload2 --bucket=c2ol-fqx --key-file=keys.txt --dest-dir=./download
```

### 6. 下载后加时间戳重命名

```bash
TS=$(date +%s)
cp ./download/comstudy.ino ./tmp/${TS}_comstudy.ino
```

## 可靠的单文件下载模板

```bash
set -e
QSH=./tmp/bin/qshell
BUCKET="c2ol-fqx"
KEY="comstudy.ino"
TS=$(date +%s)
mkdir -p ./tmp/qdl
printf "%s\n" "$KEY" > ./tmp/keys.txt
$QSH qdownload2 --bucket="$BUCKET" --key-file=./tmp/keys.txt --dest-dir=./tmp/qdl
FOUND=$(find ./tmp/qdl -type f -name "$KEY" | head -n 1)
cp "$FOUND" "./tmp/${TS}_comstudy.ino"
```

## 可靠的单文件上传模板

```bash
set -e
QSH=./tmp/bin/qshell
BUCKET="c2ol-fqx"
LOCAL="./tmp/example.txt"
REMOTE="example.txt"
$QSH fput "$BUCKET" "$REMOTE" "$LOCAL"
```

## Bundled scripts

### `scripts/get_with_qshell.sh`

单文件下载脚本，封装：

```bash
./qshell get <bucket> <key> -o <outfile>
```

用法：

```bash
bash scripts/get_with_qshell.sh <qshell_path> <bucket> <remote_key> <outfile>
```

### `scripts/upload_with_qshell.sh`

上传脚本，按文件大小自动选择 `fput` 或 `rput`：

- 默认阈值：`104857600` 字节（100MB）
- 小于阈值：`fput`
- 大于等于阈值：`rput`

可通过环境变量覆盖阈值：

```bash
QINIU_RPUT_THRESHOLD_BYTES=52428800 bash scripts/upload_with_qshell.sh ...
```

用法：

```bash
bash scripts/upload_with_qshell.sh <qshell_path> <bucket> <remote_key> <local_file>
```

### `scripts/delete_with_qshell.sh`

单对象删除脚本，封装：

```bash
./qshell delete <bucket> <key>
```

用法：

```bash
bash scripts/delete_with_qshell.sh <qshell_path> <bucket> <remote_key>
```

### `scripts/create_bucket_with_qshell.sh`

创建空间脚本，封装：

```bash
./qshell mkbucket <bucket> --region <region> [--private]
```

用法：

```bash
bash scripts/create_bucket_with_qshell.sh <qshell_path> <bucket> <region> [--private]
```

## 与文档转换类 skill 的组合工作流

当用户要做这种链路时：

- 从七牛下载 `pptx/pdf/docx/xlsx`
- 转为 Markdown
- 再上传回七牛

推荐组合：

1. 用本 skill 下载源文件到本地
2. 调用 `convert-document-to-markdown` 将文件转为 Markdown
3. 用本 skill 将生成的 `.md` 上传回 bucket

### Docker 权限经验

`convert-document-to-markdown` 依赖 Docker。若当前会话没有 Docker socket 权限，会报：

```text
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```

这通常说明：

- 当前用户不在 `docker` 组里，或
- 当前会话还没继承新的 `docker` 组权限

最小诊断思路：

```bash
id
ls -l /var/run/docker.sock
docker version
```

当 `id` 能看到 `docker` 组，并且 `docker version` 可用后，再重试 `convert-document-to-markdown`。

### 已验证组合链路

以下链路已在真实环境跑通：

- 从 `c2ol-fqx` 下载 PPT
- 使用 `convert-document-to-markdown` 成功转换为 Markdown
- 将 Markdown 上传回 `c2ol-fqx`

## 已验证经验

以下流程已在真实环境里跑通：

### 上传验证

- 使用 `qshell fput` 上传测试文件到 bucket
- 上传后对象存在

### 下载验证

- 使用 `qshell qdownload2 --key-file=...` 下载单文件
- 已成功将 `comstudy.ino` 下载到本地并重命名为带时间戳文件

### 真实踩坑

#### 坑 1：qdownload2 不支持 `--key`

错误示例：

```bash
./qshell qdownload2 --bucket=c2ol-fqx --key=comstudy.ino --dest-dir=tmp/qdl
```

会报：

```text
unknown flag: --key
```

正确方式：

```bash
printf "comstudy.ino\n" > keys.txt
./qshell qdownload2 --bucket=c2ol-fqx --key-file=keys.txt --dest-dir=tmp/qdl
```

#### 坑 2：下载 qshell 如果丢了 URL 参数，容易 403

不要把下载地址简化成不带 query 的裸 URL。

#### 坑 3：本地 qshell 账号名可能冲突

`qshell account ... tempacct` 如果已经存在，会失败。优先使用唯一账号名。

## 何时不要继续硬上

- 如果 qshell 下载站返回 403，先检查是否保留了完整 query 参数，是否带了 Referer
- 如果用户已经提供 qshell 压缩包路径，优先直接使用本地文件，不要反复联网下载
- 如果用户已经明文发 AK/SK，完成任务后提醒对方尽快轮换密钥

## 安全提醒

- 不要在最终回复中回显用户的 AK / SK
- 不要把 AK / SK 写入 skill 文件、仓库脚本或持久化配置
- 如无必要，不要长期保存 qshell 账户配置

## 输出建议

完成操作后，回复至少包含：

- bucket
- key
- 本地保存路径（下载场景）或远端 key（上传场景）
- 文件大小（若已知）
- 是否成功
