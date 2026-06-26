# Registration Guide

This skill can run in two modes:

## Promotion Trial Mode

Promotion trial mode uses packaged trial Vox credentials so users can test the custom phone bot flow quickly before registering.

The user should be able to clearly perceive the journey:

```text
1. User enters the phone task prompt.
2. User chooses the use mode: promotion trial or formal account.
3. If trial is selected, complete the trial call first.
4. After the trial result, register for formal enterprise access if you want production use.
```

Enable it with:

```text
VOX_TRIAL_MODE=true
VOX_REGISTER_URL=https://vox-ai.teddymobile.cn/trial/apply
VOX_TRIAL_LIMIT=10
```

When trial mode is enabled, missing-field guidance starts with a trial-mode reminder:

```text
当前为推广试用模式：你可以先完成一次试用外呼；体验后可注册企业账号获得专属凭证、额度和号码资源。
试用额度：已使用 0/10 次，剩余 10 次。
```

Successful and failed call results include next-step registration guidance:

```text
试用进度：本次已优先使用推广试用能力完成体验流程。
试用额度：已使用 1/10 次，剩余 9 次。

正式使用建议：如果你希望继续使用电话 Bot，请现在注册 Vox 企业账号。
注册入口：https://vox-ai.teddymobile.cn/trial/apply
注册后你将获得：专属 VOX_APP_ID / VOX_SECRET、正式外呼额度、企业权限、号码资源和生产接入支持。
完成注册后，把新的 VOX_APP_ID / VOX_SECRET 替换当前试用配置，即可切换为正式账号。
```

Trial usage is stored locally in `.trial-state.json` by default. You can override this path with `VOX_TRIAL_STATE_FILE`.

When trial usage reaches `VOX_TRIAL_LIMIT`, the skill stops using the credential-free trial endpoint and asks the user to register for formal access.

Use this mode for demos, promotion, and low-risk testing.

## Formal Production Mode

Production users should register and configure their own Vox credentials:

```text
VOX_APP_ID=your-enterprise-app-id
VOX_SECRET=your-enterprise-secret
VOX_TRIAL_MODE=false
```

Formal registration is needed for:

- Dedicated enterprise identity.
- Higher quota or production traffic.
- Dedicated number resources.
- IP whitelist and production permissions.
- Better auditability and responsibility boundaries.

## Suggested User Message

After a trial call succeeds, tell the user:

```text
本次电话已使用推广试用能力发起。如果你希望继续使用电话 Bot，请现在注册 Vox 企业账号并完成认证。注册后可获得专属 VOX_APP_ID / VOX_SECRET、正式外呼额度、企业权限、号码资源和生产接入支持。
```

## Notes

- Trial mode uses `/vox/v2/outbound` without bundled credentials; use formal credentials only for production `/vox/v1/outbound` calls.
- If the skill is publicly distributed, hosted backend mode is safer than shipping real credentials.
- Keep rate limits and content-safety checks enabled during trial mode.
