/**
 * API 响应基础类型
 */
export interface ApiResponse<T = any> {
  status: string
  message: string
  data: T
}

/**
 * 企业工商信息
 */
export interface EnterpriseInformation {
  统一社会信用代码: string
  企业名称: string
  法定代表人: string
  经营状态: string
  注册资本: string
  成立日期: string
  实缴资本: string
  组织机构代码: string
  工商注册号: string
  纳税人识别号: string
  纳税人资质: string
  企业类型: string
  营业期限: string
  登记机关: string
  所属行业: string
  所属地区: string
  注册地址: string
  经营范围: string
}

/**
 * 股东信息
 */
export interface ShareholderInfo {
  股东名称: string
  股东类型?: string
  持股比例?: string
  认缴出资额?: string
  认缴出资日期?: string
  实缴出资额?: string
  实缴出资日期?: string
}

/**
 * 主要人员信息
 */
export interface KeyPersonnelInfo {
  姓名: string
  职务: string
  直接持股比例?: string
  综合持股比例?: string
}

/**
 * 变更记录
 */
export interface ChangeRecord {
  变更日期: string
  变更事项: string
  变更前: string
  变更后: string
}

/**
 * 候选企业信息
 */
export interface CandidateEnterprise {
  eid: string
  ename: string
  logoUrl: string
  type: string
}

/**
 * Segment 类型
 */
interface Segment {
  type: string
  value: string
  ref_key?: string
}

/**
 * 原始 API 响应类型
 */
export interface RawEnterpriseInfoResponse {
  registrationInformation: {
    creditNo: string
    name: string
    operName: string
    eid: string
    status: string
    regCapi: string
    startDate: string
    actualCapi: string
    orgNo: string
    regNo: string
    taxNo: string
    qualification: string
    econKind: string
    businessTerm: string
    belongOrg: string
    IndustryFourCategories: string[]
    area: string
    address: string
    scope: string
  }
}

export interface RawShareholderResponse {
  items: Array<{
    items: Array<{
      formatName: string
      keyValues: Array<{
        key: string
        value: string
      }>
    }>
  }>
}

export interface RawKeyPersonnelResponse {
  tabList: Array<{
    empList: Array<{
      formatName: string
      position: string
      stockPercent: string
      investPercent: string
    }>
  }>
}

export interface RawChangeRecordResponse {
  items: Array<{
    date: string
    item: string
    beforeSegments: Segment[]
    afterSegments: Segment[]
  }>
}
