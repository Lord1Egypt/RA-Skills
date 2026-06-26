//  Quality Gates Skill - basic test
describe('quality-gates skill', () => {
  it('should have correct metadata', () => {
    const skill = require('../src')
    expect(skill).toBeDefined()
  })
})
