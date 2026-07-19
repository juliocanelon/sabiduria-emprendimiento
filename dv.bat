@echo off
REM Descarga el audio de un reel/video de Instagram.
REM Uso:  descargar-video "URL_DEL_REEL"
REM
REM Usa el script y las cookies que estan en esta misma carpeta,
REM sin importar desde donde lo ejecutes.

if "%~1"=="" (
    echo Uso: descargar-video "URL_DEL_REEL"
    exit /b 1
)

python "%~dp0descargar_video.py" "%~1" --cookies-archivo "%~dp0www.instagram.com_cookies.txt"
