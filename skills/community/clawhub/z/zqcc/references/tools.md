# 企查查中转站工具目录

企查查中转站统一代理 6 类、共 185 项企查查企业数据工具。

快照日期：2026-07-28。执行前必须调用 `tools/list`，并以实时 `inputSchema` 为准；本目录仅用于选择能力，上游参数契约可能独立变化。

## 企业基座 company (16)

| Tool | Capability |
| --- | --- |
| `get_actual_controller` | 实际控制人 |
| `get_annual_reports` | 企业年报 |
| `get_beneficial_owners` | 受益所有人 |
| `get_branches` | 分支机构 |
| `get_change_records` | 变更记录 |
| `get_company_by_query` | 企业实体识别 |
| `get_company_profile` | 企业简介 |
| `get_company_registration_info` | 企业工商信息 |
| `get_contact_info` | 联系方式 |
| `get_external_investments` | 对外投资 |
| `get_financial_data` | 财务数据 |
| `get_key_personnel` | 主要人员 |
| `get_listing_info` | 上市信息 |
| `get_shareholder_info` | 股东信息 |
| `get_tax_invoice_info` | 税号开票信息 |
| `verify_company_accuracy` | 企业准确性验证 |

## 风控大脑 risk (38)

| Tool | Capability |
| --- | --- |
| `get_administrative_penalty` | 行政处罚 |
| `get_bankruptcy_reorganization` | 破产重整 |
| `get_business_exception` | 经营异常 |
| `get_cancellation_record_info` | 注销备案 |
| `get_case_filing_info` | 立案信息 |
| `get_chattel_mortgage_info` | 动产抵押 |
| `get_company_related_risk_scan` | 企业关联风险扫描 |
| `get_company_risk_scan` | 企业风险扫描 |
| `get_court_notice` | 法院公告 |
| `get_default_info` | 违约事项 |
| `get_disciplinary_list` | 惩戒名单 |
| `get_dishonest_info` | 失信信息 |
| `get_environmental_penalty` | 环保处罚 |
| `get_equity_freeze` | 股权冻结 |
| `get_equity_pledge_info` | 股权出质 |
| `get_exit_restriction` | 限制出境 |
| `get_guarantee_info` | 担保信息 |
| `get_hearing_notice` | 开庭公告 |
| `get_high_consumption_restriction` | 限制高消费 |
| `get_judgment_debtor_info` | 被执行人 |
| `get_judicial_auction` | 司法拍卖 |
| `get_judicial_document_detail` | 裁判文书详情 |
| `get_judicial_documents` | 裁判文书 |
| `get_land_mortgage_info` | 土地抵押 |
| `get_liquidation_info` | 清算信息 |
| `get_pre_litigation_mediation` | 诉前调解 |
| `get_property_asset_announcement` | 财产悬赏公告 |
| `get_public_exhortation` | 公示催告 |
| `get_serious_violation` | 严重违法 |
| `get_service_announcement` | 劳动仲裁 |
| `get_service_notice` | 送达公告 |
| `get_simple_cancellation_info` | 简易注销 |
| `get_stock_pledge_info` | 股权质押 |
| `get_tax_abnormal` | 税务非正常户 |
| `get_tax_arrears_notice` | 欠税公告 |
| `get_tax_violation` | 税收违法 |
| `get_terminated_cases` | 终本案件 |
| `get_valuation_inquiry` | 询价评估 |

## 知产引擎 ipr (18)

| Tool | Capability |
| --- | --- |
| `get_app_info` | APP |
| `get_commercial_franchise` | 商业特许经营 |
| `get_copyright_work_info` | 作品著作权 |
| `get_douyin_account` | 抖音 |
| `get_integrated_circuit_layout` | 集成电路布图 |
| `get_international_patent` | 国际专利 |
| `get_internet_service_info` | 网络服务备案 |
| `get_ipr_pledge` | 知产出质 |
| `get_kuaishou_account` | 快手 |
| `get_mini_program` | 小程序 |
| `get_online_store` | 线上店铺 |
| `get_patent_info` | 专利 |
| `get_software_copyright_info` | 软件著作权 |
| `get_standard_info` | 标准信息 |
| `get_trademark_document` | 商标文书 |
| `get_trademark_info` | 商标 |
| `get_wechat_official_account` | 微信公众号 |
| `get_weibo_account` | 微博 |

