const urlToolkit = {
  encode(url) {
    return encodeURIComponent(url);
  },

  decode(url) {
    return decodeURIComponent(url);
  },

  parse(url) {
    try {
      const urlObj = new URL(url);
      const params = {};
      urlObj.searchParams.forEach((value, key) => {
        params[key] = value;
      });
      return {
        protocol: urlObj.protocol,
        hostname: urlObj.hostname,
        port: urlObj.port,
        pathname: urlObj.pathname,
        search: urlObj.search,
        hash: urlObj.hash,
        params: params
      };
    } catch (e) {
      throw new Error('Invalid URL');
    }
  },

  buildParams(params) {
    const searchParams = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      searchParams.append(key, value);
    }
    return searchParams.toString();
  },

  validate(url) {
    try {
      new URL(url);
      return true;
    } catch (e) {
      return false;
    }
  },

  getQueryParam(url, param) {
    try {
      const urlObj = new URL(url);
      return urlObj.searchParams.get(param);
    } catch (e) {
      return null;
    }
  },

  setQueryParam(url, param, value) {
    try {
      const urlObj = new URL(url);
      urlObj.searchParams.set(param, value);
      return urlObj.toString();
    } catch (e) {
      throw new Error('Invalid URL');
    }
  }
};

export default urlToolkit;
