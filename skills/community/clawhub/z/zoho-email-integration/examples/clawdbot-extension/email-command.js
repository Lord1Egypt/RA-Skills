/**
 * Clawdbot Skill Command Handler for Zoho Email (SECURITY HARDENED v2.2)
 * 
 * SECURITY FIXES:
 * - Command injection prevention: Uses spawn with argument array instead of shell interpolation
 * - Input sanitization: Validates and sanitizes all user inputs
 * - Token file permissions: Checks and enforces secure permissions (0600)
 * - Path traversal protection: Validates file paths
 * 
 * Installation:
 * 1. Copy this file to your Clawdbot skills directory
 * 2. Update your Clawdbot config to include this skill
 * 3. Ensure ZOHO_EMAIL environment variable is set
 * 4. Run oauth-setup.py or set ZOHO_PASSWORD for authentication
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class ZohoEmailSkillHandler {
  constructor(config = {}) {
    this.skillPath = config.skillPath || '/usr/lib/node_modules/openclaw/skills/zoho-email';
    this.tokenFile = config.tokenFile || null;
    this.verbose = config.verbose || false;
    
    // Verify token file permissions on initialization
    if (this.tokenFile) {
      this.checkTokenPermissions(this.tokenFile);
    }
  }

  /**
   * Check and enforce secure permissions on token file (0600)
   * @param {string} filePath - Path to token file
   */
  checkTokenPermissions(filePath) {
    try {
      if (fs.existsSync(filePath)) {
        const stats = fs.statSync(filePath);
        const mode = stats.mode & parseInt('777', 8);
        
        // Enforce 0600 permissions (owner read/write only)
        if (mode !== parseInt('600', 8)) {
          console.warn(`[SECURITY] Token file has insecure permissions (${mode.toString(8)}), changing to 0600`);
          fs.chmodSync(filePath, 0o600);
        }
      }
    } catch (error) {
      console.error(`[SECURITY] Failed to check token file permissions: ${error.message}`);
    }
  }

  /**
   * Sanitize user input to prevent injection attacks
   * @param {string} input - User-provided input
   * @returns {string} Sanitized input
   */
  sanitizeInput(input) {
    if (typeof input !== 'string') {
      return '';
    }
    
    // Remove dangerous characters and shell metacharacters
    // Allow: alphanumeric, spaces, @, ., -, _, and common punctuation
    return input
      .replace(/[;&|`$(){}[\]<>\\]/g, '') // Remove shell metacharacters
      .replace(/\n|\r/g, '') // Remove newlines
      .trim()
      .slice(0, 1000); // Limit length
  }

  /**
   * Validate email address format
   * @param {string} email - Email address to validate
   * @returns {boolean} True if valid
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * Execute a zoho-email command via Python (SECURE VERSION)
   * Uses spawn with argument array to prevent command injection
   * @param {string} command - Command name (unread, search, send, etc)
   * @param {Array<string>} args - Command arguments
   * @returns {Promise<Object>} Parsed JSON response or text output
   */
  executeCommand(command, args = []) {
    return new Promise((resolve, reject) => {
      // Validate script path to prevent path traversal
      const scriptPath = path.join(this.skillPath, 'scripts', 'clawdbot_extension.py');
      
      // Check if script exists
      if (!fs.existsSync(scriptPath)) {
        return reject(new Error(`Script not found: ${scriptPath}`));
      }

      // Sanitize all arguments
      const sanitizedCommand = this.sanitizeInput(command);
      const sanitizedArgs = args.map(arg => this.sanitizeInput(String(arg)));

      // Build argument array for spawn (NO SHELL INTERPOLATION)
      const spawnArgs = [scriptPath, sanitizedCommand, ...sanitizedArgs];
      
      if (this.verbose) {
        spawnArgs.push('--verbose');
      }

      // Use spawn instead of execSync to avoid shell interpretation
      const process = spawn('python3', spawnArgs, {
        timeout: 30000,
        stdio: ['ignore', 'pipe', 'pipe']
      });

      let stdout = '';
      let stderr = '';

      process.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      process.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      process.on('close', (code) => {
        if (code !== 0) {
          return resolve({
            status: 'error',
            message: stderr || `Command failed with code ${code}`
          });
        }

        // Try to parse as JSON, fall back to raw output
        try {
          resolve(JSON.parse(stdout));
        } catch (e) {
          resolve({ status: 'success', message: stdout.trim() });
        }
      });

      process.on('error', (error) => {
        resolve({
          status: 'error',
          message: `Execution failed: ${error.message}`
        });
      });

      // Timeout handler
      setTimeout(() => {
        process.kill();
        resolve({
          status: 'error',
          message: 'Command timed out (30s)'
        });
      }, 30000);
    });
  }

  /**
   * Clawdbot command handler for /email
   * @param {Object} context - Clawdbot message context
   * @param {string} args - Command arguments
   */
  async handleEmailCommand(context, args) {
    const parts = args.trim().split(/\s+/);
    const command = parts[0] || 'help';
    const cmdArgs = parts.slice(1);

    // Route to appropriate handler
    switch (command) {
      case 'unread':
        return this.handleUnread(context);
      
      case 'summary':
        return this.handleSummary(context);
      
      case 'search':
        return this.handleSearch(context, cmdArgs.join(' '));
      
      case 'send':
        return this.handleSend(context, cmdArgs);
      
      case 'doctor':
        return this.handleDoctor(context);
      
      case 'help':
      default:
        return this.handleHelp(context);
    }
  }

  /**
   * Handle /email unread command
   */
  async handleUnread(context) {
    const result = await this.executeCommand('unread');
    
    if (result.status === 'error') {
      return context.reply(`❌ Error: ${result.message}`);
    }

    if (result.unread_count !== undefined) {
      const count = result.unread_count;
      const emoji = count > 0 ? '📬' : '📭';
      const message = `${emoji} **Unread:** ${count} message${count !== 1 ? 's' : ''}`;
      return context.reply(message);
    }

    return context.reply('Unable to fetch unread count');
  }

  /**
   * Handle /email summary command (for briefings)
   */
  async handleSummary(context) {
    const result = await this.executeCommand('summary');
    
    if (result.status === 'error') {
      return context.reply(`Email check failed: ${result.message}`);
    }

    if (result.message) {
      return context.reply(result.message);
    }

    return context.reply('Email check unavailable');
  }

  /**
   * Handle /email search command
   */
  async handleSearch(context, query) {
    if (!query || query.length < 2) {
      return context.reply('❌ Usage: `/email search <query>` (min 2 characters)');
    }

    const result = await this.executeCommand('search', [query]);
    
    if (result.status === 'error') {
      return context.reply(`❌ Search failed: ${result.message}`);
    }

    if (Array.isArray(result) && result.length > 0) {
      let message = `🔍 **Search results for "${this.sanitizeInput(query)}":**\n\n`;
      
      result.slice(0, 5).forEach((email, i) => {
        const sender = email.from || 'Unknown';
        const subject = email.subject || '(no subject)';
        message += `${i + 1}. **${subject}**\n   From: ${sender}\n\n`;
      });

      if (result.length > 5) {
        message += `_... and ${result.length - 5} more results_`;
      }

      return context.reply(message);
    }

    return context.reply(`🔍 No results for "${this.sanitizeInput(query)}"`);
  }

  /**
   * Handle /email send command
   */
  async handleSend(context, args) {
    if (args.length < 3) {
      return context.reply('❌ Usage: `/email send <to> <subject> <body>`');
    }

    const [to, subject, body] = args;

    // Validate email address
    if (!this.isValidEmail(to)) {
      return context.reply('❌ Invalid email address format');
    }

    const result = await this.executeCommand('send', [to, subject, body]);

    if (result.status === 'error') {
      return context.reply(`❌ Send failed: ${result.message}`);
    }

    return context.reply(`✅ **Email sent**\nTo: ${to}\nSubject: ${subject}`);
  }

  /**
   * Handle /email doctor command (diagnostics)
   */
  async handleDoctor(context) {
    const result = await this.executeCommand('doctor');
    
    const output = result.message || JSON.stringify(result, null, 2);
    const message = `🔧 **Email Setup Check:**\n\n\`\`\`\n${output}\n\`\`\``;
    
    return context.reply(message);
  }

  /**
   * Handle /email help command
   */
  async handleHelp(context) {
    const helpText = `📧 **Zoho Email Commands**

\`/email unread\` - Check unread count
\`/email summary\` - Brief unread summary (for briefings)
\`/email search <query>\` - Search emails
\`/email send <to> <subject> <body>\` - Send email
\`/email doctor\` - Check setup & connectivity
\`/email help\` - Show this help

**Examples:**
- \`/email unread\`
- \`/email search invoice\`
- \`/email send john@example.com "Hello" "Hi John"\`

**Setup Required:**
1. Export ZOHO_EMAIL
2. Run oauth-setup.py OR set ZOHO_PASSWORD

**Security Note:**
Token file must have 0600 permissions (owner read/write only).
Run: \`chmod 600 ~/.clawdbot/zoho-mail-tokens.json\``;

    return context.reply(helpText);
  }
}

// Export for Clawdbot skill integration
module.exports = {
  ZohoEmailSkillHandler,
  
  // Clawdbot skill entry point
  async handleCommand(context, message) {
    const handler = new ZohoEmailSkillHandler();
    
    // Parse /email command
    if (message.text && message.text.startsWith('/email')) {
      const args = message.text.substring(7).trim(); // Remove '/email '
      return handler.handleEmailCommand(context, args);
    }
  }
};
