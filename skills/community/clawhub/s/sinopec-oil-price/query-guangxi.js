#!/usr/bin/env node

const SinopecOilPriceSkill = require('./index.js');

/**
 * 查询广西油价
 */
async function queryGuangxi() {
  console.log('=== 查询广西油价 ===\n');
  
  const skill = new SinopecOilPriceSkill();
  
  // 查询广西油价
  const result = await skill.getOilPrice({ province_name: '广西' });
  
  if (!result.success) {
    console.error('查询失败:', result.message);
    process.exit(1);
  }
  
  console.log(`查询时间: ${result.date}`);
  console.log(`省份: ${result.province}`);
  console.log(`区域: ${result.areaDesc || '默认'}\n`);
  
  // 打印价格（取第一个区域）
  const price = result.prices[0];
  if (!price) {
    console.error('未获取到油价数据');
    process.exit(1);
  }
  
  console.log('油价信息:');
  console.log('----------');
  
  const oilTypes = [
    { key: 'gas_92', name: '92号汽油' },
    { key: 'gas_95', name: '95号汽油' },
    { key: 'gas_98', name: '98号汽油' },
    { key: 'gas_89', name: '89号汽油' },
    { key: 'e92', name: 'E92乙醇汽油' },
    { key: 'e95', name: 'E95乙醇汽油' },
    { key: 'aipao_98', name: '爱跑98' },
    { key: 'aipao_95', name: '爱跑95' },
    { key: 'diesel_0', name: '0号柴油' },
    { key: 'diesel_10', name: '-10号柴油' },
    { key: 'diesel_20', name: '-20号柴油' },
    { key: 'diesel_35', name: '-35号柴油' }
  ];
  
  oilTypes.forEach(({ key, name }) => {
    const p = price[key];
    if (p) {
      const changeStr = p.change >= 0 ? `+${p.change}` : `${p.change}`;
      console.log(`${name}: ${p.price} 元/升 (${changeStr})`);
    }
  });
  
  console.log('\n仅供参考，以加油站实际价格为准');
  
  return result;
}

queryGuangxi().then(() => {
  process.exit(0);
}).catch(e => {
  console.error('执行失败:', e);
  process.exit(1);
});
