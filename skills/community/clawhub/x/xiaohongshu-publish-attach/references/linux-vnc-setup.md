# Linux + VNC (Xiaohongshu)

Same server setup as `zhihu-publish-attach` — see that skill's `linux-vnc-setup.md` or repo `readme.md`.

Additional for Xiaohongshu:

1. After Chrome starts, open https://creator.xiaohongshu.com and log in (创作者中心即可发长文).
2. If Chrome shows **Know your location**, click **Never allow** once (脚本会用 CDP 处理，但已弹出的条需先关掉).
3. 发布失败时脚本会自动尝试 **pyautogui** 真鼠标兜底（VNC 环境）；未安装则跳过：`pip3 install pyautogui`。禁用：`export XHS_DISABLE_SCREEN_CLICK=1`.
4. Accept creator terms if prompted; confirm you can open the publish page.
5. Test: `bash {baseDir}/scripts/xhs_publish.sh --check --check-creator --json`

主站 https://www.xiaohongshu.com **不需要**为 skill 单独登录。若 Zhihu 已配好，同一 Chrome profile 里登录 creator 即可。
