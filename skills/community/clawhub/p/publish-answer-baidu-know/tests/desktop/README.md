# 可选桌面 E2E（pytest）

本目录用于**匠厂桌面 + jiangchang_desktop_sdk** 的端到端冒烟，**不是** `python tests/run_tests.py` 默认路径的一部分。

## 依赖

- `pytest`
- `jiangchang_desktop_sdk`（由 `conftest.py` 按多级路径尝试加入 `sys.path`，见该文件说明）
- 匠厂桌面已安装或开发态可启动，且 `jiangchang://` 协议可用

## 为什么不默认跑

- 需要真实宿主环境，无法在纯 CI/无头环境稳定复现。
- `unittest` 的 `tests/run_tests.py` **只发现** `tests/` 根目录下 `test_*.py`，**不递归**本目录。
- 示例文件为 **`test_desktop_smoke.py.sample`**，避免被误收集。

## 如何启用

1. 将 `test_desktop_smoke.py.sample` **复制或重命名**为 `test_desktop_smoke.py`。
2. 按你的技能名称、路由关键词、期望输出修改 `ask` 与断言。
3. 运行：

```powershell
pytest tests/desktop/test_desktop_smoke.py -v -s
```

失败时，`conftest.py` 中的 `failure_snapshot_dir` fixture 会将现场目录指向 `tests/desktop/artifacts/`（需自行避免将大文件提交进仓库）。

## 与后端测试的关系

- **后端 / CLI / DB**：请使用仓库根目录下 `python tests/run_tests.py`（见 `tests/README.md`）。
- **桌面 E2E**：仅在本目录用 **pytest** 维护，二者互补、互不替代。

若仅需验证 **service 业务逻辑**、契约与 golden 回归，**不要**写 desktop E2E；desktop 只用于验证**宿主 UI、路由、`jiangchang://` 协议、真实用户交互链路**等与桌面宿主强相关的行为。

## 模板选择指南

| 场景 | 用哪个模板 |
|---|---|
| 纯问答 skill（不上传附件、不跑长流程） | `test_desktop_smoke.py.sample` |
| 需要上传附件 / RPA 长流程 / Agent 多轮工具调用 | `test_desktop_smoke_with_attachment.py.sample` |

录屏入口都用 `record_screencast.py.sample`，里面 `TEST_FILE_NAME` 常量切换测试文件。

## 已知 SDK 坑（来自 disburse-payroll-icbc 实战）

1. **`client.send_file()` 在 v2.0.17+ 抛 NotImplementedError**——附件场景必须用
   `jiangchang_desktop_sdk.e2e_helpers.drop_file_into_composer`（DataTransfer 拖拽）。
2. **`client.ask()` 内部 `user_msg_index<0` 死循环**——如果匠厂启动慢 / gateway 握手有
   延迟，导致 15s 内没抓到 user 节点，ask() 会锁死后续 900s 等待。建议长流程 / 附件场景
   绕开 ask()，用 `jiangchang_desktop_sdk.e2e_helpers` 里的 `send_prompt_via_composer`
   + `wait_for_user_message` + `wait_for_agent_complete` 自己控时。
3. **字幕关键词建议用 ASCII**——虽然 platform-kit 已修了 subprocess 编码乱码，
   保险起见字幕脚本里关键词用 `step: 1/` 这种 ASCII 锚而非中文短语。
4. **`client.bring_to_front()` 已升级**——v?? 起会 ctypes ShowWindow(SW_MAXIMIZE) +
   SetForegroundWindow，能真正铺满桌面。dev 模式下也能用（不依赖 jiangchang:// 协议）。

## 录屏新能力（platform-kit v??）

- `run_screencast(..., activate_window=True)` 自动激活+最大化匠厂窗口
- `run_screencast(..., monitor_index=1)` 多显示器场景显式录主屏
- 字幕脚本支持三元组 `(keyword, text, duration)` 给个别字幕指定独立时长，
  覆盖长等待场景中间没日志输出的"字幕真空"
