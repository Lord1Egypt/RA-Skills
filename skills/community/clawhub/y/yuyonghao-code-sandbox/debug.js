const { CodeSandbox } = require('./src/sandbox');

async function debug() {
  const sandbox = new CodeSandbox({
    tmpDir: './test-tmp',
  });
  
  console.log('Testing Node.js execution...\n');
  
  const result = await sandbox.execute({
    language: 'node',
    code: 'console.log("Hello World!"); console.log("2 + 2 =", 2 + 2);',
  });
  
  console.log('Result:', JSON.stringify(result, null, 2));
}

debug().catch(console.error);
