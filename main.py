import pandas as pd
import tqdm
#from orientdb_client import OrientDBClient

chunksize = 1000

reader = pd.read_csv('data.csv', chunksize=chunksize, sep=" ")
pbar = tqdm.tqdm(reader, total=1000000)

with OrientDBClient(host="localhost", port=2424, user="root", password="root", database="graphdb") as client:
    for chunk in pbar:
        source = chunk['source']
        target = chunk['target']
        timestamp = chunk['timestamp']
        interaction = chunk['interaction']
        client.create_edge(source, target, interaction)
        pbar.update(chunksize)

pbar.close()

