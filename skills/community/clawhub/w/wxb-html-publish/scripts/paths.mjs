// 保留源码，仅改真实标签属性和CSS引用；script/textarea正文不作为HTML解析。
export function cssPaths(text, reference) {
  return text.replace(/\/\*[\s\S]*?\*\/|url\(\s*(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|([^)]*))\s*\)|@import\s+(["'])(.*?)\4/gi, (all,a,b,c,q,d) => {
    if (all.startsWith('/*')) return all;
    const value = d ?? a ?? b ?? c?.trim();
    if (value.includes('\\')) return all; // CSS转义保持原文，交给路径警告人工定位。
    const updated = reference(value);
    return updated === value ? all : d !== undefined ? `@import ${q}${updated}${q}` : `url("${updated}")`;
  });
}
export function htmlPaths(text, reference) {
  return text.replace(/<!--[\s\S]*?-->|<(script|style|textarea)\b((?:"[^"]*"|'[^']*'|[^'">])*)>([\s\S]*?)<\/\1\s*>|<(?:"[^"]*"|'[^']*'|[^'">])*>/gi, (all,rawTag,attrs,content) => {
    if (all.startsWith('<!--')) return all;
    const end = all.indexOf('>');
    const opening = rawTag ? `<${rawTag}${attrs}>` : all;
    const updated = opening.replace(/(\s)(src|href|xlink:href|poster|data|action|srcset|style)(\s*=\s*)(?:"([^"]*)"|'([^']*)'|([^\s>]+))/gi, (attr,space,name,eq,a,b,c) => {
      const value = a ?? b ?? c; const quote = a !== undefined ? '"' : b !== undefined ? "'" : '';
      let result;
      if (name.toLowerCase() === 'style') result = cssPaths(value, reference);
      else if (name.toLowerCase() === 'srcset') {
        // data URL内部有逗号，保持此类srcset原文，不错误分割。
        result = /data:/i.test(value) ? value : value.split(',').map(part => part.replace(/^(\s*)(\S+)/,(_,s,url)=>s+reference(url))).join(',');
      } else result = reference(value);
      return result === value ? attr : `${space}${name}${eq}${quote || '"'}${result}${quote || '"'}`;
    });
    if (!rawTag) return updated;
    const body = rawTag.toLowerCase() === 'style' ? cssPaths(content,reference) : content;
    return updated + body + all.slice(end + 1 + content.length);
  });
}
