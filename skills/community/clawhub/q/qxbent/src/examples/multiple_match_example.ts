/**
 * 多个候选企业处理示例
 *
 * 演示如何处理企业名称不唯一的情况
 *
 * 使用方法：
 * 1. 设置环境变量 QXBENT_API_TOKEN
 * 2. 运行：npx ts-node src/examples/multiple_match_example.ts
 */

import 'dotenv/config'
import { createClient, MultipleMatchError, EnterpriseNotFoundError } from '../index'

async function main() {
  const client = createClient()

  // 示例 1: 使用不完整的企业名称查询（会返回多个候选企业）
  console.log('=== 示例 1: 使用不完整的企业名称查询 ===')
  try {
    const info = await client.getEnterpriseInformation('胜宏科技')
    console.log('企业信息:', info)
  } catch (error) {
    if (error instanceof MultipleMatchError) {
      console.log('找到多个匹配的企业：')
      console.log(error.getFullMessage())
      console.log('\n候选企业详情：')
      error.candidates.forEach((candidate, index) => {
        console.log(`\n${index + 1}. ${candidate.ename}`)
        console.log(`   EID: ${candidate.eid}`)
        console.log(`   Logo: ${candidate.logoUrl || '无'}`)
      })
    } else {
      console.error('错误:', error)
    }
  }
  console.log('')

  // 示例 2: 使用完整的企业名称查询（精确匹配）
  console.log('=== 示例 2: 使用完整的企业名称查询 ===')
  try {
    const info = await client.getEnterpriseInformation('胜宏科技（惠州）股份有限公司')
    console.log('✓ 成功查询到企业信息')
    console.log('企业名称:', info.企业名称)
    console.log('统一社会信用代码:', info.统一社会信用代码)
    console.log('法定代表人:', info.法定代表人)
  } catch (error: any) {
    console.error('错误:', error.message)
  }
  console.log('')

  // 示例 3: 查询不存在的企业
  console.log('=== 示例 3: 查询不存在的企业 ===')
  try {
    const info = await client.getEnterpriseInformation('这是一个不存在的企业名称123456')
    console.log('企业信息:', info)
  } catch (error) {
    if (error instanceof EnterpriseNotFoundError) {
      console.log('企业未找到:', error.message)
    } else {
      console.error('错误:', error)
    }
  }
  console.log('')

  // 示例 4: 在 AI 交互场景中的处理建议
  console.log('=== AI 交互场景处理建议 ===')
  console.log('当捕获到 MultipleMatchError 时：')
  console.log('1. AI 应向用户展示候选企业列表')
  console.log('2. 请用户选择或提供更完整的企业名称')
  console.log('3. 使用完整名称重新查询')
  console.log('')
  console.log('示例对话：')
  console.log('User: 查询胜宏科技的信息')
  console.log('AI: 找到多个匹配的企业，请选择：')
  console.log('    1. 胜宏科技（惠州）股份有限公司')
  console.log('    2. 惠州市胜宏科技研究院有限公司')
  console.log('    3. 南通胜宏科技有限公司')
  console.log('    ...')
  console.log('User: 第一个')
  console.log('AI: [使用"胜宏科技（惠州）股份有限公司"查询]')
}

main().catch(console.error)
