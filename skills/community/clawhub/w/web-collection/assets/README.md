# Web Collection Visual Assets

Place optional onboarding screenshots or GIFs in this folder. The online Feishu documents remain the source of truth; these files are for quick in-chat visual guidance.

Agents should resolve these images relative to the skill package, from the bundled `assets/` directory. Use the image/attachment mechanism supported by the current Agent host. If Markdown image rendering for packaged relative assets is supported, use:

```markdown
![进入个人中心](assets/bitable-step-00-personal-center.png)
```

If the host requires explicit attachments, attach the matching file from `assets/`. Do not hardcode machine-specific absolute paths in user-facing guidance. Do not reference these screenshots as plain text only when the user is asking for setup guidance.

For configuration guidance, images should be placed next to their matching text step, not collected at the bottom of the response. Bitable binding uses one image per substep. The connector image is the only exception: it is a single overview image for the whole third major step and appears once at the end of that major step.

Recommended filenames:

- `install-extension-connector.gif` or `install-extension-connector.png`
  - Browser extension and connector installation.
- `bitable-step-00-personal-center.png`
  - Open the browser extension, enter `个人中心`, and log in if needed.
- `bitable-step-01-template-copy.png`
  - Open the direct bitable template link, create a copy, and choose the proper copy settings.
- `bitable-step-02-auth-code.png`
  - Open `多维表格插件` -> `自定义插件`, enable the authorization code, and copy it.
- `bitable-step-03-config-save.png`
  - Fill in the bitable link and personal authorization code, test the connection, and save.
- `connector-step-01-status-token.png`
  - Overview image for the whole third major step: open `http://127.0.0.1:19820`, authorize login, verify all green statuses, and copy device ID plus Token. Use this screenshot exactly once at the end of connector guidance; do not repeat it under separate status verification and credential copying substeps.
- `view-results.gif` or `view-results.png`
  - Where to view exported bitable or CSV results.

Downloaded from the bitable configuration / connector verification guide:

- Guide URL: `https://vcn5grhrq8y0.feishu.cn/wiki/EAtJw2irFiDvMpkZXb4cBjYonNg`
- Direct bitable template URL: `https://vcn5grhrq8y0.feishu.cn/base/UKQsbVHpMac293s0cnFc1hq1nDd?table=tblTXM4lclXM6Jzr&view=vew8OdcKHw`
- `bitable-step-00-personal-center.png`
- `bitable-step-01-template-copy.png`
- `bitable-step-02-auth-code.png`
- `bitable-step-03-config-save.png`
- `connector-step-01-status-token.png`

Keep media small enough for fast Skill installation. Prefer short GIFs or compressed PNG/JPG screenshots. Put large videos in the Feishu knowledge base and link to them from `SKILL.md`.
