/**
 * Code Mode 转换层 - MCP 工具 → 代码函数
 * 
 * 基于 Cloudflare 提出的 "Code Mode" 概念：
 * - 将 MCP 工具调用转换为可执行代码
 * - 减少 LLM token 消耗（相比纯文本调用）
 * - 支持 JavaScript/PowerShell 沙箱执行
 * 
 * @version 0.1.0
 * @author 小蒲萄 (Clawd)
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * MCP 工具到代码的转换器
 */
class CodeModeConverter {
  constructor(options = {}) {
    this.options = {
      // 默认语言
      defaultLanguage: options.defaultLanguage || 'javascript',
      // 沙箱配置
      sandbox: {
        timeout: options.sandboxTimeout || 10000,
        maxOutputSize: options.maxOutputSize || 10 * 1024 * 1024, // 10MB
      },
      // 工具模板注册表
      toolTemplates: new Map(),
    };

    // 注册内置工具模板
    this._registerBuiltInTemplates();
  }

  /**
   * 注册内置工具模板
   */
  _registerBuiltInTemplates() {
    // Tavily Search
    this.registerTemplate('tavily-search', {
      javascript: (params) => `
const search = require('tavily-search');
const client = new search.TavilySearch({ apiKey: process.env.TAVILY_API_KEY });
const result = await client.search({
  query: ${this._toJson(params.query)},
  limit: ${params.limit || 5}
});
return JSON.stringify(result);
`.trim(),
      powershell: (params) => `
$headers = @{
  'Authorization' = 'Bearer $env:TAVILY_API_KEY'
  'Content-Type' = 'application/json'
}
$body = @{
  query = ${this._toJson(params.query)}
  limit = ${params.limit || 5}
} | ConvertTo-Json
Invoke-RestMethod -Uri 'https://api.tavily.com/search' -Method Post -Headers $headers -Body $body
`.trim(),
    });

    // Calculator
    this.registerTemplate('calculator', {
      javascript: (params) => `
const a = ${params.a || 0};
const b = ${params.b || 0};
const op = '${params.op || 'add'}';
let result;
switch (op) {
  case 'add': result = a + b; break;
  case 'sub': result = a - b; break;
  case 'mul': result = a * b; break;
  case 'div': result = a / b; break;
  default: throw new Error('Unknown operation: ' + op);
}
return result;
`.trim(),
      powershell: (params) => `
$a = ${params.a || 0}
$b = ${params.b || 0}
$op = '${params.op || 'add'}'
switch ($op) {
  'add' { $a + $b }
  'sub' { $a - $b }
  'mul' { $a * $b }
  'div' { $a / $b }
  default { throw "Unknown operation: $op" }
}
`.trim(),
    });

    // File Read
    this.registerTemplate('file-read', {
      javascript: (params) => `
const fs = require('fs');
const path = require('path');
const filePath = path.resolve(${this._toJson(params.path)});
const content = fs.readFileSync(filePath, 'utf8');
return content;
`.trim(),
      powershell: (params) => `
Get-Content -Path ${this._toJson(params.path)} -Raw
`.trim(),
    });

    // File Write
    this.registerTemplate('file-write', {
      javascript: (params) => `
const fs = require('fs');
const path = require('path');
const filePath = path.resolve(${this._toJson(params.path)});
fs.writeFileSync(filePath, ${this._toJson(params.content)});
return 'File written successfully';
`.trim(),
      powershell: (params) => `
${this._toJson(params.content)} | Set-Content -Path ${this._toJson(params.path)}
'File written successfully'
`.trim(),
    });

    // Directory List
    this.registerTemplate('directory-list', {
      javascript: (params) => `
const fs = require('fs');
const path = require('path');
const dirPath = path.resolve(${this._toJson(params.path || '.')});
const files = fs.readdirSync(dirPath, { withFileTypes: true });
return files.map(f => ({ name: f.name, isDirectory: f.isDirectory() }));
`.trim(),
      powershell: (params) => `
Get-ChildItem -Path ${this._toJson(params.path || '.')} | Select-Object Name, @{Name='IsDirectory';Expression={$_.PSIsContainer}} | ConvertTo-Json
`.trim(),
    });
  }

