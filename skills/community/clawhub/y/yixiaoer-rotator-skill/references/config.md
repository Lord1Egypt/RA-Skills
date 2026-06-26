# 蚁小二账号轮询配置

## 环境变量

**两个环境变量都是必需的：**

```bash
export YIXIAOER_API_KEY="你的蚁小二 API Key"
export YIXIAOER_MEMBER_ID="你的成员 ID"
```

## 如何获取 API Key 和成员 ID

1. 登录蚁小二后台：https://www.yixiaoer.cn
2. 进入 **团队管理** → **成员管理**
3. 找到你的成员账号
4. 复制 **成员 ID**（如：`69xxxxxxxxxxxxxxxxxxxxxx`）
5. 生成或复制 **API Key**

## 安全说明

- API Key 通过环境变量传递，不硬编码在代码中
- 状态文件 `account-rotator-state.json` 不含敏感凭据，可安全存储
