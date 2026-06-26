/**
 * 交互式测试脚本
 *
 * 使用方法：
 * 1. 设置环境变量 QXBENT_API_TOKEN
 * 2. 运行：npx ts-node src/examples/interactive_test.ts
 */

import 'dotenv/config'
import * as readline from 'readline'
import { createClient, MultipleMatchError, EnterpriseNotFoundError } from '../index'

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

function question(prompt: string): Promise<string> {
  return new Promise((resolve) => {
    rl.question(prompt, resolve)
  })
}

async function main() {
  console.log('=== 启信宝企业信息查询交互式测试 ===\n')

  try {
    const client = createClient()
    console.log('✓ API 客户端初始化成功\n')

    while (true) {
      console.log('\n可用操作：')
      console.log('1. 查询企业工商信息')
      console.log('2. 查询企业股东信息')
      console.log('3. 查询企业主要人员')
      console.log('4. 查询企业变更记录')
      console.log('5. 退出')

      const choice = await question('\n请选择操作 (1-5): ')

      if (choice === '5') {
        console.log('\n再见！')
        rl.close()
        break
      }

      if (!['1', '2', '3', '4'].includes(choice)) {
        console.log('无效的选择，请重新输入')
        continue
      }

      const ename = await question('\n请输入企业名称: ')

      try {
        switch (choice) {
          case '1':
            console.log('\n查询企业工商信息...')
            const info = await client.getEnterpriseInformation(ename)
            console.log('\n查询成功！')
            console.log('━'.repeat(60))
            console.log(`企业名称: ${info.企业名称}`)
            console.log(`统一社会信用代码: ${info.统一社会信用代码}`)
            console.log(`法定代表人: ${info.法定代表人}`)
            console.log(`经营状态: ${info.经营状态}`)
            console.log(`注册资本: ${info.注册资本}`)
            console.log(`成立日期: ${info.成立日期}`)
            console.log(`实缴资本: ${info.实缴资本}`)
            console.log(`企业类型: ${info.企业类型}`)
            console.log(`营业期限: ${info.营业期限}`)
            console.log(`登记机关: ${info.登记机关}`)
            console.log(`所属行业: ${info.所属行业}`)
            console.log(`所属地区: ${info.所属地区}`)
            console.log(`注册地址: ${info.注册地址}`)
            console.log(`经营范围: ${info.经营范围.substring(0, 100)}...`)
            console.log('━'.repeat(60))
            break

          case '2':
            console.log('\n查询企业股东信息...')
            const shareholders = await client.getPartnerList(ename)
            console.log(`\n查询成功！共 ${shareholders.length} 个股东：`)
            console.log('━'.repeat(60))
            shareholders.forEach((sh, index) => {
              console.log(`\n${index + 1}. ${sh.股东名称}`)
              if (sh.股东类型) console.log(`   股东类型: ${sh.股东类型}`)
              if (sh.持股比例) console.log(`   持股比例: ${sh.持股比例}`)
              if (sh.认缴出资额) console.log(`   认缴出资额: ${sh.认缴出资额}`)
              if (sh.认缴出资日期) console.log(`   认缴出资日期: ${sh.认缴出资日期}`)
              if (sh.实缴出资额) console.log(`   实缴出资额: ${sh.实缴出资额}`)
              if (sh.实缴出资日期) console.log(`   实缴出资日期: ${sh.实缴出资日期}`)
            })
            console.log('━'.repeat(60))
            break

          case '3':
            console.log('\n查询企业主要人员...')
            const personnel = await client.getEmployeesList(ename)
            console.log(`\n查询成功！共 ${personnel.length} 位主要人员：`)
            console.log('━'.repeat(60))
            personnel.forEach((person, index) => {
              console.log(`\n${index + 1}. ${person.姓名}`)
              console.log(`   职务: ${person.职务}`)
              if (person.直接持股比例 && person.直接持股比例 !== '-') {
                console.log(`   直接持股比例: ${person.直接持股比例}`)
              }
              if (person.综合持股比例 && person.综合持股比例 !== '-') {
                console.log(`   综合持股比例: ${person.综合持股比例}`)
              }
            })
            console.log('━'.repeat(60))
            break

          case '4':
            console.log('\n查询企业变更记录...')
            const changes = await client.getChangeRecords(ename)
            console.log(`\n查询成功！共 ${changes.length} 条变更记录：`)
            console.log('━'.repeat(60))
            changes.forEach((change, index) => {
              console.log(`\n${index + 1}. [${change.变更日期}] ${change.变更事项}`)
              console.log(`   变更前: ${change.变更前.substring(0, 80)}${change.变更前.length > 80 ? '...' : ''}`)
              console.log(`   变更后: ${change.变更后.substring(0, 80)}${change.变更后.length > 80 ? '...' : ''}`)
            })
            console.log('━'.repeat(60))
            break
        }
      } catch (error) {
        if (error instanceof MultipleMatchError) {
          console.log('\n⚠️ 找到多个匹配的企业，请选择：')
          console.log('━'.repeat(60))
          error.candidates.forEach((candidate, index) => {
            console.log(`${index + 1}. ${candidate.ename}`)
          })
          console.log('━'.repeat(60))
          console.log('\n提示：请使用完整的企业名称重新查询')
        } else if (error instanceof EnterpriseNotFoundError) {
          console.log('\n❌ 企业未找到:', error.message)
        } else {
          console.log('\n❌ 查询失败:', (error as Error).message)
        }
      }
    }
  } catch (error) {
    console.error('\n❌ 初始化失败:', (error as Error).message)
    console.error('请确保已设置环境变量 QXBENT_API_TOKEN')
    rl.close()
  }
}

main()
