const uuidGenerator = {
  v4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  },

  v1() {
    let d = new Date().getTime();
    if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
      d += performance.now();
    }
    return 'xxxxxxxx-xxxx-1xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = (d + Math.random() * 16) % 16 | 0;
      d = Math.floor(d / 16);
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  },

  v5(namespace, name) {
    const hash = this.simpleHash(namespace + name);
    let uuid = '';
    for (let i = 0; i < 36; i++) {
      if (i === 8 || i === 13 || i === 18 || i === 23) {
        uuid += '-';
      } else if (i === 14) {
        uuid += '5';
      } else if (i === 19) {
        uuid += '8';
      } else {
        uuid += (hash.charCodeAt(i % hash.length) % 16).toString(16);
      }
    }
    return uuid;
  },

  simpleHash(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash).toString(16).repeat(10);
  },

  generate(count = 1, version = 'v4') {
    const uuids = [];
    for (let i = 0; i < count; i++) {
      if (version === 'v1') uuids.push(this.v1());
      else if (version === 'v5') uuids.push(this.v5('ns:URL', 'name' + i));
      else uuids.push(this.v4());
    }
    return uuids;
  },

  validate(uuid) {
    const regex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return regex.test(uuid);
  }
};

export default uuidGenerator;
