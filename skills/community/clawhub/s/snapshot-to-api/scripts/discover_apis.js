/**
 * API Discovery Script
 * 
 * Run this via browser evaluate to discover all API endpoints
 * a web page called during loading.
 * 
 * Usage (in browser evaluate):
 *   () => { <paste this script> }
 * 
 * Or read and evaluate the file content directly.
 */

(() => {
  const hostname = window.location.hostname;
  
  // Get all resource entries from the same domain
  const allEntries = performance.getEntriesByType('resource')
    .filter(e => e.name.includes(hostname))
    .filter(e => !e.name.match(/\.(js|css|png|jpg|jpeg|gif|webp|svg|ico|woff|woff2|ttf|eot)(\?|$)/));
  
  // Categorize
  const apis = [];
  const other = [];
  
  allEntries.forEach(e => {
    const url = new URL(e.name);
    const path = url.pathname + url.search;
    const entry = {
      method: e.initiatorType === 'xmlhttprequest' ? 'XHR' : 
              e.initiatorType === 'fetch' ? 'Fetch' : e.initiatorType,
      path: path.length > 200 ? path.substring(0, 200) + '...' : path,
      duration: Math.round(e.duration) + 'ms',
      size: e.transferSize ? Math.round(e.transferSize / 1024) + 'KB' : 'unknown'
    };
    
    // Likely API if path contains common API patterns
    if (path.match(/\/(api|v[0-9]|graphql|rpc|rest)\//i) ||
        path.match(/\.(json|xml)(\?|$)/) ||
        e.initiatorType === 'xmlhttprequest' ||
        e.initiatorType === 'fetch') {
      apis.push(entry);
    } else {
      other.push(entry);
    }
  });
  
  return JSON.stringify({
    summary: {
      total_requests: allEntries.length,
      likely_apis: apis.length,
      other: other.length,
      hostname: hostname
    },
    apis: apis,
    other_requests: other.length > 10 ? other.slice(0, 10).concat([{note: `...and ${other.length - 10} more`}]) : other
  }, null, 2);
})();
