### Filters I’m using (tweak as needed)

```
{job="prometheus-example-app", namespace="ns1"}
```

### 1) Request rate (RPS)

```
sum by (method, handler) (
  rate(http_requests_total{job="prometheus-example-app", namespace="ns1"}[5m])
)
```

### 2) Error rate (%)

```
100 *
sum(
  rate(http_requests_total{job="prometheus-example-app", namespace="ns1", code!~"2.."}[5m])
)
/
sum(
  rate(http_requests_total{job="prometheus-example-app", namespace="ns1"}[5m])
)
```

### 3) Latency SLOs (p50/p90/p95/p99)

```
histogram_quantile(0.50,
  sum by (le) (
    rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1"}[5m])
  )
)
```

```
histogram_quantile(0.90,
  sum by (le) (
    rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1"}[5m])
  )
)
```

```
histogram_quantile(0.95,
  sum by (le) (
    rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1"}[5m])
  )
)
```

```
histogram_quantile(0.99,
  sum by (le) (
    rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1"}[5m])
  )
)
```

### 4) Per-pod breakdown (who’s slow)

```
histogram_quantile(0.95,
  sum by (pod, le) (
    rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1"}[5m])
  )
)
```

### 5) Availability (app “up” over time)

```
100 * avg_over_time(
  up{job="prometheus-example-app", namespace="ns1"}[1h]
)
```

### 6) Apdex-style score (T=0.5s, tolerate=1s)

```
(
  sum(rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1", le="0.5"}[5m]))
+ 0.5 * sum(rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1", le="1"}[5m]))
)
/
sum(rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1", le="+Inf"}[5m]))
```

### 7) Golden signals by handler (great for dashboards)

**RPS**

```
sum by (handler) (rate(http_requests_total{job="prometheus-example-app", namespace="ns1"}[5m]))
```

**Error %**

```
100 * sum by (handler) (rate(http_requests_total{job="prometheus-example-app", namespace="ns1", code!~"2.."}[5m]))
/
sum by (handler) (rate(http_requests_total{job="prometheus-example-app", namespace="ns1"}[5m]))
```

**p95 latency**

```
histogram_quantile(0.95,
  sum by (handler, le) (
    rate(http_request_duration_seconds_bucket{job="prometheus-example-app", namespace="ns1"}[5m])
  )
)
```

