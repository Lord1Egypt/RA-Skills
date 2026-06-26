package googleapi

import "time"

const (
	// MaxRateLimitRetries is the maximum number of retries on 429 responses.
	MaxRateLimitRetries = 3
	// RateLimitBaseDelay is the initial delay for rate limit exponential backoff.
	RateLimitBaseDelay = 1 * time.Second
	// Max5xxRetries is the maximum retries for server errors.
	Max5xxRetries = 1
	// ServerErrorRetryDelay is the delay before retrying on 5xx errors.
	ServerErrorRetryDelay = 1 * time.Second
)