  /**
   * 注册工具模板
   * @param {string} toolName - 工具名称
   * @param {Object} templates - 语言 → 模板函数映射
   */
  registerTemplate(toolName, templates) {
    this.options.toolTemplates.set(toolName, templates);
  }

  /**
   * 将 MCP 工具调用转换为代码
   * @param {string} toolName - 工具名称
   * @param {Object} params - 工具参数
   * @param {string} language - 目标语言 (javascript|powershell)
   * @returns {string} 生成的代码
   */
  convert(toolName, params, language = 'javascript') {
    const template = this.options.toolTemplates.get(toolName);
    
    if (!template) {
      throw new Error(`未知工具：${toolName}。请先注册工具模板。`);
    }

    const codeFn = template[language];
    if (!codeFn) {
      throw new Error(`不支持的语言：${language}。可用语言：${Object.keys(template).join(', ')}`);
    }

    return codeFn(params);
  }

  /**
   * 执行生成的代码（沙箱环境）
   * @param {string} code - 代码字符串
   * @param {string} language - 语言
   * @param {Object} options - 执行选项
   * @returns {Promise<{success: boolean, output?: string, error?: string, duration: number}>}
   */
  async execute(code, language = 'javascript', options = {}) {
    const startTime = Date.now();

    try {
      if (language === 'javascript') {
        return await this._executeJavaScript(code, options);
      } else if (language === 'powershell') {
        return await this._executePowerShell(code, options);
      } else {
        throw new Error(`不支持的语言：${language}`);
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
        duration: Date.now() - startTime,
      };
    }
  }

  /**
   * 执行 JavaScript 代码（Node.js 子进程）
   */
  async _executeJavaScript(code, options) {
    const startTime = Date.now();
    const timeout = options.timeout || this.options.sandbox.timeout;
    const tmpDir = require('os').tmpdir();
    const tmpFile = path.join(tmpDir, `code-mode-${Date.now()}.js`);

    // 包装代码（添加 async 支持）
    const wrappedCode = `
(async () => {
  try {
    const result = await (async () => {
      ${code}
    })();
    console.log('__RESULT_START__' + JSON.stringify(result) + '__RESULT_END__');
  } catch (error) {
    console.error('__ERROR_START__' + error.message + '__ERROR_END__');
    process.exit(1);
  }
})();
`.trim();

    // 写入临时文件
    fs.writeFileSync(tmpFile, wrappedCode);

    try {
      return await new Promise((resolve, reject) => {
        const child = spawn('node', [tmpFile], {
          stdio: ['pipe', 'pipe', 'pipe'],
          env: { ...process.env },
          timeout,
        });

        let output = '';
        let errorOutput = '';

        child.stdout.on('data', (data) => {
          output += data.toString();
        });

        child.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        child.on('close', (code) => {
          // 清理临时文件
          try { fs.unlinkSync(tmpFile); } catch (e) {}

          const duration = Date.now() - startTime;

          // 解析结果
          const resultMatch = output.match(/__RESULT_START__(.*?)__RESULT_END__/s);
          const errorMatch = errorOutput.match(/__ERROR_START__(.*?)__ERROR_END__/s);

          if (resultMatch) {
            try {
              const result = JSON.parse(resultMatch[1]);
              resolve({
                success: true,
                output: typeof result === 'string' ? result : JSON.stringify(result),
                duration,
              });
            } catch (e) {
              resolve({
                success: true,
                output: resultMatch[1],
                duration,
              });
            }
          } else if (errorMatch || code !== 0) {
            resolve({
              success: false,
              error: errorMatch ? errorMatch[1] : `Exit code: ${code}`,
              duration,
            });
          } else {
            resolve({
              success: true,
              output: output.trim(),
              duration,
            });
          }
        });

        child.on('error', (err) => {
          try { fs.unlinkSync(tmpFile); } catch (e) {}
          reject(err);
        });
      });
    } catch (error) {
      // 清理临时文件
      try { fs.unlinkSync(tmpFile); } catch (e) {}
      throw error;
    }
  }

