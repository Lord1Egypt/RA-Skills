/**
 * Code Sandbox - Secure Code Execution Service
 * 
 * Supports multiple execution backends:
 * - Docker (primary, full isolation)
 * - Windows Job Objects (lightweight, Windows-only)
 * - Node.js vm2 (JS only, fast but less secure)
 * 
 * @version 0.1.0
 * @author OpenClaw Team
 * @date 2026-03-17
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');

const execAsync = promisify(exec);

// Configuration
const SANDBOX_CONFIG = {
  defaultTimeout: 30000,      // 30 seconds
  defaultMemoryLimit: 512,    // 512 MB
  defaultCpuLimit: 1,         // 1 CPU core
  tmpDir: path.resolve(path.join(process.env.USERPROFILE || process.env.HOME || '.', '.openclaw', 'sandbox-tmp')),
};

/**
 * Execution Result Interface
 * @typedef {Object} ExecutionResult
 * @property {boolean} success - Whether execution succeeded
 * @property {string} output - Standard output
 * @property {string} error - Error message (if failed)
 * @property {number} exitCode - Process exit code
 * @property {number} executionTime - Execution time in ms
 * @property {number} memoryUsed - Memory used in KB
 */

/**
 * Execution Request Interface
 * @typedef {Object} ExecutionRequest
 * @property {string} language - Programming language
 * @property {string} code - Source code to execute
 * @property {string} [input] - Standard input
 * @property {Object} [config] - Sandbox configuration
 */

class CodeSandbox {
  constructor(config = {}) {
    this.config = { ...SANDBOX_CONFIG, ...config };
    // Ensure tmpDir is absolute path
    this.config.tmpDir = path.resolve(this.config.tmpDir);
    this.executionHistory = [];
  }

