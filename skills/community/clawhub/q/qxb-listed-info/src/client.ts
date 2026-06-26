import axios, { AxiosInstance } from 'axios'
import { ApiResponse, ListedInfo } from './types'

const DEFAULT_API_TOKEN = process.env.QXBENT_API_TOKEN

/**
 * 启信宝上市信息综合查询客户端
 */
export class QxbListedInfoClient {
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
   * 查询上市信息（综合）
   * @param ename 企业名称
   * @returns 上市信息
   */
  async getListedInfo(ename: string): Promise<ListedInfo> {
    const response = await this.client.post<ApiResponse<ListedInfo>>(
      '/enterprise/getListedInfo',
      { ename }
    )

    if (response.data.status !== '1') {
      throw new Error(response.data.message || '查询失败')
    }

    return response.data.data
  }

  /**
   * 通过企业ID查询上市信息
   * @param eid 企业ID
   * @returns 上市信息
   */
  async getListedInfoByEid(eid: string): Promise<ListedInfo> {
    const response = await this.client.post<ApiResponse<ListedInfo>>(
      '/enterprise/getListedInfo',
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
export function createClient(apiToken?: string): QxbListedInfoClient {
  const token = apiToken || DEFAULT_API_TOKEN
  if (!token) {
    throw new Error('请提供 API Token 或设置环境变量 QXBENT_API_TOKEN')
  }
  return new QxbListedInfoClient(token)
}
