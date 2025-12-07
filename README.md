# WPENUM – WordPress Username Enumerator

WPENUM adalah tool sederhana berbasis Python untuk melakukan enumerasi username pada website WordPress.  
Dibuat untuk keperluan **ethical hacking**, **pentest**, dan **bug bounty** — hanya gunakan pada website milik sendiri atau yang memiliki izin.

Tool ini menggunakan 3 teknik utama:

- Enumerasi melalui `/?author=ID`
- REST API: `/wp-json/wp/v2/users`
- RSS Feed: `/feed/`

---

## ✨ Fitur
- Enumerasi username WordPress
- Mendukung delay agar tidak terdeteksi WAF / rate limit
- Opsi `max-id` untuk mengatur kedalaman scanning
- Output clean dan mudah dibaca
- Command-line arguments (`--url`, `--delay`, `--max-id`)
- Aman digunakan untuk pentest legal

---

## 🛠 Cara Install

### Clone repository
```bash
git clone https://github.com/USERNAME/WPENUM.git
cd WPENUM
