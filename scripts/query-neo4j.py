import time
import csv
from neo4j import GraphDatabase

# Lista delle query
query_list = [
    """
    MATCH (a:Account)
    WHERE a.bank_country = "IT"
    RETURN a.balance AS Balance
    ORDER BY a.balance DESC
    LIMIT 5;
    """,
    """
    MATCH (:Company)<-[:DIRECTS]-(d:Person)-[:HAS_ACCOUNT]->(a:Account)
    RETURN d.first_name AS Name,
    d.last_name AS Surname,
    a.account_number AS IBAN,
    a.balance AS Balance
    ORDER BY Balance DESC;
    """,
    """
    MATCH (s:Account)-[t:HAS_TRANSACTION]->(r:Account)
    WHERE s.bank_country = r.bank_country
    AND t.amount > 600000
    RETURN s.account_number AS Sender, 
    r.account_number AS Receiver, 
    t.amount AS Amount, 
    t.transaction_date AS Date
    ORDER BY Date DESC;
    """,
    """
    MATCH (p:Person)-[owns:OWNS_PART_OF]->(c:Company)<-[:DIRECTS]-(d:Person)-[:HAS_ACCOUNT]->(a:Account)
    WHERE owns.percentage > 0.50
    AND d.nationality <> p.nationality
    AND a.balance > 250000
    RETURN p.first_name AS UBO_name,
    p.last_name AS UBO_surname,
    owns.percentage AS percentage,
    d.first_name AS Director_name,
    d.last_name AS Director_surname,
    a.balance AS Director_balance
    ORDER BY percentage DESC;
    """
]

# Dati di connessione al database neo4j
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

# Funzione per eseguire una query e registrare il tempo di esecuzione
def execute_query(query, query_num):
    filename = f"times_query_{query_num}.csv"
    times = []

    with driver.session() as session:
        for i in range(31):
            print(f"Esecuzione {i + 1} per la query {query_num}")
            start_time = time.perf_counter()
            try:
                session.run(query)
            except Exception as e:
                print(f"Errore durante l'esecuzione della query {query_num}: {e}")
                times.append(float('nan'))  # Registra il fallimento con NaN
                continue
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            times.append(execution_time)

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Run", "Execution Time"])
        for i, exec_time in enumerate(times):
            writer.writerow([i + 1, exec_time])

        # Calcola e salva la media delle esecuzioni (escludendo NaN e la prima esecuzione)
        valid_times = [t for t in times[1:] if not (t != t)]  # esclude NaN
        if valid_times:
            average_time = sum(valid_times) / len(valid_times)
            writer.writerow(["Media", average_time])
        else:
            writer.writerow(["Media", "N/A"])

# Esegui le query una alla volta e salva i tempi in file CSV separati
for i, query in enumerate(query_list):
    execute_query(query, i + 1)

print("Script completato. I tempi di esecuzione sono stati salvati nei file CSV.")

# Chiudi il driver al termine
driver.close()
