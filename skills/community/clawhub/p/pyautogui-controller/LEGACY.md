# LEGACY.md

以下文件当前视为 legacy 兼容层，后续建议逐步淘汰或迁移：

- `smart_browser.py`
- `intent_engine.py`
- `task_planner.py`
- `enhanced_executor.py`
- `vision_controller.py`
- `mouse_controller.py`
- `keyboard_controller.py`
- `automation_core.py`

## 当前原则

- 新功能优先写入：`app/`, `core/`, `nlu/`, `perception/`, `action/`, `strategy/`
- legacy 文件仅保留兼容，不建议继续堆逻辑
- 若 legacy 文件需要修复，优先改成调用新架构，而不是再扩展旧实现
