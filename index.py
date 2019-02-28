import sys
import requests

debug = False

assert len(sys.argv) >= 2, "Not enough arguments.\nUsage: checkurlvariants.py (baseURL) [destinationURL] [stripTrailingSlash]"

strip_trailing_slash = True
base_url = sys.argv[1]
if len(sys.argv) >= 4:
    strip_trailing_slash = sys.argv[3]
    destination = sys.argv[2]
elif len(sys.argv) >= 3:
    destination = sys.argv[2]
else:
    destination = None


def create_urls(base):
    urls = []
    for index, char in enumerate(base):
        if char == "?":
            if index > 0:
                if base[index-1] == ")":
                    opt = base[base.rindex("(", 0, index)+1:index-1]
                    if debug: print("Optional Segment:", base[base.rindex("(", 0, index)+1:index-1])
                    for index, url in enumerate(urls[:]):
                        urls.append(url[0:len(url) - (len(opt) + 2)])
                        urls[index] = url[0:len(url) - (len(opt) + 2)] + opt
                else:
                    opt = base[index-1]
                    if debug: print("Optional Character:", base[index-1])
                    for index, url in enumerate(urls[:]):
                        urls.append(url[0:len(url) - len(opt)])
                        urls[index] = url[0:len(url) - len(opt)] + opt
            else:
                raise IndexError("First character cannot be a ?")
        else:
            # Normal character
            urls = [x+char for x in urls]
            if len(urls) == 0:
                urls.append(char)
    if debug: print("URLs:",", ".join(urls))
    return urls


urls = create_urls(base_url)

for url in urls:
    final_url = ""
    redirects = 0
    log_str = url
    r = requests.head(url)
    if r.is_redirect:
        redirects += 1
        r2 = requests.head(r.headers["Location"])
        if r2.is_redirect:
            redirects += 1
            final_url = r2.headers["Location"]
            r3 = requests.head(r2.headers["Location"])
            if r3.is_redirect:
                redirects += 1
        else:
            final_url = r.headers["Location"]
    else:
        final_url = url
    if destination:
        if strip_trailing_slash:
            final_url = final_url.rstrip("/")
        if final_url == destination:
            log_str += " - Reached destination"
        else:
            log_str += " - Did not reach destination"
    else:
        log_str += " - " + final_url
    do_plural = "s" if redirects != 1 else ""
    log_str += " (" + str(redirects) + " redirect" + do_plural + ")"
    print(log_str)

print(len(urls), "URLs traversed")
