@echo off
git add .
git commit -m "Automated update %date% %time%"
git push origin main
echo System Sync Complete.
pause