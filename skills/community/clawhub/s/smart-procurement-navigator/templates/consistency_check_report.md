# 呈交前一致性校验报告

## 校验结论

{{ final_review_result }}

## 项目信息统一性

| 校验项 | 标准值 | 结果 | 问题位置 |
| --- | --- | --- | --- |
| 项目名称 | {{ project_name }} | {{ project_name_check }} | {{ project_name_locations }} |
| 项目编号 | {{ project_code }} | {{ project_code_check }} | {{ project_code_locations }} |
| 采购主体 | {{ buyer }} | {{ buyer_check }} | {{ buyer_locations }} |
| 实施地点 | {{ location }} | {{ location_check }} | {{ location_locations }} |
| 履约期限 | {{ service_period }} | {{ service_period_check }} | {{ service_period_locations }} |

**校验标准**：
- 项目名称：与采购公告完全一致，包括标点符号
- 项目编号：通常格式为"XX-2026-001"或"XXZFCG-2026-001"
- 采购主体：全称，不含简称或别称
- 实施地点：精确到区县级
- 履约期限：起止日期一致，格式统一（如"2026-07-01至2027-06-30"）

## 关键数据统一性

{{ key_number_check_table }}

**必查数据项**：
1. 投标总价（大写/小写一致）
2. 分项报价汇总 = 投标总价
3. 人员数量（简历人数 = 配置表中人数）
4. 案例合同金额（案例表 = 正文引用）
5. 实施周期（方案 = 投标函 = 合同草案）

## 参考文件残留检查

{{ sample_residue_check }}

**全文搜索关键词**：
- 其他公司名称
- 其他项目名称
- "XX"/"xxx"/"{{" 占位符
- 内部批注标记（如"待确认""TODO""FIXME"）

## 模板化表达与内部策略用语检查

{{ ai_tone_cleanup_check }}

## 否决风险自查

{{ rejection_risk_check }}

**否决风险自查清单**：
- [ ] 投标函是否按要求签署盖章
- [ ] 投标保证金是否足额、按时缴纳
- [ ] 所有★号条款是否完全响应
- [ ] 投标有效期是否满足要求
- [ ] 报价是否在预算范围内
- [ ] 资质证书是否在有效期内
- [ ] 业绩证明材料是否齐全
- [ ] 联合体协议是否签署（如适用）

## 呈交前待确认

{{ final_confirmation_items }}
