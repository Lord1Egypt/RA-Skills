/**
 * WebSocket Reconnect with Exponential Backoff + Jitter
 * 
 * Features:
 * - Exponential backoff with configurable base delay and multiplier
 * - Random jitter to prevent thundering herd problem
 * - Heartbeat/ping-pong detection for stale connections
 * - Maximum retry limit with circuit breaker pattern
 * - Connection state tracking and event emission
 */

class WebSocketReconnect {
  constructor(options = {}) {
    // Connection options
    this.url = options.url;
    this.protocols = options.protocols || [];
    this.websocketOptions = options.websocketOptions || {};
    
    // Retry configuration
    this.maxRetries = options.maxRetries || 10;
    this.baseDelay = options.baseDelay || 1000; // 1 second
    this.maxDelay = options.maxDelay || 30000; // 30 seconds
    this.multiplier = options.multiplier || 2;
    this.jitter = options.jitter !== undefined ? options.jitter : 0.1; // 10% jitter
    
    // Heartbeat configuration
    this.heartbeatInterval = options.heartbeatInterval || 30000; // 30 seconds
    this.heartbeatTimeout = options.heartbeatTimeout || 5000; // 5 seconds
    this.heartbeatMessage = options.heartbeatMessage || JSON.stringify({ type: 'ping' });
    
    // Circuit breaker configuration
    this.circuitBreaker = {
      failureThreshold: options.circuitBreaker?.failureThreshold || 5,
      resetTimeout: options.circuitBreaker?.resetTimeout || 60000, // 1 minute
      halfOpenMaxRequests: options.circuitBreaker?.halfOpenMaxRequests || 3
    };
    
    // State
    this.ws = null;
    this.retryCount = 0;
    this.retryTimer = null;
    this.heartbeatTimer = null;
    this.heartbeatTimeoutTimer = null;
    this.state = 'CLOSED'; // CLOSED, CONNECTING, OPEN, CLOSING
    this.circuitState = 'CLOSED'; // CLOSED, OPEN, HALF-OPEN
    this.circuitFailures = 0;
    this.circuitHalfOpenRequests = 0;
    this.lastActivity = Date.now();
    this.manualClose = false;
    
    // Event handlers
    this.handlers = {
      open: [],
      message: [],
      close: [],
      error: [],
      retry: [],
      stateChange: [],
      circuitChange: []
    };
  }
  
  /**
   * Calculate delay with exponential backoff and jitter
   */
  calculateDelay(attempt) {
    const exponentialDelay = this.baseDelay * Math.pow(this.multiplier, attempt);
    const cappedDelay = Math.min(exponentialDelay, this.maxDelay);
    
    if (this.jitter > 0) {
      // Add random jitter: delay * (1 ± jitter)
      const jitterFactor = 1 + (Math.random() * 2 - 1) * this.jitter;
      return Math.floor(cappedDelay * jitterFactor);
    }
    
    return Math.floor(cappedDelay);
  }
  
  /**
   * Connect to WebSocket server
   */
  connect() {
    if (this.manualClose) {
      this.emit('stateChange', 'CLOSED');
      return Promise.reject(new Error('Connection manually closed'));
    }
    
    // Check circuit breaker
    if (this.circuitState === 'OPEN') {
      this.emit('stateChange', 'BLOCKED');
      return Promise.reject(new Error('Circuit breaker is OPEN'));
    }
    
    if (this.circuitState === 'HALF-OPEN' && this.circuitHalfOpenRequests >= this.circuitBreaker.halfOpenMaxRequests) {
      this.emit('stateChange', 'BLOCKED');
      return Promise.reject(new Error('Circuit breaker HALF-OPEN limit reached'));
    }
    
    this.state = 'CONNECTING';
    this.emit('stateChange', 'CONNECTING');
    
    return new Promise((resolve, reject) => {
      try {
        // Create WebSocket connection
        if (typeof WebSocket !== 'undefined') {
          // Browser environment
          this.ws = new WebSocket(this.url, this.protocols);
        } else {
          // Node.js environment
          const WebSocketModule = require('ws');
          this.ws = new WebSocketModule(this.url, this.protocols, this.websocketOptions);
        }
        
        this.ws.onopen = () => {
          this.state = 'OPEN';
          this.retryCount = 0;
          this.circuitHalfOpenRequests++;
          this.lastActivity = Date.now();
          
          // If successful in HALF-OPEN state, close circuit
          if (this.circuitState === 'HALF-OPEN') {
            this.closeCircuit();
          }
          
          this.emit('stateChange', 'OPEN');
          this.emit('open');
          this.startHeartbeat();
          resolve();
        };
        
        this.ws.onmessage = (event) => {
          this.lastActivity = Date.now();
          this.handleMessage(event);
        };
        
        this.ws.onclose = (event) => {
          this.state = 'CLOSED';
          this.stopHeartbeat();
          this.emit('stateChange', 'CLOSED');
          this.emit('close', event);
          
          // Attempt reconnect if not manually closed
          if (!this.manualClose && this.circuitState !== 'OPEN') {
            this.scheduleReconnect();
          }
        };
        
        this.ws.onerror = (error) => {
          this.lastActivity = Date.now();
          this.handleError(error);
        };
        
      } catch (error) {
        this.handleError(error);
        reject(error);
      }
    });
  }
  
  /**
   * Handle incoming message
   */
  handleMessage(event) {
    const data = event.data;
    
    // Check if this is a pong response
    try {
      const message = typeof data === 'string' ? JSON.parse(data) : data;
      if (message && message.type === 'pong') {
        this.clearHeartbeatTimeout();
        return;
      }
    } catch (e) {
      // Not JSON, continue normal processing
    }
    
    this.emit('message', event);
  }
  
