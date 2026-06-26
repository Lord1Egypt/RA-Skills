const dataFormatter = {
  json: {
    format(jsonStr, indent = 2) {
      try {
        const obj = typeof jsonStr === 'string' ? JSON.parse(jsonStr) : jsonStr;
        return JSON.stringify(obj, null, indent);
      } catch (e) {
        throw new Error('Invalid JSON');
      }
    },

    minify(jsonStr) {
      try {
        const obj = typeof jsonStr === 'string' ? JSON.parse(jsonStr) : jsonStr;
        return JSON.stringify(obj);
      } catch (e) {
        throw new Error('Invalid JSON');
      }
    },

    validate(jsonStr) {
      try {
        JSON.parse(jsonStr);
        return true;
      } catch (e) {
        return false;
      }
    }
  },

  base64: {
    encode(str) {
      return Buffer.from(str).toString('base64');
    },

    decode(base64Str) {
      return Buffer.from(base64Str, 'base64').toString('utf-8');
    }
  },

  yaml: {
    toJson(yamlStr) {
      const lines = yamlStr.split('\n');
      const result = {};
      let current = result;
      const stack = [{ obj: result, indent: -1 }];

      for (const line of lines) {
        if (!line.trim() || line.trim().startsWith('#')) continue;

        const indent = line.search(/\S/);
        const content = line.trim();

        while (stack.length > 1 && stack[stack.length - 1].indent >= indent) {
          stack.pop();
        }
        current = stack[stack.length - 1].obj;

        if (content.includes(':')) {
          const [key, ...valueParts] = content.split(':');
          const value = valueParts.join(':').trim();

          if (value === '' || value === '-') {
            const newObj = {};
            current[key.trim()] = newObj;
            stack.push({ obj: newObj, indent });
          } else if (value.startsWith('-')) {
            current[key.trim()] = [value.substring(1).trim()];
          } else {
            let parsedValue = value;
            if (value === 'true') parsedValue = true;
            else if (value === 'false') parsedValue = false;
            else if (!isNaN(value) && value !== '') parsedValue = Number(value);
            current[key.trim()] = parsedValue;
          }
        } else if (content.startsWith('-')) {
          const arrKey = Object.keys(current).find(k => Array.isArray(current[k]));
          if (arrKey) {
            current[arrKey].push(content.substring(1).trim());
          }
        }
      }
      return JSON.stringify(result, null, 2);
    },

    fromJson(jsonStr) {
      const obj = typeof jsonStr === 'string' ? JSON.parse(jsonStr) : jsonStr;
      return this.objectToYaml(obj, 0);
    },

    objectToYaml(obj, indent) {
      let result = '';
      const spaces = '  '.repeat(indent);

      for (const [key, value] of Object.entries(obj)) {
        if (Array.isArray(value)) {
          result += `${spaces}${key}:\n`;
          for (const item of value) {
            result += `${spaces}  - ${item}\n`;
          }
        } else if (typeof value === 'object' && value !== null) {
          result += `${spaces}${key}:\n`;
          result += this.objectToYaml(value, indent + 1);
        } else {
          result += `${spaces}${key}: ${value}\n`;
        }
      }
      return result;
    }
  }
};

export default dataFormatter;
