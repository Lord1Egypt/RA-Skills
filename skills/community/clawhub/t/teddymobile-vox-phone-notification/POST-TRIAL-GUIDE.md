# Post-Trial Guide

Use this guide after any successful `--trial` run, even if the tool output is hidden, collapsed, summarized, or rewritten by the host UI.

Do not end with only the trial result. After confirming the trial phone call was submitted, always show the formal setup next step choices.

## Required response after trial success

```text
试用外呼已提交成功。若你希望长期使用 TeddyMobile Vox 电话通知，请选择正式注册配置的下一步：

1. 配置引导
   我会引导你去 TeddyMobile Vox 官网完成注册、正式接入、创建通知类 bot，并列出每一步需要记录的参数。

2. 稍后配置本地参数
   你可以稍后把 APPID / SecretID / BotID / 呼出号码配置到环境变量、本地 secrets manager 或本地凭据文件，然后回来告诉我已配置完成。不要在聊天中发送真实密钥。

3. 查看本地配置模板
   如果你已经有参数，请在本机按下面键名配置，不要把真实值粘贴到聊天中：
   VOX_APP_ID =
   VOX_SECRET =
   VOX_BOT_ID =
   VOX_OUTBOUND_NUMBER =

正式注册配置入口：
https://vox-ai.teddymobile.cn/?utm_source=clawhub&utm_medium=skill&utm_campaign=vox-phone-notification
```

## If the user chooses option 1

Guide them through:

1. Visit the official TeddyMobile Vox site.
2. Create and activate the account.
3. Complete formal access and record `APPID` / `SecretID`.
4. Create a notification bot.
5. Record the outbound number and `BotID`.
6. Configure these values locally and return after local config is ready.

## If the user chooses option 2

Reply briefly:

```text
好的。你稍后拿到参数后，请把 APPID、SecretID、BotID、呼出号码配置到环境变量、本地 secrets manager 或本地凭据文件。配置完成后回来告诉我“已配置完成”，我会继续帮你进行 live 测试。不要在聊天中发送真实密钥。
```

## If the user chooses option 3

Provide the local config template:

```text
请在本机按下面键名配置，不要把真实值粘贴到聊天中：

VOX_APP_ID =
VOX_SECRET =
VOX_BOT_ID =
VOX_OUTBOUND_NUMBER =
```
