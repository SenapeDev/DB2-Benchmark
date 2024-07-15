import pandas as pd
import concurrent.futures

def generate_csv_versions(file_name):
    try:
        # Apre il file CSV
        df = pd.read_csv(file_name, delimiter=',', quotechar='"', quoting=1, skipinitialspace=True)
        
        # Genera le versioni ridotte
        for percent in [100, 75, 50, 25]:
            sampled_df = df.sample(frac=percent/100, random_state=1)
            new_file_name = f"dataset{percent}/{file_name.split('.')[0]}_{percent}.csv"
            sampled_df.to_csv(new_file_name, index=False, sep=',')
            print(f"File salvato: {new_file_name}")
    except Exception as e:
        print(f"Errore durante l'elaborazione del file {file_name}: {e}")

file_list = [
    'accounts.csv',
    'companies.csv',
    'directors.csv',
    'persons.csv',
    'shareholders.csv',
    'transactions.csv'
]

# Utilizzo del multithreading per generare i file
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(generate_csv_versions, file_list)
