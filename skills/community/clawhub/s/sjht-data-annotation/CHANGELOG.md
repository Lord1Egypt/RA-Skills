# Changelog — data-annotation skill

所有日期格式为 YYYY-MM-DD。

## [1.1.0] - 2026-03-19

### 变更
- **计划驱动工作流**：新增 plan.json 标注计划机制，处理前先制定计划列出所有数据，逐条处理并更新进度
- **逐条处理防超时**：从批量处理改为每次只处理 1 条数据，处理完立即保存到 JSONL，避免超时丢失进度
- **进度汇报机制**：每处理完几条数据汇报进度（已处理 X/Y，耗时 N 秒），快超时时暂停并汇报

### 修复（实战经验）
- **视频抽帧密度增加**：每秒至少 2 帧，短视频至少 15 帧，中视频至少 20 帧，长视频至少 30 帧
- **nginx 配置教训**：
  - 不要创建独立 server 块监听 80（会冲突），改为在已有站点中添加 location
  - 使用 `^~` 前缀匹配避免正则 location 劫持 mp4/jpg 请求
  - `/root` 目录权限必须 755，否则 nginx 无法访问
  - nginx reload 可能不够，必要时 restart
- **Web 页面修复**：
  - apiBase 必须用 nginx 反代路径（`/annotation-api/`），不硬编码 localhost:8888
  - 所有文本字段 contentEditable，标签支持增删
  - 未保存修改时离开页面要有 beforeunload 警告
  - 视频文件通过 nginx 静态服务，不通过 API
- **docx 读取**：新增 pandoc 备选方案（python-docx 失败时）

## [1.0.0] - 2026-03-19

### 新增
- **完整工作流**：需求确认 → 数据读取 → 模型处理 → 标注生成 → 结果存储 → Web 查看/编辑 → Nginx 部署
- **SKILL.md**：7 步工作流程说明，包含模型选择策略、输出格式、部署流程
- **annotation-viewer.html**：Web 标注查看/编辑页面模板
- **annotation-api.py**：轻量 HTTP API 服务（文件列表/读取/保存）
- **annotation-api.service**：systemd 服务模板
- **output-formats.md**：常见标注输出格式参考
- **skill.json**：skill 元数据配置

### 设计决策
- 结果存储在数据同目录的 `results/` 子目录下
- 使用 JSONL 作为默认输出格式
- Web 页面为纯静态 HTML，通过 Python API 服务处理保存
- API 服务绑定 127.0.0.1，通过 nginx 反向代理对外提供访问
- 模型按数据类型选择：图像/视频用 VL 模型，文本用 LLM
