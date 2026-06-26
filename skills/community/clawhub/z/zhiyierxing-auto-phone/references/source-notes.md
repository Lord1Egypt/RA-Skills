# Source notes

## Zhipu AutoGLM-Phone docs
- URL: https://docs.bigmodel.cn/cn/guide/models/vlm/autoglm-phone
- Key points gathered:
  - AutoGLM-Phone is a multimodal AI phone assistant framework that uses ADB to control Android devices.
  - Recommended scenarios include shopping, food delivery, travel, media playback, and real-estate search.
  - Supported actions include Launch, Tap, Type, Swipe, Back, Home, Long Press, Double Tap, Wait, and Take_over.
  - Environment prep: Python 3.10, ADB, Android 7.0+, Developer Mode, USB debugging, ADB Keyboard.
  - Install ADB Keyboard APK from senzhk/ADBKeyBoard and enable it in input method settings.
  - Upstream examples use `pip install -r requirements.txt` and `pip install -e .`, but this skill should do that inside a repo-local `.venv`.
  - Example run for this skill: `source .venv/bin/activate && python main.py --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "..." "打开美团搜索附近的火锅店"`

## Open-AutoGLM repo
- Repo: https://github.com/zai-org/Open-AutoGLM
- Key points gathered:
  - Repo contains `main.py`, `phone_agent/`, `scripts/`, and iOS setup docs.
  - Supports BigModel, ModelScope, and self-hosted model endpoints.
  - Provides deployment check script `scripts/check_deployment_cn.py`.
  - Lists supported apps with `python main.py --list-apps`.
  - Self-hosted vLLM/SGLang deployment examples expose OpenAI-compatible `/v1` endpoints.

## ADBKeyBoard repo
- Repo: https://github.com/senzhk/ADBKeyBoard
- Key points gathered:
  - Android virtual keyboard for ADB text input.
  - APK can be installed from repo or release page.
  - Enable via `adb shell ime enable com.android.adbkeyboard/.AdbIME`.
