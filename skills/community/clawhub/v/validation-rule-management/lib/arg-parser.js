/**
 * 命令行参数解析器
 * 支持：--key value | --key=value | --json '{...}'
 */
function parseArgs(argv) {
  const args = argv.slice(2);
  const action = args[0];
  const params = {};

  // --json '整体JSON' 快捷方式
  const jsonIdx = args.indexOf('--json');
  if (jsonIdx !== -1 && args[jsonIdx + 1]) {
    try {
      return { action, params: JSON.parse(args[jsonIdx + 1]) };
    } catch (e) {
      throw new Error(`--json 解析失败：${e.message}`);
    }
  }

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) continue;

    const eqIdx = arg.indexOf('=');
    if (eqIdx !== -1) {
      // --key=value
      params[arg.slice(2, eqIdx)] = arg.slice(eqIdx + 1);
    } else {
      // --key value
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        params[key] = next;
        i++;
      } else {
        params[key] = true;
      }
    }
  }

  return { action, params };
}

module.exports = { parseArgs };
