# 配置说明

这个 skill 依赖当前项目提供的平台 API，不是直接调用禅镜原始接口。

## 用户先做什么

用户需要先完成这几步：

1. 打开 `http://easyclaw.bar/shuziren/user/` 登录平台。
2. 在平台里填写自己的禅镜 `app_id` 和 `secret_key`。
3. 如需查看禅镜官方密钥页面，引导用户访问 `https://www.chanjing.cc/platform/api_keys`。
4. 在本平台的“接口凭据”页面生成 `API Token`。

说明：

- 用户获取平台 token 的入口固定是 `http://easyclaw.bar/shuziren/user/`
- 不要把用户引导到 `http://easyclaw.bar/shuzirenapi`
- `API Token` 是本平台发放给 OpenClaw 使用的，不是禅镜的 `app_id / secret_key`

## OpenClaw 配置

推荐只配置 `CHANJING_PLATFORM_API_TOKEN`：

```json
{
  "skills": {
    "entries": {
      "chanjing-openclaw": {
        "enabled": true,
        "env": {
          "CHANJING_PLATFORM_API_TOKEN": "你的平台 API Token"
        }
      }
    }
  }
}
```

如需覆盖接口地址，也可以额外配置：

```json
{
  "skills": {
    "entries": {
      "chanjing-openclaw": {
        "enabled": true,
        "env": {
          "CHANJING_PLATFORM_API_TOKEN": "你的平台 API Token",
          "CHANJING_PLATFORM_BASE_URL": "http://easyclaw.bar/shuzirenapi"
        }
      }
    }
  }
}
```

说明：

- 现在默认接口地址已经内置为 `http://easyclaw.bar/shuzirenapi`
- 普通用户不需要手动填写 `CHANJING_PLATFORM_BASE_URL`
- 旧版 `API Key / API Secret` 仍然兼容，但优先使用 `API Token`

## 刷新 skill

配置完成后，重新打开一个 OpenClaw 会话，或者执行：

```bash
openclaw skills check
openclaw skills info chanjing-openclaw
```

如果提示未配置平台密钥，应该引导用户：

1. 打开 `http://easyclaw.bar/shuziren/user/`
2. 在平台里确认禅镜凭据已填写
3. 在“接口凭据”页面重新生成或复制 `API Token`

## 当前依赖

- `python` 或 `python3`
- 当前项目的平台服务已启动
- 当前平台账号下存在可用的 `API Token`
