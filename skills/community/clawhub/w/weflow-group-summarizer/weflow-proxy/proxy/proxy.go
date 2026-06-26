package proxy

import (
	"bytes"
	"context"
	"io"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strconv"
	"strings"
)

type contextKey int

const incomingHostKey contextKey = iota

// NewHandler creates an http.Handler that reverse-proxies all requests
// to the given upstream URL. It panics if upstream is not a valid URL,
// as this is expected to be called once at startup with a known-good value.
//
// JSON responses have upstream URLs rewritten to the proxy's host,
// so that clients can follow mediaUrl links directly.
func NewHandler(upstream string) http.Handler {
	target, err := url.Parse(upstream)
	if err != nil {
		panic("invalid upstream URL: " + err.Error())
	}

	upstreamOrigin := []byte(target.Scheme + "://" + target.Host)

	rp := &httputil.ReverseProxy{
		Rewrite: func(r *httputil.ProxyRequest) {
			ctx := context.WithValue(r.Out.Context(), incomingHostKey, r.In.Host)
			r.Out = r.Out.WithContext(ctx)
			r.SetURL(target)
		},
		ModifyResponse: func(resp *http.Response) error {
			if !strings.HasPrefix(resp.Header.Get("Content-Type"), "application/json") {
				return nil
			}

			body, err := io.ReadAll(resp.Body)
			resp.Body.Close()
			if err != nil {
				return err
			}

			if host, ok := resp.Request.Context().Value(incomingHostKey).(string); ok && host != "" {
				proxyOrigin := []byte("http://" + host)
				body = bytes.ReplaceAll(body, upstreamOrigin, proxyOrigin)
			}

			resp.Body = io.NopCloser(bytes.NewReader(body))
			resp.ContentLength = int64(len(body))
			resp.Header.Set("Content-Length", strconv.Itoa(len(body)))
			return nil
		},
	}

	return rp
}
