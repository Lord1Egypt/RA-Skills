const { exec } = require('child_process');

module.exports = async function(input, context){
  const cmd = context.message.slice(3).trim();
  if(!cmd) return '❌ No command.';
  const res = await new Promise((resolve, reject)=>{
    exec(cmd, (err, out)=>{err?reject(err):resolve(out)});
  });
  return res.trim();
}