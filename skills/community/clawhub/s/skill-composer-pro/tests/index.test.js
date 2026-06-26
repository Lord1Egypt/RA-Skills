const { decomposeTask, matchSkills, orchestrate } = require('../src/index');

describe('Skill Composer', () => {
  const mockSkills = [
    {
      id: 'first-principle-analyzer',
      name: '第一性原理分析器',
      category: 'cognitive'
    },
    {
      id: 'meta-skill-weaver',
      name: '元技能编织器',
      category: 'orchestration'
    },
    {
      id: 'copywriting',
      name: '文案写作',
      category: 'creative'
    }
  ];

  describe('decomposeTask function', () => {
    test('should throw error for empty task', () => {
      expect(() => decomposeTask('')).toThrow('Task must be a non-empty string');
    });

    test('should decompose analysis task', () => {
      const subtasks = decomposeTask('分析技术架构问题');
      expect(subtasks.length).toBeGreaterThan(0);
      expect(subtasks[0].type).toBe('analysis');
    });

    test('should decompose report task', () => {
      const subtasks = decomposeTask('生成分析报告');
      expect(subtasks.length).toBeGreaterThan(0);
      expect(subtasks.some(s => s.type === 'writing')).toBe(true);
    });

    test('should handle general task', () => {
      const subtasks = decomposeTask('执行任务');
      expect(subtasks.length).toBe(1);
      expect(subtasks[0].type).toBe('general');
    });
  });

  describe('matchSkills function', () => {
    test('should match skills to subtasks', () => {
      const subtasks = [
        { name: '分析', type: 'analysis', dependsOn: [] },
        { name: '撰写', type: 'writing', dependsOn: [0] }
      ];
      const mapping = matchSkills(subtasks, mockSkills);
      expect(mapping[0]).toBeDefined();
      expect(mapping[1]).toBeDefined();
    });

    test('should handle missing skills', () => {
      const subtasks = [
        { name: '未知类型', type: 'unknown', dependsOn: [] }
      ];
      const mapping = matchSkills(subtasks, mockSkills);
      // May be null if no matching skill
      expect(mapping[0] === null || mapping[0] !== undefined).toBe(true);
    });
  });

  describe('orchestrate function', () => {
    test('should orchestrate workflow', () => {
      const subtasks = [
        { name: '任务 1', type: 'analysis', dependsOn: [] },
        { name: '任务 2', type: 'writing', dependsOn: [0] }
      ];
      const skillMapping = {
        0: mockSkills[0],
        1: mockSkills[2]
      };
      const workflow = orchestrate(subtasks, skillMapping);
      expect(workflow).toHaveProperty('plan');
      expect(workflow).toHaveProperty('estimatedTime');
    });

    test('should identify parallel execution', () => {
      const subtasks = [
        { name: '任务 1', type: 'analysis', dependsOn: [] },
        { name: '任务 2', type: 'analysis', dependsOn: [] }
      ];
      const skillMapping = {
        0: mockSkills[0],
        1: mockSkills[0]
      };
      const workflow = orchestrate(subtasks, skillMapping);
      // Both tasks can run in parallel
      expect(workflow.plan.some(s => s.type === 'parallel')).toBe(true);
    });
  });
});