## 经营罗盘 operation (35)

| Tool | Capability |
| --- | --- |
| `get_administrative_license` | 行政许可 |
| `get_advertising_review` | 广告审查 |
| `get_asset_auction` | 资产拍卖 |
| `get_bidding_info` | 招投标信息 |
| `get_company_announcement` | 企业公告 |
| `get_counterfeit_cosmetics` | 假冒化妆品 |
| `get_credit_commitments` | 信用承诺 |
| `get_credit_evaluation` | 信用评价 |
| `get_entry_denied` | 未准入境 |
| `get_financing_lease_info` | 融资租赁 |
| `get_financing_records` | 融资信息 |
| `get_food_safety` | 食品安全 |
| `get_game_approval` | 游戏审批 |
| `get_government_announcement` | 政府公告 |
| `get_government_interview` | 政府约谈 |
| `get_honor_info` | 荣誉信息 |
| `get_import_export_credit` | 进出口信用 |
| `get_investment_institution` | 投资机构 |
| `get_land_grant_info` | 国有土地受让 |
| `get_land_transfer_info` | 土地转让 |
| `get_news_sentiment` | 新闻舆情 |
| `get_private_fund_manager` | 私募基金管理人 |
| `get_product_recall` | 产品召回 |
| `get_product_spot_check` | 产品抽查 |
| `get_property_rights_transaction` | 产权交易 |
| `get_qualifications` | 资质证书 |
| `get_random_check` | 双随机抽查 |
| `get_ranking_list_info` | 上榜榜单 |
| `get_recruitment_info` | 招聘信息 |
| `get_related_announcement` | 相关公告 |
| `get_software_violation` | 软件违规 |
| `get_spot_check_info` | 抽查检查 |
| `get_taxpayer_qualification` | 纳税人资质 |
| `get_tech_achievement` | 科技成果 |
| `get_telecom_license` | 电信许可 |

## 董监高画像 executive (44)

