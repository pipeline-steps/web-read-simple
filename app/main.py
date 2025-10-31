import sys
import timeit
import requests
from google.auth import default
from google.auth.transport.requests import Request
from steputil import StepArgs, StepArgsBuilder


def main(step: StepArgs):
    # prepare headers - start with custom headers if provided
    headers = {}
    if step.config.headers:
        headers.update(step.config.headers)
        print(f"Using custom headers: {list(step.config.headers.keys())}")

    # optionally add Google authentication
    if step.config.useGoogleToken:
        print("Getting credentials from Application Default Credentials (ADC)")
        try:
            scopes = step.config.scopes
            if scopes:
                print(f"Using scopes: {scopes}")
                credentials, project = default(scopes=scopes)
            else:
                credentials, project = default()
            credentials.refresh(Request())
            token = credentials.token
            headers['Authorization'] = f'Bearer {token}'
            print(f"Added Bearer token to request headers")
        except Exception as e:
            print(f"Error during authentication: {e}", file=sys.stderr)
            sys.exit(1)

    # fetch JSON data from URL
    start_time = timeit.default_timer()
    url = step.config.url
    print(f"Fetching JSON data from: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}, {response.text}", file=sys.stderr)
        sys.exit(1)

    data = response.json()
    execution_time = timeit.default_timer() - start_time

    # Handle both single object and array of objects
    if isinstance(data, dict):
        records = [data]
        print(f"Read 1 JSON object in {execution_time:.1f} seconds.")
    elif isinstance(data, list):
        records = data
        print(f"Read {len(records)} JSON objects in {execution_time:.1f} seconds.")
    else:
        raise ValueError(f"Unexpected JSON data type: {type(data)}")

    # store to output file
    step.output.writeJsons(records)

    print(f"Done")


def validate_config(config):
    """Validation function that checks config rules."""
    # Check that scopes is only used when useGoogleToken is true
    if config.scopes and not config.useGoogleToken:
        print("Parameter `scopes` can only be used when `useGoogleToken` is true", file=sys.stderr)
        return False

    # Check that Authorization header doesn't conflict with useGoogleToken
    if config.useGoogleToken and config.headers:
        if 'Authorization' in config.headers:
            print("Cannot use `useGoogleToken` when custom `Authorization` header is provided in `headers`", file=sys.stderr)
            return False

    return True


if __name__ == "__main__":
    main(StepArgsBuilder()
         .output()
         .config("url")
         .config("useGoogleToken", optional=True)
         .config("scopes", optional=True)
         .config("headers", optional=True)
         .validate(validate_config)
         .build()
         )
