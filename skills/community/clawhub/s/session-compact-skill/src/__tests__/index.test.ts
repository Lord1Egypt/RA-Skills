import { Command } from 'commander';
import { register } from '../index.js';

// Mock the engine module
jest.mock('../compact/engine.js', () => ({
  estimateTokenCount: jest.fn(() => 41),
  shouldCompact: jest.fn(() => false),
  compactSession: jest.fn().mockResolvedValue({
    removedCount: 2,
    savedTokens: 500,
    summary: '<summary>Test summary</summary>',
    formattedSummary: 'Test summary',
    continuationPrompt: 'Continue...',
  }),
  getCurrentModel: jest.fn(() => 'qwen/qwen3.5-122b-a10b'),
}));

// Mock config module
jest.mock('../compact/config.js', () => ({
  loadConfig: jest.fn(() => ({
    max_tokens: 10000,
    preserve_recent: 4,
    auto_compact: true,
    model: '',
  })),
  loadFromOpenClawConfig: jest.fn((pluginConfig = {}) => {
    const config = pluginConfig?.config || pluginConfig || {};
    return {
      max_tokens: config.max_tokens ?? 10000,
      preserve_recent: config.preserve_recent ?? 4,
      auto_compact: config.auto_compact ?? true,
      model: config.model ?? '',
    };
  }),
}));

import { estimateTokenCount, shouldCompact, compactSession, getCurrentModel } from '../compact/engine.js';
import { loadConfig, loadFromOpenClawConfig } from '../compact/config.js';

function createMockProgram() {
  const commands = new Map<string, any>();

  const mockCommand = (name: string) => {
    const cmd: any = {
      _name: name,
      description: jest.fn().mockReturnThis(),
      option: jest.fn().mockReturnThis(),
      argument: jest.fn().mockReturnThis(),
      action: jest.fn().mockReturnThis(),
    };
    commands.set(name, cmd);
    return cmd;
  };

  const program = {
    command: jest.fn(mockCommand),
  } as unknown as Command & { command: jest.Mock };

  return { program, commands };
}