| Tool | Capability |
| --- | --- |
| `get_executive_admin_penalty` | 董监高-行政处罚 |
| `get_executive_beneficial_owner` | 董监高-作为最终受益人 |
| `get_executive_case_filing` | 董监高-立案信息 |
| `get_executive_controlled_companies` | 董监高-控制企业 |
| `get_executive_court_notice` | 董监高-法院公告 |
| `get_executive_dishonest` | 董监高-失信被执行人 |
| `get_executive_equity_freeze` | 董监高-股权冻结 |
| `get_executive_equity_pledge` | 董监高-股权出质 |
| `get_executive_exit_restriction` | 董监高-限制出境 |
| `get_executive_hearing_notice` | 董监高-开庭公告 |
| `get_executive_high_consumption_ban` | 董监高-限制高消费 |
| `get_executive_historical_admin_penalty` | 董监高-历史行政处罚 |
| `get_executive_historical_case_filing` | 董监高-历史立案信息 |
| `get_executive_historical_court_notice` | 董监高-历史法院公告 |
| `get_executive_historical_dishonest` | 董监高-历史失信被执行人 |
| `get_executive_historical_equity_freeze` | 董监高-历史股权冻结 |
| `get_executive_historical_equity_pledge` | 董监高-历史股权出质 |
| `get_executive_historical_hearing_notice` | 董监高-历史开庭公告 |
| `get_executive_historical_high_consumption_ban` | 董监高-历史限制高消费 |
| `get_executive_historical_investments` | 董监高-历史对外投资 |
| `get_executive_historical_judgment_debtor` | 董监高-历史被执行人 |
| `get_executive_historical_judicial_docs` | 董监高-历史裁判文书 |
| `get_executive_historical_legal_rep_roles` | 董监高-历史担任法定代表人 |
| `get_executive_historical_partners` | 董监高-历史合作伙伴 |
| `get_executive_historical_positions` | 董监高-历史在外任职 |
| `get_executive_historical_pre_litigation_mediation` | 董监高-历史诉前调解 |
| `get_executive_historical_related_companies` | 董监高-历史全部关联企业 |
| `get_executive_historical_service_notice` | 董监高-历史送达公告 |
| `get_executive_historical_terminated_cases` | 董监高-历史终本案件 |
| `get_executive_investments` | 董监高-对外投资 |
| `get_executive_judgment_debtor` | 董监高-被执行人 |
| `get_executive_judicial_docs` | 董监高-裁判文书 |
| `get_executive_legal_rep_roles` | 董监高-担任法定代表人 |
| `get_executive_positions` | 董监高-在外任职 |
| `get_executive_pre_litigation_mediation` | 董监高-诉前调解 |
| `get_executive_property_reward_notice` | 董监高-财产悬赏公告 |
| `get_executive_related_companies` | 董监高-全部关联企业 |
| `get_executive_related_risk_scan` | 董监高关联风险扫描 |
| `get_executive_risk_scan` | 董监高风险扫描 |
| `get_executive_service_notice` | 董监高-送达公告 |
| `get_executive_stock_pledge` | 董监高-股权质押 |
| `get_executive_tax_violation` | 董监高-税收违法 |
| `get_executive_terminated_cases` | 董监高-终本案件 |
| `get_executive_valuation_inquiry` | 董监高-询价评估 |

## 历史存档 history (34)

| Tool | Capability |
| --- | --- |
| `get_historical_admin_license` | 历史行政许可 |
| `get_historical_admin_penalty` | 历史行政处罚 |
| `get_historical_bankruptcy` | 历史破产重整 |
| `get_historical_business_exception` | 历史经营异常 |
| `get_historical_case_filing` | 历史立案信息 |
| `get_historical_chattel_mortgage` | 历史动产抵押 |
| `get_historical_court_notice` | 历史法院公告 |
| `get_historical_dishonest` | 历史失信被执行人 |
| `get_historical_environmental_penalty` | 历史环保处罚 |
| `get_historical_equity_freeze` | 历史股权冻结 |
| `get_historical_equity_pledge` | 历史股权出质 |
| `get_historical_executives` | 历史主要人员 |
| `get_historical_hearing_notice` | 历史开庭公告 |
| `get_historical_high_consumption_ban` | 历史限制高消费 |
| `get_historical_honor` | 历史荣誉信息 |
| `get_historical_internet_service` | 历史备案网站 |
| `get_historical_investments` | 历史对外投资 |
| `get_historical_ipr_pledge` | 历史知产出质 |
| `get_historical_judgment_debtor` | 历史被执行人 |
| `get_historical_judicial_docs` | 历史裁判文书 |
| `get_historical_land_mortgage` | 历史土地抵押 |
| `get_historical_legal_rep` | 历史法定代表人 |
| `get_historical_listing` | 历史上市信息 |
| `get_historical_patent` | 历史专利信息 |
| `get_historical_pre_litigation_mediation` | 历史诉前调解 |
| `get_historical_random_check` | 历史双随机抽查 |
| `get_historical_registration` | 历史工商信息 |
| `get_historical_serious_violation` | 历史严重违法 |
| `get_historical_service_notice` | 历史送达公告 |
| `get_historical_shareholders` | 历史股东信息 |
| `get_historical_spot_check` | 历史抽查检查 |
| `get_historical_tax_arrears` | 历史欠税公告 |
| `get_historical_terminated_cases` | 历史终本案件 |
| `get_historical_trademark` | 历史商标信息 |
