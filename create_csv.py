
import os
import pandas as pd
from multiprocessing import Pool
import time
import json
from datetime import timedelta 

def main():
    df = pd.read_csv('samples-java.csv', sep=';', names=['name', '', 'link'])
    df_final = pd.DataFrame()
    df_final2 = pd.DataFrame()
    for _, row in df.iterrows():
        json_ = pd.read_json(f'{row["name"]}.json')
        df2 = pd.DataFrame.from_records(json_['commits'])
        df_final = pd.concat([df_final, df2])
        df3 = df2[df2['refactorings'].apply(lambda x: len(x) > 0)]
        df4 = pd.DataFrame(columns=['repository', 'sha1', 'type', 'description', 'leftSideLocations', 'rightSideLocations'])
        for i, row in df3.iterrows():
            df_aux = pd.DataFrame.from_records(row['refactorings'])
            df_aux['repository'] = row['repository']
            df_aux['sha1'] = row['sha1']
            df4 = pd.concat([df4, df_aux])
        df_final2 = pd.concat([df_final2, df4])
    df_final.to_csv('refactoring_analysis_general.csv', index=False)
    df_final2.to_csv('refactoring_analysis_details.csv', index=False)
if __name__ == '__main__': 
    main()