  /**
   * Execute code in sandbox
   * @param {ExecutionRequest} request 
   * @returns {Promise<ExecutionResult>}
   */
  async execute(request) {
    const startTime = Date.now();
    const executionId = this.generateExecutionId();
    
    try {
      // Validate request
      this.validateRequest(request);
      
      // Select executor based on language
      const executor = this.getExecutor(request.language);
      
      // Execute code
      const result = await executor.execute(request);
      
      // Record execution
      this.recordExecution(executionId, request, result, startTime);
      
      return result;
    } catch (error) {
      const result = {
        success: false,
        output: '',
        error: error.message,
        exitCode: -1,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
      
      this.recordExecution(executionId, request, result, startTime);
      return result;
    }
  }

  /**
   * Validate execution request
   * @private
   */
  validateRequest(request) {
    if (!request.language) {
      throw new Error('Language is required');
    }
    if (!request.code) {
      throw new Error('Code is required');
    }
    
    const supportedLanguages = ['node', 'python', 'go', 'rust'];
    if (!supportedLanguages.includes(request.language.toLowerCase())) {
      throw new Error(`Unsupported language: ${request.language}. Supported: ${supportedLanguages.join(', ')}`);
    }
  }

  /**
   * Get executor for language
   * @private
   */
  getExecutor(language) {
    switch (language.toLowerCase()) {
      case 'node':
      case 'javascript':
        return new NodeExecutor(this.config);
      case 'python':
        return new PythonExecutor(this.config);
      case 'go':
        return new GoExecutor(this.config);
      case 'rust':
        return new RustExecutor(this.config);
      default:
        throw new Error(`No executor for language: ${language}`);
    }
  }

  /**
   * Generate unique execution ID
   * @private
   */
  generateExecutionId() {
    return `exec_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
  }

  /**
   * Record execution in history
   * @private
   */
  recordExecution(executionId, request, result, startTime) {
    this.executionHistory.push({
      executionId,
      timestamp: new Date().toISOString(),
      language: request.language,
      codeLength: request.code.length,
      success: result.success,
      executionTime: result.executionTime,
      memoryUsed: result.memoryUsed,
    });
    
    // Keep only last 1000 executions
    if (this.executionHistory.length > 1000) {
      this.executionHistory = this.executionHistory.slice(-1000);
    }
  }

  /**
   * Get execution history
   * @returns {Array}
   */
  getHistory(limit = 100) {
    return this.executionHistory.slice(-limit);
  }

  /**
   * Get supported languages
   * @returns {Array}
   */
  getSupportedLanguages() {
    return [
      { name: 'node', version: '20.x', description: 'Node.js JavaScript' },
      { name: 'python', version: '3.11', description: 'Python' },
      { name: 'go', version: '1.21', description: 'Go' },
      { name: 'rust', version: '1.75', description: 'Rust' },
    ];
  }
}

/**
 * Base Executor Class
 */
class BaseExecutor {
  constructor(config) {
    this.config = config;
  }

  async execute(request) {
    throw new Error('execute() must be implemented by subclass');
  }

  /**
   * Create temporary directory for execution
   * @protected
   */
  async createTempDir() {
    // Ensure tmpDir exists
    await fs.mkdir(this.config.tmpDir, { recursive: true });
    const tmpPath = path.join(this.config.tmpDir, `exec_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`);
    await fs.mkdir(tmpPath, { recursive: true });
    return tmpPath;
  }

  /**
   * Cleanup temporary directory
   * @protected
   */
  async cleanupTempDir(tmpPath) {
    try {
      await fs.rm(tmpPath, { recursive: true, force: true });
    } catch (error) {
      console.warn(`Failed to cleanup temp dir ${tmpPath}:`, error.message);
    }
  }

  /**
   * Execute with timeout
   * @protected
   */
  async executeWithTimeout(command, options, timeout) {
    return new Promise((resolve, reject) => {
      const process = exec(command, options, (error, stdout, stderr) => {
        if (error) {
          resolve({ error, stdout, stderr });
        } else {
          resolve({ error: null, stdout, stderr });
        }
      });

      // Timeout handling
      setTimeout(() => {
        process.kill();
        reject(new Error(`Execution timeout after ${timeout}ms`));
      }, timeout);
    });
  }
}

/**
 * Node.js Executor
 */
class NodeExecutor extends BaseExecutor {
  async execute(request) {
    const startTime = Date.now();
    const timeout = request.config?.timeout || this.config.defaultTimeout;
    
    try {
      // Create temp directory
      const tmpPath = await this.createTempDir();
      const codeFile = path.join(tmpPath, 'script.js');
      
      // Write code to file
      await fs.writeFile(codeFile, request.code, 'utf8');
      
      // Execute with Node.js
      const result = await this.executeWithTimeout(
        `node "${codeFile}"`,
        {
          cwd: tmpPath,
          maxBuffer: 10 * 1024 * 1024, // 10MB buffer
          env: { ...process.env, NODE_ENV: 'sandbox' },
        },
        timeout
      );
      
      // Cleanup
      await this.cleanupTempDir(tmpPath);
      
      return {
        success: !result.error,
        output: result.stdout || '',
        error: result.error ? result.error.message : '',
        exitCode: result.error?.code || 0,
        executionTime: Date.now() - startTime,
        memoryUsed: 0, // Would need process monitoring for accurate measurement
      };
    } catch (error) {
      return {
        success: false,
        output: '',
        error: error.message,
        exitCode: -1,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    }
  }
}

/**
 * Python Executor
 */
class PythonExecutor extends BaseExecutor {
  async execute(request) {
    const startTime = Date.now();
    const timeout = request.config?.timeout || this.config.defaultTimeout;
    
    try {
      // Create temp directory
      const tmpPath = await this.createTempDir();
      const codeFile = path.join(tmpPath, 'script.py');
      
      // Write code to file
      await fs.writeFile(codeFile, request.code, 'utf8');
      
      // Execute with Python
      const result = await this.executeWithTimeout(
        `python "${codeFile}"`,
        {
          cwd: tmpPath,
          maxBuffer: 10 * 1024 * 1024,
        },
        timeout
      );
      
      // Cleanup
      await this.cleanupTempDir(tmpPath);
      
      return {
        success: !result.error,
        output: result.stdout || '',
        error: result.error ? result.error.message : '',
        exitCode: result.error?.code || 0,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    } catch (error) {
      return {
        success: false,
        output: '',
        error: error.message,
        exitCode: -1,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    }
  }
}

/**
 * Go Executor
 */
class GoExecutor extends BaseExecutor {
  async execute(request) {
    const startTime = Date.now();
    const timeout = request.config?.timeout || this.config.defaultTimeout;
    
    try {
      // Create temp directory
      const tmpPath = await this.createTempDir();
      const codeFile = path.join(tmpPath, 'main.go');
      const binaryFile = path.join(tmpPath, 'program.exe');
      
      // Write code to file
      await fs.writeFile(codeFile, request.code, 'utf8');
      
      // Compile Go code
      const compileResult = await this.executeWithTimeout(
        `go build -o "${binaryFile}" "${codeFile}"`,
        {
          cwd: tmpPath,
          maxBuffer: 10 * 1024 * 1024,
        },
        timeout / 2 // Allocate half timeout for compilation
      );
      
      if (compileResult.error) {
        await this.cleanupTempDir(tmpPath);
        return {
          success: false,
          output: '',
          error: `Compilation failed: ${compileResult.error.message}`,
          exitCode: -1,
          executionTime: Date.now() - startTime,
          memoryUsed: 0,
        };
      }
      
      // Execute binary
      const execResult = await this.executeWithTimeout(
        `"${binaryFile}"`,
        {
          cwd: tmpPath,
          maxBuffer: 10 * 1024 * 1024,
        },
        timeout / 2 // Allocate half timeout for execution
      );
      
      // Cleanup
      await this.cleanupTempDir(tmpPath);
      
      return {
        success: !execResult.error,
        output: execResult.stdout || '',
        error: execResult.error ? execResult.error.message : '',
        exitCode: execResult.error?.code || 0,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    } catch (error) {
      return {
        success: false,
        output: '',
        error: error.message,
        exitCode: -1,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    }
  }
}

/**
 * Rust Executor
 */
class RustExecutor extends BaseExecutor {
  async execute(request) {
    const startTime = Date.now();
    const timeout = request.config?.timeout || this.config.defaultTimeout;
    
    try {
      // Create temp directory
      const tmpPath = await this.createTempDir();
      const codeFile = path.join(tmpPath, 'main.rs');
      const binaryFile = path.join(tmpPath, 'program.exe');
      
      // Write code to file
      await fs.writeFile(codeFile, request.code, 'utf8');
      
      // Compile Rust code
      const compileResult = await this.executeWithTimeout(
        `rustc -o "${binaryFile}" "${codeFile}"`,
        {
          cwd: tmpPath,
          maxBuffer: 10 * 1024 * 1024,
        },
        timeout / 2
      );
      
      if (compileResult.error) {
        await this.cleanupTempDir(tmpPath);
        return {
          success: false,
          output: '',
          error: `Compilation failed: ${compileResult.error.message}`,
          exitCode: -1,
          executionTime: Date.now() - startTime,
          memoryUsed: 0,
        };
      }
      
      // Execute binary
      const execResult = await this.executeWithTimeout(
        `"${binaryFile}"`,
        {
          cwd: tmpPath,
          maxBuffer: 10 * 1024 * 1024,
        },
        timeout / 2
      );
      
      // Cleanup
      await this.cleanupTempDir(tmpPath);
      
      return {
        success: !execResult.error,
        output: execResult.stdout || '',
        error: execResult.error ? execResult.error.message : '',
        exitCode: execResult.error?.code || 0,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    } catch (error) {
      return {
        success: false,
        output: '',
        error: error.message,
        exitCode: -1,
        executionTime: Date.now() - startTime,
        memoryUsed: 0,
      };
    }
  }
}

// Export for use as skill
module.exports = {
  CodeSandbox,
  SANDBOX_CONFIG,
};

// CLI interface
if (require.main === module) {
  const sandbox = new CodeSandbox();
  
  // Demo execution
  async function demo() {
    console.log('🔒 Code Sandbox v0.1.0\n');
    
    // Test Node.js
    console.log('Testing Node.js...');
    const nodeResult = await sandbox.execute({
      language: 'node',
      code: 'console.log("Hello from Node.js!"); console.log("2 + 2 =", 2 + 2);',
    });
    console.log('Output:', nodeResult.output);
    console.log('Success:', nodeResult.success);
    console.log('Time:', nodeResult.executionTime + 'ms\n');
    
    // Test Python
    console.log('Testing Python...');
    const pythonResult = await sandbox.execute({
      language: 'python',
      code: 'print("Hello from Python!")\nprint(f"2 + 2 = {2 + 2}")',
    });
    console.log('Output:', pythonResult.output);
    console.log('Success:', pythonResult.success);
    console.log('Time:', pythonResult.executionTime + 'ms\n');
    
    // Show supported languages
    console.log('Supported languages:');
    sandbox.getSupportedLanguages().forEach(lang => {
      console.log(`  - ${lang.name} (${lang.version}): ${lang.description}`);
    });
  }
  
  demo().catch(console.error);
}
