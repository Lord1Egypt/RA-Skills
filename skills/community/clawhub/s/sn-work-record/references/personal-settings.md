# 多账号个人设置与 OA 选项

## 首次选择和确认

1. 用 `terminal` 运行 `python scripts/oa_options.py --credentials <encrypted-credentials>`，通过当前账号只读查询项目及系统字典；返回代码和中文标签，不猜测编号。
2. 展示项目名称、填报类型、项目阶段、工作类型，请用户选择并确认实际时长。禁止代选岗位、项目或 8h。`boToPmStatus` 不是独立选项，也不是全系统固定常数：由选择的项目元数据派生（1 项目、0 商机）。项目名称也按此属性选择 `projectPmName` 或 `projectBoName`。商机不允许阶段代码 1（研发/交付）。
3. 将用户精确中文标签或代码传给下面命令；每次重新用当前凭据查询。未知标签、重复/歧义标签、缺少字典、项目列表不完整、无效元数据、无效时长均拒绝。系统字典不按岗位代选；项目列表限当前账号可见范围。不同账号/系统不得复用选项快照。

```text
python scripts/configure_personal_settings.py --credentials <encrypted-credentials> --project "<selected-project-name>" --man-hour <confirmed-hours> --fill-type "<selected-label>" --project-phase "<selected-label>" --work-type "<selected-label>"
```

默认只读预览，输出可供本次提交入口使用的七项已解析字段，不写设置、不提交。只有用户明确同意以后使用这些个人默认，才增加 `--confirm-save --settings <private-settings-path>`。配置入口现在会登录/复用认证并只读查询，不再是纯离线写文件；不存在 `--bo-to-pm-status` 用户选项，也不再接受旧的 `--project-id/--project-name` 绕过映射的配置接口。

保存仍使用账号 SHA-256 指纹与完整 base_url 绑定，原子写入 0600，默认 `~/.config/sn-work-record/personal-settings.json`，不存密码、token、密钥。不修改旧凭据或自动迁移项目。地址仅去尾部 `/`。绑定不符、损坏 JSON、未确认设置、宽权限均拒绝。

## 提交边界

`submit_time_entry.py` 的 `--project`、`--fill-type`、`--project-phase`、`--work-type` 现在接受精确中文名称/标签或当前账号实时可见的代码。标签不做模糊匹配，代码不去空格、不补零、不转换全角字符；未知、歧义、格式错误、字典缺失或项目列表不完整均停止，查询失败绝不进入写请求。

```text
python scripts/submit_time_entry.py <confirmed-date> --project "<selected-project-name>" --fill-type "工作" --project-phase "<selected-phase-label>" --work-type "<selected-work-label>" --man-hour <confirmed-hours> --job-desc "<confirmed-description>" --preview --json
```

`--preview` 与真实提交共用全部提交前解析及校验，分支仅发生在解析成功之后：预览只输出最终名称、日期、时长、描述和动作，不调用 `saveOrUpdate`，也不保存个人设置。默认隐藏内部代码；明确需要时加 `--include-codes`。`--preview --save-draft` 也不会创建真实草稿。只有确认真实日期/工作/项目/时长并明确授权后，才去掉 `--preview` 真实提交；测试预览的时长与描述不能充作真实工作事实。

已确认的账号/地址绑定默认设置仍可使用，但每次必须将其代码重新与 live 选项匹配；旧项目名称及 boToPmStatus 不进入请求，始终从当前选中项目重新派生。切换项目后仍校验继承阶段，商机不能继承研发/交付阶段；用 `--project-phase` 显式覆盖为适用阶段，绝不自动猜选。单次中文/代码覆盖不修改默认设置。未配置时必须显式提供项目、类型、阶段、工作类型与正有限时长，缺少字段或非法时长在认证前失败，没有 8h 默认。日期严格 YYYY-MM-DD，描述非空。

