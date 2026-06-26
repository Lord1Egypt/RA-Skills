import { loadConfig, loadFromOpenClawConfig, mergeConfigs, type CompactConfig } from '../config.js';

describe('Config', () => {
  describe('loadConfig', () => {
    it('should return default config when no overrides provided', () => {
      const config = loadConfig();
      expect(config.max_tokens).toBe(10000);
      expect(config.preserve_recent).toBe(4);
      expect(config.auto_compact).toBe(true);
      expect(config.model).toBe('');
    });

    it('should override default values with provided options', () => {
      const config = loadConfig({
        max_tokens: 5000,
        preserve_recent: 6,
        model: 'qwen/qwen3.5-122b'
      });
      expect(config.max_tokens).toBe(5000);
      expect(config.preserve_recent).toBe(6);
      expect(config.model).toBe('qwen/qwen3.5-122b');
      expect(config.auto_compact).toBe(true); // default preserved
    });

    it('should handle partial overrides', () => {
      const config = loadConfig({ max_tokens: 8000 });
      expect(config.max_tokens).toBe(8000);
      expect(config.preserve_recent).toBe(4); // default
      expect(config.auto_compact).toBe(true); // default
    });
  });

  describe('loadFromOpenClawConfig', () => {
    it('should return default config when pluginConfig is empty', () => {
      const config = loadFromOpenClawConfig({});
      expect(config.max_tokens).toBe(10000);
      expect(config.preserve_recent).toBe(4);
      expect(config.auto_compact).toBe(true);
      expect(config.model).toBe('');
    });

    it('should return default config when pluginConfig is null', () => {
      const config = loadFromOpenClawConfig(null);
      expect(config.max_tokens).toBe(10000);
      expect(config.preserve_recent).toBe(4);
      expect(config.auto_compact).toBe(true);
      expect(config.model).toBe('');
    });

    it('should return default config when pluginConfig is undefined', () => {
      const config = loadFromOpenClawConfig(undefined);
      expect(config.max_tokens).toBe(10000);
      expect(config.preserve_recent).toBe(4);
      expect(config.auto_compact).toBe(true);
      expect(config.model).toBe('');
    });

    it('should load config from pluginConfig.config field', () => {
      const pluginConfig = {
        config: {
          max_tokens: 15000,
          preserve_recent: 6,
          auto_compact: false,
          model: 'custom-model'
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(15000);
      expect(config.preserve_recent).toBe(6);
      expect(config.auto_compact).toBe(false);
      expect(config.model).toBe('custom-model');
    });

    it('should load config from pluginConfig directly when config field is missing', () => {
      const pluginConfig = {
        max_tokens: 12000,
        preserve_recent: 5,
        auto_compact: true,
        model: 'direct-model'
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(12000);
      expect(config.preserve_recent).toBe(5);
      expect(config.auto_compact).toBe(true);
      expect(config.model).toBe('direct-model');
    });

    it('should use default values for missing config parameters', () => {
      const pluginConfig = {
        config: {
          max_tokens: 8000
          // preserve_recent, auto_compact, model are missing
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(8000);
      expect(config.preserve_recent).toBe(4); // default
      expect(config.auto_compact).toBe(true); // default
      expect(config.model).toBe(''); // default
    });

    it('should handle partial config with only preserve_recent', () => {
      const pluginConfig = {
        config: {
          preserve_recent: 8
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(10000); // default
      expect(config.preserve_recent).toBe(8);
      expect(config.auto_compact).toBe(true); // default
      expect(config.model).toBe(''); // default
    });

    it('should handle partial config with only auto_compact', () => {
      const pluginConfig = {
        config: {
          auto_compact: false
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(10000); // default
      expect(config.preserve_recent).toBe(4); // default
      expect(config.auto_compact).toBe(false);
      expect(config.model).toBe(''); // default
    });

    it('should handle partial config with only model', () => {
      const pluginConfig = {
        config: {
          model: 'qwen/qwen3.5-122b-a10b'
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(10000); // default
      expect(config.preserve_recent).toBe(4); // default
      expect(config.auto_compact).toBe(true); // default
      expect(config.model).toBe('qwen/qwen3.5-122b-a10b');
    });

    it('should handle config with zero values', () => {
      const pluginConfig = {
        config: {
          max_tokens: 0,
          preserve_recent: 0
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(0);
      expect(config.preserve_recent).toBe(0);
      expect(config.auto_compact).toBe(true); // default
      expect(config.model).toBe(''); // default
    });

    it('should handle config with empty string model', () => {
      const pluginConfig = {
        config: {
          model: ''
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(10000); // default
      expect(config.preserve_recent).toBe(4); // default
      expect(config.auto_compact).toBe(true); // default
      expect(config.model).toBe('');
    });

    it('should handle OpenClaw plugin config structure', () => {
      const pluginConfig = {
        enabled: true,
        config: {
          max_tokens: 20000,
          preserve_recent: 6,
          auto_compact: true,
          model: 'nvidia/qwen/qwen3.5-122b-a10b'
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(20000);
      expect(config.preserve_recent).toBe(6);
      expect(config.auto_compact).toBe(true);
      expect(config.model).toBe('nvidia/qwen/qwen3.5-122b-a10b');
    });

    it('should handle config with null values', () => {
      const pluginConfig = {
        config: {
          max_tokens: null,
          preserve_recent: null,
          auto_compact: null,
          model: null
        }
      };
      const config = loadFromOpenClawConfig(pluginConfig);
      expect(config.max_tokens).toBe(10000); // default
      expect(config.preserve_recent).toBe(4); // default
      expect(config.auto_compact).toBe(true); // default
      expect(config.model).toBe(''); // default
    });
  });

  describe('mergeConfigs', () => {
    it('should merge base and override configs correctly', () => {
      const base = { max_tokens: 12000, preserve_recent: 5 };
      const override = { model: 'custom-model' };
      const config = mergeConfigs(base, override);
      
      expect(config.max_tokens).toBe(12000);
      expect(config.preserve_recent).toBe(5);
      expect(config.model).toBe('custom-model');
      expect(config.auto_compact).toBe(true); // default
    });

    it('should prioritize override over base', () => {
      const base = { max_tokens: 10000, preserve_recent: 4 };
      const override = { max_tokens: 15000 };
      const config = mergeConfigs(base, override);
      
      expect(config.max_tokens).toBe(15000);
      expect(config.preserve_recent).toBe(4);
    });

    it('should apply defaults when both base and override are empty', () => {
      const config = mergeConfigs({}, {});
      expect(config.max_tokens).toBe(10000);
      expect(config.preserve_recent).toBe(4);
      expect(config.auto_compact).toBe(true);
    });
  });
});
