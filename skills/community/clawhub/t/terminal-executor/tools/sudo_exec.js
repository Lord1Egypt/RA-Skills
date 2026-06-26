const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

module.exports = async (command, options = {}) => {
try {
const fullCommand = `sudo ${command}`;
const { stdout, stderr } = await execAsync(fullCommand, {
cwd: options.cwd || process.cwd(),
env: { ...process.env, ...options.env },
timeout: options.timeout || 60000
});

return {
success: true,
stdout: stdout.trim(),
stderr: stderr.trim(),
command: fullCommand
};
} catch (error) {
return {
success: false,
error: error.message,
stdout: error.stdout?.trim() || '',
stderr: error.stderr?.trim() || '',
command
};
}
};
