# 自动化脚本设计（通用框架）

## 技术选型建议

| 技术方案 | 适用场景 | 优势 | 劣势 |
|---------|---------|------|------|
| Selenium WebDriver | 多国家自动化 | 稳定、跨浏览器、可处理复杂交互 | 需要环境配置 |
| Puppeteer | Node.js 环境 | 轻量、速度快、Chrome 原生支持 | 仅支持 Chrome 系 |
| Playwright | 跨浏览器自动化 | 现代化、支持多浏览器、API 友好 | 相对较新 |

## 通用自动化框架伪代码

**⚠️ 重要说明**：
- 以下伪代码仅为示例性质，展示多国家自动化流程的逻辑结构
- 实际实现时需要根据每个国家网站的实际 DOM 结构进行调整
- 网站界面可能随时更新，需要定期维护

```javascript
// 通用入境卡填写框架
class ArrivalCardAutomation {
  constructor(country, userInfo) {
    this.country = country
    this.userInfo = userInfo
    this.config = this.getCountryConfig(country)
  }
  
  // 获取国家配置
  getCountryConfig(country) {
    const configs = {
      'malaysia': {
        url: 'https://imigresen-online.imi.gov.my/mdac/main',
        dateFormat: 'DD/MM/YYYY',
        requiresEmailVerification: true,
        requiresPrint: true
      },
      'thailand': {
        url: 'https://extranet.immigration.go.th/fn/TM6/',
        dateFormat: 'DD/MM/YYYY',
        requiresEmailVerification: false,
        requiresPrint: false
      },
      'singapore': {
        url: 'https://eservices.ica.gov.sg/sgarrivalcard/',
        dateFormat: 'DD/MM/YYYY',
        requiresEmailVerification: true,
        requiresPrint: false,
        timeLimit: { days: 3, before: 'arrival' }
      },
      'indonesia': {
        url: 'https://ecd.imigrasi.go.id/',
        dateFormat: 'DD/MM/YYYY',
        requiresEmailVerification: true,
        requiresPrint: true
      },
      'vietnam': {
        url: 'https://dichvucong.bocongan.gov.vn/',
        dateFormat: 'DD/MM/YYYY',
        requiresEmailVerification: false,
        requiresPrint: false
      },
      'philippines': {
        url: 'https://etravel.gov.ph/',
        dateFormat: 'YYYY-MM-DD',
        requiresEmailVerification: true,
        requiresPrint: true,
        timeLimit: { hours: 72, before: 'departure' }
      }
    }
    return configs[country.toLowerCase()]
  }
  
  // 主流程
  async execute() {
    try {
      // 1. 检查时间限制
      if (this.config.timeLimit) {
        this.checkTimeLimit()
      }
      
      // 2. 访问网站
      await this.navigateToWebsite()
      
      // 3. 根据国家执行不同流程
      switch(this.country.toLowerCase()) {
        case 'malaysia':
          await this.fillMalaysia()
          break
        case 'thailand':
          await this.fillThailand()
          break
        case 'singapore':
          await this.fillSingapore()
          break
        case 'indonesia':
          await this.fillIndonesia()
          break
        case 'vietnam':
          await this.fillVietnam()
          break
        case 'philippines':
          await this.fillPhilippines()
          break
        default:
          throw new Error(`不支持的国家: ${this.country}`)
      }
      
      // 4. 处理邮件验证（如需要）
      if (this.config.requiresEmailVerification) {
        await this.handleEmailVerification()
      }
      
      // 5. 下载/保存确认信息
      await this.saveConfirmation()
      
      return {
        success: true,
        country: this.country,
        confirmationPath: this.confirmationPath
      }
    } catch (error) {
      return {
        success: false,
        country: this.country,
        error: error.message
      }
    }
  }
  
  // 检查时间限制
  checkTimeLimit() {
    const { timeLimit } = this.config
    const now = new Date()
    const arrivalDate = new Date(this.userInfo.arrival_date)
    
    if (timeLimit.before === 'arrival') {
      const daysBeforeArrival = (arrivalDate - now) / (1000 * 60 * 60 * 24)
      if (daysBeforeArrival > timeLimit.days) {
        throw new Error(`${this.country} 入境卡只能在入境前 ${timeLimit.days} 天内填写`)
      }
    } else if (timeLimit.before === 'departure') {
      const hoursBeforeDeparture = (arrivalDate - now) / (1000 * 60 * 60)
      if (hoursBeforeDeparture > timeLimit.hours) {
        throw new Error(`${this.country} 入境卡只能在出发前 ${timeLimit.hours} 小时内填写`)
      }
    }
  }
  
  // 格式化日期
  formatDate(dateString) {
    const date = new Date(dateString)
    const format = this.config.dateFormat
    
    if (format === 'DD/MM/YYYY') {
      return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear()}`
    } else if (format === 'YYYY-MM-DD') {
      return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
    }
  }
}

// 使用示例
const automation = new ArrivalCardAutomation('malaysia', {
  passport_number: 'E12345678',
  country_of_issue: 'China',
  passport_expiry: '31/12/2030',
  surname: 'ZHANG',
  given_name: 'SAN',
  gender: 'Male',
  date_of_birth: '01/01/1990',
  nationality: 'China',
  email: 'user@example.com',
  arrival_date: '15/04/2026',
  flight_number: 'MH370',
  address_in_malaysia: 'Hotel ABC, Kuala Lumpur'
})

const result = await automation.execute()
console.log(result)
```

## 实现建议

1. **模块化设计**：为每个国家创建独立的填写模块，便于维护
2. **配置管理**：使用配置文件管理不同国家的差异（日期格式、时间限制等）
3. **错误处理**：实现统一的错误处理和日志记录机制
4. **重试机制**：添加重试机制，应对网络不稳定
5. **定期维护**：定期测试和更新，因为网站可能会变化
