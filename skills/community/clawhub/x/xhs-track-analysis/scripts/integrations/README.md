# A 方案接入骨架（scripts/integrations）

> 把「官方/第三方合规数据平台」作为**稳定主数据源**，与 `scripts/collector`（B 方案，人工补采兜底）共用同一下游。

## 架构
```
config.json
    │  source: mock | pgy | juguang | thirdparty
    ▼
run_pipeline.py ──► Adapter(DataSsource 接口)
    │                ├─ MockAdapter       (演示，无需凭证)
    │                ├─ PgyAdapter        (蒲公英·官方)
    │                ├─ JuguangAdapter    (聚光·官方)
    │                └─ ThirdPartyAdapter(千瓜/新红/蝉妈妈/灰豚)
    ▼
normalizer.save() ──► raw_notes_A_*.csv + collection_report_A_*.md
    │
    ▼
交给 xhs-track-analysis Skill 按 methodology 完成分析
```
**关键**：A 与 B 产出 schema 完全一致（同 `NoteRecord` → 同 CSV/MD），下游分析无差别。

## 为什么是骨架
- 蒲公英/聚光/第三方各需**品牌自有账号与授权**，endpoint 与字段以各平台官方文档为准；
- 适配器已实现：`authenticate()` 鉴权 + `_map_note()` 字段映射模板；
- `search_notes()` 等方法当前为 `NotImplementedError` 骨架，填入官方请求与字段映射即可上线；
- 无凭证时用 `source=mock` 跑通整条管线，验证归一化与下游衔接。

## 安装与运行
```bash
cd scripts/integrations
pip install requests            # 真实适配器调用时需要
cp config.example.json config.json
# 编辑 config.json：source 选 pgy/juguang/thirdparty，并在 credentials 填 token
python3 run_pipeline.py config.json
```
输出写入 `output/`：`raw_notes_A_<ts>.csv` 与 `collection_report_A_<ts>.md`。

## 合规边界
- ✅ 官方/第三方平台为合规数据来源（需账号/订阅）；
- ✅ 仅用于本 Skill 定义的赛道分析资料准备；
- ⚠️ 真实接入须遵守各平台 API 条款与《个人信息保护法》对评论等个人信息处理的要求；
- A 方案为主、B 方案（采集器）为人工补采兜底，二者互补，不替代彼此。

## 文件
| 文件 | 作用 |
|---|---|
| `source_base.py` | `DataSource` 抽象接口 + `NoteRecord` 结构 |
| `normalizer.py` | 归一化为 CSV/MD（与 collector 同构） |
| `pgy.py` / `juguang.py` / `thirdparty.py` | 官方/第三方适配器骨架 |
| `mock.py` | 演示适配器（无凭证跑通管线） |
| `run_pipeline.py` | 编排：选源→摘取→归一化→落盘 |
| `config.example.json` | 配置样例 |
