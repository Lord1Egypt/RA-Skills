# 惠科接口同步到多维表 Skill（独立包）

本文件夹为 **仅同步** 的 OpenClaw Skill：从惠科/小爱数据接口增量拉取数据并写入飞书多维表，不包含标注逻辑。

- **Skill 名称**：`xiaoai_sync_to_bitable`
- **入口**：`python sync_skill.py`
- **入参**：`minutes`、`folder_id`、`customer_id`、`app_id`、`app_secret`、`xiaoai_token`、`bitable_url`、`xiaoai_base_url`
- **输出**：`inserted_count`

上传到 Clawhub 时请上传本文件夹（`sync_skill/`）作为该 Skill 的根目录。
