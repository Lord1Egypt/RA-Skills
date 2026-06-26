# Workflow

## Input
- 单个视频 URL

## End States
- 下载成功，已记录
- 已存在，已补全并记录
- 已存在，无需下载，仅补记录
- 失败：链接不可访问
- 失败：不是可下载视频
- 失败：下载失败
- 失败：下载成功，但记录失败
- 失败：表格字段缺失/类型不匹配，已停止等待确认

## Step 1: 运行执行脚本
调用：
- `scripts/run_video_archive.py <url>`

该脚本负责：
1. URL 合法性校验
2. yt-dlp 元数据探测
3. 生成 `站点-视频ID` 主键
4. 本地目录/文件查重
5. 调用 `scripts/ytfetch.sh` 完成下载或补全
6. 探测本地视频分辨率 / 帧率 / 编码 / 码率
7. 输出结构化 JSON，包括：
   - `meta`
   - `file_path`
   - `info_json`
   - `record_fields`
   - `bitable.app_token`
   - `bitable.table_id`

## Step 2: 校验脚本结果
- 若 `ok=false`，直接返回错误并终止
- 若未定位到本地文件，终止
- 若缺少 `record_fields`，终止

## Step 3: 读取目标表字段
调用：
- `feishu_bitable_app_table_field.list`

目的：
- 校验目标表字段是否存在
- 校验字段类型是否与 `record_fields` 匹配

若发现以下任一情况，必须暂停并询问用户：
- 字段缺失
- 字段类型不匹配
- 需要新增字段

## Step 4: 查飞书表内是否已有记录
调用：
- `feishu_bitable_app_table_record.list`

筛选逻辑：
- 先按 `视频主键 is <主键>` 查
- 如无结果，可再按 `视频唯一ID is <主键>` 查

## Step 5: 写入飞书
### 若已有记录
调用：
- `feishu_bitable_app_table_record.update`

### 若没有记录
调用：
- `feishu_bitable_app_table_record.create`

写入内容：
- 使用脚本输出的 `record_fields`

## Step 6: 附件补充（后续可选增强）
当前可先不强制执行：
- 缩略图上传到“缩略图”字段
- `.info.json` 上传到“info.json (附件)”字段

若附件上传失败：
- 不回滚主记录
- 在“备注”中说明即可

## Step 7: 返回结果
返回时简洁说明：
- 是新下载还是补全
- 本地路径
- 是否写表成功
- 若写表失败，要明确说明“下载成功，但记录失败”

## Notes
- 下载成功但写表失败时，保留本地文件，不删除
- 如果用户手动移动了文件，优先反查，不要因为路径变化就直接重下
- 缩略图拿不到不应导致整个任务失败
