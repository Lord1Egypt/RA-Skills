/**
 * 状态机测试套件
 * @version v0.3.0
 */

const { EvolutionStateMachine, STATES, TRANSITIONS } = require('../state-machine/evolution-state-machine');
const path = require('path');
const fs = require('fs').promises;

describe('EvolutionStateMachine', () => {
  let sm;
  const testSkillName = 'test-skill';
  const testDataDir = path.join(__dirname, '../../data/test');

  beforeEach(async () => {
    try { await fs.rm(testDataDir, { recursive: true, force: true }); } catch (e) {}
    sm = new EvolutionStateMachine(testSkillName, { dataDir: testDataDir, timeoutMs: 5000 });
  });

  afterEach(async () => {
    await sm.reset();
    try { await fs.rm(testDataDir, { recursive: true, force: true }); } catch (e) {}
  });

  describe('初始状态', () => {
    test('应该初始化为 IDLE 状态', () => {
      expect(sm.getCurrentState()).toBe(STATES.IDLE);
    });

    test('应该返回正确的状态机信息', () => {
      const info = sm.getInfo();
      expect(info.skillName).toBe(testSkillName);
      expect(info.currentState).toBe(STATES.IDLE);
      expect(info.historyLength).toBe(0);
    });
  });

  describe('状态转换', () => {
    test('应该允许有效的状态转换', async () => {
      await sm.start();
      expect(sm.getCurrentState()).toBe(STATES.ANALYZING);
    });

    test('应该拒绝无效的状态转换', async () => {
      await expect(sm.transition(STATES.COMPLETED)).rejects.toThrow('Invalid transition');
    });
  });

  describe('状态持久化', () => {
    test('应该持久化状态到文件', async () => {
      await sm.start();
      await sm.persistState();
      const stateFile = path.join(testDataDir, 'state-store', `${testSkillName}-state.json`);
      const content = await fs.readFile(stateFile, 'utf-8');
      const data = JSON.parse(content);
      expect(data.currentState).toBe(STATES.ANALYZING);
    });
  });
});
