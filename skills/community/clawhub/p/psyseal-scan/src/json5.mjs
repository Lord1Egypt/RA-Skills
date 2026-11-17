// Parser JSON5 mínimo y sin dependencias (solo lectura).
// Cubre lo que usa openclaw.json: comentarios, comas finales, claves sin comillas,
// comillas simples, números hexadecimales/con signo, Infinity/NaN.
// No ejecuta nada (no usa eval ni Function) y no contamina prototipos.

const WS = new Set([' ', '\t', '\n', '\r', '\v', '\f', '\u00a0', '\u2028', '\u2029', '\ufeff']);
const MAX_DEPTH = 64;

export class Json5Error extends Error {
  constructor(message, line, col) {
    super(`${message} (línea ${line}, columna ${col})`);
    this.name = 'Json5Error';
    this.line = line;
    this.col = col;
  }
}

function isIdStart(ch) {
  return /[\p{L}\p{Nl}$_]/u.test(ch);
}
function isIdPart(ch) {
  return /[\p{L}\p{Nl}\p{Mn}\p{Mc}\p{Nd}\p{Pc}$_\u200c\u200d]/u.test(ch);
}

function setOwn(obj, key, value) {
  Object.defineProperty(obj, key, { value, enumerable: true, writable: true, configurable: true });
}

export function parse(text) {
  if (typeof text !== 'string') throw new TypeError('parse espera un string');
  let i = 0;
  const n = text.length;

  function fail(msg, at = i) {
    let line = 1;
    let col = 1;
    for (let k = 0; k < at && k < n; k++) {
      if (text[k] === '\n') {
        line++;
        col = 1;
      } else col++;
    }
    throw new Json5Error(msg, line, col);
  }

  function skip() {
    for (;;) {
      const ch = text[i];
      if (ch === undefined) return;
      if (WS.has(ch)) {
        i++;
      } else if (ch === '/' && text[i + 1] === '/') {
        i += 2;
        while (i < n && text[i] !== '\n' && text[i] !== '\r' && text[i] !== '\u2028' && text[i] !== '\u2029') i++;
      } else if (ch === '/' && text[i + 1] === '*') {
        const end = text.indexOf('*/', i + 2);
        if (end === -1) fail('Comentario sin cerrar');
        i = end + 2;
      } else return;
    }
  }

  function parseValue(depth) {
    if (depth > MAX_DEPTH) fail('Anidamiento demasiado profundo');
    skip();
    const ch = text[i];
    if (ch === undefined) fail('Fin inesperado del texto');
    if (ch === '{') return parseObject(depth);
    if (ch === '[') return parseArray(depth);
    if (ch === '"' || ch === "'") return parseString();
    if (ch === '-' || ch === '+' || ch === '.' || (ch >= '0' && ch <= '9')) return parseNumber();
    if (isIdStart(ch)) {
      const word = parseIdentifier();
      if (word === 'true') return true;
      if (word === 'false') return false;
      if (word === 'null') return null;
      if (word === 'Infinity') return Infinity;
      if (word === 'NaN') return NaN;
      // No se repite el texto encontrado: podría ser una credencial pegada sin comillas.
      fail('Valor no reconocido', i - word.length);
    }
    fail('Carácter inesperado');
  }

  function parseIdentifier() {
    const start = i;
    if (!isIdStart(text[i])) fail('Identificador inválido');
    i++;
    while (i < n && isIdPart(text[i])) i++;
    return text.slice(start, i);
  }

  function parseNumber() {
    const start = i;
    let sign = 1;
    if (text[i] === '-' || text[i] === '+') {
      if (text[i] === '-') sign = -1;
      i++;
    }
    if (text.startsWith('Infinity', i)) {
      i += 8;
      return sign * Infinity;
    }
    if (text.startsWith('NaN', i)) {
      i += 3;
      return NaN;
    }
    if (text[i] === '0' && (text[i + 1] === 'x' || text[i + 1] === 'X')) {
      i += 2;
      const hs = i;
      while (i < n && /[0-9a-fA-F]/.test(text[i])) i++;
      if (i === hs) fail('Hexadecimal vacío', start);
      return sign * parseInt(text.slice(hs, i), 16);
    }
    const m = /^(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?/.exec(text.slice(i, i + 64));
    if (!m) fail('Número inválido', start);
    i += m[0].length;
    return sign * Number(m[0]);
  }

  function parseString() {
    const quote = text[i];
    const start = i;
    i++;
    let out = '';
    for (;;) {
      if (i >= n) fail('Texto sin cerrar', start);
      const ch = text[i];
      if (ch === quote) {
        i++;
        return out;
      }
      if (ch === '\n' || ch === '\r') fail('Salto de línea dentro de un texto', i);
      if (ch !== '\\') {
        out += ch;
        i++;
        continue;
      }
      i++;
      const esc = text[i];
      if (esc === undefined) fail('Escape incompleto', start);
      i++;
      switch (esc) {
        case 'n': out += '\n'; break;
        case 'r': out += '\r'; break;
        case 't': out += '\t'; break;
        case 'b': out += '\b'; break;
        case 'f': out += '\f'; break;
        case 'v': out += '\v'; break;
        case '0': out += '\0'; break;
        case 'x': {
          const h = text.slice(i, i + 2);
          if (!/^[0-9a-fA-F]{2}$/.test(h)) fail('Escape \\x inválido', i);
          out += String.fromCharCode(parseInt(h, 16));
          i += 2;
          break;
        }
        case 'u': {
          const h = text.slice(i, i + 4);
          if (!/^[0-9a-fA-F]{4}$/.test(h)) fail('Escape \\u inválido', i);
          out += String.fromCharCode(parseInt(h, 16));
          i += 4;
          break;
        }
        case '\r':
          if (text[i] === '\n') i++;
          break;
        case '\n':
        case '\u2028':
        case '\u2029':
          break;
        default:
          out += esc;
      }
    }
  }

  function parseObject(depth) {
    const obj = {};
    i++; // {
    for (;;) {
      skip();
      if (text[i] === '}') {
        i++;
        return obj;
      }
      let key;
      const ch = text[i];
      if (ch === '"' || ch === "'") key = parseString();
      else if (ch !== undefined && isIdStart(ch)) key = parseIdentifier();
      else fail('Se esperaba una clave');
      skip();
      if (text[i] !== ':') fail('Se esperaba ":"');
      i++;
      setOwn(obj, key, parseValue(depth + 1));
      skip();
      if (text[i] === ',') {
        i++;
        continue;
      }
      if (text[i] === '}') {
        i++;
        return obj;
      }
      fail('Se esperaba "," o "}"');
    }
  }

  function parseArray(depth) {
    const arr = [];
    i++; // [
    for (;;) {
      skip();
      if (text[i] === ']') {
        i++;
        return arr;
      }
      arr.push(parseValue(depth + 1));
      skip();
      if (text[i] === ',') {
        i++;
        continue;
      }
      if (text[i] === ']') {
        i++;
        return arr;
      }
      fail('Se esperaba "," o "]"');
    }
  }

  const value = parseValue(0);
  skip();
  if (i < n) fail('Contenido extra después del valor');
  return value;
}
