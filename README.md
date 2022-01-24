# CMKstatus

The script was created with the purpose of helping the maintaining the integrity of monitoring the CheckMk. Created and testing on version 2.0 raw edition.

Add a entrace in crontab for execute periodicly the checking status and restart if service status is *stopped*


As a sudo user

```
contrab -e
```

To run every 5 minute

```bash
*/1  *  * * *   /usr/bin/python3 statuscmk.py
```
