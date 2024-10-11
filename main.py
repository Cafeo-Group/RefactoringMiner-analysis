
import os
import pandas as pd
from multiprocessing import Pool
import time
from datetime import timedelta 

refactor_miner_path = ''
current_path = os.getcwd()
print(current_path)

def project_analysis(row):
    print(f"git clone {row['link']}")
    os.system(f"git clone {row['link']}")
    try:
        branch = os.popen(f"cd {row['name']} && git rev-parse --abbrev-ref HEAD").read().strip()
        print('branch:', branch)
        print(f"COMMAND: cd {refactor_miner_path} && ./RefactoringMiner -a {current_path}/{row['name']} {branch} -json {current_path}/{row['name']}.json")
        os.system(f"cd {refactor_miner_path} && ./RefactoringMiner -a {current_path}/{row['name']} {branch} -json {current_path}/{row['name']}.json")
    except:
        print(f"ERROR: {row['name']}")
    os.system(f'cd {current_path}')
    os.system(f"rm -rf {row['name']}")
    return

def main():
    df = pd.read_csv('samples-java.csv', sep=';', names=['name', '', 'link'])
    init_time = time.time()
    # print("start at", init_time.strftime("%Y-%m-%d %H:%M:%S"))
    num_cores = os.cpu_count()
    print(f"Number of cores: {num_cores}")
    with Pool(processes=num_cores) as pool:
        pool.map(project_analysis, [row for _, row in df.iterrows()])
    end_time = time.time()
    # print("end at", end_time.strftime("%Y-%m-%d %H:%M:%S"))
    print('Total Time:', str(timedelta(seconds=(end_time - init_time))))

if __name__ == '__main__': 
    main()