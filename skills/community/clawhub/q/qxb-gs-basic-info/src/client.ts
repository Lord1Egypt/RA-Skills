import axios, { AxiosInstance } from 'axios'
import { ApiResponse, GsBasicInfo } from './types'

const DEFAULT_API_TOKEN = process.env.QXBENT_API_TOKEN

/**
 * 启信宝企业工商基本信息查询客户端
 */
export class QxbGsBasicInfoClient {
  private client: AxiosInstance

  constructor(apiToken: string, baseURL: string = 'https://external-api.qixin.com/skill/ent/public') {
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
   * 查询企业工商基本信息
   * @param ename 企业名称
   * @returns 企业工商基本信息
   */
  async getGsBasicInfo(ename: string): Promise<GsBasicInfo> {
    const response = await this.client.post<ApiResponse<GsBasicInfo>>(
      '/enterprise/getGsBasicInfo',
      { ename }
    )

    if (response.data.status !== '1') {
      throw new Error(response.data.message || '查询失败')
    }

    return response.data.data
  }

  /**
   * 通过企业ID查询工商基本信息
   * @param eid 企业ID
   * @returns 企业工商基本信息
   */
  async getGsBasicInfoByEid(eid: string): Promise<GsBasicInfo> {
    const response = await this.client.post<ApiResponse<GsBasicInfo>>(
      '/enterprise/getGsBasicInfo',
      { eid }
    )

    if (response.data.status !== '1') {
      throw new Error(response.data.message || '查询失败')
    }

    return response.data.data
  }
}

/**
 * 创建客户端实例
 * @param apiToken API Token，可选，默认从环境变量 QXBENT_API_TOKEN 读取
 */
export function createClient(apiToken?: string): QxbGsBasicInfoClient {
  const token = apiToken || DEFAULT_API_TOKEN
  if (!token) {
    throw new Error('请提供 API Token 或设置环境变量 QXBENT_API_TOKEN')
  }
  return new QxbGsBasicInfoClient(token)
}
