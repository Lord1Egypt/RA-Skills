---
name: zhiyierxing-auto-phone
emoji: "🤖"
metadata:
  openclaw:
    requires:
      env:
        - MODEL_BASE_URL
        - MODEL_NAME
        - MODEL_API_KEY
      tools:
        - git
        - python3
        - adb
        - hdc
        - bash
    recommended_model: "Zhipu AutoGLM-Phone"
    recommended_model_doc: "https://docs.bigmodel.cn/cn/guide/models/vlm/autoglm-phone"
description: >-
     Product-grade deployment and operation skill for Zhipu AutoGLM-Phone / Open-AutoGLM.Use when the user wants a complete, runnable local setup: clone the GitHub repo onto the computer, prepare Android/HarmonyOS/iPhone devices, install ADB Keyboard, enable developer options and USB debugging, configure model endpoints, start the agent, verify deployment, and troubleshoot failures with exact user instructions.
---

# zhiyierxing_auto_phone

Build and run a real phone-agent deployment.

## Recommended model
Prefer Zhipu's AutoGLM-Phone model for this workflow.

Official docs:
https://docs.bigmodel.cn/cn/guide/models/vlm/autoglm-phone

## Golden rule
Do not stop at explanation. Move the setup forward, or give the exact next user action when a manual step is required.

The user should be able to speak in plain natural language.
Do not require the user to understand deployment steps, repo layout, venv usage, or model flags before using this skill.
Interpret the user's request as the target phone task, then complete the prerequisite setup chain automatically when needed.

Default behavior:
- first try the end-to-end workflow
- automatically reuse any existing repo, `.venv`, installed dependencies, device connection, and model env vars
- only ask the user to do something after a real runtime blocker is observed
- do not front-load setup instructions "just in case"
- do not ask the user to install ADB Keyboard, enable debugging, or configure env vars unless the workflow actually proves that those are the blockers

## Environment variables
This skill expects the following variables when applicable:
- `MODEL_BASE_URL`: OpenAI-compatible model endpoint, e.g. `https://open.bigmodel.cn/api/paas/v4` or `http://localhost:8000/v1`
- `MODEL_NAME`: model name to call, e.g. `autoglm-phone`
- `MODEL_API_KEY`: API key for BigModel or provider endpoints that require auth

Optional but useful:
- `PHONE_DEVICE_TYPE`: `android`, `harmonyos`, or `iphone`
- `PHONE_CONNECTION_MODE`: `usb` or `wifi`
- `PHONE_DEVICE_ID`: explicit adb/hdc device id
- `OPEN_AUTOGLM_REPO_DIR`: local repo path

For Android device reuse:
- if the phone was previously USB-authorized and later shares the same LAN with the computer, prefer reconnecting over ADB Wi‑Fi automatically
- save reachable device identifiers and remembered Wi‑Fi targets so future runs can reconnect and reuse the same phone when `adb` can still see it

## Scope
This skill covers:
- understanding natural-language phone task requests from the user
- deciding whether deployment already exists or must be completed first
- downloading or updating the Open-AutoGLM repo on the user's computer
- host prerequisite checks
- macOS, Linux, and Windows host compatibility guidance
- Android / HarmonyOS / iPhone setup paths
- ADB Keyboard setup for Android
- model endpoint configuration
- startup and smoke-test execution
- actual task execution after setup is ready
- deployment verification
- troubleshooting with explicit user instructions

## How users will ask for this
Users may not say "deploy" or mention this skill name at all.
They may say things like:
- 帮我用手机打开抖音，找到某个视频，然后按我的要求评论
- 用手机打开小红书，搜索某个关键词，看看热门内容
- 帮我在手机上打开美团，找附近评分高的火锅店
- 用手机打开淘宝搜索无线耳机，对比前几个结果

Treat requests like these as end-to-end task requests, not as documentation questions.
The skill should infer that it may need to deploy, configure, verify, and then execute.

## Inputs you may need
Ask only for what is missing and only when it truly blocks progress:
- device type: `android`, `harmonyos`, or `iphone`
- connection mode: `usb` or `wifi`
- model mode: `bigmodel`, `third-party-openai-compatible`, or `self-hosted`
- repository location if the user wants a custom folder
- `base-url`, `model`, and `apikey` if the model endpoint is not already known
- clarification of the phone task only if the requested action is ambiguous or unsafe

## Success criteria
Treat the job as complete only when all of these are true:
- repo exists locally
- a suitable Python 3.10+ runtime is available and selected
- `.venv` exists in the repo root and is used for Python execution
- dependencies are installed inside `.venv` and critical runtime imports succeed
- device is visible to adb/hdc or iPhone setup is completed
- text input works on Android
- model endpoint passes verification
- at least one smoke-test task runs from `.venv`
- user knows what to do when a failure happens

