import requests
import threading
from datetime import datetime

MS_BUREAU_URL = "http://localhost:8081/api/v1/kyc"
cpfs = []
errors_list = []

errors = open("assets\errors.txt", "a")

def get_time():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

print(f"start: {get_time()}")


with open("assets\list.txt", "r") as list:
    lines = list.read().split('\n')

for line in lines:
    cpfs.append(line.replace('.', '').replace('-', ''))


def data_lake(cpf):
    url = f"{MS_BUREAU_URL}/{cpf}"
    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(response.text)

    except Exception as e:
        errors_list.append(f"DOCUMENT: {cpf}, ERROR: {str(e)}\n")

threads = []

for cpf in cpfs:
    t = threading.Thread(target=data_lake, args=[cpf])
    threads.append(t)

    t.start()

for t in threads:
    t.join()

errors.write("\n".join(errors_list))
errors.close()
print(f"end: {get_time()}")

