# Opening & Closing Sidebar

## Table of Contents
- [Toggle Functionality](#toggle-functionality)
- [Programmatic Show/Hide](#programmatic-showhide)
- [Auto-Close Behavior](#auto-close-behavior)
- [Event Handling](#event-handling)
- [Animation & Transitions](#animation--transitions)
- [Complete Examples](#complete-examples)

---

## Toggle Functionality

### Basic Toggle with Button

```jsx
import React, { useState, useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function App() {
  const sidebarRef = useRef(null);

  const handleToggle = () => {
    if (sidebarRef.current) {
      sidebarRef.current.toggle();
    }
  };

  return (
    <div>
      <ButtonComponent onClick={handleToggle}>
        ☰ Toggle Menu
      </ButtonComponent>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="250px"
      >
        {/* Sidebar content */}
      </SidebarComponent>
    </div>
  );
}

export default App;
```

### Toggle with State Management

```jsx
import React, { useState } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  const handleChange = (args) => {
    const nowOpen = args.element.classList.contains('e-open');
    setIsOpen(nowOpen);
  };

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>
        Toggle: {isOpen ? 'Close' : 'Open'}
      </button>

      <SidebarComponent
        isOpen={isOpen}
        change={handleChange}
        type="Over"
      >
        Content
      </SidebarComponent>
    </div>
  );
}

export default App;
```

---

## Programmatic Show/Hide

### Show Method

Opens the sidebar programmatically.

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const openSidebar = () => {
    if (sidebarRef.current) {
      sidebarRef.current.show();
    }
  };

  return (
    <div>
      <button onClick={openSidebar}>Open Sidebar</button>
      <SidebarComponent ref={sidebarRef} type="Over" width="250px">
        Sidebar Content
      </SidebarComponent>
    </div>
  );
}

export default App;
```

### Hide Method

Closes the sidebar programmatically.

```jsx
const closeSidebar = () => {
  if (sidebarRef.current) {
    sidebarRef.current.hide();
  }
};

return <button onClick={closeSidebar}>Close Sidebar</button>;
```

### Show/Hide Based on Conditions

```jsx
function App() {
  const sidebarRef = useRef(null);
  const [userRole, setUserRole] = useState('guest');

  const handleLogin = (role) => {
    setUserRole(role);
    // Show sidebar only for authenticated users
    if (role !== 'guest' && sidebarRef.current) {
      sidebarRef.current.show();
    }
  };

  const handleLogout = () => {
    setUserRole('guest');
    // Hide sidebar on logout
    if (sidebarRef.current) {
      sidebarRef.current.hide();
    }
  };

  return (
    <div>
      {userRole === 'guest' ? (
        <>
          <button onClick={() => handleLogin('user')}>Login</button>
        </>
      ) : (
        <button onClick={handleLogout}>Logout</button>
      )}

      <SidebarComponent
        ref={sidebarRef}
        type="Push"
        width="250px"
      >
        <h3>Welcome, {userRole}!</h3>
      </SidebarComponent>
    </div>
  );
}
```

---

## Auto-Close Behavior

### Close on Document Click

Automatically closes sidebar when user clicks on main content area.

```jsx
<SidebarComponent
  type="Over"
  width="250px"
  closeOnDocumentClick={true}
  showBackdrop={true}
>
  {/* Closes when backdrop/content clicked */}
</SidebarComponent>
```

**Caveat:** Works best with `showBackdrop={true}` for better UX.

### Close on Escape Key

```jsx
import React, { useRef, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape' && sidebarRef.current) {
        sidebarRef.current.hide();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Over"
      width="250px"
    >
      Press ESC to close
    </SidebarComponent>
  );
}

export default App;
```

### Close on Navigation Item Click

```jsx
import React, { useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const sidebarRef = useRef(null);

  const handleNavigation = (e) => {
    if (e.target.tagName === 'A') {
      // Close sidebar when any link is clicked
      if (sidebarRef.current) {
        sidebarRef.current.hide();
      }
    }
  };

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Over"
      width="250px"
    >
      <nav onClick={handleNavigation}>
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
      </nav>
    </SidebarComponent>
  );
}

export default App;
```

### Close After Delay

```jsx
function App() {
  const sidebarRef = useRef(null);

  const openAndAutoClose = () => {
    if (sidebarRef.current) {
      sidebarRef.current.show();
      // Auto-close after 5 seconds
      setTimeout(() => {
        if (sidebarRef.current) {
          sidebarRef.current.hide();
        }
      }, 5000);
    }
  };

  return (
    <div>
      <button onClick={openAndAutoClose}>Open (Auto-closes in 5s)</button>
      <SidebarComponent ref={sidebarRef} type="Over" width="250px">
        This sidebar will auto-close
      </SidebarComponent>
    </div>
  );
}
```

---

## Event Handling

### Change Event (State Change)

Triggers when sidebar opens or closes.

```jsx
<SidebarComponent
  change={(args) => {
    const isNowOpen = args.element.classList.contains('e-open');
    console.log(isNowOpen ? 'Opened' : 'Closed');
    console.log('User interaction:', args.isInteracted);
  }}
/>
```

### Open Event (Before Opening)

Triggers before sidebar opens. Can prevent opening.

```jsx
<SidebarComponent
  open={(args) => {
    console.log('Sidebar opening...');
    
    // Prevent opening under certain conditions
    if (userHasNoPermission) {
      args.cancel = true;
    }
  }}
/>
```

### Close Event (Before Closing)

Triggers before sidebar closes. Can prevent closing.

```jsx
<SidebarComponent
  close={(args) => {
    console.log('Sidebar closing...');
    
    // Ask for confirmation before closing
    if (!confirm('Are you sure?')) {
      args.cancel = true;
    }
  }}
/>
```

### Created & Destroyed Events

```jsx
<SidebarComponent
  created={() => console.log('Sidebar initialized')}
  destroyed={() => console.log('Sidebar removed from DOM')}
/>
```

### Complete Event Example

```jsx
import React, { useState, useRef } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';

function App() {
  const [status, setStatus] = useState('');
  const sidebarRef = useRef(null);

  const handleChange = (args) => {
    const isOpen = args.element.classList.contains('e-open');
    setStatus(`State changed: ${isOpen ? 'Opened' : 'Closed'}`);
  };

  const handleOpen = (args) => {
    setStatus('Opening...');
  };

  const handleClose = (args) => {
    setStatus('Closing...');
  };

  return (
    <div>
      <p>Status: {status}</p>
      <button onClick={() => sidebarRef.current?.toggle()}>Toggle</button>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="250px"
        change={handleChange}
        open={handleOpen}
        close={handleClose}
      >
        Sidebar with Events
      </SidebarComponent>
    </div>
  );
}

export default App;
```

---

## Animation & Transitions

### Enable/Disable Animations

```jsx
// With animation (default)
<SidebarComponent animate={true} />

// Without animation (instant)
<SidebarComponent animate={false} />
```

### Custom Animation Duration

```css
/* Slower animation */
.e-sidebar.e-open {
  transition: transform 0.5s ease-in-out;
}

/* Faster animation */
.e-sidebar.e-open {
  transition: transform 0.2s ease-out;
}
```

### Animation Effects

```css
/* Slide in from left */
.e-sidebar.e-slide {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}

/* Fade and slide */
.e-sidebar.e-open {
  animation: fadeSlide 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes fadeSlide {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

---

## Complete Examples

### Example 1: Mobile Menu with All Features

```jsx
import React, { useState, useRef, useEffect } from 'react';
import { SidebarComponent } from '@syncfusion/ej2-react-navigations';
import { ButtonComponent } from '@syncfusion/ej2-react-buttons';

function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const [lastAction, setLastAction] = useState('');
  const sidebarRef = useRef(null);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        sidebarRef.current?.hide();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  const handleNavClick = (e) => {
    if (e.target.tagName === 'A') {
      setLastAction(`Navigated to: ${e.target.textContent}`);
      sidebarRef.current?.hide();
    }
  };

  return (
    <div className="mobile-menu-app">
      <header className="header">
        <ButtonComponent
          cssClass="e-icon-btn e-outline"
          onClick={() => setIsOpen(!isOpen)}
        >
          ☰
        </ButtonComponent>
        <h1>Mobile App</h1>
      </header>

      <SidebarComponent
        ref={sidebarRef}
        type="Over"
        width="280px"
        isOpen={isOpen}
        change={() => setIsOpen(!isOpen)}
        open={() => setLastAction('Menu opened')}
        close={() => setLastAction('Menu closed')}
        showBackdrop={true}
        closeOnDocumentClick={true}
        animate={true}
      >
        <nav className="nav" onClick={handleNavClick}>
          <a href="#home" className="nav-item">🏠 Home</a>
          <a href="#products" className="nav-item">📦 Products</a>
          <a href="#about" className="nav-item">ℹ️ About</a>
          <a href="#contact" className="nav-item">📧 Contact</a>
          <a href="#settings" className="nav-item">⚙️ Settings</a>
        </nav>
      </SidebarComponent>

      <main className="main-content">
        <h2>Welcome</h2>
        <p>Last action: {lastAction || 'None'}</p>
      </main>
    </div>
  );
}

export default MobileMenu;
```

### Example 2: Desktop Sidebar with Persistent State

```jsx
function DesktopSidebar() {
  const [isOpen, setIsOpen] = useState(() => {
    // Load from localStorage
    return localStorage.getItem('sidebarOpen') === 'true';
  });
  const sidebarRef = useRef(null);

  useEffect(() => {
    // Save to localStorage
    localStorage.setItem('sidebarOpen', isOpen);
  }, [isOpen]);

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Push"
      width="250px"
      isOpen={isOpen}
      change={() => setIsOpen(!isOpen)}
    >
      {/* Persistent sidebar */}
    </SidebarComponent>
  );
}
```

### Example 3: Conditional Sidebar Opening

```jsx
function ConditionalSidebar() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const sidebarRef = useRef(null);

  const login = async (credentials) => {
    try {
      const response = await authenticate(credentials);
      if (response.success) {
        setIsAuthenticated(true);
        // Open sidebar on successful login
        sidebarRef.current?.show();
      }
    } catch (error) {
      console.error('Login failed');
    }
  };

  if (!isAuthenticated) {
    return <LoginForm onLogin={login} />;
  }

  return (
    <SidebarComponent
      ref={sidebarRef}
      type="Push"
      isOpen={true}
    >
      {/* Dashboard with sidebar */}
    </SidebarComponent>
  );
}
```

---
