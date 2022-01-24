from time import sleep
import subprocess
import logging
import os
import re


SITE_NAME = "check_mk"
PATH_LOG = ""
FILE_NAME = "cmkstatus.log"

pros_status = subprocess.Popen(
    f"omd status {SITE_NAME}", shell=True, stdout=subprocess.PIPE
)
logging.basicConfig(
    filename=os.path.join(PATH_LOG, FILE_NAME),
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("Service")

output = pros_status.stdout.read().decode()

dict_service = {}

for out in output.split("\n"):
    if "------" in out:
        break
    splited = out.split(":")
    dict_service[splited[0].strip()] = splited[1].strip()

for service, status in dict_service.items():
    if status == "stopped":
        logger.critical(f"O Serviço: {service} parou!")
        pros_restart = subprocess.Popen(
            f"omd restart check_mk {service}",
            shell=True,
            stdout=subprocess.PIPE,
        )
        restarted = pros_restart.stdout.read().decode()
        if re.search(f"Starting {service}(.*?)...OK", restarted):
            logger.info(f"O serviço {service} foi restartado com sucesso.")
        else:
            logger.critical(f"O restart do serviço {service} falhou")
            logger.critical(restarted)
