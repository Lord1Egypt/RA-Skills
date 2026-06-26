const EXIT_CODES = {
  INVALID_INPUT: 2,
  BUSINESS_RULE: 3,
  RUNTIME: 4,
};

class AppError extends Error {
  constructor(code, message, exitCode = EXIT_CODES.RUNTIME, details = undefined) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.exitCode = exitCode;
    this.details = details;
  }
}

function normalizeError(error) {
  if (error instanceof AppError) {
    return error;
  }

  const message = error instanceof Error
    ? error.message
    : 'Unexpected runtime error';

  return new AppError('RUNTIME_ERROR', message, EXIT_CODES.RUNTIME);
}

module.exports = {
  AppError,
  EXIT_CODES,
  normalizeError,
};
