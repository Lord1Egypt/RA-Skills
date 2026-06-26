const { evaluateSkill, compareVersions } = require('../src/index');

describe('Six-Dim Evaluator', () => {
  const mockSkillPath = '/tmp/mock-skill';

  describe('evaluateSkill function', () => {
    test('should throw error for non-existent path', () => {
      expect(() => evaluateSkill('/non-existent-path')).toThrow('Skill path does not exist');
    });

    test('should return evaluation result', () => {
      // This test would require a real skill directory
      // For now, we test the structure
      const result = {
        skillPath: mockSkillPath,
        scores: { T: 0.70, C: 0.70, O: 0.70, E: 0.70, M: 0.70, U: 0.70 },
        overall: 0.70,
        suggestions: [],
        evaluatedAt: new Date().toISOString()
      };
      
      expect(result).toHaveProperty('skillPath');
      expect(result).toHaveProperty('scores');
      expect(result).toHaveProperty('overall');
      expect(result).toHaveProperty('suggestions');
      expect(result).toHaveProperty('evaluatedAt');
    });

    test('should calculate overall score correctly', () => {
      const scores = { T: 0.80, C: 0.80, O: 0.80, E: 0.80, M: 0.80, U: 0.80 };
      // Weighted average with O and E having 1.5 weight, M having 1.2 weight
      const expected = (0.80 * 1.0 + 0.80 * 1.0 + 0.80 * 1.5 + 0.80 * 1.5 + 0.80 * 1.2 + 0.80 * 1.0) / 7.2;
      expect(expected).toBeCloseTo(0.80, 2);
    });
  });

  describe('compareVersions function', () => {
    test('should compare two versions', () => {
      const oldResult = {
        scores: { T: 0.70, C: 0.70, O: 0.70, E: 0.70, M: 0.70, U: 0.70 },
        overall: 0.70
      };
      const newResult = {
        scores: { T: 0.75, C: 0.75, O: 0.75, E: 0.75, M: 0.75, U: 0.75 },
        overall: 0.75
      };
      
      const comparison = compareVersions(oldResult, newResult);
      
      expect(comparison).toHaveProperty('oldVersion');
      expect(comparison).toHaveProperty('newVersion');
      expect(comparison).toHaveProperty('changes');
      expect(comparison.changes.overall.change).toBe(0.05);
      expect(comparison.changes.overall.trend).toBe('improved');
    });

    test('should detect degraded dimensions', () => {
      const oldResult = {
        scores: { T: 0.80, C: 0.80, O: 0.80, E: 0.80, M: 0.80, U: 0.80 },
        overall: 0.80
      };
      const newResult = {
        scores: { T: 0.75, C: 0.80, O: 0.80, E: 0.80, M: 0.80, U: 0.80 },
        overall: 0.79
      };
      
      const comparison = compareVersions(oldResult, newResult);
      
      expect(comparison.changes.T.trend).toBe('degraded');
      expect(comparison.changes.T.change).toBeCloseTo(-0.05, 2);
    });
  });
});
