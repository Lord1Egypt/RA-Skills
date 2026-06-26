document.addEventListener('DOMContentLoaded', () => {
  const portInput = document.getElementById('portInput');
  const blockedSitesInput = document.getElementById('blockedSitesInput');
  const sharedPathsInput = document.getElementById('sharedPathsInput');
  const themeSelect = document.getElementById('themeSelect');
  const saveBtn = document.getElementById('saveBtn');
  const statusEl = document.getElementById('status');

  // Load current settings
  chrome.storage.local.get(['terminalPort', 'blockedSites', 'terminalTheme', 'sharedPaths'], (result) => {
    if (result.terminalPort) {
      portInput.value = result.terminalPort;
    } else {
      portInput.value = '8989';
    }
    
    if (result.blockedSites && Array.isArray(result.blockedSites)) {
      blockedSitesInput.value = result.blockedSites.join('\n');
    }
    
    if (result.terminalTheme) {
      themeSelect.value = result.terminalTheme;
    }
    
    if (result.sharedPaths && Array.isArray(result.sharedPaths)) {
      sharedPathsInput.value = result.sharedPaths.join('\n');
    }
  });

  // Save settings
  saveBtn.addEventListener('click', () => {
    const port = portInput.value || '8989';
    const theme = themeSelect.value || 'dark';
    const blockedSitesText = blockedSitesInput.value.trim();
    const sharedPathsText = sharedPathsInput.value.trim();
    
    const blockedSites = blockedSitesText 
      ? blockedSitesText.split('\n').map(s => s.trim()).filter(s => s)
      : [];
    
    const sharedPaths = sharedPathsText
      ? sharedPathsText.split('\n').map(s => s.trim()).filter(s => s)
      : [];
    
    chrome.storage.local.set({ 
      terminalPort: port,
      blockedSites: blockedSites,
      terminalTheme: theme,
      sharedPaths: sharedPaths
    }, () => {
      // Show status
      statusEl.style.display = 'block';
      setTimeout(() => {
        statusEl.style.display = 'none';
      }, 2000);

      // Notify all tabs about the port change
      chrome.tabs.query({}, (tabs) => {
        tabs.forEach(tab => {
          chrome.tabs.sendMessage(tab.id, { 
            type: 'UPDATE_SETTINGS', 
            port: port,
            theme: theme 
          }).catch(() => {
            // Ignore errors for tabs where content script isn't injected
          });
        });
      });
    });
  });
});