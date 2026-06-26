import { CandidateEnterprise } from './types'

/**
 * 多个候选企业错误
 * 当企业名称不唯一时抛出此错误
 */
export class MultipleMatchError extends Error {
  public readonly candidates: CandidateEnterprise[]

  constructor(message: string, candidates: CandidateEnterprise[]) {
    super(message)
    this.name = 'MultipleMatchError'
    this.candidates = candidates

    // 设置原型链（TypeScript 继承 Error 需要）
    Object.setPrototypeOf(this, MultipleMatchError.prototype)
  }

  /**
   * 格式化候选企业列表为可读字符串
   */
  formatCandidates(): string {
    return this.candidates
      .map((c, index) => `${index + 1}. ${c.ename}`)
      .join('\n')
  }

  /**
   * 获取完整的错误信息（包含候选企业列表）
   */
  getFullMessage(): string {
    return `${this.message}\n\n候选企业列表：\n${this.formatCandidates()}\n\n请使用完整的企业名称重新查询。`
  }
}

/**
 * 企业未找到错误
 */
export class EnterpriseNotFoundError extends Error {
  constructor(enterpriseName: string) {
    super(`未找到企业: ${enterpriseName}`)
    this.name = 'EnterpriseNotFoundError'
    Object.setPrototypeOf(this, EnterpriseNotFoundError.prototype)
  }
}
