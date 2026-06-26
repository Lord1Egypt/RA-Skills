/**
 * windows-esm-installer 单元测试
 */

import { fixWindowsPath, checkSystemDeps, generateInstallScript } from '../src/index';
import { writeFileSync, existsSync, unlinkSync } from 'fs';
import { join } from 'path';

describe('windows-esm-installer', () => {
  describe('fixWindowsPath', () => {
    it('should convert Windows path to file URL', () => {
      expect(fixWindowsPath('C:\\Users\\test')).toBe('file:///C:/Users/test');
      expect(fixWindowsPath('c:\\path\\to\\file')).toBe('file:///c:/path/to/file');
    });

    it('should handle forward slashes', () => {
      expect(fixWindowsPath('C:/Users/test')).toBe('file:///C:/Users/test');
    });

    it('should handle mixed slashes', () => {
      expect(fixWindowsPath('C:\\Users/test\\file')).toBe('file:///C:/Users/test/file');
    });

    it('should handle UNC paths', () => {
      expect(fixWindowsPath('\\\\server\\share')).toBe('file://///server/share');
    });
  });

  describe('checkSystemDeps', () => {
    it('should detect Node.js version', async () => {
      const result = await checkSystemDeps();
      expect(result).toHaveProperty('nodeVersion');
      expect(result).toHaveProperty('npmVersion');
      expect(result).toHaveProperty('missing');
      expect(result).toHaveProperty('warnings');
    });

    it('should return array for missing and warnings', async () => {
      const result = await checkSystemDeps();
      expect(Array.isArray(result.missing)).toBe(true);
      expect(Array.isArray(result.warnings)).toBe(true);
    });
  });

  describe('generateInstallScript', () => {
    const testDir = '/tmp/test-install';
    
    beforeEach(() => {
      // Create test directory if not exists
      try {
        writeFileSync(join(testDir, '.gitkeep'), '');
      } catch {}
    });

    afterEach(() => {
      // Cleanup
      try {
        unlinkSync(join(testDir, 'install.bat'));
        unlinkSync(join(testDir, 'install.ps1'));
        unlinkSync(join(testDir, '.gitkeep'));
      } catch {}
    });

    it('should generate bat and ps1 scripts', () => {
      const result = generateInstallScript(testDir);
      expect(result).toHaveProperty('batPath');
      expect(result).toHaveProperty('ps1Path');
      expect(existsSync(result.batPath)).toBe(true);
      expect(existsSync(result.ps1Path)).toBe(true);
    });

    it('should generate valid bat script content', () => {
      const result = generateInstallScript(testDir);
      const content = existsSync(result.batPath) 
        ? require('fs').readFileSync(result.batPath, 'utf-8') 
        : '';
      
      expect(content).toContain('@echo off');
      expect(content).toContain('npm config set registry');
      expect(content).toContain('npm install');
    });

    it('should generate valid ps1 script content', () => {
      const result = generateInstallScript(testDir);
      const content = existsSync(result.ps1Path) 
        ? require('fs').readFileSync(result.ps1Path, 'utf-8') 
        : '';
      
      expect(content).toContain('Write-Host');
      expect(content).toContain('npm config set registry');
      expect(content).toContain('npm install');
    });
  });
});