  /**
   * 执行 PowerShell 代码
   */
  async _executePowerShell(code, options) {
    const startTime = Date.now();
    const timeout = options.timeout || this.options.sandbox.timeout;
    const tmpDir = require('os').tmpdir();
    const tmpFile = path.join(tmpDir, `code-mode-${Date.now()}.ps1`);

    // 包装代码（添加错误处理）
    const wrappedCode = `
$ErrorActionPreference = 'Stop'
try {
  $result = & {
    ${code}
  }
  if ($result -ne $null) {
    Write-Output "__RESULT_START__"
    Write-Output ($result | ConvertTo-Json -Depth 10)
    Write-Output "__RESULT_END__"
  }
} catch {
  Write-Error "__ERROR_START__$($_.Exception.Message)__ERROR_END__"
  exit 1
}
`.trim();

    // 写入临时文件
    fs.writeFileSync(tmpFile, wrappedCode, 'utf8');

    try {
      return await new Promise((resolve, reject) => {
        const child = spawn('powershell.exe', [
          '-NoProfile',
          '-ExecutionPolicy', 'Bypass',
          '-File', tmpFile
        ], {
          stdio: ['pipe', 'pipe', 'pipe'],
          timeout,
        });

        let output = '';
        let errorOutput = '';

        child.stdout.on('data', (data) => {
          output += data.toString();
        });

        child.stderr.on('data', (data) => {
          errorOutput += data.toString();
        });

        child.on('close', (code) => {
          // 清理临时文件
          try { fs.unlinkSync(tmpFile); } catch (e) {}

          const duration = Date.now() - startTime;

          // 解析结果
          const resultMatch = output.match(/__RESULT_START__([\s\S]*?)__RESULT_END__/);
          const errorMatch = errorOutput.match(/__ERROR_START__(.*?)__ERROR_END__/s);

          if (resultMatch) {
            try {
              const result = JSON.parse(resultMatch[1]);
              resolve({
                success: true,
                output: typeof result === 'string' ? result : JSON.stringify(result),
                duration,
              });
            } catch (e) {
              resolve({
                success: true,
                output: resultMatch[1].trim(),
                duration,
              });
            }
          } else if (errorMatch || code !== 0) {
            resolve({
              success: false,
              error: errorMatch ? errorMatch[1] : `Exit code: ${code}`,
              duration,
            });
          } else {
            resolve({
              success: true,
              output: output.trim(),
              duration,
            });
          }
        });

        child.on('error', (err) => {
          try { fs.unlinkSync(tmpFile); } catch (e) {}
          reject(err);
        });
      });
    } catch (error) {
      // 清理临时文件
      try { fs.unlinkSync(tmpFile); } catch (e) {}
      throw error;
    }
  }

  /**
   * JSON 字符串化辅助函数
   */
  _toJson(value) {
    return JSON.stringify(value);
  }

  /**
   * 获取已注册的工具列表
   */
  getRegisteredTools() {
    return Array.from(this.options.toolTemplates.keys());
  }

  /**
   * 估算 Token 消耗（对比传统方式 vs Code Mode）
   * @param {string} toolName - 工具名称
   * @param {Object} params - 参数
   * @returns {{traditional: number, codeMode: number, saved: number, percentage: number}}
   */
  estimateTokenSavings(toolName, params) {
    // 传统方式：工具调用描述 + 参数
    const traditionalTokens = JSON.stringify({ tool: toolName, params }).length / 4;

    // Code Mode：生成的代码
    const code = this.convert(toolName, params, 'javascript');
    const codeModeTokens = code.length / 4;

    // 节省
    const saved = traditionalTokens - codeModeTokens;
    const percentage = ((saved / traditionalTokens) * 100).toFixed(1);

    return {
      traditional: Math.round(traditionalTokens),
      codeMode: Math.round(codeModeTokens),
      saved: Math.round(saved),
      percentage: parseFloat(percentage),
    };
  }
}

// 导出
module.exports = { CodeModeConverter };
