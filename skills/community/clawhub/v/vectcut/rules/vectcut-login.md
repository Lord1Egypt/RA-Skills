---
name: vectcut-login
description: "用于获取并校验 VECTCUT_API_KEY 的登录前置技能。只要用户要调用任意 VectCut 开放平台能力，或出现 VECTCUT_API_KEY 缺失、为空、疑似失效、401/403 鉴权失败，就必须优先使用本技能。默认引导到网页登录并让用户从头像处复制 API Key；拿到 token 后自动输出 export 命令并完成有效性校验。"
---

# VectCut Login Skill

用于在调用 VectCut API 前完成登录态准备，避免因缺少 `VECTCUT_API_KEY` 导致接口调用失败。

## 适用场景

- 用户准备调用任意 VectCut 开放平台接口
- 已出现 `VECTCUT_API_KEY` 缺失、为空或鉴权失败
- 用户明确提到 OAuth2 登录、jwt_token、登录取 token

## 前置条件

- Python 3
- 可访问 `https://www.vectcut.com/auth` 与 `https://open.vectcut.com`

## 环境变量检查规范

- 从环境变量读取 `VECTCUT_API_KEY`而不是读取本地配置文件

## 执行目标

- 打开网页登录页并引导用户获取 `VECTCUT_API_KEY`
- 输出可直接执行的环境变量设置命令
- 调用 `verify_token()` 完成有效性校验
- 校验通过后再继续执行其他 VectCut 技能

## 执行方式

```bash
python <skill-path>/scripts/vectcut_login.py
```

默认使用网页登录模式：

```bash
python <skill-path>/scripts/vectcut_login.py --mode web
```

如果已拿到 token，可直接传入并输出一条可执行设置命令：

```bash
python <skill-path>/scripts/vectcut_login.py --jwt-token "your_jwt_token"
```

## 标准流程

1. 运行脚本，默认进入网页登录引导。
2. 打开 `https://www.vectcut.com/auth`，登录后点击头像复制 `VECTCUT_API_KEY`。
3. 将 token 作为 `--jwt-token` 传给脚本。
4. 脚本输出 `export VECTCUT_API_KEY=...` 命令。
5. 脚本内部调用 `verify_token()` 发起鉴权校验。
6. 校验通过后再调用其他 VectCut 技能。

## 输出

- 成功时输出一条可执行命令：`export VECTCUT_API_KEY=...`
- 校验失败时返回非 0 退出码并提示重试

## 结果判定

- 成功：`VECTCUT_API_KEY` 非空且通过 `verify_token()`校验，可继续调用其他 VectCut 技能
- 失败：token 为空或校验返回 4xx/网络失败，应提示用户重新获取并重试
