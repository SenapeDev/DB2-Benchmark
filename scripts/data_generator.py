import csv
import random
from faker import Faker
import threading

fake = Faker()

NUM_PERSONS = 30000
NUM_COMPANIES = 5000
NUM_ACCOUNTS = 30000
NUM_TRANSACTIONS = 80000

persons = []
companies = []
accounts = []
transactions = []
directors = []
shareholders = []

def generate_persons(num):
    for _ in range(num):
        persons.append({
            "id": fake.uuid4(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            "nationality": fake.country()
        })

def generate_companies(num):
    for _ in range(num):
        companies.append({
            "id": fake.uuid4(),
            "company_name": fake.company(),
            "legal_form": fake.company_suffix(),
            "legal_country": fake.country(),
            "operational_country": fake.country(),
            "opening_date": fake.date_this_century().isoformat()
        })

def generate_accounts(num):
    for person in persons:
        # Ogni persona ha almeno un conto
        num_accounts = 1
        if random.random() < 0.33:
            num_accounts += 1
        if random.random() < 0.33:
            num_accounts += 1
        if random.random() < 0.17:
            num_accounts += 1
        
        for _ in range(num_accounts):
            accounts.append({
                "id": fake.uuid4(),
                "account_number": fake.iban(),
                "balance": round(random.uniform(1000, 1000000), 2),
                "owner_id": person["id"],
                "bank_country": fake.country_code()
            })

def generate_transactions(num):
    for _ in range(num):
        sender = random.choice(accounts)
        receiver = random.choice(accounts)
        transactions.append({
            "id": fake.uuid4(),
            "sender_id": sender["id"],
            "receiver_id": receiver["id"],
            "amount": round(random.uniform(10, 900000), 2),
            "transaction_date": fake.date_this_year().isoformat()
        })

def generate_directors():
    for company in companies:
        num_directors = random.randint(1, 5)
        directors.extend([{
            "person_id": random.choice(persons)["id"],
            "company_id": company["id"],
            "join_date": fake.date_this_decade().isoformat()
        } for _ in range(num_directors)])

def generate_shareholders():
    for company in companies:
        num_shareholders = random.randint(1, 5)
        remaining_percentage = 1.0
        for _ in range(num_shareholders):
            if remaining_percentage <= 0:
                break
            share = round(random.uniform(0.01, remaining_percentage), 2)
            shareholders.append({
                "entity_id": random.choice(persons + companies)["id"],
                "company_id": company["id"],
                "percentage": share
            })
            remaining_percentage -= share

# Salva i dati in file CSV
def save_csv(filename, data, headers):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=',')
        writer.writeheader()
        writer.writerows(data)

# Genera i dati utilizzando il multithreading
threads = [
    threading.Thread(target=generate_persons, args=(NUM_PERSONS,)),
    threading.Thread(target=generate_companies, args=(NUM_COMPANIES,)),
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# A causa della loro dipendenza, genera i conti e le transazioni senza avvalersi del multithreading
generate_accounts(NUM_ACCOUNTS)
generate_transactions(NUM_TRANSACTIONS)

# Genera le relazioni
generate_directors()
generate_shareholders()

# Salva i risultati in file CSV
save_csv("persons.csv", persons, ["id", "first_name", "last_name", "dob", "nationality"])
save_csv("companies.csv", companies, ["id", "company_name", "legal_form", "legal_country", "operational_country", "opening_date"])
save_csv("accounts.csv", accounts, ["id", "account_number", "balance", "owner_id", "bank_country"])
save_csv("transactions.csv", transactions, ["id", "sender_id", "receiver_id", "amount", "transaction_date"])
save_csv("directors.csv", directors, ["person_id", "company_id", "join_date"])
save_csv("shareholders.csv", shareholders, ["entity_id", "company_id", "percentage"])
