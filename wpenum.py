#!/usr/bin/env python3
import argparse
import time
import requests
from urllib.parse import urljoin

# ============================
#  COLORS
# ============================
BLUE = "\033[94m"
WHITE = "\033[97m"
RESET = "\033[0m"

# ============================
#  HEADER (BANNER MINIMALIS)
# ============================
def banner():
    print(BLUE + "\n[ WPENUM ]" + RESET + WHITE + " WordPress Username Enumerator" + RESET)
    print(BLUE + "Author :" + RESET + WHITE + " iyanji" + RESET)
    print(BLUE + "-----------------------------------------\n" + RESET)

# ============================
#  ENUM FUNCTIONS
# ============================
def check_author_id(base_url, max_id, delay):
    found = []
    print("[*] Checking /?author=")
    for i in range(1, max_id + 1):
        url = base_url + f"/?author={i}"
        try:
            r = requests.get(url, timeout=10, allow_redirects=True)
            if "/author/" in r.url:
                user = r.url.split("/author/")[1].strip("/").split("/")[0]
                if user not in found:
                    found.append(user)
                print(f"[+] Found username from author ID {i}: {user}")
        except:
            pass

        time.sleep(delay)
    return found


def check_rest_api(base_url, delay):
    print("\n[*] Checking REST API /wp-json/wp/v2/users")
    rest_url = base_url + "/wp-json/wp/v2/users"
    try:
        r = requests.get(rest_url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            found = [u["slug"] for u in data]
            for u in found:
                print(f"[+] Found username via REST API: {u}")
            time.sleep(delay)
            return found
    except:
        pass

    print("[-] REST API blocked/disabled")
    return []


def check_rss(base_url, delay):
    print("\n[*] Checking RSS feed /feed/")
    feed_url = base_url + "/feed/"
    found = []
    try:
        r = requests.get(feed_url, timeout=10)
        for line in r.text.splitlines():
            if "<dc:creator>" in line:
                user = line.replace("<dc:creator><![CDATA[", "").replace("]]></dc:creator>", "").strip()
                found.append(user)
                print(f"[+] Found username in RSS feed: {user}")
        time.sleep(delay)
        return found
    except:
        return []


# ============================
#  MAIN FUNCTION
# ============================
def main():
    parser = argparse.ArgumentParser(
        description="WPENUM – WordPress Username Enumerator by iyanji"
    )

    parser.add_argument(
        "--url",
        required=True,
        help="Target WordPress site (contoh: https://example.com)"
    )

    parser.add_argument(
        "--max-id",
        type=int,
        default=10,
        help="Author ID range (default: 10)"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay setiap request agar tidak terdeteksi (default: 1 detik)"
    )

    args = parser.parse_args()
    base_url = args.url.rstrip("/")
    delay = args.delay
    max_id = args.max_id

    banner()
    print("URL:", base_url)
    print("Delay:", delay, "detik")
    print("Max ID:", max_id)
    print("\n=== START ENUMERATION ===\n")

    usernames = set()
    usernames.update(check_author_id(base_url, max_id, delay))
    usernames.update(check_rest_api(base_url, delay))
    usernames.update(check_rss(base_url, delay))

    print("\n=== RESULT ===")
    if usernames:
        for u in usernames:
            print(f"[FOUND] {u}")
    else:
        print("Tidak ada username ditemukan.")


if __name__ == "__main__":
    main()