## Execution policy
When the user gives a phone task in natural language, execute in this order:

### 1. Understand the target task
Extract the real user goal, for example:
- target app
- search term
- navigation goal
- expected action such as open, search, comment, compare, collect, or inspect

Do not dump setup instructions first unless setup is actually required.

### 2. Prefer a direct end-to-end run first
Default to running the full workflow first, not to asking setup questions first.

Use:
- `scripts/ensure_and_run_task.py` as the default path
- `scripts/run_phone_task.py` only when you already know the environment is ready and want a shorter path

Assume the environment may already be usable. Let the workflow prove what is missing.

### 3. Reuse existing environment aggressively
Before telling the user to install or configure anything, prefer to let the workflow reuse:
- existing local repo
- existing repo-local `.venv`
- existing installed dependencies
- existing connected device
- existing model environment variables
- remembered Android device identity and remembered ADB Wi‑Fi target

Do not ask the user to reinstall or reconfigure something that may already be present.

For Android:
- if a previously authorized USB device is connected, try enabling TCP/IP and connecting over Wi‑Fi automatically
- if a remembered Wi‑Fi target exists and the computer and phone are on the same LAN, try `adb connect` automatically before asking the user to reconnect anything
- if a remembered device is currently visible in `adb devices`, prefer reusing it automatically
- when executing the real task, pass the preferred remembered device into the runner explicitly so multi-device environments do not accidentally target the wrong phone

### 4. Auto-fix local blockers when possible
For host-side tools and environments that the agent can safely install or repair on the local machine, do that proactively instead of pushing the work to the user.

Examples:
- install `adb` / Android platform-tools when missing and locally installable
- detect whether Python meets the minimum version required by the project
- auto-install or auto-select Python 3.10+ when the host can self-service it
- clone or update the Open-AutoGLM repo
- create or repair the repo-local `.venv`
- install Python dependencies into `.venv`
- choose the correct install path for the current host OS instead of assuming macOS-only tooling

Only stop and ask the user when the blocker is not locally self-serviceable or requires user action on the phone or in an external service.

### 5. Ask the user only after a real blocker is observed
If the workflow fails or reports missing pieces, then explain:
- what failed
- what was already checked automatically
- the likely cause
- the exact next user action

Examples of appropriate user prompts after a real blocker:
- `adb devices` is empty → ask the user to reconnect the cable / accept authorization / enable USB debugging
- model env vars are actually missing → ask the user to set `MODEL_BASE_URL`, `MODEL_NAME`, `MODEL_API_KEY`
- Android text input actually fails or readiness check explicitly shows missing IME → ask the user to install or enable ADB Keyboard

Do not give those instructions before the workflow has evidence they are needed.

### 6. Verify before claiming success
Use `scripts/verify_open_autoglm.py` and any upstream verification script when appropriate.

Use a neutral smoke-test prompt for verification.
Do not use a realistic downstream app task like “打开美团搜索附近的火锅店” as the default verification prompt, because it pollutes logs and makes it look like the real user task was replaced.
Prefer a format-only verification prompt such as a minimal `Wait` action.

If verification fails, explain:
- what failed
- likely cause
- exact next step

If the only failure is a transient repo update/network issue but the local repo, Python runtime, `.venv`, dependencies, and model path are already usable, continue with the local repo instead of blocking unnecessarily.

### 7. Execute the real task, then decide whether takeover is needed
After deployment, env, and verification are ready, run the actual natural-language task the user asked for.

Examples:
- 打开抖音找到某个视频并按要求评论
- 打开小红书搜索关键词并浏览结果
- 打开美团查找附近高分商家

Keep moving the workflow forward until the task is completed or a real blocker is reached.

## Host compatibility
This skill must support Windows hosts in addition to macOS and Linux.

Rules:
- do not assume Homebrew exists
- do not assume `bash` is the only shell available
- do not assume `.venv/bin/activate` is the only activation path
- do not assume the system default `python3` is new enough
- when giving commands, prefer OS-appropriate variants
- when automating install steps, detect the host OS first and choose the correct package manager or manual instructions
- prefer Python 3.10+ and auto-install or auto-select it when the host can self-service that
- transient GitHub connectivity failures should not block task execution if the local repo already contains the needed files

Examples:
- macOS: Homebrew may be used for `adb` and a newer Python
- Linux: use the distro package manager when appropriate
- Windows: prefer `winget` when available for Android platform tools and Python, otherwise provide exact manual steps

## ADB Keyboard rules
Use ADB Keyboard only on Android.

