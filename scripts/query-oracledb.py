import time
import csv
import cx_Oracle

# Dati di connessione al database Oracle
dsn = cx_Oracle.makedsn("localhost", 1521)
connection = cx_Oracle.connect(user="SYSTEM", password="12345678", dsn=dsn)

# Lista delle query
queries = [
    """
    SELECT balance AS Balance
    FROM Accounts
    WHERE bank_country = 'IT'
    ORDER BY balance DESC
    FETCH FIRST 5 ROWS ONLY
    """,
    """
    SELECT p.first_name AS Name, p.last_name AS Surname, a.account_number AS IBAN, a.balance AS Balance
    FROM Persons p
    JOIN Directors d ON p.id = d.person_id
    JOIN Accounts a ON p.id = a.owner_id
    ORDER BY a.balance DESC
    """,
    """
    SELECT 
        s.account_number AS Sender,
        r.account_number AS Receiver,
        t.amount AS Amount,
        t.transaction_date AS Transaction_date
    FROM Transactions t
    JOIN Accounts s ON t.sender_id = s.id
    JOIN Accounts r ON t.receiver_id = r.id
    WHERE s.bank_country = r.bank_country
    AND t.amount > 600000
    ORDER BY t.transaction_date DESC
    """,
    """
    SELECT 
        ubo.first_name AS UBO_name,
        ubo.last_name AS UBO_surname,
        sh.percentage AS percentage,
        dir.first_name AS Director_name,
        dir.last_name AS Director_surname,
        acc.balance AS Director_balance
    FROM Shareholders sh
    JOIN Persons ubo ON sh.entity_id = ubo.id
    JOIN Companies c ON sh.company_id = c.id
    JOIN Directors d ON c.id = d.company_id
    JOIN Persons dir ON d.person_id = dir.id
    JOIN Accounts acc ON dir.id = acc.owner_id
    WHERE sh.percentage > 0.5
    AND ubo.nationality <> dir.nationality
    AND acc.balance > 250000
    ORDER BY sh.percentage DESC
    """
]

# Funzione per eseguire una query e registrare il tempo di esecuzione
def execute_query(query, query_num):
    filename = f"times_query_{query_num}.csv"
    times = []

    print(f"Esecuzione query {query_num}...")

    for i in range(31):
        print(f"Iterazione {i + 1}... ", end="")
        start_time = time.perf_counter()
        cursor = connection.cursor()
        cursor.execute(query)
        if i == 0:  # Stampa il risultato solo per la prima iterazione
            print("Risultato della prima esecuzione:")
            for row in cursor.fetchall():
                print(row)
        cursor.close()
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        times.append(execution_time)
        print(f"Completato in {execution_time:.6f} secondi.")

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Run", "Execution Time"])
        for i, exec_time in enumerate(times):
            writer.writerow([i + 1, exec_time])

        # Calcola e salva la media delle esecuzioni (escludendo la prima)
        average_time = sum(times[1:]) / (len(times) - 1)
        writer.writerow(["Media", average_time])

    print(f"Query {query_num} completata. Media tempo di esecuzione: {average_time:.6f} secondi.\n")

# Esegui le query una alla volta e salva i tempi in file CSV separati
for i, query in enumerate(queries):
    execute_query(query, i + 1)

print("Script completato. I tempi di esecuzione sono stati salvati nei file CSV.")

# Chiudi la connessione al termine
connection.close()
