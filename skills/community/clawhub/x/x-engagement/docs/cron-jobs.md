# 手动提醒与维护

## 概述

本地安全版 `x-engagement` **默认不安装任何持久化调度任务**。

原因：
- 不直接修改用户 `crontab`
- 不直接创建后台常驻自动互动任务
- 所有维护和提醒都改成手动执行或由用户自行配置外部提醒工具

---

## 1. 每日热点总结

建议方式：
- 由用户在自己的日历、提醒事项、Notion、飞书任务里手动创建提醒
- 到点后由用户主动触发 skill

建议提醒文案：

```text
x-engagement: 查看 X Creator Inspiration 热点，更新 memory/daily/hotspots/tables/YYYY-MM-DD.md
```

---

## 2. 记忆清理

### 2.1 预览

```bash
cd /path/to/x-engagement
./scripts/cleanup-memory.sh
```

### 2.2 实际删除

```bash
cd /path/to/x-engagement
./scripts/cleanup-memory.sh --apply
```

说明：
- 默认只预览，不删除
- 只处理 `~/memory/daily/hotspots` 子树
- 遇到 symlink 或路径异常会拒绝执行

---

## 3. 手动提醒模板

生成模板：

```bash
./scripts/setup-cron.sh
```

这个脚本现在只会生成：

```text
runtime/manual-reminders.txt
```

它不会：
- 写入 `crontab`
- 调用任何后台调度器
- 自动注册 X 互动任务

---

## 4. 状态检查

```bash
./scripts/check-cron.sh
```

当前作用：
- 检查手动提醒模板是否存在
- 检查记忆目录是否存在
- 提示当前模式是“无自动调度”

---

## 5. 如果以后仍想要调度

建议原则：
1. 先审查将执行的命令
2. 先备份现有调度配置
3. 只创建提醒，不创建自动发帖/自动评论任务
4. 不要让调度器绕过人工确认

推荐：
- 用系统提醒类工具提醒“该去执行”
- 不要让调度器直接驱动浏览器去点赞/评论/关注

---

## 6. 安全边界

这个 skill 的安全边界现在是：
- Browser Relay 用于受控浏览器操作
- 记忆目录只在 `~/memory/daily/hotspots`
- 维护任务必须人工触发
- 评论、点赞、关注必须人工确认