If typing fails, tell the user to:
1. reinstall or re-enable ADB Keyboard
2. set it as the current input method
3. retry the task

Useful commands:
```bash
adb shell ime enable com.android.adbkeyboard/.AdbIME
adb shell ime set com.android.adbkeyboard/.AdbIME
adb shell ime list -a
adb shell ime reset
```

## Troubleshooting behavior
When something breaks, respond with:
- what failed
- the likely cause
- the exact next step the user should do

Prefer explicit status tags in script output when available:
- `[auto-fixed]`: a local blocker was repaired automatically
- `[phone-action-needed]`: the user must do something on the phone
- `[decision-needed]`: the user must provide missing intent or choose among unresolved options
- `[takeover-paused]`: execution paused at a real takeover boundary
- `[config-needed]`: model or environment configuration is missing
- `[runtime-failed]`: execution failed and needs investigation
- `[safe-to-retry]`: the workflow can be rerun after the named blocker is fixed
- `[diagnosis] ...`: post-run classification of the most likely blocker or success state

Do not answer with generic encouragement alone.

### Common failures
- `adb devices` empty: cable/authorization/debugging issue
- typing broken: ADB Keyboard not enabled, or upstream IME detection is blocked by vendor restrictions
- black screen: sensitive page, takeover needed
- interactive EOF: use direct task mode or a TTY
- endpoint failure: URL/model/key mismatch or server down

ADB Keyboard is not a front-loaded blocker by default.
Treat it as a follow-up fix only when text input actually fails, or when the runtime explicitly proves IME is the blocker.

## Manual takeover
Always request user takeover only for:
- login
- captcha
- payment
- biometrics
- explicit platform trust/security prompts that cannot be safely automated

Default automation rule:
- if the user asked for a phone task, complete the whole task end-to-end when technically possible
- do not stop at the last step just to ask the user to tap submit / send / publish / comment
- do not introduce an extra confirmation checkpoint unless the user explicitly asked for one
- the requested final action is part of the task and should be executed automatically when the path is clear

For public comments, posts, and messages:
- if the user clearly asked for that external action, perform it as part of the automation
- only pause if a real takeover condition appears, such as login, captcha, payment, biometrics, or a platform security interstitial that requires the human
- do not convert normal final-step actions into manual tasks for the user

## Script entry points
Useful helper scripts in this skill:
- `scripts/check_skill_ready.py`: preferred cross-platform readiness check for repo, `.venv`, model env vars, and device path
- `scripts/check_skill_ready.sh`: shell-oriented readiness check for macOS/Linux-style environments
- `scripts/install_host_tools.py`: preferred cross-platform host-tool installer for self-serviceable local dependencies such as adb when supported
- `scripts/install_host_tools.sh`: shell-oriented host-tool installer for macOS/Linux-style environments
- `scripts/clone_or_update_open_autoglm.py`: preferred cross-platform repo sync helper
- `scripts/clone_or_update_open_autoglm.sh`: shell-oriented repo sync helper
- `scripts/check_android_ready.py`: preferred cross-platform Android readiness check
- `scripts/check_android_ready.sh`: shell-oriented Android readiness check
- `scripts/prepare_android_connection.py`: auto-prepare Android connectivity by reusing remembered Wi‑Fi targets, enabling TCP/IP on authorized USB devices, and saving device memory for future runs
- `scripts/device_memory.py`: device-memory helper for persisting remembered Android identifiers and Wi‑Fi targets
- `scripts/check_harmonyos_ready.py`: preferred cross-platform HarmonyOS readiness check
- `scripts/check_harmonyos_ready.sh`: shell-oriented HarmonyOS readiness check
- `scripts/check_iphone_ready.py`: preferred cross-platform iPhone reminder/check helper
- `scripts/check_iphone_ready.sh`: shell-oriented iPhone reminder/check helper
- `scripts/deploy_open_autoglm.py`: preferred cross-platform deployment flow for repo sync, `.venv`, and dependency installation
- `scripts/deploy_open_autoglm.sh`: shell-oriented deployment flow for macOS/Linux-style environments
- `scripts/verify_open_autoglm.py`: verify the model endpoint
- `scripts/run_phone_task.py`: preferred cross-platform real-task runner from `.venv`
- `scripts/run_phone_task.sh`: shell-oriented task runner from `.venv`
- `scripts/ensure_and_run_task.py`: preferred cross-platform full workflow for natural-language tasks, including readiness check, deploy/repair, verification, and execution
- `scripts/ensure_and_run_task.sh`: shell-oriented full workflow for macOS/Linux-style environments

## References
Read these when needed:
- `references/deployment-flow.md`
- `references/adb-keyboard.md`
- `references/troubleshooting.md`
