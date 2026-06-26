import { createClient } from './client'

async function main() {
  const client = createClient()

  try {
    const result = await client.getRiskAssessment('恒大地产集团有限公司')
    console.log('=== 企业风险排查 ===')
    console.log('企业名称:', result.ename)
    console.log('')

    console.log('--- 空壳企业排查 ---')
    console.log('空壳概率:', result.shellCompanyCheck.shellProbability || '未命中')
    if (result.shellCompanyCheck.abnormalFeatures.length > 0) {
      console.log('异常特征:')
      for (const f of result.shellCompanyCheck.abnormalFeatures) {
        console.log(`  - ${f.feature}: ${f.description}`)
      }
    }
    console.log('')

    console.log('--- 合同违约 ---')
    console.log('违约等级:', result.contractBreach.breachLevel || '无数据')
    console.log('违约次数:', result.contractBreach.breachCount || '无数据')
    console.log('违约规模:', result.contractBreach.breachScale || '无数据')
    console.log('')

    console.log('--- 日常经营风险 ---')
    console.log('自身风险总数:', result.qixinRisk.selfRiskCount)
    console.log('高风险:', result.qixinRisk.highRiskCount)
    console.log('中风险:', result.qixinRisk.mediumRiskCount)
    console.log('低风险:', result.qixinRisk.lowRiskCount)
    console.log('关联风险总数:', result.qixinRisk.relatedRiskCount)
    if (result.qixinRisk.highRiskItems.length > 0) {
      console.log('最新高风险:')
      for (const item of result.qixinRisk.highRiskItems.slice(0, 3)) {
        console.log(`  - [${item.date}] ${item.title}`)
      }
    }
    console.log('')

    console.log('--- 企业存续 ---')
    console.log('破产风险:', result.entSurvival.bankruptcyRisk)
    console.log('非正常解散:', result.entSurvival.abnormalDissolution)
    console.log('经营状态:', result.entSurvival.operatingStatus)
  } catch (error: any) {
    console.error('查询失败:', error.message)
  }
}

main()
