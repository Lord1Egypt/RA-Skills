import { createClient } from './client'

async function main() {
  const client = createClient()

  try {
    const result = await client.getListedInfo('贵州茅台酒股份有限公司')
    console.log('=== 上市信息 ===')
    console.log('企业名称:', result.ename)
    console.log('上市类型数:', result.listings.length)
    console.log('')

    for (const listing of result.listings) {
      console.log(`--- ${listing.type} ---`)
      console.log('证券简称:', listing.basicInfo.stockName)
      console.log('证券代码:', listing.basicInfo.stockCode)
      console.log('上市日期:', listing.basicInfo.listDate)
      console.log('交易所:', listing.basicInfo.exchange)
      console.log('总市值:', listing.basicInfo.totalMarketValue)
      console.log('流通市值:', listing.basicInfo.circulatingMarketValue)
      console.log('市盈率:', listing.basicInfo.pe)
      console.log('市净率:', listing.basicInfo.pb)
      console.log('')

      console.log('十大股东 (报告期:', listing.shareholders.top10.reportDate, ')')
      for (const s of listing.shareholders.top10.items.slice(0, 5)) {
        console.log(`  ${s.name} - ${s.shares} (${s.ratio})`)
      }

      if (listing.shareholders.top10Tradable) {
        console.log('十大流通股东 (报告期:', listing.shareholders.top10Tradable.reportDate, ')')
        for (const s of listing.shareholders.top10Tradable.items.slice(0, 5)) {
          console.log(`  ${s.name} - ${s.shares} (${s.ratio})`)
        }
      }
      console.log('')

      console.log('财务报表:')
      const fr = listing.financialReport
      if (fr.reportDate) {
        console.log('  报告期:', fr.reportDate)
        // A股/新三板
        if (fr.operatereve) console.log('  营业总收入:', fr.operatereve)
        if (fr.netprofit) console.log('  净利润:', fr.netprofit)
        if (fr.zcfzl) console.log('  资产负债率:', fr.zcfzl)
        // H股
        if (fr.yysr) console.log('  营业收入:', fr.yysr)
        if (fr.yylr) console.log('  营业利润:', fr.yylr)
      } else {
        console.log('  无财务数据')
      }
      console.log('')
    }
  } catch (error: any) {
    console.error('查询失败:', error.message)
  }
}

main()
