#!/usr/bin/env python3
"""
Descargador de audio de reels/videos de Instagram por consola.

Descarga el video, extrae el audio a MP3, borra el video y nombra el
archivo con el titulo (caption) del reel.

Uso:
    python descargar_video.py <url> [-o CARPETA] [--cookies-archivo ARCHIVO]
                                    [--cookies-navegador NAVEGADOR] [--formato mp3]

Ejemplos:
    python descargar_video.py https://www.instagram.com/reel/XXXX/
    python descargar_video.py <url> --cookies-archivo www.instagram.com_cookies.txt

Requisitos:
    pip install yt-dlp     (y tener ffmpeg instalado para extraer el audio)
"""

import argparse
import sys
from pathlib import Path

try:
    from yt_dlp import YoutubeDL
except ImportError:
    print("Falta la dependencia 'yt-dlp'. Instalala con:\n")
    print("    pip install yt-dlp\n")
    sys.exit(1)


def descargar(url: str, destino: str, formato: str, cookies_navegador: str | None,
              cookies_archivo: str | None) -> None:
    carpeta = Path(destino)
    carpeta.mkdir(parents=True, exist_ok=True)

    opciones = {
        # Nombre del archivo = titulo/caption del reel (recortado a 150 chars
        # para no pasar el limite de Windows). yt-dlp limpia caracteres invalidos.
        "outtmpl": str(carpeta / "%(title).150B [%(id)s].%(ext)s"),
        # Bajamos el mejor audio disponible; si no hay pista de audio suelta,
        # cae al mejor formato combinado y ffmpeg extrae el audio igual.
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
        # Extrae el audio a MP3 y borra el video original (keepvideo por
        # defecto es False, asi que el video se elimina tras la extraccion).
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": formato,
                "preferredquality": "192",
            }
        ],
    }

    # Autenticacion para contenido privado / que requiere login
    if cookies_navegador:
        opciones["cookiesfrombrowser"] = (cookies_navegador,)
    elif cookies_archivo:
        opciones["cookiefile"] = cookies_archivo

    print(f"Descargando y extrayendo audio de: {url}")
    print(f"Destino: {carpeta.resolve()}\n")

    with YoutubeDL(opciones) as ydl:
        ydl.download([url])

    print("\nListo. Audio extraido correctamente.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Descarga un reel/video de Instagram y guarda solo el audio."
    )
    parser.add_argument("url", help="URL del reel o video de Instagram")
    parser.add_argument(
        "-o", "--output", default=".",
        help="Carpeta de destino (por defecto: la carpeta actual)",
    )
    parser.add_argument(
        "--formato", default="mp3",
        help="Formato de audio de salida (mp3, m4a, wav, opus...). Por defecto: mp3",
    )
    parser.add_argument(
        "--cookies-navegador", metavar="NAVEGADOR",
        help="Lee cookies de tu navegador (chrome, firefox, edge, brave...)",
    )
    parser.add_argument(
        "--cookies-archivo", metavar="ARCHIVO",
        help="Ruta a un archivo cookies.txt",
    )
    args = parser.parse_args()

    try:
        descargar(args.url, args.output, args.formato,
                  args.cookies_navegador, args.cookies_archivo)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        print(
            "\nNotas:\n"
            "  - Para extraer el audio necesitas 'ffmpeg' instalado.\n"
            "  - Si el video es privado usa --cookies-archivo o --cookies-navegador.\n"
            "  - Actualiza yt-dlp:  pip install -U yt-dlp",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
