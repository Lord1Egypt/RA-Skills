
const readline = require('readline');

// 创建readline接口
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// 对话映射
const responses = {
  '1': '你好呀',
  '2': '今天天气怎么样',
  '3': '很高兴认识你'
};

// 显示菜单
function showMenu() {
  console.log('\n=== 交互式对话系统 ===');
  console.log('1. 你好呀');
  console.log('2. 今天天气怎么样');
  console.log('3. 很高兴认识你');
  console.log('输入 q 退出程序');
  console.log('========================');
}

// 处理用户输入
function handleInput(input) {
  const choice = input.trim();
  
  if (choice === 'q' || choice === 'Q') {
    console.log('再见！');
    rl.close();
    return;
  }
  
  if (responses[choice]) {
    console.log(`系统回复: ${responses[choice]}`);
  } else {
    console.log('无效输入，请输入 1、2、3 或 q');
  }
  
  showMenu();
  rl.question('请选择 (1-3) 或输入 q 退出: ', handleInput);
}

// 启动程序
function main() {
  console.log('欢迎使用交互式对话系统！');
  showMenu();
  rl.question('请选择 (1-3) 或输入 q 退出: ', handleInput);
}

// 程序入口
if (require.main === module) {
  main();
}

module.exports = { main, handleInput, showMenu };
