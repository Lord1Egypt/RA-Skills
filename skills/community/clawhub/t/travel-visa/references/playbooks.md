# Playbooks

## 参数速查表
| 目标 | 首选命令组合 | 典型输入重点 |
|---|---|---|
| 先判断是否需要签证 | `fliggy-fast-search` | 国籍、目的地、停留时长 |
| 确认办理地点与递签路径 | `fliggy-fast-search` + `search-poi` | 办理城市、签证中心关键词 |
| 递签行程联动住宿 | `search-poi` + `search-hotels` | 签证中心名称、办理日期、预算 |
| 多国连程签证核验 | `fliggy-fast-search` + `search-flight` | 入境顺序、转机地、出发日期 |

## Playbook A：单一目的地旅游签证
- **适用**：用户只去一个国家/地区，核心问题是“要不要签、怎么签、多久出签”。
- **命令模板**：

```bash
flyai fliggy-fast-search --query "<国籍> 护照去 <目的地> 旅游签证要求 材料 办理时效"
flyai fliggy-fast-search --query "<目的地> 签证 是否支持电子签 或 落地签"
```

## Playbook B：签证中心办理路径
- **适用**：用户已知需签证，希望确定办理地点、交通和周边落脚点。
- **命令模板**：

```bash
flyai search-poi --city-name "<办理城市>" --keyword "<目的地国家> 签证中心"
flyai search-hotels --dest-name "<办理城市>" --poi-name "<签证中心名称>" --check-in-date <yyyy-mm-dd> --check-out-date <yyyy-mm-dd> --sort distance_asc --max-price <预算>
```

## Playbook C：多国连程与过境风险核验
- **适用**：用户计划多段航班、经停或转机，需识别可能的签证/过境要求风险。
- **命令模板**：

```bash
flyai search-flight --dep "<出发城市>" --arr "<目的地城市>" --date <yyyy-mm-dd> --sort_by duration
flyai fliggy-fast-search --query "<国籍> 经停 <转机地> 过境签 免签 条件"
```
