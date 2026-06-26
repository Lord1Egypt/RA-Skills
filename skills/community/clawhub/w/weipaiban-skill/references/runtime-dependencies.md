# 运行时依赖与数据流参考

本文件集中说明微排版技能在运行时所需的凭据、外部服务、本地二进制、磁盘写入以及数据流向。元数据（SKILL.md / README.md 顶部）是简要声明，此处是完整释义。

---

## 依赖总览

| 类别       | 名称                  | 必需 / 可选 | 用途                                   |
| ---------- | --------------------- | ----------- | -------------------------------------- |
| 凭据       | `WEIPAIBAN_API_KEY`   | 必需        | 微排版平台 API 鉴权                    |
| 凭据       | `WEIPAIBAN_API_BASE`  | 可选        | 自定义微排版 API 地址（默认官方）      |
| 凭据       | `VOLCENGINE_AK`       | 可选\*      | 火山引擎鉴权（Step 8 必需）            |
| 凭据       | `VOLCENGINE_SK`       | 可选\*      | 永久凭证鉴权（SK/TOKEN 二选一）        |
| 凭据       | `VOLCENGINE_TOKEN`    | 可选\*      | 临时凭证（AKTP/STS）鉴权               |
| 依赖技能   | `jimeng-ai`           | 可选        | 封装即梦图片生成调用                   |
| 本地二进制 | `python3`（≥3.9）     | 可选        | 运行 rembg                             |
| 本地二进制 | `rembg` CLI           | 可选        | 背景去除（仅使用 `u2netp` 轻量模型）   |
| 外部服务   | `weipaiban.cn`        | 必需        | 模板搜索、作品管理、素材 CDN 上传      |
| 外部服务   | 即梦 API              | 可选        | 根据 prompt 生成图片                   |
| 磁盘写入   | `/tmp/weipaiban-task-{workId}/` | 必需 | 任务中间文件（元信息、图片、进度）     |
| 磁盘写入   | `~/.u2net/u2netp.onnx`| 可选        | rembg u2netp 模型缓存（约 4.7MB）      |

> \* 整体 Step 8（图片生成）为可选阶段；一旦启用，则 `VOLCENGINE_AK` 必需，且 `VOLCENGINE_SK` 与 `VOLCENGINE_TOKEN` 至少配置其一。

---

## 数据流

### 基础流程（必需依赖）

```text
用户输入
  → 主代理
  → weipaiban.cn（模板搜索、克隆、获取 elements、更新作品）
  → 本地 /tmp/weipaiban-task-{workId}/（缓存中间 JSON）
  → 返回作品编辑链接
```

此流程仅在微排版平台和本地磁盘之间往返，不涉及第三方图片服务。

### 图片生成流程（可选阶段 Step 8）

```text
主代理
  → jimeng-ai 技能 → 即梦 API（发送 prompt / ratio，返回临时图片 URL）
  → 本地下载到 /tmp/weipaiban-task-{workId}/images/{elementId}_generated.png
  → rembg -m u2netp（若 needsTransparent=true）→ {elementId}_nobg.png
  → weipaiban.cn /api/v1/assets/upload 或 /api/v1/assets/fetch
  → 获取 CDN 永久 URL
```

> **重要**：发送给即梦 API 的 prompt 由用户主题 + 模板画像 + 配色方案拼接而成；图片内容最终会上传到 weipaiban CDN 并成为作品的一部分。用户应确认这两个服务对上传内容的隐私政策。

---

## 安装命令与副作用

### 安装 `jimeng-ai` 技能

通过 clawhub 或 find-skill 技能查找并安装。具体命令由 clawhub/find-skill 决定，不在本技能控制范围内。

### 安装 `rembg`

```bash
pip3 install "rembg[cpu,cli]~=2.0.67"
```

**副作用**：

- 安装 `rembg`、`onnxruntime`（CPU 版本）、`pymatting` 等依赖
- **首次运行时**下载 `u2netp.onnx`（约 4.7MB）到 `~/.u2net/u2netp.onnx`
- 本技能**固定**使用 `u2netp` 轻量模型（命令 `rembg i -m u2netp`），不会下载其他模型（如完整版 `u2net` 176MB）

### 版本升级流程（锁定版本维护）

为降低供应链风险，`rembg` 采用精确版本锁定。升级时按以下流程执行：

1. 在隔离环境评估新版本兼容性（命令参数、模型下载行为、处理质量）
2. 通过 Step 8 全链路回归（8a/8b/8c/8d）验证稳定性
3. 更新本文和 Step 8a 中的锁定版本号，保持文档口径一致
4. 在变更记录中注明升级理由与验证范围

### 申请 `VOLCENGINE_AK` / `VOLCENGINE_SK` / `VOLCENGINE_TOKEN`

需在火山引擎/即梦平台自行申请。本技能不会通过 API 自动生成或读取密钥文件。

- **永久凭证**：在火山引擎控制台创建访问密钥，得到 `AKLT…` 开头的 AK 与对应的 SK，配置 `VOLCENGINE_AK` + `VOLCENGINE_SK`
- **临时凭证（STS）**：通过 STS 接口换取临时凭证，得到 `AKTP…` 开头的 AK + Token，配置 `VOLCENGINE_AK` + `VOLCENGINE_TOKEN`（此时 SK 可省略）

---

## 用户同意原则

本技能严格遵循以下原则：

1. **不在未经用户同意的情况下执行安装命令**。Step 8a 的依赖检测只做"检测 + 展示结果 + 请求用户选择"，不会直接运行 `pip install` 或安装其他技能
2. **降级可用**：缺失可选依赖时，用户可选择跳过 Step 8，作品保留模板原图，其他步骤仍然完成
3. **展示完整命令**：用户选择「安装」后，每条命令执行前都会再次展示并请求确认

---

## 隔离与最小化凭据建议

- **隔离运行**：若对隐私或磁盘占用有顾虑，建议在容器或沙箱环境中运行。任务目录 `/tmp/weipaiban-task-*/` 默认随系统重启清理；`~/.u2net/u2netp.onnx` 可以手动删除
- **凭据最小化**：仅为微排版账号提供必要权限的 API Key。若使用火山引擎/即梦，建议优先使用 STS 临时凭证（`VOLCENGINE_AK` + `VOLCENGINE_TOKEN`），并设定使用期限或调用配额限制
- **任务目录清理**：任务完成后可手动执行 `rm -rf /tmp/weipaiban-task-{workId}/` 清理中间文件（技能本身不会主动删除，以便失败重试）

---

## 已知外部端点清单

- `https://weipaiban.cn/api/v1/templates` / `/templates/default` / `/templates/{id}/clone`
- `https://weipaiban.cn/api/v1/vectors/{workId}/parser`
- `https://weipaiban.cn/api/v1/assets/fetch` / `/assets/upload`
- 即梦图片生成端点（由 `jimeng-ai` 技能内部调用，本技能不直接暴露 URL）

本技能不会向除此之外的任何外部服务发送请求。
