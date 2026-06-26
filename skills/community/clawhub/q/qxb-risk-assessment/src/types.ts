/**
 * API 响应基础类型
 */
export interface ApiResponse<T = any> {
  status: string
  message: string
  data: T
}

/**
 * 风险明细项
 */
export interface RiskItem {
  title: string
  date: string
  details: string[]
}

/**
 * 空壳企业排查
 */
export interface ShellCompanyCheck {
  shellProbability: string
  abnormalFeatures: Array<{
    feature: string
    description: string
  }>
}

/**
 * 合同违约情况
 */
export interface ContractBreach {
  breachLevel: string
  breachCount: string
  breachScale: string
}

/**
 * 日常经营风险
 */
export interface QixinRisk {
  selfRiskCount: number
  highRiskCount: number
  highRiskItems: RiskItem[]
  mediumRiskCount: number
  mediumRiskItems: RiskItem[]
  lowRiskCount: number
  lowRiskItems: RiskItem[]
  tipCount: number
  relatedRiskCount: number
  relatedHighRiskCount: number
  relatedMediumRiskCount: number
  relatedLowRiskCount: number
}

/**
 * 企业存续情况
 */
export interface EntSurvival {
  bankruptcyRisk: string
  abnormalDissolution: string
  operatingStatus: string
}

/**
 * 企业风险排查（综合）
 */
export interface RiskAssessment {
  ename: string
  shellCompanyCheck: ShellCompanyCheck
  contractBreach: ContractBreach
  qixinRisk: QixinRisk
  entSurvival: EntSurvival
}
