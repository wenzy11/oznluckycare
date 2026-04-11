# ÖZN LuckyCare — statik site

## GitHub + Vercel

1. GitHub’da yeni bir repository oluştur (boş, README ekleme).
2. Bu klasörde:

```bash
git remote add origin https://github.com/KULLANICI_ADIN/REPO_ADI.git
git branch -M main
git push -u origin main
```

3. [vercel.com/new](https://vercel.com/new) → **Import Git Repository** → repoyu seç → **Deploy** (Framework: Other, Build Command boş, Output: `.` / kök).

Site `*.vercel.app` adresinde yayına alınır; sonraki `git push` ile otomatik yeniden deploy olur.
