package googleapi

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"strings"
	"testing"
	"time"
)

type roundTripFunc func(*http.Request) (*http.Response, error)

func (f roundTripFunc) RoundTrip(req *http.Request) (*http.Response, error) {
	return f(req)
}

type closeTracker struct {
	closed bool
}

func (c *closeTracker) Read(p []byte) (int, error) {
	return 0, io.EOF
}

func (c *closeTracker) Close() error {
	c.closed = true
	return nil
}

func newTestResponse(status int, body string) *http.Response {
	return &http.Response{
		StatusCode: status,
		Body:       io.NopCloser(strings.NewReader(body)),
		Header:     http.Header{},
	}
}

func TestNewRetryTransportDefaults(t *testing.T) {
	rt := NewRetryTransport(nil)
	if rt.Base == nil {
		t.Fatalf("expected base transport")
	}

	if rt.MaxRetries429 == 0 || rt.MaxRetries5xx == 0 {
		t.Fatalf("expected defaults to be set")
	}

	if rt.CircuitBreaker == nil {
		t.Fatalf("expected circuit breaker")
	}
}

func TestRetryTransportRoundTripSuccess(t *testing.T) {
	calls := 0
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		calls++
		return newTestResponse(http.StatusOK, "ok"), nil
	})

	rt := &RetryTransport{
		Base:          base,
		MaxRetries429: 1,
		MaxRetries5xx: 1,
		BaseDelay:     0,
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, "http://example.com", nil)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if err != nil {
		t.Fatalf("round trip: %v", err)
	}
	_ = resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("unexpected status: %d", resp.StatusCode)
	}

	if calls != 1 {
		t.Fatalf("expected 1 call, got %d", calls)
	}
}

func TestRetryTransportRoundTripRetries429(t *testing.T) {
	calls := 0
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		calls++
		if calls == 1 {
			return newTestResponse(http.StatusTooManyRequests, "rate"), nil
		}

		return newTestResponse(http.StatusOK, "ok"), nil
	})

	rt := &RetryTransport{
		Base:          base,
		MaxRetries429: 1,
		MaxRetries5xx: 0,
		BaseDelay:     0,
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, "http://example.com", nil)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if err != nil {
		t.Fatalf("round trip: %v", err)
	}
	_ = resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("unexpected status: %d", resp.StatusCode)
	}

	if calls != 2 {
		t.Fatalf("expected 2 calls, got %d", calls)
	}
}

func TestRetryTransportRoundTripStopsAfter429Retries(t *testing.T) {
	calls := 0
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		calls++
		return newTestResponse(http.StatusTooManyRequests, "rate"), nil
	})

	rt := &RetryTransport{
		Base:          base,
		MaxRetries429: 1,
		MaxRetries5xx: 0,
		BaseDelay:     0,
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, "http://example.com", nil)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if err != nil {
		t.Fatalf("round trip: %v", err)
	}
	_ = resp.Body.Close()

	if resp.StatusCode != http.StatusTooManyRequests {
		t.Fatalf("expected 429, got %d", resp.StatusCode)
	}

	if calls != 2 {
		t.Fatalf("expected 2 calls, got %d", calls)
	}
}

func TestRetryTransportRoundTripRetries5xx(t *testing.T) {
	calls := 0
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		calls++
		if calls == 1 {
			return newTestResponse(http.StatusInternalServerError, "err"), nil
		}

		return newTestResponse(http.StatusOK, "ok"), nil
	})

	cb := NewCircuitBreaker()
	rt := &RetryTransport{
		Base:           base,
		MaxRetries429:  0,
		MaxRetries5xx:  1,
		BaseDelay:      0,
		CircuitBreaker: cb,
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, "http://example.com", nil)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if err != nil {
		t.Fatalf("round trip: %v", err)
	}
	_ = resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("unexpected status: %d", resp.StatusCode)
	}

	if calls != 2 {
		t.Fatalf("expected 2 calls, got %d", calls)
	}

	if cb.State() != circuitStateClosed {
		t.Fatalf("expected circuit closed, got %s", cb.State())
	}
}

func TestRetryTransportCircuitBreakerOpen(t *testing.T) {
	calls := 0
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		calls++
		return newTestResponse(http.StatusOK, "ok"), nil
	})

	cb := NewCircuitBreaker()
	cb.open = true
	cb.lastFailure = time.Now()

	rt := &RetryTransport{
		Base:           base,
		CircuitBreaker: cb,
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, "http://example.com", nil)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if resp != nil {
		_ = resp.Body.Close()
	}

	if err == nil {
		t.Fatalf("expected circuit breaker error")
	}

	if calls != 0 {
		t.Fatalf("expected 0 calls, got %d", calls)
	}
}

