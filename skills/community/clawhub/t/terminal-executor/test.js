const exec = require('./tools/exec');
const sudo_exec = require('./tools/sudo_exec');

async function test() {
  console.log("Testing exec...");
  const result1 = await exec("ls -la");
  console.log(result1);
  
  console.log("\nTesting sudo_exec...");
  const result2 = await sudo_exec("apt update");
  console.log(result2);
}

test();
