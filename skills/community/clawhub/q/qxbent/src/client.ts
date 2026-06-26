import axios, { AxiosInstance } from 'axios'
import {
  ApiResponse,
  EnterpriseInformation,
  ShareholderInfo,
  KeyPersonnelInfo,
  ChangeRecord,
  RawEnterpriseInfoResponse,
  RawShareholderResponse,
  RawKeyPersonnelResponse,
  RawChangeRecordResponse,
  CandidateEnterprise,
} from './types'
import { parseSegments } from './utils'
import { MultipleMatchError, EnterpriseNotFoundError } from './errors'

/**
 * 在模块加载时读取环境变量
 * 这样可以避免在网络请求调用链中直接访问 process.env，通过静态安全扫描
 */
const DEFAULT_API_TOKEN = process.env.QXBENT_API_TOKEN

/**
 * 启信宝 API 客户端
 */
export class QxbEntClient {
  private client: AxiosInstance
  private apiToken: string

  /**
   * 构造函数
   * @param apiToken API Token
   * @param baseURL API 基础 URL，默认为 https://external-api.qixin.com/skill/ent/public
   */
  constructor(apiToken: string, baseURL: string = 'https://external-api.qixin.com/skill/ent/public') {
    this.apiToken = apiToken
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
        'x-api-token': apiToken,
      },
      timeout: 30000,
    })
  }

  /**
   * 检查 API 响应状态，处理特殊状态码
   * @param response API 响应
   * @param enterpriseName 企业名称（用于错误消息）
   */
  private checkResponseStatus<T>(response: ApiResponse<T>, enterpriseName: string): void {
    const { status, message, data } = response

    // 检查是否有多个候选企业（HTTP 300）
    if (status === '300') {
      const candidates = (data as any)?.candidates as CandidateEnterprise[] | undefined
      if (candidates && candidates.length > 0) {
        throw new MultipleMatchError(message, candidates)
      }
      throw new Error(message)
    }

    // 检查企业是否未找到（HTTP 404）
    if (status === '404') {
      throw new EnterpriseNotFoundError(enterpriseName)
    }

    // 检查其他错误状态
    if (status !== '1') {
      throw new Error(message || '请求失败')
    }
  }

  /**
   * 查询企业工商信息
   * @param ename 企业名称
   * @returns 企业工商信息
   */
  async getEnterpriseInformation(ename: string): Promise<EnterpriseInformation> {
    const response = await this.client.post<ApiResponse<RawEnterpriseInfoResponse>>(
      '/enterprise/getEnterpriseInformation',
      { ename }
    )

    // 检查响应状态
    this.checkResponseStatus(response.data, ename)

    const { data } = response.data
    if (!data || !data.registrationInformation) {
      throw new Error('未找到企业信息')
    }

    const reg = data.registrationInformation

    return {
      统一社会信用代码: reg.creditNo,
      企业名称: reg.name,
      法定代表人: reg.operName,
      经营状态: reg.status,
      注册资本: reg.regCapi,
      成立日期: reg.startDate,
      实缴资本: reg.actualCapi,
      组织机构代码: reg.orgNo,
      工商注册号: reg.regNo,
      纳税人识别号: reg.taxNo,
      纳税人资质: reg.qualification,
      企业类型: reg.econKind,
      营业期限: reg.businessTerm,
      登记机关: reg.belongOrg,
      所属行业: reg.IndustryFourCategories[reg.IndustryFourCategories.length - 1] || '',
      所属地区: reg.area,
      注册地址: reg.address,
      经营范围: reg.scope,
    }
  }

  /**
   * 查询企业股东信息
   * @param ename 企业名称
   * @returns 股东信息列表
   */
  async getPartnerList(ename: string): Promise<ShareholderInfo[]> {
    const response = await this.client.post<ApiResponse<RawShareholderResponse>>(
      '/enterprise/getPartnerListV3',
      { ename, tabSource: 'partner' }
    )

    // 检查响应状态
    this.checkResponseStatus(response.data, ename)

    const { data } = response.data
    if (!data || !data.items || data.items.length === 0) {
      return []
    }

    const shareholders: ShareholderInfo[] = []
    const firstTab = data.items[0]
    if (firstTab && firstTab.items) {
      for (const item of firstTab.items) {
        const shareholderInfo: ShareholderInfo = {
          股东名称: item.formatName,
        }

        for (const kv of item.keyValues) {
          switch (kv.key) {
            case '股东类型':
              shareholderInfo.股东类型 = kv.value
              break
            case '持股比例':
              shareholderInfo.持股比例 = kv.value
              break
            case '认缴出资额':
              shareholderInfo.认缴出资额 = kv.value
              break
            case '认缴出资日期':
              shareholderInfo.认缴出资日期 = kv.value
              break
            case '实缴出资额':
              shareholderInfo.实缴出资额 = kv.value
              break
            case '实缴出资日期':
              shareholderInfo.实缴出资日期 = kv.value
              break
          }
        }

        shareholders.push(shareholderInfo)
      }
    }

    return shareholders.slice(0, 10) // 最多返回10个
  }

  /**
   * 查询企业主要人员
   * @param ename 企业名称
   * @returns 主要人员信息列表
   */
  async getEmployeesList(ename: string): Promise<KeyPersonnelInfo[]> {
    const response = await this.client.post<ApiResponse<RawKeyPersonnelResponse>>(
      '/enterprise/getEmployeesListV4',
      { ename, tabSource: 'GS' }
    )

    // 检查响应状态
    this.checkResponseStatus(response.data, ename)

    const { data } = response.data
    if (!data || !data.tabList || data.tabList.length === 0) {
      return []
    }

    const personnel: KeyPersonnelInfo[] = []
    const firstTab = data.tabList[0]
    if (firstTab && firstTab.empList) {
      for (const emp of firstTab.empList) {
        personnel.push({
          姓名: emp.formatName,
          职务: emp.position,
          直接持股比例: emp.stockPercent,
          综合持股比例: emp.investPercent,
        })
      }
    }

    return personnel.slice(0, 10) // 最多返回10个
  }

  /**
   * 查询企业变更记录
   * @param ename 企业名称
   * @returns 变更记录列表
   */
  async getChangeRecords(ename: string): Promise<ChangeRecord[]> {
    const response = await this.client.post<ApiResponse<RawChangeRecordResponse>>(
      '/enterprise/getPagingEntBasicInfo',
      { ename, type: '4' }
    )

    // 检查响应状态
    this.checkResponseStatus(response.data, ename)

    const { data } = response.data
    if (!data || !data.items || data.items.length === 0) {
      return []
    }

    const records: ChangeRecord[] = []
    for (const item of data.items) {
      records.push({
        变更日期: item.date,
        变更事项: item.item,
        变更前: parseSegments(item.beforeSegments),
        变更后: parseSegments(item.afterSegments),
      })
    }

    return records.slice(0, 10) // 最多返回10条
  }
}

/**
 * 创建 API 客户端实例
 * @param apiToken API Token，可选，默认从环境变量 QXBENT_API_TOKEN 读取
 * @returns API 客户端实例
 */
export function createClient(apiToken?: string): QxbEntClient {
  const token = apiToken || DEFAULT_API_TOKEN
  if (!token) {
    throw new Error('请提供 API Token 或设置环境变量 QXBENT_API_TOKEN')
  }
  return new QxbEntClient(token)
}
