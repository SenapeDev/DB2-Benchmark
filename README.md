# Benchmark database NoSQL
Progetto Database NoSQL - Università degli Studi di Messina

- **Caso di studio**: Identificazione e verifica degli UBO (Ultimate Beneficial Owner)
- **Database utilizzati**: Oracle SQL Developer, Neo4j

## Struttura repository

### Data
All'interno della cartella *data* vengono salvati i dataset generati tramite script.
### Results
All'interno della cartella *results* vengono salvati i risultati dei benchmark per ciascun database. In particolare:
- le cartelle `neo4j` e `oracle` contengono i risultati di esecuzione delle query per ciascun dataset utilizzato (25%, 50%, 75%, 100%).
- Il foglio di calcolo `Tests DB2.xlsx` contiene tutti i risultati e i relativi grafici.
### Scripts
All'interno della cartella *scripts* si trovano gli script, sviluppati in Python, utilizzati per la creazione dei dati e l'interazione con i database. In particolare:
- `data_generator.py`, utilizzato per generare i dataset tramite la libreria `Faker`.
- `data_reducer.py`, utilizzato per creare, a partire da dataset precedentemente generati, le versioni 25%, 50%, 75% e 100% del dataset originale.
- `query-neo4j.py`, utilizzato per effettuare le query con il database Neo4j. Per ciascuna query viene generato un file CSV differente, all'interno del quale vengono salvati i tempi di esecuzione per ciascuna iterazione.
- `query-oracledb.py`, utilizzato per effettuare le query con il database Oracle SQL Developer. Per ciascuna query viene generato un file CSV differente, all'interno del quale vengono salvati i tempi di esecuzione per ciascuna iterazione.
