module.exports = {
name: 'terminal-executor',
version: '1.0.0',
description: 'Execute terminal commands with sudo support',
tools: {
exec: require('./tools/exec'),
sudo_exec: require('./tools/sudo_exec')
}
};