describe('register()', () => {
  let mockApi: any;
  let program: Command & { command: jest.Mock };
  let commands: Map<string, any>;

  beforeEach(() => {
    jest.clearAllMocks();
    const result = createMockProgram();
    program = result.program;
    commands = result.commands;
    mockApi = {
      registerCli: jest.fn(),
    };
  });

  it('should call api.registerCli with correct commands list', () => {
    register(mockApi);

    expect(mockApi.registerCli).toHaveBeenCalledTimes(1);
    const callArgs = mockApi.registerCli.mock.calls[0];
    expect(callArgs[1]).toEqual({
      commands: ['compact', 'compact-status', 'compact-config', 'sessions', 'session-info'],
      descriptors: [
        { name: 'compact', description: 'Manually compact the current session history to save tokens' },
        { name: 'compact-status', description: 'Show current session token usage and compression status' },
        { name: 'compact-config', description: 'Show or update compact configuration' },
        { name: 'sessions', description: 'List all saved sessions' },
        { name: 'session-info', description: 'Show detailed session information' },
      ],
    });
  });

  it('should pass a registrar function to api.registerCli', () => {
    register(mockApi);
    const registrar = mockApi.registerCli.mock.calls[0][0];
    expect(typeof registrar).toBe('function');
  });

  describe('registrar function', () => {
    it('should register compact command when invoked', async () => {
      register(mockApi);
      const registrar = mockApi.registerCli.mock.calls[0][0];
      await registrar({ program });

      expect(program.command).toHaveBeenCalledWith('compact');
      const compactCmd = commands.get('compact');
      expect(compactCmd.description).toHaveBeenCalledWith(
        'Manually compact the current session history to save tokens'
      );
      expect(compactCmd.option).toHaveBeenCalledWith('--force', 'Force compact even if under threshold');
      expect(compactCmd.action).toHaveBeenCalled();
    });

    it('should register compact-status command when invoked', async () => {
      register(mockApi);
      const registrar = mockApi.registerCli.mock.calls[0][0];
      await registrar({ program });

      expect(program.command).toHaveBeenCalledWith('compact-status');
      const cmd = commands.get('compact-status');
      expect(cmd.description).toHaveBeenCalledWith(
        'Show current session token usage and compression status'
      );
      expect(cmd.action).toHaveBeenCalled();
    });

    it('should register compact-config command when invoked', async () => {
      register(mockApi);
      const registrar = mockApi.registerCli.mock.calls[0][0];
      await registrar({ program });

      expect(program.command).toHaveBeenCalledWith('compact-config');
      const cmd = commands.get('compact-config');
      expect(cmd.description).toHaveBeenCalledWith(
        'Show or update compact configuration'
      );
      expect(cmd.argument).toHaveBeenCalledWith('[key]', 'Configuration key (e.g., max_tokens, preserve_recent)');
      expect(cmd.argument).toHaveBeenCalledWith('[value]', 'New value');
      expect(cmd.action).toHaveBeenCalled();
    });
  });

  describe('compact command action', () => {
    let compactAction: (opts: any) => Promise<void>;

    beforeEach(async () => {
      register(mockApi);
      const registrar = mockApi.registerCli.mock.calls[0][0];
      await registrar({ program });
      compactAction = commands.get('compact').action.mock.calls[0][0];
    });

    it('should show token count and skip when under threshold', async () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(false);

      await compactAction({});

      expect(logSpy).toHaveBeenCalledWith('📊 Current session tokens: 41');
      expect(logSpy).toHaveBeenCalledWith('📉 Threshold: 10000');
      expect(logSpy).toHaveBeenCalledWith('✅ Session is within token limits. No compaction needed.');
      expect(compactSession).not.toHaveBeenCalled();

      logSpy.mockRestore();
    });

    it('should compact when force is true', async () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(false);

      await compactAction({ force: true });

      expect(logSpy).toHaveBeenCalledWith('🔄 Compacting session...');
      expect(compactSession).toHaveBeenCalled();
      expect(logSpy).toHaveBeenCalledWith('✅ Successfully compacted 2 messages.');
      expect(logSpy).toHaveBeenCalledWith('💰 Saved ~500 tokens.');

      logSpy.mockRestore();
    });

    it('should compact when shouldCompact returns true', async () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(true);

      await compactAction({});

      expect(compactSession).toHaveBeenCalled();
      logSpy.mockRestore();
    });

    it('should warn when no messages to compact', async () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(true);
      (compactSession as jest.Mock).mockResolvedValueOnce({
        removedCount: 0,
        savedTokens: 0,
        summary: '',
        formattedSummary: '',
        continuationPrompt: '',
      });

      await compactAction({});

      expect(logSpy).toHaveBeenCalledWith('⚠️ No messages to compact.');
      logSpy.mockRestore();
    });
  });

  describe('compact-status command action', () => {
    let statusAction: () => void;

    beforeEach(async () => {
      register(mockApi);
      const registrar = mockApi.registerCli.mock.calls[0][0];
      await registrar({ program });
      statusAction = commands.get('compact-status').action.mock.calls[0][0];
    });

    it('should display session status with OK status', () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(false);
      (estimateTokenCount as jest.Mock).mockReturnValue(41);

      statusAction();

      expect(logSpy).toHaveBeenCalledWith('📊 Session Status');
      expect(logSpy).toHaveBeenCalledWith('  Current tokens: 41');
      expect(logSpy).toHaveBeenCalledWith('  Threshold:      10,000');
      expect(logSpy).toHaveBeenCalledWith('  Usage:          0%');
      expect(logSpy).toHaveBeenCalledWith('  Status:         ✅ OK');
      expect(logSpy).toHaveBeenCalledWith('  Preserve recent: 4 messages');
      expect(logSpy).toHaveBeenCalledWith('  Auto compact:    Enabled');
      expect(logSpy).toHaveBeenCalledWith('  Model:           qwen/qwen3.5-122b-a10b');

      logSpy.mockRestore();
    });

    it('should display needs compact status when threshold exceeded', () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(true);
      (estimateTokenCount as jest.Mock).mockReturnValue(9500);

      statusAction();

      expect(logSpy).toHaveBeenCalledWith('  Usage:          95%');
      expect(logSpy).toHaveBeenCalledWith('  Status:         ⚠️ Needs compact');

      logSpy.mockRestore();
    });

    it('should use configured model when set', () => {
      // The register() function calls loadFromOpenClawConfig() once at registration time.
      // To test with a custom model, we need to re-register with a fresh mock.
      (loadFromOpenClawConfig as jest.Mock).mockReturnValue({
        max_tokens: 10000,
        preserve_recent: 4,
        auto_compact: true,
        model: 'custom/model',
      });
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      (shouldCompact as jest.Mock).mockReturnValue(false);
      (estimateTokenCount as jest.Mock).mockReturnValue(41);

      // Re-register with the updated config mock
      const mockApi2 = { registerCli: jest.fn() };
      register(mockApi2);
      const registrar2 = mockApi2.registerCli.mock.calls[0][0];
      const { program: p2, commands: c2 } = createMockProgram();
      registrar2({ program: p2 });
      const action2 = c2.get('compact-status').action.mock.calls[0][0];
      action2();

      expect(logSpy).toHaveBeenCalledWith('  Model:           custom/model');

      logSpy.mockRestore();
    });
  });

  describe('compact-config command action', () => {
    let configAction: (key: string, value: string) => void;

    beforeEach(async () => {
      register(mockApi);
      const registrar = mockApi.registerCli.mock.calls[0][0];
      await registrar({ program });
      configAction = commands.get('compact-config').action.mock.calls[0][0];
    });

    it('should show all config when no key provided', () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

      configAction(undefined as any, undefined as any);

      expect(logSpy).toHaveBeenCalledWith('🔧 Current Configuration');
      expect(logSpy).toHaveBeenCalledWith('  max_tokens: 10000');
      expect(logSpy).toHaveBeenCalledWith('  preserve_recent: 4');
      expect(logSpy).toHaveBeenCalledWith('  auto_compact: true');
      // model is empty string, so output is '  model: '
      const modelCall = logSpy.mock.calls.find(c => c[0].startsWith('  model:'));
      expect(modelCall).toBeTruthy();

      logSpy.mockRestore();
    });

    it('should show single config value when key provided without value', () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

      configAction('max_tokens', undefined as any);

      expect(logSpy).toHaveBeenCalledWith('max_tokens = 10000');
      logSpy.mockRestore();
    });

    it('should show error for unknown config key', () => {
      const errSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

      configAction('unknown_key', undefined as any);

      expect(errSpy).toHaveBeenCalledWith('❌ Unknown config key: unknown_key');
      errSpy.mockRestore();
    });

    it('should show set message when key and value provided', () => {
      const logSpy = jest.spyOn(console, 'log').mockImplementation(() => {});

      configAction('max_tokens', '5000');

      expect(logSpy).toHaveBeenCalledWith('⚙️  Setting max_tokens = 5000 (not persisted yet)');
      logSpy.mockRestore();
    });
  });
});
