/**
 * API 响应基础类型
 */
export interface ApiResponse<T = any> {
  status: string
  message: string
  data: T
}

/**
 * 企业工商基本信息
 */
export interface GsBasicInfo {
  ename: string
  creditNo: string
  name: string
  operName: string
  startDate: string
  regCapi: string
  actualCapi: string
  status: string
  actualController: {
    name: string
    stockPercent: string
  } | null
  econKind: string
  businessTerm: string
  qualification: string
  socialSecurityInfo: {
    year: string
    count: number
  } | null
  area: string
  industry: string
}
