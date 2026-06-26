const { handler, listTemplates, validateParams } = require('../index.js');

// Mock fetch globally
const mockFetch = jest.fn();
global.fetch = mockFetch;

// Mock successful API response
const mockApiResponse = {
  files: {
    'SOUL.md': '# Test Soul Content',
    'IDENTITY.md': '# Test Identity Content',
    'MEMORY.md': '# Test Memory Content',
    'USER.md': '# Test User Content',
    'TOOLS.md': '# Test Tools Content',
    'AGENTS.md': '# Test Agents Content'
  },
  template: { id: 'developer_v1' },
  language: 'ZH'
};

// Mock successful image response
const mockImageResponse = {
  imageUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=='
};

describe('Soul Weaver', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  test('listTemplates returns available templates', () => {
    const templates = listTemplates();
    
    expect(templates).toHaveProperty('celebrity');
    expect(templates).toHaveProperty('profession');
    expect(templates).toHaveProperty('requiredTools');
    
    expect(templates.celebrity).toContain('musk');
    expect(templates.profession).toContain('developer');
    expect(templates.requiredTools).toContain('find-skills');
  });

  test('validateParams validates correct parameters', () => {
    const validation = validateParams({
      aiName: 'TestAI',
      celebrityName: 'musk',
      profession: 'developer'
    });
    
    expect(validation.valid).toBe(true);
    expect(validation.errors).toHaveLength(0);
  });

  test('validateParams rejects invalid celebrity', () => {
    const validation = validateParams({
      aiName: 'TestAI',
      celebrityName: 'invalid_celebrity'
    });
    
    expect(validation.valid).toBe(false);
    expect(validation.errors).toContain(
      'Invalid celebrityName. Available: musk, jobs, einstein, bezos, da_vinci, qianxuesen, ng, kondo, ferris'
    );
  });

  test('validateParams rejects invalid profession', () => {
    const validation = validateParams({
      aiName: 'TestAI',
      profession: 'invalid_profession'
    });
    
    expect(validation.valid).toBe(false);
    expect(validation.errors).toContain(
      'Invalid profession. Available: developer, writer, researcher, analyst, collaborator'
    );
  });

  test('validateParams requires aiName', () => {
    const validation = validateParams({
      profession: 'developer'
    });
    
    expect(validation.valid).toBe(false);
    expect(validation.errors).toContain('aiName is required');
  });

  test('handler calls API with correct parameters', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockApiResponse
    });

    const result = await handler({
      aiName: 'TestAI',
      userName: 'TestUser',
      profession: 'developer',
      language: 'ZH'
    });

    expect(result.success).toBe(true);
    expect(result.files).toBeDefined();
    expect(result.template).toBeDefined();
    
    // Verify API call
    expect(mockFetch).toHaveBeenCalledWith(
      '
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
    );
  });

  test('handler handles API errors gracefully', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    });

    const result = await handler({
      aiName: 'TestAI',
      profession: 'developer'
    });

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
    expect(result.message).toContain('Failed to generate configuration');
  });

  test('handler includes avatar generation when requested', async () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockImageResponse
      });

    const result = await handler({
      aiName: 'TestAI',
      profession: 'developer',
      generateAvatar: true
    });

    expect(result.success).toBe(true);
    // Should have made two API calls: config + avatar
    expect(mockFetch).toHaveBeenCalledTimes(2);
  });

  test('handler handles avatar generation failure gracefully', async () => {
    mockFetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => mockApiResponse
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 500
      });

    const result = await handler({
      aiName: 'TestAI',
      profession: 'developer',
      generateAvatar: true
    });

    expect(result.success).toBe(true); // Main config should still succeed
    expect(mockFetch).toHaveBeenCalledTimes(2);
  });
});
