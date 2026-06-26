#!/usr/bin/env node

const { execSync } = require('child_process');

console.log('=== MEMORY TEST ===');
try {
    const mem = execSync('top -l 1 -n 0 | grep PhysMem', { encoding: 'utf8' });
    console.log('Raw memory output:', JSON.stringify(mem));
    console.log('Memory output:', mem);
} catch (e) {
    console.log('Memory error:', e.message);
}

console.log('\\n=== CPU TEST ===');  
try {
    const cpu = execSync('top -l 1 -n 0 | grep "CPU usage"', { encoding: 'utf8' });
    console.log('Raw CPU output:', JSON.stringify(cpu));
    console.log('CPU output:', cpu);
} catch (e) {
    console.log('CPU error:', e.message);
}

console.log('\\n=== DISK TEST ===');
try {
    const disk = execSync('df -h / | tail -1', { encoding: 'utf8' });
    console.log('Raw disk output:', JSON.stringify(disk));  
    console.log('Disk output:', disk);
    console.log('Split test:', disk.trim().split(/\\s+/));
} catch (e) {
    console.log('Disk error:', e.message);
}

console.log('\\n=== UPTIME TEST ===');
try {
    const uptime = execSync('uptime', { encoding: 'utf8' });
    console.log('Raw uptime output:', JSON.stringify(uptime));
    console.log('Uptime output:', uptime);
} catch (e) {
    console.log('Uptime error:', e.message);
}
