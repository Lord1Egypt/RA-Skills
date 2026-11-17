# 脚本目录与维护说明

### 获取项目列表
```bash
python scripts/list_projects.py [--credentials PATH] [--base-url URL]
```
列出 OA 系统所有项目；**首次使用时必须让用户从中选择**，不要自行指定。

## 当前脚本

- `scripts/personal_settings.py`：账号/地址绑定的已确认设置、安全存储及严格字段校验
- `scripts/configure_personal_settings.py`：当前账号只读验证中文标签/代码，默认预览；明确 `--confirm-save` 后保存个人设置
- `scripts/oa_options.py`：只读项目与系统业务字典查询，boToPmStatus 由选中项目派生
- `scripts/runtime_bootstrap.py`：运行时解释器自检/自动切换
- `scripts/sn_oa_login.py`：登录并输出 token；支持 `--fetch-only` / `--submit` 两阶段（agent 多模态优先）与默认 ddddocr 闭环
- `scripts/query_fee_requests.py`：查询报销申请状态，可选展开当前审批节点/审批人
- `scripts/list_projects.py`：查询项目列表（支持 `--json`）
- `scripts/submission_guard.py`：公共提交保护（认证绑定、同日核对、一次写入、读回、私有持久日志与 POSIX 日锁）；只读 live 验证工具为 `tests/live_duplicate_readonly.py`
- `scripts/submit_time_entry.py`：普通工作中文/代码 live 解析，受保护提交或 `--preview` 只读预览；草稿仅支持预览，休假不可提交
- `scripts/query_time_entry.py`：查询某天工时列表
- `scripts/query_time_ranges.py`：多区间只读查询；复用认证，重叠日期只查询一次，ID 去重、Decimal 汇总、逐日描述和完整性报告；`--raw-output` 可选私有原始证据。常规批量查询优先此入口，不另写临时驱动。
- `scripts/get_time_entry_details.py`：按工时 ID 查询详情
- `scripts/update_time_entry.py`：修改只读预览、明确授权的撤回重提；保留旧描述更新；删除/恢复因无可靠服务端恢复契约暂禁，CLI 在读取凭据前拒绝，公共 API 在任何网络前拒绝；`scripts/deletion_guard.py` 仅保留离线 fake 流程，不接入生产入口。
- `scripts/amendment_guard.py`：已有记录的状态流转、不可变字段、同日锁和持久修改意图保护
- `scripts/oa_utils.py`：公共能力（登录、认证会话、状态映射、工时管理、报销列表/详情/审批进度查询、`fetch_captcha` / `submit_login` / `login_with_code` / `OAAuth` 会话缓存与自动续期）

## 增强说明

- 公共认证头逻辑已统一收口到 `oa_utils.py`，避免不同脚本各写一套导致认证不一致
- 项目列表脚本新增 `--json`，方便调试或二次处理
- 提交、查询、详情、修改四个工时脚本都走同一套登录与认证逻辑，减少后续维护成本
- 所有入口脚本已接入 `runtime_bootstrap.py`：若当前解释器缺少依赖，会自动切换到可用解释器再执行
- 解释器优先级支持环境变量 `SN_WORK_RECORD_PYTHON` 覆盖，也会自动探测常见虚拟环境名称
- 当前 ClawHub 1.4.3 发布包未包含 `sn-work-record` launcher；在 Hermes 中直接使用 `scripts/` 下的入口
- 目录说明已与实际文件对齐：提交/查询/详情/修改都已提供脚本，避免再次误判
