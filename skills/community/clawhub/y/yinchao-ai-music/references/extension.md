# 歌曲扩写已下线

根据[官方更新日志](https://platform.yinchaoyongxian.com/docs/quickstart/changelog)（2026-10-16 核对），平台已下线歌曲扩写，提交新扩写任务会返回 HTTP 400。

用户要求续写、延长歌曲或从指定时间继续时，说明当前不支持，不要上传音频或调用扩写接口。参考音频创作会生成新作品，不能替代原曲续写；只有用户另行选择创作新歌时才转入该流程。

脚本的旧 `extend` 命令仅返回下线提示，不读取凭据、不上传文件、不提交任务；DSH 工具不再提供该操作。已有任务 ID 仍可通过 `status --task-id "任务 ID"` 查询，按 [delivery.md](delivery.md) 处理结果，不重新提交。
