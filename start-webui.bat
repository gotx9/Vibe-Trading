@echo off
title Vibe-Trading Web UI Launcher

echo =============================================
echo   Vibe-Trading Web UI (Dev Mode)
echo =============================================
echo.
echo Backend API  : http://localhost:8899
echo Frontend UI  : http://localhost:5899
echo.
echo Starting services in separate windows...
echo Close those windows to stop.
echo =============================================

:: Backend (API server)
start "Vibe-Trading API Server" cmd /k "cd /d E:\GH\Vibe-Trading && call .venv\Scripts\activate.bat && vibe-trading serve --port 8899"

:: Frontend (Vite dev server - proxies API to :8899)
start "Vibe-Trading Frontend" cmd /k "cd /d E:\GH\Vibe-Trading\frontend && npm run dev"

echo.
echo Both services launched. Open http://localhost:5899 in your browser.
echo.

timeout /t 3 >nul
exit
