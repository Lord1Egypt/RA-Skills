// === Native App Enhancements ===

// 1. Splash screen dismiss
window.addEventListener('load', () => {
    setTimeout(() => {
        const splash = document.getElementById('app-splash');
        if (splash) {
            splash.classList.add('fade-out');
            setTimeout(() => splash.remove(), 600);
        }
    }, 800);
});

// 2. Prevent pull-to-refresh and overscroll bounce
document.addEventListener('touchmove', function(e) {
    // Allow scrolling inside scrollable containers
    let el = e.target;
    while (el && el !== document.body) {
        const style = window.getComputedStyle(el);
        if ((style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight) {
            return; // Allow scroll inside this element
        }
        el = el.parentElement;
    }
    e.preventDefault();
}, { passive: false });

// 3. Prevent double-tap zoom
let lastTouchEnd = 0;
document.addEventListener('touchend', function(e) {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        e.preventDefault();
    }
    lastTouchEnd = now;
}, false);

// 4. Prevent pinch zoom
document.addEventListener('gesturestart', function(e) {
    e.preventDefault();
});
document.addEventListener('gesturechange', function(e) {
    e.preventDefault();
});

// 5. Prevent context menu on long press - mobile only (except in chat messages)
const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
if (isTouchDevice) {
    document.addEventListener('contextmenu', function(e) {
        const allowed = e.target.closest('.message-agent, .message-user, .markdown-body, textarea, input');
        if (!allowed) {
            e.preventDefault();
        }
    });
}

// 6. Online/Offline detection
function updateOnlineStatus() {
    const banner = document.getElementById('offline-banner');
    if (navigator.onLine) {
        banner.classList.remove('show');
    } else {
        banner.classList.add('show');
    }
}
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

// 7. Register Service Worker for PWA caching
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
}

// 8. iOS standalone: handle navigation to stay in-app
if (window.navigator.standalone) {
    document.addEventListener('click', function(e) {
        const a = e.target.closest('a');
        if (a && a.href && !a.target && a.hostname === location.hostname) {
            e.preventDefault();
            location.href = a.href;
        }
    });
}

// 9. Keyboard handling for mobile/PWA - comprehensive solution
if (isTouchDevice && window.visualViewport) {
    const chatMain = document.querySelector('.chat-main');
    const chatContainer = document.querySelector('.chat-container');
    const header = document.querySelector('header');
    const inputArea = document.querySelector('.border-t.p-2');
    
    // PWA Standalone mode detection
    const isPWA = window.matchMedia('(display-mode: standalone)').matches || 
                  window.navigator.standalone === true;
    
    let lastHeight = window.visualViewport.height;
    
    function handleViewportChange() {
        const vh = window.visualViewport.height;
        const windowHeight = window.innerHeight;
        const keyboardHeight = windowHeight - vh;
        
        // Detect if keyboard is open (more than 100px difference)
        const keyboardOpen = keyboardHeight > 100;
        
        if (isPWA || keyboardOpen) {
            // PWA mode or keyboard open: adjust heights
            const availableHeight = vh;
            
            // Update CSS variable for app height
            document.documentElement.style.setProperty('--app-height', availableHeight + 'px');
            
            // Chat main takes full available height
            if (chatMain) {
                chatMain.style.height = availableHeight + 'px';
                chatMain.style.maxHeight = availableHeight + 'px';
            }
            
            // Ensure flex behavior
            if (header) header.style.flexShrink = '0';
            if (inputArea) inputArea.style.flexShrink = '0';
            
            // Chat container gets remaining space via flex
            if (chatContainer) {
                chatContainer.style.flex = '1';
                chatContainer.style.minHeight = '0';
            }
        } else {
            // Normal mode: reset to CSS defaults
            document.documentElement.style.removeProperty('--app-height');
            
            if (chatMain) {
                chatMain.style.height = '';
                chatMain.style.maxHeight = '';
            }
            
            if (header) header.style.flexShrink = '';
            if (inputArea) inputArea.style.flexShrink = '';
            
            if (chatContainer) {
                chatContainer.style.flex = '';
                chatContainer.style.minHeight = '';
            }
        }
        
        lastHeight = vh;
    }
    
    // Debounced resize handler
    let resizeTimeout;
    function debouncedHandleViewportChange() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(handleViewportChange, 50);
    }
    
    // Initial call
    handleViewportChange();
    
    // Listen for viewport changes
    window.visualViewport.addEventListener('resize', debouncedHandleViewportChange);
    window.visualViewport.addEventListener('scroll', handleViewportChange);
    
    // Also listen for window resize (orientation change)
    window.addEventListener('resize', debouncedHandleViewportChange);
    window.addEventListener('orientationchange', () => {
        setTimeout(handleViewportChange, 100);
    });
}

// Input focus: scroll into view on mobile
const inputEl = document.getElementById('user-input');
if (inputEl && isTouchDevice) {
    inputEl.addEventListener('focus', () => {
        setTimeout(() => {
            // Scroll input into view
            inputEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            // Also trigger viewport check
            if (window.visualViewport) {
                window.dispatchEvent(new Event('resize'));
            }
        }, 100);
    });
    
    // On blur: reset after keyboard closes
    inputEl.addEventListener('blur', () => {
        setTimeout(() => {
            if (window.visualViewport) {
                window.dispatchEvent(new Event('resize'));
            }
        }, 200);
    });
}
