#!/usr/bin/env python3
"""
OpenAI DALL·E 3 ile sektör görselleri üretir; assets/sektor/ai/ altına kaydeder.
Kullanım: OPENAI_API_KEY=sk-... python3 scripts/generate_openai_images.py

Anahtarı asla repoya commit etmeyin.
"""
from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sektor" / "ai"
OUT.mkdir(parents=True, exist_ok=True)

# Marka metni modele verilir; okunabilirlik için sayfada ayrıca HTML overlay da kullanılacak.
BRAND = (
    "Small elegant white text watermark in the bottom right corner reading exactly "
    "'ÖZN LuckyCare', sans-serif, professional corporate style, subtle opacity."
)

STYLE = (
    "Cinematic professional photography, premium tech company aesthetic, "
    "deep navy blue (#0f2848) and electric sky blue (#3b82f6 / #7dd3fc) color grading, sharp detail, "
    "no cluttered text except the brand watermark, 8k quality."
)

JOBS: list[tuple[str, str, str, list[str]]] = [
    (
        "5g",
        "5G cellular network towers at twilight, fiber optic light trails, industrial IoT campus, futuristic connectivity",
        "1792x1024",
        [
            "5G private network server room with blue LED racks and network diagrams on monitors",
            "Engineer with tablet inspecting 5G small cell antenna on rooftop, safety vest, golden hour",
            "Abstract visualization of low-latency data streams and edge computing nodes, soft blue glow",
        ],
    ),
    (
        "guvenlik",
        "High-tech security command center with surveillance wall, dark room cool blue highlights, professional",
        "1792x1024",
        [
            "Biometric access control gate at modern facility, glass and steel, night",
            "Cybersecurity analyst dual monitors with network map, dark office",
            "Perimeter fence with sensors and camera poles, dramatic sky",
        ],
    ),
    (
        "kamera",
        "Smart city CCTV and AI analytics concept, urban street at night, blue accent lighting, cinematic",
        "1792x1024",
        [
            "IP security camera array on building corner, shallow depth of field",
            "Video wall operator room, multiple camera feeds, calm professional",
            "Retail store ceiling dome cameras, clean interior lighting",
        ],
    ),
    (
        "drone",
        "Professional surveying drone over landscape at sunrise, dramatic light, tech precision",
        "1792x1024",
        [
            "Drone controller with telemetry tablet in hands, outdoor mission",
            "Thermal imaging camera payload close-up on drone, engineering detail",
            "Aerial view of industrial site inspection, geometric patterns",
        ],
    ),
    (
        "iot",
        "Smart city skyline at night with connected lights, IoT sensors concept, futuristic sustainable city",
        "1792x1024",
        [
            "Smart streetlight with environmental sensor module, urban boulevard",
            "City operations dashboard on large screen, traffic and utilities data",
            "Water and energy smart meters in utility room, clean composition",
        ],
    ),
    (
        "ev",
        "Luxury modern smart home living room, hidden LED strips, voice assistant panel, warm and tech",
        "1792x1024",
        [
            "Smart thermostat and lighting control on wall tablet, minimal interior",
            "Automated blinds and smart kitchen appliances, daylight",
            "Family using smartphone for home automation app, cozy evening",
        ],
    ),
    (
        "yat",
        "Luxury yacht helm at sea, polished wood and glass instruments, navigation screens, ocean horizon",
        "1792x1024",
        [
            "Marine electrical panel and batteries in yacht engine room, tidy cabling",
            "Captain bridge touchscreen navigation, turquoise water outside",
            "Solar panels on yacht deck, nautical lifestyle technology",
        ],
    ),
    (
        "yapay-zeka",
        "Abstract AI neural network hologram over dark server room, blue light particles, futuristic, no gibberish text",
        "1792x1024",
        [
            "Data scientist workstation with ML training curves on monitors",
            "Robot arm quality inspection with vision system in factory",
            "Cloud API integration diagram holographic style, clean vectors",
        ],
    ),
    (
        "yasli",
        "Warm compassionate elderly care technology, wearable and calm sensors at home, soft light, respectful",
        "1792x1024",
        [
            "Emergency call pendant and discreet room sensor on shelf, home setting",
            "Tablet telehealth call with doctor, senior person on sofa, gentle",
            "Caregiver notification smartphone app mockup style scene, not literal UI text",
        ],
    ),
    (
        "medikal",
        "Modern hospital corridor with digital displays, medical technology, clean sterile cool white and blue lighting",
        "1792x1024",
        [
            "Medical imaging workstation radiology, professional healthcare IT",
            "Patient monitor devices networked in ICU soft focus background",
            "Telemedicine cart with camera and peripherals in clinic room",
        ],
    ),
]


def api_generate(prompt: str, size: str, api_key: str) -> str:
    body = {
        "model": "dall-e-3",
        "prompt": f"{prompt}. {STYLE} {BRAND}",
        "n": 1,
        "size": size,
        "quality": "standard",
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=300, context=ctx) as resp:
        payload = json.loads(resp.read().decode())
    return payload["data"][0]["url"]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest)


def main() -> None:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        print("OPENAI_API_KEY ortam değişkeni gerekli.")
        raise SystemExit(1)

    total = 0
    for slug, hero_prompt, hero_size, gallery_prompts in JOBS:
        print(f"\n=== {slug} ===")
        # Hero
        path_hero = OUT / f"{slug}-hero.png"
        if path_hero.exists():
            print(f"  atlanıyor (var): {path_hero.name}")
        else:
            url = api_generate(hero_prompt, hero_size, key)
            download(url, path_hero)
            print(f"  kaydedildi: {path_hero.name}")
            total += 1
            time.sleep(2.5)

        for i, gp in enumerate(gallery_prompts, start=1):
            path_g = OUT / f"{slug}-{i}.png"
            if path_g.exists():
                print(f"  atlanıyor (var): {path_g.name}")
                continue
            url = api_generate(gp, "1024x1024", key)
            download(url, path_g)
            print(f"  kaydedildi: {path_g.name}")
            total += 1
            time.sleep(2.5)

    print(f"\nTamamlandı. Bu çalışmada yeni indirilen görsel: {total}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="replace")
        print("HTTP hata:", e.code, err)
        raise SystemExit(1)
