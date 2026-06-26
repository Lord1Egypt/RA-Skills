import { createClient } from './client'

async function main() {
  const client = createClient()

  try {
    const result = await client.getGsBasicInfo('深圳市腾讯计算机系统有限公司')
    console.log('=== 企业工商基本信息 ===')
    console.log('企业名称:', result.ename)
    console.log('统一社会信用代码:', result.creditNo)
    console.log('法定代表人:', result.operName)
    console.log('注册资本:', result.regCapi)
    console.log('实缴资本:', result.actualCapi)
    console.log('经营状态:', result.status)
    console.log('成立日期:', result.startDate)
    console.log('企业类型:', result.econKind)
    console.log('营业期限:', result.businessTerm)
    console.log('纳税人资质:', result.qualification)
    console.log('所属地区:', result.area)
    console.log('所属行业:', result.industry)
    if (result.actualController) {
      console.log('疑似实控人:', result.actualController.name, result.actualController.stockPercent)
    }
    if (result.socialSecurityInfo) {
      console.log('社保人数:', result.socialSecurityInfo.count, `(${result.socialSecurityInfo.year}年)`)
    }
  } catch (error: any) {
    console.error('查询失败:', error.message)
  }
}

main()
