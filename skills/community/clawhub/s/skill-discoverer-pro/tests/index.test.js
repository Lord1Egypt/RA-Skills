const { searchSkills, recommendSkills } = require('../src/index');

describe('Skill Discoverer', () => {
  const mockSkills = [
    {
      id: 'first-principle-analyzer',
      name: '第一性原理分析器',
      description: '第一性原理思维增强工具',
      category: 'cognitive',
      tags: ['analysis', 'first-principles', 'problem-solving']
    },
    {
      id: 'meta-skill-weaver',
      name: '元技能编织器',
      description: '技能编排引擎',
      category: 'orchestration',
      tags: ['orchestration', 'workflow', 'multi-skill']
    },
    {
      id: 'skill-evolver',
      name: '技能进化器',
      description: '技能自我进化引擎',
      category: 'evolution',
      tags: ['evolution', 'improvement', 'feedback']
    }
  ];

  describe('searchSkills function', () => {
    test('should throw error for empty query', () => {
      expect(() => searchSkills('', mockSkills)).toThrow('Query must be a non-empty string');
    });

    test('should return matching skills', () => {
      const results = searchSkills('第一性原理 分析', mockSkills);
      expect(results.length).toBeGreaterThan(0);
      expect(results[0].id).toBe('first-principle-analyzer');
    });

    test('should return skills with similarity scores', () => {
      const results = searchSkills('分析', mockSkills);
      results.forEach(result => {
        expect(result).toHaveProperty('similarity');
        expect(result.similarity).toBeGreaterThanOrEqual(0);
      });
    });

    test('should filter low similarity results', () => {
      const results = searchSkills('不相关的查询', mockSkills);
      results.forEach(result => {
        expect(result.similarity).toBeGreaterThan(0.3);
      });
    });
  });

  describe('recommendSkills function', () => {
    test('should recommend technical skills', () => {
      const results = recommendSkills('technical', mockSkills);
      expect(results.length).toBeGreaterThan(0);
      results.forEach(skill => {
        expect(skill).toHaveProperty('recommendationReason');
      });
    });

    test('should recommend business skills', () => {
      const results = recommendSkills('business', mockSkills);
      // May be empty if no business skills in mock data
      expect(Array.isArray(results)).toBe(true);
    });

    test('should handle unknown task type', () => {
      const results = recommendSkills('unknown', mockSkills);
      expect(Array.isArray(results)).toBe(true);
    });
  });
});
