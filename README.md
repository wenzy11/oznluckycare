# ÖZN LuckyCare — statik site

## GitHub’a bağlama

**Önemli:** Aşağıdaki URL’de `senin-kullanici-adin` ve `repo-adi` kısımlarını GitHub’daki gerçek değerlerinle değiştir. Örnek: `https://github.com/w3nzy/ozn-luckycare.git`

1. [github.com/new](https://github.com/new) ile **boş** repo oluştur (README ekleme).

2. Terminalde proje klasöründe:

```bash
cd "/Users/w3nzy/Desktop/adsız klasör 5"

# Daha önce hatalı origin eklediysen önce sil:
# git remote remove origin

git remote add origin https://github.com/senin-kullanici-adin/repo-adi.git
git branch -M main
git push -u origin main
```

3. `git push` şifre istememeli; istiyorsa GitHub artık **şifre kabul etmiyor**. [Personal Access Token](https://github.com/settings/tokens) oluşturup şifre yerine yapıştır veya [SSH anahtarı](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) kullan.

## Vercel

[vercel.com/new](https://vercel.com/new) → **Import Git Repository** → repoyu seç → **Deploy** (Framework: Other, build yok).
