const axios = require('axios');
const fs = require('fs');
const path = require('path');

/**
 * 中石化油价查询Skill
 * 查询中石化官方油价信息
 */
class SinopecOilPriceSkill {
  constructor() {
    this.baseUrl = 'https://cx.sinopecsales.com/yjkqiantai';
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8'
      }
    });
  }

  /**
   * 获取油价信息
   * @param {Object} params - 参数
   * @param {string} [params.province_id] - 省份ID
   * @param {string} [params.province_name] - 省份名称（如"北京"、"上海"）
   * @returns {Promise<Object>} 油价数据
   */
  async getOilPrice(params = {}) {
    try {
      // 如果指定了省份名称，先获取省份ID
      if (params.province_name && !params.province_id) {
        const provinceId = await this._getProvinceIdByName(params.province_name);
        if (!provinceId) {
          return {
            success: false,
            message: `未找到省份: ${params.province_name}`,
            date: '',
            prices: []
          };
        }
        params.province_id = provinceId;
      }

      // 调用切换省份API获取油价数据
      const response = await this.client.post('/data/switchProvince', {
        provinceId: params.province_id || ''
      });

      return this._formatResult(response.data);
    } catch (error) {
      console.error('获取油价失败:', error.message);
      return {
        success: false,
        message: `获取油价失败: ${error.message}`,
        date: '',
        prices: []
      };
    }
  }

  /**
   * 监控油价变化（需要保存历史数据）
   * @param {Object} params - 参数
   * @param {string} params.province_name - 省份名称（必填）
   * @param {string} [params.recipient_id] - 接收通知的用户open_id
   * @returns {Promise<Object>} 监控结果
   */
  async monitorOilPrice(params = {}) {
    if (!params.province_name) {
      return {
        success: false,
        message: '缺少必填参数: province_name'
      };
    }

    try {
      // 1. 查询当前油价
      const current = await this.getOilPrice({ province_name: params.province_name });
      if (!current.success) {
        return {
          success: false,
          message: `查询油价失败: ${current.message}`
        };
      }

      // 2. 读取历史数据
      const history = this._readHistory(params.province_name);
      console.log(`上次记录: ${history.date || '无记录'}`);

      // 3. 提取当前价格（取第一个区域）
      const currentPrice = current.prices[0];
      if (!currentPrice) {
        return {
          success: false,
          message: '未获取到油价数据'
        };
      }

      // 4. 定义要监控的油品类型
      const oilTypes = [
        { key: 'gas_92', name: '92号汽油' },
        { key: 'gas_95', name: '95号汽油' },
        { key: 'gas_98', name: '98号汽油' },
        { key: 'diesel_0', name: '0号柴油' },
        { key: 'aipao_98', name: '爱跑98' }
      ];

      // 5. 比较价格变化
      const changes = [];
      oilTypes.forEach(({ key, name }) => {
        const oldPrice = history.prices[key];
        const newPrice = currentPrice[key];
        
        if (newPrice) {
          const comparison = this._comparePrices(oldPrice, newPrice);
          if (comparison && comparison.changed) {
            changes.push({
              name,
              old: comparison.old,
              new: comparison.new,
              diff: comparison.diff
            });
          }
        }
      });

      // 6. 生成消息内容
      let message = '';
      if (changes.length > 0) {
        message = `⛽ ${params.province_name}油价变动通知（${current.date}）\n\n`;
        changes.forEach(change => {
          const arrow = change.diff > 0 ? '↑' : '↓';
          message += `${change.name}: ${change.old} → ${change.new}元/升 (${arrow} ${Math.abs(change.diff)})\n`;
        });
        message += `\n数据来源：中石化官方API\n仅供参考，以加油站实际价格为准`;
      } else {
        message = `⛽ ${params.province_name}油价日报（${current.date}）\n\n`;
        oilTypes.forEach(({ key, name }) => {
          const price = currentPrice[key];
          if (price) {
            message += `${name}: ${price.price}元/升 (${price.change >= 0 ? '+' : ''}${price.change})\n`;
          }
        });
        message += `\n（今日油价无变化）`;
      }

      // 7. 保存当前数据为历史
      this._saveHistory(params.province_name, {
        date: current.date,
        province: current.province,
        prices: {}
      }, currentPrice, oilTypes);

      // 8. 返回结果（实际发送消息由OpenClaw系统处理）
      return {
        success: true,
        message: message,
        hasChanges: changes.length > 0,
        changes: changes,
        province: current.province,
        date: current.date
      };

    } catch (error) {
      console.error('监控油价失败:', error.message);
      return {
        success: false,
        message: `监控失败: ${error.message}`
      };
    }
  }

  /**
   * 根据省份名称获取省份ID
   * @private
   */
  async _getProvinceIdByName(name) {
    try {
      const response = await this.client.get('/core/main');
      const html = response.data;
      
      // 解析省份列表
      const provinceRegex = /{"provinceId":"(\d+)","name":"([^"]+)"}/g;
      let match;
      while ((match = provinceRegex.exec(html)) !== null) {
        if (match[2] === name) {
          return match[1];
        }
      }
      return null;
    } catch (error) {
      console.error('获取省份ID失败:', error.message);
      return null;
    }
  }

  /**
   * 格式化返回结果
   * @private
   */
  async _formatResult(response) {
    if (!response || !response.data) {
      return {
        success: false,
        message: '数据格式错误',
        date: '',
        prices: []
      };
    }

    const { provinceCheck, provinceData, area } = response.data;
    
    // 获取当前日期（从initMainData获取）
    let date = '';
    try {
      const initData = await this.client.get('/data/initMainData');
      date = initData.data.toDay || '';
    } catch (e) {
      date = provinceCheck?.START_DATE ? new Date().toISOString().split('T')[0] : '';
    }

    const result = {
      success: true,
      date: date,
      province: provinceCheck?.PROVINCE_NAME || '',
      areaDesc: provinceCheck?.AREA_DESC || '',
      prices: []
    };

    // 主省份数据
    if (provinceData) {
      result.prices.push(this._extractPrice(provinceData, provinceCheck?.PROVINCE_NAME));
    }

    // 区域数据（某些省份如广东可能有多个价区）
    if (area && Array.isArray(area)) {
      area.forEach(item => {
        if (item.areaData) {
          result.prices.push(this._extractPrice(item.areaData, item.areaCheck?.AREA_DESC || item.areaCheck?.AREA_NAME));
        }
      });
    }

    return result;
  }

  /**
   * 提取价格信息
   * @private
   */
  _extractPrice(priceData, areaName) {
    const getPrice = (field, statusField) => {
      const value = priceData[field];
      const status = priceData[statusField];
      if (value === undefined || value === 0 || value === 0.00) return null;
      return {
        price: value,
        change: status || 0
      };
    };

    return {
      area: areaName || '',
      gas_92: getPrice('GAS_92', 'GAS_92_STATUS'),
      gas_95: getPrice('GAS_95', 'GAS_95_STATUS'),
      gas_98: getPrice('GAS_98', 'GAS_98_STATUS'),
      gas_89: getPrice('GAS_89', 'GAS_89_STATUS'),
      e92: getPrice('E92', 'E92_STATUS'),
      e95: getPrice('E95', 'E95_STATUS'),
      e98: getPrice('E98', 'E98_STATUS'),
      aipao_98: getPrice('AIPAO_GAS_98', 'AIPAO_GAS_98_STATUS'),
      aipao_95: getPrice('AIPAO_GAS_95', 'AIPAO_GAS_95_STATUS'),
      diesel_0: getPrice('CHECHAI_0', 'CHECHAI_0_STATUS'),
      diesel_10: getPrice('CHECHAI_10', 'CHECHAI_10_STATUS'),
      diesel_20: getPrice('CHAI_20', 'CHAI_20_STATUS'),
      diesel_35: getPrice('CHAI_35', 'CHAI_35_STATUS')
    };
  }

  /**
   * 读取历史数据
   * @private
   */
  _readHistory(province) {
    try {
      const historyDir = path.join(__dirname, 'history');
      if (!fs.existsSync(historyDir)) {
        fs.mkdirSync(historyDir, { recursive: true });
      }
      const historyFile = path.join(historyDir, `${province}.json`);
      if (fs.existsSync(historyFile)) {
        const data = fs.readFileSync(historyFile, 'utf8');
        return JSON.parse(data);
      }
    } catch (e) {
      console.error('读取历史数据失败:', e.message);
    }
    return { date: '', prices: {} };
  }

  /**
   * 保存历史数据
   * @private
   */
  _saveHistory(province, baseData, currentPrice, oilTypes) {
    try {
      const historyDir = path.join(__dirname, 'history');
      if (!fs.existsSync(historyDir)) {
        fs.mkdirSync(historyDir, { recursive: true });
      }
      const historyFile = path.join(historyDir, `${province}.json`);
      
      // 提取价格数据
      oilTypes.forEach(({ key }) => {
        if (currentPrice[key]) {
          baseData.prices[key] = currentPrice[key];
        }
      });
      
      fs.writeFileSync(historyFile, JSON.stringify(baseData, null, 2));
      console.log('历史数据已保存:', historyFile);
    } catch (e) {
      console.error('保存历史数据失败:', e.message);
    }
  }

  /**
   * 比较价格变化
   * @private
   */
  _comparePrices(oldPrice, newPrice) {
    if (!oldPrice || !newPrice) return null;
    const priceChanged = oldPrice.price !== newPrice.price;
    const change = newPrice.price - oldPrice.price;
    return {
      changed: priceChanged,
      old: oldPrice.price,
      new: newPrice.price,
      diff: change
    };
  }
}

module.exports = SinopecOilPriceSkill;