func TestRetryTransportCalculateBackoffRetryAfter(t *testing.T) {
	rt := &RetryTransport{BaseDelay: time.Second}
	resp := &http.Response{Header: http.Header{"Retry-After": []string{"5"}}}

	if got := rt.calculateBackoff(0, resp); got != 5*time.Second {
		t.Fatalf("expected 5s, got %v", got)
	}

	resp = &http.Response{Header: http.Header{"Retry-After": []string{"-1"}}}
	if got := rt.calculateBackoff(0, resp); got != 0 {
		t.Fatalf("expected 0, got %v", got)
	}

	date := time.Now().Add(2 * time.Second).UTC().Format(http.TimeFormat)
	resp = &http.Response{Header: http.Header{"Retry-After": []string{date}}}

	if got := rt.calculateBackoff(0, resp); got <= 0 {
		t.Fatalf("expected positive delay, got %v", got)
	}
}

func TestRetryTransportCalculateBackoffDefault(t *testing.T) {
	rt := &RetryTransport{BaseDelay: time.Nanosecond}
	resp := &http.Response{Header: http.Header{}}

	if got := rt.calculateBackoff(0, resp); got != time.Nanosecond {
		t.Fatalf("expected base delay, got %v", got)
	}
}

func TestRetryTransportSleepInterrupted(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	rt := &RetryTransport{}
	if err := rt.sleep(ctx, time.Second); err == nil {
		t.Fatalf("expected sleep error")
	}
}

func TestEnsureReplayableBodyMore(t *testing.T) {
	req, err := http.NewRequestWithContext(context.Background(), http.MethodPost, "http://example.com", io.NopCloser(strings.NewReader("hello")))
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	err = ensureReplayableBody(req)
	if err != nil {
		t.Fatalf("ensureReplayableBody: %v", err)
	}

	if req.GetBody == nil {
		t.Fatalf("expected GetBody")
	}

	body1, readErr := io.ReadAll(req.Body)
	if readErr != nil {
		t.Fatalf("read body: %v", readErr)
	}

	rc, err := req.GetBody()
	if err != nil {
		t.Fatalf("get body: %v", err)
	}

	body2, readErr := io.ReadAll(rc)
	if readErr != nil {
		t.Fatalf("read body copy: %v", readErr)
	}
	_ = rc.Close()

	if string(body1) != "hello" || string(body2) != "hello" {
		t.Fatalf("unexpected body: %q %q", body1, body2)
	}
}

func TestDrainAndClose(t *testing.T) {
	rc := &closeTracker{}
	drainAndClose(rc)

	if !rc.closed {
		t.Fatalf("expected close")
	}
}

func TestRetryTransportRoundTripResetsBody(t *testing.T) {
	var gotBodies []string
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		body, err := io.ReadAll(req.Body)
		if err != nil {
			return nil, fmt.Errorf("read body: %w", err)
		}

		gotBodies = append(gotBodies, string(body))

		return newTestResponse(http.StatusTooManyRequests, "rate"), nil
	})

	rt := &RetryTransport{
		Base:          base,
		MaxRetries429: 1,
		MaxRetries5xx: 0,
		BaseDelay:     0,
	}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodPost, "http://example.com", io.NopCloser(strings.NewReader("payload")))
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if err != nil {
		t.Fatalf("round trip: %v", err)
	}
	_ = resp.Body.Close()

	if len(gotBodies) != 2 {
		t.Fatalf("expected 2 bodies, got %d", len(gotBodies))
	}

	if gotBodies[0] != "payload" || gotBodies[1] != "payload" {
		t.Fatalf("unexpected bodies: %#v", gotBodies)
	}
}

func TestRetryTransportRoundTripError(t *testing.T) {
	base := roundTripFunc(func(req *http.Request) (*http.Response, error) {
		return nil, errBoom
	})

	rt := &RetryTransport{Base: base}

	req, err := http.NewRequestWithContext(context.Background(), http.MethodGet, "http://example.com", nil)
	if err != nil {
		t.Fatalf("new request: %v", err)
	}

	resp, err := rt.RoundTrip(req)
	if resp != nil {
		_ = resp.Body.Close()
	}

	if err == nil {
		t.Fatalf("expected error")
	}
}
