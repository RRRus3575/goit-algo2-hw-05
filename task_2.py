import json
from datasketch import HyperLogLog
import timeit

file = "./lms-stage-access.log"

set_data = set()
hll = HyperLogLog(p=14)

with open(file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                log_entry = json.loads(line)  
                ip = log_entry.get("remote_addr")
                if str(ip):  
                    set_data.add(ip)
                    hll.update(ip.encode("utf-8"))

            except json.JSONDecodeError:
                continue  

def count_unique_ips_set(data):     
    return len(data)


def count_unique_ips_hyperloglog(data):    
    return data.count()



time_set = timeit.timeit(lambda: count_unique_ips_set(set_data), number=1)
time_hyperloglog = timeit.timeit(lambda: count_unique_ips_hyperloglog(hll), number=1)

print(f"Час виконанная методу Set(): {time_set} \n Унікальних IP-адрес: {count_unique_ips_set(set_data)}")
print(f"Час виконанная методу Hyperloglog: {time_hyperloglog} \n Унікальних IP-адрес: {count_unique_ips_hyperloglog(hll)}")