# web-read-simple

Reading JSON data from a URL endpoint

## Docker Image

This application is available as a Docker image on Docker Hub: `pipelining/web-read-simple`

### Usage

```bash
docker run -v /path/to/config.json:/config.json \
           -v /path/to/output:/output \
           pipelining/web-read-simple:latest \
           --config /config.json \
           --output /output/data.jsonl
```

With Google authentication (using ADC):
```bash
docker run -v /path/to/config.json:/config.json \
           -v /path/to/output:/output \
           -v /path/to/credentials.json:/credentials.json \
           -e GOOGLE_APPLICATION_CREDENTIALS=/credentials.json \
           pipelining/web-read-simple:latest \
           --config /config.json \
           --output /output/data.jsonl
```

To see this documentation, run without arguments:
```bash
docker run pipelining/web-read-simple:latest
```

## Parameters

| Name            | Required | Description                                                              |
|-----------------|----------|--------------------------------------------------------------------------|
| url             | X        | The URL endpoint to fetch JSON data from                                 |
| useGoogleToken  |          | If true, uses Google Application Default Credentials to add Bearer token |
| scopes          |          | List of OAuth scopes to request (only valid when useGoogleToken is true) |
| headers         |          | Dictionary of custom HTTP headers to include in the request             |

**Notes:**
  * url: The endpoint should return valid JSON data (either a single object or an array of objects)
  * useGoogleToken: When enabled, the pipeline will use ADC to obtain a Google OAuth token and add it as `Authorization: Bearer <token>` header
  * useGoogleToken: Requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set or gcloud to be configured
  * scopes: Optional list of OAuth scopes (e.g., `["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/webmasters"]`). If not specified, default scopes will be used. Can only be used when useGoogleToken is true.
  * headers: Optional dictionary of HTTP headers (e.g., `{"User-Agent": "MyApp/1.0", "Accept-Language": "en-US"}`). These headers will be merged with any authentication headers.
