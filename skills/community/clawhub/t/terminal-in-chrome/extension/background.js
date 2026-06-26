chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'TERMINAL_ACTIVITY' && sender.tab) {
    const tabId = sender.tab.id;
    if (message.status === 'processing') {
      const isVisible = message.blink !== false;
      chrome.action.setBadgeText({ text: isVisible ? 'REC' : '', tabId: tabId });
      chrome.action.setBadgeBackgroundColor({ color: '#F44336', tabId: tabId });
      if (chrome.action.setBadgeTextColor) chrome.action.setBadgeTextColor({ color: '#FFFFFF', tabId: tabId });
    } else if (message.status === 'done') {
      chrome.action.setBadgeText({ text: '✓', tabId: tabId });
      chrome.action.setBadgeBackgroundColor({ color: '#4CAF50', tabId: tabId });
      if (chrome.action.setBadgeTextColor) chrome.action.setBadgeTextColor({ color: '#FFFFFF', tabId: tabId });
    } else if (message.status === 'clear') {
      chrome.action.setBadgeText({ text: '', tabId: tabId });
    }
  }
});