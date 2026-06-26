# Session Contract

## 目标

为外呼 Agent 约定一个最小会话契约，确保 `auth.json` 不只是“保存成功”，而是“确实还能进入业务页”。

## 最小校验项

- 文件存在
- 文件可解析
- `cookies` 非空
- `origins` 存在或 cookie 足以支撑登录态
- 用该文件打开业务页后能进入工作台

## 推荐补充元数据

除 Playwright 原始存储状态外，建议额外记录：

- `saved_at`
- `saved_by`
- `target_url`
- `recheck_passed`
- `recheck_at`

如果不想污染 Playwright 原始结构，可保存为旁路文件，例如：

- `runtime/sessions/auth.meta.json`

## 复检策略

保存完会话后立即做一次冷启动校验：

1. 新建 browser context
2. 加载 `auth.json`
3. 打开业务 URL
4. 等待业务控件或成功接口
5. 成功才标记会话有效

## 失效信号

- 被重定向到登录页
- 出现扫码区、账号密码框、统一登录按钮
- 关键业务控件长期不可见
- 接口返回未认证或权限错误
