# week-to-day-splitter — 隐私清理说明

## 清理内容

发版前已清理：
- ❌ 真实姓名 ✓
- ❌ 真实路径（/Users/home/...）✓
- ❌ 项目代号（项目A-E、地点A-H、甲方A-I）✓
- ❌ 责任人（客户A-D）✓
- ❌ cron ID ✓
- ❌ 飞书 user_id ✓
- ❌ 飞书 webhook URL ✓

## 占位符

文档中使用的占位符：
- `${HOME}` — 用户主目录
- `${NOTES_DIR}` — 笔记根目录
- `${CRON_ID}` — 定时任务 ID
- `${FEISHU_USER_ID}` — 飞书用户 open_id
- `${FEISHU_WEBHOOK}` — 飞书机器人 webhook URL
- `${联系人}` — 责任人姓名（用真实姓名替换）

## 验证

发版前 6 轮 grep 复检：
1. ✅ 项目代号
2. ✅ 责任人
3. ✅ 真实路径
4. ✅ cron ID
5. ✅ 飞书 user_id
6. ✅ 飞书 webhook

## 使用前

1. 替换占位符为实际值（见占位符列表）
2. 安装依赖（无第三方 npm 包）
3. 配置 3 个 cron 任务（参考 SKILL.md）
