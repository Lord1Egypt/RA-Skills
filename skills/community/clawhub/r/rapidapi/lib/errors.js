export class HttpError extends Error {
  constructor(status, message, details) {
    super(message);
    this.status = status;
    this.details = details;
  }
}

export function toErrorResult(err, meta) {
  if (err instanceof HttpError) {
    return {
      ok: false,
      status: err.status,
      error: { message: err.message, details: err.details },
      meta
    };
  }
  return {
    ok: false,
    status: 500,
    error: { message: "Unexpected error", details: err },
    meta
  };
}
