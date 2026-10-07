@echo off
REM ALGENZA Explainer Video Engine - Windows 1-Click Builder
echo =================================================================
echo     ALGENZA VIDEO ENGINE - HIGH-PERFORMANCE VIDEO BUILDER
echo     algenza.com  -  Lead Architect: Muhammad Hassan
echo =================================================================

set TARGET=%1
if "%TARGET%"=="" set TARGET=16:9

if "%TARGET%"=="titan" (
    python cli.py titan --workers 4
) else (
    python cli.py build --aspect %TARGET% --workers 4
)

echo.
echo Build finished! Check assets\ directory.
pause
