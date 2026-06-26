---
name: teamgram-tool-services
description: Documents the tool services in Teamgram Server including idgen (Snowflake ID), status (online TTL), dfs (Minio file storage), and media (metadata/thumbnails).
compatibility: Documentation/knowledge skill only. No executable code. Reference material for Teamgram Server developers.
metadata:
  author: zhihang9978
  version: "1.0.0"
  source: https://github.com/teamgram/teamgram-server
  homepage: https://github.com/teamgram/teamgram-server
  openclaw:
    requires:
      env: []
      bins: []
    securityNotes: |
      Documentation-only skill. Contains no executable code, no network calls, no credential handling.
      Config snippets show localhost-only addresses from the default development setup.
      All content references the open-source teamgram-server project (Apache-2.0).
---

# 工具服务：idgen / status / dfs / media

## idgen（service.idgen）— ID 生成服务

### 配置

```yaml
Name: service.idgen
ListenOn: 127.0.0.1:20660
Etcd:
  Key: service.idgen
NodeId: 1
SeqIDGen:
  - Host: 127.0.0.1:6379
```

### 用途
- Snowflake/序列 ID 生成
- 生成 message_id / photo_id / dialog_id 等
- NodeId 配置用于分布式 Snowflake 避免 ID 冲突
- 序列 ID 使用 Redis 原子递增

### 关键代码路径
- `app/service/idgen/`

---

## status（service.status）— 在线状态服务

### 配置

```yaml
Name: service.status
ListenOn: 127.0.0.1:20670
Etcd:
  Key: service.status
Status:
  - Host: 127.0.0.1:6379
StatusExpire: 90
```

### 用途
- 维护用户在线状态
- 会话 TTL 管理（StatusExpire: 90秒）
- 被 BFF 调用来判断用户是否在线
- 被 session 调用来注册/注销在线会话

### 关键代码路径
- `app/service/status/`

---

## dfs（service.dfs）— 分布式文件存储

### 配置要点
- gRPC 端口：20640
- MiniHttp 端口：11701（HTTP 文件下载入口）
- 后端存储：Minio

### Minio Buckets

| Bucket | 用途 |
|---|---|
| documents | 文档文件 |
| photos | 照片 |
| videos | 视频 |
| encryptedfiles | 加密文件 |

### 用途
- 文件分片上传/下载
- 通过 MiniHttp (0.0.0.0:11701) 提供 HTTP 下载入口
- 被 BFF.files 模块调用

### 关键代码路径
- `app/service/dfs/`

---

## media（service.media）— 媒体处理服务

### 配置

```yaml
Name: service.media
ListenOn: 127.0.0.1:20650
Etcd:
  Key: service.media
Mysql:
  DSN: root:@tcp(127.0.0.1:3306)/teamgram?charset=utf8mb4&parseTime=true
Cache:
  - Host: 127.0.0.1:6379
Dfs:
  Etcd:
    Key: service.dfs
```

### 用途
- 媒体元数据管理
- 缩略图生成与处理
- 依赖 dfs 进行实际文件存取
- 依赖 MySQL 存储元数据（documents/photos/photo_sizes/video_sizes 表）

### 关键代码路径
- `app/service/media/`

---

## 文件上传下载完整链路

```text
Client
  -> files.upload* / upload.getFile
  -> bff.files
       -> dfs 保存/获取 file parts
       -> media 生成缩略图/元数据
       -> db 写入 documents/photos/photo_sizes/...
  <- 返回 inputFile / fileLocation / document/photo

DFS
  - Minio buckets: documents/photos/videos/encryptedfiles
  - MiniHttp 0.0.0.0:11701 提供 HTTP 下载入口
```

## 服务依赖关系

```text
bff.files → dfs (gRPC) → Minio (S3)
         → media (gRPC) → MySQL + dfs
idgen    → Redis (原子递增)
status   → Redis (TTL)
```


## Source Code References

- Repository: https://github.com/teamgram/teamgram-server (Apache-2.0)
