import subprocess
import logging

pros_status = subprocess.Popen("omd status check_mk", shell=True, stdout=subprocess.PIPE)
logging.basicConfig(filename="teste.log", format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)

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
        pros_restart = subprocess.Popen(f"omd restart check_mk {service}", shell=True, stdout=subprocess.PIPE)
        restarted = pros_restart.stdout.read().decode()
        if f"Starting {service}...OK" in restarted:
            logger.info(f"O serviço {service} foi restartado com sucesso.")
        else:
            logger.critical(f"O restart do serviço {service} falhou")
            logger.critical(restarted)
