/**
 * Code Sandbox - Docker 代码执行沙箱 v1.0
 * 
 * 功能:
 * - Docker 隔离执行
 * - 多语言支持（Python、JavaScript、TypeScript、Bash、Go）
 * - 资源限制（内存、CPU、超时）
 * - 安全隔离
 * - 本地降级执行
 * 
 * Usage:
 *     import { CodeSandbox } from './system/sandbox.js';
 *     
 *     const sandbox = new CodeSandbox({ timeout: 60 });
 *     const result = await sandbox.execute("print('Hello World')", "python");
 *     console.log(result.output);
 */

// ============================================================
// Imports
// ============================================================

import { spawn } from 'child_process';
import { existsSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';
import { randomUUID } from 'crypto';
import { tmpdir } from 'os';
import { mkdirSync, writeFileSync, readFileSync, rmSync } from 'fs';

// ============================================================
// Execution Result
// ============================================================

export class ExecutionResult {
  constructor({
    success = false,
    output = '',
    error = '',
    exitCode = -1,
    duration = 0,
    language = '',
    containerId = '',
    files = {},
    metrics = {},
  }) {
    this.success = success;
    this.output = output;
    this.error = error;
    this.exitCode = exitCode;
    this.duration = duration;
    this.language = language;
    this.containerId = containerId;
    this.files = files;
    this.metrics = metrics;
  }

  toJSON() {
    return {
      success: this.success,
      output: this.output,
      error: this.error,
      exitCode: this.exitCode,
      duration: this.duration,
      language: this.language,
      files: this.files,
      metrics: this.metrics,
    };
  }
}

// ============================================================
// Code Sandbox
// ============================================================

export class CodeSandbox {
  // Docker images for each language
  static IMAGES = {
    'python': 'python:3.11-slim',
    'python3': 'python:3.11-slim',
    'javascript': 'node:18-slim',
    'js': 'node:18-slim',
    'typescript': 'node:18-slim',
    'ts': 'node:18-slim',
    'bash': 'alpine:latest',
    'shell': 'alpine:latest',
    'go': 'golang:1.21-alpine',
    'golang': 'golang:1.21-alpine',
    'java': 'openjdk:17-slim',
    'rust': 'rust:slim',
    'ruby': 'ruby:3.2-slim',
  };

  // File extensions
  static EXTENSIONS = {
    'python': '.py',
    'python3': '.py',
    'javascript': '.js',
    'js': '.js',
    'typescript': '.ts',
    'ts': '.ts',
    'bash': '.sh',
    'shell': '.sh',
    'go': '.go',
    'golang': '.go',
    'java': '.java',
    'rust': '.rs',
    'ruby': '.rb',
  };

  // Run commands
  static RUN_COMMANDS = {
    'python': ['python', 'main.py'],
    'python3': ['python', 'main.py'],
    'javascript': ['node', 'main.js'],
    'js': ['node', 'main.js'],
    'typescript': ['npx', 'ts-node', 'main.ts'],
    'ts': ['npx', 'ts-node', 'main.ts'],
    'bash': ['sh', 'main.sh'],
    'shell': ['sh', 'main.sh'],
    'go': ['go', 'run', 'main.go'],
    'golang': ['go', 'run', 'main.go'],
    'java': ['java', 'Main.java'],
    'rust': ['sh', '-c', 'rustc main.rs -o main && ./main'],
    'ruby': ['ruby', 'main.rb'],
  };

  /**
   * @param {Object} options
   */
  constructor(options = {}) {
    this.timeout = options.timeout || 60;
    this.memoryLimit = options.memoryLimit || '256m';
    this.cpuLimit = options.cpuLimit || '1';
    this.networkDisabled = options.networkDisabled !== false;
    this.useDocker = options.useDocker;
    this._localExecutors = new Map();
    this._detectLocalExecutors();
    if (this.useDocker === undefined) {
      this.useDocker = this._checkDocker();
    }
  }

  _checkDocker() {
    try {
      const { execSync } = require('child_process');
      execSync('docker version', { stdio: 'ignore' });
      return true;
    } catch {
      return false;
    }
  }

  _detectLocalExecutors() {
    const executors = ['python', 'python3', 'node', 'bash', 'sh', 'go', 'ruby'];
    const { execSync } = require('child_process');

    for (const exec of executors) {
      try {
        execSync('which ' + exec, { stdio: 'ignore' });
        this._localExecutors.set(exec, true);
      } catch {
        this._localExecutors.set(exec, false);
      }
    }

    // Map language to executables
    this._langExecutors = {
      'python': this._localExecutors.get('python3') || this._localExecutors.get('python') ? ['python3', 'python'] : [],
      'python3': this._localExecutors.get('python3') ? ['python3'] : [],
      'javascript': this._localExecutors.get('node') ? ['node'] : [],
      'js': this._localExecutors.get('node') ? ['node'] : [],
      'bash': this._localExecutors.get('bash') ? ['bash'] : (this._localExecutors.get('sh') ? ['sh'] : []),
      'shell': this._localExecutors.get('bash') ? ['bash'] : (this._localExecutors.get('sh') ? ['sh'] : []),
      'go': this._localExecutors.get('go') ? ['go'] : [],
      'ruby': this._localExecutors.get('ruby') ? ['ruby'] : [],
    };
  }

  /**
   * Execute code
   * @param {string} code
   * @param {string} language
   * @param {Object} options
   * @returns {Promise<ExecutionResult>}
   */
  async execute(code, language = 'python', options = {}) {
    const {
      files = null,
      env = null,
      stdin = null,
      workdirFiles = null,
    } = options;

    language = language.toLowerCase();

    if (!CodeSandbox.IMAGES[language]) {
      return new ExecutionResult({
        success: false,
        output: '',
        error: `不支持的语言: ${language}。支持: ${Object.keys(CodeSandbox.IMAGES).join(', ')}`,
        exitCode: -1,
        duration: 0,
        language,
      });
    }

    if (this.useDocker) {
      return this._dockerExecute(code, language, files, env, stdin, workdirFiles);
    } else {
      return this._localExecute(code, language, files, env, stdin, workdirFiles);
    }
  }

  /**
   * Docker execution
   * @private
   */
  async _dockerExecute(code, language, files, env, stdin, workdirFiles) {
    const startTime = Date.now();
    let containerId = '';
    const tmpDir = join(tmpdir(), `sandbox_${randomUUID().slice(0, 8)}`);

    try {
      mkdirSync(tmpDir, { recursive: true });

      // Write main code file
      const ext = CodeSandbox.EXTENSIONS[language] || '.txt';
      const mainFile = join(tmpDir, `main${ext}`);
      writeFileSync(mainFile, code, 'utf-8');

      // Write additional files
      if (files) {
        for (const [name, content] of Object.entries(files)) {
          writeFileSync(join(tmpDir, name), content, 'utf-8');
        }
      }

      // Write workdir files
      if (workdirFiles) {
        for (const [name, content] of Object.entries(workdirFiles)) {
          writeFileSync(join(tmpDir, name), content, 'utf-8');
        }
      }

      const image = CodeSandbox.IMAGES[language];

      // Build docker command
      /** @type {string[]} */
      const dockerCmd = [
        'docker', 'run', '--rm',
        '-v', `${tmpDir}:/workspace`,
        '-w', '/workspace',
        '--memory', this.memoryLimit,
        '--cpus', this.cpuLimit,
      ];

      // Network settings
      if (this.networkDisabled) {
        dockerCmd.push('--network=none');
      }

      // Environment variables
      if (env) {
        for (const [k, v] of Object.entries(env)) {
          dockerCmd.extend(['-e', `${k}=${v}`]);
        }
      }

      // Container name for tracking
      containerId = `sandbox_${Date.now()}`;
      dockerCmd.extend(['--name', containerId]);

      // Image and command
      dockerCmd.push(image);
      dockerCmd.push(...(CodeSandbox.RUN_COMMANDS[language] || ['cat', 'main.txt']));

      // Execute
      const result = await this._runProcess(dockerCmd, {
        timeout: this.timeout,
        input: stdin,
      });

      const duration = (Date.now() - startTime) / 1000;

      // Collect generated files
      const outputFiles = {};
      try {
        const { readdirSync } = require('fs');
        const dirFiles = readdirSync(tmpDir);
        for (const f of dirFiles) {
          if (f !== `main${ext}`) {
            try {
              outputFiles[f] = readFileSync(join(tmpDir, f), 'utf-8');
            } catch {}
          }
        }
      } catch {}

      return new ExecutionResult({
        success: result.exitCode === 0,
        output: result.stdout,
        error: result.stderr,
        exitCode: result.exitCode,
        duration,
        language,
        containerId,
        files: outputFiles,
        metrics: {
          memory_limit: this.memoryLimit,
          cpu_limit: this.cpuLimit,
          network_disabled: this.networkDisabled,
        },
      });
    } catch (e) {
      const duration = (Date.now() - startTime) / 1000;

      if (e.message && e.message.includes('Timeout')) {
        return new ExecutionResult({
          success: false,
          output: '',
          error: `执行超时 (${this.timeout}s)`,
          exitCode: -1,
          duration: this.timeout,
          language,
          containerId,
        });
      }

      return new ExecutionResult({
        success: false,
        output: '',
        error: e.message,
        exitCode: -1,
        duration,
        language,
      });
    } finally {
      // Cleanup
      try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
    }
  }

  /**
   * Local execution (fallback)
   * @private
   */
  async _localExecute(code, language, files, env, stdin, workdirFiles) {
    const startTime = Date.now();
    const tmpDir = join(tmpdir(), `sandbox_${randomUUID().slice(0, 8)}`);

    try {
      mkdirSync(tmpDir, { recursive: true });

      // Check if language is available locally
      const executors = this._langExecutors[language] || [];
      if (executors.length === 0) {
        const available = [...new Set(Object.values(this._langExecutors).flat())];
        return new ExecutionResult({
          success: false,
          output: '',
          error: `本地执行不支持: ${language}。可用: ${available.join(', ')}`,
          exitCode: -1,
          duration: 0,
          language,
        });
      }

      // Write code
      const ext = CodeSandbox.EXTENSIONS[language] || '.txt';
      const mainFile = join(tmpDir, `main${ext}`);
      writeFileSync(mainFile, code, 'utf-8');

      // Write additional files
      if (files) {
        for (const [name, content] of Object.entries(files)) {
          writeFileSync(join(tmpDir, name), content, 'utf-8');
        }
      }

      // Build command
      let cmd;
      const exec = executors[0];

      if (language === 'python' || language === 'python3') {
        cmd = [exec, mainFile];
      } else if (language === 'javascript' || language === 'js') {
        cmd = [exec, mainFile];
      } else if (language === 'bash' || language === 'shell') {
        cmd = [exec, mainFile];
      } else if (language === 'go') {
        cmd = [exec, 'run', mainFile];
      } else if (language === 'ruby') {
        cmd = [exec, mainFile];
      } else {
        cmd = ['cat', mainFile];
      }

      // Execute
      const result = await this._runProcess(cmd, {
        timeout: this.timeout,
        input: stdin,
        cwd: tmpDir,
        env,
      });

      return new ExecutionResult({
        success: result.exitCode === 0,
        output: result.stdout,
        error: result.stderr,
        exitCode: result.exitCode,
        duration: (Date.now() - startTime) / 1000,
        language,
        metrics: { mode: 'local' },
      });
    } catch (e) {
      return new ExecutionResult({
        success: false,
        output: '',
        error: e.message,
        exitCode: -1,
        duration: (Date.now() - startTime) / 1000,
        language,
      });
    } finally {
      try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
    }
  }

  /**
   * Run a process with timeout
   * @private
   */
  _runProcess(cmd, options = {}) {
    return new Promise((resolve) => {
      const {
        timeout = 60,
        input = null,
        cwd = null,
        env = null,
      } = options;

      const procEnv = env ? { ...process.env, ...env } : undefined;

      const proc = spawn(cmd[0], cmd.slice(1), {
        cwd,
        env: procEnv,
        stdio: input ? ['pipe', 'pipe', 'pipe'] : ['ignore', 'pipe', 'pipe'],
      });

      let stdout = '';
      let stderr = '';
      let timedOut = false;

      const timer = setTimeout(() => {
        timedOut = true;
        proc.kill('SIGKILL');
      }, timeout * 1000);

      if (input && proc.stdin) {
        proc.stdin.write(input);
        proc.stdin.end();
      }

      if (proc.stdout) {
        proc.stdout.on('data', (data) => { stdout += data.toString(); });
      }
      if (proc.stderr) {
        proc.stderr.on('data', (data) => { stderr += data.toString(); });
      }

      proc.on('close', (code) => {
        clearTimeout(timer);
        resolve({
          stdout,
          stderr,
          exitCode: timedOut ? -1 : code,
          timedOut,
        });
      });

      proc.on('error', (e) => {
        clearTimeout(timer);
        resolve({
          stdout: '',
          stderr: e.message,
          exitCode: -1,
          timedOut: false,
        });
      });
    });
  }

  /**
   * Test code
   * @param {string} code
   * @param {string} testCode
   * @param {string} language
   * @param {string} testFramework
   * @returns {Promise<ExecutionResult>}
   */
  async testCode(code, testCode = null, language = 'python', testFramework = 'pytest') {
    let fullCode;

    if (language === 'python') {
      if (testFramework === 'pytest' && testCode) {
        fullCode = `${code}\n\n# Tests\n${testCode}`;
      } else {
        fullCode = `${code}\n\nif __name__ == '__main__':\n${testCode || ''}`;
      }
    } else if (language === 'javascript' || language === 'js') {
      fullCode = `${code}\n\n// Tests\n${testCode || ''}`;
    } else {
      fullCode = code;
    }

    return this.execute(fullCode, language);
  }

  /**
   * Run a file
   * @param {string} filePath
   * @param {string|null} language
   * @param {Object} options
   * @returns {Promise<ExecutionResult>}
   */
  async runFile(filePath, language = null, options = {}) {
    if (!existsSync(filePath)) {
      return new ExecutionResult({
        success: false,
        output: '',
        error: `文件不存在: ${filePath}`,
        exitCode: -1,
        duration: 0,
      });
    }

    // Auto-detect language
    if (!language) {
      const ext = filePath.split('.').pop().toLowerCase();
      const extMap = {
        'py': 'python',
        'js': 'javascript',
        'ts': 'typescript',
        'sh': 'bash',
        'go': 'go',
        'rb': 'ruby',
      };
      language = extMap[ext] || 'python';
    }

    const code = readFileSync(filePath, 'utf-8');
    return this.execute(code, language, options);
  }

  /**
   * List supported languages
   * @returns {string[]}
   */
  listLanguages() {
    return Object.keys(CodeSandbox.IMAGES);
  }

  /**
   * Get executor info
   * @returns {Object}
   */
  getExecutorInfo() {
    return {
      docker_available: this.useDocker,
      local_executors: Object.fromEntries(this._localExecutors),
      supported_languages: this.listLanguages(),
      config: {
        timeout: this.timeout,
        memory_limit: this.memoryLimit,
        cpu_limit: this.cpuLimit,
        network_disabled: this.networkDisabled,
      },
    };
  }
}

// ============================================================
// CLI
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'info';

  let useDocker = undefined;
  if (args.includes('--docker')) useDocker = true;
  if (args.includes('--local')) useDocker = false;

  const sandbox = new CodeSandbox({ useDocker });

  if (command === 'info') {
    const info = sandbox.getExecutorInfo();
    console.log('沙箱信息:');
    console.log(`  Docker 可用: ${info.docker_available}`);
    console.log('  本地执行器:');
    for (const [lang, available] of Object.entries(info.local_executors)) {
      console.log(`    - ${lang}: ${available ? '✅' : '❌'}`);
    }
    console.log(`  支持的语言: ${info.supported_languages.join(', ')}`);
    console.log(`  配置: ${JSON.stringify(info.config)}`);
    return;
  }

  if (command === 'run') {
    const codeIndex = args.indexOf('--code');
    const fileIndex = args.indexOf('--file');
    const langIndex = args.indexOf('--language');
    const lang = langIndex >= 0 ? args[langIndex + 1] : 'python';

    let result;
    if (codeIndex >= 0) {
      const code = args.slice(codeIndex + 1).join(' ').replace(/^['"]|['"]$/g, '');
      result = await sandbox.execute(code, lang);
    } else if (fileIndex >= 0) {
      result = await sandbox.runFile(args[fileIndex + 1], lang);
    } else {
      console.error('请提供 --code 或 --file');
      process.exit(1);
    }

    console.log(`成功: ${result.success}`);
    console.log(`退出码: ${result.exitCode}`);
    console.log(`耗时: ${result.duration.toFixed(2)}s`);
    console.log(`输出:\n${result.output}`);
    if (result.error) console.log(`错误:\n${result.error}`);
    return;
  }

  if (command === 'test') {
    const code = args.find(a => a.startsWith('--code='))?.split('=')[1] ||
      "def add(a, b):\n    return a + b";
    const testCode = `
def test_add():
    assert add(1, 2) == 3
    assert add(0, 0) == 0
    print('All tests passed!')
`;
    const result = await sandbox.testCode(code, testCode, 'python');
    console.log(`测试${result.success ? '通过' : '失败'}`);
    console.log(`输出: ${result.output}`);
    if (result.error) console.log(`错误: ${result.error}`);
    return;
  }

  if (command === 'demo') {
    const demos = {
      'python': "print('Hello from Python!')\nfor i in range(3):\n    print(f'Count: {i}')",
      'javascript': "console.log('Hello from JavaScript!');\nfor(let i = 0; i < 3; i++) {\n  console.log(`Count: ${i}`);\n}",
      'bash': "echo 'Hello from Bash!'\nfor i in 1 2 3; do\n  echo \"Count: $i\"\ndone",
    };

    for (const [lang, code] of Object.entries(demos)) {
      console.log(`\n--- ${lang.toUpperCase()} ---`);
      const result = await sandbox.execute(code, lang);
      console.log(`成功: ${result.success}`);
      console.log(`输出: ${result.output.slice(0, 100)}`);
    }
  }
}

const isMain = process.argv[1]?.endsWith('sandbox.js') || process.argv[1]?.endsWith('sandbox.mjs');
if (isMain) {
  main().catch(console.error);
}

export default CodeSandbox;
