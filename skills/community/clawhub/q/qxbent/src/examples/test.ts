/**
 * 快速测试示例
 *
 * 使用方法：
 * 1. 设置环境变量 QXBENT_API_TOKEN
 * 2. 运行：npm run test
 */

import 'dotenv/config'
import { createClient } from '../client'

async function test() {
  try {
    console.log('=== 启信宝 API 测试 ===\n')

    // 创建客户端
    const client = createClient()
    const companyName = '上海合合信息科技股份有限公司'

    // 测试 1: 查询企业工商信息
    console.log('1. 测试查询企业工商信息...')
    try {
      const info = await client.getEnterpriseInformation(companyName)
      console.log('✓ 成功')
      console.log(`  企业名称: ${info.企业名称}`)
      console.log(`  统一社会信用代码: ${info.统一社会信用代码}`)
      console.log(`  法定代表人: ${info.法定代表人}`)
      console.log(`  注册资本: ${info.注册资本}`)
    } catch (error: any) {
      console.log('✗ 失败:', error.message)
    }
    console.log('')

    // 测试 2: 查询股东信息
    console.log('2. 测试查询股东信息...')
    try {
      const shareholders = await client.getPartnerList(companyName)
      console.log('✓ 成功')
      console.log(`  共 ${shareholders.length} 个股东`)
      if (shareholders.length > 0) {
        console.log(`  示例: ${shareholders[0].股东名称} - 持股${shareholders[0].持股比例 || '未知'}`)
      }
    } catch (error: any) {
      console.log('✗ 失败:', error.message)
    }
    console.log('')

    // 测试 3: 查询主要人员
    console.log('3. 测试查询主要人员...')
    try {
      const personnel = await client.getEmployeesList(companyName)
      console.log('✓ 成功')
      console.log(`  共 ${personnel.length} 位主要人员`)
      if (personnel.length > 0) {
        console.log(`  示例: ${personnel[0].姓名} - ${personnel[0].职务}`)
      }
    } catch (error: any) {
      console.log('✗ 失败:', error.message)
    }
    console.log('')

    // 测试 4: 查询变更记录
    console.log('4. 测试查询变更记录...')
    try {
      const changes = await client.getChangeRecords(companyName)
      console.log('✓ 成功')
      console.log(`  共 ${changes.length} 条变更记录`)
      if (changes.length > 0) {
        console.log(`  最新: [${changes[0].变更日期}] ${changes[0].变更事项}`)
      }
    } catch (error: any) {
      console.log('✗ 失败:', error.message)
    }
    console.log('')

    console.log('=== 测试完成 ===')
  } catch (error: any) {
    console.error('测试失败:', error.message)
    process.exit(1)
  }
}

test()
