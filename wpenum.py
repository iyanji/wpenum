import requests
from urllib.parse import urljoin

# ===============================
# WORDPRESS USERNAME ENUMERATOR
# Legal use only – for testing your own site
# ===============================

def check_author_id(base_url, max_id=10):
    found = []
    print("[*] Checking /?author= method...")
    for i in range(1, max_id + 1):
        url = base_url + f"/?author={i}"
        r = requests.get(url, allow_redirects=True)
        if "/author/" in r.url:
            username = r.url.split("/author/")[1].strip("/").split("/")[0]
            found.append(username)
            print(f"[+] Found username from author ID {i}: {username}")
    return found


def check_rest_api(base_url):
    print("\n[*] Checking REST API /wp-json/wp/v2/users")
    rest_url = base_url + "/wp-json/wp/v2/users"
    try:
        r = requests.get(rest_url)
        if r.status_code == 200:
            data = r.json()
            found = [user["slug"] for user in data]
            for user in found:
                print(f"[+] Found username from REST API: {user}")
            return found
    except:
        pass
    print("[-] REST API blocked or disabled")
    return []


def check_rss(base_url):
    print("\n[*] Checking RSS feed /feed/")
    feed_url = base_url + "/feed/"
    try:
        r = requests.get(feed_url)
        found = []
        for line in r.text.splitlines():
            if "<dc:creator>" in line:
                username = line.replace("<dc:creator><![CDATA[", "").replace("]]></dc:creator>", "").strip()
                found.append(username)
                print(f"[+] Found username in RSS feed: {username}")
        return found
    except:
        return []


def main():
    base_url = input("Masukkan URL WordPress (contoh: https://example.com): ").strip()

    print("\n=== ENUMERATING USERNAMES ===\n")

    usernames = set()

    usernames.update(check_author_id(base_url))
    usernames.update(check_rest_api(base_url))
    usernames.update(check_rss(base_url))

    print("\n=== HASIL AKHIR ===")
    if usernames:
        for u in usernames:
            print(f"[FOUND] Username: {u}")
    else:
        print("Tidak ada username yang bisa ditemukan (site aman).")


if __name__ == "__main__":
    main()

