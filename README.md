# server-feed

# Service File
## To edit file
sudo nano /etc/systemd/system/serverfeed.service
## File
```
[Unit]
Description=Server event logger for PavlovVR Dedicated server

[Service]
Type=simple
WorkingDirectory=/home/steam/logger
ExecStart=/home/steam/steam/logger/start.sh

StandardOutput=append:/var/log/pavlovLogger.log
StandardError=append:/var/log/pavlovLogger.log

RestartSec=1
Restart=always
User=steam
Group=steam

[Install]
WantedBy = multi-user.target
```
