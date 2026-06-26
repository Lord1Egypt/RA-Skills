export class WereadAuthError extends Error {
  constructor(message) {
    super(message);
    this.name = 'WereadAuthError';
  }
}

export class WereadApiError extends Error {
  constructor(message) {
    super(message);
    this.name = 'WereadApiError';
  }
}

export class WereadGatewayMissingKeyError extends Error {
  constructor(message) {
    super(message);
    this.name = 'WereadGatewayMissingKeyError';
  }
}

export class WereadGatewayAuthError extends Error {
  constructor(message) {
    super(message);
    this.name = 'WereadGatewayAuthError';
  }
}

export class WereadGatewayUpgradeError extends Error {
  constructor(message) {
    super(message);
    this.name = 'WereadGatewayUpgradeError';
  }
}

export class WereadGatewayUnavailableError extends Error {
  constructor(message) {
    super(message);
    this.name = 'WereadGatewayUnavailableError';
  }
}
