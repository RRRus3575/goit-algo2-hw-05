import json
from datasketch import HyperLogLog
import time
import pandas as pd 

file = "./lms-stage-access.log"

hll = HyperLogLog(p=10)
set_data = set()

with open(file, "r", encoding="utf-8") as f:
    for line in f:
        try:
            log_entry = json.loads(line)  
            ip = log_entry.get("remote_addr")  
            if isinstance(ip, str):  
                set_data.add(ip)    
                hll.update(ip.encode("utf-8"))

        except json.JSONDecodeError:
            continue  

def count_unique_ips_set(data):         
    return len(data)


def count_unique_ips_hyperloglog(data): 
    return data.count()



start_time_set = time.perf_counter()
unique_ips_set = count_unique_ips_set(set_data)
end_time_set = time.perf_counter()
time_set = end_time_set - start_time_set

start_time_hll = time.perf_counter()
unique_ips_hll = count_unique_ips_hyperloglog(hll)
end_time_hll = time.perf_counter()
time_hll = end_time_hll - start_time_hll

df = pd.DataFrame({
    "Метод": ["Точний підрахунок", "HyperLogLog"],
    "Унікальні елементи": [unique_ips_set, unique_ips_hll],
    "Час виконання (сек.)": [time_set, time_hll]
})


print(df.to_string(index=False))