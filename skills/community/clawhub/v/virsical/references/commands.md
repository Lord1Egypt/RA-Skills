# Virsical 命令参考

本文档包含所有可直接执行的 Python 命令片段，供 WorkBuddy 在执行具体操作时复制使用。
SKILL.md 中引用了对应的函数名和模块，此处为实际可执行命令。

> **语言提示**：命令中 Python `print` 输出的中文文本仅为技术调试信息，不应直接呈现给用户。
> 执行命令后，提取结构化数据，按用户语言重新组织呈现。

---

## 会话管理

### 配置检查

```bash
# 检查配置状态
python -c "from scripts.config import get_config; cfg = get_config(); print(f'Base URL: {cfg.base_url}')"
```

### 登录

```bash
# 智能预检（本地 + 服务端双重验证）
python -c "from scripts.config import get_config, reset_config; reset_config(); from scripts.auth_manager import TokenManager, check_token_before_login; import json; cfg = get_config(); tm = TokenManager(cfg); result = check_token_before_login(tm); print(json.dumps(result, ensure_ascii=False))"

# Agent 授权码登录：使用用户粘贴的授权码换取 token
python -c "from scripts.config import get_config, reset_config; reset_config(); from scripts.auth_manager import TokenManager, exchange_agent_code_for_token; import json; cfg = get_config(); tm = TokenManager(cfg); result = exchange_agent_code_for_token('<auth_code>', cfg, tm); print(json.dumps(result, ensure_ascii=False))"

# 本地登录（备用：桌面环境，自动打开浏览器）
python -c "from scripts.config import get_config; from scripts.auth_manager import TokenManager, local_login; import json; cfg = get_config(); tm = TokenManager(cfg); result = local_login(cfg, tm); print(json.dumps(result, ensure_ascii=False))"

```

### 一站式预检

```bash
# 预检（配置 + 登录 + license）
python -c "from scripts.session import ensure_ready; import json; result = ensure_ready('<scene>'); print(json.dumps(result, ensure_ascii=False, indent=2))"
```

### License 检查

```bash
# 检查特定场景 license
python -c "from scripts.license import check_license_for_scene; import json; result = check_license_for_scene('<scene>'); print(json.dumps(result, ensure_ascii=False, indent=2))"

# 列出所有 license
python -c "from scripts.license import fetch_licenses, format_license_list; result = fetch_licenses(); print(f'已获取许可列表：\n{format_license_list(result[\"licenses\"])}') if result['success'] else print(f'获取失败: {result[\"message\"]}')"
```

### 登出

```bash
python -c "from scripts.config import get_config; from scripts.auth_manager import TokenManager; cfg = get_config(); tm = TokenManager(cfg); tm.logout(); print('已登出')"
```

---

## 会议室

### 查询可用会议室

```bash
# 一站式查询（所有会议室）
python -c "from scripts.meeting import query_available_rooms; print(query_available_rooms())"

# 按容量筛选
python -c "from scripts.meeting import query_available_rooms; print(query_available_rooms(capacity_min=3, capacity_max=20))"

# 按时间段查询占用
python -c "from scripts.meeting import check_room_occupancy, format_room_list; result = check_room_occupancy(start_time='2026-06-02T14:00:00+08:00', end_time='2026-06-02T16:00:00+08:00', exclude_capacities='1;8'); print(format_room_list(result.get('data', [])))"
```

### 预订会议室

```bash
python -c "from scripts.meeting import book_meeting; import json; result = book_meeting(room_id='<会议室ID或名称>', title='<会议标题>', start_time='2026-06-02T14:00:00+08:00', end_time='2026-06-02T15:30:00+08:00', attendees=['<userId1>', '<userId2>'], description='<会议描述>'); print(json.dumps(result, ensure_ascii=False, indent=2))"
```

### 查询我的会议

```bash
python -c "from scripts.meeting import list_meetings; import json; result = list_meetings(); records = result.get('data', result.get('result', {})); records = records.get('records', []) if isinstance(records, dict) else records; [print(f\"- {m.get('name', '无标题')} | {m.get('roomNames', '')} | {m.get('startTime', '')} ~ {m.get('endTime', '')}\") for m in records]"
```

---

## 访客

```bash
# 查询所有访客
python -c "from scripts.visitor import list_visitors, format_visitor_list; result = list_visitors(); print(format_visitor_list(result.get('records', [])))"

# 按姓名搜索
python -c "from scripts.visitor import list_visitors, format_visitor_list; result = list_visitors(visitor_name='<访客姓名>'); print(format_visitor_list(result.get('records', [])))"
```

---

## 工单

### 获取工单参数

```bash
python -c "from scripts.requirement import get_requirement_params; import json; result = get_requirement_params(); print(json.dumps(result, ensure_ascii=False, indent=2)[:3000])"
```

### 创建工单

```bash
python -c "from scripts.requirement import create_requirement; import json; result = create_requirement(project_id=<项目ID>, content='<工单描述>', requirement_type_id=<类型ID>, priority=<优先级>); print(json.dumps(result, ensure_ascii=False, indent=2))"
```

---

## 时间转换

```bash
python -c "from datetime import datetime, timezone, timedelta; CST = timezone(timedelta(hours=8)); now = datetime.now(CST).strftime('%Y-%m-%dT%H:%M:%S+08:00'); ts = int(datetime.strptime('2026-06-02 14:00', '%Y-%m-%d %H:%M').replace(tzinfo=CST).timestamp() * 1000); print(f'ISO: {now}'); print(f'Timestamp: {ts}')"
```
