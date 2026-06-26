/**
 * API 响应基础类型
 */
export interface ApiResponse<T = any> {
  status: string
  message: string
  data: T
}

/**
 * 股东项
 */
export interface ShareholderItem {
  name: string
  shares: string
  ratio: string
}

/**
 * 基础行情信息
 */
export interface BasicInfo {
  stockName: string
  stockCode: string
  listDate: string
  exchange: string
  totalMarketValue: string
  circulatingMarketValue: string
  totalShares: string
  circulatingShares: string
  pe: string
  pb: string
}

/**
 * 股东信息
 */
export interface Shareholders {
  top10: {
    reportDate: string
    items: ShareholderItem[]
  }
  top10Tradable?: {
    reportDate: string
    items: ShareholderItem[]
  }
}

/**
 * 财务报表（key-value 结构，字段根据上市类型不同）
 */
export interface FinancialReport {
  [key: string]: string
}

/**
 * 单个上市类型信息
 */
export interface Listing {
  type: string
  basicInfo: BasicInfo
  shareholders: Shareholders
  financialReport: FinancialReport
}

/**
 * 上市信息查询结果
 */
export interface ListedInfo {
  ename: string
  listings: Listing[]
}
