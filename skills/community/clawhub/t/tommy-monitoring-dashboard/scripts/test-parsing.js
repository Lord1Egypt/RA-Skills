#!/usr/bin/env node

// Quick test of system parsing
const { execSync } = require('child_process');

console.log('Testing system info parsing...');

// Test memory
try {
    const topOutput = execSync('top -l 1 -n 0 | grep "PhysMem:"', { encoding: 'utf8', timeout: 5000 });
    console.log('PhysMem line:', topOutput.trim());
    
    const memMatch = topOutput.match(/PhysMem: ([\\d.]+)([GMK]) used.*?([\\d.]+)([GMK]) unused/);
    console.log('Memory match:', memMatch);
    
    if (memMatch) {
        const usedValue = parseFloat(memMatch[1]);
        const usedUnit = memMatch[2];
        const unusedValue = parseFloat(memMatch[3]);
        const unusedUnit = memMatch[4];
        
        console.log('Parsed:', { usedValue, usedUnit, unusedValue, unusedUnit });
        
        const usedGB = usedUnit === 'G' ? usedValue : usedUnit === 'M' ? usedValue / 1024 : usedValue / (1024 * 1024);
        const unusedGB = unusedUnit === 'G' ? unusedValue : unusedUnit === 'M' ? unusedValue / 1024 : unusedValue / (1024 * 1024);
        
        console.log('Memory result:', { 
            used: Math.round(usedGB), 
            unused: Math.round(unusedGB),
            total: Math.round(usedGB + unusedGB),
            percent: Math.round((usedGB / (usedGB + unusedGB)) * 100)
        });
    }
} catch (error) {
    console.error('Memory error:', error.message);
}

// Test CPU
try {
    const topOutput = execSync('top -l 1 -n 0 | grep "CPU usage:"', { encoding: 'utf8', timeout: 5000 });
    console.log('CPU line:', topOutput.trim());
    
    const cpuMatch = topOutput.match(/CPU usage: ([\\d.]+)% user, ([\\d.]+)% sys, ([\\d.]+)% idle/);
    console.log('CPU match:', cpuMatch);
    
    if (cpuMatch) {
        const user = parseFloat(cpuMatch[1]);
        const sys = parseFloat(cpuMatch[2]);
        const idle = parseFloat(cpuMatch[3]);
        
        console.log('CPU result:', { 
            user, sys, idle,
            percent: Math.round(user + sys)
        });
    }
} catch (error) {
    console.error('CPU error:', error.message);
}

// Test disk
try {
    const dfOutput = execSync('df -h / | tail -1', { encoding: 'utf8', timeout: 5000 });
    console.log('Disk line:', dfOutput.trim());
    
    const parts = dfOutput.trim().split(/\\s+/);
    console.log('Disk parts:', parts);
    
    if (parts.length >= 5) {
        const total = parts[1];
        const used = parts[2];
        const percentStr = parts[4];
        
        console.log('Disk result:', { total, used, percent: parseInt(percentStr) });
    }
} catch (error) {
    console.error('Disk error:', error.message);
}