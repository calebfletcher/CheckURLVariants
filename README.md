# CheckURLVariants

A small script to check the redirects of variants of a base URL. The current version of the script is currently arbitrarily limited to 3 redirects

## Usage
`checkurlvariants.py (baseURL) [destinationURL] [stripTrailingSlash]`

The format of the base URL is a very simplified version of Regex, with only the `?` operator and the `()` groups being implemented. For example, the URL string `https?://(www.)example.com` will generate:
- `http://example.com`
- `http://www.example.com`
- `https://example.com`
- `https://www.example.com`

If destinationURL is set, the output from the script changes to indicate whether the URL being tested redirects to the destination URL.
If stripTrailingSlash is set, the check whether the final redirected URL is equal to the destination URL will ignore any trailing slashes in the redirected URL. This does not have any effect when destinationURL is not set, and defaults to `True`. This argument can be set to any falsy value as defined in the Python specification regarding booleans.

## Debugging
An internal variable named `debug` enables the debugging output of the script.
