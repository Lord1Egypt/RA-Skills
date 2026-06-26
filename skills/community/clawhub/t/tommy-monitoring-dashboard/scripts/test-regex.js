const { execSync } = require('child_process');

// Test memory parsing
const memOutput = "PhysMem: 16G used (3318M wired, 1092M compressor), 469M unused.\n";
console.log('Memory test:');
console.log('Input:', JSON.stringify(memOutput));

const memMatch = memOutput.match(/PhysMem: (\d+)G used.*?(\d+)M unused/);
console.log('Match result:', memMatch);

if (memMatch) {
    const used = parseInt(memMatch[1]);
    const unusedMB = parseInt(memMatch[2]); 
    console.log('Parsed:', { used, unusedMB });
}

// Test CPU parsing
const cpuOutput = "CPU usage: 2.91% user, 10.87% sys, 86.21% idle \n";
console.log('\nCPU test:');
console.log('Input:', JSON.stringify(cpuOutput));

const cpuMatch = cpuOutput.match(/CPU usage: ([\d.]+)% user, ([\d.]+)% sys/);
console.log('Match result:', cpuMatch);

if (cpuMatch) {
    const user = parseFloat(cpuMatch[1]);
    const sys = parseFloat(cpuMatch[2]);
    console.log('Parsed:', { user, sys, total: user + sys });
}
