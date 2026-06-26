# 腾讯云 ASR 自检说明

## 何时阅读本文档

仅在以下情况阅读：

- 用户刚提供了新的腾讯云凭证
- 用户要求“帮我验证配置是否可用”
- Agent 需要把自检结果解释给用户

## 默认命令

```bash
python3 <SKILL_DIR>/scripts/self_check.py
```

默认样例音频会优先读取：

1. `assets/16k.wav`
2. `assets/self-check/16k.wav`
3. `16k.wav`

如需显式指定：

```bash
python3 <SKILL_DIR>/scripts/self_check.py --sample "/absolute/path/to/16k.wav"
```

## 自检内容

脚本会自动完成这些动作：

1. 检查并确保 `ffmpeg` / `ffprobe` 可用
2. 用样例音频规范化出一份标准 `16kHz` 单声道 WAV
3. 直接用同一份样例分别调用：
   - `sentence_recognize.py`
   - `flash_recognize.py`
   - `file_recognize.py rec`
4. 输出结构化 JSON，并附带一段可直接发给用户的 `report_markdown`

## 结果解释

- `status = "success"`
  - 三个模式都通过
- `status = "all_failed"`
  - 三个模式都失败
  - 优先提示用户检查密钥、服务开通、资源包/计费状态
- `status = "flash_only_failed"`
  - 一句话识别与录音文件识别通过，只有极速版失败
  - 向用户说明：这通常是极速版单独受限，常见于国际站账号，或国内站账号在海外访问时受限
  - 同时提醒检查 `AppId` 和极速版开通状态
- `status = "flash_not_checked"`
  - 基础模式通过，但极速版没有完成验证
  - 最常见原因是缺少 `AppId`

## 对用户的返回口径

成功时尽量简短：

> `✅ 3/3 自检通过，可以继续使用。`

失败时使用脚本内置的 `report_markdown`，保留：

- `✅ / ❌ / ⚠️` 状态符号
- 每个模式的结果
- 汇总结论

如果三个模式都失败，补一句：

> `如果确认密钥和服务配置无误，建议把报错信息整理后直接咨询腾讯云官网客服。`