兼容旧 `--project-id`（与 `--project` 互斥），仍需 live 校验；`--project-name` 和 `--bo-to-pm-status` 仅是可选一致性断言，不能覆盖真实映射，也不再必填。默认文件损坏、绑定不符或权限不安全仍拒绝；旧凭据项目不迁移、不用于提交。底层七项必填安全门保留。修改入口未扩大为中文选择入口。

**提交/草稿/提交预览当前仅支持普通工作（填报类型 1）。事假、公休假等非工作类型均明确拒绝。** 前端对事假不要求项目/阶段/工作类型，而底层七项安全门仍要求这些字段；休假条件必填尚未实现，不能伪造项目满足安全门。

## 重复提交及真实写入边界

- 公共 `oa_utils.submit_time_entry()` 已加入同日完整核对、OA origin/账号/token 绑定、本地账号日期锁、POST 前持久意图与写后只读核实。完全相同且有效已提交记录返回 `skipped-existing`；其他同日记录拒绝，绝不静默覆盖。查询失败/不完整不写入。
- 写操作保持 `allow_relogin=False`；网络超时或不确定响应后最多三次只读核对，不重发写请求。HTTP 成功不等于已核实成功；字段/状态不一致、历史意图无法确认均拒绝再写。日志与锁保护只覆盖同一机器/用户/保护目录，不是服务端跨主机 exactly-once。
- 草稿真实写入暂时 fail-closed；`--preview --save-draft` 保持只读。直接导入公共 API 同样受保护，但仍不自行发现业务字典，交互提交不可绕过统一 CLI 的 live 选项校验。
- 完整规则、持久日志边界及只读重复验证工具见 [`submission-idempotency.md`](submission-idempotency.md)。真实新写入仅可在事实确认与授权后执行，不能把本次离线 fake 测试当 live 写入证据。
- 所有 live 证据仅保留脱敏输出与请求路径，不保存账号、主机地址、token、项目 ID 或真实项目名。

## 可复核来源

2026-10-10 从当前 OA 静态资源 `app.v1.0.3.40bbeea7.js` 的模块 `066e` 发现 `/sn/system/dict/data/typeList` POST（原始 JSON 字典名称数组）；模块 `f155` 映射 `dictValue`/`dictLabel`。`chunk-08b624b1.v1.0.3.40bbeea7.js` 的工时表单 `getDict` 使用 `sn_fill_type`、`sn_fee_request_project_type`、`sn_job_type`；`remoteMethod` 排除商机阶段 1；`bussinessSubmit` 和 `changeProject` 从选中项目复制 `boToPmStatus`。前端默认填报代码 1 不被技能作为业务默认采用。

脱敏 API 标签/代码及资源 SHA-256 见 `oa-options-evidence.json`；该文件是一次取证快照，不作为运行时字典。取证资源在 `/root/.hermes/cache/scratch/oa-evidence/`，可能被缓存清理。响应未留账号、token、项目 ID 或名称。

## 验证

用 `terminal` 在技能目录执行 `python -m unittest discover -s tests -v`。单元测试不联网；live 调用另行执行 `python scripts/oa_options.py` 或 `python scripts/submit_time_entry.py ... --preview --json`，切勿把 fixture 当 live。`complete=false` 不能宣称获取全部项目。只读 API 401 使用现有认证续期一次，不枚举未知端点。

2026-10-10（系统时区 CST，UTC+08:00）本地全套 23 项测试通过。实际提交 CLI 的同一路径完成 live 中文预览与代码预览（结果一致），未知项目/填报类型/阶段/工作类型、全角及尾随空格代码、事假共 7 项拒绝验证。请求守卫仅允许认证、项目/字典和日期查询端点；`saveOrUpdate`/修改端点调用为零。该日期记录在预览前后只读查询结果一致，个人设置字节未变，无草稿写入。测试预览 0.5h 和“中文选项链路验证（仅预览，不提交）”不是已确认实际工作。脱敏原始 CLI 字段及请求路径见 `submission-preview-live-verification.json`；真实项目名称替换为脱敏占位符，其他预览字段保留。真实写入仍待事实确认、授权及提交后读回。