  /**
   * Handle connection error
   */
  handleError(error) {
    this.circuitFailures++;
    this.emit('error', error);
    
    // Check if circuit breaker should open
    if (this.circuitFailures >= this.circuitBreaker.failureThreshold) {
      this.openCircuit();
    }
  }
  
  /**
   * Schedule reconnection with exponential backoff
   */
  scheduleReconnect() {
    if (this.retryCount >= this.maxRetries) {
      this.emit('stateChange', 'FAILED');
      this.emit('close', { 
        code: 'MAX_RETRIES', 
        reason: `Maximum retry attempts (${this.maxRetries}) exceeded` 
      });
      return;
    }
    
    const delay = this.calculateDelay(this.retryCount);
    this.retryCount++;
    
    this.emit('retry', {
      attempt: this.retryCount,
      delay: delay,
      maxRetries: this.maxRetries
    });
    
    this.retryTimer = setTimeout(() => {
      this.connect().catch(() => {});
    }, delay);
  }
  
  /**
   * Start heartbeat mechanism
   */
  startHeartbeat() {
    this.stopHeartbeat(); // Clear any existing timers
    
    this.heartbeatTimer = setInterval(() => {
      if (this.state === 'OPEN' && this.ws) {
        this.send(this.heartbeatMessage);
        
        // Set timeout for pong response
        this.heartbeatTimeoutTimer = setTimeout(() => {
          this.handleHeartbeatTimeout();
        }, this.heartbeatTimeout);
      }
    }, this.heartbeatInterval);
  }
  
  /**
   * Stop heartbeat mechanism
   */
  stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
    this.clearHeartbeatTimeout();
  }
  
  /**
   * Clear heartbeat timeout timer
   */
  clearHeartbeatTimeout() {
    if (this.heartbeatTimeoutTimer) {
      clearTimeout(this.heartbeatTimeoutTimer);
      this.heartbeatTimeoutTimer = null;
    }
  }
  
  /**
   * Handle heartbeat timeout (stale connection)
   */
  handleHeartbeatTimeout() {
    this.emit('error', new Error('Heartbeat timeout - connection appears stale'));
    
    // Close the connection to trigger reconnect
    if (this.ws) {
      this.ws.close();
    }
  }
  
  /**
   * Send message through WebSocket
   */
  send(data) {
    if (this.state !== 'OPEN' || !this.ws) {
      throw new Error('WebSocket is not connected');
    }
    
    this.lastActivity = Date.now();
    this.ws.send(data);
  }
  
  /**
   * Close the connection
   */
  close(code = 1000, reason = 'Normal closure') {
    this.manualClose = true;
    this.stopHeartbeat();
    
    if (this.retryTimer) {
      clearTimeout(this.retryTimer);
      this.retryTimer = null;
    }
    
    if (this.ws) {
      this.state = 'CLOSING';
      this.emit('stateChange', 'CLOSING');
      this.ws.close(code, reason);
    } else {
      this.state = 'CLOSED';
      this.emit('stateChange', 'CLOSED');
    }
  }
  
  /**
   * Reset connection state and retry count
   */
  reset() {
    this.manualClose = false;
    this.retryCount = 0;
    this.circuitFailures = 0;
    this.closeCircuit();
  }
  
  /**
   * Open circuit breaker
   */
  openCircuit() {
    if (this.circuitState !== 'OPEN') {
      this.circuitState = 'OPEN';
      this.circuitHalfOpenRequests = 0;
      this.emit('circuitChange', 'OPEN');
      
      // Schedule circuit to transition to HALF-OPEN
      setTimeout(() => {
        if (this.circuitState === 'OPEN') {
          this.circuitState = 'HALF-OPEN';
          this.circuitHalfOpenRequests = 0;
          this.emit('circuitChange', 'HALF-OPEN');
        }
      }, this.circuitBreaker.resetTimeout);
    }
  }
  
  /**
   * Close circuit breaker (reset to normal operation)
   */
  closeCircuit() {
    if (this.circuitState !== 'CLOSED') {
      this.circuitState = 'CLOSED';
      this.circuitFailures = 0;
      this.circuitHalfOpenRequests = 0;
      this.emit('circuitChange', 'CLOSED');
    }
  }
  
  /**
   * Get current circuit breaker state
   */
  getCircuitState() {
    return this.circuitState;
  }
  
  /**
   * Get connection statistics
   */
  getStats() {
    return {
      state: this.state,
      circuitState: this.circuitState,
      retryCount: this.retryCount,
      maxRetries: this.maxRetries,
      circuitFailures: this.circuitFailures,
      failureThreshold: this.circuitBreaker.failureThreshold,
      lastActivity: this.lastActivity,
      uptime: Date.now() - this.lastActivity
    };
  }
  
  /**
   * Register event handler
   */
  on(event, handler) {
    if (!this.handlers[event]) {
      this.handlers[event] = [];
    }
    this.handlers[event].push(handler);
    return this;
  }
  
  /**
   * Remove event handler
   */
  off(event, handler) {
    if (this.handlers[event]) {
      if (handler) {
        this.handlers[event] = this.handlers[event].filter(h => h !== handler);
      } else {
        this.handlers[event] = [];
      }
    }
    return this;
  }
  
  /**
   * Emit event to all registered handlers
   */
  emit(event, data) {
    if (this.handlers[event]) {
      this.handlers[event].forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`Error in event handler for '${event}':`, error);
        }
      });
    }
  }
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { WebSocketReconnect };
}

// Export for browser
if (typeof window !== 'undefined') {
  window.WebSocketReconnect = WebSocketReconnect;
}
