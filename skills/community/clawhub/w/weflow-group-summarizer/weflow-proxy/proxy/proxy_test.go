package proxy_test

import (
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"weflow-proxy/proxy"
)

func TestProxyForwardsRequestPathAndQuery(t *testing.T) {
	// Fake upstream WeFlow server
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/api/v1/sessions" {
			t.Errorf("expected path /api/v1/sessions, got %s", r.URL.Path)
		}
		if r.URL.RawQuery != "keyword=test&limit=10" {
			t.Errorf("expected query keyword=test&limit=10, got %s", r.URL.RawQuery)
		}
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"success":true}`))
	}))
	defer upstream.Close()

	handler := proxy.NewHandler(upstream.URL)
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	resp, err := http.Get(proxyServer.URL + "/api/v1/sessions?keyword=test&limit=10")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("expected status 200, got %d", resp.StatusCode)
	}

	body, _ := io.ReadAll(resp.Body)
	if string(body) != `{"success":true}` {
		t.Errorf("expected body {\"success\":true}, got %s", string(body))
	}
}

func TestProxyForwardsResponseHeaders(t *testing.T) {
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Custom-Header", "weflow-value")
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{}`))
	}))
	defer upstream.Close()

	handler := proxy.NewHandler(upstream.URL)
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	resp, err := http.Get(proxyServer.URL + "/health")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if got := resp.Header.Get("X-Custom-Header"); got != "weflow-value" {
		t.Errorf("expected X-Custom-Header=weflow-value, got %s", got)
	}
	if got := resp.Header.Get("Content-Type"); got != "application/json" {
		t.Errorf("expected Content-Type=application/json, got %s", got)
	}
}

func TestProxyReturns502WhenUpstreamDown(t *testing.T) {
	// Point at a server that is not running
	handler := proxy.NewHandler("http://127.0.0.1:19999")
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	resp, err := http.Get(proxyServer.URL + "/health")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusBadGateway {
		t.Errorf("expected status 502, got %d", resp.StatusCode)
	}
}

func TestProxyForwardsRequestHeaders(t *testing.T) {
	var receivedHeaders http.Header
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		receivedHeaders = r.Header.Clone()
		w.WriteHeader(http.StatusOK)
	}))
	defer upstream.Close()

	handler := proxy.NewHandler(upstream.URL)
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	req, _ := http.NewRequest("GET", proxyServer.URL+"/api/v1/contacts", nil)
	req.Header.Set("Accept", "application/json")
	req.Header.Set("X-Request-ID", "abc123")

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if got := receivedHeaders.Get("Accept"); got != "application/json" {
		t.Errorf("expected Accept=application/json, got %s", got)
	}
	if got := receivedHeaders.Get("X-Request-ID"); got != "abc123" {
		t.Errorf("expected X-Request-ID=abc123, got %s", got)
	}
}

func TestProxyRewritesMediaUrlHost(t *testing.T) {
	var upstreamURL string
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		body := fmt.Sprintf(`{"messages":[{"mediaUrl":"%s/api/v1/media/room1/images/abc.png","text":"hello"}]}`, upstreamURL)
		w.Write([]byte(body))
	}))
	defer upstream.Close()
	upstreamURL = upstream.URL

	handler := proxy.NewHandler(upstream.URL)
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	resp, err := http.Get(proxyServer.URL + "/api/v1/messages?talker=room1&media=1&image=1")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)

	if strings.Contains(string(body), upstream.URL) {
		t.Errorf("response still contains upstream URL %s: %s", upstream.URL, body)
	}

	expectedURL := proxyServer.URL + "/api/v1/media/room1/images/abc.png"
	if !strings.Contains(string(body), expectedURL) {
		t.Errorf("expected response to contain %s, got: %s", expectedURL, body)
	}
}

func TestProxyRewritesMultipleMediaUrls(t *testing.T) {
	var upstreamURL string
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		body := fmt.Sprintf(`{"messages":[{"mediaUrl":"%s/api/v1/media/room1/images/a.png"},{"mediaUrl":"%s/api/v1/media/room1/images/b.png"}]}`, upstreamURL, upstreamURL)
		w.Write([]byte(body))
	}))
	defer upstream.Close()
	upstreamURL = upstream.URL

	handler := proxy.NewHandler(upstream.URL)
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	resp, err := http.Get(proxyServer.URL + "/api/v1/messages?talker=room1&media=1&image=1")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	count := strings.Count(string(body), proxyServer.URL)
	if count != 2 {
		t.Errorf("expected 2 occurrences of proxy URL, got %d: %s", count, body)
	}
}

func TestProxyDoesNotRewriteNonJsonResponse(t *testing.T) {
	var upstreamURL string
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/plain")
		body := fmt.Sprintf("visit %s/api/v1/media/room1/images/a.png", upstreamURL)
		w.Write([]byte(body))
	}))
	defer upstream.Close()
	upstreamURL = upstream.URL

	handler := proxy.NewHandler(upstream.URL)
	proxyServer := httptest.NewServer(handler)
	defer proxyServer.Close()

	resp, err := http.Get(proxyServer.URL + "/test")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	if !strings.Contains(string(body), upstream.URL) {
		t.Errorf("non-JSON response should not be rewritten: %s", body)
	}
}

func TestProxyForwardsAllWeFlowEndpoints(t *testing.T) {
	tests := []struct {
		name       string
		path       string
		query      string
		wantStatus int
		wantBody   string
	}{
		{
			name:       "health check",
			path:       "/health",
			wantStatus: http.StatusOK,
			wantBody:   `{"status":"ok"}`,
		},
		{
			name:       "get messages",
			path:       "/api/v1/messages",
			query:      "talker=wxid_abc123&limit=50",
			wantStatus: http.StatusOK,
			wantBody:   `{"success":true,"count":0,"messages":[]}`,
		},
		{
			name:       "get sessions",
			path:       "/api/v1/sessions",
			query:      "keyword=test",
			wantStatus: http.StatusOK,
			wantBody:   `{"success":true,"count":0,"sessions":[]}`,
		},
		{
			name:       "get contacts",
			path:       "/api/v1/contacts",
			query:      "limit=200",
			wantStatus: http.StatusOK,
			wantBody:   `{"success":true,"count":0,"contacts":[]}`,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				if r.URL.Path != tt.path {
					t.Errorf("expected path %s, got %s", tt.path, r.URL.Path)
				}
				if tt.query != "" && r.URL.RawQuery != tt.query {
					t.Errorf("expected query %s, got %s", tt.query, r.URL.RawQuery)
				}
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(tt.wantStatus)
				w.Write([]byte(tt.wantBody))
			}))
			defer upstream.Close()

			handler := proxy.NewHandler(upstream.URL)
			proxyServer := httptest.NewServer(handler)
			defer proxyServer.Close()

			url := proxyServer.URL + tt.path
			if tt.query != "" {
				url += "?" + tt.query
			}

			resp, err := http.Get(url)
			if err != nil {
				t.Fatalf("request failed: %v", err)
			}
			defer resp.Body.Close()

			if resp.StatusCode != tt.wantStatus {
				t.Errorf("expected status %d, got %d", tt.wantStatus, resp.StatusCode)
			}

			body, _ := io.ReadAll(resp.Body)
			if string(body) != tt.wantBody {
				t.Errorf("expected body %s, got %s", tt.wantBody, string(body))
			}
		})
	}
}
